import os
import io
import re
import json
import hashlib
import logging
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import joblib

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import docx
except ImportError:
    docx = None

from ..config import settings
from ..models.schemas import ResumeAnalysisResponse

logger = logging.getLogger("novapath.ats")

def _load_all_role_benchmarks() -> Dict[str, Dict[str, Any]]:
    """
    Dynamically loads all versioned role benchmark JSON files from backend/data/roles/.
    Supports canonical role names and aliases without network calls at runtime.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(os.path.dirname(current_dir))
    roles_dir = os.path.join(backend_dir, "data", "roles")

    benchmarks: Dict[str, Dict[str, Any]] = {}

    if os.path.isdir(roles_dir):
        for fname in os.listdir(roles_dir):
            if fname.endswith(".json"):
                fpath = os.path.join(roles_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        role_name = data.get("role")
                        if role_name:
                            # Standardize fields
                            data["good_to_have"] = data.get("bonus_skills", [])
                            benchmarks[role_name] = data
                            # Map aliases
                            for alias in data.get("aliases", []):
                                benchmarks[alias] = data
                except Exception as e:
                    logger.error(f"Error loading role JSON {fname}: {e}")

    if not benchmarks:
        logger.warning(f"No role benchmarks found in {roles_dir}. Please run scripts/generate_role_benchmarks.py")

    return benchmarks

# Global dynamically loaded benchmarks
ROLE_BENCHMARKS = _load_all_role_benchmarks()

class SkillNormalizer:
    """
    Normalizes skill aliases, acronyms, and variations to canonical skill names.
    Examples: 'k8s' -> 'kubernetes', 'ts' -> 'typescript', 'react.js' -> 'react'.
    """
    def __init__(self, benchmarks: Dict[str, Dict[str, Any]]):
        self.global_synonym_map: Dict[str, str] = {}
        self.role_synonym_maps: Dict[str, Dict[str, str]] = {}
        self._build_maps(benchmarks)

    def _build_maps(self, benchmarks: Dict[str, Dict[str, Any]]):
        for role_name, data in benchmarks.items():
            role_map: Dict[str, str] = {}
            synonyms = data.get("skill_synonyms", {})
            for canonical, aliases in synonyms.items():
                c_low = canonical.lower().strip()
                role_map[c_low] = c_low
                self.global_synonym_map[c_low] = c_low
                for alias in aliases:
                    a_low = alias.lower().strip()
                    role_map[a_low] = c_low
                    self.global_synonym_map[a_low] = c_low
            self.role_synonym_maps[role_name] = role_map

    def normalize(self, skill: str, role_name: Optional[str] = None) -> str:
        s_low = skill.lower().strip()
        if role_name and role_name in self.role_synonym_maps:
            if s_low in self.role_synonym_maps[role_name]:
                return self.role_synonym_maps[role_name][s_low]
        return self.global_synonym_map.get(s_low, s_low)

class ATSService:
    def __init__(self):
        self.benchmarks = ROLE_BENCHMARKS
        self.normalizer = SkillNormalizer(self.benchmarks)
        self._model = None
        self._model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "models",
            "ats_role_model.joblib"
        )
        self._load_model()

    def reload_benchmarks(self):
        """Refreshes role definitions from JSON files on disk."""
        global ROLE_BENCHMARKS
        ROLE_BENCHMARKS = _load_all_role_benchmarks()
        self.benchmarks = ROLE_BENCHMARKS
        self.normalizer = SkillNormalizer(self.benchmarks)

    def get_role_profile(self, target_role: str) -> Dict[str, Any]:
        """Fetches role profile or defaults to AI Engineer."""
        if target_role in self.benchmarks:
            return self.benchmarks[target_role]
        # Case-insensitive search
        for k, v in self.benchmarks.items():
            if k.lower() == target_role.lower():
                return v
        # Fallback to AI Engineer or first available
        return self.benchmarks.get("AI Engineer", list(self.benchmarks.values())[0] if self.benchmarks else {})

    def _load_model(self):
        """Loads trained CalibratedClassifierCV/LogisticRegression role-fit pipeline."""
        if os.path.isfile(self._model_path):
            try:
                self._model = joblib.load(self._model_path)
                logger.info(f"Loaded trained ATS role-fit model from {self._model_path}")
            except Exception as e:
                logger.error(f"Failed to load trained model: {e}")
                self._model = None
        else:
            logger.warning(f"ATS model not found at {self._model_path}. Please train via scripts/train_ats_model.py")

    def clean_text_for_model(self, text: str) -> str:
        """Sanitizes text and removes PII matching the training pipeline."""
        if not isinstance(text, str):
            return ""
        text = re.sub(r"https?://\S+|www\.\S+", " ", text)
        text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", " ", text)
        text = re.sub(r"\+?\d[\d -]{8,}\d", " ", text)
        text = re.sub(r"[^\w\s]", " ", text)
        return re.sub(r"\s+", " ", text).strip().lower()

    def extract_text_from_file(self, file_bytes: bytes, filename: str) -> str:
        """
        Robustly extracts readable text from PDF, DOCX, or TXT.
        Handles scanned/empty PDFs, DOCX, size limits, and non-English text.
        """
        max_size = 5 * 1024 * 1024
        if len(file_bytes) > max_size:
            raise ValueError(f"File size ({len(file_bytes) / 1024 / 1024:.2f} MB) exceeds maximum limit of 5 MB.")

        if len(file_bytes) == 0:
            raise ValueError("The uploaded file is empty (0 bytes).")

        fname = filename.lower()
        extracted_text = ""

        # 1. PDF Extraction
        if fname.endswith(".pdf"):
            if pypdf is None:
                raise RuntimeError("pypdf library is required for PDF parsing.")
            try:
                reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"
                    # Capture hyperlink annotation URLs (e.g. Portfolio, GitHub, Play Store, Figma links)
                    try:
                        if "/Annots" in page:
                            annots = page["/Annots"]
                            if annots:
                                for annot in annots:
                                    annot_obj = annot.get_object() if hasattr(annot, "get_object") else annot
                                    if annot_obj and annot_obj.get("/Subtype") == "/Link":
                                        action = annot_obj.get("/A")
                                        if action:
                                            action_obj = action.get_object() if hasattr(action, "get_object") else action
                                            uri = action_obj.get("/URI")
                                            if uri:
                                                uri_str = str(uri).strip()
                                                if not uri_str.lower().startswith(("mailto:", "tel:")):
                                                    extracted_text += f"\n{uri_str}\n"
                    except Exception as annot_err:
                        logger.debug(f"Could not parse annotations from page: {annot_err}")
            except Exception as e:
                raise ValueError(f"Unable to read PDF file format: {str(e)}")

            if len(extracted_text.strip()) < 40:
                raise ValueError(
                    "This PDF appears to be a scanned image or contains no readable text layer. "
                    "Please upload a text-searchable PDF or DOCX file."
                )

        # 2. DOCX Extraction
        elif fname.endswith(".docx"):
            if docx is None:
                raise RuntimeError("python-docx library is required for DOCX parsing.")
            try:
                doc = docx.Document(io.BytesIO(file_bytes))
                paragraphs = [p.text for p in doc.paragraphs if p.text]
                for table in doc.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            if cell.text:
                                paragraphs.append(cell.text)
                extracted_text = "\n".join(paragraphs)
            except Exception as e:
                raise ValueError(f"Unable to read DOCX file: {str(e)}")

            if len(extracted_text.strip()) < 40:
                raise ValueError("The DOCX file contains insufficient extractable text.")

        # 3. Plain Text Extraction
        elif fname.endswith(".txt"):
            try:
                extracted_text = file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                extracted_text = file_bytes.decode("latin-1", errors="replace")
        else:
            raise ValueError(f"Unsupported file format: {filename}. Supported formats are .pdf, .docx, and .txt.")

        # 4. Non-English and Quality Robustness Checks
        words = re.findall(r"[a-zA-Z]{2,}", extracted_text)
        if len(words) < 25:
            raise ValueError(
                "Document contains insufficient readable English words (fewer than 25 words detected). "
                "If your resume is a scanned PDF or photo without selectable text, please use the 'Paste Text' tab to paste your resume text directly."
            )

        return extracted_text

    def _calibrate_role_fit_probability(self, prob: float) -> float:
        """
        Calibrates multi-class posterior probability (0.0 to 1.0 across 16 roles)
        into a smooth continuous score (0.0 to 98.5) without artificial saturation at 100.0.
        Discriminates between:
        - Low/irrelevant fit: ~0-15%
        - Emerging/weak fit: ~15-50%
        - Moderate fit: ~50-70%
        - Good fit: ~70-80%
        - Strong fit: ~80-90%
        - Exceptional/Near-perfect: ~90-98.5%
        """
        p = max(0.0, min(1.0, float(prob)))
        if p <= 0.0625:
            # Below 1/16 random chance
            score = (p / 0.0625) * 15.0
        elif p <= 0.20:
            score = 15.0 + ((p - 0.0625) / (0.20 - 0.0625)) * 35.0
        elif p <= 0.45:
            score = 50.0 + ((p - 0.20) / (0.45 - 0.20)) * 30.0
        elif p <= 0.70:
            score = 80.0 + ((p - 0.45) / (0.70 - 0.45)) * 10.0
        else:
            score = 90.0 + ((p - 0.70) / (1.00 - 0.70)) * 8.5
        return round(score, 1)

    def _calculate_ml_role_fit(self, cleaned_text: str, target_role: str) -> Tuple[float, List[Dict[str, Any]], str]:
        """
        Computes 40% ML role-fit probability and top contributing features.
        Supports direct multi-class 16-role prediction and fallback domain class maps.
        """
        role_profile = self.get_role_profile(target_role)
        canonical_role = role_profile.get("role", target_role)
        target_classes_map = role_profile.get("model_classes", {canonical_role: 1.0})

        if not self._model:
            return 80.0, [], "Model offline fallback"

        try:
            classes = list(self._model.classes_)
            probas = self._model.predict_proba([cleaned_text])[0]
            predicted_class = classes[int(np.argmax(probas))]

            # Direct class match if model trained on all 16 roles
            if canonical_role in classes:
                role_idx = classes.index(canonical_role)
                role_prob = float(probas[role_idx])
                role_fit_score = self._calibrate_role_fit_probability(role_prob)
                target_idx = role_idx
            else:
                # Cumulative probability across mapped domain classes
                domain_prob = sum(float(probas[classes.index(cls_name)]) for cls_name in target_classes_map.keys() if cls_name in classes)
                role_fit_score = self._calibrate_role_fit_probability(domain_prob)
                primary_class = list(target_classes_map.keys())[0]
                target_idx = classes.index(primary_class) if primary_class in classes else 0

            # Explainability: Top contributing features
            top_features: List[Dict[str, Any]] = []
            tfidf = self._model.named_steps["tfidf"]
            clf = self._model.named_steps["clf"]
            feature_names = tfidf.get_feature_names_out()
            vec = tfidf.transform([cleaned_text])

            # Extract model coefficients (LogisticRegression or CalibratedClassifierCV)
            if hasattr(clf, "coef_"):
                coefs = clf.coef_[target_idx]
            elif hasattr(clf, "calibrated_classifiers_"):
                coefs = np.mean([c.estimator.coef_[target_idx] for c in clf.calibrated_classifiers_], axis=0)
            else:
                coefs = None

            if coefs is not None:
                contributions = vec.toarray()[0] * coefs
                pos_indices = np.where(contributions > 0.001)[0]
                if len(pos_indices) > 0:
                    sorted_pos = pos_indices[np.argsort(contributions[pos_indices])[::-1]]
                    for i in sorted_pos[:8]:
                        top_features.append({
                            "feature": str(feature_names[i]),
                            "weight": round(float(contributions[i]), 4)
                        })

            return round(role_fit_score, 1), top_features, predicted_class

        except Exception as e:
            logger.error(f"Error computing ML role fit: {e}")
            return 75.0, [], "Error"

    def _detect_candidate_seniority(self, text_lower: str) -> str:
        """
        Detects candidate experience tier: 'fresher', 'mid', or 'senior'
        based on titles, years of experience expressions, education dates, and language.
        """
        senior_patterns = [
            r"\b(senior|sr\.|lead|staff|principal|director|head of|architect)\b",
            r"\b([6-9]|[1-9]\d)\+?\s*years?(?:\s+of)?\s+(?:experience|hands[- ]on)\b",
            r"\b(6|7|8|9|10|12|15)\+?\s*years\b"
        ]
        mid_patterns = [
            r"\b([2-5])\+?\s*years?(?:\s+of)?\s+(?:experience|hands[- ]on)\b",
            r"\b(mid[- ]level|intermediate)\b",
            r"\b([2-5])\s*years\b"
        ]
        fresher_patterns = [
            r"\b(intern|internship|fresher|entry[- ]level|junior|jr\.|trainee|apprentice)\b",
            r"\b(recent\s+(?:college\s+)?graduate|class of 202[4-6]|(?:bachelor'?s?|b\.?s\.?|b\.?a\.?|b\.?tech)\s*(?:degree)?\s*(?:in)?\s*[a-z\s]+202[4-6])\b",
            r"\b(coursework|academic projects|capstone project)\b",
            r"\b(0|1)\s*years?(?:\s+of)?\s+(?:experience|hands[- ]on)\b"
        ]

        has_senior_exp = bool(re.search(r"\b([6-9]|[1-9]\d)\+?\s*years?(?:\s+of)?\s+(?:experience|hands[- ]on)\b", text_lower))
        has_mid_exp = bool(re.search(r"\b([2-5])\+?\s*years?(?:\s+of)?\s+(?:experience|hands[- ]on)\b", text_lower))
        has_fresher_exp = bool(re.search(r"\b(0|1)\s*years?(?:\s+of)?\s+(?:experience|hands[- ]on)\b", text_lower))

        senior_score = sum(len(re.findall(p, text_lower)) for p in senior_patterns)
        mid_score = sum(len(re.findall(p, text_lower)) for p in mid_patterns)
        fresher_score = sum(len(re.findall(p, text_lower)) for p in fresher_patterns)

        if has_senior_exp or (senior_score >= 2 and senior_score > (fresher_score + mid_score)):
            return "senior"
        if has_mid_exp or (mid_score >= 1 and mid_score >= fresher_score):
            return "mid"
        if has_fresher_exp or fresher_score >= 2 or (fresher_score >= 1 and senior_score == 0 and mid_score == 0):
            return "fresher"
        if senior_score >= 1 and mid_score == 0 and fresher_score == 0:
            return "senior"
        return "mid"

    def _calculate_keyword_coverage(self, text_lower: str, target_role: str) -> Tuple[float, List[str], List[str], List[str], List[str], str]:
        """
        Computes 25% keyword and skill coverage with level-aware scoring against level_expectations.
        Ensures a strong fresher is evaluated on fresher expectations rather than penalized for missing senior skills.
        Returns: keyword_score, matched_critical, missing_critical, missing_bonus, extracted_all, detected_seniority
        """
        role_profile = self.get_role_profile(target_role)
        critical_skills = [s.lower() for s in role_profile.get("critical_skills", [])]
        bonus_skills = [s.lower() for s in role_profile.get("bonus_skills", role_profile.get("good_to_have", []))]
        synonyms_dict = role_profile.get("skill_synonyms", {})
        level_exp = role_profile.get("level_expectations", {})

        matched_canonical_set = set()

        # Check all critical and bonus skills with synonyms
        all_skills = list(set(critical_skills + bonus_skills))
        for canonical in all_skills:
            aliases = [canonical] + synonyms_dict.get(canonical, [])
            escaped = [re.escape(a) for a in aliases if len(a.strip()) > 0]
            if not escaped:
                continue
            pattern = r"\b(" + "|".join(escaped) + r")\b"
            if re.search(pattern, text_lower):
                matched_canonical_set.add(canonical)
            elif len(canonical) > 6 and canonical in text_lower:
                matched_canonical_set.add(canonical)

        matched_critical = [s for s in critical_skills if s in matched_canonical_set]
        missing_critical = [s for s in critical_skills if s not in matched_canonical_set]

        matched_bonus = [s for s in bonus_skills if s in matched_canonical_set]
        missing_bonus = [s for s in bonus_skills if s not in matched_canonical_set]

        # Detect candidate seniority level
        detected_level = self._detect_candidate_seniority(text_lower)
        expected_level_skills = [
            s.lower() for s in level_exp.get(detected_level, {}).get("expected_skills", [])
        ]

        crit_ratio = len(matched_critical) / max(1, len(critical_skills))
        bonus_ratio = len(matched_bonus) / max(1, len(bonus_skills))

        # Compute raw critical keyword coverage (acts as an inviolable baseline floor)
        raw_kw = min(100.0, max(0.0, (crit_ratio * 85.0) + (bonus_ratio * 15.0)))

        if expected_level_skills:
            if detected_level == "fresher":
                # Fresher: evaluated primarily on core entry-level expectations (70%),
                # overall critical skills (20%), and bonus skills (10%).
                # Extra skills beyond fresher expectations provide booster points.
                matched_level = [s for s in expected_level_skills if s in matched_canonical_set]
                level_ratio = len(matched_level) / max(1, len(expected_level_skills))
                base_kw = (level_ratio * 70.0) + (crit_ratio * 20.0) + (bonus_ratio * 10.0)
                extra_skills = max(0, len(matched_critical) - len(matched_level))
                booster = min(10.0, extra_skills * 2.5)
                keyword_score = min(100.0, max(raw_kw, base_kw + booster))

            elif detected_level == "mid":
                # Mid: expected to master foundational + mid competencies cumulatively
                fresher_skills = [s.lower() for s in level_exp.get("fresher", {}).get("expected_skills", [])]
                mid_skills = [s.lower() for s in level_exp.get("mid", {}).get("expected_skills", [])]
                cumulative_mid = list(set(fresher_skills + mid_skills)) if (fresher_skills or mid_skills) else expected_level_skills
                matched_mid = [s for s in cumulative_mid if s in matched_canonical_set]
                mid_ratio = len(matched_mid) / max(1, len(cumulative_mid))

                base_kw = (crit_ratio * 55.0) + (mid_ratio * 35.0) + (bonus_ratio * 10.0)
                extra_skills = max(0, len(matched_critical) - len(matched_mid))
                booster = min(10.0, extra_skills * 2.0)
                keyword_score = min(100.0, max(raw_kw, base_kw + booster))

            else:  # senior
                # Senior: expected to cover broad critical skills, cumulative competency, plus senior architecture
                fresher_skills = [s.lower() for s in level_exp.get("fresher", {}).get("expected_skills", [])]
                mid_skills = [s.lower() for s in level_exp.get("mid", {}).get("expected_skills", [])]
                senior_skills = [s.lower() for s in level_exp.get("senior", {}).get("expected_skills", [])]
                all_expected = list(set(fresher_skills + mid_skills + senior_skills)) if (fresher_skills or mid_skills or senior_skills) else critical_skills

                matched_all = [s for s in all_expected if s in matched_canonical_set]
                exp_ratio = len(matched_all) / max(1, len(all_expected))
                matched_senior = [s for s in senior_skills if s in matched_canonical_set]
                senior_ratio = len(matched_senior) / max(1, len(senior_skills)) if senior_skills else crit_ratio

                base_kw = (crit_ratio * 60.0) + (exp_ratio * 25.0) + (senior_ratio * 10.0) + (bonus_ratio * 5.0)
                booster = min(10.0, max(0.0, (crit_ratio - 0.70) * 33.3)) if crit_ratio >= 0.70 else 0.0
                keyword_score = min(100.0, max(raw_kw, base_kw + booster))
        else:
            keyword_score = raw_kw

        # Format with titlecase
        def fmt(lst):
            return [s.title() if len(s) > 3 else s.upper() for s in lst]

        fmt_matched = fmt(list(matched_canonical_set))
        fmt_missing_crit = fmt(missing_critical)
        fmt_missing_bonus = fmt(missing_bonus)
        fmt_extracted = fmt(list(matched_canonical_set))

        return round(keyword_score, 1), fmt_matched, fmt_missing_crit, fmt_missing_bonus, fmt_extracted, detected_level

    def _calculate_section_completeness(self, text_lower: str, target_role: str) -> Tuple[float, List[str], List[str], List[str]]:
        """
        Computes 15% section completeness across standard sections + role-specific rules.
        (e.g., Portfolio link is strictly verified for UI/UX Designer and Mobile App Developer).
        """
        role_profile = self.get_role_profile(target_role)
        rules = role_profile.get("role_specific_rules", {})
        portfolio_required = rules.get("portfolio_required", False)

        section_patterns = {
            "Contact Info": r"(\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b|\+?\d[\d -]{8,}\d|github\.com|linkedin\.com)",
            "Professional Summary": r"\b(summary|objective|profile|about me|professional summary)\b",
            "Technical Skills": r"\b(skills|technologies|technical competencies|proficiencies|tech stack)\b",
            "Work Experience": r"\b(experience|employment|work history|internship|projects experience)\b",
            "Education": r"\b(education|degree|bachelor|master|b\.tech|university|college|gpa|cgpa)\b",
            "Projects": r"\b(projects|personal projects|open source|hackathon|portfolio)\b"
        }

        # Role-specific rule: Portfolio link required
        portfolio_notes = []
        if portfolio_required:
            section_patterns["Portfolio / Live Demo Link"] = r"(github\.com|gitlab\.com|behance\.net|dribbble\.com|figma\.com|testflight|play\.google\.com|apps\.apple\.com|vercel\.app|netlify\.app|expo\.dev|portfolio|personal website|case study)"

        present_sections = []
        missing_sections = []

        for section_name, pattern in section_patterns.items():
            if re.search(pattern, text_lower):
                present_sections.append(section_name)
            else:
                missing_sections.append(section_name)

        if portfolio_required and "Portfolio / Live Demo Link" in missing_sections:
            portfolio_notes.append(f"A verifiable portfolio link (GitHub, Play Store, TestFlight, Figma, Behance) is required for {role_profile.get('role', target_role)} candidates.")

        section_score = min(100.0, max(0.0, (len(present_sections) / len(section_patterns)) * 100.0))
        return round(section_score, 1), present_sections, missing_sections, portfolio_notes

    def _calculate_formatting_parsability(self, text: str) -> Tuple[float, List[str]]:
        """Computes 10% formatting and parsability checks."""
        words = text.split()
        word_count = len(words)
        bullet_count = len(re.findall(r"(?:^|\n)\s*[-•*]\s+", text)) + len(re.findall(r"(?:^|\n)\s*\d+\.\s+", text))

        notes = []
        score = 100.0

        if word_count < 150:
            score -= 35.0
            notes.append("Resume length is very brief (under 150 words).")
        elif word_count < 250:
            score -= 15.0
            notes.append("Resume could benefit from more detailed project context (under 250 words).")
        elif word_count > 1400:
            score -= 15.0
            notes.append("Resume length is excessive (over 1,400 words); keep to 1-2 pages.")

        if bullet_count == 0:
            score -= 30.0
            notes.append("No bullet points detected; use bulleted lists for experience and projects.")
        elif bullet_count < 4:
            score -= 15.0
            notes.append("Few bullet points detected; structure achievements with clear bullet points.")

        lines = [l for l in text.split("\n") if l.strip()]
        if len(lines) < 8:
            score -= 20.0
            notes.append("Text appears monolithic; add clear line spacing between sections.")

        score = min(100.0, max(20.0, score))
        return round(score, 1), notes

    def _calculate_quantified_impact(self, text_lower: str, target_role: str) -> Tuple[float, int, int]:
        """Computes 10% quantified-impact bullets (numbers, percentages, outcomes)."""
        role_profile = self.get_role_profile(target_role)

        metric_pattern = r"(\b\d+(\.\d+)?(%|x|ms|s|m|gb|tb|\+)\b|\$\d+|\b\d{1,3}(?:,\d{3})+\b)"
        metrics = re.findall(metric_pattern, text_lower)
        metric_count = len(metrics)

        action_verbs = role_profile.get("action_verbs", ["engineered", "built", "designed", "optimized", "implemented"])
        action_verb_count = 0
        for verb in action_verbs:
            matches = re.findall(r"\b" + re.escape(verb.lower()) + r"\b", text_lower)
            action_verb_count += len(matches)

        metric_points = min(60.0, (metric_count / 5.0) * 60.0)
        verb_points = min(40.0, (action_verb_count / 4.0) * 40.0)
        impact_score = min(100.0, max(0.0, metric_points + verb_points))

        return round(impact_score, 1), metric_count, action_verb_count

    def _generate_personalized_roadmap(
        self,
        target_role: str,
        missing_critical: List[str],
        missing_bonus: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Synthesizes a personalized roadmap of the top 5 missing topics in learning order
        from the authoritative role JSON benchmark.
        """
        role_profile = self.get_role_profile(target_role)
        roadmap_steps = role_profile.get("roadmap", [])
        if not roadmap_steps:
            return []

        missing_crit_set = {s.lower() for s in missing_critical}
        missing_bonus_set = {s.lower() for s in missing_bonus}
        all_missing = missing_crit_set.union(missing_bonus_set)

        prioritized_topics = []

        for step in roadmap_steps:
            step_skills = [s.lower() for s in step.get("skills", [])]
            step_missing = [s for s in step_skills if s in all_missing]

            has_critical = any(s in missing_crit_set for s in step_skills)

            # If any skill in the topic is missing, include it in the personalized roadmap
            if step_missing or not set(step_skills).isdisjoint(all_missing):
                prioritized_topics.append({
                    "step": step.get("step", len(prioritized_topics) + 1),
                    "topic": step.get("topic", "Target Skill Module"),
                    "missing_skills": [s.title() if len(s) > 3 else s.upper() for s in (step_missing if step_missing else step_skills)],
                    "description": step.get("description", ""),
                    "resources": step.get("resources", []),
                    "priority": "Critical" if has_critical else "Recommended"
                })

        # If candidate already has all roadmap skills, provide top advanced topics
        if not prioritized_topics:
            for step in roadmap_steps[-3:]:
                prioritized_topics.append({
                    "step": step.get("step", 1),
                    "topic": step.get("topic", ""),
                    "missing_skills": [s.title() for s in step.get("skills", [])],
                    "description": step.get("description", ""),
                    "resources": step.get("resources", []),
                    "priority": "Mastery"
                })

        # Maintain learning order (sorted by step) and take top 5
        prioritized_topics.sort(key=lambda x: x["step"])
        return prioritized_topics[:5]

    def analyze_resume_text(self, text: str, target_role: str = "AI Engineer") -> ResumeAnalysisResponse:
        """
        Executes full deterministic ATS analysis pipeline:
        40% ML role-fit probability for target role
        25% keyword/skill coverage (normalized via SkillNormalizer)
        15% section completeness (with role-specific rules)
        10% formatting/parsability
        10% quantified-impact
        Returns matched skills, missing critical, missing bonus, and personalized roadmap.
        """
        role_profile = self.get_role_profile(target_role)
        canonical_role_name = role_profile.get("role", target_role)

        text_lower = text.lower()
        cleaned_text = self.clean_text_for_model(text)
        text_hash = hashlib.sha256(cleaned_text.encode("utf-8")).hexdigest()

        # 1. Component calculations
        role_fit_score, top_features, predicted_class = self._calculate_ml_role_fit(cleaned_text, canonical_role_name)
        keyword_score, matched_skills, missing_critical, missing_bonus, extracted_skills, detected_level = self._calculate_keyword_coverage(text_lower, canonical_role_name)
        section_score, present_sections, missing_sections, portfolio_notes = self._calculate_section_completeness(text_lower, canonical_role_name)
        format_score, format_notes = self._calculate_formatting_parsability(text)
        impact_score, metric_count, action_verb_count = self._calculate_quantified_impact(text_lower, canonical_role_name)

        # Limited validation check for roles without real Kaggle resumes
        roles_with_limited_val = {
            "AI Engineer",
            "Full Stack Developer",
            "Data Analyst",
            "Mobile App Developer",
            "SRE",
            "UI/UX Designer",
            "Frontend Developer"
        }
        is_limited = canonical_role_name in roles_with_limited_val
        val_notes = (
            f"Validated on authoritative domain standards (roadmap.sh, O*NET) and synthetic benchmarks due to lack of public open-source resumes for '{canonical_role_name}'."
            if is_limited else None
        )

        # 2. Documented Weighted Blend (Scoring weights stay strictly unchanged)
        w_role = settings.ATS_WEIGHT_ROLE_FIT              # 0.40
        w_key = settings.ATS_WEIGHT_KEYWORD_COVERAGE       # 0.25
        w_sec = settings.ATS_WEIGHT_SECTION_COMPLETENESS   # 0.15
        w_fmt = settings.ATS_WEIGHT_FORMATTING             # 0.10
        w_imp = settings.ATS_WEIGHT_QUANTIFIED_IMPACT      # 0.10

        composite_score = (
            (role_fit_score * w_role) +
            (keyword_score * w_key) +
            (section_score * w_sec) +
            (format_score * w_fmt) +
            (impact_score * w_imp)
        )
        ats_score = int(round(composite_score))
        ats_score = max(0, min(100, ats_score))

        # Combined missing skills for backward compatibility
        all_missing_skills = missing_critical + missing_bonus

        # 3. Personalized Roadmap (Top 5 missing topics in learning order)
        personalized_roadmap = self._generate_personalized_roadmap(canonical_role_name, missing_critical, missing_bonus)

        # 4. Deductions & Plain-Language Reasons
        deductions: List[Dict[str, Any]] = []

        if keyword_score < 90:
            lost = round((100.0 - keyword_score) * w_key, 1)
            missing_preview = ", ".join(missing_critical[:3]) if missing_critical else "advanced tooling"
            deductions.append({
                "category": "Keyword Coverage",
                "lost_points": lost,
                "reason": f"Missing critical technical competencies for {canonical_role_name}: {missing_preview}."
            })

        if role_fit_score < 85:
            lost = round((100.0 - role_fit_score) * w_role, 1)
            deductions.append({
                "category": "Role-Fit Probability",
                "lost_points": lost,
                "reason": f"ML model role alignment is {role_fit_score:.1f}% (closest predicted domain: {predicted_class})."
            })

        if missing_sections:
            lost = round((100.0 - section_score) * w_sec, 1)
            reason_str = f"Missing standard sections: {', '.join(missing_sections)}."
            if portfolio_notes:
                reason_str += f" {' '.join(portfolio_notes)}"
            deductions.append({
                "category": "Section Completeness",
                "lost_points": lost,
                "reason": reason_str
            })

        if format_score < 90:
            lost = round((100.0 - format_score) * w_fmt, 1)
            deductions.append({
                "category": "Formatting & Parsability",
                "lost_points": lost,
                "reason": "; ".join(format_notes) if format_notes else "Layout and bullet formatting can be tightened."
            })

        if impact_score < 80:
            lost = round((100.0 - impact_score) * w_imp, 1)
            deductions.append({
                "category": "Quantified Impact",
                "lost_points": lost,
                "reason": f"Only {metric_count} metric benchmarks detected (target: >= 5 measurable outcomes like %, latency, throughput)."
            })

        # 5. Actionable Recommendations
        actionable_recommendations = []
        if missing_critical:
            actionable_recommendations.append({
                "category": "Skill Gap",
                "priority": "High",
                "title": f"Add proof of competency in {missing_critical[0]}",
                "description": f"Recruiter search filters for '{canonical_role_name}' prioritize candidates with hands-on projects demonstrating {', '.join(missing_critical[:3])}."
            })
        if portfolio_notes:
            actionable_recommendations.append({
                "category": "Portfolio Link",
                "priority": "High",
                "title": "Add a verifiable portfolio / live demo link",
                "description": portfolio_notes[0]
            })
        if metric_count < 5:
            actionable_recommendations.append({
                "category": "Impact Metrics",
                "priority": "Medium",
                "title": "Quantify outcomes with the XYZ formula",
                "description": "Structure bullet points as: 'Accomplished [X] as measured by [Y], by doing [Z]'. Example: 'Reduced inference latency by 35%'."
            })
        if action_verb_count < 5:
            actionable_recommendations.append({
                "category": "Action Verbs",
                "priority": "Medium",
                "title": "Lead with high-impact engineering verbs",
                "description": f"Start experience bullets with active verbs tailored to {canonical_role_name} like {', '.join(role_profile.get('action_verbs', ['architected', 'developed'])[:3])}."
            })

        # 6. Component Breakdown Structure
        score_breakdown = {
            "role_fit": {
                "name": "ML Role-Fit Probability",
                "score": round(role_fit_score, 1),
                "weight_percent": int(w_role * 100),
                "weighted_points": round(role_fit_score * w_role, 1),
                "description": f"Machine Learning classifier likelihood of matching {canonical_role_name} profile"
            },
            "keyword_coverage": {
                "name": "Keyword & Skill Coverage",
                "score": round(keyword_score, 1),
                "weight_percent": int(w_key * 100),
                "weighted_points": round(keyword_score * w_key, 1),
                "description": f"Taxonomy match against {canonical_role_name} competencies ({len(matched_skills)} matched, {len(missing_critical)} missing critical)"
            },
            "section_completeness": {
                "name": "Section Completeness",
                "score": round(section_score, 1),
                "weight_percent": int(w_sec * 100),
                "weighted_points": round(section_score * w_sec, 1),
                "description": "Standard sections present: Contact, Summary, Skills, Experience, Education, Projects" + (" + Portfolio Link" if portfolio_notes else "")
            },
            "formatting_parsability": {
                "name": "Formatting & Parsability",
                "score": round(format_score, 1),
                "weight_percent": int(w_fmt * 100),
                "weighted_points": round(format_score * w_fmt, 1),
                "description": "Word counts, bullet points, clean structure without unparsable blocks"
            },
            "quantified_impact": {
                "name": "Quantified Impact",
                "score": round(impact_score, 1),
                "weight_percent": int(w_imp * 100),
                "weighted_points": round(impact_score * w_imp, 1),
                "description": "Measurable benchmarks: %, multipliers, latency, and business outcomes"
            }
        }

        # 7. Concise Summary Critique
        critique = (
            f"ATS Compatibility Score (estimate): {ats_score}/100 for '{canonical_role_name}'. "
            f"Role-fit probability is {role_fit_score:.1f}% with {len(matched_skills)} recognized competencies. "
            f"To reach the top applicant bracket, incorporate missing critical skills ({', '.join(missing_critical[:3]) if missing_critical else 'advanced tooling'}) "
            f"and follow the personalized learning roadmap."
        )

        return ResumeAnalysisResponse(
            ats_score=ats_score,
            formatting_score=int(round(format_score)),
            skills_match_score=int(round(keyword_score)),
            impact_score=int(round(impact_score)),
            role_fit_score=role_fit_score,
            section_score=section_score,
            extracted_skills=extracted_skills,
            missing_skills=all_missing_skills,
            missing_critical_skills=missing_critical,
            missing_bonus_skills=missing_bonus,
            matched_skills=matched_skills,
            personalized_roadmap=personalized_roadmap,
            action_verb_count=action_verb_count,
            quantifiable_metrics_count=metric_count,
            summary_critique=critique,
            actionable_recommendations=actionable_recommendations,
            score_breakdown=score_breakdown,
            top_contributing_features=top_features,
            deductions=deductions,
            target_role=canonical_role_name,
            raw_text_hash=text_hash,
            limited_validation=is_limited,
            validation_notes=val_notes,
            detected_seniority=detected_level
        )

ats_service = ATSService()

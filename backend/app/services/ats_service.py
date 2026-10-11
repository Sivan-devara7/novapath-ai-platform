import os
import io
import re
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

# Taxonomy for target roles and expected skills
ROLE_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "AI Engineer": {
        "critical_skills": [
            "python", "pytorch", "transformers", "vector database", "rag",
            "langchain", "docker", "fastapi", "cuda", "model evaluation",
            "mlops", "fine-tuning"
        ],
        "good_to_have": ["kubernetes", "tensorrt", "aws", "git", "ci/cd", "triton", "scikit-learn", "numpy", "pandas"],
        "action_verbs": ["fine-tuned", "architected", "deployed", "optimized", "benchmarked", "accelerated", "implemented", "trained"],
        "model_classes": {"Data Science": 0.65, "Python Developer": 0.35}
    },
    "Full Stack Developer": {
        "critical_skills": [
            "typescript", "react", "node.js", "next.js", "postgresql",
            "tailwind css", "rest api", "graphql", "docker", "git"
        ],
        "good_to_have": ["redis", "aws", "jest", "ci/cd", "microservices", "mongodb", "javascript", "html", "css"],
        "action_verbs": ["built", "scaled", "designed", "integrated", "refactored", "shipped", "developed", "engineered"],
        "model_classes": {"Web Designing": 0.50, "Python Developer": 0.25, "Java Developer": 0.25}
    },
    "Cloud & DevOps Engineer": {
        "critical_skills": [
            "kubernetes", "docker", "terraform", "aws", "ci/cd",
            "linux", "prometheus", "grafana", "python", "bash"
        ],
        "good_to_have": ["argo cd", "helm", "istio", "ansible", "gcp", "git", "cloudformation", "jenkins"],
        "action_verbs": ["automated", "orchestrated", "provisioned", "migrated", "hardened", "monitored", "deployed", "configured"],
        "model_classes": {"DevOps Engineer": 0.60, "Network Security Engineer": 0.20, "Database": 0.20}
    },
    "Data Engineer": {
        "critical_skills": [
            "python", "sql", "spark", "kafka", "airflow",
            "snowflake", "data modeling", "etl", "docker", "dbt"
        ],
        "good_to_have": ["aws", "bigquery", "flink", "hadoop", "postgresql", "git", "scala", "databricks"],
        "action_verbs": ["architected", "orchestrated", "streamed", "transformed", "optimized", "pipelined", "ingested", "scaled"],
        "model_classes": {"Database": 0.55, "Data Science": 0.30, "Python Developer": 0.15}
    },
    "Cybersecurity Analyst": {
        "critical_skills": [
            "network security", "threat intelligence", "soc", "siem", "vulnerability assessment",
            "wireshark", "penetration testing", "incident response", "linux", "firewall"
        ],
        "good_to_have": ["owasp", "burp suite", "python", "cryptography", "iam", "cloud security", "mitre att&ck"],
        "action_verbs": ["mitigated", "triaged", "investigated", "hardened", "audited", "defended", "neutralized", "patched"],
        "model_classes": {"Network Security Engineer": 0.70, "DevOps Engineer": 0.20, "Database": 0.10}
    }
}

class ATSService:
    def __init__(self):
        self._model = None
        self._model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "models",
            "ats_role_model.joblib"
        )
        self._load_model()

    def _load_model(self):
        """Loads trained CalibratedClassifierCV/LinearSVC role-fit pipeline."""
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
        # 1. Size Limit Check (5 MB)
        max_size = 5 * 1024 * 1024
        if len(file_bytes) > max_size:
            raise ValueError(f"File size ({len(file_bytes) / 1024 / 1024:.2f} MB) exceeds maximum limit of 5 MB.")

        if len(file_bytes) == 0:
            raise ValueError("The uploaded file is empty (0 bytes).")

        fname = filename.lower()
        extracted_text = ""

        # 2. PDF Extraction
        if fname.endswith(".pdf"):
            if pypdf is None:
                raise RuntimeError("pypdf library is required for PDF parsing.")
            try:
                reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        extracted_text += page_text + "\n"
            except Exception as e:
                raise ValueError(f"Unable to read PDF file format: {str(e)}")

            if len(extracted_text.strip()) < 40:
                raise ValueError(
                    "This PDF appears to be a scanned image or contains no readable text layer. "
                    "Please upload a text-searchable PDF or DOCX file."
                )

        # 3. DOCX Extraction
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

        # 4. Plain Text Extraction
        elif fname.endswith(".txt"):
            try:
                extracted_text = file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                extracted_text = file_bytes.decode("latin-1", errors="replace")
        else:
            raise ValueError(f"Unsupported file format: {filename}. Supported formats are .pdf, .docx, and .txt.")

        # 5. Non-English and Quality Robustness Checks
        words = re.findall(r"[a-zA-Z]{2,}", extracted_text)
        if len(words) < 25:
            raise ValueError(
                "Document contains insufficient readable English words (fewer than 25 words detected). "
                "If your resume is a scanned PDF or photo without selectable text, please use the 'Paste Text' tab to paste your resume text directly."
            )

        return extracted_text

    def _calculate_ml_role_fit(self, cleaned_text: str, target_role: str) -> Tuple[float, List[Dict[str, Any]], str]:
        """
        Computes 40% ML role-fit probability and top contributing features.
        Be honest: Model predicts role-fit probability, not ground-truth ATS score.
        """
        role_profile = ROLE_BENCHMARKS.get(target_role, ROLE_BENCHMARKS["AI Engineer"])
        target_classes_map = role_profile.get("model_classes", {"Data Science": 1.0})

        if not self._model:
            # Fallback if model not loaded
            return 80.0, [], "Model offline fallback"

        try:
            classes = list(self._model.classes_)
            probas = self._model.predict_proba([cleaned_text])[0]
            predicted_class = classes[int(np.argmax(probas))]

            # Compute cumulative probability across target domain classes
            domain_prob = sum(float(probas[classes.index(cls_name)]) for cls_name in target_classes_map.keys() if cls_name in classes)

            # Role fit score on 0-100 scale: 0.75+ cumulative probability represents top-tier domain match
            role_fit_score = min(100.0, max(0.0, (domain_prob / 0.75) * 100.0))
            if predicted_class in target_classes_map and role_fit_score < 70.0:
                role_fit_score = max(role_fit_score, 70.0 + (domain_prob * 30.0))

            # Explainability: Top contributing features
            top_features: List[Dict[str, Any]] = []
            tfidf = self._model.named_steps["tfidf"]
            clf = self._model.named_steps["clf"]
            feature_names = tfidf.get_feature_names_out()
            vec = tfidf.transform([cleaned_text])

            # Get target primary class index
            primary_class = list(target_classes_map.keys())[0]
            if primary_class in classes:
                target_idx = classes.index(primary_class)
                # Average coefficients across calibrated classifiers
                coefs = np.mean([c.estimator.coef_[target_idx] for c in clf.calibrated_classifiers_], axis=0)
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

    def _calculate_keyword_coverage(self, text_lower: str, target_role: str) -> Tuple[float, List[str], List[str], List[str]]:
        """Computes 25% keyword and skill coverage with exact and fuzzy taxonomy matching."""
        role_profile = ROLE_BENCHMARKS.get(target_role, ROLE_BENCHMARKS["AI Engineer"])
        critical_skills = [s.lower() for s in role_profile["critical_skills"]]
        good_to_have = [s.lower() for s in role_profile["good_to_have"]]
        all_tracked = list(set(critical_skills + good_to_have))

        extracted = []
        for skill in all_tracked:
            # Word boundary regex match
            pattern = r"\b" + re.escape(skill) + r"\b"
            if re.search(pattern, text_lower):
                extracted.append(skill)
            elif len(skill) > 5 and skill in text_lower:
                extracted.append(skill)

        matched_critical = [s for s in critical_skills if s in extracted]
        missing_critical = [s for s in critical_skills if s not in extracted]

        # Calculate score: matched critical skills weighted 85%, good-to-have 15%
        crit_ratio = len(matched_critical) / max(1, len(critical_skills))
        good_matched = [s for s in good_to_have if s in extracted]
        good_ratio = len(good_matched) / max(1, len(good_to_have))

        keyword_score = min(100.0, max(0.0, (crit_ratio * 85.0) + (good_ratio * 15.0)))

        fmt_extracted = [s.title() if len(s) > 3 else s.upper() for s in extracted]
        fmt_matched = [s.title() if len(s) > 3 else s.upper() for s in matched_critical]
        fmt_missing = [s.title() if len(s) > 3 else s.upper() for s in missing_critical]

        return round(keyword_score, 1), fmt_matched, fmt_missing, fmt_extracted

    def _calculate_section_completeness(self, text_lower: str) -> Tuple[float, List[str], List[str]]:
        """Computes 15% section completeness across 6 standard sections."""
        section_patterns = {
            "Contact Info": r"(\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b|\+?\d[\d -]{8,}\d|github\.com|linkedin\.com)",
            "Professional Summary": r"\b(summary|objective|profile|about me|professional summary)\b",
            "Technical Skills": r"\b(skills|technologies|technical competencies|proficiencies|tech stack)\b",
            "Work Experience": r"\b(experience|employment|work history|internship|projects experience)\b",
            "Education": r"\b(education|degree|bachelor|master|b\.tech|university|college|gpa|cgpa)\b",
            "Projects": r"\b(projects|personal projects|open source|hackathon|portfolio)\b"
        }

        present_sections = []
        missing_sections = []

        for section_name, pattern in section_patterns.items():
            if re.search(pattern, text_lower):
                present_sections.append(section_name)
            else:
                missing_sections.append(section_name)

        section_score = min(100.0, max(0.0, (len(present_sections) / len(section_patterns)) * 100.0))
        return round(section_score, 1), present_sections, missing_sections

    def _calculate_formatting_parsability(self, text: str) -> Tuple[float, List[str]]:
        """Computes 10% formatting and parsability checks."""
        words = text.split()
        word_count = len(words)
        bullet_count = len(re.findall(r"(?:^|\n)\s*[-•*]\s+", text)) + len(re.findall(r"(?:^|\n)\s*\d+\.\s+", text))

        notes = []
        score = 100.0

        # Word count check (ideal: 250 - 1100 words)
        if word_count < 150:
            score -= 35.0
            notes.append("Resume length is very brief (under 150 words).")
        elif word_count < 250:
            score -= 15.0
            notes.append("Resume could benefit from more detailed project context (under 250 words).")
        elif word_count > 1400:
            score -= 15.0
            notes.append("Resume length is excessive (over 1,400 words); keep to 1-2 pages.")

        # Bullet points check (ideal: >= 5 bullets)
        if bullet_count == 0:
            score -= 30.0
            notes.append("No bullet points detected; use bulleted lists for experience and projects.")
        elif bullet_count < 4:
            score -= 15.0
            notes.append("Few bullet points detected; structure achievements with clear bullet points.")

        # Line break check
        lines = [l for l in text.split("\n") if l.strip()]
        if len(lines) < 8:
            score -= 20.0
            notes.append("Text appears monolithic; add clear line spacing between sections.")

        score = min(100.0, max(20.0, score))
        return round(score, 1), notes

    def _calculate_quantified_impact(self, text_lower: str, target_role: str) -> Tuple[float, int, int]:
        """Computes 10% quantified-impact bullets (numbers, percentages, outcomes)."""
        role_profile = ROLE_BENCHMARKS.get(target_role, ROLE_BENCHMARKS["AI Engineer"])

        # Metric patterns: %, ms, s, x, k, $, numbers with commas
        metric_pattern = r"(\b\d+(\.\d+)?(%|x|ms|s|m|gb|tb|\+)\b|\$\d+|\b\d{1,3}(?:,\d{3})+\b)"
        metrics = re.findall(metric_pattern, text_lower)
        metric_count = len(metrics)

        # Action verbs
        action_verb_count = 0
        for verb in role_profile.get("action_verbs", []):
            matches = re.findall(r"\b" + re.escape(verb) + r"\b", text_lower)
            action_verb_count += len(matches)

        # Score formula: 5+ metrics and 4+ action verbs gives 100%
        metric_points = min(60.0, (metric_count / 5.0) * 60.0)
        verb_points = min(40.0, (action_verb_count / 4.0) * 40.0)
        impact_score = min(100.0, max(0.0, metric_points + verb_points))

        return round(impact_score, 1), metric_count, action_verb_count

    def analyze_resume_text(self, text: str, target_role: str = "AI Engineer") -> ResumeAnalysisResponse:
        """
        Executes full deterministic ATS analysis pipeline:
        40% ML role-fit probability for target role
        25% keyword/skill coverage
        15% section completeness
        10% formatting/parsability
        10% quantified-impact
        """
        text_lower = text.lower()
        cleaned_text = self.clean_text_for_model(text)
        text_hash = hashlib.sha256(cleaned_text.encode("utf-8")).hexdigest()

        # 1. Component calculations
        role_fit_score, top_features, predicted_class = self._calculate_ml_role_fit(cleaned_text, target_role)
        keyword_score, matched_skills, missing_skills, extracted_skills = self._calculate_keyword_coverage(text_lower, target_role)
        section_score, present_sections, missing_sections = self._calculate_section_completeness(text_lower)
        format_score, format_notes = self._calculate_formatting_parsability(text)
        impact_score, metric_count, action_verb_count = self._calculate_quantified_impact(text_lower, target_role)

        # 2. Documented Weighted Blend (from config)
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

        # 3. Deductions & Plain-Language Reasons
        deductions: List[Dict[str, Any]] = []

        if keyword_score < 90:
            lost = round((100.0 - keyword_score) * w_key, 1)
            missing_preview = ", ".join(missing_skills[:3]) if missing_skills else "advanced tools"
            deductions.append({
                "category": "Keyword Coverage",
                "lost_points": lost,
                "reason": f"Missing high-impact skills for {target_role}: {missing_preview}."
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
            deductions.append({
                "category": "Section Completeness",
                "lost_points": lost,
                "reason": f"Standard resume sections missing: {', '.join(missing_sections)}."
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

        # 4. Actionable Recommendations
        actionable_recommendations = []
        if missing_skills:
            actionable_recommendations.append({
                "category": "Skill Gap",
                "priority": "High",
                "title": f"Add proof of competency in {missing_skills[0]}",
                "description": f"Recruiter search filters for '{target_role}' prioritize candidates with hands-on projects demonstrating {', '.join(missing_skills[:3])}."
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
                "description": "Start experience bullets with active engineering verbs like fine-tuned, architected, optimized, or automated."
            })

        # 5. Component Breakdown Structure
        score_breakdown = {
            "role_fit": {
                "name": "ML Role-Fit Probability",
                "score": round(role_fit_score, 1),
                "weight_percent": int(w_role * 100),
                "weighted_points": round(role_fit_score * w_role, 1),
                "description": f"Machine Learning classifier likelihood of matching {target_role} profile"
            },
            "keyword_coverage": {
                "name": "Keyword & Skill Coverage",
                "score": round(keyword_score, 1),
                "weight_percent": int(w_key * 100),
                "weighted_points": round(keyword_score * w_key, 1),
                "description": "Taxonomy match against target industry competencies"
            },
            "section_completeness": {
                "name": "Section Completeness",
                "score": round(section_score, 1),
                "weight_percent": int(w_sec * 100),
                "weighted_points": round(section_score * w_sec, 1),
                "description": "Standard sections present: Contact, Summary, Skills, Experience, Education, Projects"
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

        # 6. Concise Summary Critique
        critique = (
            f"ATS Compatibility Score (estimate): {ats_score}/100 for '{target_role}'. "
            f"Role-fit probability is {role_fit_score:.1f}% with {len(matched_skills)} verified technical competencies. "
            f"To reach the top applicant bracket, incorporate missing critical keywords ({', '.join(missing_skills[:3]) if missing_skills else 'advanced tooling'}) "
            f"and strengthen bullets with quantifiable metrics."
        )

        return ResumeAnalysisResponse(
            ats_score=ats_score,
            formatting_score=int(round(format_score)),
            skills_match_score=int(round(keyword_score)),
            impact_score=int(round(impact_score)),
            role_fit_score=role_fit_score,
            section_score=section_score,
            extracted_skills=extracted_skills,
            missing_skills=missing_skills,
            matched_skills=matched_skills,
            action_verb_count=action_verb_count,
            quantifiable_metrics_count=metric_count,
            summary_critique=critique,
            actionable_recommendations=actionable_recommendations,
            score_breakdown=score_breakdown,
            top_contributing_features=top_features,
            deductions=deductions,
            target_role=target_role,
            raw_text_hash=text_hash
        )

ats_service = ATSService()

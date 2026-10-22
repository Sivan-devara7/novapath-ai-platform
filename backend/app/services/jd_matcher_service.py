"""
JD Matcher Service (Job Description vs Resume Matcher)
Provides tailored resume analysis against specific posted Job Descriptions (JDs).
Zero scraping, zero persistence beyond the request lifecycle.
Deterministic matching using normalized skill taxonomy and local TF-IDF semantic similarity.
"""

import re
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .ats_service import ats_service
from ..models.schemas import (
    JDMatchResponse,
    KeywordGapPlacement,
    ResumeEditSuggestion
)

MUST_HAVE_SECTION_HEADERS = [
    r"(?:basic|minimum|required|core)\s+(?:qualifications|requirements|skills|competencies)",
    r"(?:what\s+you(?:'ll)?\s+(?:need|bring)|requirements|must[- ]haves?|what\s+we(?:'re)?\s+looking\s+for)"
]

NICE_TO_HAVE_SECTION_HEADERS = [
    r"(?:preferred|desired|bonus|additional)\s+(?:qualifications|requirements|skills|competencies)",
    r"(?:nice[- ]to[- ]haves?|bonus\s+points|good\s+to\s+have|preferred|what\s+sets\s+you\s+apart)"
]

MUST_HAVE_INLINE_CUES = [
    r"\b(must|required|essential|mandatory|minimum|necessity|strictly)\b",
    r"\b(must\s+have|required\s+to|proficient\s+in|hands[- ]on\s+experience\s+with)\b"
]

NICE_TO_HAVE_INLINE_CUES = [
    r"\b(preferred|nice\s+to\s+have|bonus|plus|good\s+to\s+have|desired|ideal|optional)\b",
    r"\b(familiarity\s+with|exposure\s+to|advantageous|would\s+be\s+a\s+plus)\b"
]

ROOT_CONCEPTS = {
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "ci/cd": "CI/CD",
    "cicd": "CI/CD",
    "restful api": "REST APIs",
    "rest api": "REST APIs",
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "fastapi": "FastAPI",
    "python": "Python",
    "redis": "Redis",
    "kafka": "Kafka",
    "graphql": "GraphQL",
    "terraform": "Terraform",
    "aws": "AWS",
    "gcp": "GCP",
    "azure": "Azure",
    "git": "Git",
    "linux": "Linux",
    "react": "React",
    "typescript": "TypeScript",
    "javascript": "JavaScript",
    "sql": "SQL",
    "mongodb": "MongoDB",
    "pytorch": "PyTorch",
    "tensorflow": "TensorFlow",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "langchain": "LangChain",
    "rag": "RAG",
    "vector database": "Vector Databases",
    "celery": "Celery",
    "selenium": "Selenium",
    "pytest": "Pytest",
    "system design": "System Design",
    "microservices": "Microservices",
    "tableau": "Tableau",
    "power bi": "Power BI",
    "splunk": "Splunk",
    "wireshark": "Wireshark",
    "html5": "HTML5",
    "css3": "CSS3",
    "tailwind": "Tailwind CSS",
    "next.js": "Next.js",
    "vue": "Vue.js",
    "angular": "Angular",
    "node": "Node.js"
}

class JDMatcherService:
    def __init__(self):
        self.normalizer = ats_service.normalizer
        self.all_known_skills = self._build_known_skills_vocab()

    def _build_known_skills_vocab(self) -> Dict[str, str]:
        """Collects all canonical skills and aliases across all role benchmarks."""
        vocab = {}
        for role_name, profile in ats_service.benchmarks.items():
            for crit in profile.get("critical_skills", []):
                vocab[crit.lower()] = crit
            for bon in profile.get("bonus_skills", profile.get("good_to_have", [])):
                vocab[bon.lower()] = bon
            for canonical, aliases in profile.get("skill_synonyms", {}).items():
                vocab[canonical.lower()] = canonical
                for a in aliases:
                    vocab[a.lower()] = canonical
        return vocab

    def canonicalize_skill(self, text_snippet: str) -> str:
        s_low = text_snippet.lower().strip()
        for root_key, canonical in ROOT_CONCEPTS.items():
            if root_key in s_low:
                return canonical
        norm = self.normalizer.normalize(s_low)
        for root_key, canonical in ROOT_CONCEPTS.items():
            if root_key in norm:
                return canonical
        return norm.title() if len(norm) > 3 else norm.upper()

    def extract_skills_from_text(self, text_lower: str) -> List[str]:
        """Extracts and normalizes known technical skills to deduplicated canonical names."""
        extracted = set()

        # 1. Match direct ROOT_CONCEPTS first
        for root_key, canonical in ROOT_CONCEPTS.items():
            escaped = re.escape(root_key)
            if re.search(r"\b" + escaped + r"\b", text_lower):
                extracted.add(canonical)

        # 2. Match role benchmark synonyms
        for alias, canonical in self.all_known_skills.items():
            escaped = re.escape(alias)
            if re.search(r"\b" + escaped + r"\b", text_lower):
                extracted.add(self.canonicalize_skill(canonical))
            elif len(alias) > 6 and alias in text_lower:
                extracted.add(self.canonicalize_skill(canonical))

        return sorted(list(extracted))

    def parse_experience_years(self, text_lower: str) -> Optional[int]:
        """Extracts required or candidate years of experience."""
        patterns = [
            r"(?<!\.)\b([0-9]{1,2}(?:\.[0-9]+)?)\+?\s*(?:to\s*([0-9]{1,2})\s*)?years?(?:\s+of)?\s+(?:experience|hands[- ]on)\b",
            r"\b(?:minimum|at\s+least)\s+([0-9]{1,2})\s+years?\b",
            r"(?<!\.)\b([0-9]{1,2})\s*\+\s*years\b"
        ]
        years_found = []
        for p in patterns:
            for m in re.finditer(p, text_lower):
                g = m.group(1)
                if g:
                    try:
                        val = int(round(float(g)))
                        if 1 <= val <= 25:
                            years_found.append(val)
                    except ValueError:
                        pass
        return max(years_found) if years_found else None

    def parse_education_level(self, text_lower: str) -> Tuple[Optional[str], int]:
        """Detects education requirement/attainment and returns (label, rank_tier)."""
        if re.search(r"\b(ph\.?d|doctorate|doctoral)\b", text_lower):
            return "PhD", 3
        if re.search(r"\b(master'?s?|m\.?s\.?|m\.?tech|mba)\b", text_lower):
            return "Master's Degree", 2
        if re.search(r"\b(bachelor'?s?|b\.?s\.?|b\.?tech|b\.?e\.?|undergraduate)\b", text_lower):
            return "Bachelor's Degree", 1
        return None, 0

    def parse_job_description(self, jd_text: str) -> Dict[str, Any]:
        """
        Parses JD text into must-have vs nice-to-have requirements,
        years of experience, and education expectations.
        """
        lines = [line.strip() for line in jd_text.splitlines() if line.strip()]
        must_have_lines = []
        nice_to_have_lines = []
        general_lines = []

        current_mode = "general"

        for line in lines:
            line_low = line.lower()
            is_must_header = any(re.search(p, line_low) for p in MUST_HAVE_SECTION_HEADERS)
            is_nice_header = any(re.search(p, line_low) for p in NICE_TO_HAVE_SECTION_HEADERS)

            if is_must_header:
                current_mode = "must_have"
                continue
            elif is_nice_header:
                current_mode = "nice_to_have"
                continue

            if any(re.search(p, line_low) for p in NICE_TO_HAVE_INLINE_CUES):
                nice_to_have_lines.append(line)
            elif any(re.search(p, line_low) for p in MUST_HAVE_INLINE_CUES):
                must_have_lines.append(line)
            elif current_mode == "must_have":
                must_have_lines.append(line)
            elif current_mode == "nice_to_have":
                nice_to_have_lines.append(line)
            else:
                general_lines.append(line)

        if not must_have_lines and not nice_to_have_lines:
            must_have_lines = general_lines

        must_text = " ".join(must_have_lines).lower()
        nice_text = " ".join(nice_to_have_lines).lower()
        full_text = jd_text.lower()

        must_skills = self.extract_skills_from_text(must_text)
        nice_skills = [s for s in self.extract_skills_from_text(nice_text) if s not in must_skills]

        # If must_skills is sparse but full text has skills, include them
        if len(must_skills) < 3:
            all_jd_skills = self.extract_skills_from_text(full_text)
            for s in all_jd_skills:
                if s not in must_skills and s not in nice_skills:
                    must_skills.append(s)

        req_years = self.parse_experience_years(full_text)
        req_edu_label, req_edu_tier = self.parse_education_level(full_text)

        return {
            "must_have_skills": must_skills,
            "nice_to_have_skills": nice_skills,
            "required_years": req_years,
            "required_education_label": req_edu_label,
            "required_education_tier": req_edu_tier
        }

    def compute_semantic_similarity(self, resume_text: str, jd_text: str) -> float:
        """Computes calibrated TF-IDF cosine similarity between resume and JD."""
        try:
            vec = TfidfVectorizer(max_features=2500, ngram_range=(1, 2), stop_words="english", sublinear_tf=True)
            tfidf_mat = vec.fit_transform([resume_text, jd_text])
            sim = float(cosine_similarity(tfidf_mat[0:1], tfidf_mat[1:2])[0][0])
            # Calibrate TF-IDF cosine similarity between 2 documents
            if sim <= 0.04:
                score = (sim / 0.04) * 20.0
            elif sim <= 0.10:
                score = 20.0 + ((sim - 0.04) / (0.10 - 0.04)) * 30.0
            elif sim <= 0.20:
                score = 50.0 + ((sim - 0.10) / (0.20 - 0.10)) * 30.0
            else:
                score = 80.0 + min(18.5, ((sim - 0.20) / (0.40 - 0.20)) * 18.5)
            return round(float(score), 1)
        except Exception:
            return 50.0

    def match_resume_to_jd(self, resume_text: str, jd_text: str) -> JDMatchResponse:
        """
        Executes complete Resume-vs-JD audit:
        Must-Have Skills: 45% (or 55% if no nice-to-haves)
        Nice-to-Have Skills: 15%
        Semantic Similarity (TF-IDF): 20% (or 25% if no nice-to-haves)
        Experience Alignment: 10%
        Education Alignment: 10%
        """
        resume_lower = resume_text.lower()
        jd_parsed = self.parse_job_description(jd_text)

        must_skills = jd_parsed["must_have_skills"]
        nice_skills = jd_parsed["nice_to_have_skills"]
        req_years = jd_parsed["required_years"]
        req_edu_label = jd_parsed["required_education_label"]
        req_edu_tier = jd_parsed["required_education_tier"]

        # Resume analysis
        candidate_skills = set(self.extract_skills_from_text(resume_lower))
        cand_years = self.parse_experience_years(resume_lower)
        cand_edu_label, cand_edu_tier = self.parse_education_level(resume_lower)

        # 1. Must-Haves
        matched_must = [s for s in must_skills if s in candidate_skills]
        missing_must = [s for s in must_skills if s not in candidate_skills]
        must_ratio = len(matched_must) / max(1, len(must_skills))
        must_score = round(must_ratio * 100.0, 1)

        # 2. Nice-to-Haves
        matched_nice = [s for s in nice_skills if s in candidate_skills]
        missing_nice = [s for s in nice_skills if s not in candidate_skills]
        nice_ratio = len(matched_nice) / max(1, len(nice_skills)) if nice_skills else 1.0
        nice_score = round(nice_ratio * 100.0, 1) if nice_skills else 100.0

        # 3. Semantic Similarity
        semantic_score = self.compute_semantic_similarity(resume_text, jd_text)

        # 4. Experience Check
        if req_years is None:
            exp_score = 100.0
            exp_status = f"No minimum experience required (Detected: {cand_years or 0} yrs)"
        else:
            cand_y = cand_years if cand_years is not None else 1
            if cand_y >= req_years:
                exp_score = 100.0
                exp_status = f"Requirement Met ({cand_y} yrs detected vs {req_years} yrs required)"
            elif cand_y >= (req_years - 1):
                exp_score = 75.0
                exp_status = f"Near Requirement ({cand_y} yrs detected vs {req_years} yrs required)"
            else:
                exp_score = max(20.0, (cand_y / max(1, req_years)) * 60.0)
                exp_status = f"Experience Gap ({cand_y} yrs detected vs {req_years} yrs required)"

        # 5. Education Check
        if req_edu_tier == 0 or not req_edu_label:
            edu_score = 100.0
            edu_status = f"No degree restriction specified (Candidate: {cand_edu_label or 'Self-Directed / Unspecified'})"
        else:
            if cand_edu_tier >= req_edu_tier:
                edu_score = 100.0
                edu_status = f"Degree Requirement Met ({cand_edu_label} meets or exceeds {req_edu_label})"
            elif cand_edu_tier > 0:
                edu_score = 70.0
                edu_status = f"Partial Education Match ({cand_edu_label} vs {req_edu_label} preferred)"
            else:
                edu_score = 40.0
                edu_status = f"Degree Not Explicitly Stated (Target: {req_edu_label})"

        # 6. Weighted JD Match Score Formula
        if nice_skills:
            w_must = 0.45
            w_nice = 0.15
            w_sem = 0.20
            w_exp = 0.10
            w_edu = 0.10
        else:
            w_must = 0.55
            w_nice = 0.00
            w_sem = 0.25
            w_exp = 0.10
            w_edu = 0.10

        composite = (
            (must_score * w_must) +
            (nice_score * w_nice) +
            (semantic_score * w_sem) +
            (exp_score * w_exp) +
            (edu_score * w_edu)
        )
        jd_match_score = int(round(max(0.0, min(100.0, composite))))

        # 7. Keyword Gaps with Placement Advice
        placement_advice: List[KeywordGapPlacement] = []
        for kw in missing_must[:6]:
            placement_advice.append(KeywordGapPlacement(
                keyword=kw,
                importance="Must-Have",
                recommended_section="Technical Skills & Work Experience",
                placement_tip=f"Add '{kw}' to your core skills list and describe a concrete project milestone or business outcome where you utilized {kw}."
            ))
        for kw in missing_nice[:4]:
            placement_advice.append(KeywordGapPlacement(
                keyword=kw,
                importance="Nice-to-Have",
                recommended_section="Secondary Skills or Project Bullets",
                placement_tip=f"Incorporate '{kw}' into relevant project bullets or tools summary to capture recruiter bonus filters."
            ))

        # 8. Actionable Resume Edits
        actionable_edits: List[ResumeEditSuggestion] = []
        if missing_must:
            top_miss = ", ".join(missing_must[:3])
            actionable_edits.append(ResumeEditSuggestion(
                priority="High",
                category="Critical Keyword Gap",
                action=f"Explicitly weave in {top_miss} into your Summary and latest Work Experience bullets.",
                before_example="Developed backend services and managed deployment pipelines.",
                after_example=f"Architected scalable microservices using {missing_must[0]} with automated CI/CD container deployments."
            ))
        if exp_score < 100.0 and req_years:
            actionable_edits.append(ResumeEditSuggestion(
                priority="High",
                category="Experience Alignment",
                action=f"Highlight overall project tenure or cumulative freelance/internship experience to bridge the {req_years}-year target.",
                before_example="Worked on multiple projects over the last 2 years.",
                after_example=f"3+ years of cumulative software development experience across production platforms and academic capstones."
            ))
        if semantic_score < 70.0:
            actionable_edits.append(ResumeEditSuggestion(
                priority="Medium",
                category="Vocabulary & Phrasing Congruence",
                action="Mirror domain terminology used in the job description (e.g. business goals, delivery metrics, and architectural patterns).",
                before_example="Responsible for team tasks and delivering code.",
                after_example="Partnered with cross-functional stakeholders to define technical roadmap and deliver high-availability services."
            ))

        summary_text = (
            f"JD Match Score: {jd_match_score}/100. "
            f"Matched {len(matched_must)} of {len(must_skills)} must-have requirements "
            f"and {len(matched_nice)} of {len(nice_skills)} preferred qualifications. "
            f"Semantic similarity is {semantic_score:.1f}%. "
            f"{exp_status}. {edu_status}."
        )

        weights_doc = {
            "must_haves_weight": int(w_must * 100),
            "nice_to_haves_weight": int(w_nice * 100),
            "semantic_similarity_weight": int(w_sem * 100),
            "experience_alignment_weight": int(w_exp * 100),
            "education_alignment_weight": int(w_edu * 100),
            "formula": "Score = (Must * w_must) + (Nice * w_nice) + (TF-IDF * w_sem) + (Exp * w_exp) + (Edu * w_edu)"
        }

        return JDMatchResponse(
            jd_match_score=jd_match_score,
            semantic_similarity_score=semantic_score,
            must_have_score=must_score,
            nice_to_have_score=nice_score,
            matched_must_haves=matched_must,
            missing_must_haves=missing_must,
            matched_nice_to_haves=matched_nice,
            missing_nice_to_haves=missing_nice,
            required_years_experience=req_years,
            candidate_years_experience=cand_years,
            experience_status=exp_status,
            required_education=req_edu_label,
            candidate_education=cand_edu_label,
            education_status=edu_status,
            keyword_gaps_with_placement=placement_advice,
            actionable_resume_edits=actionable_edits,
            scoring_formula_weights=weights_doc,
            summary=summary_text,
            matched_skills=list(candidate_skills)
        )

jd_matcher_service = JDMatcherService()

import re
from typing import List, Dict, Any
from ..models.schemas import ResumeAnalysisResponse

ROLE_BENCHMARKS: Dict[str, Dict[str, Any]] = {
    "AI Engineer": {
        "critical_skills": [
            "python", "pytorch", "transformers", "vector database", "rag",
            "langchain", "docker", "fastapi", "cuda", "model evaluation",
            "mlops", "fine-tuning"
        ],
        "good_to_have": ["kubernetes", "tensorrt", "aws", "git", "ci/cd", "triton"],
        "action_verbs": ["fine-tuned", "architected", "deployed", "optimized", "benchmarked", "accelerated", "implemented", "trained"],
    },
    "Full Stack Developer": {
        "critical_skills": [
            "typescript", "react", "node.js", "next.js", "postgresql",
            "tailwind css", "rest api", "graphql", "docker", "git"
        ],
        "good_to_have": ["redis", "aws", "jest", "ci/cd", "microservices"],
        "action_verbs": ["built", "scaled", "designed", "integrated", "refactored", "shipped"],
    },
    "Cloud & DevOps Engineer": {
        "critical_skills": [
            "kubernetes", "docker", "terraform", "aws", "ci/cd",
            "linux", "prometheus", "grafana", "python", "bash"
        ],
        "good_to_have": ["argo cd", "helm", "istio", "ansible", "gcp"],
        "action_verbs": ["automated", "orchestrated", "provisioned", "migrated", "hardened", "monitored"],
    }
}

class ATSService:
    def analyze_resume_text(self, text: str, target_role: str = "AI Engineer") -> ResumeAnalysisResponse:
        role_profile = ROLE_BENCHMARKS.get(target_role, ROLE_BENCHMARKS["AI Engineer"])
        text_lower = text.lower()

        # 1. Extracted and Matched Skills
        all_candidate_skills = role_profile["critical_skills"] + role_profile["good_to_have"] + [
            "c++", "java", "sql", "pandas", "numpy", "scikit-learn", "huggingface", "llm", "git", "linux"
        ]
        
        extracted_skills = []
        for skill in set(all_candidate_skills):
            # word boundary match
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                extracted_skills.append(skill.title() if len(skill) > 3 else skill.upper())

        critical = [s.lower() for s in role_profile["critical_skills"]]
        matched = [s for s in extracted_skills if s.lower() in critical]
        missing = [s.title() for s in critical if s not in [x.lower() for x in extracted_skills]]

        # 2. Action Verbs Count
        action_verb_count = 0
        for verb in role_profile["action_verbs"]:
            matches = re.findall(r'\b' + re.escape(verb) + r'\b', text_lower)
            action_verb_count += len(matches)

        # 3. Quantifiable Metrics (e.g. 40%, 10x, $50k, 150ms, 10,000 users)
        metric_pattern = r'(\b\d+(\.\d+)?(%|x|k|ms|s|m|gb|tb|\+)?\b|\$\d+)'
        quantifiable_metrics = re.findall(metric_pattern, text_lower)
        quantifiable_metrics_count = len(quantifiable_metrics)

        # 4. Formatting health checks
        sections_found = 0
        common_sections = ["experience", "education", "projects", "skills", "certifications"]
        for section in common_sections:
            if section in text_lower:
                sections_found += 1
        formatting_score = min(98, int((sections_found / len(common_sections)) * 70 + 28))

        # 5. Skills match calculation
        skills_match_score = min(98, int((len(matched) / max(1, len(critical))) * 100))
        
        # 6. Impact calculation
        impact_score = min(95, int(min(quantifiable_metrics_count, 12) * 6 + min(action_verb_count, 8) * 4))

        # 7. Weighted Composite ATS Score
        ats_score = int(
            (skills_match_score * 0.50) +
            (formatting_score * 0.25) +
            (impact_score * 0.25)
        )
        ats_score = max(42, min(97, ats_score))

        # Actionable recommendations
        actionable_recommendations = []
        if missing:
            actionable_recommendations.append({
                "category": "Skill Gap",
                "priority": "High",
                "title": f"Add proof of competency in {', '.join(missing[:3])}",
                "description": f"Recruiter search filters for '{target_role}' prioritize candidates with hands-on projects showing {missing[0]}."
            })
        if quantifiable_metrics_count < 5:
            actionable_recommendations.append({
                "category": "Impact Metrics",
                "priority": "Medium",
                "title": "Quantify outcomes with the XYZ formula",
                "description": "Transform bullet points into: 'Accomplished [X] as measured by [Y], by doing [Z]'. Example: 'Reduced inference latency by 35%'."
            })
        if action_verb_count < 6:
            actionable_recommendations.append({
                "category": "Action Verbs",
                "priority": "Medium",
                "title": "Replace passive language with strong engineering verbs",
                "description": f"Use high-impact verbs like {', '.join(role_profile['action_verbs'][:4])} at the start of bullet points."
            })

        critique = (
            f"Your resume shows solid foundation with {len(extracted_skills)} recognized skills, "
            f"scoring {ats_score}/100 for '{target_role}'. To reach the top 5% applicant tier, "
            f"incorporate the missing high-frequency keywords ({', '.join(missing[:3])}) and "
            f"reinforce technical bullet points with benchmarked metrics."
        )

        return ResumeAnalysisResponse(
            ats_score=ats_score,
            formatting_score=formatting_score,
            skills_match_score=skills_match_score,
            impact_score=impact_score,
            extracted_skills=extracted_skills,
            missing_skills=missing,
            matched_skills=matched,
            action_verb_count=action_verb_count,
            quantifiable_metrics_count=quantifiable_metrics_count,
            summary_critique=critique,
            actionable_recommendations=actionable_recommendations
        )

ats_service = ATSService()

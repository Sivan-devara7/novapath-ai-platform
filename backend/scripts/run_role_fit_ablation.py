"""
Ablation Study: Evaluates the impact of ML Role-Fit scoring weight
at 40% (default) vs 20% vs 0% on sample resumes.
Does NOT change default weights in settings/ATSService, purely for analysis and reporting.
"""

import os
import sys
import json

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from app.services.ats_service import ATSService

# 3 Representative Sample Resumes
SAMPLE_RESUMES = [
    {
        "name": "Sample A: Strong Match (Senior AI Engineer -> AI Engineer)",
        "target_role": "AI Engineer",
        "text": """
Alex Chen | AI Engineer | alex.chen@example.com | https://github.com/alexchen-ai

PROFESSIONAL SUMMARY
Senior AI Engineer with 6+ years of production experience fine-tuning and deploying large language models,
building low-latency RAG systems, and scaling distributed deep learning workloads. Expert in PyTorch,
Transformers, LangChain, vector databases (FAISS, Pinecone), and high-throughput model serving with FastAPI and Docker.

CORE TECHNICAL SKILLS
- Machine Learning & DL: PyTorch, Hugging Face Transformers, LoRA, QLoRA, Fine-Tuning, Embeddings, CUDA, Vector Databases
- LLM & Agents: LangChain, LlamaIndex, RAG, Prompt Engineering, Model Evaluation, Ragas
- Infrastructure & Tools: Docker, Kubernetes, FastAPI, vLLM, Triton, Weights & Biases, Git, Linux

WORK EXPERIENCE
Staff AI Engineer | Apex Cloud Solutions | 2022 - Present
- Architected enterprise hybrid RAG pipeline with Pinecone and cross-encoder re-ranking, improving retrieval accuracy by 48%.
- Fine-tuned open-source 7B and 14B parameter foundation models using LoRA and PEFT, cutting inference compute costs by 52%.
- Deployed high-concurrency vLLM serving cluster on AWS Kubernetes with automated scaling, supporting 3.5M daily requests at 99.9% uptime.
- Benchmarked model evaluation metrics with Ragas across 10,000 production queries, reducing hallucination rate by 34%.

Senior Machine Learning Engineer | DataPulse AI | 2019 - 2022
- Engineered end-to-end NLP data processing pipeline in PyTorch, accelerating training throughput by 2.8x.
- Containerized microservices using Docker and orchestrated automated CI/CD evaluation pipelines in GitHub Actions.
- Mentored 4 junior ML engineers on distributed training practices and PyTorch autograd optimizations.

EDUCATION
Master of Science in Computer Science | GPA: 3.9 / 4.0
Certifications: AWS Certified Machine Learning - Specialty, NVIDIA Generative AI Associate
"""
    },
    {
        "name": "Sample B: Entry-Level Match (Junior Frontend Dev -> Frontend Developer)",
        "target_role": "Frontend Developer",
        "text": """
Jordan Smith | Frontend Developer | jordan.smith@example.com | https://github.com/jordansmith

SUMMARY
Entry-level Frontend Developer with hands-on experience building interactive web applications using React,
JavaScript (ES6+), HTML5, and CSS3. Strong foundation in component architecture and Git workflows.

TECHNICAL SKILLS
- Languages: JavaScript, TypeScript, HTML5, CSS3
- Frameworks: React, Tailwind CSS, Next.js basics
- Tools: Git, GitHub, VS Code, Chrome DevTools, npm

PROJECTS
Personal Portfolio & Tech Blog
- Built responsive web application using React and Tailwind CSS with light/dark theme toggle.
- Integrated third-party weather API using fetch API and managed component state with React hooks.

Task Manager Web App
- Developed CRUD application using React and localStorage for persistent client-side state.
- Styled layouts with flexbox and media queries ensuring seamless mobile and desktop responsiveness.

EDUCATION
Bachelor of Science in Information Technology | 2024 | GPA: 3.6 / 4.0
"""
    },
    {
        "name": "Sample C: Cross-Role Mismatch (Cybersecurity Analyst -> Product Manager)",
        "target_role": "Product Manager",
        "text": """
Marcus Vance | Cybersecurity Analyst | marcus.vance@example.com | https://linkedin.com/in/marcusvance

PROFESSIONAL SUMMARY
Dedicated Information Security Analyst with 4 years in SOC operations, incident response, packet analysis,
and vulnerability assessments. Skilled in Splunk, Wireshark, Snort, and network penetration testing.

CORE SKILLS
- Security: SIEM, Splunk, Wireshark, Incident Response, Vulnerability Assessment, Firewall Management, MITRE ATT&CK
- Systems: Kali Linux, Bash, Active Directory, IAM, Cryptography

WORK EXPERIENCE
Security Operations Center (SOC) Analyst | Vanguard Cyber Defense | 2021 - Present
- Monitored security alerts in Splunk SIEM, triaging over 200 daily network anomalies and phishing attempts.
- Investigated suspicious packet captures using Wireshark and tcpdump, containing 12 potential malware incidents.
- Hardened internal Linux servers and configured iptables firewalls following CIS benchmarks.

EDUCATION & CERTS
B.S. in Cybersecurity | CompTIA Security+ Certified
"""
    }
]

def calculate_ablation_score(component_scores: dict, weights: dict) -> float:
    score = (
        component_scores["role_fit"] * weights["role_fit"] +
        component_scores["keyword_match"] * weights["keyword_match"] +
        component_scores["section_completeness"] * weights["section_completeness"] +
        component_scores["formatting"] * weights["formatting"] +
        component_scores["impact_metrics"] * weights["impact_metrics"]
    )
    return round(score, 2)

def run_ablation():
    print("=" * 85)
    print("NOVAPATH AI — ATS MODEL ABLATION STUDY: ML ROLE-FIT WEIGHT (40% vs 20% vs 0%)")
    print("=" * 85)

    ats = ATSService()

    # Weight Configurations (all sum to 1.00):
    # Base remaining weights sum: 25 + 15 + 10 + 10 = 60
    weights_configs = {
        "40% ML Fit (Default Baseline)": {
            "role_fit": 0.40,
            "keyword_match": 0.25,
            "section_completeness": 0.15,
            "formatting": 0.10,
            "impact_metrics": 0.10
        },
        "20% ML Fit (Proportional Split)": {
            "role_fit": 0.20,
            "keyword_match": round(0.80 * (25 / 60), 4),
            "section_completeness": round(0.80 * (15 / 60), 4),
            "formatting": round(0.80 * (10 / 60), 4),
            "impact_metrics": round(0.80 * (10 / 60), 4)
        },
        "0% ML Fit (Keyword/Rule Only)": {
            "role_fit": 0.00,
            "keyword_match": round(1.00 * (25 / 60), 4),
            "section_completeness": round(1.00 * (15 / 60), 4),
            "formatting": round(1.00 * (10 / 60), 4),
            "impact_metrics": round(1.00 * (10 / 60), 4)
        }
    }

    results = []

    for sample in SAMPLE_RESUMES:
        name = sample["name"]
        target_role = sample["target_role"]
        text = sample["text"]

        # Run real ATS evaluation to get individual component scores
        eval_res = ats.analyze_resume_text(text, target_role)

        comp_scores = {
            "role_fit": float(eval_res.role_fit_score or 0.0),
            "keyword_match": float(eval_res.skills_match_score or 0.0),
            "section_completeness": float(eval_res.section_score or 0.0),
            "formatting": float(eval_res.formatting_score or 0.0),
            "impact_metrics": float(eval_res.impact_score or 0.0)
        }

        # Calculate scores under each ablation weight config
        score_40 = calculate_ablation_score(comp_scores, weights_configs["40% ML Fit (Default Baseline)"])
        score_20 = calculate_ablation_score(comp_scores, weights_configs["20% ML Fit (Proportional Split)"])
        score_0 = calculate_ablation_score(comp_scores, weights_configs["0% ML Fit (Keyword/Rule Only)"])

        diff_20_vs_40 = round(score_20 - score_40, 2)
        diff_0_vs_40 = round(score_0 - score_40, 2)

        results.append({
            "sample_name": name,
            "target_role": target_role,
            "components": comp_scores,
            "score_40_pct": score_40,
            "score_20_pct": score_20,
            "score_0_pct": score_0,
            "delta_20_vs_40": diff_20_vs_40,
            "delta_0_vs_40": diff_0_vs_40
        })

    # Print Table
    print(f"\n{'Sample Resume':<45} | {'Role-Fit':8s} | {'Keyword':8s} | {'40% ML':8s} | {'20% ML':8s} | {'0% ML':8s} | {'Delta (0% vs 40%)':18s}")
    print("-" * 115)
    for r in results:
        rf = r["components"]["role_fit"]
        kw = r["components"]["keyword_match"]
        delta_str = f"{r['delta_0_vs_40']:+0.2f} pts"
        print(f"{r['sample_name'][:45]:<45} | {rf:8.1f} | {kw:8.1f} | {r['score_40_pct']:8.2f} | {r['score_20_pct']:8.2f} | {r['score_0_pct']:8.2f} | {delta_str:18s}")

    # Save artifact
    data_dir = os.path.join(backend_dir, "data")
    output_path = os.path.join(data_dir, "ablation_study_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"weights_configs": weights_configs, "results": results}, f, indent=2)
    print(f"\nAblation study results saved to: {output_path}")

if __name__ == "__main__":
    run_ablation()

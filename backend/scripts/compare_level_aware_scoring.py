"""
Compare Level-Aware Keyword Scoring and Calibrated Role-Fit
Evaluates Samples A, B, C plus 5 new representative resumes:
- Sample D: Fresher Data Analyst
- Sample E: Mid Backend Developer
- Sample F: Senior DevOps Engineer
- Sample G: Fresher QA / Test Automation Engineer
- Sample H: Mid SRE
"""

import os
import sys
import json
import re

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from app.services.ats_service import ATSService

# Resumes dataset
SAMPLES = [
    {
        "id": "A",
        "name": "Sample A: Senior AI Engineer",
        "target_role": "AI Engineer",
        "expected_level": "senior",
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
        "id": "B",
        "name": "Sample B: Junior Frontend Developer",
        "target_role": "Frontend Developer",
        "expected_level": "fresher",
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
Bachelor of Science in Information Technology | Class of 2024 | GPA: 3.6 / 4.0
"""
    },
    {
        "id": "C",
        "name": "Sample C: Security Analyst (Mismatch)",
        "target_role": "Product Manager",
        "expected_level": "mid",
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
    },
    {
        "id": "D",
        "name": "Sample D: Fresher Data Analyst",
        "target_role": "Data Analyst",
        "expected_level": "fresher",
        "text": """
Priya Patel | Data Analyst | priya.patel@example.com | https://github.com/priyapatel-data

SUMMARY
Enthusiastic entry-level Data Analyst and recent graduate with strong proficiency in SQL, Excel, Python,
and Tableau. Experienced in transforming raw datasets into interactive dashboards and actionable business insights.

CORE SKILLS
- Analysis & BI: SQL, Microsoft Excel (Pivot Tables, VLOOKUP, Power Query), Tableau, Power BI
- Programming & Stats: Python, Pandas, NumPy, Matplotlib, Exploratory Data Analysis, Descriptive Statistics
- Tools: Git, Jupyter Notebook, PostgreSQL

ACADEMIC PROJECTS
E-Commerce Sales Performance Dashboard | Capstone Project (2024)
- Extracted and cleaned 50,000+ transaction records using SQL queries and Python Pandas.
- Designed an interactive 4-page Tableau dashboard visualizing monthly revenue trends, customer retention, and regional sales metrics.
- Identified underperforming product categories and recommended inventory adjustments projected to save 8% carrying cost.

Customer Churn Analysis
- Conducted exploratory data analysis on 10,000 telecom customer records using Python, NumPy, and Seaborn.
- Formulated key customer retention indicators that highlighted contract duration as the primary churn driver.

EDUCATION
Bachelor of Science in Statistics and Data Science | Class of 2024 | GPA: 3.75 / 4.0
Relevant Coursework: Applied Statistics, Database Management Systems, Data Visualization, Business Analytics
"""
    },
    {
        "id": "E",
        "name": "Sample E: Mid-Level Backend Developer",
        "target_role": "Backend Developer",
        "expected_level": "mid",
        "text": """
David Miller | Backend Developer | david.miller@example.com | https://github.com/dmiller-backend

PROFESSIONAL SUMMARY
Backend Developer with 3+ years of experience designing scalable microservices, RESTful APIs, and database
architectures. Proficient in Python, FastAPI, PostgreSQL, Redis caching, and Docker containerization.

TECHNICAL SKILLS
- Languages: Python, Go basics, SQL
- Frameworks & Libs: FastAPI, Django REST Framework, SQLAlchemy, Pydantic, Celery
- Databases & Caching: PostgreSQL, Redis, MongoDB
- DevOps & Tools: Docker, Git, CI/CD pipelines, Pytest, Postman, Linux

WORK EXPERIENCE
Backend Software Engineer | CloudScale Systems | 2022 - Present
- Architected and implemented 15+ RESTful API microservices in FastAPI serving 1.2M daily active requests.
- Optimized slow PostgreSQL queries by creating composite indexes and connection pools, decreasing P95 query latency by 42%.
- Integrated Redis caching layer for authenticated session tokens and frequently queried product catalogs.
- Authored comprehensive test suites with Pytest achieving 88% code coverage across backend services.

Junior Software Engineer | TechCraft Solutions | 2021 - 2022
- Developed asynchronous task processing pipeline using Celery and Redis to handle automated email notifications.
- Created Dockerized local development environments simplifying team onboarding from 2 days to 30 minutes.

EDUCATION
Bachelor of Science in Computer Science | 2021 | GPA: 3.5 / 4.0
"""
    },
    {
        "id": "F",
        "name": "Sample F: Senior DevOps / Cloud Engineer",
        "target_role": "Cloud & DevOps",
        "expected_level": "senior",
        "text": """
Samantha Reed | Senior Cloud & DevOps Engineer | samantha.reed@example.com | https://github.com/samanthareed-devops

PROFESSIONAL SUMMARY
Senior Cloud & DevOps Engineer with 8+ years of expertise designing resilient multi-region AWS cloud infrastructure,
automating enterprise CI/CD pipelines, and orchestrating high-density Kubernetes clusters. Expert in Terraform,
Docker, Kubernetes, Prometheus, Grafana, and zero-downtime deployment strategies.

TECHNICAL SKILLS
- Cloud Platforms: Amazon Web Services (AWS - VPC, EKS, RDS, IAM, S3, Route53), GCP
- Infrastructure as Code: Terraform, Terragrunt, CloudFormation, Ansible
- Containers & Orchestration: Docker, Kubernetes, Helm, ArgoCD
- CI/CD & Observability: GitLab CI, GitHub Actions, Prometheus, Grafana, ELK Stack, Datadog
- Languages: Python, Bash, Go

WORK EXPERIENCE
Staff DevOps Engineer | Enterprise Global Cloud | 2020 - Present
- Architected enterprise multi-account AWS Landing Zone with Terraform managing over $250k monthly cloud infrastructure.
- Migrated 40+ containerized microservices to Amazon EKS using Helm charts and GitOps with ArgoCD.
- Implemented full-stack observability with Prometheus and Grafana alerts, reducing MTTR from 45 minutes to 7 minutes.
- Enforced strict SOC-2 compliance, IAM least-privilege policies, and automated vulnerability scanning in GitLab CI.

Senior Cloud Infrastructure Engineer | Nexus Stream | 2017 - 2020
- Built zero-downtime blue/green deployment automation across AWS ECS clusters using Python and Docker.
- Spearheaded cloud cost optimization program renegotiating reserved instances and right-sizing workloads, saving $180k annually.

EDUCATION & CERTIFICATIONS
B.S. in Computer Engineering
Certifications: AWS Certified Solutions Architect - Professional, Certified Kubernetes Administrator (CKA), HashiCorp Certified Terraform Associate
"""
    },
    {
        "id": "G",
        "name": "Sample G: Fresher QA / Test Automation Engineer",
        "target_role": "QA/Test Automation Engineer",
        "expected_level": "fresher",
        "text": """
Kavita Sharma | QA Test Automation Engineer | kavita.sharma@example.com | https://github.com/kavitasharma-qa

SUMMARY
Detail-oriented entry-level QA Engineer and 2024 graduate with strong foundational knowledge in automated UI testing,
REST API verification, test case design, and bug tracking. Hands-on experience with Selenium WebDriver, Python, Postman, and Pytest.

SKILLS
- Testing Frameworks & Tools: Selenium WebDriver, Pytest, Postman, TestNG basics, Manual Testing
- Methodologies: Test Case Design, Functional Testing, Regression Testing, SDLC, STLC, Bug Lifecycle
- Languages & Tools: Python, Java basics, SQL, Git, GitHub, Jira

PROJECTS & INTERNSHIP
QA Automation Intern | SoftQuality Labs | Jan 2024 - June 2024
- Wrote 60+ automated regression test scripts using Python and Selenium WebDriver for an e-commerce web platform.
- Executed API integration tests using Postman collections and automated response schema validation.
- Documented and tracked 25+ software defects in Jira with reproducible steps and browser logs, collaborating closely with developers.

Automated Healthcare Portal Testing (Capstone Project)
- Designed comprehensive test strategy and test matrix covering patient registration, appointment booking, and records upload.
- Implemented Page Object Model (POM) pattern in Pytest, ensuring reusable and clean test architecture.
- Verified backend database state using SQL queries to validate transactional integrity after frontend submissions.

EDUCATION
Bachelor of Technology in Computer Science | Class of 2024 | GPA: 3.7 / 4.0
Certifications: ISTQB Foundation Level (Certified Tester)
"""
    },
    {
        "id": "H",
        "name": "Sample H: Mid-Level SRE",
        "target_role": "SRE",
        "expected_level": "mid",
        "text": """
Vikram Nair | Site Reliability Engineer (SRE) | vikram.nair@example.com | https://github.com/vikramnair-sre

PROFESSIONAL SUMMARY
Site Reliability Engineer with 4 years of experience enhancing systems availability, scalability, and performance.
Proficient in Linux systems internals, Kubernetes, Terraform, Prometheus/Grafana monitoring, and incident response.

CORE TECHNICAL SKILLS
- SRE Practices: SLO / SLI definition, Error Budgets, Incident Management, Postmortems, On-Call Operations
- Infrastructure & Orchestration: Kubernetes, Docker, Linux (Ubuntu/Debian, kernel tuning), Terraform
- Observability: Prometheus, Grafana, OpenTelemetry, Alertmanager, Jaeger tracing
- Scripting & Automation: Python, Bash, Go basics, Git

WORK EXPERIENCE
Site Reliability Engineer | Apex Streaming Media | 2022 - Present
- Maintained 99.95% system availability for core streaming platform handling over 25,000 requests per second.
- Established actionable SLOs, SLIs, and alert thresholds in Prometheus, eliminating over 60% of noisy pagers.
- Automated Kubernetes cluster node autoscaling and horizontal pod autoscalers (HPA) to seamlessly handle traffic surges.
- Led root cause analysis (RCA) and blameless postmortems for high-severity platform incidents.

Junior DevOps / Systems Engineer | CloudBridge | 2020 - 2022
- Managed Linux production servers, configuring systemd services, log rotation, and automated cron maintenance jobs.
- Authored Bash and Python automation scripts for routine database backups, disk cleanups, and SSL certificate renewals.

EDUCATION
Bachelor of Engineering in Information Technology | 2020
"""
    }
]


def run_comparison():
    ats = ATSService()

    results = []

    for s in SAMPLES:
        role = s["target_role"]
        text = s["text"]
        profile = ats.get_role_profile(role)
        canonical = profile.get("role", role)
        text_lower = text.lower()

        # 1. Detected seniority
        detected_level = ats._detect_candidate_seniority(text_lower)

        # 2. Before Keyword Score (flat calculation against critical + bonus skills without level expectations)
        crit_skills = [k.lower() for k in profile.get("critical_skills", [])]
        bonus_skills = [k.lower() for k in profile.get("bonus_skills", profile.get("good_to_have", []))]
        synonyms = profile.get("skill_synonyms", {})
        
        matched_set = set()
        for c in set(crit_skills + bonus_skills):
            aliases = [c] + synonyms.get(c, [])
            escaped = [re.escape(a) for a in aliases if len(a.strip()) > 0]
            if not escaped:
                continue
            p = r"\b(" + "|".join(escaped) + r")\b"
            if re.search(p, text_lower) or (len(c) > 6 and c in text_lower):
                matched_set.add(c)
        
        m_crit = [c for c in crit_skills if c in matched_set]
        m_bon = [b for b in bonus_skills if b in matched_set]
        c_ratio = len(m_crit) / max(1, len(crit_skills))
        b_ratio = len(m_bon) / max(1, len(bonus_skills))
        old_keyword_score = round(min(100.0, max(0.0, (c_ratio * 85.0) + (b_ratio * 15.0))), 1)

        # 3. After Keyword Score (level-aware)
        new_keyword_score, matched_kws, miss_crit, miss_bon, extracted, det_level = ats._calculate_keyword_coverage(text_lower, role)

        # 4. Old Saturated Role Fit vs Calibrated Role Fit
        classes = list(ats._model.classes_) if ats._model else []
        cleaned_text = ats.clean_text_for_model(text)
        if ats._model and canonical in classes:
            prob = float(ats._model.predict_proba([cleaned_text])[0][classes.index(canonical)])
        else:
            prob = 0.5

        old_role_fit = round(min(100.0, (prob / 0.65) * 100.0), 1)
        new_role_fit, top_features, pred_cls = ats._calculate_ml_role_fit(cleaned_text, role)

        # 5. Section, Action Verbs, Formatting
        sec_score, _, _, _ = ats._calculate_section_completeness(text_lower, role)
        fmt_score, _ = ats._calculate_formatting_parsability(text)
        impact_score, _, _ = ats._calculate_quantified_impact(text_lower, role)

        # 6. Total Scores (weights unchanged: 40% role fit, 25% keywords, 15% sections, 10% formatting, 10% impact)
        old_total = round((old_role_fit * 0.40) + (old_keyword_score * 0.25) + (sec_score * 0.15) + (fmt_score * 0.10) + (impact_score * 0.10), 1)
        new_total = round((new_role_fit * 0.40) + (new_keyword_score * 0.25) + (sec_score * 0.15) + (fmt_score * 0.10) + (impact_score * 0.10), 1)

        results.append({
            "id": s["id"],
            "name": s["name"],
            "target_role": role,
            "detected_level": det_level,
            "expected_level": s["expected_level"],
            "matched_crit_count": len(m_crit),
            "total_crit_count": len(crit_skills),
            "old_keyword_score": old_keyword_score,
            "new_keyword_score": new_keyword_score,
            "keyword_delta": round(new_keyword_score - old_keyword_score, 1),
            "prob": round(prob, 4),
            "old_role_fit": old_role_fit,
            "new_role_fit": new_role_fit,
            "role_fit_delta": round(new_role_fit - old_role_fit, 1),
            "old_total": old_total,
            "new_total": new_total,
            "total_delta": round(new_total - old_total, 1)
        })

    print(json.dumps(results, indent=2))
    with open(os.path.join(backend_dir, "data", "level_aware_comparison_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_comparison()

"""
Level Detection Accuracy Audit
Builds 20 labeled test snippets (fresher/mid/senior), including sparse mid-level
and strong fresher resumes, and computes the 3x3 confusion matrix and classification report.
Also documents the exact fresher booster formula.
"""

import os
import sys
import json
import re

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from app.services.ats_service import ATSService

TEST_SNIPPETS = [
    # --- 7 FRESHERS ---
    {
        "id": 1,
        "true_level": "fresher",
        "description": "Strong Fresher: 2024 grad, 3.9 GPA, 4 projects, hackathon winner, 0 yrs exp",
        "text": """
Aarav Patel | aarav@example.com | github.com/aarav | Class of 2024
Summary: High-achieving entry-level Computer Science graduate with strong algorithms foundation and 4 full-stack projects.
Winner of 2024 National Hackathon. Looking for first software engineer role.
Education: Bachelor of Science in Computer Science, May 2024. GPA: 3.9 / 4.0.
Academic Projects:
- Distributed Key-Value Store (Capstone Project): Implemented Raft consensus in Go.
- E-Commerce Mobile App: Built React Native frontend with Node.js backend.
Technical Skills: Python, Java, Go, React, Git, SQL.
"""
    },
    {
        "id": 2,
        "true_level": "fresher",
        "description": "Junior Developer Intern: 6-month internship, recent graduate",
        "text": """
Maya Lin | maya@example.com | linkedin.com/in/mayalin
Professional Summary: Recent graduate and junior developer with 6-month software engineering internship experience.
Education: B.S. in Software Engineering, Class of 2024.
Experience:
Software Engineering Intern | NextGen Cloud | Jan 2024 - June 2024
- Assisted senior engineers in writing unit tests in Pytest and fixing bug tickets.
- Documented internal REST APIs using OpenAPI specifications.
Skills: Python, Git, HTML5, CSS3, Docker basics.
"""
    },
    {
        "id": 3,
        "true_level": "fresher",
        "description": "Entry-level trainee: Coursework and academic projects",
        "text": """
Rohan Das | rohan@example.com
Objective: Enthusiastic entry-level trainee seeking a junior backend developer position.
Education: Bachelor of Technology, 2024. Coursework: Operating Systems, Database Management, Data Structures.
Projects:
- Student Record Management System: CRUD application using Python and SQLite.
- Weather Dashboard: Academic project consuming public REST APIs.
Skills: Python, C++, SQL, Git.
"""
    },
    {
        "id": 4,
        "true_level": "fresher",
        "description": "Data Analyst Fresher: Recent grad with thesis and capstone",
        "text": """
Sneha Rao | sneha@example.com | github.com/sneharao
Summary: Motivated entry-level data analyst and recent graduate with strong passion for statistical modeling.
Education: B.S. in Statistics and Data Science, 2024. GPA: 3.8 / 4.0.
Capstone Project:
- Telecom Customer Churn Analysis: Cleaned 40k rows in Pandas, visualized trends in Tableau.
Skills: SQL, Excel, Python, Pandas, Tableau, R.
"""
    },
    {
        "id": 5,
        "true_level": "fresher",
        "description": "QA Apprentice / Trainee: Entry level testing coursework",
        "text": """
Kiran Verma | kiran@example.com
Summary: QA Apprentice trained in manual test case execution, STLC, and bug lifecycle reporting.
Education: Bachelor of Computer Applications, Class of 2024.
Projects & Training:
- Healthcare Portal Testing: Authored 50+ manual test cases in Jira and validated bug fixes.
Skills: Manual Testing, Test Cases, Bug Reporting, Jira, Postman basics, SQL.
"""
    },
    {
        "id": 6,
        "true_level": "fresher",
        "description": "Frontend Fresher: 5 React projects, portfolio link",
        "text": """
Liam Taylor | liam@example.com | liamtaylor.dev | github.com/liamtaylor
Summary: Creative junior frontend developer and recent college graduate. Built 5 responsive web applications.
Education: B.A. in Web Design & Computer Science, 2024.
Projects:
- Interactive Audio Visualizer: React, Web Audio API, Tailwind CSS.
- Task Tracker App: React hooks, LocalStorage, responsive CSS flexbox.
Skills: JavaScript, TypeScript, React, HTML5, CSS3, Git, Figma.
"""
    },
    {
        "id": 7,
        "true_level": "fresher",
        "description": "Strong Fresher: College TA, research project, 0 years",
        "text": """
Ananya Iyer | ananya@example.com | github.com/ananya-cs
Summary: Entry-level software engineer with strong theoretical foundation. Undergraduate Teaching Assistant for Data Structures.
Education: Bachelor of Science in Computer Science, 2024. CGPA: 3.92 / 4.0.
Academic Projects:
- Compiler for Subset of C: Lexical analysis and LL(1) parsing in Python.
- Real-Time Chat App: WebSocket server in Node.js with Redis pub/sub.
Skills: C++, Python, Algorithms, Linux, Git.
"""
    },

    # --- 7 MID-LEVELS ---
    {
        "id": 8,
        "true_level": "mid",
        "description": "Standard Mid: 3 years experience at SaaS company",
        "text": """
David Miller | david@example.com | github.com/dmiller
Summary: Backend Developer with 3+ years of experience building microservices and RESTful APIs in Python and FastAPI.
Work Experience:
Backend Software Engineer | CloudScale Systems | 2021 - Present (3 years)
- Developed and maintained 12 FastAPI microservices handling 1.5M daily requests.
- Optimized slow PostgreSQL queries with composite indexes, cutting latency by 35%.
- Integrated Redis caching layer for session management.
Education: B.S. in Computer Science, 2021.
Skills: Python, FastAPI, PostgreSQL, Redis, Docker, Git.
"""
    },
    {
        "id": 9,
        "true_level": "mid",
        "description": "Sparse Mid-Level: Brief bullets, no buzzword stuffing, 3 years exp",
        "text": """
Elena Rostova | elena@example.com
Experience:
Software Engineer | Alpha Corp | 2021 - Present (3 years of experience)
- Built internal APIs in Python.
- Maintained production MySQL databases and ran data migrations.
- Set up automated unit test suites with Pytest.
Education: Bachelor of Science, 2020.
Skills: Python, SQL, Linux, Git, REST APIs.
"""
    },
    {
        "id": 10,
        "true_level": "mid",
        "description": "DevOps Mid: 4 years exp, past role was junior sysadmin",
        "text": """
Carlos Gomez | carlos@example.com | linkedin.com/in/carlosg
Professional Summary: DevOps Engineer with 4 years hands-on experience in AWS infrastructure and CI/CD automation.
Work History:
DevOps Engineer | CloudBridge Inc | 2022 - Present
- Provisioned multi-tier VPCs and EKS clusters using Terraform.
- Managed Prometheus and Grafana dashboards for cluster observability.
Junior Systems Administrator | TechCare | 2020 - 2022
- Managed Linux production servers and configured bash cron backup scripts.
Education: B.S. in Information Systems, 2020.
"""
    },
    {
        "id": 11,
        "true_level": "mid",
        "description": "Frontend Mid: 3+ years experience, React/TypeScript",
        "text": """
Hannah Schmidt | hannah@example.com | github.com/hannah-frontend
Summary: Mid-level Frontend Engineer with 3+ years of hands-on experience building scalable SPAs.
Experience:
Frontend Developer | WebVibe Studio | 2021 - Present (3 years)
- Migrated legacy jQuery codebase to React and TypeScript.
- Architected reusable design system component library used across 4 internal products.
- Collaborated with UX team to ensure WCAG 2.1 AA accessibility compliance.
Education: B.S. in Computer Science, 2021.
"""
    },
    {
        "id": 12,
        "true_level": "mid",
        "description": "Data Analyst Mid: 4 years experience, BI reporting",
        "text": """
Rajesh Kulkarni | rajesh@example.com
Summary: Data Analyst with 4 years of experience delivering actionable business intelligence and KPI dashboards.
Work Experience:
Business Data Analyst | FinTech Global | 2020 - Present (4 years)
- Designed executive Power BI dashboards tracking monthly recurring revenue ($4.2M MRR).
- Wrote advanced SQL CTEs and window functions on Snowflake data warehouse.
- Partnered with product managers to define A/B testing experiment metrics.
Education: Bachelor of Commerce & Statistics, 2020.
"""
    },
    {
        "id": 13,
        "true_level": "mid",
        "description": "QA Mid: 2.5 years experience, test automation",
        "text": """
Chloe Bennett | chloe@example.com
Summary: QA Automation Engineer with 2.5 years experience designing automated regression testing frameworks.
Experience:
Test Automation Engineer | InsureTech | 2022 - Present (2.5 years)
- Built Selenium WebDriver and Pytest framework covering 120+ end-to-end user workflows.
- Integrated automated smoke test suite into GitHub Actions CI/CD pipeline.
- Triaged failed builds and logged reproducible bug tickets in Jira.
Education: B.S. in Computer Information Systems, 2021.
"""
    },
    {
        "id": 14,
        "true_level": "mid",
        "description": "Sparse Mid SRE: 4 years experience, on-call, concise text",
        "text": """
Vikram Nair | vikram@example.com
Summary: Site Reliability Engineer with 4 years experience supporting high-availability production systems.
Experience:
Site Reliability Engineer | Apex Streaming | 2020 - Present (4 years)
- Participated in 24/7 on-call rotation maintaining 99.9% platform availability.
- Configured Prometheus alerts and Grafana visualization dashboards.
- Maintained Docker containers and Kubernetes deployments.
Education: Bachelor of Engineering, 2020.
"""
    },

    # --- 6 SENIORS ---
    {
        "id": 15,
        "true_level": "senior",
        "description": "Senior AI Engineer: 7 years exp, PyTorch, RAG, mentoring",
        "text": """
Alex Chen | alex@example.com | github.com/alexchen
Summary: Senior AI Engineer with 7+ years of experience building deep learning systems and generative AI pipelines.
Experience:
Senior AI Engineer | Apex Cloud Solutions | 2020 - Present
- Architected enterprise hybrid RAG pipeline with vector databases reducing hallucinations by 40%.
- Fine-tuned open-source foundation models using LoRA and PEFT on distributed GPU cluster.
- Mentored 5 junior and mid-level machine learning engineers.
Senior Machine Learning Engineer | DataPulse | 2017 - 2020
- Built predictive NLP classification models in PyTorch.
Education: Master of Science in Computer Science, 2017.
"""
    },
    {
        "id": 16,
        "true_level": "senior",
        "description": "Staff Infrastructure Architect: 10+ years exp, multi-cloud",
        "text": """
Samantha Reed | samantha@example.com
Summary: Staff Infrastructure Architect with 10+ years of cloud engineering experience.
Work Experience:
Staff Cloud Architect | Enterprise Global | 2019 - Present
- Spearheaded enterprise multi-account AWS Landing Zone architecture managing $3M annual spend.
- Defined enterprise infrastructure-as-code standards using Terraform and Terragrunt.
Lead DevOps Engineer | Nexus Stream | 2014 - 2019
- Migrated 60+ legacy on-premises workloads to AWS ECS and Kubernetes.
Certifications: AWS Solutions Architect Professional, CKA.
Education: B.S. in Computer Engineering, 2013.
"""
    },
    {
        "id": 17,
        "true_level": "senior",
        "description": "Principal Software Engineer: 12 years exp, high throughput",
        "text": """
Marcus Vance | marcus@example.com
Summary: Principal Software Engineer with 12+ years of distributed systems engineering and microservice architecture.
Experience:
Principal Engineer | Apex Commerce | 2018 - Present
- Designed distributed transactional order engine processing 45,000 peak transactions per second.
- Led technical architecture across 4 distributed engineering squads.
Senior Backend Engineer | FinTech Corp | 2012 - 2018
- Built low-latency payment processing pipelines in Java and Go.
Education: B.S. in Computer Science, 2012.
"""
    },
    {
        "id": 18,
        "true_level": "senior",
        "description": "Lead Data Scientist: 8 years exp, predictive modeling",
        "text": """
Dr. Evelyn Harper | evelyn@example.com
Summary: Lead Data Scientist with 8+ years of production experience in machine learning, statistics, and team leadership.
Experience:
Lead Data Scientist | HealthAnalytics | 2020 - Present
- Directed 6 data scientists delivering clinical prediction algorithms with 94% ROC-AUC.
- Established MLOps continuous model retraining pipeline with MLflow.
Senior Data Scientist | BioTech Labs | 2016 - 2020
- Developed survival analysis models and patient stratification algorithms in Python and R.
Education: Ph.D. in Biostatistics, 2016.
"""
    },
    {
        "id": 19,
        "true_level": "senior",
        "description": "Senior QA Lead: 9 years exp, automated test architecture",
        "text": """
Rajiv Mehta | rajiv@example.com
Summary: Senior QA Lead with 9+ years experience architecting enterprise quality assurance frameworks.
Experience:
Senior Quality Assurance Lead | CoreBanking | 2019 - Present
- Architected enterprise automated testing framework reducing regression cycle from 5 days to 4 hours.
- Oversaw QA roadmap and automated test coverage across 14 microservice repositories.
Senior QA Engineer | FinTech Systems | 2015 - 2019
- Built Selenium and Cypress end-to-end automation test suites.
Education: B.Tech in Computer Science, 2015.
"""
    },
    {
        "id": 20,
        "true_level": "senior",
        "description": "Director of Engineering: 15 years exp, roadmap, hiring",
        "text": """
Thomas Wright | thomas@example.com
Summary: Director of Engineering with 15+ years of technology leadership scaling engineering organizations.
Experience:
Director of Engineering | CloudScale | 2018 - Present
- Managed organization of 45 engineers across platform, mobile, and backend teams.
- Drove technical strategy, hiring pipelines, architectural reviews, and SOC-2 compliance.
Lead Architect | TechGlobal | 2013 - 2018
- Architected global distributed data synchronization engine.
Senior Software Engineer | SystemWorks | 2009 - 2013
Education: M.S. in Computer Science, 2009.
"""
    }
]

def run_level_audit():
    ats = ATSService()

    levels = ["fresher", "mid", "senior"]
    matrix = {true_lvl: {pred_lvl: 0 for pred_lvl in levels} for true_lvl in levels}
    results = []
    correct_count = 0

    for item in TEST_SNIPPETS:
        text_lower = item["text"].lower()
        predicted = ats._detect_candidate_seniority(text_lower)
        true_lvl = item["true_level"]
        matrix[true_lvl][predicted] += 1
        is_correct = (predicted == true_lvl)
        if is_correct:
            correct_count += 1
        results.append({
            "id": item["id"],
            "description": item["description"],
            "true_level": true_lvl,
            "predicted_level": predicted,
            "correct": is_correct
        })

    accuracy = correct_count / len(TEST_SNIPPETS)

    print("\n=== LEVEL DETECTION ACCURACY AUDIT (20 TEST RESUMES) ===")
    print(f"Total Snippets: {len(TEST_SNIPPETS)}")
    print(f"Correct: {correct_count} / {len(TEST_SNIPPETS)} ({accuracy * 100:.1f}%)")
    print("\nConfusion Matrix (Rows: True, Cols: Predicted):")
    print(f"{'True \\ Pred':<12} | {'Fresher':<8} | {'Mid':<8} | {'Senior':<8}")
    print("-" * 44)
    for row_lvl in levels:
        print(f"{row_lvl.capitalize():<12} | {matrix[row_lvl]['fresher']:<8} | {matrix[row_lvl]['mid']:<8} | {matrix[row_lvl]['senior']:<8}")

    # Compute per-class precision and recall
    print("\nPer-Class Metrics:")
    for lvl in levels:
        tp = matrix[lvl][lvl]
        fn = sum(matrix[lvl][p] for p in levels if p != lvl)
        fp = sum(matrix[t][lvl] for t in levels if t != lvl)
        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
        print(f"  {lvl.capitalize():<8}: Precision = {prec:.2f}, Recall = {rec:.2f}, F1 = {f1:.2f} (Support = {tp + fn})")

    audit_payload = {
        "total_samples": len(TEST_SNIPPETS),
        "correct": correct_count,
        "accuracy": accuracy,
        "confusion_matrix": matrix,
        "detailed_results": results
    }

    out_path = os.path.join(backend_dir, "data", "level_detection_audit_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(audit_payload, f, indent=2)
    print(f"\nSaved audit results to {out_path}")

if __name__ == "__main__":
    run_level_audit()

"""
Unit Test: Resume vs Job Description (JD) Matcher
Validates:
1. Matching resume (Senior Backend -> Senior Backend JD) achieves high score (>= 80%).
2. Partial match (Junior Frontend -> Fullstack JD) achieves moderate score (~50-70%).
3. Mismatch resume (Cybersecurity -> Data Science JD) achieves low score (< 35%).
4. Verifies keyword gaps with placement advice and actionable resume edits.
"""

import pytest
from app.services.jd_matcher_service import jd_matcher_service

SAMPLE_BACKEND_JD = """
Job Title: Senior Backend Software Engineer
Company: CloudScale Platforms
Location: Remote

About the Role:
We are seeking an experienced Senior Backend Software Engineer to design, scale, and maintain our high-throughput microservices.

Basic Qualifications (Required):
- 4+ years of professional backend software development experience.
- Bachelor's degree in Computer Science, Software Engineering, or related technical field.
- Strong proficiency in Python, FastAPI, and PostgreSQL.
- Experience with Docker containerization and Redis caching.
- Solid understanding of RESTful API design and CI/CD pipelines.

Preferred Qualifications (Bonus):
- Experience with Kubernetes and Kafka event streaming.
- Familiarity with AWS cloud architecture and Terraform.
- Exposure to GraphQL and Celery task queues.
"""

SAMPLE_MATCHING_RESUME = """
David Miller | Senior Backend Developer | david.miller@example.com | github.com/dmiller

Summary:
Backend Software Engineer with 4+ years of production experience building distributed microservices,
optimizing relational databases, and scaling cloud applications. Expert in Python, FastAPI, and PostgreSQL.

Technical Skills:
- Languages & Frameworks: Python, FastAPI, SQL, REST APIs, Celery
- Databases & Caching: PostgreSQL, Redis, MongoDB
- Infrastructure: Docker, Git, CI/CD, GitHub Actions, AWS basics

Work Experience:
Senior Backend Engineer | CloudScale Systems | 2020 - Present (4 years)
- Architected and deployed 15+ microservices in Python and FastAPI serving 2M daily requests.
- Optimized slow PostgreSQL queries with composite indexes and connection pools, cutting P95 latency by 45%.
- Integrated Redis caching layer for authenticated session tokens, reducing DB load by 60%.
- Containerized development and production pipelines with Docker and automated testing in CI/CD.

Education:
Bachelor of Science in Computer Science, 2020 | GPA: 3.7 / 4.0
"""

SAMPLE_PARTIAL_RESUME = """
Jordan Smith | Frontend Developer | jordan.smith@example.com | github.com/jordansmith

Summary:
Junior Frontend Developer with 1.5 years experience building interactive web applications using React,
JavaScript, HTML5, and CSS3. Strong component architecture skills and Git workflows.

Skills:
- Frontend: React, JavaScript, TypeScript, HTML5, CSS3, Tailwind CSS
- Tools & Basics: Git, GitHub, Docker basics, REST APIs consumption

Projects:
- E-Commerce Web Store: Built responsive store frontend in React and Tailwind CSS.
- Task Manager App: CRUD application with client-side state and REST API endpoints.

Education:
Bachelor of Science in Information Technology, 2023 | GPA: 3.6 / 4.0
"""

SAMPLE_MISMATCH_RESUME = """
Marcus Vance | Cybersecurity Analyst | marcus.vance@example.com | linkedin.com/in/marcusvance

Professional Summary:
Dedicated Information Security Analyst with 4 years in SOC operations, incident response, packet analysis,
and vulnerability assessments. Skilled in Splunk, Wireshark, Snort, and network penetration testing.

Core Skills:
- Security: SIEM, Splunk, Wireshark, Incident Response, Vulnerability Assessment, Firewall Management, MITRE ATT&CK
- Systems: Kali Linux, Bash, Active Directory, IAM, Cryptography, Packet Capture

Work Experience:
Security Operations Center (SOC) Analyst | Vanguard Cyber Defense | 2020 - Present (4 years)
- Monitored security alerts in Splunk SIEM, triaging over 200 daily network anomalies and phishing attempts.
- Investigated suspicious packet captures using Wireshark, containing 12 potential malware incidents.
- Hardened internal Linux servers and configured iptables firewalls following CIS benchmarks.

Education & Certs:
B.S. in Cybersecurity | CompTIA Security+ Certified
"""

SAMPLE_DATA_SCIENCE_JD = """
Job Title: Senior Data Scientist / Machine Learning Engineer
Company: DeepPulse AI

Required Qualifications:
- 5+ years experience in statistical modeling, machine learning, and predictive analytics.
- Master's degree or PhD in Statistics, Machine Learning, Data Science, or related quantitative field.
- Deep expertise in Python, PyTorch, Scikit-Learn, Pandas, and NumPy.
- Experience building RAG pipelines and vector databases (Pinecone, FAISS).
- Demonstrated track record deploying models to production with Docker and FastAPI.

Preferred Qualifications:
- Experience with distributed GPU training (DeepSpeed, CUDA).
- Familiarity with MLOps and Weights & Biases.
"""

SAMPLE_FULLSTACK_JD = """
Job Title: Full Stack Developer (React & Node.js)
Company: WebMatrix Solutions
Experience: 2+ years of web development experience.
Education: Bachelor's degree in Computer Science, IT, or related field.

Required Skills (Must Have):
- 2+ years building web applications with React, JavaScript, HTML5, and CSS3.
- Hands-on experience developing RESTful APIs with Node.js or Python.
- Proficiency in Git, GitHub, and component-driven architecture.
- Experience with Docker containerization and client-side state management.

Preferred Skills (Nice to Have):
- Experience with Next.js, TypeScript, and Tailwind CSS.
- Familiarity with PostgreSQL or MongoDB databases.
"""

def test_matching_resume_scores_high():
    result = jd_matcher_service.match_resume_to_jd(SAMPLE_MATCHING_RESUME, SAMPLE_BACKEND_JD)
    
    print("\n--- Matching Resume Results ---")
    print(f"JD Match Score: {result.jd_match_score}/100")
    print(f"Must-Haves Matched: {result.matched_must_haves}")
    print(f"Semantic Similarity: {result.semantic_similarity_score}%")
    print(f"Experience Status: {result.experience_status}")

    assert result.jd_match_score >= 80, f"Expected matching resume to score >= 80, got {result.jd_match_score}"
    assert "Python" in result.matched_must_haves
    assert "FastAPI" in result.matched_must_haves
    assert "PostgreSQL" in result.matched_must_haves
    assert "Docker" in result.matched_must_haves
    assert "Requirement Met" in result.experience_status

def test_partial_resume_scores_moderate():
    result = jd_matcher_service.match_resume_to_jd(SAMPLE_PARTIAL_RESUME, SAMPLE_FULLSTACK_JD)
    
    print("\n--- Partial Match Resume Results ---")
    print(f"JD Match Score: {result.jd_match_score}/100")
    print(f"Must-Haves Matched: {result.matched_must_haves}")
    print(f"Must-Haves Missing: {result.missing_must_haves}")
    print(f"Experience Status: {result.experience_status}")

    assert 48 <= result.jd_match_score <= 75, f"Expected partial resume score 48-75, got {result.jd_match_score}"
    assert "React" in result.matched_must_haves
    assert "Git" in result.matched_must_haves
    assert len(result.missing_must_haves) > 0
    assert len(result.keyword_gaps_with_placement) > 0

def test_mismatch_resume_scores_low():
    result = jd_matcher_service.match_resume_to_jd(SAMPLE_MISMATCH_RESUME, SAMPLE_DATA_SCIENCE_JD)
    
    print("\n--- Mismatch Resume Results ---")
    print(f"JD Match Score: {result.jd_match_score}/100")
    print(f"Must-Haves Matched: {result.matched_must_haves}")
    print(f"Must-Haves Missing: {result.missing_must_haves}")
    print(f"Semantic Similarity: {result.semantic_similarity_score}%")

    assert result.jd_match_score <= 35, f"Expected mismatch resume to score <= 35, got {result.jd_match_score}"
    assert len(result.matched_must_haves) <= 2
    assert len(result.missing_must_haves) >= 4

if __name__ == "__main__":
    test_matching_resume_scores_high()
    test_partial_resume_scores_moderate()
    test_mismatch_resume_scores_low()
    print("\nAll JD Matcher tests PASSED.")

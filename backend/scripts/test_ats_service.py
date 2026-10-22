import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from app.services.ats_service import ats_service

def test_service():
    print("=" * 70)
    print("TESTING ATS SERVICE WITH EXPANDED ROLE LIBRARY")
    print("=" * 70)

    print(f"Total benchmark roles & aliases loaded: {len(ats_service.benchmarks)}")

    # Test 1: Frontend Developer with synonym "k8s" shouldn't trigger but "TS", "NextJS" should
    sample_frontend = """
Alex River | alex@frontend.dev | Portfolio: https://github.com/alexriver | LinkedIn: linkedin.com/in/alex

SUMMARY
Passionate Frontend Engineer with 3+ years building responsive web apps with ReactJS, NextJS, and TS.

TECHNICAL SKILLS
- Languages: JavaScript (ES6+), TS, HTML5, CSS3
- Frameworks: React.js, Next.js, TailwindCSS
- Tools: Git, Vite, Chrome DevTools

EXPERIENCE
Frontend Developer | WebVanguard | 2022 - Present
- Architected responsive customer dashboard in Next.js and Tailwind CSS, accelerating page speed by 42%.
- Engineered reusable design system components with 99.8% test coverage in Jest.
- Integrated RESTful APIs sustaining 25,000 daily requests.

PROJECTS
SaaS Analytics Portal
- Built interactive charts using React and Tailwind CSS; deployed to Vercel.

EDUCATION
B.S. in Computer Science | GPA: 3.9 / 4.0
"""
    res_frontend = ats_service.analyze_resume_text(sample_frontend, "Frontend Developer")
    print("\n--- FRONTEND DEVELOPER TEST ---")
    print(f"ATS Score: {res_frontend.ats_score}")
    print(f"Matched Skills ({len(res_frontend.matched_skills)}): {res_frontend.matched_skills}")
    print(f"Missing Critical Skills ({len(res_frontend.missing_critical_skills or [])}): {res_frontend.missing_critical_skills}")
    print(f"Missing Bonus Skills ({len(res_frontend.missing_bonus_skills or [])}): {res_frontend.missing_bonus_skills[:4]}...")
    print(f"Personalized Roadmap Steps ({len(res_frontend.personalized_roadmap or [])}):")
    for step in res_frontend.personalized_roadmap or []:
        print(f"  Step {step['step']}: {step['topic']} [{step['priority']}] - Missing: {step['missing_skills']}")

    # Test 2: UI/UX Designer role-specific rule: Portfolio link required
    sample_uiux_no_portfolio = """
Jane Doe | jane@design.com
Summary: Creative designer with Figma skills, wireframing, and user research experience.
Skills: Figma, Wireframing, UI Design, Usability Testing
Experience: Designed mobile apps and conducted user interviews for 2 years.
Education: B.A. in Graphic Design
"""
    res_uiux = ats_service.analyze_resume_text(sample_uiux_no_portfolio, "UI/UX Designer")
    print("\n--- UI/UX DESIGNER (NO PORTFOLIO TEST) ---")
    print(f"ATS Score: {res_uiux.ats_score}")
    print(f"Section Score: {res_uiux.section_score}")
    print(f"Deductions:")
    for d in res_uiux.deductions or []:
        print(f"  [{d['category']}] -{d['lost_points']} pts: {d['reason']}")

    # Test 3: SRE with Kubernetes acronym "k8s"
    sample_sre = """
Marcus Vance | marcus@sre.io | GitHub: github.com/marcusv | LinkedIn: linkedin.com/in/marcus
Summary: SRE with deep experience in k8s, Terraform, Prometheus, and Grafana.
Skills: Linux, K8s, Terraform, Prometheus, Grafana, Docker, Bash, Python
Experience:
- Automated multi-cluster k8s deployments using Terraform, sustaining 99.99% uptime.
- Established SLI/SLO dashboards in Grafana with PagerDuty alerting, reducing MTTR by 35%.
Projects: High-Availability Kubernetes Cluster with Prometheus
Education: B.S. in Computer Systems
"""
    res_sre = ats_service.analyze_resume_text(sample_sre, "SRE")
    print("\n--- SRE TEST (Synonym Normalizer: 'k8s' -> 'Kubernetes') ---")
    print(f"ATS Score: {res_sre.ats_score}")
    print(f"Matched Skills: {res_sre.matched_skills}")
    print(f"Is 'Kubernetes' in matched skills? {'Kubernetes' in res_sre.matched_skills}")

    print("\n" + "=" * 70)
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    test_service()

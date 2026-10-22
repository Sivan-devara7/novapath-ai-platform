import os
import re
import json

BENCHMARK_PATH = os.path.join(os.path.dirname(__file__), "generate_role_benchmarks.py")
roles_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "roles")

# Authoritative ONET metadata configuration
ONET_METADATA = {
    "Frontend Developer": {
        "code": "15-1254.00",
        "title": "Web Developers",
        "status": "reference_only",
        "match_type": "exact_match",
        "notes": "Exact match: Official SOC classification for web and frontend developers."
    },
    "Backend Developer": {
        "code": "15-1252.00",
        "title": "Software Developers",
        "status": "reference_only",
        "match_type": "exact_match",
        "notes": "Exact match: Official SOC classification for software developers building applications and services."
    },
    "Data Analyst": {
        "code": "15-2051.01",
        "title": "Business Intelligence Analysts",
        "status": "reference_only",
        "match_type": "exact_match",
        "notes": "Exact match: Official SOC classification for BI analysts and data analysts."
    },
    "Data Scientist/ML Engineer": {
        "code": "15-2051.00",
        "title": "Data Scientists",
        "status": "reference_only",
        "match_type": "exact_match",
        "notes": "Exact match: Official SOC classification for data scientists and ML modeling specialists."
    },
    "Mobile App Developer": {
        "code": "15-1252.00",
        "title": "Software Developers",
        "status": "reference_only",
        "match_type": "exact_match",
        "notes": "Exact match: Official SOC classification covering mobile application developers."
    },
    "QA/Test Automation Engineer": {
        "code": "15-1253.00",
        "title": "Software Quality Assurance Analysts and Testers",
        "status": "reference_only",
        "match_type": "exact_match",
        "notes": "Exact match: Official SOC classification for software QA and test automation engineers."
    },
    "Software Engineer (generic)": {
        "code": "15-1252.00",
        "title": "Software Developers",
        "status": "reference_only",
        "match_type": "exact_match",
        "notes": "Exact match: Official SOC classification for core software developers."
    },
    "SRE": {
        "code": None,
        "title": None,
        "status": "reference_only",
        "match_type": "no_direct_match",
        "notes": "No direct match: O*NET code 15-1244.00 is Network/Systems Administrators; Site Reliability Engineering is a software discipline and lacks an individual SOC code."
    },
    "Product Manager": {
        "code": None,
        "title": None,
        "status": "reference_only",
        "match_type": "no_direct_match",
        "notes": "No direct match: O*NET code 11-2021.00 is Marketing Managers, which is inaccurate for software product management. Tech PM lacks an official O*NET SOC code."
    },
    "UI/UX Designer": {
        "code": "15-1255.00",
        "title": "Web and Digital Interface Designers",
        "status": "reference_only",
        "match_type": "exact_match",
        "notes": "Exact match: Official SOC classification for UI, UX, and digital interface designers."
    },
    "Business Analyst": {
        "code": "13-1111.00",
        "title": "Management Analysts",
        "status": "reference_only",
        "match_type": "loose_match",
        "notes": "Loose match: Mapped to Management Analysts (13-1111.00); encompasses IT Business Analysts, BPMN process specialists, and requirements analysts."
    },
    "AI Engineer": {
        "code": "15-2051.00",
        "title": "Data Scientists",
        "status": "reference_only",
        "match_type": "loose_match",
        "notes": "Loose match: Mapped to Data Scientists (15-2051.00); modern LLM/GenAI systems engineering is an emerging field not yet separately distinguished in SOC taxonomy."
    },
    "Full Stack Developer": {
        "code": "15-1254.00",
        "title": "Web Developers",
        "status": "reference_only",
        "match_type": "exact_match",
        "notes": "Exact match: Official SOC classification for web and full stack developers."
    },
    "Cloud & DevOps Engineer": {
        "code": None,
        "title": None,
        "status": "reference_only",
        "match_type": "no_direct_match",
        "notes": "No direct match: Cloud infrastructure and DevOps automation currently lack a distinct standalone SOC code in O*NET."
    },
    "Data Engineer": {
        "code": "15-1243.00",
        "title": "Database Architects",
        "status": "reference_only",
        "match_type": "loose_match",
        "notes": "Loose match: Mapped to Database Architects (15-1243.00) as modern cloud data engineering and streaming pipelines lack an independent O*NET SOC code."
    },
    "Cybersecurity Analyst": {
        "code": "15-1212.00",
        "title": "Information Security Analysts",
        "status": "reference_only",
        "match_type": "exact_match",
        "notes": "Exact match: Official SOC classification for information security and cybersecurity analysts."
    }
}

# Update role JSON files on disk
for filename in os.listdir(roles_dir):
    if filename.endswith(".json"):
        filepath = os.path.join(roles_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        role_name = data.get("role")
        if role_name in ONET_METADATA:
            data["onet"] = ONET_METADATA[role_name]
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            print(f"Updated {filename}: ONET status = {data['onet']['status']} ({data['onet']['match_type']})")

print("\nSuccessfully updated all role JSON files with reference_only ONET metadata.")

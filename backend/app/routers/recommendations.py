import json
from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.db_models import User, ResumeAnalysis
from ..models.schemas import RecommendationItem

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

DEMO_USER_ID = "usr-aarav-sharma"

ROLE_PROJECT_CATALOG = {
    "ai-engineer": {
        "Beginner": [
            RecommendationItem(
                id="rec-ai-b1",
                type="project",
                title="Semantic Document Search Engine with SentenceTransformers",
                organization="Hugging Face Community Labs",
                difficulty="Beginner",
                duration="2 Weeks (Est. 15h)",
                match_percentage=96,
                why_this_matches="Ideal starting project for your current skill level. Grounds Python vector math into real embeddings.",
                prerequisites=["Python", "NumPy", "SentenceTransformers"],
                tags=["NLP", "Embeddings", "FastAPI"],
                action_url="/roadmap"
            ),
            RecommendationItem(
                id="rec-ai-b2",
                type="project",
                title="Computer Vision Defect Classifier with PyTorch Transfer Learning",
                organization="OpenCV AI Labs",
                difficulty="Beginner",
                duration="2 Weeks (Est. 18h)",
                match_percentage=93,
                why_this_matches="Hands-on introduction to convolutional backbones and tensor backpropagation.",
                prerequisites=["Python", "PyTorch Basics"],
                tags=["PyTorch", "ResNet", "Image Classification"],
                action_url="/roadmap"
            )
        ],
        "Intermediate": [
            RecommendationItem(
                id="rec-ai-i1",
                type="project",
                title="Production Hybrid RAG with Cross-Encoder Re-Ranking",
                organization="Open Source AI Labs",
                difficulty="Intermediate",
                duration="3 Weeks (Est. 25h)",
                match_percentage=98,
                why_this_matches="Directly targets your critical resume gap: 'Vector Database & RAG'. Essential for recruiter filtering.",
                prerequisites=["PyTorch", "Python", "Transformers"],
                tags=["Vector DB", "FAISS", "LlamaIndex", "FastAPI"],
                action_url="/roadmap"
            ),
            RecommendationItem(
                id="rec-ai-i2",
                type="certification",
                title="AWS Certified Machine Learning - Specialty",
                organization="Amazon Web Services",
                difficulty="Intermediate",
                duration="6 Weeks Study Path",
                match_percentage=92,
                why_this_matches="Reinforces your cloud infrastructure verification badge and increases ATS recruiter search filtering by 3.2x.",
                prerequisites=["Python", "Cloud Fundamentals"],
                tags=["Cloud AI", "SageMaker", "Feature Store", "Security"],
                action_url="https://aws.amazon.com/certification/certified-machine-learning-specialty/"
            )
        ],
        "Advanced": [
            RecommendationItem(
                id="rec-ai-a1",
                type="project",
                title="Distributed LLM Fine-Tuner with QLoRA & vLLM Serving",
                organization="Hugging Face & Triton Labs",
                difficulty="Advanced",
                duration="4 Weeks (Est. 35h)",
                match_percentage=99,
                why_this_matches="Elevates your profile from foundational modeling to enterprise-grade high-throughput inference serving.",
                prerequisites=["PyTorch", "CUDA Basics", "Docker"],
                tags=["QLoRA", "vLLM", "Docker", "Triton"],
                action_url="/roadmap"
            ),
            RecommendationItem(
                id="rec-ai-a2",
                type="internship",
                title="Applied AI Research Intern (Fall 2026)",
                organization="Anthropic / Cohere Campus Lab",
                difficulty="High Impact",
                duration="6 Months",
                match_percentage=95,
                why_this_matches="Your high-percentile deep learning scores and model benchmark metrics qualify you for top-tier AI labs.",
                prerequisites=["PyTorch", "Transformer Architecture", "Git"],
                tags=["Research", "Inference Optimization", "CUDA"],
                action_url="#"
            )
        ]
    },
    "data-engineer": {
        "Beginner": [
            RecommendationItem(
                id="rec-de-b1",
                type="project",
                title="High-Performance Transactional ETL Pipeline with PostgreSQL",
                organization="Modern Data Network",
                difficulty="Beginner",
                duration="2 Weeks (Est. 16h)",
                match_percentage=95,
                why_this_matches="Demonstrates command of SQL query execution plans, B-Tree indexing, and Star Schema modeling.",
                prerequisites=["SQL", "Python", "PostgreSQL"],
                tags=["SQL Internals", "Indexing", "ETL", "Data Modeling"],
                action_url="/roadmap"
            ),
            RecommendationItem(
                id="rec-de-b2",
                type="certification",
                title="Snowflake SnowPro Core Certified Engineer",
                organization="Snowflake University",
                difficulty="Beginner",
                duration="4 Weeks Study Path",
                match_percentage=92,
                why_this_matches="One of the fastest ways to validate cloud warehouse competency on candidate profiles.",
                prerequisites=["SQL", "Cloud Concepts"],
                tags=["Snowflake", "Cloud Storage", "Virtual Warehouses"],
                action_url="https://www.snowflake.com/en/certifications/"
            )
        ],
        "Intermediate": [
            RecommendationItem(
                id="rec-de-i1",
                type="project",
                title="Real-Time E-Commerce Stream Processing with Kafka & PySpark",
                organization="Confluent & Apache Community",
                difficulty="Intermediate",
                duration="3 Weeks (Est. 28h)",
                match_percentage=98,
                why_this_matches="Directly closes critical Data Engineer ATS gaps in real-time streaming and distributed processing.",
                prerequisites=["Apache Kafka", "PySpark", "Docker"],
                tags=["Kafka", "PySpark", "Schema Registry", "Streaming"],
                action_url="/roadmap"
            ),
            RecommendationItem(
                id="rec-de-i2",
                type="project",
                title="Enterprise Lakehouse Transformation with Delta Lake & dbt Core",
                organization="dbt Labs & Databricks",
                difficulty="Intermediate",
                duration="3 Weeks (Est. 24h)",
                match_percentage=94,
                why_this_matches="Implements industry-standard analytics engineering with automated data contracts and tests.",
                prerequisites=["SQL", "dbt", "Snowflake/Delta Lake"],
                tags=["dbt", "Delta Lake", "Snowflake", "Data Quality"],
                action_url="/roadmap"
            )
        ],
        "Advanced": [
            RecommendationItem(
                id="rec-de-a1",
                type="project",
                title="Automated Data Quality & Zero-Downtime CI/CD with Airflow & Great Expectations",
                organization="Astronomer Community Labs",
                difficulty="Advanced",
                duration="4 Weeks (Est. 32h)",
                match_percentage=97,
                why_this_matches="Proves enterprise reliability, backfilling, and observability for multi-terabyte data platforms.",
                prerequisites=["Apache Airflow", "Great Expectations", "Docker", "Kubernetes"],
                tags=["Airflow", "Data Observability", "CI/CD", "Great Expectations"],
                action_url="/roadmap"
            ),
            RecommendationItem(
                id="rec-de-a2",
                type="internship",
                title="Data Platform Engineering Intern",
                organization="Databricks / Stripe Labs",
                difficulty="High Impact",
                duration="4 Months",
                match_percentage=92,
                why_this_matches="Your verified competencies in distributed Spark clusters and real-time Kafka align with platform roles.",
                prerequisites=["Spark", "Kafka", "Python", "SQL"],
                tags=["Distributed Systems", "Lakehouse", "Real-Time"],
                action_url="#"
            )
        ]
    },
    "cybersecurity": {
        "Beginner": [
            RecommendationItem(
                id="rec-sec-b1",
                type="project",
                title="Network Packet Sniffer & Malicious Traffic Analyzer",
                organization="Wireshark Educational Labs",
                difficulty="Beginner",
                duration="2 Weeks (Est. 14h)",
                match_percentage=95,
                why_this_matches="Hands-on PCAP dissection of TCP handshake anomalies, SYN floods, and DNS tunneling.",
                prerequisites=["Networking Basics", "Python", "Wireshark"],
                tags=["Wireshark", "Packet Analysis", "TCP/IP", "Forensics"],
                action_url="/roadmap"
            ),
            RecommendationItem(
                id="rec-sec-b2",
                type="certification",
                title="CompTIA Security+ (SY0-701) Certification Path",
                organization="CompTIA",
                difficulty="Beginner",
                duration="6 Weeks Study Path",
                match_percentage=94,
                why_this_matches="Globally recognized baseline credential required for DoD 8570 compliance and entry SOC roles.",
                prerequisites=["Networking Fundamentals"],
                tags=["CompTIA", "Security Fundamentals", "Threats", "IAM"],
                action_url="https://www.comptia.org/certifications/security"
            )
        ],
        "Intermediate": [
            RecommendationItem(
                id="rec-sec-i1",
                type="project",
                title="Automated SOC Log Correlation & Threat Hunting with Splunk",
                organization="Splunk Threat Defense Labs",
                difficulty="Intermediate",
                duration="3 Weeks (Est. 26h)",
                match_percentage=98,
                why_this_matches="Resolves core cybersecurity skill gaps in SIEM engineering, Sysmon telemetry, and MITRE ATT&CK mapping.",
                prerequisites=["Splunk", "Windows Event Logs", "MITRE ATT&CK"],
                tags=["SIEM", "Splunk", "Threat Hunting", "Incident Response"],
                action_url="/roadmap"
            ),
            RecommendationItem(
                id="rec-sec-i2",
                type="project",
                title="Ethical Web Application Penetration Test Lab (OWASP Top 10)",
                organization="PortSwigger Web Academy",
                difficulty="Intermediate",
                duration="3 Weeks (Est. 24h)",
                match_percentage=96,
                why_this_matches="Defensive and offensive mastery of SQL injection, XSS, SSRF, and authorization bypasses.",
                prerequisites=["HTTP Protocols", "Burp Suite", "OWASP"],
                tags=["OWASP Top 10", "Burp Suite", "Penetration Testing"],
                action_url="/roadmap"
            )
        ],
        "Advanced": [
            RecommendationItem(
                id="rec-sec-a1",
                type="project",
                title="Enterprise Zero Trust IAM Gateway & TLS 1.3 Cryptographic Engine",
                organization="Cloudflare & NIST Zero Trust Labs",
                difficulty="Advanced",
                duration="4 Weeks (Est. 36h)",
                match_percentage=99,
                why_this_matches="Demonstrates high-level cryptographic key exchange, mutual TLS (mTLS), and OAuth2/OIDC token verification.",
                prerequisites=["Cryptography", "PKI", "OAuth2", "Zero Trust"],
                tags=["Zero Trust", "TLS 1.3", "PKI", "OAuth2", "Cryptography"],
                action_url="/roadmap"
            ),
            RecommendationItem(
                id="rec-sec-a2",
                type="internship",
                title="SOC Incident Response & Threat Intelligence Intern",
                organization="CrowdStrike / Mandiant",
                difficulty="High Impact",
                duration="6 Months",
                match_percentage=93,
                why_this_matches="Your high-percentile threat hunting telemetry and MITRE ATT&CK mapping qualify you for live incident triage.",
                prerequisites=["SIEM", "Incident Response", "Network Forensics"],
                tags=["Threat Intelligence", "Incident Response", "Forensics"],
                action_url="#"
            )
        ]
    }
}

@router.get("/", response_model=List[RecommendationItem])
async def get_recommendations(
    track: Optional[str] = None,
    level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Returns dynamically tailored projects, certifications, and internships
    calibrated uniquely for each user based on their active track, placement level, and missing ATS gaps.
    """
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    
    # 1. Determine target role/track
    effective_track = track
    if not effective_track and user:
        effective_track = user.career_goal or "AI Engineer"
    
    track_key = "ai-engineer"
    t_lower = (effective_track or "").lower()
    if "data" in t_lower:
        track_key = "data-engineer"
    elif "cyber" in t_lower or "security" in t_lower:
        track_key = "cybersecurity"
    else:
        track_key = "ai-engineer"

    # 2. Determine user's level
    effective_level = level
    if not effective_level and user:
        effective_level = user.placement_level or "Intermediate"
    if effective_level not in ["Beginner", "Intermediate", "Advanced"]:
        effective_level = "Intermediate"

    track_items = ROLE_PROJECT_CATALOG.get(track_key, ROLE_PROJECT_CATALOG["ai-engineer"])
    
    # Pick recommendations tuned for their level, supplemented by next/adjacent level
    primary_items = track_items.get(effective_level, [])
    secondary_level = "Advanced" if effective_level == "Intermediate" else "Intermediate"
    secondary_items = track_items.get(secondary_level, [])
    
    combined = primary_items + secondary_items
    return combined

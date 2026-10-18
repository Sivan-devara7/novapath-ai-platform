import json
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from ..config import settings
from ..models.db_models import (
    Base,
    User,
    Course,
    Module,
    UserModuleProgress,
    XPEvent,
)

logger = logging.getLogger("novapath.database")


# ---------------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------------

def get_database_url() -> str:
    """
    Resolve the database URL.

    Production:
        Use PostgreSQL configured through DATABASE_URL.

    Local development:
        Use SQLite if DATABASE_URL is not configured.

    SQLite on serverless:
        Use /tmp for a temporary database rather than attempting
        to write into Vercel's read-only application directory.
    """
    database_url = settings.effective_database_url.strip()

    if database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql+psycopg://",
            1,
        )

    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    elif database_url.startswith("sqlite:///"):
        # Never use the deployed application directory for SQLite.
        # SQLite stored in /tmp is temporary and is not persistent.
        import os

        if os.environ.get("VERCEL") == "1":
            database_url = "sqlite:////tmp/novapath.db"

    return database_url


DATABASE_URL = get_database_url()

connect_args = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
    echo=False,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ---------------------------------------------------------
# DATABASE SESSION
# ---------------------------------------------------------

def get_db():
    """
    FastAPI dependency for database session management.
    """
    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------
# COURSE AND MODULE SEED DATA
# ---------------------------------------------------------

AI_ENGINEER_MODULES = [
    {
        "id": "py-foundations",
        "order_index": 1,
        "title": "Python & Modern Software Engineering for AI",
        "summary": (
            "Object-oriented patterns, vector operations, asynchronous "
            "processing, and clean code principles."
        ),
        "estimated_hours": 12,
        "lessons_count": 5,
        "skills": [
            "Python 3.12",
            "Type Hints",
            "AsyncIO",
            "OOP",
            "Data Structures",
        ],
        "difficulty": "Beginner",
        "topics": [
            "Python Basics",
            "Data Structures",
            "OOP & Decorators",
            "AsyncIO",
            "Profiling",
        ],
        "learning_objectives": [
            "Write idiomatic type-safe Python",
            "Understand asynchronous I/O",
            "Benchmark vector performance",
        ],
    },
    {
        "id": "math-ml",
        "order_index": 2,
        "title": "Linear Algebra, Calculus & Probabilistic Modeling",
        "summary": (
            "Matrix decompositions, gradients, probability distributions, "
            "and the mathematical foundations of ML."
        ),
        "estimated_hours": 16,
        "lessons_count": 6,
        "skills": [
            "Linear Algebra",
            "Matrix Calculus",
            "Probability",
            "Optimization",
            "Loss Landscapes",
        ],
        "difficulty": "Beginner",
        "topics": [
            "Matrices & Tensors",
            "Eigenvalues & SVD",
            "Gradients & Hessians",
            "Probability Distributions",
            "Convex Optimization",
        ],
        "learning_objectives": [
            "Compute analytical matrix derivatives",
            "Interpret SVD decompositions",
            "Understand loss surfaces",
        ],
    },
    {
        "id": "classical-ml",
        "order_index": 3,
        "title": "Classical Machine Learning & Statistical Learning",
        "summary": (
            "Tree-based ensembles, SVMs, clustering, cross-validation, "
            "and bias-variance tradeoff."
        ),
        "estimated_hours": 18,
        "lessons_count": 6,
        "skills": [
            "Scikit-Learn",
            "XGBoost",
            "Feature Engineering",
            "Ensembles",
            "Cross-Validation",
        ],
        "difficulty": "Intermediate",
        "topics": [
            "Linear & Logistic Regression",
            "Decision Trees & Ensembles",
            "SVMs",
            "Clustering & PCA",
            "Evaluation Metrics",
        ],
        "learning_objectives": [
            "Train high-accuracy tree ensembles",
            "Prevent data leakage",
            "Diagnose overfitting",
        ],
    },
    {
        "id": "deep-learning",
        "order_index": 4,
        "title": "Deep Neural Networks, CNNs & Sequence Models",
        "summary": (
            "PyTorch tensor operations, backpropagation from scratch, "
            "convolutional networks, and attention."
        ),
        "estimated_hours": 24,
        "lessons_count": 8,
        "skills": [
            "PyTorch",
            "Backpropagation",
            "CNNs",
            "Transformers",
            "Regularization",
        ],
        "difficulty": "Intermediate",
        "topics": [
            "Feedforward Networks",
            "PyTorch Autograd",
            "CNN Architectures",
            "Attention Mechanisms",
            "Transformer Encoder/Decoder",
        ],
        "learning_objectives": [
            "Implement custom PyTorch modules",
            "Debug gradient saturation",
            "Fine-tune modern Transformer backbones",
        ],
    },
    {
        "id": "rag-systems",
        "order_index": 5,
        "title": "Retrieval-Augmented Generation & Vector Databases",
        "summary": (
            "Dense passage retrieval, hybrid search, FAISS/Chroma "
            "index strategies, and reranking pipelines."
        ),
        "estimated_hours": 20,
        "lessons_count": 6,
        "skills": [
            "RAG Architecture",
            "Vector Embeddings",
            "FAISS",
            "Cross-Encoders",
            "Prompt Grounding",
        ],
        "difficulty": "Advanced",
        "topics": [
            "Embedding Models",
            "Chunking Strategies",
            "Vector Indexing (HNSW)",
            "Hybrid Retrieval",
            "Evaluation & Hallucination Mitigation",
        ],
        "learning_objectives": [
            "Build production-grade RAG indexes",
            "Implement hybrid lexical-dense reranking",
            "Ground LLM generation",
        ],
    },
    {
        "id": "mlops-deploy",
        "order_index": 6,
        "title": "MLOps, Model Serving & Scalable Inference",
        "summary": (
            "Containerized model runtimes, Triton/vLLM serving, "
            "latency optimization, and automated CI/CD pipelines."
        ),
        "estimated_hours": 22,
        "lessons_count": 7,
        "skills": [
            "Docker",
            "FastAPI Serving",
            "Model Monitoring",
            "Drift Detection",
            "vLLM / Triton",
        ],
        "difficulty": "Advanced",
        "topics": [
            "FastAPI Serving Runtimes",
            "Docker Containerization",
            "Model Quantization & ONNX",
            "Data & Concept Drift",
            "CI/CD Deployment Pipelines",
        ],
        "learning_objectives": [
            "Deploy high-throughput inference endpoints",
            "Quantize weights for low latency",
            "Monitor models in production",
        ],
    },
]

DATA_ENGINEER_MODULES = [
    {
        "id": "de-sql-internals",
        "order_index": 1,
        "title": "Advanced SQL Internals, Indexing & Data Modeling",
        "summary": (
            "Query execution plans, B-Tree & hash indexes, window "
            "functions, and dimensional modeling."
        ),
        "estimated_hours": 14,
        "lessons_count": 5,
        "skills": [
            "Advanced SQL",
            "Query Planning",
            "B-Tree Indexing",
            "Dimensional Modeling",
            "PostgreSQL Internals",
        ],
        "difficulty": "Beginner",
        "topics": [
            "Query Execution Plans",
            "EXPLAIN ANALYZE",
            "Window Functions & CTEs",
            "Star & Snowflake Schema",
            "Data Vault 2.0",
        ],
        "learning_objectives": [
            "Analyze query execution plans",
            "Structure high-performance dimensional schemas",
            "Eliminate full table scans",
        ],
    },
    {
        "id": "de-distributed-spark",
        "order_index": 2,
        "title": "Distributed Computing with Apache Spark & PySpark",
        "summary": (
            "RDD internals, Catalyst Optimizer, Tungsten execution engine, "
            "DataFrame transformations, broadcast joins, and memory tuning."
        ),
        "estimated_hours": 20,
        "lessons_count": 7,
        "skills": [
            "Apache Spark",
            "PySpark",
            "Catalyst Optimizer",
            "Broadcast Joins",
            "Memory Tuning",
        ],
        "difficulty": "Intermediate",
        "topics": [
            "Spark Architecture & DAGs",
            "DataFrame & Dataset APIs",
            "Catalyst Optimizer Internals",
            "Shuffle & Partitioning Strategy",
            "PySpark Cluster Tuning",
        ],
        "learning_objectives": [
            "Write optimized PySpark batch transformations",
            "Tune partition counts to prevent data skew",
            "Diagnose memory spill issues",
        ],
    },
    {
        "id": "de-streaming-kafka",
        "order_index": 3,
        "title": "Real-Time Event Streaming with Apache Kafka",
        "summary": (
            "Distributed commit logs, partition leader election, "
            "producer idempotence, consumer groups, and stream processing."
        ),
        "estimated_hours": 18,
        "lessons_count": 6,
        "skills": [
            "Apache Kafka",
            "Event Streaming",
            "Schema Registry",
            "Avro/Protobuf",
            "Consumer Groups",
        ],
        "difficulty": "Intermediate",
        "topics": [
            "Commit Log Architecture",
            "Partitions & Replication",
            "Exactly-Once Semantics",
            "Kafka Streams",
            "Schema Registry Evolution",
        ],
        "learning_objectives": [
            "Configure fault-tolerant Kafka clusters",
            "Implement idempotent producer patterns",
            "Evolve Avro schemas safely",
        ],
    },
    {
        "id": "de-lakehouse-dbt",
        "order_index": 4,
        "title": "Modern Cloud Lakehouse, Snowflake & dbt Core",
        "summary": (
            "Delta Lake ACID transactions, Parquet columnar format, "
            "Snowflake virtual warehouses, and dbt transformations."
        ),
        "estimated_hours": 22,
        "lessons_count": 7,
        "skills": [
            "Snowflake",
            "dbt Core",
            "Delta Lake",
            "Parquet Format",
            "Analytics Engineering",
        ],
        "difficulty": "Advanced",
        "topics": [
            "ACID on Object Storage",
            "Delta Log & Time Travel",
            "Snowflake Micro-Partitioning",
            "dbt Models, Tests & Docs",
            "Materializations & Jinja",
        ],
        "learning_objectives": [
            "Build modular DAGs using dbt",
            "Implement automated data contract testing",
            "Optimize Snowflake credit consumption",
        ],
    },
    {
        "id": "de-orchestration-airflow",
        "order_index": 5,
        "title": "Production Pipeline Orchestration with Apache Airflow & Data Quality",
        "summary": (
            "Dynamic DAG authoring, custom operators, executors, "
            "automated backfilling, and data quality validation."
        ),
        "estimated_hours": 16,
        "lessons_count": 6,
        "skills": [
            "Apache Airflow",
            "Data Observability",
            "Great Expectations",
            "CI/CD Data Pipelines",
            "Docker",
        ],
        "difficulty": "Advanced",
        "topics": [
            "Airflow Scheduler & Executors",
            "Dynamic DAG Authoring",
            "Sensor & Branching Patterns",
            "Data Contracts & Quality Tests",
            "Production Monitoring & Alerting",
        ],
        "learning_objectives": [
            "Author idempotent production DAGs",
            "Deploy automated data assertions",
            "Implement zero-downtime pipeline deployments",
        ],
    },
]

CYBERSECURITY_MODULES = [
    {
        "id": "sec-network-fundamentals",
        "order_index": 1,
        "title": "Network Security, Packet Forensics & Perimeter Defense",
        "summary": (
            "Packet analysis, TCP handshake analysis, firewalls, "
            "IDS/IPS, and secure VPN tunneling."
        ),
        "estimated_hours": 14,
        "lessons_count": 5,
        "skills": [
            "Wireshark",
            "TCP/IP Protocols",
            "Network Forensics",
            "Firewalls",
            "IDS/IPS",
        ],
        "difficulty": "Beginner",
        "topics": [
            "OSI Model & Packet Anatomy",
            "Wireshark PCAP Analysis",
            "TCP Flag Anomalies",
            "Next-Gen Firewalls",
            "Snort & Suricata Signatures",
        ],
        "learning_objectives": [
            "Identify malicious traffic patterns in PCAP captures",
            "Configure Snort IDS detection rules",
            "Audit firewall access control lists",
        ],
    },
    {
        "id": "sec-threat-hunting",
        "order_index": 2,
        "title": "SIEM Operations, Threat Hunting & MITRE ATT&CK",
        "summary": (
            "Security event log correlation, MITRE ATT&CK mapping, "
            "and incident triage."
        ),
        "estimated_hours": 20,
        "lessons_count": 6,
        "skills": [
            "SIEM",
            "Splunk",
            "MITRE ATT&CK",
            "Threat Intelligence",
            "Incident Response",
        ],
        "difficulty": "Intermediate",
        "topics": [
            "Windows Event Logs & Sysmon",
            "Splunk SPL Query Optimization",
            "MITRE TTP Mapping",
            "IoC vs Pyramid of Pain",
            "Playbook Automation (SOAR)",
        ],
        "learning_objectives": [
            "Correlate multi-stage attack vectors across SIEM logs",
            "Map adversary behavior to MITRE techniques",
            "Execute containment and eradication playbooks",
        ],
    },
    {
        "id": "sec-vuln-pentesting",
        "order_index": 3,
        "title": "Vulnerability Assessment & Offensive Penetration Testing",
        "summary": (
            "Ethical web security testing, vulnerability assessment, "
            "and remediation reporting."
        ),
        "estimated_hours": 22,
        "lessons_count": 7,
        "skills": [
            "OWASP Top 10",
            "Burp Suite",
            "Nmap",
            "Penetration Testing",
            "Vulnerability Assessment",
        ],
        "difficulty": "Intermediate",
        "topics": [
            "Active & Passive Reconnaissance",
            "SQL Injection & XSS",
            "SSRF & IDOR Vulnerabilities",
            "Linux/Windows Privilege Escalation",
            "CVSS Scoring & Reporting",
        ],
        "learning_objectives": [
            "Conduct ethical web vulnerability audits",
            "Exploit and remediate OWASP Top 10 flaws",
            "Write executive and technical penetration test reports",
        ],
    },
    {
        "id": "sec-iam-crypto",
        "order_index": 4,
        "title": "Applied Cryptography, PKI & Zero Trust Identity",
        "summary": (
            "Symmetric and asymmetric cryptography, TLS, certificates, "
            "OAuth 2.0, OIDC, and Zero Trust."
        ),
        "estimated_hours": 18,
        "lessons_count": 6,
        "skills": [
            "Cryptography",
            "PKI & Certificates",
            "OAuth 2.0",
            "Zero Trust",
            "IAM",
        ],
        "difficulty": "Advanced",
        "topics": [
            "AES-GCM & RSA/ECC Mathematics",
            "TLS 1.3 Key Exchange",
            "Certificate Authority & CRL",
            "OAuth 2.0 Grant Flows & JWTs",
            "Zero Trust Verification Models",
        ],
        "learning_objectives": [
            "Implement cryptographic key management",
            "Configure OAuth2 / OIDC authentication",
            "Architect Zero Trust verification models",
        ],
    },
    {
        "id": "sec-cloud-governance",
        "order_index": 5,
        "title": "Cloud Infrastructure Security & Compliance Governance",
        "summary": (
            "Cloud IAM, audit logs, container hardening, benchmarks, "
            "and security compliance."
        ),
        "estimated_hours": 16,
        "lessons_count": 5,
        "skills": [
            "AWS Cloud Security",
            "Container Hardening",
            "CIS Benchmarks",
            "ISO 27001 / SOC2",
            "CSPM",
        ],
        "difficulty": "Advanced",
        "topics": [
            "Cloud Shared Responsibility Model",
            "AWS IAM Policy Evaluation Logic",
            "Docker Security & Seccomp Profiles",
            "Infrastructure as Code Scanning",
            "Audit Compliance & SOC2 Evidence",
        ],
        "learning_objectives": [
            "Harden cloud infrastructure",
            "Implement container runtime security policies",
            "Evaluate CIS benchmark and SOC2 controls",
        ],
    },
]


COURSES = [
    {
        "id": "ai-engineer",
        "title": "AI Engineer & ML Systems Career Track",
        "description": (
            "Master modern artificial intelligence, deep learning architectures, "
            "RAG pipelines, and MLOps deployment."
        ),
        "target_role": "AI Engineer",
        "modules": AI_ENGINEER_MODULES,
    },
    {
        "id": "data-engineer",
        "title": "Data Engineering & Modern Lakehouse Architecture",
        "description": (
            "Master distributed pipelines, SQL internals, Apache Spark, Kafka, "
            "Snowflake, and dbt analytics engineering."
        ),
        "target_role": "Data Engineer",
        "modules": DATA_ENGINEER_MODULES,
    },
    {
        "id": "cybersecurity",
        "title": "Cybersecurity Defense, Threat Intelligence & SOC Ops",
        "description": (
            "Master defensive security, network analysis, SIEM/SOC operations, "
            "ethical penetration testing, IAM, and cryptography."
        ),
        "target_role": "Cybersecurity Analyst",
        "modules": CYBERSECURITY_MODULES,
    },
]


# ---------------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------------

def init_db():
    """
    Create tables and seed courses/modules/demo user.

    PostgreSQL is recommended for Vercel production.
    SQLite in /tmp is only a temporary fallback and must not be
    treated as persistent storage.
    """
    if (
        DATABASE_URL.startswith("sqlite")
        and __import__("os").environ.get("VERCEL") == "1"
    ):
        logger.warning(
            "Using temporary SQLite storage on Vercel. "
            "Data may be lost between executions. Configure DATABASE_URL "
            "to use PostgreSQL for persistent storage."
        )

    logger.info("Initializing NovaPath database.")

    try:
        Base.metadata.create_all(bind=engine)

        with SessionLocal() as db:
            for course_data in COURSES:
                course = (
                    db.query(Course)
                    .filter(Course.id == course_data["id"])
                    .first()
                )

                if course is None:
                    course = Course(
                        id=course_data["id"],
                        title=course_data["title"],
                        description=course_data["description"],
                        target_role=course_data["target_role"],
                    )
                    db.add(course)
                    db.flush()

                for module_data in course_data["modules"]:
                    existing_module = (
                        db.query(Module)
                        .filter(Module.id == module_data["id"])
                        .first()
                    )

                    if existing_module is not None:
                        continue

                    module = Module(
                        id=module_data["id"],
                        course_id=course_data["id"],
                        order_index=module_data["order_index"],
                        title=module_data["title"],
                        summary=module_data["summary"],
                        estimated_hours=module_data["estimated_hours"],
                        lessons_count=module_data["lessons_count"],
                        skills_json=json.dumps(module_data["skills"]),
                        difficulty=module_data["difficulty"],
                        topics_json=json.dumps(module_data["topics"]),
                        learning_objectives_json=json.dumps(
                            module_data["learning_objectives"]
                        ),
                    )
                    db.add(module)

            # Create demo user only if it does not already exist.
            demo_user = (
                db.query(User)
                .filter(User.id == "usr-aarav-sharma")
                .first()
            )

            if demo_user is None:
                demo_user = User(
                    id="usr-aarav-sharma",
                    name="Aarav Sharma",
                    email="aarav.sharma@vizag.edu",
                    hashed_password="mock-hashed-password",
                    role="student",
                    career_goal="AI Engineer",
                    avatar=(
                        "https://images.unsplash.com/"
                        "photo-1534528741775-53994a69daeb"
                        "?w=150&auto=format&fit=crop&q=80"
                    ),
                    placement_level="Intermediate",
                    placement_score=68.5,
                    streak=14,
                    total_xp=860,
                    mastery_overall=72,
                    radar_data_json=json.dumps([
                        {
                            "subject": "Deep Learning",
                            "A": 85,
                            "fullMark": 100,
                        },
                        {
                            "subject": "System Design",
                            "A": 65,
                            "fullMark": 100,
                        },
                        {
                            "subject": "Algorithms",
                            "A": 90,
                            "fullMark": 100,
                        },
                        {
                            "subject": "MLOps",
                            "A": 55,
                            "fullMark": 100,
                        },
                        {
                            "subject": "Cloud & Infra",
                            "A": 70,
                            "fullMark": 100,
                        },
                        {
                            "subject": "Applied RAG",
                            "A": 68,
                            "fullMark": 100,
                        },
                    ]),
                    verified_skills_json=json.dumps([
                        "Python",
                        "PyTorch",
                        "Linear Algebra",
                        "Git",
                        "Docker",
                    ]),
                )
                db.add(demo_user)
                db.flush()

                # Seed demo progress only for the AI Engineer course.
                progress_seeds = [
                    {
                        "module_id": "py-foundations",
                        "status": "passed",
                        "best_score": 13,
                    },
                    {
                        "module_id": "math-ml",
                        "status": "passed",
                        "best_score": 12,
                    },
                    {
                        "module_id": "classical-ml",
                        "status": "available",
                        "best_score": 0,
                    },
                    {
                        "module_id": "deep-learning",
                        "status": "locked",
                        "best_score": 0,
                    },
                    {
                        "module_id": "rag-systems",
                        "status": "locked",
                        "best_score": 0,
                    },
                    {
                        "module_id": "mlops-deploy",
                        "status": "locked",
                        "best_score": 0,
                    },
                ]

                for progress in progress_seeds:
                    db.add(
                        UserModuleProgress(
                            user_id=demo_user.id,
                            module_id=progress["module_id"],
                            status=progress["status"],
                            best_score=progress["best_score"],
                            attempts_count=(
                                1
                                if progress["status"] == "passed"
                                else 0
                            ),
                        )
                    )

                db.add(
                    XPEvent(
                        user_id=demo_user.id,
                        source="initial_seed",
                        amount=860,
                        metadata_json=json.dumps({
                            "reason": "pre-existing course progression"
                        }),
                        idempotency_key=(
                            f"seed-{demo_user.id}-initial"
                        ),
                    )
                )

            db.commit()

        logger.info("NovaPath database initialized successfully.")

    except Exception:
        logger.exception("NovaPath database initialization failed.")
        raise
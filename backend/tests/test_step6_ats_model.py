import io
import pytest
from pypdf import PdfWriter
import docx

from app.config import settings
from app.services.ats_service import ats_service
from app.core.database import SessionLocal, init_db
from app.models.db_models import User, Module, UserModuleProgress, ResumeAnalysis
from app.routers.resume import add_skill_to_roadmap, AddToRoadmapPayload

# 10 Sample Resumes of Graduating Quality for Monotonicity Testing
SAMPLE_RESUMES = [
    # 1. Completely Irrelevant (Advocate / Legal background, zero tech)
    """
    John Doe | Legal Advocate | legal@example.com
    Experience: 5 years representing civil litigation cases in municipal court.
    Drafted contracts, negotiated settlements, filed petitions.
    Education: Bachelor of Laws (LLB), State Law Academy.
    Skills: Contract Negotiation, Civil Litigation, Legal Research, Client Advocacy.
    """,

    # 2. Ultra-sparse One-Liner (Almost no content)
    """
    Bob Smith. Email: bob@example.com. Phone: 1234567890.
    I want to learn coding. I used a computer once.
    """,

    # 3. Junior Non-Technical Retail
    """
    Alice Retail | alice@example.com
    Summary: Enthusiastic customer service specialist seeking transition.
    Experience: Retail Cashier at Target (2022-2024). Handled POS cash register, answered customer inquiries.
    Education: High School Diploma.
    Skills: Cash Handling, Customer Support, Teamwork.
    """,

    # 4. Beginner Programmer (Basic Python scripting, no AI or DL)
    """
    Charlie Beginner | charlie@example.com | github.com/charlie
    Summary: Novice programmer learning basic Python syntax.
    Skills: Python, Basic HTML, CSS, Print statements, Loops.
    Projects: Calculator app written in Python with Tkinter GUI.
    Education: B.Sc in Information Technology, 2024.
    Experience: Academic lab coursework.
    """,

    # 5. Junior Web Dev (JavaScript, HTML, CSS, no backend or AI)
    """
    David Web | david@example.com | github.com/david
    Summary: Junior Frontend builder creating static landing pages.
    Skills: HTML5, CSS3, JavaScript, Bootstrap, Git.
    Experience: Web Design Intern at Local Agency. Created 3 static HTML websites for local bakeries.
    Projects: Personal portfolio site hosted on GitHub Pages.
    Education: Diploma in Web Development.
    """,

    # 6. Moderate Backend Dev (Node.js, SQL, basic Docker, no deep learning)
    """
    Eva Backend | eva@example.com | github.com/eva | linkedin.com/in/eva
    Summary: Backend software developer with experience in API microservices and relational databases.
    Skills: JavaScript, Node.js, Express, PostgreSQL, Docker, Git, Linux.
    Experience: Backend Developer at FinCorp (1 yr). Built REST APIs for transaction records.
    Projects: E-commerce inventory API handling 500 product catalog entries.
    Education: B.Tech in Computer Science, 2023.
    """,

    # 7. Junior Data Analyst (Pandas, SQL, basic Scikit-Learn, 1-2 metrics)
    """
    Frank Analyst | frank@example.com | github.com/frank | linkedin.com/in/frank
    Summary: Data analyst with experience in SQL reporting and introductory predictive models.
    Skills: Python, SQL, Pandas, NumPy, Scikit-Learn, Matplotlib, Git.
    Experience: Junior Data Analyst at RetailCorp (1 yr). Analyzed sales data across 4 retail branches.
    Projects: Customer churn predictor using Scikit-Learn Logistic Regression with 78% accuracy.
    Education: B.Tech in Data Science, 2023.
    """,

    # 8. Mid-level ML Engineer (PyTorch, Scikit-Learn, Docker, 2-3 quantified bullets)
    """
    Grace ML | grace@example.com | github.com/grace | linkedin.com/in/grace
    Summary: Machine Learning Engineer with 2 years of experience building computer vision and NLP models.
    Skills: Python, PyTorch, Scikit-Learn, Docker, FastAPI, Git, Linux, NumPy, Pandas.
    Experience:
    - Built convolutional neural network models for image defect detection, achieving 91% recall.
    - Containerized ML inference services using Docker and FastAPI with 150ms average response time.
    Projects:
    - Object detection pipeline in PyTorch evaluated on custom dataset of 10,000 images.
    Education: B.Tech Computer Science & Engineering, 2022.
    """,

    # 9. Senior AI Engineer (PyTorch, Transformers, RAG, CUDA, high quantified metrics)
    """
    Henry Senior AI | henry@example.com | github.com/henry | linkedin.com/in/henry
    Summary: Senior AI & Machine Learning Engineer with 4 years developing deep learning models, Data Science solutions, LLM deployment, and retrieval-augmented generation.
    Technical Skills:
    - Languages & Core: Python, C++, CUDA, Bash, SQL, Data Science
    - AI Frameworks: PyTorch, Hugging Face Transformers, LangChain, Vector Database, Scikit-Learn, Deep Learning
    - Production & MLOps: FastAPI, Docker, Kubernetes, Linux, TensorRT, Model Evaluation, Fine-Tuning, MLOps
    Experience:
    - Fine-tuned open-source 7B parameter machine learning models using QLoRA, cutting latency by 42% and GPU VRAM usage by 60%.
    - Architected enterprise RAG system indexing 250,000 documents with FAISS vector database and cross-encoder re-ranking.
    - Optimized production inference pipeline with TensorRT and FP16 quantization, achieving 18ms latency for 5,000+ daily queries.
    - Led machine learning data science experimentation cutting model training iterations by 35%.
    Projects:
    - Multi-tenant Hybrid RAG Search Engine with MMR diversity filtering and reranking.
    - Vision Transformer Classifier in pure PyTorch trained on distributed GPU cluster.
    Education: Master of Science in Computer Science & Data Science, 2021.
    """,

    # 10. Staff / Principal AI Engineer (Comprehensive skills, exceptional quantified outcomes)
    """
    Irene Staff AI | irene@example.com | github.com/irene | linkedin.com/in/irene
    Summary: Principal AI Architect & Data Scientist with deep machine learning expertise across transformer architectures, distributed PyTorch, RAG vector systems, and scalable MLOps.
    Technical Competencies:
    - Python, PyTorch, Transformers, Vector Database, RAG, LangChain, Docker, FastAPI, CUDA, Model Evaluation, MLOps, Fine-Tuning
    - Secondary: Machine Learning, Data Science, Deep Learning, Kubernetes, TensorRT, Triton, AWS, Linux, Git, CI/CD, Scikit-Learn, NumPy, Pandas
    Professional Experience:
    - Architected and deployed enterprise machine learning GenAI platform processing 12,000,000 tokens daily with 99.99% uptime.
    - Accelerated multi-GPU distributed deep learning fine-tuning throughput by 75% using DeepSpeed ZeRO-3 and custom CUDA kernels.
    - Reduced hallucination rates by 38% through hybrid vector database retrieval and dynamic contextual re-ranking.
    - Optimized model serving cluster from 180ms down to 24ms per request, saving $120,000 in annual cloud compute.
    - Built production data science feature pipelines serving 50,000 real-time inference predictions per second.
    Key Projects:
    - Open-source distributed RAG orchestrator with 4,500 GitHub stars and 50+ enterprise contributors.
    - Low-latency real-time voice translation pipeline leveraging Whisper and custom Triton model serving.
    Education:
    - Bachelor of Technology in Computer Science & Data Science, GPA: 3.9/4.0.
    """
]

def test_ats_weights_in_config():
    """Verifies that all 5 ATS scoring weights sum to exactly 1.00."""
    total = (
        settings.ATS_WEIGHT_ROLE_FIT +
        settings.ATS_WEIGHT_KEYWORD_COVERAGE +
        settings.ATS_WEIGHT_SECTION_COMPLETENESS +
        settings.ATS_WEIGHT_FORMATTING +
        settings.ATS_WEIGHT_QUANTIFIED_IMPACT
    )
    assert round(total, 4) == 1.00
    assert settings.ATS_WEIGHT_ROLE_FIT == 0.40
    assert settings.ATS_WEIGHT_KEYWORD_COVERAGE == 0.25
    assert settings.ATS_WEIGHT_SECTION_COMPLETENESS == 0.15
    assert settings.ATS_WEIGHT_FORMATTING == 0.10
    assert settings.ATS_WEIGHT_QUANTIFIED_IMPACT == 0.10

def test_ats_model_artifact_loaded():
    """Verifies the real trained model artifact is loaded and functional."""
    assert ats_service._model is not None
    assert len(ats_service._model.classes_) == 16
    assert "AI Engineer" in ats_service._model.classes_
    assert "Backend Developer" in ats_service._model.classes_

def test_ats_deterministic_scoring():
    """Ensures that uploading the exact same resume twice gives the exact same score."""
    sample = SAMPLE_RESUMES[8]
    res1 = ats_service.analyze_resume_text(sample, "AI Engineer")
    res2 = ats_service.analyze_resume_text(sample, "AI Engineer")

    assert res1.ats_score == res2.ats_score
    assert res1.role_fit_score == res2.role_fit_score
    assert res1.skills_match_score == res2.skills_match_score
    assert res1.raw_text_hash == res2.raw_text_hash
    assert len(res1.matched_skills) == len(res2.matched_skills)

def test_ats_quality_monotonicity_with_10_resumes():
    """
    Tests 10 sample resumes of varying quality and asserts that
    better resumes score higher (monotonic quality graduation).
    """
    scores = []
    for i, resume_text in enumerate(SAMPLE_RESUMES):
        result = ats_service.analyze_resume_text(resume_text, "AI Engineer")
        scores.append((i + 1, result.ats_score, result.role_fit_score, result.skills_match_score))

    # Print scored progression
    print("\n--- Monotonic Quality Progression (10 Resumes) ---")
    for idx, overall, role_fit, kw in scores:
        print(f"Resume {idx:2d}: Overall ATS = {overall:2d} | Role-Fit = {role_fit:5.1f}% | Keywords = {kw:2d}%")

    poor_avg = sum(s[1] for s in scores[:3]) / 3.0
    mid_avg = sum(s[1] for s in scores[3:7]) / 4.0
    high_avg = sum(s[1] for s in scores[7:]) / 3.0

    print(f"\nGroup Averages -> Poor: {poor_avg:.1f} | Mid: {mid_avg:.1f} | High: {high_avg:.1f}")

    # Monotonicity checks
    assert high_avg > mid_avg > poor_avg, "Expected high quality resumes to outscore mid and poor resumes"
    assert scores[9][1] > scores[0][1], "Staff AI engineer must outscore non-technical legal resume"
    assert scores[8][1] > scores[4][1], "Senior AI engineer must outscore junior web designer"
    assert scores[9][1] >= 80, "Staff AI resume should achieve high score (>= 80 with calibrated role-fit)"
    assert scores[0][1] <= 35, "Legal resume should receive low ATS score for AI Engineer (<= 35)"

def test_ats_robustness_unreadable_and_edge_cases():
    """Verifies handling of empty, scanned, huge, and non-English files."""
    # 1. Empty bytes
    with pytest.raises(ValueError, match="empty"):
        ats_service.extract_text_from_file(b"", "empty.pdf")

    # 2. File exceeding 5MB limit
    huge_bytes = b"A" * (6 * 1024 * 1024)
    with pytest.raises(ValueError, match="exceeds maximum limit"):
        ats_service.extract_text_from_file(huge_bytes, "huge.pdf")

    # 3. Scanned PDF with zero extractable text
    writer = PdfWriter()
    writer.add_blank_page(width=200, height=200)
    pdf_buf = io.BytesIO()
    writer.write(pdf_buf)
    with pytest.raises(ValueError, match="scanned image or contains no readable text"):
        ats_service.extract_text_from_file(pdf_buf.getvalue(), "scanned.pdf")

    # 4. DOCX with insufficient text
    doc = docx.Document()
    doc.add_paragraph("Tiny")
    docx_buf = io.BytesIO()
    doc.save(docx_buf)
    with pytest.raises(ValueError, match="insufficient"):
        ats_service.extract_text_from_file(docx_buf.getvalue(), "tiny.docx")

    # 5. Non-English / gibberish text
    gibberish = "123456 !!! ??? &&& 999 888 777"
    with pytest.raises(ValueError, match="insufficient readable English words"):
        ats_service.extract_text_from_file(gibberish.encode("utf-8"), "gibberish.txt")

def test_ats_add_to_roadmap():
    """Tests that '+ Add to Roadmap' persists a real module in SQLite."""
    import asyncio
    init_db()
    db = SessionLocal()
    try:
        payload = AddToRoadmapPayload(skill="Docker", target_role="AI Engineer")
        res = asyncio.run(add_skill_to_roadmap(payload, db))

        assert res["success"] is True
        assert res["skill"] == "Docker"
        mod_id = res["module_id"]

        # Verify module was created in DB
        mod = db.query(Module).filter(Module.id == mod_id).first()
        assert mod is not None
        assert "Docker" in mod.title
        assert "Docker" in mod.skills_json

        # Verify user progress is available
        prog = db.query(UserModuleProgress).filter(
            UserModuleProgress.user_id == "usr-aarav-sharma",
            UserModuleProgress.module_id == mod_id
        ).first()
        assert prog is not None
        assert prog.status == "available"
    finally:
        db.close()

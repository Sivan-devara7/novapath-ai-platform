import json
import re
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.db_models import User, Module, UserModuleProgress, ResumeAnalysis
from ..models.schemas import ResumeAnalysisResponse, BridgeRoadmapResponse, GenerateBridgeRoadmapRequest, BridgeMilestone
from ..services.ats_service import ats_service
from ..services.llm_service import llm_service

router = APIRouter(prefix="/resume", tags=["resume"])

DEMO_USER_ID = "usr-aarav-sharma"

class AnalyzeTextPayload(BaseModel):
    resume_text: str
    target_role: Optional[str] = "AI Engineer"

class AddToRoadmapPayload(BaseModel):
    skill: str
    target_role: Optional[str] = "AI Engineer"

SAMPLE_STUDENT_RESUME = """
Aarav Sharma | aarav.sharma@vizag.edu | GitHub: github.com/aarav | LinkedIn: linkedin.com/in/aarav

SUMMARY
Results-driven Computer Science undergraduate with focused experience in PyTorch deep learning pipelines,
transformer models, and high-throughput Python backends. Passionate about LLM deployment and efficient fine-tuning.

TECHNICAL SKILLS
- Languages: Python, C++, SQL, TypeScript, Bash
- Frameworks & Libraries: PyTorch, Hugging Face Transformers, FastAPI, Docker, NumPy, Pandas, Scikit-Learn
- Tools: Git, Linux, Weights & Biases, PostgreSQL, CUDA

EXPERIENCE
AI Engineering Intern | QuantAI Technologies | 6 mos
- Fine-tuned BERT and RoBERTa classification models, achieving a 14% improvement in domain sentiment accuracy.
- Accelerated inference latency by 45% (from 180ms to 42ms) by implementing TensorRT FP16 quantization.
- Built and deployed RESTful microservices in FastAPI, sustaining 12,000+ requests daily with 99.9% uptime.

PROJECTS
Vision Transformer (ViT) Classifier from Scratch
- Implemented multi-head self-attention and patch embedding projection in pure PyTorch; achieved 88.2% top-1 accuracy on CIFAR-100.
- Orchestrated distributed data parallel training across 2x NVIDIA RTX 4090 GPUs, cutting epoch training time by 48%.

Hybrid RAG Document Search Engine
- Designed hierarchical chunking pipeline indexing 50,000+ technical PDF documents using FAISS vector store.
- Reduced hallucination rates by 28% using cross-encoder re-ranking and MMR diversity filtering.

EDUCATION
Bachelor of Technology in Computer Science & Engineering | CGPA: 8.9 / 10.0
"""

def _persist_analysis(analysis: ResumeAnalysisResponse, target_role: str, db: Session) -> None:
    """Stores the deterministic ATS analysis in SQLite database."""
    try:
        user = db.query(User).filter(User.id == DEMO_USER_ID).first()
        if not user:
            return

        db_analysis = ResumeAnalysis(
            user_id=user.id,
            target_role=target_role,
            overall_ats_score=analysis.ats_score,
            role_fit_score=analysis.role_fit_score or 0.0,
            keyword_score=float(analysis.skills_match_score),
            section_score=analysis.section_score or 0.0,
            format_score=float(analysis.formatting_score),
            impact_score=float(analysis.impact_score),
            extracted_skills_json=json.dumps(analysis.extracted_skills),
            missing_skills_json=json.dumps(analysis.missing_skills),
            deductions_json=json.dumps(analysis.deductions or []),
            top_features_json=json.dumps(analysis.top_contributing_features or []),
            raw_text_hash=analysis.raw_text_hash or ""
        )
        db.add(db_analysis)
        db.commit()
    except Exception as e:
        db.rollback()
        # Keep analysis functional even if DB logging encounters an issue

@router.get("/sample-analysis", response_model=ResumeAnalysisResponse)
async def get_sample_analysis(target_role: str = "AI Engineer", db: Session = Depends(get_db)):
    """Analyzes the verified sample resume using the 5-component ML blend."""
    analysis = ats_service.analyze_resume_text(SAMPLE_STUDENT_RESUME, target_role)
    _persist_analysis(analysis, target_role, db)
    return analysis

@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_custom_text(payload: AnalyzeTextPayload, db: Session = Depends(get_db)):
    """Analyzes pasted resume text deterministically and persists result to database."""
    role = payload.target_role or "AI Engineer"
    text = payload.resume_text.strip()
    if len(text) < 40:
        raise HTTPException(
            status_code=400,
            detail="Resume text is too brief (minimum 40 characters required for ATS audit)."
        )

    analysis = ats_service.analyze_resume_text(text, role)
    _persist_analysis(analysis, role, db)
    return analysis

@router.post("/upload", response_model=ResumeAnalysisResponse)
async def upload_and_analyze(
    file: UploadFile = File(...),
    target_role: Optional[str] = Form("AI Engineer"),
    db: Session = Depends(get_db)
):
    """
    Handles PDF, DOCX, and TXT file uploads.
    Extracts text, guards against corrupted/empty/scanned files,
    and returns full ATS audit breakdown.
    """
    role = target_role or "AI Engineer"
    try:
        content = await file.read()
        extracted_text = ats_service.extract_text_from_file(content, file.filename or "resume.pdf")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

    analysis = ats_service.analyze_resume_text(extracted_text, role)
    _persist_analysis(analysis, role, db)
    return analysis

@router.post("/add-to-roadmap")
async def add_skill_to_roadmap(payload: AddToRoadmapPayload, db: Session = Depends(get_db)):
    """
    Creates a real module or topic in the user's roadmap database (v2 Section E).
    """
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    skill_clean = payload.skill.strip()
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", skill_clean.lower()).strip("-")
    module_id = f"mod-{slug}"

    # Check if a module with this ID already exists
    existing_mod = db.query(Module).filter(Module.id == module_id).first()

    if not existing_mod:
        # Determine highest order index
        max_order = db.query(Module).filter(Module.course_id == "ai-engineer").count()
        new_module = Module(
            id=module_id,
            course_id="ai-engineer",
            order_index=max_order + 1,
            title=f"Mastering {skill_clean}",
            summary=f"Custom roadmap module targeted at bridging your ATS resume gap in {skill_clean}.",
            estimated_hours=10,
            lessons_count=4,
            skills_json=json.dumps([skill_clean]),
            difficulty="Intermediate",
            topics_json=json.dumps([
                f"Core {skill_clean} Principles",
                f"Hands-On {skill_clean} Architecture",
                f"Production Integration & Testing",
                f"{skill_clean} Performance Optimization"
            ]),
            learning_objectives_json=json.dumps([
                f"Develop working competency in {skill_clean}",
                f"Implement real-world projects featuring {skill_clean}"
            ])
        )
        db.add(new_module)
        db.flush()

    # Ensure progress record exists and is available
    progress = db.query(UserModuleProgress).filter(
        UserModuleProgress.user_id == user.id,
        UserModuleProgress.module_id == module_id
    ).first()

    if not progress:
        progress = UserModuleProgress(
            user_id=user.id,
            module_id=module_id,
            status="available",
            best_score=0,
            attempts_count=0
        )
        db.add(progress)
    else:
        if progress.status == "locked":
            progress.status = "available"

    db.commit()

    return {
        "success": True,
        "module_id": module_id,
        "skill": skill_clean,
        "message": f"Successfully added '{skill_clean}' module to your roadmap!"
    }

@router.post("/generate-bridge-roadmap", response_model=BridgeRoadmapResponse)
async def generate_bridge_roadmap(payload: GenerateBridgeRoadmapRequest):
    """
    Synthesizes an AI Bridge Roadmap using OmniRoute models based on detected ATS resume gaps.
    Generates 4 tailored milestones, projected score increase, and milestone capstone tasks.
    """
    role = payload.target_role or "AI Engineer"
    gaps = payload.missing_skills or ["Vector Database", "RAG", "Docker"]
    current_score = payload.current_ats_score or 70
    projected = min(98, current_score + 22)

    # Deterministic high-quality fallback tailored to role
    gap_str = ", ".join(gaps[:3])
    fallback_milestones = [
        BridgeMilestone(
            step=1,
            title=f"Core Foundations of {gaps[0] if gaps else 'Core Concepts'}",
            target_skill=gaps[0] if gaps else "Python & Data Structures",
            description=f"Close foundational knowledge gaps in {gaps[0] if gaps else 'Core'}. Focus on memory representations, basic syntax, and standard patterns.",
            estimated_hours=12,
            project=f"Build a clean runnable pipeline implementing {gaps[0] if gaps else 'Core'} from scratch."
        ),
        BridgeMilestone(
            step=2,
            title=f"Hands-On {gaps[1] if len(gaps) > 1 else 'Architecture'} Integration",
            target_skill=gaps[1] if len(gaps) > 1 else "API Design",
            description=f"Implement practical microservice or data layer integrations featuring {gaps[1] if len(gaps) > 1 else 'Architecture'}.",
            estimated_hours=16,
            project=f"End-to-end service featuring {gaps[1] if len(gaps) > 1 else 'Architecture'} with unit tests."
        ),
        BridgeMilestone(
            step=3,
            title=f"Production Deployment & Testing ({gaps[2] if len(gaps) > 2 else 'DevOps'})",
            target_skill=gaps[2] if len(gaps) > 2 else "Containerization",
            description=f"Package and containerize applications with automated testing, benchmarking latency, and throughput.",
            estimated_hours=14,
            project=f"Dockerized staging deployment with GitHub Actions CI/CD."
        ),
        BridgeMilestone(
            step=4,
            title=f"Recruiter-Ready Capstone Portfolio Project",
            target_skill=f"{role} Synthesis",
            description=f"Synthesize all bridged skills into a recruiter-visible GitHub portfolio repository with full documentation and live demo.",
            estimated_hours=20,
            project=f"Production-grade {role} showcase platform ready for resume inclusion."
        )
    ]

    fallback = BridgeRoadmapResponse(
        target_role=role,
        current_ats_score=current_score,
        projected_ats_score=projected,
        estimated_weeks="5-6 Weeks",
        summary=f"Custom AI curriculum calibrated to bridge your detected skill gaps ({gap_str}) and elevate your ATS alignment from {current_score}% to {projected}%.",
        milestones=fallback_milestones
    )

    system_prompt = (
        "You are NovaPath AI's expert career roadmap strategist. "
        "Given a student's target role, current ATS score, and detected skill gaps, "
        "generate a concise, structured 4-milestone bridge roadmap that will eliminate their resume gaps "
        "and prepare them for top industry placement. "
        "Respond strictly with JSON adhering to the BridgeRoadmapResponse schema."
    )

    user_prompt = (
        f"Generate a customized bridge roadmap for target role '{role}'. "
        f"Current ATS Score: {current_score}/100. "
        f"Detected Missing Skills: {', '.join(gaps)}. "
        f"Verified Matched Skills: {', '.join(payload.matched_skills[:5])}."
    )

    try:
        res = await llm_service.chat_json(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            schema=BridgeRoadmapResponse,
            fallback=fallback,
            temperature=0.3,
            max_tokens=1400
        )
        return res
    except Exception:
        return fallback

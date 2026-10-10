from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from ..models.schemas import ResumeAnalysisResponse
from ..services.ats_service import ats_service
from .auth import DEMO_USER

router = APIRouter(prefix="/resume", tags=["resume"])

class AnalyzeTextPayload(BaseModel):
    resume_text: str
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

@router.get("/sample-analysis", response_model=ResumeAnalysisResponse)
async def get_sample_analysis(target_role: str = "AI Engineer"):
    return ats_service.analyze_resume_text(SAMPLE_STUDENT_RESUME, target_role)

@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_custom_text(payload: AnalyzeTextPayload):
    return ats_service.analyze_resume_text(payload.resume_text, payload.target_role or "AI Engineer")

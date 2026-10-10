from fastapi import APIRouter
from typing import List
from ..models.schemas import RecommendationItem

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

RECOMMENDATIONS_DATABASE: List[RecommendationItem] = [
    RecommendationItem(
        id="rec-proj-1",
        type="project",
        title="Production Hybrid RAG with Cross-Encoder Re-Ranking",
        organization="Open Source AI Labs",
        difficulty="Advanced",
        duration="3 Weeks (Est. 25h)",
        match_percentage=98,
        why_this_matches="Addresses the critical missing keyword 'Vector Database & RAG' detected in your resume ATS audit. Recruiters specifically seek portfolio proof of real-world chunking and re-ranking.",
        prerequisites=["PyTorch", "Python", "Transformers"],
        tags=["Vector DB", "FAISS", "LlamaIndex", "FastAPI"],
        action_url="/roadmap"
    ),
    RecommendationItem(
        id="rec-proj-2",
        type="project",
        title="Distributed LLM Fine-Tuner with QLoRA & vLLM Serving",
        organization="Hugging Face Community Project",
        difficulty="Advanced",
        duration="4 Weeks (Est. 35h)",
        match_percentage=95,
        why_this_matches="Elevates your deep learning profile from foundational modeling to industry-standard high-throughput inference serving.",
        prerequisites=["PyTorch", "CUDA Basics"],
        tags=["QLoRA", "vLLM", "Docker", "Triton"],
        action_url="/roadmap"
    ),
    RecommendationItem(
        id="rec-cert-1",
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
    ),
    RecommendationItem(
        id="rec-cert-2",
        type="certification",
        title="DeepLearning.AI Generative AI for Large Language Models",
        organization="DeepLearning.AI & AWS",
        difficulty="Intermediate",
        duration="4 Weeks Study Path",
        match_percentage=94,
        why_this_matches="Directly validates transformer fine-tuning and RLHF alignment on your public student profile.",
        prerequisites=["Python", "PyTorch"],
        tags=["GenAI", "RLHF", "PEFT", "Evaluation"],
        action_url="https://www.coursera.org/learn/generative-ai-with-llms"
    ),
    RecommendationItem(
        id="rec-intern-1",
        type="internship",
        title="Applied AI Research Intern (Fall 2026)",
        organization="Anthropic / Cohere Campus Lab",
        difficulty="High Impact",
        duration="6 Months",
        match_percentage=91,
        why_this_matches="Your 85/100 Deep Learning score and PyTorch project portfolio meet 92% of the candidate baseline qualifications.",
        prerequisites=["PyTorch", "Transformer Architecture", "Git"],
        tags=["Research", "Inference Optimization", "CUDA"],
        action_url="#"
    ),
    RecommendationItem(
        id="rec-intern-2",
        type="internship",
        title="Machine Learning Platform Engineer Intern",
        organization="Scale AI",
        difficulty="High Impact",
        duration="3 Months",
        match_percentage=89,
        why_this_matches="Matches your demonstrated expertise in FastAPI microservices and model quantization pipelines.",
        prerequisites=["Docker", "Python", "FastAPI"],
        tags=["MLOps", "Kubernetes", "Data Pipelines"],
        action_url="#"
    )
]

@router.get("/", response_model=List[RecommendationItem])
async def get_recommendations():
    return RECOMMENDATIONS_DATABASE

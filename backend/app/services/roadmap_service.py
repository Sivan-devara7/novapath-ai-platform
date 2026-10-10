from typing import List, Dict, Any
from ..models.schemas import SkillNode, SkillGraphResponse

# Master skill tree configurations by career goal
CAREER_ROADMAPS: Dict[str, List[Dict[str, Any]]] = {
    "AI Engineer": [
        {
            "id": "py-foundations",
            "name": "Python & Algorithmic Foundations",
            "category": "Core CS",
            "prerequisites": [],
            "mastery_level": 92,
            "status": "completed",
            "verified_via": "Resume & GitHub Verification",
            "icon": "Code2",
            "estimated_hours": 20,
            "milestone_project": "High-throughput Async Data Pipeline"
        },
        {
            "id": "math-linear-algebra",
            "name": "Linear Algebra & Tensor Calculus",
            "category": "Foundations",
            "prerequisites": ["py-foundations"],
            "mastery_level": 85,
            "status": "completed",
            "verified_via": "Academic Marksheet OCR",
            "icon": "Binary",
            "estimated_hours": 25,
            "milestone_project": "Custom Matrix Eigen-decomposition Engine"
        },
        {
            "id": "pytorch-deep-learning",
            "name": "PyTorch & Deep Neural Networks",
            "category": "Deep Learning",
            "prerequisites": ["math-linear-algebra"],
            "mastery_level": 74,
            "status": "in_progress",
            "verified_via": "In Progress (Module 3/5)",
            "icon": "Brain",
            "estimated_hours": 35,
            "milestone_project": "Vision Transformer (ViT) Classifier from Scratch"
        },
        {
            "id": "transformers-nlp",
            "name": "Transformers & Attention Architectures",
            "category": "GenAI",
            "prerequisites": ["pytorch-deep-learning"],
            "mastery_level": 40,
            "status": "ready",
            "verified_via": None,
            "icon": "Sparkles",
            "estimated_hours": 30,
            "milestone_project": "Fine-Tuned LLaMA-3 with QLoRA on Domain Corpus"
        },
        {
            "id": "rag-vector-db",
            "name": "RAG Systems & Vector Databases",
            "category": "Applied AI",
            "prerequisites": ["transformers-nlp"],
            "mastery_level": 0,
            "status": "locked",
            "verified_via": None,
            "icon": "Database",
            "estimated_hours": 25,
            "milestone_project": "Production Multi-Tenant Hybrid RAG with Re-ranking"
        },
        {
            "id": "mlops-deployment",
            "name": "MLOps, TensorRT & Model Serving",
            "category": "Production",
            "prerequisites": ["rag-vector-db"],
            "mastery_level": 0,
            "status": "locked",
            "verified_via": None,
            "icon": "Cpu",
            "estimated_hours": 30,
            "milestone_project": "Kubernetes-Orchestrated Triton Inference Cluster"
        }
    ],
    "Full Stack Developer": [
        {
            "id": "modern-ts",
            "name": "Modern TypeScript & ESNext",
            "category": "Frontend Core",
            "prerequisites": [],
            "mastery_level": 90,
            "status": "completed",
            "verified_via": "GitHub Verification",
            "icon": "Code",
            "estimated_hours": 15,
            "milestone_project": "Type-Safe Reactive State Store"
        },
        {
            "id": "react-architecture",
            "name": "React 19 & Next.js App Router",
            "category": "Frontend Architecture",
            "prerequisites": ["modern-ts"],
            "mastery_level": 82,
            "status": "completed",
            "verified_via": "Portfolio Assessment",
            "icon": "Layers",
            "estimated_hours": 25,
            "milestone_project": "Server Actions SaaS Platform"
        },
        {
            "id": "backend-fastapi-node",
            "name": "Distributed APIs & Microservices",
            "category": "Backend",
            "prerequisites": ["modern-ts"],
            "mastery_level": 60,
            "status": "in_progress",
            "verified_via": None,
            "icon": "Server",
            "estimated_hours": 30,
            "milestone_project": "Event-Driven Order Processing with Kafka"
        },
        {
            "id": "cloud-docker",
            "name": "Cloud Infrastructure & Containerization",
            "category": "DevOps",
            "prerequisites": ["backend-fastapi-node"],
            "mastery_level": 20,
            "status": "ready",
            "verified_via": None,
            "icon": "Cloud",
            "estimated_hours": 20,
            "milestone_project": "Automated Multi-Environment CI/CD Pipeline"
        }
    ]
}

class RoadmapService:
    def get_roadmap(self, career_goal: str = "AI Engineer", user_skills: List[str] = None) -> SkillGraphResponse:
        skills = CAREER_ROADMAPS.get(career_goal, CAREER_ROADMAPS["AI Engineer"])
        
        nodes = []
        edges = []
        completed_count = 0

        for item in skills:
            # Check if user has this skill verified
            node = SkillNode(
                id=item["id"],
                name=item["name"],
                category=item["category"],
                prerequisites=item["prerequisites"],
                mastery_level=item["mastery_level"],
                status=item["status"],
                verified_via=item.get("verified_via"),
                icon=item.get("icon"),
                estimated_hours=item.get("estimated_hours", 20),
                milestone_project=item.get("milestone_project")
            )
            if node.status == "completed":
                completed_count += 1
            nodes.append(node)

            for prereq in item["prerequisites"]:
                edges.append({
                    "source": prereq,
                    "target": item["id"]
                })

        completion_rate = int((completed_count / len(nodes)) * 100) if nodes else 0

        return SkillGraphResponse(
            nodes=nodes,
            edges=edges,
            career_goal=career_goal,
            completion_rate=completion_rate
        )

roadmap_service = RoadmapService()

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from ..models.schemas import SkillGraphResponse
from ..services.roadmap_service import roadmap_service
from .auth import DEMO_USER

router = APIRouter(prefix="/roadmap", tags=["roadmap"])

class GenerateRoadmapRequest(BaseModel):
    career_goal: str
    verified_skills: Optional[List[str]] = None

@router.get("/graph", response_model=SkillGraphResponse)
async def get_roadmap_graph(career_goal: Optional[str] = None):
    goal = career_goal or DEMO_USER.career_goal
    return roadmap_service.get_roadmap(goal, DEMO_USER.verified_skills)

@router.post("/generate", response_model=SkillGraphResponse)
async def generate_roadmap(payload: GenerateRoadmapRequest):
    DEMO_USER.career_goal = payload.career_goal
    return roadmap_service.get_roadmap(payload.career_goal, payload.verified_skills or DEMO_USER.verified_skills)

@router.post("/complete-node/{node_id}")
async def complete_node(node_id: str):
    DEMO_USER.points += 150
    DEMO_USER.streak += 1
    DEMO_USER.mastery_overall = min(100, DEMO_USER.mastery_overall + 5)
    return {
        "status": "success",
        "completed_node_id": node_id,
        "new_streak": DEMO_USER.streak,
        "new_points": DEMO_USER.points,
        "new_mastery": DEMO_USER.mastery_overall
    }

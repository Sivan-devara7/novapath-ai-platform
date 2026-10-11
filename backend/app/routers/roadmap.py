import json
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session
from ..models.schemas import SkillGraphResponse
from ..models.db_models import User, UserModuleProgress, XPEvent
from ..core.database import get_db
from ..services.roadmap_service import roadmap_service

router = APIRouter(prefix="/roadmap", tags=["roadmap"])

DEMO_USER_ID = "usr-aarav-sharma"

class GenerateRoadmapRequest(BaseModel):
    career_goal: str
    verified_skills: Optional[List[str]] = None

@router.get("/graph", response_model=SkillGraphResponse)
async def get_roadmap_graph(career_goal: Optional[str] = None, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    verified_skills = json.loads(user.verified_skills_json) if user and user.verified_skills_json else []
    goal = career_goal or (user.career_goal if user else "AI Engineer")
    return roadmap_service.get_roadmap(goal, verified_skills)

@router.post("/generate", response_model=SkillGraphResponse)
async def generate_roadmap(payload: GenerateRoadmapRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if user:
        user.career_goal = payload.career_goal
        db.commit()
    verified_skills = payload.verified_skills or (json.loads(user.verified_skills_json) if user and user.verified_skills_json else [])
    return roadmap_service.get_roadmap(payload.career_goal, verified_skills)

@router.post("/complete-node/{node_id}")
async def complete_node(node_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.total_xp += 150
    user.streak += 1
    user.mastery_overall = min(100, user.mastery_overall + 5)
    
    # Update module progress in DB
    progress = db.query(UserModuleProgress).filter(
        UserModuleProgress.user_id == user.id,
        UserModuleProgress.module_id == node_id
    ).first()
    if progress:
        progress.status = "passed"
    else:
        db.add(UserModuleProgress(
            user_id=user.id,
            module_id=node_id,
            status="passed",
            best_score=15,
            attempts_count=1
        ))

    # Add XP event ledger entry
    idempotency_key = f"complete-node-{user.id}-{node_id}-{uuid.uuid4().hex[:8]}"
    db.add(XPEvent(
        user_id=user.id,
        source="node_completion",
        amount=150,
        metadata_json=json.dumps({"node_id": node_id}),
        idempotency_key=idempotency_key
    ))

    db.commit()
    db.refresh(user)

    return {
        "status": "success",
        "completed_node_id": node_id,
        "new_streak": user.streak,
        "new_points": user.total_xp,
        "new_mastery": user.mastery_overall
    }

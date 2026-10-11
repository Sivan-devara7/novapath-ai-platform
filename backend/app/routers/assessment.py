import json
import uuid
import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session

from ..config import settings
from ..models.schemas import AssessmentQuestion, AssessmentFeedback
from ..models.db_models import User, Question, QuizAttempt, XPEvent
from ..core.database import get_db
from ..services.assessment_service import assessment_service
from ..services.placement_service import placement_service

router = APIRouter(prefix="/assessment", tags=["assessment"])

DEMO_USER_ID = "usr-aarav-sharma"

class SubmitPayload(BaseModel):
    question_id: str
    selected_option_index: int
    consecutive_correct: int = 0

class PlacementSubmitRequest(BaseModel):
    question_ids: List[str] = Field(description="List of 20 sampled question IDs")
    answers: Dict[str, int] = Field(description="Map of question_id -> selected_option_index")

@router.get("/placement/status")
async def get_placement_status(db: Session = Depends(get_db)):
    """Returns current user placement ranking and retake eligibility."""
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    can_retake, cooldown_msg = placement_service.can_take_placement(user)
    return {
        "has_taken_placement": bool(user.placement_taken_at),
        "level": user.placement_level,
        "score_percentage": user.placement_score,
        "placement_taken_at": user.placement_taken_at.isoformat() if user.placement_taken_at else None,
        "can_retake": can_retake,
        "cooldown_message": cooldown_msg
    }

@router.get("/placement/start")
async def start_placement_quiz(force: bool = Query(False), db: Session = Depends(get_db)):
    """
    Samples 20 adaptive questions from validated placement question bank.
    Enforces 7-day retake cooldown unless force=True for testing.
    """
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not force:
        can_retake, cooldown_msg = placement_service.can_take_placement(user)
        if not can_retake:
            raise HTTPException(status_code=403, detail=cooldown_msg)

    questions = placement_service.sample_placement_questions(db, count=settings.PLACEMENT_QUESTIONS_COUNT)
    client_questions = [q.to_dict(include_answer=False) for q in questions]

    return {
        "quiz_type": "placement",
        "total_questions": len(client_questions),
        "questions": client_questions
    }

@router.post("/placement/submit")
async def submit_placement_quiz(payload: PlacementSubmitRequest, db: Session = Depends(get_db)):
    """
    Deterministically scores placement quiz, computes level rank,
    unlocks roadmap modules, awards XP, and generates LLM explanation.
    """
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch referenced questions from DB
    questions = db.query(Question).filter(Question.id.in_(payload.question_ids)).all()
    if len(questions) < len(payload.question_ids):
        raise HTTPException(status_code=400, detail="Invalid question IDs provided")

    # Deterministic scoring
    result = placement_service.compute_placement_result(questions, payload.answers)
    level = result["level"]
    score_pct = result["score_percentage"]
    topic_breakdown = result["topic_breakdown"]
    weak_topics = result["weak_topics"]

    # Generate LLM explanation (or graceful offline fallback)
    explanation = await placement_service.generate_explanation(
        level=level,
        score_pct=score_pct,
        topic_breakdown=topic_breakdown,
        weak_topics=weak_topics
    )

    # Award idempotent XP
    now = datetime.datetime.now(datetime.timezone.utc)
    attempt_id = str(uuid.uuid4())
    idempotency_key = f"placement-{user.id}-{int(now.timestamp())}"
    
    xp_amount = settings.PLACEMENT_BASE_XP
    db.add(XPEvent(
        id=str(uuid.uuid4()),
        user_id=user.id,
        source="placement_quiz",
        amount=xp_amount,
        metadata_json=json.dumps({"level": level, "score": score_pct}),
        idempotency_key=idempotency_key
    ))
    user.total_xp += xp_amount

    # Update User Placement State
    user.placement_level = level
    user.placement_score = score_pct
    user.placement_taken_at = now

    # Record Quiz Attempt
    attempt = QuizAttempt(
        id=attempt_id,
        user_id=user.id,
        module_id=None,
        is_placement=True,
        score_correct=result["correct_count"],
        total_questions=result["total_questions"],
        score_percentage=score_pct,
        passed=True,
        answers_json=json.dumps(payload.answers),
        question_ids_json=json.dumps(payload.question_ids),
        weak_topics_json=json.dumps(weak_topics),
        xp_awarded=xp_amount
    )
    db.add(attempt)

    # Server-Side Roadmap Module Unlocking
    placement_service.apply_placement_unlocks(db, user, level, topic_breakdown)

    db.commit()
    db.refresh(user)

    return {
        "status": "success",
        "attempt_id": attempt_id,
        "level": level,
        "score_percentage": score_pct,
        "correct_count": result["correct_count"],
        "total_questions": result["total_questions"],
        "topic_breakdown": topic_breakdown,
        "weak_topics": weak_topics,
        "explanation": explanation,
        "xp_awarded": xp_amount,
        "new_total_xp": user.total_xp,
        "review": result["review"]
    }

# Legacy single question endpoints for backward compatibility
@router.get("/{skill_id}/questions", response_model=List[AssessmentQuestion])
async def get_questions(skill_id: str):
    return assessment_service.get_questions_for_skill(skill_id)

@router.post("/{skill_id}/submit", response_model=AssessmentFeedback)
async def submit_answer(skill_id: str, payload: SubmitPayload, db: Session = Depends(get_db)):
    feedback = assessment_service.evaluate_answer(
        question_id=payload.question_id,
        selected_index=payload.selected_option_index,
        current_consecutive_correct=payload.consecutive_correct
    )
    if feedback.is_correct:
        user = db.query(User).filter(User.id == DEMO_USER_ID).first()
        if user:
            user.total_xp += feedback.points_earned
            db.commit()
    return feedback

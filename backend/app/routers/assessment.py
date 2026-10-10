from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from ..models.schemas import AssessmentQuestion, AssessmentFeedback, AssessmentAnswerSubmission
from ..services.assessment_service import assessment_service
from .auth import DEMO_USER

router = APIRouter(prefix="/assessment", tags=["assessment"])

class SubmitPayload(BaseModel):
    question_id: str
    selected_option_index: int
    consecutive_correct: int = 0

@router.get("/{skill_id}/questions", response_model=List[AssessmentQuestion])
async def get_questions(skill_id: str):
    return assessment_service.get_questions_for_skill(skill_id)

@router.post("/{skill_id}/submit", response_model=AssessmentFeedback)
async def submit_answer(skill_id: str, payload: SubmitPayload):
    feedback = assessment_service.evaluate_answer(
        question_id=payload.question_id,
        selected_index=payload.selected_option_index,
        current_consecutive_correct=payload.consecutive_correct
    )
    if feedback.is_correct:
        DEMO_USER.points += feedback.points_earned
    return feedback

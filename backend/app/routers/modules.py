import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session

from ..config import settings
from ..models.db_models import User, Module, UserModuleProgress, QuizAttempt, Course, ResumeAnalysis
from ..models.schemas import LessonContent, GenerateLessonRequest
from ..core.database import get_db
from ..services.module_quiz_service import module_quiz_service
from ..services.rag_service import rag_service
from ..services.llm_service import llm_service

router = APIRouter(prefix="/modules", tags=["modules"])

DEMO_USER_ID = "usr-aarav-sharma"

class ModuleQuizSubmitRequest(BaseModel):
    attempt_id: str
    question_ids: List[str]
    answers: Dict[str, int]

@router.get("/courses")
async def list_courses(db: Session = Depends(get_db)):
    """Returns all available career track courses."""
    courses = db.query(Course).all()
    return [
        {
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "target_role": c.target_role,
            "modules_count": len(c.modules)
        }
        for c in courses
    ]

@router.get("/")
async def list_modules(course_id: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Returns modules for the requested course (or user's career goal).
    Dynamically prioritizes and adapts module sequence based on the user's specific ATS skill gaps.
    """
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Resolve course_id from param or user career goal
    effective_course_id = course_id
    if not effective_course_id:
        goal = (user.career_goal or "").lower()
        if "data" in goal:
            effective_course_id = "data-engineer"
        elif "cyber" in goal or "security" in goal:
            effective_course_id = "cybersecurity"
        else:
            effective_course_id = "ai-engineer"

    modules = db.query(Module).filter(Module.course_id == effective_course_id).order_by(Module.order_index).all()
    if not modules:
        # Fallback to ai-engineer if course_id had no modules
        effective_course_id = "ai-engineer"
        modules = db.query(Module).filter(Module.course_id == "ai-engineer").order_by(Module.order_index).all()

    # Retrieve user's latest missing skill gaps from ATS resume analysis
    latest_resume = db.query(ResumeAnalysis).filter(
        ResumeAnalysis.user_id == user.id
    ).order_by(ResumeAnalysis.created_at.desc()).first()

    user_gaps: List[str] = []
    if latest_resume and latest_resume.missing_skills_json:
        try:
            user_gaps = json.loads(latest_resume.missing_skills_json)
        except Exception:
            user_gaps = []

    results = []
    for mod in modules:
        progress = db.query(UserModuleProgress).filter(
            UserModuleProgress.user_id == user.id,
            UserModuleProgress.module_id == mod.id
        ).first()

        status = progress.status if progress else ("available" if mod.order_index == 1 else "locked")
        best_score = progress.best_score if progress else 0

        # Cross-reference module competencies with identified user skill gaps
        mod_skills = json.loads(mod.skills_json) if mod.skills_json else []
        mod_topics = json.loads(mod.topics_json) if mod.topics_json else []
        all_keywords = [s.lower() for s in (mod_skills + mod_topics)]

        targeted_gaps = [
            gap for gap in user_gaps
            if any(gap.lower() in kw or kw in gap.lower() for kw in all_keywords)
        ]
        is_gap_targeted = len(targeted_gaps) > 0

        m_dict = mod.to_dict()
        m_dict["status"] = status
        m_dict["best_score"] = best_score
        m_dict["is_gap_targeted"] = is_gap_targeted
        m_dict["targeted_gaps"] = targeted_gaps
        m_dict["custom_recommendation"] = (
            f"Prioritized for you: Directly bridges your ATS gap in {', '.join(targeted_gaps[:2])}."
            if is_gap_targeted else None
        )
        results.append(m_dict)

    # Adaptive Sorting: Modules bridging critical gaps are prioritized to the front of the learning path
    # while maintaining completion state
    def adaptive_sort_key(m):
        # 0: Gap-targeted & not yet passed (Highest Priority)
        # 1: Standard available / in-progress
        # 2: Locked standard
        # 3: Completed / passed
        is_targeted = m.get("is_gap_targeted", False)
        st = m.get("status", "locked")
        if st == "passed":
            rank = 3
        elif is_targeted:
            rank = 0
        elif st in ("available", "in_progress"):
            rank = 1
        else:
            rank = 2
        return (rank, m.get("order_index", 1))

    results.sort(key=adaptive_sort_key)

    # Ensure the top-most module is accessible (unlocked)
    if results and results[0]["status"] == "locked":
        results[0]["status"] = "available"

    return {
        "course_id": effective_course_id,
        "total_modules": len(results),
        "user_skill_gaps_addressed": len([m for m in results if m["is_gap_targeted"]]),
        "modules": results
    }

@router.get("/{module_id}")
async def get_module_detail(module_id: str, db: Session = Depends(get_db)):
    """
    Returns full module detail including lessons, resources, and quiz metadata.
    Refuses access with 403 if the module is locked.
    """
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    module, progress = module_quiz_service.get_module_with_access_check(db, user, module_id)

    # Get grounded resources for this module from RAG service
    skills = json.loads(module.skills_json) if module.skills_json else []
    query_topic = skills[0] if skills else module.title
    resources_data = rag_service.search_resources(query_topic)

    m_dict = module.to_dict()
    m_dict["status"] = progress.status
    m_dict["best_score"] = progress.best_score
    m_dict["attempts_count"] = progress.attempts_count
    m_dict["resources"] = resources_data

    # Return latest attempt if any
    latest_attempt = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == user.id,
        QuizAttempt.module_id == module_id
    ).order_by(QuizAttempt.created_at.desc()).first()

    if latest_attempt:
        m_dict["latest_attempt"] = {
            "id": latest_attempt.id,
            "score_correct": latest_attempt.score_correct,
            "total_questions": latest_attempt.total_questions,
            "passed": latest_attempt.passed,
            "created_at": latest_attempt.created_at.isoformat()
        }
    else:
        m_dict["latest_attempt"] = None

    return m_dict

@router.get("/{module_id}/quiz/start")
async def start_module_quiz(module_id: str, db: Session = Depends(get_db)):
    """
    Starts a module quiz: draws 15 questions from the validated module bank.
    Refuses access with 403 if the module is locked.
    """
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return module_quiz_service.sample_module_quiz(db, user, module_id)

@router.post("/{module_id}/quiz/submit")
async def submit_module_quiz(
    module_id: str,
    payload: ModuleQuizSubmitRequest,
    db: Session = Depends(get_db)
):
    """
    Server-side scoring of 15 questions.
    Enforces 65% pass mark (10/15 correct answers required).
    Unlocks next module on pass. Awards idempotent XP.
    """
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return module_quiz_service.evaluate_module_quiz(
        db=db,
        user=user,
        module_id=module_id,
        attempt_id=payload.attempt_id,
        question_ids=payload.question_ids,
        answers=payload.answers
    )

@router.get("/{module_id}/quiz/history")
async def get_quiz_history(module_id: str, db: Session = Depends(get_db)):
    """Returns past attempts for this module."""
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    attempts = db.query(QuizAttempt).filter(
        QuizAttempt.user_id == user.id,
        QuizAttempt.module_id == module_id
    ).order_by(QuizAttempt.created_at.desc()).all()

    return [
        {
            "id": a.id,
            "score_correct": a.score_correct,
            "total_questions": a.total_questions,
            "score_percentage": a.score_percentage,
            "passed": a.passed,
            "xp_awarded": a.xp_awarded,
            "created_at": a.created_at.isoformat()
        }
        for a in attempts
    ]

@router.post("/{module_id}/lesson", response_model=LessonContent)
async def generate_module_lesson(
    module_id: str,
    payload: GenerateLessonRequest,
    db: Session = Depends(get_db)
):
    """
    Generates an adaptive interactive lesson using OmniRoute LLM gateway.
    Adapts explanation depth based on student entry level (scratch / basics vs advanced).
    Provides structured runnable code, analogies, common pitfalls, and hands-on exercises.
    """
    user = db.query(User).filter(User.id == DEMO_USER_ID).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    module, progress = module_quiz_service.get_module_with_access_check(db, user, module_id)

    topic = payload.topic_name.strip()
    is_scratch = payload.level.lower() == "scratch"

    badge = "Foundational Basics (Zero Assumptions)" if is_scratch else "Intermediate Deep Dive"

    # Robust fallback lesson tailored to the topic
    fallback = LessonContent(
        title=f"{topic} — Foundational Guide",
        level_badge=badge,
        estimated_read_time="6 mins",
        analogy=(
            f"Think of {topic} like learning how to ride a bicycle with training wheels: "
            "before you perform complex tricks, you need to understand how the pedals, chain, and handlebars work together. "
            "In computing and machine learning, this foundational concept serves as the core building block for all downstream pipelines."
        ),
        core_explanation=(
            f"Welcome to your lesson on {topic}! Starting from scratch, here is everything you need to know step-by-step:\n\n"
            "1. Core Purpose: Why does this concept exist? In modern software and AI engineering, we must process structured data reliably and efficiently without memory bottlenecks.\n\n"
            "2. Fundamental Mechanics: Every instruction executes deterministically. When you define variables, arrays, or functions, memory is allocated and processed in sequential order.\n\n"
            "3. Best Practice Patterns: Write clean, readable code with explicit type annotations and modular function boundaries. Avoid deeply nested control flow whenever vectorized or comprehension patterns can be used."
        ),
        code_example=(
            f"# Python Basics: Hands-on implementation of {topic}\n"
            "def demonstrate_concept(items: list[int]) -> dict[str, int | float]:\n"
            "    \"\"\"Calculates baseline statistics demonstrating foundational logic.\"\"\"\n"
            "    total = sum(items)\n"
            "    count = len(items)\n"
            "    average = total / count if count > 0 else 0.0\n"
            "    return {\n"
            "        'total_sum': total,\n"
            "        'item_count': count,\n"
            "        'mean_value': round(average, 2)\n"
            "    }\n\n"
            "# Run with sample inputs\n"
            "sample_data = [12, 24, 36, 48, 60]\n"
            "result = demonstrate_concept(sample_data)\n"
            "print(f'Processed {topic} successfully: {result}')"
        ),
        common_mistakes=[
            "Assuming zero-indexed collections start at 1 instead of 0.",
            "Modifying a list while iterating directly over it.",
            "Neglecting boundary conditions (such as empty collections or division by zero)."
        ],
        practice_exercise=(
            f"Write a short function that accepts a list of numbers and returns only the even values multiplied by 2. "
            "Verify that it handles an empty list without raising an error."
        ),
        practice_solution=(
            "def double_evens(nums: list[int]) -> list[int]:\n"
            "    return [n * 2 for n in nums if n % 2 == 0]\n\n"
            "# Test:\n"
            "assert double_evens([1, 2, 3, 4]) == [4, 8]\n"
            "assert double_evens([]) == []"
        ),
        ai_tutor_tip=(
            "NovaPath Mentor Tip: As a beginner starting from scratch, don't worry about memorizing syntax. "
            "Focus on understanding the mental model. Once the concept clicks, syntax becomes muscle memory!"
        )
    )

    system_prompt = (
        "You are NovaPath AI's expert personal academic tutor. "
        "Generate an engaging, pedagogically rigorous lesson tailored to the student's entry background. "
        + (
            "The student is starting from scratch (level='scratch'). Assume ZERO prior knowledge. "
            "Explain core fundamentals step-by-step from square one using a vivid real-world analogy, "
            "clear foundational explanations, clean runnable code examples with line-by-line comments, "
            "common traps beginners fall into, a small hands-on practice challenge, and an encouraging AI tutor tip."
            if is_scratch else
            "The student has basic familiarity. Provide an accelerated intermediate lesson with architecture intuition, "
            "production-grade code patterns, and practical optimization tips."
        )
    )

    user_message = (
        f"Generate a customized lesson for the module '{module.title}', focusing on topic '{topic}'. "
        f"Student background: {payload.level}."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    try:
        lesson = await llm_service.chat_json(
            messages=messages,
            schema=LessonContent,
            fallback=fallback,
            temperature=0.3,
            max_tokens=1400
        )
        return lesson
    except Exception as e:
        return fallback

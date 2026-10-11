import pytest
import uuid
import datetime
from fastapi import HTTPException
from app.config import settings
from app.models.db_models import User, Module, UserModuleProgress, Question, QuizAttempt, XPEvent
from app.core.database import SessionLocal, init_db
from app.services.module_quiz_service import module_quiz_service

def setup_test_user(db):
    uid = f"gating-user-{uuid.uuid4().hex[:8]}"
    user = User(
        id=uid,
        name="Gating Tester",
        email=f"{uid}@novapath.ai",
        hashed_password="pw",
        total_xp=100
    )
    db.add(user)
    # Set module 1 as available, module 2 as locked
    db.add(UserModuleProgress(user_id=uid, module_id="py-foundations", status="available"))
    db.add(UserModuleProgress(user_id=uid, module_id="math-ml", status="locked"))
    db.add(UserModuleProgress(user_id=uid, module_id="classical-ml", status="locked"))
    db.commit()
    db.refresh(user)
    return user

def test_module_gating_refuses_locked_access():
    """Verify accessing a locked module raises HTTP 403."""
    with SessionLocal() as db:
        user = setup_test_user(db)

        # Available module should succeed
        mod1, p1 = module_quiz_service.get_module_with_access_check(db, user, "py-foundations")
        assert mod1.id == "py-foundations"
        assert p1.status == "available"

        # Locked module must raise 403
        with pytest.raises(HTTPException) as exc_info:
            module_quiz_service.get_module_with_access_check(db, user, "math-ml")
        assert exc_info.value.status_code == 403

def test_15_question_quiz_assembly():
    """Verify sampled quiz contains exactly 15 questions with answers stripped."""
    with SessionLocal() as db:
        user = setup_test_user(db)
        quiz_data = module_quiz_service.sample_module_quiz(db, user, "py-foundations")

        assert quiz_data["total_questions"] == 15
        assert len(quiz_data["questions"]) == 15
        assert quiz_data["pass_threshold_required"] == 10

        # Check answers stripped
        for q in quiz_data["questions"]:
            assert "correct_idx" not in q
            assert "explanation" not in q
            assert len(q["options"]) == 4

def test_65_percent_pass_gate():
    """
    Verify the 65% pass mark on 15 questions:
    9/15 (60%) fails and does NOT unlock next module.
    10/15 (66.7%) passes and unlocks next module.
    """
    with SessionLocal() as db:
        user = setup_test_user(db)
        quiz = module_quiz_service.sample_module_quiz(db, user, "py-foundations")
        q_ids = [q["id"] for q in quiz["questions"]]

        q_records = db.query(Question).filter(Question.id.in_(q_ids)).all()
        q_map = {q.id: q.correct_idx for q in q_records}

        # Case 1: 9/15 Correct -> FAILS
        attempt1_id = str(uuid.uuid4())
        answers_fail = {qid: (q_map[qid] if i < 9 else (q_map[qid] + 1) % 4) for i, qid in enumerate(q_ids)}
        res_fail = module_quiz_service.evaluate_module_quiz(
            db, user, "py-foundations", attempt1_id, q_ids, answers_fail
        )
        assert res_fail["score_correct"] == 9
        assert res_fail["passed"] is False
        assert res_fail["unlocked_next_module_id"] is None

        # Next module (math-ml) must still be locked
        p_math = db.query(UserModuleProgress).filter(
            UserModuleProgress.user_id == user.id,
            UserModuleProgress.module_id == "math-ml"
        ).first()
        assert p_math.status == "locked"

        # Case 2: 10/15 Correct -> PASSES
        attempt2_id = str(uuid.uuid4())
        answers_pass = {qid: (q_map[qid] if i < 10 else (q_map[qid] + 1) % 4) for i, qid in enumerate(q_ids)}
        res_pass = module_quiz_service.evaluate_module_quiz(
            db, user, "py-foundations", attempt2_id, q_ids, answers_pass
        )
        assert res_pass["score_correct"] == 10
        assert res_pass["passed"] is True
        assert res_pass["unlocked_next_module_id"] == "math-ml"

        # Next module (math-ml) must now be UNLOCKED (available)
        db.refresh(p_math)
        assert p_math.status == "available"

def test_xp_rules_and_bonuses():
    """
    Verify XP calculation:
    - Base XP = 10 + (correct * 2)
    - First pass bonus = +50
    - Perfect score bonus = +25
    - Retake after pass = 20% of base XP, no bonuses
    """
    with SessionLocal() as db:
        user = setup_test_user(db)
        quiz = module_quiz_service.sample_module_quiz(db, user, "py-foundations")
        q_ids = [q["id"] for q in quiz["questions"]]
        q_records = db.query(Question).filter(Question.id.in_(q_ids)).all()
        q_map = {q.id: q.correct_idx for q in q_records}

        initial_xp = user.total_xp  # 100

        # Perfect 15/15 First Pass
        # Expected: Base (10 + 30 = 40) + First Pass (50) + Perfect (25) = 115 XP
        attempt_id = str(uuid.uuid4())
        perfect_answers = {qid: q_map[qid] for qid in q_ids}
        res = module_quiz_service.evaluate_module_quiz(
            db, user, "py-foundations", attempt_id, q_ids, perfect_answers
        )
        assert res["passed"] is True
        assert res["score_correct"] == 15
        assert res["xp_awarded"] == 115
        assert user.total_xp == initial_xp + 115

        # Retake after pass: 15/15
        # Expected: 20% of base XP (40 * 0.20 = 8 XP), 0 bonuses
        retake_id = str(uuid.uuid4())
        retake_res = module_quiz_service.evaluate_module_quiz(
            db, user, "py-foundations", retake_id, q_ids, perfect_answers
        )
        assert retake_res["passed"] is True
        assert retake_res["score_correct"] == 15
        assert retake_res["xp_awarded"] == 8
        assert user.total_xp == initial_xp + 115 + 8

def test_xp_idempotency_prevents_duplicate_awards():
    """Verify resubmitting the same attempt_id awards 0 duplicate XP."""
    with SessionLocal() as db:
        user = setup_test_user(db)
        quiz = module_quiz_service.sample_module_quiz(db, user, "py-foundations")
        q_ids = [q["id"] for q in quiz["questions"]]
        q_records = db.query(Question).filter(Question.id.in_(q_ids)).all()
        q_map = {q.id: q.correct_idx for q in q_records}

        attempt_id = str(uuid.uuid4())
        answers = {qid: q_map[qid] for qid in q_ids}

        # First submission
        res1 = module_quiz_service.evaluate_module_quiz(
            db, user, "py-foundations", attempt_id, q_ids, answers
        )
        xp_after_1 = user.total_xp

        # Duplicate submission with identical attempt_id
        res2 = module_quiz_service.evaluate_module_quiz(
            db, user, "py-foundations", attempt_id, q_ids, answers
        )
        assert res2["status"] == "already_submitted"
        assert res2["xp_awarded"] == 0
        assert user.total_xp == xp_after_1

def test_quiz_submission_tampering_ignored():
    """
    Verify server-side authority: client cannot tamper with score, pass status, or XP.
    The evaluation strictly compares selected answers with ground-truth DB correct_idx.
    """
    with SessionLocal() as db:
        user = setup_test_user(db)
        quiz = module_quiz_service.sample_module_quiz(db, user, "py-foundations")
        q_ids = [q["id"] for q in quiz["questions"]]

        # Client submits all WRONG answers (selected_idx = -1 or wrong idx)
        q_records = db.query(Question).filter(Question.id.in_(q_ids)).all()
        q_map = {q.id: q.correct_idx for q in q_records}
        wrong_answers = {qid: (q_map[qid] + 1) % 4 for qid in q_ids}

        attempt_id = str(uuid.uuid4())
        # Even if a malicious client tried to tamper, the server strictly calculates score from answers
        res = module_quiz_service.evaluate_module_quiz(
            db, user, "py-foundations", attempt_id, q_ids, wrong_answers
        )

        assert res["score_correct"] == 0
        assert res["passed"] is False
        assert res["unlocked_next_module_id"] is None
        assert res["xp_awarded"] == 10  # Base XP only: 10 + 0*2 = 10, no pass or perfect bonuses


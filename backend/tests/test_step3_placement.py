import pytest
import datetime
import uuid
from app.config import settings
from app.models.db_models import User, Question, UserModuleProgress, XPEvent
from app.core.database import SessionLocal, init_db
from app.services.placement_service import placement_service

def test_placement_level_ranking_thresholds():
    """Verify deterministic ranking: Beginner < 40%, Intermediate 40-74%, Advanced >= 75%."""
    with SessionLocal() as db:
        questions = placement_service.sample_placement_questions(db, count=20)
        assert len(questions) == 20

        # Case 1: Low score (3/20 correct) -> Beginner
        low_answers = {q.id: (q.correct_idx if i < 3 else (q.correct_idx + 1) % 4) for i, q in enumerate(questions)}
        low_res = placement_service.compute_placement_result(questions, low_answers)
        assert low_res["level"] == "Beginner"
        assert low_res["score_percentage"] < 40.0

        # Case 2: Mid score (11/20 correct) -> Intermediate
        mid_answers = {q.id: (q.correct_idx if i < 11 else (q.correct_idx + 1) % 4) for i, q in enumerate(questions)}
        mid_res = placement_service.compute_placement_result(questions, mid_answers)
        assert mid_res["level"] == "Intermediate"
        assert 40.0 <= mid_res["score_percentage"] < 75.0

        # Case 3: High score (19/20 correct) -> Advanced
        high_answers = {q.id: (q.correct_idx if i < 19 else (q.correct_idx + 1) % 4) for i, q in enumerate(questions)}
        high_res = placement_service.compute_placement_result(questions, high_answers)
        assert high_res["level"] == "Advanced"
        assert high_res["score_percentage"] >= 75.0

def test_roadmap_unlocking_by_placement_level():
    """Verify level sets roadmap start: Beginner starts at mod 1; Advanced skips foundations."""
    with SessionLocal() as db:
        test_uid = f"level-test-{uuid.uuid4().hex[:8]}"
        user = User(
            id=test_uid,
            name="Placement Tester",
            email=f"{test_uid}@test.edu",
            hashed_password="pw"
        )
        db.add(user)
        db.commit()

        # 1. Beginner Test
        placement_service.apply_placement_unlocks(db, user, "Beginner", {})
        db.commit()
        p1 = db.query(UserModuleProgress).filter(UserModuleProgress.user_id == user.id, UserModuleProgress.module_id == "py-foundations").first()
        p2 = db.query(UserModuleProgress).filter(UserModuleProgress.user_id == user.id, UserModuleProgress.module_id == "math-ml").first()
        assert p1.status == "available"
        assert p2.status == "locked"

        # 2. Advanced Test
        placement_service.apply_placement_unlocks(db, user, "Advanced", {})
        db.commit()
        mod1 = db.query(UserModuleProgress).filter(UserModuleProgress.user_id == user.id, UserModuleProgress.module_id == "py-foundations").first()
        mod2 = db.query(UserModuleProgress).filter(UserModuleProgress.user_id == user.id, UserModuleProgress.module_id == "math-ml").first()
        mod3 = db.query(UserModuleProgress).filter(UserModuleProgress.user_id == user.id, UserModuleProgress.module_id == "classical-ml").first()
        mod4 = db.query(UserModuleProgress).filter(UserModuleProgress.user_id == user.id, UserModuleProgress.module_id == "deep-learning").first()
        mod5 = db.query(UserModuleProgress).filter(UserModuleProgress.user_id == user.id, UserModuleProgress.module_id == "rag-systems").first()
        
        # Foundations skipped/passed
        assert mod1.status == "passed"
        assert mod2.status == "passed"
        assert mod3.status == "passed"
        # First post-foundation available
        assert mod4.status == "available"
        # Remaining locked
        assert mod5.status == "locked"

def test_placement_retake_cooldown_7_days():
    """Verify 7-day retake cooldown is strictly enforced."""
    now = datetime.datetime.now(datetime.timezone.utc)
    user = User(
        id=f"cd-user-{uuid.uuid4().hex[:8]}",
        name="Cooldown Tester",
        email="cd@test.edu",
        hashed_password="pw",
        placement_taken_at=now - datetime.timedelta(days=2)  # Taken 2 days ago
    )

    can_retake, msg = placement_service.can_take_placement(user)
    assert can_retake is False
    assert "cooldown" in msg.lower()

    # User taken 8 days ago
    user.placement_taken_at = now - datetime.timedelta(days=8)
    can_retake_after, msg_after = placement_service.can_take_placement(user)
    assert can_retake_after is True
    assert msg_after is None

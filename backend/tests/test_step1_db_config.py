import pytest
import os
import json
import uuid
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.config import settings
from app.models.db_models import (
    Base,
    User,
    Course,
    Module,
    UserModuleProgress,
    Question,
    QuizAttempt,
    XPEvent,
    ResumeAnalysis
)
from app.core.database import init_db, SessionLocal, engine

def test_config_values():
    """Verify all configuration thresholds and rules match Requirements Update v2."""
    # Section A: Placement quiz & level ranking
    assert settings.PLACEMENT_BEGINNER_MAX_RATIO == 0.39
    assert settings.PLACEMENT_INTERMEDIATE_MAX_RATIO == 0.74
    assert settings.PLACEMENT_ADVANCED_MIN_RATIO == 0.75
    assert settings.PLACEMENT_RETAKE_COOLDOWN_DAYS == 7
    assert settings.PLACEMENT_QUESTIONS_COUNT == 20
    assert settings.PLACEMENT_BASE_XP == 50

    # Section B: Course structure & gating
    assert settings.MODULE_QUIZ_QUESTIONS_COUNT == 15
    assert settings.MODULE_QUIZ_PASS_THRESHOLD_RATIO == 0.65
    assert settings.MODULE_QUIZ_PASS_MIN_CORRECT == 10
    assert settings.MODULE_BANK_MIN_QUESTIONS == 40

    # Section C: XP system
    assert settings.XP_BASE_FIXED == 10
    assert settings.XP_PER_CORRECT_ANSWER == 2
    assert settings.XP_FIRST_PASS_BONUS == 50
    assert settings.XP_PERFECT_SCORE_BONUS == 25
    assert settings.XP_RETAKE_BASE_RATIO == 0.20

    # Section E: ATS scoring weights (must sum to exactly 1.00)
    total_weights = (
        settings.ATS_WEIGHT_ROLE_FIT +
        settings.ATS_WEIGHT_KEYWORD_COVERAGE +
        settings.ATS_WEIGHT_SECTION_COMPLETENESS +
        settings.ATS_WEIGHT_FORMATTING +
        settings.ATS_WEIGHT_QUANTIFIED_IMPACT
    )
    assert abs(total_weights - 1.00) < 1e-6
    assert settings.ATS_WEIGHT_ROLE_FIT == 0.40
    assert settings.ATS_WEIGHT_KEYWORD_COVERAGE == 0.25
    assert settings.ATS_WEIGHT_SECTION_COMPLETENESS == 0.15
    assert settings.ATS_WEIGHT_FORMATTING == 0.10
    assert settings.ATS_WEIGHT_QUANTIFIED_IMPACT == 0.10

def test_db_initialization_and_seeding():
    """Verify database initialization creates all tables and seeds core records."""
    init_db()

    with SessionLocal() as db:
        # Check course
        course = db.query(Course).filter(Course.id == "ai-engineer").first()
        assert course is not None
        assert course.target_role == "AI Engineer"

        # Check the core modules
        modules = db.query(Module).filter(Module.course_id == "ai-engineer").order_by(Module.order_index).all()
        expected_ids = ["py-foundations", "math-ml", "classical-ml", "deep-learning", "rag-systems", "mlops-deploy"]
        core_modules = [m for m in modules if m.id in expected_ids]
        assert len(core_modules) == 6
        assert [m.id for m in core_modules] == expected_ids
        assert len(modules) >= 6

        # Check demo user
        demo_user = db.query(User).filter(User.id == "usr-aarav-sharma").first()
        assert demo_user is not None
        assert demo_user.email == "aarav.sharma@vizag.edu"
        assert demo_user.total_xp >= 860

        # Check user module progression
        progress = db.query(UserModuleProgress).filter(UserModuleProgress.user_id == demo_user.id).all()
        core_progress = [p for p in progress if p.module_id in expected_ids]
        assert len(core_progress) == 6
        assert len(progress) >= 6

def test_xp_ledger_and_idempotency():
    """Verify XP events ledger records entries and strictly enforces idempotency keys."""
    test_user_id = f"test-user-{uuid.uuid4().hex[:8]}"

    with SessionLocal() as db:
        user = User(
            id=test_user_id,
            name="Test User",
            email=f"{test_user_id}@novapath.ai",
            hashed_password="pw",
            total_xp=0
        )
        db.add(user)
        db.commit()

        # Insert first XP event
        idempotency_key = f"quiz-attempt-{test_user_id}-1"
        event1 = XPEvent(
            user_id=test_user_id,
            source="module_quiz_pass",
            amount=80,
            metadata_json=json.dumps({"correct": 10, "module_id": "py-foundations"}),
            idempotency_key=idempotency_key
        )
        db.add(event1)
        user.total_xp += 80
        db.commit()

        # Query user XP and ledger
        events = db.query(XPEvent).filter(XPEvent.user_id == test_user_id).all()
        assert len(events) == 1
        assert sum(e.amount for e in events) == 80

        # Attempt to insert duplicate event with identical idempotency_key must raise IntegrityError
        event2 = XPEvent(
            user_id=test_user_id,
            source="module_quiz_pass",
            amount=80,
            metadata_json=json.dumps({"correct": 10, "module_id": "py-foundations"}),
            idempotency_key=idempotency_key
        )
        db.add(event2)
        with pytest.raises(IntegrityError):
            db.commit()
        db.rollback()

def test_persistence_across_sessions():
    """Verify records survive across independent session creation and SQLite file."""
    test_uid = f"persist-user-{uuid.uuid4().hex[:8]}"

    # Session 1: Create user & progress
    with SessionLocal() as session1:
        u = User(
            id=test_uid,
            name="Persistence Test",
            email=f"{test_uid}@novapath.ai",
            hashed_password="pw",
            total_xp=500,
            placement_level="Intermediate",
            placement_score=60.0
        )
        session1.add(u)
        session1.commit()

    # Session 2: Read back from fresh session
    with SessionLocal() as session2:
        saved_user = session2.query(User).filter(User.id == test_uid).first()
        assert saved_user is not None
        assert saved_user.total_xp == 500
        assert saved_user.placement_level == "Intermediate"
        assert saved_user.placement_score == 60.0

        # Mutate
        saved_user.total_xp += 150
        session2.commit()

    # Session 3: Confirm mutation persisted
    with SessionLocal() as session3:
        mutated_user = session3.query(User).filter(User.id == test_uid).first()
        assert mutated_user is not None
        assert mutated_user.total_xp == 650

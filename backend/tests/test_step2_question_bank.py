import pytest
import os
import json
import random
from sqlalchemy.orm import Session
from app.config import settings
from app.models.db_models import Question
from app.core.database import SessionLocal

def test_question_bank_counts():
    """Verify that every module and placement quiz has at least 40 validated questions."""
    with SessionLocal() as db:
        modules = ["py-foundations", "math-ml", "classical-ml", "deep-learning", "rag-systems", "mlops-deploy"]
        for mod in modules:
            count = db.query(Question).filter(Question.module_id == mod).count()
            assert count >= settings.MODULE_BANK_MIN_QUESTIONS, f"Module {mod} has only {count} questions, expected >= {settings.MODULE_BANK_MIN_QUESTIONS}"

        placement_count = db.query(Question).filter(Question.is_placement == True).count()
        assert placement_count >= 40, f"Placement bank has {placement_count} questions, expected >= 40"

def test_question_schema_integrity():
    """Verify all 294 questions have exactly 4 distinct options, 1 valid correct_idx, and explanation."""
    with SessionLocal() as db:
        all_questions = db.query(Question).all()
        assert len(all_questions) >= 252

        seen_texts = set()
        for q in all_questions:
            # Question text
            assert q.question_text and len(q.question_text.strip()) > 10
            assert q.question_text not in seen_texts, f"Duplicate question text: {q.question_text}"
            seen_texts.add(q.question_text)

            # Options
            options = json.loads(q.options_json)
            assert len(options) == 4, f"Question {q.id} must have exactly 4 options"
            assert len(set(options)) == 4, f"Question {q.id} has duplicate options: {options}"

            # Correct index
            assert q.correct_idx in [0, 1, 2, 3], f"Question {q.id} has invalid correct_idx: {q.correct_idx}"

            # Explanation
            assert q.explanation and len(q.explanation.strip()) > 10, f"Question {q.id} lacks explanation"

            # Difficulty
            assert q.difficulty in ["Easy", "Medium", "Hard", "Expert"]

def test_quiz_sampling_hides_answers():
    """Verify sampled 15-question quiz does not expose correct answers or explanations."""
    with SessionLocal() as db:
        questions = db.query(Question).filter(Question.module_id == "py-foundations").all()
        assert len(questions) >= 15

        sample = random.sample(questions, 15)
        assert len(sample) == 15
        assert len(set(q.id for q in sample)) == 15

        # Check client payload rendering
        client_payload = [q.to_dict(include_answer=False) for q in sample]
        for item in client_payload:
            assert "correct_idx" not in item
            assert "explanation" not in item
            assert len(item["options"]) == 4

def test_retake_question_sampling_variance():
    """Verify two sequential samplings from the 42-question pool yield distinct question sets."""
    with SessionLocal() as db:
        pool = db.query(Question).filter(Question.module_id == "math-ml").all()
        ids_pool = [q.id for q in pool]
        assert len(ids_pool) >= 40

        sample_1 = set(random.sample(ids_pool, 15))
        sample_2 = set(random.sample(ids_pool, 15))

        # Two independent 15-question samples from a 42-question pool should not be identical
        assert sample_1 != sample_2, "Retake question samples should differ"

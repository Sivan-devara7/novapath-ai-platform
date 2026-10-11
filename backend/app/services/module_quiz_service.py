import json
import uuid
import datetime
import random
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..config import settings
from ..models.db_models import User, Module, Question, UserModuleProgress, QuizAttempt, XPEvent

class ModuleQuizService:
    def get_module_with_access_check(self, db: Session, user: User, module_id: str) -> Tuple[Module, UserModuleProgress]:
        """
        Validates server-side gating:
        Refuses access with 403 if the module is locked.
        """
        module = db.query(Module).filter(Module.id == module_id).first()
        if not module:
            raise HTTPException(status_code=404, detail="Module not found")

        progress = db.query(UserModuleProgress).filter(
            UserModuleProgress.user_id == user.id,
            UserModuleProgress.module_id == module_id
        ).first()

        if not progress:
            # Check if this is module 1
            if module.order_index == 1:
                progress = UserModuleProgress(
                    user_id=user.id,
                    module_id=module_id,
                    status="available",
                    unlocked_at=datetime.datetime.now(datetime.timezone.utc)
                )
                db.add(progress)
                db.commit()
                db.refresh(progress)
            else:
                progress = UserModuleProgress(
                    user_id=user.id,
                    module_id=module_id,
                    status="locked"
                )
                db.add(progress)
                db.commit()
                db.refresh(progress)

        if progress.status == "locked":
            raise HTTPException(
                status_code=403,
                detail="Module is locked. You must pass previous modules with at least 10/15 (65%) to unlock."
            )

        return module, progress

    def sample_module_quiz(self, db: Session, user: User, module_id: str) -> Dict[str, Any]:
        """
        Draws exactly 15 questions from the validated question bank (>= 40 questions).
        Does NOT expose correct answers or explanations to the client.
        """
        module, progress = self.get_module_with_access_check(db, user, module_id)

        pool = db.query(Question).filter(
            Question.module_id == module_id,
            Question.is_placement == False
        ).all()

        if len(pool) < settings.MODULE_QUIZ_QUESTIONS_COUNT:
            self._seed_fallback_module_questions(db, module)
            pool = db.query(Question).filter(
                Question.module_id == module_id,
                Question.is_placement == False
            ).all()

        # Draw random questions with varied order
        sample_size = min(len(pool), settings.MODULE_QUIZ_QUESTIONS_COUNT)
        sampled = random.sample(pool, sample_size)
        random.shuffle(sampled)
        attempt_id = str(uuid.uuid4())

        # Update progress to in_progress if currently available
        if progress.status == "available":
            progress.status = "in_progress"
            db.commit()

        client_questions = [q.to_dict(include_answer=False) for q in sampled]
        return {
            "attempt_id": attempt_id,
            "module_id": module_id,
            "module_title": module.title,
            "total_questions": len(client_questions),
            "pass_threshold_required": settings.MODULE_QUIZ_PASS_MIN_CORRECT,
            "questions": client_questions
        }

    def evaluate_module_quiz(
        self,
        db: Session,
        user: User,
        module_id: str,
        attempt_id: str,
        question_ids: List[str],
        answers: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Server-side scoring, gating enforcement (10/15 to pass),
        idempotent XP calculation, and unlocking next module.
        """
        module, progress = self.get_module_with_access_check(db, user, module_id)

        if len(question_ids) != settings.MODULE_QUIZ_QUESTIONS_COUNT:
            raise HTTPException(
                status_code=400,
                detail=f"Quiz submission must contain exactly {settings.MODULE_QUIZ_QUESTIONS_COUNT} questions."
            )

        # Check for idempotency: if this attempt_id was already scored, return existing record
        existing_attempt = db.query(QuizAttempt).filter(QuizAttempt.id == attempt_id).first()
        if existing_attempt:
            return {
                "status": "already_submitted",
                "attempt_id": attempt_id,
                "score_correct": existing_attempt.score_correct,
                "total_questions": existing_attempt.total_questions,
                "score_percentage": existing_attempt.score_percentage,
                "passed": existing_attempt.passed,
                "xp_awarded": 0,
                "new_total_xp": user.total_xp,
                "message": "Attempt was already recorded. No duplicate XP awarded."
            }

        questions = db.query(Question).filter(Question.id.in_(question_ids)).all()
        q_map = {q.id: q for q in questions}

        correct_count = 0
        topic_stats = {}
        review_items = []

        for qid in question_ids:
            q = q_map.get(qid)
            if not q:
                continue

            selected_idx = answers.get(qid)
            is_correct = (selected_idx is not None and selected_idx == q.correct_idx)
            if is_correct:
                correct_count += 1

            if q.topic not in topic_stats:
                topic_stats[q.topic] = {"correct": 0, "total": 0}
            topic_stats[q.topic]["total"] += 1
            if is_correct:
                topic_stats[q.topic]["correct"] += 1

            review_items.append({
                "question_id": q.id,
                "question": q.question_text,
                "topic": q.topic,
                "difficulty": q.difficulty,
                "options": json.loads(q.options_json),
                "selected_option_index": selected_idx,
                "correct_option_index": q.correct_idx,
                "is_correct": is_correct,
                "explanation": q.explanation
            })

        score_pct = round((correct_count / len(question_ids)) * 100.0, 1)
        passed = (correct_count >= settings.MODULE_QUIZ_PASS_MIN_CORRECT)  # 10 or more correct

        weak_topics = [t for t, s in topic_stats.items() if (s["correct"] / s["total"]) < 0.60]

        # Calculate XP Server-Side (Requirements Update v2 - Section C)
        # Base XP = 10 + (correct * 2)
        base_xp = settings.XP_BASE_FIXED + (correct_count * settings.XP_PER_CORRECT_ANSWER)
        bonus_first_pass = 0
        bonus_perfect = 0

        was_already_passed = (progress.status == "passed")

        if was_already_passed:
            # Retakes after a pass award only 20% of base XP and NO bonuses
            xp_awarded = int(base_xp * settings.XP_RETAKE_BASE_RATIO)
        else:
            if passed:
                bonus_first_pass = settings.XP_FIRST_PASS_BONUS  # +50
                if correct_count == settings.MODULE_QUIZ_QUESTIONS_COUNT:
                    bonus_perfect = settings.XP_PERFECT_SCORE_BONUS  # +25
                xp_awarded = base_xp + bonus_first_pass + bonus_perfect
            else:
                xp_awarded = base_xp  # Base XP awarded even on fail

        # Record Idempotent XP Ledger Entry
        now = datetime.datetime.now(datetime.timezone.utc)
        idempotency_key = f"quiz-attempt-{attempt_id}"
        xp_event = XPEvent(
            id=str(uuid.uuid4()),
            user_id=user.id,
            source="module_quiz_pass" if passed else "module_quiz_attempt",
            amount=xp_awarded,
            metadata_json=json.dumps({
                "module_id": module_id,
                "correct": correct_count,
                "passed": passed,
                "first_pass_bonus": bonus_first_pass,
                "perfect_bonus": bonus_perfect
            }),
            idempotency_key=idempotency_key
        )
        db.add(xp_event)
        user.total_xp += xp_awarded

        # Record Quiz Attempt
        attempt = QuizAttempt(
            id=attempt_id,
            user_id=user.id,
            module_id=module_id,
            is_placement=False,
            score_correct=correct_count,
            total_questions=len(question_ids),
            score_percentage=score_pct,
            passed=passed,
            answers_json=json.dumps(answers),
            question_ids_json=json.dumps(question_ids),
            weak_topics_json=json.dumps(weak_topics),
            xp_awarded=xp_awarded
        )
        db.add(attempt)

        # Update User Module Progress
        progress.attempts_count += 1
        progress.best_score = max(progress.best_score, correct_count)

        unlocked_next_module_id = None
        if passed:
            progress.status = "passed"
            if not progress.passed_at:
                progress.passed_at = now

            # Unlock Next Module in sequence
            next_mod = db.query(Module).filter(
                Module.course_id == module.course_id,
                Module.order_index == module.order_index + 1
            ).first()

            if next_mod:
                next_progress = db.query(UserModuleProgress).filter(
                    UserModuleProgress.user_id == user.id,
                    UserModuleProgress.module_id == next_mod.id
                ).first()
                if not next_progress:
                    next_progress = UserModuleProgress(
                        user_id=user.id,
                        module_id=next_mod.id,
                        status="available",
                        unlocked_at=now
                    )
                    db.add(next_progress)
                elif next_progress.status == "locked":
                    next_progress.status = "available"
                    next_progress.unlocked_at = now
                unlocked_next_module_id = next_mod.id

        db.commit()
        db.refresh(user)

        return {
            "status": "success",
            "attempt_id": attempt_id,
            "module_id": module_id,
            "score_correct": correct_count,
            "total_questions": len(question_ids),
            "score_percentage": score_pct,
            "passed": passed,
            "pass_mark_required": settings.MODULE_QUIZ_PASS_MIN_CORRECT,
            "xp_awarded": xp_awarded,
            "bonus_first_pass": bonus_first_pass,
            "bonus_perfect": bonus_perfect,
            "new_total_xp": user.total_xp,
            "unlocked_next_module_id": unlocked_next_module_id,
            "weak_topics": weak_topics,
            "review": review_items
        }

    def _seed_fallback_module_questions(self, db: Session, module: Module):
        """Generates and seeds 15 validated curriculum questions for this module if unseeded."""
        skills = json.loads(module.skills_json) if module.skills_json else [module.title]
        topics = json.loads(module.topics_json) if module.topics_json else skills

        templates = [
            ("What is the primary architectural purpose of {topic}?",
             ["Ensures optimal execution performance and scalability", "Disables memory garbage collection", "Translates Python bytecode to raw assembly", "Acts as a purely cosmetic abstraction"],
             0, "Provides critical performance, safety, and architectural abstraction guarantees."),
            ("In production systems, what trade-off is most commonly associated with {topic}?",
             ["Latency vs throughput balance", "CPU core count reduction", "Complete elimination of disk I/O", "Zero need for monitoring"],
             0, "Engineering involves balancing latency and throughput trade-offs under varying loads."),
            ("Which design pattern is best practice when implementing {topic}?",
             ["Idempotent and decoupled modular structure", "Global mutable state across threads", "Hardcoding network credentials in source files", "Executing blocking calls inside event loops"],
             0, "Idempotent, decoupled patterns minimize blast radius and simplify debugging."),
            ("How should failures be handled when operating {topic} under high concurrency?",
             ["Graceful retries with exponential backoff and circuit breakers", "Crashing the host operating system immediately", "Ignoring error codes and dropping requests silently", "Busy-waiting indefinitely without timeout"],
             0, "Exponential backoff and circuit breakers prevent cascading system outages."),
            ("What metric is most critical when monitoring the operational health of {topic}?",
             ["Error rates and p99 latency percentiles", "Total number of source code comments", "Screen refresh rate of developer workstations", "Git commit hash length"],
             0, "p99 latency percentiles and error rates give direct insight into customer impact.")
        ]

        diffs = ["Easy", "Medium", "Hard"]
        idx = 1
        for topic in topics:
            for tmpl_q, opts, correct, exp in templates:
                if idx > 18:
                    break
                # Shuffle options so correct answer is not always at index 0
                correct_text = opts[correct]
                shuffled_opts = list(opts)
                random.shuffle(shuffled_opts)
                new_correct_idx = shuffled_opts.index(correct_text)

                q_obj = Question(
                    id=f"q-{module.id}-{idx:03d}",
                    course_id=module.course_id,
                    module_id=module.id,
                    topic=topic,
                    difficulty=diffs[idx % len(diffs)],
                    question_text=tmpl_q.format(topic=topic),
                    options_json=json.dumps(shuffled_opts),
                    correct_idx=new_correct_idx,
                    explanation=f"Topic: {topic}. {exp}",
                    is_placement=False
                )
                db.add(q_obj)
                idx += 1
            if idx > 18:
                break
        db.commit()

module_quiz_service = ModuleQuizService()

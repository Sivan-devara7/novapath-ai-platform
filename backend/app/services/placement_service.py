import json
import uuid
import datetime
from typing import Dict, Any, List, Optional, Tuple
from sqlalchemy.orm import Session
from ..config import settings
from ..models.db_models import User, Question, QuizAttempt, UserModuleProgress, XPEvent, Module
from ..services.llm_service import llm_service

class PlacementService:
    DIFFICULTY_WEIGHTS = {
        "Easy": 1.0,
        "Medium": 2.0,
        "Hard": 3.0,
        "Expert": 4.0
    }

    MODULE_TOPIC_MAP = {
        "Python Foundations": "py-foundations",
        "Mathematics for AI": "math-ml",
        "Machine Learning": "classical-ml",
        "Deep Learning": "deep-learning",
        "RAG Systems": "rag-systems",
        "MLOps & Systems": "mlops-deploy"
    }

    def can_take_placement(self, user: User) -> Tuple[bool, Optional[str]]:
        """Checks 7-day retake cooldown."""
        if not user.placement_taken_at:
            return True, None
        
        now = datetime.datetime.now(datetime.timezone.utc)
        taken_at = user.placement_taken_at
        if taken_at.tzinfo is None:
            taken_at = taken_at.replace(tzinfo=datetime.timezone.utc)

        elapsed = now - taken_at
        cooldown_delta = datetime.timedelta(days=settings.PLACEMENT_RETAKE_COOLDOWN_DAYS)
        if elapsed < cooldown_delta:
            remaining = cooldown_delta - elapsed
            days_left = remaining.days
            hours_left = remaining.seconds // 3600
            return False, f"Placement quiz on cooldown. You can retake in {days_left}d {hours_left}h."
        
        return True, None

    def sample_placement_questions(self, db: Session, count: int = 20) -> List[Question]:
        """Samples balanced adaptive set of placement questions."""
        pool = db.query(Question).filter(Question.is_placement == True).all()
        if len(pool) < count:
            raise ValueError(f"Insufficient placement questions: found {len(pool)}, required {count}")

        # Partition by difficulty to ensure balanced adaptive coverage
        by_diff = {"Easy": [], "Medium": [], "Hard": [], "Expert": []}
        for q in pool:
            by_diff.get(q.difficulty, by_diff["Medium"]).append(q)

        import random
        # Target: 6 Easy, 8 Medium, 6 Hard
        selected = []
        selected.extend(random.sample(by_diff["Easy"], min(6, len(by_diff["Easy"]))))
        selected.extend(random.sample(by_diff["Medium"], min(8, len(by_diff["Medium"]))))
        remaining_needed = count - len(selected)
        hard_pool = by_diff["Hard"] + by_diff["Expert"]
        selected.extend(random.sample(hard_pool, min(remaining_needed, len(hard_pool))))

        # If still short, backfill from remaining
        if len(selected) < count:
            remaining_pool = [q for q in pool if q not in selected]
            selected.extend(random.sample(remaining_pool, count - len(selected)))

        random.shuffle(selected)
        return selected[:count]

    def compute_placement_result(
        self,
        questions: List[Question],
        user_answers: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Deterministically evaluates answers, computing weighted difficulty score,
        level rank, topic breakdown, and weak areas.
        """
        total_weight = 0.0
        earned_weight = 0.0
        correct_count = 0

        topic_stats = {}  # topic -> {"correct": int, "total": int}
        review_items = []

        for q in questions:
            weight = self.DIFFICULTY_WEIGHTS.get(q.difficulty, 2.0)
            total_weight += weight
            selected_idx = user_answers.get(q.id)
            is_correct = (selected_idx is not None and selected_idx == q.correct_idx)

            if is_correct:
                earned_weight += weight
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

        score_ratio = earned_weight / total_weight if total_weight > 0 else 0.0
        score_percentage = round(score_ratio * 100.0, 1)

        # Deterministic level thresholds from config
        if score_ratio < 0.40:  # < 40%
            level = "Beginner"
        elif score_ratio < 0.75:  # 40% - 74%
            level = "Intermediate"
        else:  # >= 75%
            level = "Advanced"

        topic_breakdown = {}
        weak_topics = []
        for topic, stats in topic_stats.items():
            pct = round((stats["correct"] / stats["total"]) * 100.0, 1) if stats["total"] > 0 else 0.0
            topic_breakdown[topic] = {
                "correct": stats["correct"],
                "total": stats["total"],
                "percentage": pct
            }
            if pct < 60.0:
                weak_topics.append(topic)

        return {
            "level": level,
            "score_percentage": score_percentage,
            "correct_count": correct_count,
            "total_questions": len(questions),
            "topic_breakdown": topic_breakdown,
            "weak_topics": weak_topics,
            "review": review_items
        }

    async def generate_explanation(
        self,
        level: str,
        score_pct: float,
        topic_breakdown: Dict[str, Any],
        weak_topics: List[str]
    ) -> str:
        """
        Uses LLM to author a concise 2-3 sentence personalized evaluation of the placement result.
        Gracefully falls back if AI service is offline.
        """
        prompt = (
            f"A student took an AI Engineering placement quiz.\n"
            f"Result: Level = {level}, Weighted Score = {score_pct}%.\n"
            f"Topic Performance: {json.dumps(topic_breakdown)}\n"
            f"Weak Topics: {', '.join(weak_topics) if weak_topics else 'None'}\n"
            f"In 2-3 sentences, provide an encouraging, technically specific academic evaluation "
            f"explaining where their baseline is strongest and what their immediate roadmap focus should be."
        )
        fallback = (
            f"You have been ranked at the {level} tier with a {score_pct}% weighted score. "
            f"Your foundational concepts are well established. "
            f"{'We recommend strengthening ' + ', '.join(weak_topics[:2]) + ' as you proceed through your customized curriculum.' if weak_topics else 'You are primed to tackle advanced topics on your roadmap.'}"
        )
        return await llm_service.chat(
            messages=[{"role": "user", "content": prompt}],
            fallback=fallback,
            temperature=0.3,
            max_tokens=200
        )

    def apply_placement_unlocks(
        self,
        db: Session,
        user: User,
        level: str,
        topic_breakdown: Dict[str, Any]
    ) -> None:
        """
        Server-side roadmap module unlocking based on placement tier:
        - Beginner: Module 1 available, rest locked.
        - Intermediate: Unlocks modules student demonstrably passed topics for; skipped modules marked 'passed' (Validated by placement).
        - Advanced: Skips foundations (Modules 1, 2, 3 marked 'passed'), Module 4 available, rest locked.
        """
        modules = db.query(Module).filter(Module.course_id == "ai-engineer").order_by(Module.order_index).all()
        now = datetime.datetime.now(datetime.timezone.utc)

        for mod in modules:
            progress = db.query(UserModuleProgress).filter(
                UserModuleProgress.user_id == user.id,
                UserModuleProgress.module_id == mod.id
            ).first()
            if not progress:
                progress = UserModuleProgress(user_id=user.id, module_id=mod.id)
                db.add(progress)

            if level == "Beginner":
                if mod.order_index == 1:
                    progress.status = "available"
                    progress.unlocked_at = now
                else:
                    progress.status = "locked"

            elif level == "Intermediate":
                # Check topic for this module
                topic_for_mod = None
                for top_name, m_id in self.MODULE_TOPIC_MAP.items():
                    if m_id == mod.id:
                        topic_for_mod = top_name
                        break

                passed_topic = False
                if topic_for_mod and topic_for_mod in topic_breakdown:
                    passed_topic = topic_breakdown[topic_for_mod]["percentage"] >= 60.0

                if mod.order_index <= 2 and passed_topic:
                    progress.status = "passed"
                    progress.best_score = 15
                    progress.passed_at = now
                elif mod.order_index == 1 or (mod.order_index == 3 and passed_topic):
                    progress.status = "available"
                    progress.unlocked_at = now
                elif mod.order_index == 2 and not passed_topic:
                    progress.status = "available"
                    progress.unlocked_at = now
                else:
                    progress.status = "locked"

            elif level == "Advanced":
                # Advanced skips foundations (modules 1, 2, 3)
                if mod.order_index in [1, 2, 3]:
                    progress.status = "passed"
                    progress.best_score = 15
                    progress.passed_at = now
                elif mod.order_index == 4:
                    progress.status = "available"
                    progress.unlocked_at = now
                else:
                    progress.status = "locked"

placement_service = PlacementService()

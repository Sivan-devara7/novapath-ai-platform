import datetime
import uuid
import json
from typing import List, Dict, Any, Optional
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship

def now_utc():
    return datetime.datetime.now(datetime.timezone.utc)

Base = declarative_base()

def generate_uuid() -> str:
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, index=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    role = Column(String(32), default="student", nullable=False)
    avatar = Column(String(512), default="")
    career_goal = Column(String(128), default="AI Engineer", nullable=False)
    
    # Placement Quiz State (v2 Section A)
    placement_level = Column(String(32), nullable=True)  # Beginner | Intermediate | Advanced
    placement_score = Column(Float, nullable=True)       # Weighted % 0-100
    placement_taken_at = Column(DateTime, nullable=True)

    # Gamification & XP State (v2 Section C)
    total_xp = Column(Integer, default=0, nullable=False)
    streak = Column(Integer, default=1, nullable=False)
    mastery_overall = Column(Integer, default=0, nullable=False)
    radar_data_json = Column(Text, default="[]", nullable=False)
    verified_skills_json = Column(Text, default="[]", nullable=False)

    created_at = Column(DateTime, default=now_utc, nullable=False)
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc, nullable=False)

    # Relationships
    xp_events = relationship("XPEvent", back_populates="user", cascade="all, delete-orphan")
    module_progress = relationship("UserModuleProgress", back_populates="user", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    resume_analyses = relationship("ResumeAnalysis", back_populates="user", cascade="all, delete-orphan")

    def to_profile_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "career_goal": self.career_goal,
            "avatar": self.avatar,
            "placement_level": self.placement_level,
            "placement_score": self.placement_score,
            "placement_taken_at": self.placement_taken_at.isoformat() if self.placement_taken_at else None,
            "streak": self.streak,
            "points": self.total_xp,
            "total_xp": self.total_xp,
            "mastery_overall": self.mastery_overall,
            "radar_data": json.loads(self.radar_data_json) if self.radar_data_json else [],
            "verified_skills": json.loads(self.verified_skills_json) if self.verified_skills_json else []
        }

class XPEvent(Base):
    """
    Idempotent XP Event Ledger (v2 Section C).
    Every XP change is an immutable ledger entry.
    """
    __tablename__ = "xp_events"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    user_id = Column(String(64), ForeignKey("users.id"), index=True, nullable=False)
    source = Column(String(64), index=True, nullable=False)  # e.g., 'placement_quiz', 'module_first_pass', 'module_retake'
    amount = Column(Integer, nullable=False)
    metadata_json = Column(Text, default="{}", nullable=False)
    idempotency_key = Column(String(128), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=now_utc, nullable=False)

    user = relationship("User", back_populates="xp_events")

class Course(Base):
    __tablename__ = "courses"

    id = Column(String(64), primary_key=True)  # e.g., 'ai-engineer'
    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)
    target_role = Column(String(128), nullable=False)

    modules = relationship("Module", back_populates="course", order_by="Module.order_index")

class Module(Base):
    __tablename__ = "modules"

    id = Column(String(64), primary_key=True)  # e.g., 'py-foundations'
    course_id = Column(String(64), ForeignKey("courses.id"), index=True, nullable=False)
    order_index = Column(Integer, index=True, nullable=False)
    title = Column(String(128), nullable=False)
    summary = Column(Text, nullable=False)
    estimated_hours = Column(Integer, default=10, nullable=False)
    lessons_count = Column(Integer, default=4, nullable=False)
    skills_json = Column(Text, default="[]", nullable=False)
    difficulty = Column(String(32), default="Beginner", nullable=False)  # Beginner | Intermediate | Advanced
    topics_json = Column(Text, default="[]", nullable=False)
    learning_objectives_json = Column(Text, default="[]", nullable=False)

    course = relationship("Course", back_populates="modules")
    questions = relationship("Question", back_populates="module")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "course_id": self.course_id,
            "order_index": self.order_index,
            "title": self.title,
            "summary": self.summary,
            "estimated_hours": self.estimated_hours,
            "lessons_count": self.lessons_count,
            "skills": json.loads(self.skills_json) if self.skills_json else [],
            "difficulty": self.difficulty,
            "topics": json.loads(self.topics_json) if self.topics_json else [],
            "learning_objectives": json.loads(self.learning_objectives_json) if self.learning_objectives_json else []
        }

class UserModuleProgress(Base):
    """
    Tracks server-side gating state per user per module (v2 Section B).
    States: 'locked', 'available', 'in_progress', 'passed'
    """
    __tablename__ = "user_module_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "module_id", name="uq_user_module"),
    )

    id = Column(String(64), primary_key=True, default=generate_uuid)
    user_id = Column(String(64), ForeignKey("users.id"), index=True, nullable=False)
    module_id = Column(String(64), ForeignKey("modules.id"), index=True, nullable=False)
    status = Column(String(32), default="locked", index=True, nullable=False)  # locked | available | in_progress | passed
    best_score = Column(Integer, default=0, nullable=False)  # Out of 15
    attempts_count = Column(Integer, default=0, nullable=False)
    unlocked_at = Column(DateTime, nullable=True)
    passed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=now_utc, onupdate=now_utc, nullable=False)

    user = relationship("User", back_populates="module_progress")
    module = relationship("Module")

class Question(Base):
    """
    Validated Question Bank (v2 Section A & B).
    Placement questions: is_placement=True.
    Module questions: is_placement=False, tied to module_id.
    """
    __tablename__ = "questions"

    id = Column(String(64), primary_key=True)
    course_id = Column(String(64), index=True, nullable=False)
    module_id = Column(String(64), ForeignKey("modules.id"), index=True, nullable=True)
    topic = Column(String(64), index=True, nullable=False)
    difficulty = Column(String(32), index=True, nullable=False)  # Easy | Medium | Hard | Expert
    question_text = Column(Text, nullable=False)
    options_json = Column(Text, nullable=False)  # JSON list of exactly 4 strings
    correct_idx = Column(Integer, nullable=False)  # 0, 1, 2, or 3
    explanation = Column(Text, nullable=False)
    is_placement = Column(Boolean, default=False, index=True, nullable=False)

    module = relationship("Module", back_populates="questions")

    def to_dict(self, include_answer: bool = False) -> Dict[str, Any]:
        data = {
            "id": self.id,
            "course_id": self.course_id,
            "module_id": self.module_id,
            "topic": self.topic,
            "difficulty": self.difficulty,
            "question": self.question_text,
            "options": json.loads(self.options_json),
            "is_placement": self.is_placement
        }
        if include_answer:
            data["correct_idx"] = self.correct_idx
            data["explanation"] = self.explanation
        return data

class QuizAttempt(Base):
    """
    Records every quiz attempt server-side (v2 Section B).
    """
    __tablename__ = "quiz_attempts"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    user_id = Column(String(64), ForeignKey("users.id"), index=True, nullable=False)
    module_id = Column(String(64), ForeignKey("modules.id"), index=True, nullable=True)
    is_placement = Column(Boolean, default=False, index=True, nullable=False)
    score_correct = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    score_percentage = Column(Float, nullable=False)
    passed = Column(Boolean, nullable=False)
    answers_json = Column(Text, nullable=False)         # Map of question_id -> selected_idx
    question_ids_json = Column(Text, nullable=False)    # Sampled question order
    weak_topics_json = Column(Text, default="[]", nullable=False)
    xp_awarded = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=now_utc, nullable=False)

    user = relationship("User", back_populates="quiz_attempts")
    module = relationship("Module")

class ResumeAnalysis(Base):
    """
    Persistent ML ATS Analysis Record (v2 Section E).
    """
    __tablename__ = "resume_analyses"

    id = Column(String(64), primary_key=True, default=generate_uuid)
    user_id = Column(String(64), ForeignKey("users.id"), index=True, nullable=False)
    target_role = Column(String(128), nullable=False)
    overall_ats_score = Column(Integer, nullable=False)  # 0-100 weighted
    role_fit_score = Column(Float, nullable=False)       # 0-100 (40% weight)
    keyword_score = Column(Float, nullable=False)        # 0-100 (25% weight)
    section_score = Column(Float, nullable=False)        # 0-100 (15% weight)
    format_score = Column(Float, nullable=False)         # 0-100 (10% weight)
    impact_score = Column(Float, nullable=False)         # 0-100 (10% weight)
    extracted_skills_json = Column(Text, default="[]", nullable=False)
    missing_skills_json = Column(Text, default="[]", nullable=False)
    deductions_json = Column(Text, default="[]", nullable=False)
    top_features_json = Column(Text, default="[]", nullable=False)
    raw_text_hash = Column(String(64), index=True, nullable=False)
    created_at = Column(DateTime, default=now_utc, nullable=False)

    user = relationship("User", back_populates="resume_analyses")

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class UserBase(BaseModel):
    name: str
    email: str
    career_goal: str = "AI Engineer"

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class GoogleLoginRequest(BaseModel):
    credential: Optional[str] = None
    email: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None
    google_id: Optional[str] = None
    career_goal: Optional[str] = "AI Engineer"

class UserProfile(UserBase):
    id: str
    role: str = "student"
    avatar: str = ""
    streak: int = 5
    points: int = 420
    mastery_overall: int = 68
    radar_data: List[Dict[str, Any]] = []
    verified_skills: List[str] = []

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserProfile

class SkillNode(BaseModel):
    id: str
    name: str
    category: str
    prerequisites: List[str] = []
    mastery_level: int = 0  # 0 to 100
    status: str = "locked"  # "completed", "in_progress", "ready", "locked"
    verified_via: Optional[str] = None
    icon: Optional[str] = None
    estimated_hours: int = 15
    milestone_project: Optional[str] = None

class SkillGraphResponse(BaseModel):
    nodes: List[SkillNode]
    edges: List[Dict[str, str]]
    career_goal: str
    completion_rate: int

class ResourceItem(BaseModel):
    id: str
    skill_id: str
    title: str
    type: str  # "video", "doc", "course", "paper", "interactive"
    url: str
    provider: str
    estimated_time: str
    difficulty: str  # "Beginner", "Intermediate", "Advanced"
    summary: str
    grounding_reason: str
    rating: float = 4.8
    match_score: int = 95

class AssessmentQuestion(BaseModel):
    id: str
    skill_id: str
    question: str
    code_snippet: Optional[str] = None
    options: List[str]
    difficulty: str  # "Easy", "Medium", "Hard", "Expert"
    type: str = "multiple_choice"
    hint: Optional[str] = None

class AssessmentAnswerSubmission(BaseModel):
    question_id: str
    selected_option_index: int
    time_taken_seconds: int = 30

class AssessmentFeedback(BaseModel):
    is_correct: bool
    correct_option_index: int
    explanation: str
    grounded_source: str
    new_difficulty: str
    points_earned: int
    current_score: int

class ResumeAnalysisResponse(BaseModel):
    ats_score: int
    formatting_score: int
    skills_match_score: int
    impact_score: int
    role_fit_score: Optional[float] = 0.0
    section_score: Optional[float] = 0.0
    extracted_skills: List[str]
    missing_skills: List[str]
    matched_skills: List[str]
    action_verb_count: int
    quantifiable_metrics_count: int
    summary_critique: str
    actionable_recommendations: List[Dict[str, str]]
    score_breakdown: Optional[Dict[str, Any]] = None
    top_contributing_features: Optional[List[Dict[str, Any]]] = None
    deductions: Optional[List[Dict[str, Any]]] = None
    bullet_improvements: Optional[List[Dict[str, str]]] = None
    target_role: Optional[str] = "AI Engineer"
    raw_text_hash: Optional[str] = None

class RecommendationItem(BaseModel):
    id: str
    type: str  # "project", "certification", "internship"
    title: str
    organization: str
    difficulty: str
    duration: str
    match_percentage: int
    why_this_matches: str
    prerequisites: List[str] = []
    tags: List[str] = []
    action_url: str = "#"

class LessonContent(BaseModel):
    title: str
    level_badge: str
    estimated_read_time: str
    analogy: str
    core_explanation: str
    code_example: Optional[str] = None
    common_mistakes: List[str] = []
    practice_exercise: str
    practice_solution: str
    ai_tutor_tip: str

class GenerateLessonRequest(BaseModel):
    topic_index: int = 0
    topic_name: str
    level: str = "scratch"  # "scratch", "intermediate", "advanced"

class BridgeMilestone(BaseModel):
    step: int
    title: str
    target_skill: str
    description: str
    estimated_hours: int
    project: str

class BridgeRoadmapResponse(BaseModel):
    target_role: str
    current_ats_score: int
    projected_ats_score: int
    estimated_weeks: str
    summary: str
    milestones: List[BridgeMilestone]

class GenerateBridgeRoadmapRequest(BaseModel):
    target_role: str
    current_ats_score: int
    missing_skills: List[str]
    matched_skills: List[str]

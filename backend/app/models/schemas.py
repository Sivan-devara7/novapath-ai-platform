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
    role_fit_score: Optional[float] = 0.0  # Maintained for backwards compatibility
    role_alignment_score: Optional[float] = 0.0  # Calibrated alignment index (not a probability)
    role_alignment_note: Optional[str] = "Calibrated alignment index measuring textual congruence with role benchmarks, not a raw Bayesian posterior probability."
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
    missing_critical_skills: Optional[List[str]] = None
    missing_bonus_skills: Optional[List[str]] = None
    personalized_roadmap: Optional[List[Dict[str, Any]]] = None
    target_role: Optional[str] = "AI Engineer"
    raw_text_hash: Optional[str] = None
    limited_validation: bool = False
    validation_notes: Optional[str] = None
    detected_seniority: Optional[str] = "mid"

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

class JDMatchRequest(BaseModel):
    resume_text: str
    jd_text: str

class KeywordGapPlacement(BaseModel):
    keyword: str
    importance: str  # "Must-Have" or "Nice-to-Have"
    recommended_section: str
    placement_tip: str

class ResumeEditSuggestion(BaseModel):
    priority: str  # "High", "Medium", "Low"
    category: str
    action: str
    before_example: Optional[str] = None
    after_example: Optional[str] = None

class JDMatchResponse(BaseModel):
    jd_match_score: int  # 0 to 100
    semantic_similarity_score: float
    must_have_score: float
    nice_to_have_score: float
    matched_must_haves: List[str]
    missing_must_haves: List[str]
    matched_nice_to_haves: List[str]
    missing_nice_to_haves: List[str]
    required_years_experience: Optional[int] = None
    candidate_years_experience: Optional[int] = None
    experience_status: str
    required_education: Optional[str] = None
    candidate_education: Optional[str] = None
    education_status: str
    keyword_gaps_with_placement: List[KeywordGapPlacement]
    actionable_resume_edits: List[ResumeEditSuggestion]
    scoring_formula_weights: Dict[str, Any]
    summary: str
    matched_skills: Optional[List[str]] = None

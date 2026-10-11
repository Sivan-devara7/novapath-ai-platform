export interface UserProfile {
  id: string;
  name: string;
  email: string;
  role: string;
  career_goal: string;
  avatar: string;
  streak: number;
  points: number;
  mastery_overall: number;
  placement_level?: string;
  radar_data: Array<{ subject: string; A: number; fullMark: number }>;
  verified_skills: string[];
}

export interface SkillNode {
  id: string;
  name: string;
  category: string;
  prerequisites: string[];
  mastery_level: number;
  status: 'completed' | 'in_progress' | 'ready' | 'locked';
  verified_via?: string | null;
  icon?: string | null;
  estimated_hours: number;
  milestone_project?: string | null;
}

export interface SkillGraphResponse {
  nodes: SkillNode[];
  edges: Array<{ source: string; target: string }>;
  career_goal: string;
  completion_rate: number;
}

export interface ResourceItem {
  id: string;
  skill_id: string;
  title: string;
  type: 'video' | 'doc' | 'course' | 'paper' | 'interactive';
  url: string;
  provider: string;
  estimated_time: string;
  difficulty: string;
  summary: string;
  grounding_reason: string;
  rating: number;
  match_score: number;
}

export interface AssessmentQuestion {
  id: string;
  skill_id: string;
  question: string;
  code_snippet?: string | null;
  options: string[];
  difficulty: 'Easy' | 'Medium' | 'Hard' | 'Expert';
  type: string;
  hint?: string | null;
}

export interface AssessmentFeedback {
  is_correct: boolean;
  correct_option_index: number;
  explanation: string;
  grounded_source: string;
  new_difficulty: 'Easy' | 'Medium' | 'Hard' | 'Expert';
  points_earned: number;
  current_score: number;
}

export interface ActionableRecommendation {
  category: string;
  priority: string;
  title: string;
  description: string;
}

export interface ScoreBreakdownItem {
  name: string;
  score: number;
  weight_percent: number;
  weighted_points: number;
  description: string;
}

export interface DeductionItem {
  category: string;
  lost_points: number;
  reason: string;
}

export interface ContributingFeature {
  feature: string;
  weight: number;
}

export interface ResumeAnalysisResponse {
  ats_score: number;
  formatting_score: number;
  skills_match_score: number;
  impact_score: number;
  role_fit_score?: number;
  section_score?: number;
  extracted_skills: string[];
  missing_skills: string[];
  matched_skills: string[];
  action_verb_count: number;
  quantifiable_metrics_count: number;
  summary_critique: string;
  actionable_recommendations: ActionableRecommendation[];
  score_breakdown?: {
    role_fit: ScoreBreakdownItem;
    keyword_coverage: ScoreBreakdownItem;
    section_completeness: ScoreBreakdownItem;
    formatting_parsability: ScoreBreakdownItem;
    quantified_impact: ScoreBreakdownItem;
  };
  top_contributing_features?: ContributingFeature[];
  deductions?: DeductionItem[];
  bullet_improvements?: Array<{ original: string; improved: string; reason: string }>;
  target_role?: string;
  raw_text_hash?: string;
}

export interface RecommendationItem {
  id: string;
  type: 'project' | 'certification' | 'internship';
  title: string;
  organization: string;
  difficulty: string;
  duration: string;
  match_percentage: number;
  why_this_matches: string;
  prerequisites: string[];
  tags: string[];
  action_url: string;
}

export interface CourseModule {
  id: string;
  course_id: string;
  order_index: number;
  title: string;
  summary: string;
  estimated_hours: number;
  lessons_count: number;
  skills: string[];
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  topics: string[];
  learning_objectives: string[];
  status: 'locked' | 'available' | 'in_progress' | 'passed';
  best_score: number;
  is_gap_targeted?: boolean;
  targeted_gaps?: string[];
  custom_recommendation?: string | null;
  attempts_count?: number;
  resources?: ResourceItem[];
  latest_attempt?: {
    id: string;
    score_correct: number;
    total_questions: number;
    passed: boolean;
    created_at: string;
  } | null;
}

export interface QuizQuestionItem {
  id: string;
  course_id: string;
  module_id: string | null;
  topic: string;
  difficulty: string;
  question: string;
  options: string[];
}

export interface QuizSubmissionReviewItem {
  question_id: string;
  question: string;
  topic: string;
  difficulty: string;
  options: string[];
  selected_option_index: number | null;
  correct_option_index: number;
  is_correct: boolean;
  explanation: string;
}

export interface QuizSubmissionResponse {
  status: string;
  attempt_id: string;
  module_id?: string;
  level?: string;
  score_correct: number;
  total_questions: number;
  score_percentage: number;
  passed: boolean;
  pass_mark_required?: number;
  xp_awarded: number;
  bonus_first_pass?: number;
  bonus_perfect?: number;
  new_total_xp: number;
  unlocked_next_module_id?: string | null;
  topic_breakdown?: Record<string, { correct: number; total: number; percentage: number }>;
  weak_topics: string[];
  explanation?: string;
  review: QuizSubmissionReviewItem[];
}

export interface LessonContent {
  title: string;
  level_badge: string;
  estimated_read_time: string;
  analogy: string;
  core_explanation: string;
  code_example?: string;
  common_mistakes: string[];
  practice_exercise: string;
  practice_solution: string;
  ai_tutor_tip: string;
}

export interface BridgeMilestone {
  step: number;
  title: string;
  target_skill?: string;
  skill?: string;
  description?: string;
  objective?: string;
  estimated_hours?: number;
  duration_weeks?: number;
  project?: string;
  project_task?: string;
}

export interface BridgeRoadmapResponse {
  target_role: string;
  current_ats_score?: number;
  projected_ats_score: number;
  estimated_weeks: string | number;
  summary?: string;
  executive_strategy?: string;
  milestones: BridgeMilestone[];
}

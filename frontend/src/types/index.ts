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

export interface ResumeAnalysisResponse {
  ats_score: number;
  formatting_score: number;
  skills_match_score: number;
  impact_score: number;
  extracted_skills: string[];
  missing_skills: string[];
  matched_skills: string[];
  action_verb_count: number;
  quantifiable_metrics_count: number;
  summary_critique: string;
  actionable_recommendations: ActionableRecommendation[];
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

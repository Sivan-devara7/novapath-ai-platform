import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import confetti from 'canvas-confetti';
import {
  Map,
  CheckCircle2,
  Clock,
  Sparkles,
  Lock,
  ArrowRight,
  BookOpen,
  Award,
  Zap,
  RotateCcw,
  Compass,
  AlertCircle,
  ChevronRight,
  Check
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../services/api';
import { GlassCard } from '../components/ui/GlassCard';
import { Badge } from '../components/ui/Badge';
import { CourseModule, QuizQuestionItem, QuizSubmissionResponse } from '../types';

export const Roadmap: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { user, addPoints } = useAuth();
  const { t } = useLanguage();

  const [modules, setModules] = useState<CourseModule[]>([]);
  const [isLoadingModules, setIsLoadingModules] = useState(true);
  const [activeTab, setActiveTab] = useState<'modules' | 'graph'>('modules');

  // Placement Quiz State
  const [placementStatus, setPlacementStatus] = useState<{
    has_taken_placement: boolean;
    level: string | null;
    score_percentage: number | null;
    can_retake: boolean;
    cooldown_message: string | null;
  } | null>(null);

  const [isPlacementModalOpen, setIsPlacementModalOpen] = useState(false);
  const [placementQuestions, setPlacementQuestions] = useState<QuizQuestionItem[]>([]);
  const [placementAnswers, setPlacementAnswers] = useState<Record<string, number>>({});
  const [placementCurrentIdx, setPlacementCurrentIdx] = useState(0);
  const [isSubmittingPlacement, setIsSubmittingPlacement] = useState(false);
  const [placementResult, setPlacementResult] = useState<QuizSubmissionResponse | null>(null);

  const prefersReducedMotion = typeof window !== 'undefined' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const [selectedCourse, setSelectedCourse] = useState<string>(() => {
    const goal = (user?.career_goal || '').toLowerCase();
    if (goal.includes('data')) return 'data-engineer';
    if (goal.includes('cyber') || goal.includes('security')) return 'cybersecurity';
    return 'ai-engineer';
  });

  const loadData = async (courseId = selectedCourse) => {
    setIsLoadingModules(true);
    try {
      const [modsRes, placeRes] = await Promise.allSettled([
        api.getModules(courseId),
        api.getPlacementStatus()
      ]);
      if (modsRes.status === 'fulfilled') {
        const sorted = (modsRes.value.modules || []).slice().sort((a, b) => (a.order_index || 0) - (b.order_index || 0));
        setModules(sorted);
      }
      if (placeRes.status === 'fulfilled') {
        setPlacementStatus(placeRes.value);
      }
    } catch (err) {
      console.error('Error loading roadmap data:', err);
    } finally {
      setIsLoadingModules(false);
    }
  };

  const handleTrackChange = (courseId: string) => {
    setSelectedCourse(courseId);
    loadData(courseId);
  };

  useEffect(() => {
    loadData();
    if (searchParams.get('placement') === 'true') {
      handleStartPlacement(true);
    }
  }, [searchParams]);

  const handleStartPlacement = async (force = false) => {
    try {
      const data = await api.startPlacementQuiz(force);
      setPlacementQuestions(data.questions);
      setPlacementAnswers({});
      setPlacementCurrentIdx(0);
      setPlacementResult(null);
      setIsPlacementModalOpen(true);
    } catch (err: any) {
      alert(err.message || 'Cannot start placement quiz right now.');
    }
  };

  const handleSubmitPlacement = async () => {
    if (placementQuestions.length === 0) return;
    setIsSubmittingPlacement(true);

    try {
      const res = await api.submitPlacementQuiz({
        question_ids: placementQuestions.map((q) => q.id),
        answers: placementAnswers
      });
      setPlacementResult(res);

      if (res.xp_awarded > 0) {
        addPoints(res.xp_awarded);
      }

      confetti({
        particleCount: 120,
        spread: 90,
        origin: { y: 0.5 }
      });

      // Reload modules to reflect updated unlocked/skipped states
      loadData();
    } catch (err: any) {
      console.error('Failed to submit placement quiz:', err);
    } finally {
      setIsSubmittingPlacement(false);
    }
  };

  const handleModuleClick = (mod: CourseModule) => {
    navigate(`/roadmap/${mod.id}`);
  };

  const passedCount = modules.filter((m) => m.status === 'passed').length;
  const progressPercent = modules.length > 0 ? Math.round((passedCount / modules.length) * 100) : 0;

  return (
    <div className="relative min-h-screen bg-[var(--bg-primary)] pb-20 pt-8 text-[var(--text-primary)] transition-colors duration-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-[var(--border-subtle)] pb-6">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="in_progress">{t('label_omniroute_powered', 'Gated Academic Curriculum')}</Badge>
              <span className="text-xs text-slate-400">Server-Enforced Mastery Progression</span>
            </div>
            <h1 className="mt-2 text-2xl sm:text-4xl font-extrabold text-white">
              {t('roadmap_title', 'Personalized Learning Roadmap')}
            </h1>
            <p className="mt-1 text-xs sm:text-sm text-slate-300">
              {t('roadmap_subtitle', 'Adaptive curriculum tailored to your placement score and missing skill gaps')}
            </p>
          </div>

          {/* Course Track Switcher & View Switcher */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
            {/* Career Track Tabs */}
            <div className="flex items-center gap-1 rounded-xl border border-white/[0.08] bg-slate-900/60 p-1">
              {[
                { id: 'ai-engineer', label: t('roadmap_tab_ai', 'AI Engineer') },
                { id: 'data-engineer', label: t('roadmap_tab_data', 'Data Engineer') },
                { id: 'cybersecurity', label: t('roadmap_tab_cyber', 'Cybersecurity') }
              ].map((trk) => (
                <button
                  key={trk.id}
                  onClick={() => handleTrackChange(trk.id)}
                  className={`rounded-lg px-3 py-1.5 text-xs font-bold transition-all ${
                    selectedCourse === trk.id
                      ? 'bg-gradient-to-r from-sky-500 to-indigo-600 text-white shadow-neon-blue'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {trk.label}
                </button>
              ))}
            </div>

            {/* View Mode Switcher */}
            <div className="flex items-center gap-1 rounded-xl border border-white/[0.08] bg-slate-900/60 p-1">
              <button
                onClick={() => setActiveTab('modules')}
                className={`rounded-lg px-3.5 py-1.5 text-xs font-semibold transition-all ${
                  activeTab === 'modules'
                    ? 'bg-slate-800 text-sky-400 border border-sky-400/20'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Curriculum Modules
              </button>
              <button
                onClick={() => setActiveTab('graph')}
                className={`rounded-lg px-3.5 py-1.5 text-xs font-semibold transition-all ${
                  activeTab === 'graph'
                    ? 'bg-slate-800 text-sky-400 border border-sky-400/20'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                DAG Graph Overview
              </button>
            </div>
          </div>
        </div>

        {/* Section A: Placement Assessment Banner */}
        <div className="mt-6 overflow-hidden rounded-2xl border border-sky-500/30 bg-gradient-to-r from-sky-950/40 via-indigo-950/30 to-purple-950/40 p-5 backdrop-blur-xl">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 shadow-neon-blue">
                <Compass className="h-6 w-6 text-white" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-bold text-white">
                    Track Placement Assessment
                  </h3>
                  {placementStatus?.level && (
                    <span className="rounded-full border border-sky-400/30 bg-sky-500/20 px-2.5 py-0.5 text-[11px] font-extrabold text-sky-300">
                      Tier: {placementStatus.level}
                    </span>
                  )}
                </div>
                <p className="mt-0.5 text-xs text-slate-300">
                  {placementStatus?.has_taken_placement
                    ? `Completed (${placementStatus.score_percentage}% weighted score). Foundations auto-validated by placement. ${placementStatus.can_retake ? 'Retake available.' : placementStatus.cooldown_message || ''}`
                    : 'Take our 20-question adaptive placement quiz to skip known foundations and establish your starting baseline.'}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-2 shrink-0">
              <button
                onClick={() => handleStartPlacement(!placementStatus?.can_retake)}
                className="rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-5 py-2.5 text-xs font-bold text-white shadow-neon-blue transition-all hover:scale-105"
              >
                {placementStatus?.has_taken_placement ? 'Retake Placement Quiz' : 'Start Placement Quiz (20 Qs)'}
              </button>
            </div>
          </div>
        </div>

        {/* Overall Curriculum Progress Bar */}
        <div className="mt-6 flex items-center justify-between rounded-2xl border border-white/[0.06] bg-slate-900/40 p-4 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-400/20">
              <Award className="h-5 w-5" />
            </div>
            <div>
              <span className="text-xs font-bold text-white block">
                Track Completion Status
              </span>
              <span className="text-xs text-slate-400">
                {passedCount} of {modules.length} Modules Cleared
              </span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden sm:block text-right">
              <span className="text-xs text-slate-400 block">Validated Trajectory</span>
              <span className="text-sm font-extrabold text-emerald-400">{progressPercent}%</span>
            </div>
            <div className="h-3 w-32 sm:w-48 overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full rounded-full bg-gradient-to-r from-emerald-400 to-sky-400 transition-all duration-700"
                style={{ width: `${progressPercent}%` }}
              />
            </div>
          </div>
        </div>

        {/* Section D: Ordered Module Cards with Shared Element Transitions */}
        {activeTab === 'modules' ? (
          <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {modules.map((mod) => {
              const isLocked = mod.status === 'locked';
              const isPassed = mod.status === 'passed';
              const isInProgress = mod.status === 'in_progress';

              return (
                <motion.div
                  key={mod.id}
                  onClick={() => handleModuleClick(mod)}
                  whileHover={isLocked ? {} : { y: -4 }}
                  className={`relative flex flex-col justify-between rounded-2xl border p-6 transition-all cursor-pointer backdrop-blur-xl ${
                    isLocked
                      ? 'border-white/[0.04] bg-slate-950/40 opacity-70 cursor-not-allowed'
                      : isPassed
                      ? 'border-emerald-500/30 bg-slate-900/60 shadow-[0_0_20px_rgba(16,185,129,0.1)] hover:border-emerald-400/50'
                      : isInProgress
                      ? 'border-violet-500/40 bg-slate-900/70 shadow-[0_0_25px_rgba(168,85,247,0.15)] ring-1 ring-violet-500/30'
                      : 'border-sky-500/30 bg-slate-900/60 hover:border-sky-400/60 shadow-neon-blue'
                  }`}
                >
                  <div>
                    {/* Top Status & Difficulty Row */}
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <span className="flex h-6 w-6 items-center justify-center rounded-lg bg-slate-800 text-xs font-bold text-sky-400 border border-white/[0.08]">
                          #{mod.order_index}
                        </span>
                        <span className={`text-[11px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${
                          isPassed
                            ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                            : isInProgress
                            ? 'bg-violet-500/20 text-violet-300 border border-violet-500/30 animate-pulse'
                            : isLocked
                            ? 'bg-slate-800 text-slate-400 border border-slate-700'
                            : 'bg-sky-500/20 text-sky-300 border border-sky-400/30'
                        }`}>
                          {isPassed ? 'Passed' : isInProgress ? 'In Progress' : isLocked ? 'Locked' : 'Available'}
                        </span>
                      </div>

                      <span className="text-[11px] font-semibold text-slate-400">
                        {mod.difficulty}
                      </span>
                    </div>

                    {/* Title & 2-3 Line Summary */}
                    {mod.is_gap_targeted && (
                      <div className="mt-2.5 inline-flex items-center gap-1.5 rounded-lg border border-amber-400/40 bg-amber-400/10 px-2.5 py-1 text-[11px] font-bold text-amber-300 shadow-[0_0_12px_rgba(251,191,36,0.15)]">
                        <Sparkles className="h-3 w-3 text-amber-400 animate-pulse" />
                        <span>Prioritized: Bridges Your ATS Gap</span>
                      </div>
                    )}
                    <h3 className="mt-3 text-lg font-bold text-white group-hover:text-sky-300 transition-colors line-clamp-1">
                      {mod.title}
                    </h3>
                    <p className="mt-1.5 text-xs text-slate-300 line-clamp-3 leading-relaxed">
                      {mod.summary}
                    </p>

                    {/* Skills Tags */}
                    <div className="mt-4 flex flex-wrap gap-1.5">
                      {mod.skills.slice(0, 3).map((s) => (
                        <span key={s} className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] font-medium text-slate-300 border border-white/[0.04]">
                          {s}
                        </span>
                      ))}
                      {mod.skills.length > 3 && (
                        <span className="rounded-md bg-slate-800/80 px-1.5 py-0.5 text-[10px] text-slate-400">
                          +{mod.skills.length - 3}
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Footer Metrics Row */}
                  <div className="mt-6 pt-4 border-t border-white/[0.06] flex items-center justify-between text-xs">
                    <div className="flex items-center gap-3 text-slate-400">
                      <span className="flex items-center gap-1">
                        <Clock className="h-3.5 w-3.5 text-sky-400" />
                        {mod.estimated_hours}h
                      </span>
                      <span className="flex items-center gap-1">
                        <BookOpen className="h-3.5 w-3.5 text-indigo-400" />
                        {mod.lessons_count} Lessons
                      </span>
                    </div>

                    <div className="flex items-center gap-1 font-bold">
                      {isLocked ? (
                        <span className="flex items-center gap-1 text-slate-400 text-[11px]">
                          <Lock className="h-3.5 w-3.5 text-rose-400" /> Locked • Req. #{mod.order_index - 1}
                        </span>
                      ) : (
                        <span className="flex items-center gap-1 text-sky-400 group-hover:translate-x-0.5 transition-transform">
                          Quiz: {mod.best_score > 0 ? `${mod.best_score}/15` : 'Start'}
                          <ChevronRight className="h-4 w-4" />
                        </span>
                      )}
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </div>
        ) : (
          /* DAG Graph View Mode */
          <div className="mt-8 space-y-4">
            <div className="relative border-l border-sky-500/20 pl-6 ml-4 space-y-6">
              {modules.map((mod, idx) => (
                <div
                  key={mod.id}
                  onClick={() => handleModuleClick(mod)}
                  className={`relative p-5 rounded-2xl border cursor-pointer transition-all ${
                    mod.status === 'locked'
                      ? 'border-white/[0.05] bg-slate-950/40 opacity-70'
                      : 'border-white/[0.1] bg-slate-900/60 hover:border-sky-400/40'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <span className="flex h-7 w-7 items-center justify-center rounded-full bg-slate-800 text-xs font-bold text-sky-400">
                        {idx + 1}
                      </span>
                      <div>
                        <h4 className="text-sm font-bold text-white">{mod.title}</h4>
                        <span className="text-xs text-slate-400">{mod.difficulty} • {mod.estimated_hours} Hours</span>
                      </div>
                    </div>
                    <Badge variant={mod.status === 'passed' ? 'verified' : mod.status === 'in_progress' ? 'in_progress' : mod.status === 'locked' ? 'locked' : 'ready'}>
                      {mod.status}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Interactive Placement Quiz Modal (20 Questions) */}
      <AnimatePresence>
        {isPlacementModalOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-md p-4 overflow-y-auto">
            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="relative w-full max-w-3xl rounded-3xl border border-sky-500/30 bg-slate-950 p-6 sm:p-8 text-white shadow-2xl my-8"
            >
              {!placementResult ? (
                <div>
                  <div className="flex items-center justify-between border-b border-white/[0.08] pb-4">
                    <div>
                      <span className="text-xs font-bold uppercase tracking-wider text-sky-400">
                        Adaptive Placement Quiz
                      </span>
                      <h3 className="text-lg font-bold text-white">
                        Question {placementCurrentIdx + 1} of {placementQuestions.length}
                      </h3>
                    </div>
                    <button
                      onClick={() => setIsPlacementModalOpen(false)}
                      className="rounded-lg p-1.5 text-slate-400 hover:text-white"
                    >
                      ✕
                    </button>
                  </div>

                  {placementQuestions[placementCurrentIdx] && (
                    <div className="mt-6 space-y-4">
                      <div className="flex items-center gap-2 text-xs text-slate-400">
                        <span className="rounded bg-slate-800 px-2 py-0.5">
                          {placementQuestions[placementCurrentIdx].topic}
                        </span>
                        <span>• {placementQuestions[placementCurrentIdx].difficulty}</span>
                      </div>

                      <h4 className="text-base font-semibold text-white">
                        {placementQuestions[placementCurrentIdx].question}
                      </h4>

                      <div className="mt-4 space-y-2.5">
                        {placementQuestions[placementCurrentIdx].options.map((opt, optIdx) => {
                          const qid = placementQuestions[placementCurrentIdx].id;
                          const isSelected = placementAnswers[qid] === optIdx;
                          return (
                            <button
                              key={optIdx}
                              onClick={() => setPlacementAnswers((prev) => ({ ...prev, [qid]: optIdx }))}
                              className={`w-full text-left rounded-xl p-3.5 text-xs transition-all border ${
                                isSelected
                                  ? 'border-sky-400 bg-sky-500/20 text-sky-200 font-semibold shadow-[0_0_15px_rgba(56,189,248,0.2)]'
                                  : 'border-white/[0.06] bg-slate-900/50 text-slate-300 hover:border-white/20'
                              }`}
                            >
                              <div className="flex items-center gap-3">
                                <span className={`flex h-5 w-5 items-center justify-center rounded-full text-[11px] font-bold ${
                                  isSelected ? 'bg-sky-400 text-slate-950' : 'bg-slate-800 text-slate-400'
                                }`}>
                                  {String.fromCharCode(65 + optIdx)}
                                </span>
                                <span>{opt}</span>
                              </div>
                            </button>
                          );
                        })}
                      </div>

                      {/* Navigation Controls */}
                      <div className="flex items-center justify-between pt-6 border-t border-white/[0.08]">
                        <button
                          disabled={placementCurrentIdx === 0}
                          onClick={() => setPlacementCurrentIdx((i) => Math.max(0, i - 1))}
                          className="px-4 py-2 text-xs font-semibold text-slate-400 disabled:opacity-30"
                        >
                          Previous
                        </button>

                        <div className="flex gap-2">
                          {placementCurrentIdx < placementQuestions.length - 1 ? (
                            <button
                              onClick={() => setPlacementCurrentIdx((i) => Math.min(placementQuestions.length - 1, i + 1))}
                              className="rounded-xl bg-slate-800 px-5 py-2 text-xs font-bold text-white hover:bg-slate-700"
                            >
                              Next
                            </button>
                          ) : (
                            <button
                              disabled={isSubmittingPlacement}
                              onClick={handleSubmitPlacement}
                              className="rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-6 py-2 text-xs font-bold text-white shadow-neon-blue"
                            >
                              {isSubmittingPlacement ? 'Grading...' : 'Submit 20 Qs'}
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              ) : (
                /* Placement Quiz Results */
                <div className="text-center py-4 space-y-6">
                  <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 shadow-neon-blue">
                    <Sparkles className="h-8 w-8 text-white" />
                  </div>

                  <div>
                    <span className="text-xs uppercase font-extrabold tracking-wider text-sky-400">
                      Placement Complete
                    </span>
                    <h3 className="mt-1 text-2xl font-extrabold text-white">
                      Ranked: {placementResult.level} Tier
                    </h3>
                    <p className="mt-1 text-xs text-slate-300">
                      Weighted Score: {placementResult.score_percentage}% ({placementResult.score_correct} / {placementResult.total_questions} correct)
                    </p>
                  </div>

                  <div className="rounded-2xl border border-white/[0.08] bg-slate-900/60 p-4 text-xs text-slate-300 text-left leading-relaxed">
                    <span className="font-bold text-sky-400 block mb-1">AI Academic Evaluation:</span>
                    {placementResult.explanation}
                  </div>

                  {placementResult.topic_breakdown && (
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-left">
                      {Object.entries(placementResult.topic_breakdown).map(([top, stat]: any) => (
                        <div key={top} className="bg-slate-900/40 p-2.5 rounded-xl border border-white/[0.04]">
                          <span className="text-[11px] font-semibold text-slate-300 block line-clamp-1">{top}</span>
                          <span className="text-xs font-extrabold text-sky-400">{stat.percentage}% ({stat.correct}/{stat.total})</span>
                        </div>
                      ))}
                    </div>
                  )}

                  <div className="pt-4">
                    <button
                      onClick={() => setIsPlacementModalOpen(false)}
                      className="rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-8 py-2.5 text-xs font-bold text-white shadow-neon-blue"
                    >
                      View Updated Roadmap
                    </button>
                  </div>
                </div>
              )}
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </div>
  );
};

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import confetti from 'canvas-confetti';
import {
  Award,
  CheckCircle2,
  XCircle,
  Clock,
  Sparkles,
  HelpCircle,
  ArrowRight,
  RotateCcw,
  Zap,
  TrendingUp,
  BookOpen,
  Code
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import { GlassCard } from '../components/ui/GlassCard';
import { MagneticButton } from '../components/ui/MagneticButton';
import { Badge } from '../components/ui/Badge';
import { AssessmentQuestion, AssessmentFeedback } from '../types';

export const Assessment: React.FC = () => {
  const { addPoints } = useAuth();
  const [questions, setQuestions] = useState<AssessmentQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [feedback, setFeedback] = useState<AssessmentFeedback | null>(null);
  const [consecutiveCorrect, setConsecutiveCorrect] = useState(0);
  const [currentDifficulty, setCurrentDifficulty] = useState<'Easy' | 'Medium' | 'Hard' | 'Expert'>('Easy');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [scoreTotal, setScoreTotal] = useState(0);
  const [isCompleted, setIsCompleted] = useState(false);
  const [showHint, setShowHint] = useState(false);

  useEffect(() => {
    api.getQuestions('pytorch').then((items) => {
      setQuestions(items);
      if (items.length > 0) {
        setCurrentDifficulty(items[0].difficulty);
      }
    });
  }, []);

  const currentQ = questions[currentIndex];

  const handleSelectOption = (idx: number) => {
    if (feedback) return; // Locked once evaluated
    setSelectedOption(idx);
  };

  const handleSubmit = async () => {
    if (selectedOption === null || !currentQ || isSubmitting) return;
    setIsSubmitting(true);

    try {
      const res = await api.submitAnswer(
        currentQ.skill_id,
        currentQ.id,
        selectedOption,
        consecutiveCorrect
      );
      setFeedback(res);
      setCurrentDifficulty(res.new_difficulty);

      if (res.is_correct) {
        setConsecutiveCorrect(prev => prev + 1);
        setScoreTotal(prev => prev + res.points_earned);
        addPoints(res.points_earned);
        confetti({
          particleCount: 50,
          spread: 60,
          origin: { y: 0.7 }
        });
      } else {
        setConsecutiveCorrect(0);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNext = () => {
    setFeedback(null);
    setSelectedOption(null);
    setShowHint(false);

    if (currentIndex + 1 < questions.length) {
      setCurrentIndex(prev => prev + 1);
    } else {
      setIsCompleted(true);
    }
  };

  const handleRestart = () => {
    setCurrentIndex(0);
    setSelectedOption(null);
    setFeedback(null);
    setIsCompleted(false);
    setScoreTotal(0);
    setConsecutiveCorrect(0);
    setCurrentDifficulty('Easy');
  };

  const difficultyColors = {
    Easy: 'bg-emerald-500/20 text-emerald-300 border-emerald-400/30',
    Medium: 'bg-sky-500/20 text-sky-300 border-sky-400/30',
    Hard: 'bg-amber-500/20 text-amber-300 border-amber-400/30',
    Expert: 'bg-rose-500/20 text-rose-300 border-rose-400/30 shadow-[0_0_15px_rgba(244,63,94,0.3)]',
  };

  return (
    <div className="relative min-h-screen bg-[var(--bg-primary)] pb-20 pt-8 text-[var(--text-primary)] transition-colors duration-300">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        {/* Top Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-[var(--border-subtle)] pb-6">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="verified">Live Adaptive Assessment Runner</Badge>
              <span className="text-xs text-slate-400">PyTorch & Deep Learning Milestone</span>
            </div>
            <h1 className="mt-2 text-2xl sm:text-3xl font-extrabold text-white">
              Adaptive Mastery <span className="text-gradient">Challenge</span>
            </h1>
          </div>

          {/* Difficulty & Streak Gauge */}
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 rounded-xl border border-white/[0.08] bg-slate-900/70 px-3.5 py-2 text-xs">
              <span className="text-slate-400">Adaptive Tier:</span>
              <span className={`rounded-full px-2.5 py-0.5 font-bold uppercase ${difficultyColors[currentDifficulty]}`}>
                {currentDifficulty}
              </span>
            </div>

            <div className="flex items-center gap-1.5 rounded-xl border border-violet-500/30 bg-violet-500/10 px-3 py-2 text-xs font-semibold text-violet-300">
              <Zap className="h-4 w-4 fill-violet-400" />
              <span>{scoreTotal} XP Won</span>
            </div>
          </div>
        </div>

        {/* Quiz Runner View or Results */}
        {!isCompleted && currentQ ? (
          <div className="mt-8 space-y-6">
            {/* Question Progress & Meta */}
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Question {currentIndex + 1} of {questions.length}</span>
              <span className="flex items-center gap-1 text-sky-400">
                <TrendingUp className="h-3.5 w-3.5" />
                Adaptive difficulty dynamic recalibration active
              </span>
            </div>

            {/* Question Card */}
            <GlassCard glowColor="blue" className="p-6 sm:p-8">
              <div className="flex items-start justify-between gap-4">
                <h2 className="text-lg sm:text-xl font-bold text-white leading-snug">
                  {currentQ.question}
                </h2>
                {currentQ.hint && (
                  <button
                    onClick={() => setShowHint(!showHint)}
                    className="flex items-center gap-1 rounded-lg border border-white/[0.08] bg-slate-800/80 px-2.5 py-1 text-xs text-slate-300 hover:text-white"
                  >
                    <HelpCircle className="h-3.5 w-3.5 text-amber-400" />
                    <span>Hint</span>
                  </button>
                )}
              </div>

              {/* Optional Hint Toggle */}
              {showHint && currentQ.hint && (
                <div className="mt-4 rounded-xl border border-amber-500/20 bg-amber-500/10 p-3 text-xs text-amber-200">
                  💡 <strong>Concept Hint:</strong> {currentQ.hint}
                </div>
              )}

              {/* Code Snippet Box */}
              {currentQ.code_snippet && (
                <div className="mt-5 overflow-hidden rounded-xl border border-slate-700/60 bg-slate-950 p-4">
                  <div className="flex items-center gap-2 border-b border-slate-800 pb-2 mb-3 text-xs text-slate-400">
                    <Code className="h-3.5 w-3.5 text-sky-400" />
                    <span>Python 3.12 / PyTorch Execution Context</span>
                  </div>
                  <pre className="overflow-x-auto text-xs sm:text-sm text-sky-200 leading-relaxed font-mono">
                    <code>{currentQ.code_snippet}</code>
                  </pre>
                </div>
              )}

              {/* Options List */}
              <div className="mt-6 space-y-3">
                {currentQ.options.map((option, idx) => {
                  const isSelected = selectedOption === idx;
                  const isAnswered = feedback !== null;
                  const isCorrectAnswer = isAnswered && idx === feedback.correct_option_index;
                  const isWrongSelected = isAnswered && isSelected && !feedback.is_correct;

                  let cardStyle = 'border-white/[0.08] bg-slate-900/50 hover:bg-white/[0.04] text-slate-200';
                  if (isSelected && !isAnswered) {
                    cardStyle = 'border-sky-400 bg-sky-500/10 text-white shadow-neon-blue';
                  }
                  if (isCorrectAnswer) {
                    cardStyle = 'border-emerald-400 bg-emerald-500/15 text-emerald-200 shadow-[0_0_20px_rgba(16,185,129,0.3)]';
                  } else if (isWrongSelected) {
                    cardStyle = 'border-rose-400 bg-rose-500/15 text-rose-200';
                  }

                  return (
                    <motion.div
                      key={idx}
                      whileHover={!isAnswered ? { scale: 1.01 } : {}}
                      whileTap={!isAnswered ? { scale: 0.99 } : {}}
                      onClick={() => handleSelectOption(idx)}
                      className={`flex items-center justify-between rounded-xl border p-4 text-xs sm:text-sm font-medium transition-all cursor-pointer ${cardStyle}`}
                    >
                      <div className="flex items-center gap-3">
                        <span className="flex h-6 w-6 items-center justify-center rounded-lg border border-white/[0.1] bg-slate-800 text-xs font-bold text-slate-300">
                          {String.fromCharCode(65 + idx)}
                        </span>
                        <span>{option}</span>
                      </div>

                      {isCorrectAnswer && (
                        <CheckCircle2 className="h-5 w-5 text-emerald-400 flex-shrink-0" />
                      )}
                      {isWrongSelected && (
                        <XCircle className="h-5 w-5 text-rose-400 flex-shrink-0" />
                      )}
                    </motion.div>
                  );
                })}
              </div>

              {/* Action Buttons */}
              <div className="mt-8 flex items-center justify-between border-t border-white/[0.06] pt-6">
                {!feedback ? (
                  <MagneticButton
                    variant="primary"
                    onClick={handleSubmit}
                    disabled={selectedOption === null || isSubmitting}
                    className="ml-auto"
                  >
                    <span>Submit & Verify</span>
                    <ArrowRight className="h-4 w-4" />
                  </MagneticButton>
                ) : (
                  <MagneticButton
                    variant="primary"
                    onClick={handleNext}
                    className="ml-auto shadow-neon-blue"
                  >
                    <span>Next Challenge</span>
                    <ArrowRight className="h-4 w-4" />
                  </MagneticButton>
                )}
              </div>
            </GlassCard>

            {/* Instant Feedback Modal / Box */}
            <AnimatePresence>
              {feedback && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                >
                  <GlassCard
                    glowColor={feedback.is_correct ? 'emerald' : 'violet'}
                    className="p-6"
                  >
                    <div className="flex items-center gap-3">
                      {feedback.is_correct ? (
                        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                          <CheckCircle2 className="h-6 w-6" />
                        </div>
                      ) : (
                        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-rose-500/20 text-rose-400 border border-rose-500/30">
                          <XCircle className="h-6 w-6" />
                        </div>
                      )}
                      <div>
                        <h3 className="text-base font-bold text-white">
                          {feedback.is_correct ? 'Mastery Confirmed! (+50 XP)' : 'Insightful Opportunity to Reinforce'}
                        </h3>
                        <p className="text-xs text-slate-400">
                          Difficulty calibrated to <strong className="text-sky-300">{feedback.new_difficulty}</strong> for subsequent challenges.
                        </p>
                      </div>
                    </div>

                    <div className="mt-4 rounded-xl border border-white/[0.06] bg-slate-900/60 p-4">
                      <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
                        {feedback.explanation}
                      </p>
                      <div className="mt-3 flex items-center gap-2 text-xs text-sky-400 font-semibold border-t border-white/[0.05] pt-2">
                        <BookOpen className="h-3.5 w-3.5" />
                        <span>Source Grounding: {feedback.grounded_source}</span>
                      </div>
                    </div>
                  </GlassCard>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ) : (
          /* Completion Screen */
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mt-8 text-center"
          >
            <GlassCard glowColor="blue" className="p-10 md:p-14">
              <div className="mx-auto flex h-20 w-20 items-center justify-center rounded-full bg-gradient-to-tr from-sky-500 to-indigo-600 shadow-neon-blue">
                <Award className="h-10 w-10 text-white" />
              </div>

              <h2 className="mt-6 text-3xl font-extrabold text-white">
                Assessment Completed!
              </h2>
              <p className="mt-2 text-sm text-slate-300 max-w-md mx-auto">
                You earned <strong className="text-sky-400 font-bold">{scoreTotal} XP</strong> and demonstrated high proficiency across reverse-mode autograd and optimizer mechanics.
              </p>

              <div className="mt-8 flex justify-center gap-4">
                <MagneticButton variant="primary" onClick={handleRestart}>
                  <RotateCcw className="h-4 w-4" />
                  <span>Retake Challenge</span>
                </MagneticButton>
                <MagneticButton variant="secondary" onClick={() => window.location.href = '/roadmap'}>
                  <span>Return to Roadmap</span>
                </MagneticButton>
              </div>
            </GlassCard>
          </motion.div>
        )}
      </div>
    </div>
  );
};

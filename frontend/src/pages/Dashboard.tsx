import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip
} from 'recharts';
import {
  Flame,
  Zap,
  Award,
  TrendingUp,
  Map,
  BookOpen,
  CheckCircle2,
  FileText,
  ArrowUpRight,
  ChevronRight,
  Sparkles,
  Target,
  Play
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import { GlassCard } from '../components/ui/GlassCard';
import { MagneticButton } from '../components/ui/MagneticButton';
import { Badge } from '../components/ui/Badge';
import { SkillGraphResponse } from '../types';

const PROGRESS_HISTORY = [
  { week: 'Wk 1', mastery: 35, ats: 58 },
  { week: 'Wk 2', mastery: 48, ats: 66 },
  { week: 'Wk 3', mastery: 58, ats: 74 },
  { week: 'Wk 4', mastery: 68, ats: 81 },
  { week: 'Current', mastery: 74, ats: 84 },
];

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [roadmap, setRoadmap] = useState<SkillGraphResponse | null>(null);

  useEffect(() => {
    api.getRoadmap(user?.career_goal || 'AI Engineer').then(setRoadmap);
  }, [user?.career_goal]);

  const radarData = user?.radar_data || [
    { subject: 'Deep Learning', A: 85, fullMark: 100 },
    { subject: 'System Design', A: 65, fullMark: 100 },
    { subject: 'Algorithms', A: 90, fullMark: 100 },
    { subject: 'MLOps', A: 55, fullMark: 100 },
    { subject: 'Cloud & Infra', A: 70, fullMark: 100 },
    { subject: 'Applied RAG', A: 68, fullMark: 100 },
  ];

  const currentMilestone = roadmap?.nodes.find(n => n.status === 'in_progress') || roadmap?.nodes[2];

  return (
    <div className="relative min-h-screen bg-[var(--bg-primary)] pb-16 pt-8 text-[var(--text-primary)] transition-colors duration-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Welcome Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-[var(--border-subtle)] pb-6">
          <div>
            <div className="flex items-center gap-2.5">
              <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
                Welcome back, {user?.name.split(' ')[0] || 'Aarav'}
              </h1>
              <Badge variant="verified">Profile Verified</Badge>
            </div>
            <p className="mt-1 text-xs sm:text-sm text-slate-400">
              Track your trajectory toward <span className="text-sky-400 font-semibold">{user?.career_goal || 'AI Engineer'}</span> with real-time RAG guidance.
            </p>
          </div>

          {/* Stat Pills */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2 rounded-xl border border-amber-500/30 bg-amber-500/10 px-4 py-2 text-xs font-semibold text-amber-300 backdrop-blur-md">
              <Flame className="h-4 w-4 fill-amber-400 text-amber-400" />
              <div>
                <span className="block text-sm font-bold text-amber-200">{user?.streak || 14} Days</span>
                <span className="text-[10px] text-amber-400/80 uppercase">Active Streak</span>
              </div>
            </div>

            <div className="flex items-center gap-2 rounded-xl border border-violet-500/30 bg-violet-500/10 px-4 py-2 text-xs font-semibold text-violet-300 backdrop-blur-md">
              <Zap className="h-4 w-4 fill-violet-400 text-violet-400" />
              <div>
                <span className="block text-sm font-bold text-violet-200">{user?.points || 860} XP</span>
                <span className="text-[10px] text-violet-400/80 uppercase">Total XP</span>
              </div>
            </div>

            <div className="flex items-center gap-2 rounded-xl border border-sky-500/30 bg-sky-500/10 px-4 py-2 text-xs font-semibold text-sky-300 backdrop-blur-md">
              <Target className="h-4 w-4 text-sky-400" />
              <div>
                <span className="block text-sm font-bold text-sky-200">{roadmap?.completion_rate || 66}%</span>
                <span className="text-[10px] text-sky-400/80 uppercase">Roadmap Progress</span>
              </div>
            </div>
          </div>
        </div>

        {/* Top Grid: Hero Milestone & Skill Radar */}
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Active Milestone Spotlight (7 cols) */}
          <div className="lg:col-span-7 flex flex-col gap-6">
            <GlassCard glowColor="blue" className="p-6 md:p-8 relative overflow-hidden">
              <div className="pointer-events-none absolute -right-16 -top-16 h-64 w-64 rounded-full bg-sky-500/10 blur-3xl" />
              
              <div className="flex items-center justify-between">
                <Badge variant="in_progress">Active Focus Milestone</Badge>
                <span className="text-xs text-slate-400">Estimated {currentMilestone?.estimated_hours || 35}h Remaining</span>
              </div>

              <h2 className="mt-3 text-2xl font-bold text-white">
                {currentMilestone?.name || 'PyTorch & Deep Neural Networks'}
              </h2>
              <p className="mt-2 text-xs sm:text-sm text-slate-300 leading-relaxed">
                Master autograd reverse-mode automatic differentiation, custom Module classes, and distributed multi-GPU data parallelism.
              </p>

              {/* Progress Bar */}
              <div className="mt-5 space-y-1.5">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-400">Mastery Level</span>
                  <span className="text-sky-400 font-bold">{currentMilestone?.mastery_level || 74}%</span>
                </div>
                <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-sky-400 to-indigo-500 transition-all duration-500"
                    style={{ width: `${currentMilestone?.mastery_level || 74}%` }}
                  />
                </div>
              </div>

              {/* Capstone Callout */}
              <div className="mt-6 rounded-xl border border-white/[0.08] bg-slate-900/60 p-4">
                <div className="flex items-center gap-2 text-xs font-semibold text-sky-300">
                  <Sparkles className="h-4 w-4" />
                  <span>Capstone Project Requirement:</span>
                </div>
                <p className="mt-1 text-xs text-slate-300">
                  {currentMilestone?.milestone_project || 'Vision Transformer (ViT) Classifier from Scratch with Top-1 Accuracy >= 85%'}
                </p>
              </div>

              {/* Actions */}
              <div className="mt-6 flex flex-wrap items-center gap-3">
                <Link to="/assessment">
                  <MagneticButton variant="primary">
                    <Play className="h-4 w-4 fill-white" />
                    <span>Launch Adaptive Quiz</span>
                  </MagneticButton>
                </Link>
                <Link to="/resources">
                  <MagneticButton variant="secondary">
                    <BookOpen className="h-4 w-4 text-sky-400" />
                    <span>View Grounded Resources</span>
                  </MagneticButton>
                </Link>
                <Link to="/roadmap" className="ml-auto text-xs font-semibold text-sky-400 hover:text-sky-300 flex items-center gap-1">
                  Full Roadmap <ChevronRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </GlassCard>

            {/* Trajectory Growth Graph */}
            <GlassCard glowColor="violet" className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-base font-bold text-white">Trajectory & ATS Growth</h3>
                  <p className="text-xs text-slate-400">Weekly progression of technical mastery and ATS readiness</p>
                </div>
                <Badge variant="rag">RAG Model v1.0</Badge>
              </div>

              <div className="h-56 w-full">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={PROGRESS_HISTORY}>
                    <defs>
                      <linearGradient id="colorMastery" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#38bdf8" stopOpacity={0} />
                      </linearGradient>
                      <linearGradient id="colorAts" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#a855f7" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#a855f7" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <XAxis dataKey="week" stroke="#64748b" fontSize={11} />
                    <YAxis stroke="#64748b" fontSize={11} domain={[0, 100]} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#0f172a',
                        border: '1px solid rgba(255,255,255,0.1)',
                        borderRadius: '8px',
                        fontSize: '12px',
                        color: '#fff',
                      }}
                    />
                    <Area
                      type="monotone"
                      dataKey="mastery"
                      stroke="#38bdf8"
                      strokeWidth={2}
                      fillOpacity={1}
                      fill="url(#colorMastery)"
                      name="Technical Mastery %"
                    />
                    <Area
                      type="monotone"
                      dataKey="ats"
                      stroke="#a855f7"
                      strokeWidth={2}
                      fillOpacity={1}
                      fill="url(#colorAts)"
                      name="ATS Score %"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </GlassCard>
          </div>

          {/* Right Column: 6-Axis Radar & Quick Launch (5 cols) */}
          <div className="lg:col-span-5 flex flex-col gap-6">
            {/* Recharts Skill Radar */}
            <GlassCard glowColor="blue" className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-base font-bold text-white">6-Axis Competency Radar</h3>
                  <p className="text-xs text-slate-400">Recruiter benchmark vs your verified profile</p>
                </div>
                <Badge variant="verified">Top 8% Tier</Badge>
              </div>

              <div className="h-64 w-full mt-2">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="75%" data={radarData}>
                    <PolarGrid stroke="rgba(255, 255, 255, 0.1)" />
                    <PolarAngleAxis dataKey="subject" stroke="#94a3b8" fontSize={10} tickLine={false} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" fontSize={9} />
                    <Radar
                      name="Aarav Sharma"
                      dataKey="A"
                      stroke="#38bdf8"
                      fill="#38bdf8"
                      fillOpacity={0.35}
                    />
                  </RadarChart>
                </ResponsiveContainer>
              </div>

              <div className="mt-3 flex items-center justify-between border-t border-white/[0.06] pt-3 text-xs text-slate-400">
                <span>Strongest: <strong className="text-sky-400">Algorithms (90%)</strong></span>
                <span>Next Target: <strong className="text-violet-400">MLOps (55%)</strong></span>
              </div>
            </GlassCard>

            {/* Quick Actions Panel */}
            <GlassCard glowColor="emerald" className="p-6">
              <h3 className="text-base font-bold text-white mb-3">Quick Navigation</h3>
              <div className="space-y-2.5">
                <Link
                  to="/resume"
                  className="flex items-center justify-between rounded-xl border border-white/[0.06] bg-slate-900/50 p-3 hover:bg-white/[0.04] transition-all"
                >
                  <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-violet-500/10 text-violet-400 border border-violet-500/20">
                      <FileText className="h-4 w-4" />
                    </div>
                    <div>
                      <span className="text-xs font-bold text-white block">Resume ATS Analyzer</span>
                      <span className="text-[11px] text-slate-400">Current Score: 84/100 (3 gaps detected)</span>
                    </div>
                  </div>
                  <ArrowUpRight className="h-4 w-4 text-slate-400" />
                </Link>

                <Link
                  to="/recommendations"
                  className="flex items-center justify-between rounded-xl border border-white/[0.06] bg-slate-900/50 p-3 hover:bg-white/[0.04] transition-all"
                >
                  <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      <Sparkles className="h-4 w-4" />
                    </div>
                    <div>
                      <span className="text-xs font-bold text-white block">AI Job & Project Matches</span>
                      <span className="text-[11px] text-slate-400">98% match on Hybrid RAG project</span>
                    </div>
                  </div>
                  <ArrowUpRight className="h-4 w-4 text-slate-400" />
                </Link>

                <Link
                  to="/onboarding"
                  className="flex items-center justify-between rounded-xl border border-white/[0.06] bg-slate-900/50 p-3 hover:bg-white/[0.04] transition-all"
                >
                  <div className="flex items-center gap-3">
                    <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-sky-500/10 text-sky-400 border border-sky-500/20">
                      <CheckCircle2 className="h-4 w-4" />
                    </div>
                    <div>
                      <span className="text-xs font-bold text-white block">Upload New Certificate / Marksheet</span>
                      <span className="text-[11px] text-slate-400">Instant CV/OCR credential validation</span>
                    </div>
                  </div>
                  <ArrowUpRight className="h-4 w-4 text-slate-400" />
                </Link>
              </div>
            </GlassCard>
          </div>
        </div>
      </div>
    </div>
  );
};

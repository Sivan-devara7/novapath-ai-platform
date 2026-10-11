import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
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
  User,
  Award,
  ShieldCheck,
  CheckCircle2,
  Mail,
  Target,
  Flame,
  Zap,
  BookOpen,
  Sparkles,
  Save,
  Compass,
  ArrowRight,
  TrendingUp,
  BarChart2,
  Clock,
  Check
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../services/api';
import { GlassCard } from '../components/ui/GlassCard';
import { MagneticButton } from '../components/ui/MagneticButton';
import { Badge } from '../components/ui/Badge';
import { SkillGalaxyHero } from '../components/3d/SkillGalaxyHero';
import { ActivityHeatmap } from '../components/ui/ActivityHeatmap';
import { CourseModule } from '../types';

export const Profile: React.FC = () => {
  const navigate = useNavigate();
  const { user, updateUser } = useAuth();
  const { t } = useLanguage();
  const [careerGoal, setCareerGoal] = useState(user?.career_goal || 'AI Engineer');
  const [saved, setSaved] = useState(false);
  const [modules, setModules] = useState<CourseModule[]>([]);
  const [isLoadingModules, setIsLoadingModules] = useState(true);

  useEffect(() => {
    api.getModules()
      .then((data) => {
        setModules(data.modules || []);
      })
      .catch((err) => {
        console.error('Failed to load modules:', err);
      })
      .finally(() => {
        setIsLoadingModules(false);
      });
  }, []);

  const handleSave = () => {
    updateUser({ career_goal: careerGoal });
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  const passedCount = modules.filter(m => m.status === 'passed').length;
  const overallMastery = user?.mastery_overall || Math.round((passedCount / Math.max(modules.length, 1)) * 100) || 72;

  const radarData = user?.radar_data || [
    { subject: 'Deep Learning', A: 85, fullMark: 100 },
    { subject: 'System Design', A: 65, fullMark: 100 },
    { subject: 'Algorithms', A: 90, fullMark: 100 },
    { subject: 'MLOps', A: 55, fullMark: 100 },
    { subject: 'Cloud & Infra', A: 70, fullMark: 100 },
    { subject: 'Applied RAG', A: 68, fullMark: 100 },
  ];

  const velocityData = [
    { week: 'Wk 1', xp: 120, mastery: 35 },
    { week: 'Wk 2', xp: 240, mastery: 48 },
    { week: 'Wk 3', xp: 420, mastery: 58 },
    { week: 'Wk 4', xp: 650, mastery: 68 },
    { week: 'Current', xp: user?.points || 860, mastery: overallMastery },
  ];

  return (
    <div className="relative min-h-screen bg-[var(--bg-primary)] pb-20 pt-8 text-[var(--text-primary)] transition-colors duration-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 space-y-8">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-white/[0.07] pb-6">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="verified">Student Identity & Academic Analytics</Badge>
              <span className="text-xs text-sky-400">Verified Credentials & Learning Velocity</span>
            </div>
            <h1 className="mt-2 text-2xl sm:text-4xl font-extrabold text-white">
              {t('profile_title', 'Student Intelligence Profile')}
            </h1>
            <p className="mt-1 text-xs sm:text-sm text-slate-300">
              {t('profile_subtitle', 'Your verified skill mastery, activity velocity, and learning progress')}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => navigate('/roadmap')}
              className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-4 py-2.5 text-xs font-bold text-white shadow-neon-blue hover:scale-105 transition-all"
            >
              <Compass className="h-4 w-4" />
              <span>Resume Active Roadmap</span>
            </button>
          </div>
        </div>

        {/* ================= ROW 1: PROFILE DETAILS + SKILL DEPICTOR CARD ================= */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
          
          {/* Main Profile Detail Card (5 cols) */}
          <GlassCard glowColor="blue" className="lg:col-span-5 p-6 flex flex-col justify-between">
            <div>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-4">
                  <div className="relative flex h-20 w-20 shrink-0 items-center justify-center rounded-2xl border-2 border-sky-400/40 bg-slate-800 text-2xl font-black text-sky-300 shadow-neon-blue">
                    {user?.name.slice(0, 2).toUpperCase() || 'AS'}
                    <div className="absolute -bottom-1 -right-1 flex h-6 w-6 items-center justify-center rounded-full bg-emerald-500 text-slate-950 shadow-md">
                      <CheckCircle2 className="h-4 w-4" />
                    </div>
                  </div>
                  <div>
                    <h2 className="text-xl font-bold text-white">{user?.name || 'Aarav Sharma'}</h2>
                    <p className="text-xs text-slate-400 flex items-center gap-1.5 mt-0.5">
                      <Mail className="h-3 w-3" />
                      {user?.email || 'aarav.sharma@vizag.edu'}
                    </p>
                    <span className="mt-2 inline-flex items-center gap-1 rounded-full border border-sky-400/30 bg-sky-500/10 px-2.5 py-0.5 text-[11px] font-semibold text-sky-300">
                      Target: {careerGoal}
                    </span>
                  </div>
                </div>
              </div>

              {/* Core Quick Stats */}
              <div className="mt-6 grid grid-cols-3 gap-2 border-y border-white/[0.06] py-3 text-center text-xs">
                <div>
                  <span className="text-slate-400 block text-[11px]">Active Streak</span>
                  <span className="text-sm font-bold text-amber-300 flex items-center justify-center gap-0.5 mt-0.5">
                    <Flame className="h-3.5 w-3.5 fill-amber-400" />
                    {user?.streak || 14}d
                  </span>
                </div>
                <div className="border-x border-white/[0.06]">
                  <span className="text-slate-400 block text-[11px]">Mastery XP</span>
                  <span className="text-sm font-bold text-violet-300 flex items-center justify-center gap-0.5 mt-0.5">
                    <Zap className="h-3.5 w-3.5 fill-violet-400" />
                    {user?.points || 860}
                  </span>
                </div>
                <div>
                  <span className="text-slate-400 block text-[11px]">Overall Mastery</span>
                  <span className="text-sm font-bold text-emerald-300 mt-0.5 block">
                    {overallMastery}%
                  </span>
                </div>
              </div>

              {/* University & Degree Information */}
              <div className="mt-5 space-y-2.5 text-xs">
                <div className="flex justify-between text-slate-400">
                  <span>Institution:</span>
                  <strong className="text-slate-200">IIIT Vizag / Andhra University</strong>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Degree & Track:</span>
                  <strong className="text-slate-200">B.Tech Computer Science</strong>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Academic CGPA:</span>
                  <strong className="text-emerald-400">8.9 / 10.0 (Verified OCR)</strong>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Modules Cleared:</span>
                  <strong className="text-sky-300">{passedCount} of {modules.length || 6} Completed</strong>
                </div>
              </div>
            </div>

            {/* Target Role Selector */}
            <div className="mt-6 border-t border-white/[0.06] pt-4">
              <label className="block text-xs font-bold text-slate-300 mb-2">
                Active Career Track Trajectory:
              </label>
              <div className="grid grid-cols-2 gap-2">
                {['AI Engineer', 'Data Engineer', 'Cybersecurity Analyst', 'Full Stack Developer'].map((role) => (
                  <button
                    key={role}
                    type="button"
                    onClick={() => {
                      setCareerGoal(role);
                      updateUser({ career_goal: role });
                    }}
                    className={`rounded-xl border p-2 text-left text-xs font-semibold transition-all ${
                      careerGoal === role
                        ? 'border-sky-400 bg-sky-500/15 text-white shadow-sm'
                        : 'border-white/[0.06] bg-slate-900/40 text-slate-400 hover:text-white'
                    }`}
                  >
                    <div className="flex items-center gap-1.5">
                      <Target className="h-3 w-3 text-sky-400 shrink-0" />
                      <span className="line-clamp-1">{role}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </GlassCard>

          {/* Skill Depictor 3D Card (7 cols) - replaces solar system as requested */}
          <GlassCard glowColor="violet" className="lg:col-span-7 p-6 flex flex-col justify-between">
            <div className="flex items-center justify-between border-b border-white/[0.06] pb-3 mb-3">
              <div>
                <div className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-violet-400" />
                  <h3 className="text-base font-bold text-white">{t('profile_skill_galaxy_title', '3D Skill Depictor & Mastery Core')}</h3>
                </div>
                <p className="text-xs text-slate-400 mt-0.5">
                  Interactive topological cluster mapping verified capabilities and active competencies.
                </p>
              </div>
              <span className="rounded-full border border-violet-400/30 bg-violet-500/10 px-3 py-1 text-xs font-bold text-violet-300">
                Live Spatial Depictor
              </span>
            </div>

            {/* 3D Skill Galaxy Embedded Viewer */}
            <div className="relative w-full h-[320px] rounded-2xl overflow-hidden border border-white/[0.06] bg-slate-950/70">
              <SkillGalaxyHero />
            </div>

            <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400">
              <span>🔵 Cyan: Completed • 🟣 Purple: In Progress • 🟢 Emerald: Ready</span>
              <span>Drag to rotate nodes</span>
            </div>
          </GlassCard>
        </div>

        {/* ================= ROW 2: TOTAL ACTIVE DAYS HEATMAP ================= */}
        <div>
          <ActivityHeatmap
            totalActiveDays={48}
            currentStreak={user?.streak || 14}
            longestStreak={21}
            totalXp={user?.points || 860}
          />
        </div>

        {/* ================= ROW 3: LEARNING ANALYTICS & PROGRESS TRACKING ================= */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* Radar Competency Chart (6 cols) */}
          <GlassCard glowColor="blue" className="lg:col-span-6 p-6">
            <div className="flex items-center justify-between border-b border-white/[0.06] pb-3 mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <BarChart2 className="h-4 w-4 text-sky-400" />
                  Competency Mastery Radar
                </h3>
                <p className="text-xs text-slate-400">
                  Multidimensional skill evaluation synthesized from placement quizzes and module tests.
                </p>
              </div>
              <span className="text-xs font-extrabold text-emerald-400">
                {overallMastery}% Average
              </span>
            </div>

            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData}>
                  <PolarGrid stroke="rgba(255, 255, 255, 0.1)" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
                  <Radar
                    name="Student Mastery"
                    dataKey="A"
                    stroke="#38bdf8"
                    fill="#38bdf8"
                    fillOpacity={0.4}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            <div className="mt-3 grid grid-cols-3 gap-2 text-center text-xs border-t border-white/[0.04] pt-3">
              <div>
                <span className="text-slate-400 block text-[10px]">Top Strength</span>
                <span className="font-bold text-sky-300">Algorithms (90%)</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">Primary Gap</span>
                <span className="font-bold text-rose-300">MLOps (55%)</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">Growth Velocity</span>
                <span className="font-bold text-emerald-300">+14% / Mo</span>
              </div>
            </div>
          </GlassCard>

          {/* XP & Progress Velocity Area Chart (6 cols) */}
          <GlassCard glowColor="violet" className="lg:col-span-6 p-6">
            <div className="flex items-center justify-between border-b border-white/[0.06] pb-3 mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-violet-400" />
                  Learning Velocity & XP Growth
                </h3>
                <p className="text-xs text-slate-400">
                  Weekly mastery accrual through milestone quiz clears and RAG study modules.
                </p>
              </div>
              <span className="text-xs font-extrabold text-violet-300">
                {user?.points || 860} XP Total
              </span>
            </div>

            <div className="h-64 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={velocityData}>
                  <defs>
                    <linearGradient id="xpGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#a855f7" stopOpacity={0.4} />
                      <stop offset="95%" stopColor="#a855f7" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="week" stroke="#64748b" fontSize={11} />
                  <YAxis stroke="#64748b" fontSize={11} />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      borderColor: 'rgba(255,255,255,0.1)',
                      borderRadius: '12px',
                      fontSize: '12px'
                    }}
                  />
                  <Area
                    type="monotone"
                    dataKey="xp"
                    stroke="#a855f7"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#xpGradient)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            {/* Verified Skills Cloud */}
            <div className="mt-3 border-t border-white/[0.04] pt-3">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-white">Verified Competencies:</span>
                <span className="text-[10px] text-emerald-400 font-semibold">
                  {(user?.verified_skills || ['Python', 'PyTorch', 'Linear Algebra', 'FastAPI', 'Docker', 'Git', 'CUDA']).length} Verified
                </span>
              </div>
              <div className="flex flex-wrap gap-1.5">
                {(user?.verified_skills || ['Python', 'PyTorch', 'Linear Algebra', 'FastAPI', 'Docker', 'Git', 'CUDA']).map((s) => (
                  <span
                    key={s}
                    className="inline-flex items-center gap-1 rounded-lg border border-emerald-500/30 bg-emerald-500/10 px-2 py-0.5 text-[10px] font-semibold text-emerald-300"
                  >
                    <Check className="h-3 w-3 text-emerald-400" />
                    {s}
                  </span>
                ))}
              </div>
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
};

export default Profile;

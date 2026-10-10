import React, { useState } from 'react';
import { motion } from 'framer-motion';
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
  Save
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { GlassCard } from '../components/ui/GlassCard';
import { MagneticButton } from '../components/ui/MagneticButton';
import { Badge } from '../components/ui/Badge';

export const Profile: React.FC = () => {
  const { user, updateUser } = useAuth();
  const [careerGoal, setCareerGoal] = useState(user?.career_goal || 'AI Engineer');
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    updateUser({ career_goal: careerGoal });
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="relative min-h-screen bg-[var(--bg-primary)] pb-20 pt-8 text-[var(--text-primary)] transition-colors duration-300">
      <div className="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="border-b border-white/[0.07] pb-6">
          <Badge variant="verified">Student Identity</Badge>
          <h1 className="mt-2 text-2xl sm:text-4xl font-extrabold text-white">
            Academic & Career <span className="text-gradient">Profile</span>
          </h1>
          <p className="mt-1 text-xs sm:text-sm text-slate-300">
            Manage your verified credentials, academic GPA records, and target trajectory parameters.
          </p>
        </div>

        <div className="mt-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column: Identity Card (4 cols) */}
          <GlassCard glowColor="blue" className="lg:col-span-4 p-6 flex flex-col items-center text-center">
            <div className="relative flex h-24 w-24 items-center justify-center rounded-full border-2 border-sky-400/40 bg-slate-800 text-2xl font-black text-sky-300 shadow-neon-blue">
              {user?.name.slice(0, 2).toUpperCase() || 'AS'}
              <div className="absolute -bottom-1 -right-1 flex h-7 w-7 items-center justify-center rounded-full bg-emerald-500 text-slate-950 shadow-md">
                <CheckCircle2 className="h-4 w-4" />
              </div>
            </div>

            <h2 className="mt-4 text-xl font-bold text-white">{user?.name || 'Aarav Sharma'}</h2>
            <p className="text-xs text-slate-400 flex items-center gap-1.5 mt-0.5">
              <Mail className="h-3 w-3" />
              {user?.email || 'aarav.sharma@vizag.edu'}
            </p>

            <div className="mt-6 flex w-full justify-around border-y border-white/[0.06] py-3 text-xs">
              <div>
                <span className="text-slate-400 block">Streak</span>
                <span className="text-sm font-bold text-amber-300 flex items-center justify-center gap-0.5">
                  <Flame className="h-3.5 w-3.5 fill-amber-400" />
                  {user?.streak || 14}d
                </span>
              </div>
              <div className="border-r border-white/[0.06]" />
              <div>
                <span className="text-slate-400 block">Mastery XP</span>
                <span className="text-sm font-bold text-violet-300 flex items-center justify-center gap-0.5">
                  <Zap className="h-3.5 w-3.5 fill-violet-400" />
                  {user?.points || 860}
                </span>
              </div>
            </div>

            <div className="mt-6 w-full text-left space-y-2 text-xs">
              <div className="flex justify-between text-slate-400">
                <span>Institution:</span>
                <strong className="text-slate-200">IIIT Vizag / Andhra Univ</strong>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Degree:</span>
                <strong className="text-slate-200">B.Tech Computer Science</strong>
              </div>
              <div className="flex justify-between text-slate-400">
                <span>Academic CGPA:</span>
                <strong className="text-emerald-400">8.9 / 10.0 (Verified)</strong>
              </div>
            </div>
          </GlassCard>

          {/* Right Column: Career Target & Verified Competencies (8 cols) */}
          <div className="lg:col-span-8 space-y-6">
            <GlassCard glowColor="violet" className="p-6">
              <h3 className="text-base font-bold text-white mb-1">Target Role Configuration</h3>
              <p className="text-xs text-slate-400 mb-4">
                Recalibrates your 3D Skill Galaxy, prerequisite roadmaps, and adaptive challenge difficulty.
              </p>

              <div className="space-y-3">
                {['AI Engineer', 'Full Stack Developer', 'Cloud & DevOps Engineer'].map((role) => (
                  <label
                    key={role}
                    className={`flex items-center justify-between rounded-xl border p-3.5 cursor-pointer transition-all ${
                      careerGoal === role
                        ? 'border-sky-400 bg-sky-500/10 text-white shadow-neon-blue'
                        : 'border-white/[0.06] bg-slate-900/40 text-slate-300 hover:bg-white/[0.03]'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <Target className="h-4 w-4 text-sky-400" />
                      <span className="text-sm font-semibold">{role}</span>
                    </div>
                    <input
                      type="radio"
                      name="careerGoal"
                      checked={careerGoal === role}
                      onChange={() => setCareerGoal(role)}
                      className="accent-sky-400"
                    />
                  </label>
                ))}
              </div>

              <div className="mt-6 flex items-center justify-between">
                {saved && (
                  <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1">
                    <CheckCircle2 className="h-4 w-4" /> Trajectory parameters saved!
                  </span>
                )}
                <MagneticButton variant="primary" onClick={handleSave} className="ml-auto">
                  <Save className="h-4 w-4" />
                  <span>Update Career Trajectory</span>
                </MagneticButton>
              </div>
            </GlassCard>

            {/* Verified Skills Cloud */}
            <GlassCard glowColor="emerald" className="p-6">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-base font-bold text-white">Verified Skills & Badges</h3>
                <Badge variant="verified">{user?.verified_skills?.length || 7} Verified</Badge>
              </div>
              <p className="text-xs text-slate-400 mb-4">
                Extracted via PyMuPDF resume parsing, CV/OCR marksheet analysis, and adaptive assessments.
              </p>

              <div className="flex flex-wrap gap-2">
                {(user?.verified_skills || ['Python', 'PyTorch', 'Linear Algebra', 'FastAPI', 'Docker', 'Git', 'CUDA']).map(
                  (skill) => (
                    <span
                      key={skill}
                      className="inline-flex items-center gap-1.5 rounded-xl border border-emerald-500/30 bg-emerald-500/10 px-3 py-1.5 text-xs font-semibold text-emerald-300"
                    >
                      <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />
                      {skill}
                    </span>
                  )
                )}
              </div>
            </GlassCard>
          </div>
        </div>
      </div>
    </div>
  );
};

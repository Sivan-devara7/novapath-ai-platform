import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import {
  FileCheck,
  Upload,
  AlertTriangle,
  CheckCircle2,
  TrendingUp,
  Sparkles,
  ArrowRight,
  Plus,
  RefreshCw,
  Award,
  FileText
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { api } from '../services/api';
import { GlassCard } from '../components/ui/GlassCard';
import { MagneticButton } from '../components/ui/MagneticButton';
import { Badge } from '../components/ui/Badge';
import { SkeletonLoader } from '../components/ui/SkeletonLoader';
import { ResumeAnalysisResponse } from '../types';

export const Resume: React.FC = () => {
  const [analysis, setAnalysis] = useState<ResumeAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [targetRole, setTargetRole] = useState('AI Engineer');
  const [addedSkills, setAddedSkills] = useState<string[]>([]);

  const fetchAnalysis = async (role = targetRole) => {
    setLoading(true);
    try {
      const data = await api.analyzeResume(undefined, role);
      setAnalysis(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalysis(targetRole);
  }, [targetRole]);

  const handleAddSkillToRoadmap = (skillName: string) => {
    setAddedSkills(prev => [...prev, skillName]);
    confetti({
      particleCount: 40,
      spread: 50,
      origin: { y: 0.7 }
    });
  };

  return (
    <div className="relative min-h-screen bg-[var(--bg-primary)] pb-20 pt-8 text-[var(--text-primary)] transition-colors duration-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Header & Role Switcher */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-[var(--border-subtle)] pb-6">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="verified">ATS Recruiter Intelligence Engine</Badge>
              <span className="text-xs text-slate-400">Benchmarked against Tier-1 Tech Job Specs</span>
            </div>
            <h1 className="mt-2 text-2xl sm:text-4xl font-extrabold text-white">
              Resume Intelligence & <span className="text-gradient">ATS Audit</span>
            </h1>
            <p className="mt-1 text-xs sm:text-sm text-slate-300">
              Live feedback on technical keyword density, impact quantification, and missing prerequisite skills.
            </p>
          </div>

          {/* Role Filter */}
          <div className="flex items-center gap-2 rounded-xl border border-white/[0.08] bg-slate-900/60 p-1">
            {['AI Engineer', 'Full Stack Developer', 'Cloud & DevOps Engineer'].map((role) => (
              <button
                key={role}
                onClick={() => setTargetRole(role)}
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-all ${
                  targetRole === role
                    ? 'bg-gradient-to-r from-sky-500 to-indigo-600 text-white shadow-neon-blue'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {role}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="mt-12 space-y-6">
            <SkeletonLoader lines={5} className="h-28" />
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <SkeletonLoader lines={3} className="h-40" />
              <SkeletonLoader lines={3} className="h-40" />
              <SkeletonLoader lines={3} className="h-40" />
            </div>
          </div>
        ) : analysis ? (
          <div className="mt-8 space-y-8">
            {/* Top Score Banner */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
              {/* Main Circular Score (4 cols) */}
              <GlassCard glowColor="blue" className="lg:col-span-4 p-8 flex flex-col items-center justify-center text-center">
                <div className="relative flex h-36 w-36 items-center justify-center">
                  {/* SVG circular track */}
                  <svg className="h-full w-full -rotate-90 transform" viewBox="0 0 100 100">
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      className="stroke-slate-800"
                      strokeWidth="8"
                      fill="transparent"
                    />
                    <circle
                      cx="50"
                      cy="50"
                      r="40"
                      className="stroke-sky-400 transition-all duration-1000 ease-out"
                      strokeWidth="8"
                      strokeDasharray={251.2}
                      strokeDashoffset={251.2 - (251.2 * analysis.ats_score) / 100}
                      strokeLinecap="round"
                      fill="transparent"
                    />
                  </svg>
                  <div className="absolute flex flex-col items-center">
                    <span className="text-4xl font-black text-white">{analysis.ats_score}</span>
                    <span className="text-[10px] uppercase font-bold text-sky-400">Out of 100</span>
                  </div>
                </div>

                <h3 className="mt-4 text-base font-bold text-white">Overall ATS Alignment</h3>
                <p className="mt-1 text-xs text-slate-300">
                  Targeted role: <strong className="text-sky-300">{targetRole}</strong>
                </p>
                <Badge variant="ats_high" className="mt-3">Top 12% Candidate Bracket</Badge>
              </GlassCard>

              {/* Score Breakdown (8 cols) */}
              <GlassCard glowColor="violet" className="lg:col-span-8 p-8 flex flex-col justify-between">
                <div>
                  <h3 className="text-base font-bold text-white">Dimensional Score Breakdown</h3>
                  <p className="text-xs text-slate-400 mt-0.5">Evaluated across recruiter parsing pipelines</p>

                  <div className="mt-6 space-y-4">
                    {/* Skills Match */}
                    <div>
                      <div className="flex justify-between text-xs font-semibold mb-1.5">
                        <span className="text-slate-300">Target Role Skill Coverage</span>
                        <span className="text-sky-400">{analysis.skills_match_score}%</span>
                      </div>
                      <div className="h-2.5 w-full rounded-full bg-slate-800 overflow-hidden">
                        <div
                          className="h-full bg-sky-400 rounded-full transition-all duration-700"
                          style={{ width: `${analysis.skills_match_score}%` }}
                        />
                      </div>
                    </div>

                    {/* Impact Metrics */}
                    <div>
                      <div className="flex justify-between text-xs font-semibold mb-1.5">
                        <span className="text-slate-300">Quantifiable Metrics & Latency Benchmarks</span>
                        <span className="text-violet-400">{analysis.impact_score}%</span>
                      </div>
                      <div className="h-2.5 w-full rounded-full bg-slate-800 overflow-hidden">
                        <div
                          className="h-full bg-violet-500 rounded-full transition-all duration-700"
                          style={{ width: `${analysis.impact_score}%` }}
                        />
                      </div>
                    </div>

                    {/* Formatting */}
                    <div>
                      <div className="flex justify-between text-xs font-semibold mb-1.5">
                        <span className="text-slate-300">Standard Parsing Section Structure</span>
                        <span className="text-emerald-400">{analysis.formatting_score}%</span>
                      </div>
                      <div className="h-2.5 w-full rounded-full bg-slate-800 overflow-hidden">
                        <div
                          className="h-full bg-emerald-400 rounded-full transition-all duration-700"
                          style={{ width: `${analysis.formatting_score}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-6 grid grid-cols-2 sm:grid-cols-4 gap-3 border-t border-white/[0.06] pt-4 text-xs">
                  <div>
                    <span className="text-slate-400 block">Action Verbs</span>
                    <strong className="text-white text-sm">{analysis.action_verb_count} Detected</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 block">Metrics Found</span>
                    <strong className="text-white text-sm">{analysis.quantifiable_metrics_count} Benchmarks</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 block">Matched Skills</span>
                    <strong className="text-sky-400 text-sm">{analysis.matched_skills.length} Skills</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 block">Critical Gaps</span>
                    <strong className="text-rose-400 text-sm">{analysis.missing_skills.length} Missing</strong>
                  </div>
                </div>
              </GlassCard>
            </div>

            {/* Gap Analysis & 1-Click "Add to Roadmap" Action */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Critical Missing Skills Gaps (6 cols) */}
              <GlassCard glowColor="amber" className="lg:col-span-6 p-6">
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="h-4 w-4 text-amber-400" />
                  <h3 className="text-base font-bold text-white">Identified Critical Skill Gaps</h3>
                </div>
                <p className="text-xs text-slate-300">
                  These missing competencies appear in &gt;75% of candidate requirements for <strong className="text-white">{targetRole}</strong>.
                </p>

                <div className="mt-4 space-y-3">
                  {analysis.missing_skills.map((skill) => {
                    const isAdded = addedSkills.includes(skill);
                    return (
                      <div
                        key={skill}
                        className="flex items-center justify-between rounded-xl border border-rose-500/20 bg-rose-950/10 p-3.5 backdrop-blur-md"
                      >
                        <div>
                          <span className="text-xs font-bold text-rose-300 block">{skill}</span>
                          <span className="text-[11px] text-slate-400">High search weight for recruiter filtering</span>
                        </div>

                        <MagneticButton
                          variant={isAdded ? 'secondary' : 'primary'}
                          onClick={() => handleAddSkillToRoadmap(skill)}
                          disabled={isAdded}
                          className="text-xs py-1.5 px-3"
                        >
                          {isAdded ? (
                            <>
                              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />
                              <span>Added to Roadmap</span>
                            </>
                          ) : (
                            <>
                              <Plus className="h-3.5 w-3.5" />
                              <span>Add to Roadmap</span>
                            </>
                          )}
                        </MagneticButton>
                      </div>
                    );
                  })}
                </div>
              </GlassCard>

              {/* Matched Verified Skills (6 cols) */}
              <GlassCard glowColor="emerald" className="lg:col-span-6 p-6">
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                  <h3 className="text-base font-bold text-white">Verified Matched Competencies</h3>
                </div>
                <p className="text-xs text-slate-300">
                  Successfully parsed and recognized by ATS keyword taxonomy.
                </p>

                <div className="mt-4 flex flex-wrap gap-2">
                  {analysis.matched_skills.map((skill) => (
                    <span
                      key={skill}
                      className="inline-flex items-center gap-1.5 rounded-lg border border-emerald-500/30 bg-emerald-500/10 px-3 py-1.5 text-xs font-medium text-emerald-300"
                    >
                      <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />
                      {skill}
                    </span>
                  ))}
                </div>

                {/* AI Executive Summary Critique */}
                <div className="mt-6 rounded-xl border border-white/[0.08] bg-slate-900/60 p-4">
                  <div className="flex items-center gap-1.5 text-xs font-bold text-sky-300 mb-1">
                    <Sparkles className="h-3.5 w-3.5" />
                    <span>AI Mentor Executive Critique:</span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    {analysis.summary_critique}
                  </p>
                </div>
              </GlassCard>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
};

import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Sparkles,
  ArrowRight,
  Brain,
  Compass,
  FileCheck,
  TrendingUp,
  Award,
  Terminal,
  Zap,
  CheckCircle,
  Play
} from 'lucide-react';
import { SkillGalaxyHero } from '../components/3d/SkillGalaxyHero';
import { GlassCard } from '../components/ui/GlassCard';
import { MagneticButton } from '../components/ui/MagneticButton';
import { Badge } from '../components/ui/Badge';

export const Landing: React.FC = () => {
  return (
    <div className="relative min-h-screen bg-[var(--bg-primary)] text-[var(--text-primary)] overflow-hidden transition-colors duration-300">
      {/* Background Lighting & Glow Orbs */}
      <div className="pointer-events-none absolute left-1/2 top-0 -translate-x-1/2 w-full max-w-7xl h-[600px] bg-hero-glow blur-3xl opacity-60" />
      <div className="pointer-events-none absolute -left-48 top-96 h-96 w-96 rounded-full bg-sky-600/10 blur-[128px]" />
      <div className="pointer-events-none absolute -right-48 top-1/2 h-96 w-96 rounded-full bg-violet-600/15 blur-[128px]" />

      {/* Hero Section */}
      <section className="relative mx-auto max-w-7xl px-4 pt-12 pb-20 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center text-center">
          {/* Top Pill */}
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="inline-flex items-center gap-2 rounded-full border border-sky-400/30 bg-sky-950/40 px-4 py-1.5 text-xs font-semibold text-sky-300 backdrop-blur-md shadow-[0_0_20px_rgba(56,189,248,0.2)]">
              <Sparkles className="h-3.5 w-3.5 text-sky-400 animate-spin" style={{ animationDuration: '8s' }} />
              <span>Next-Gen Student AI Academic Companion & Career Mentor</span>
              <span className="rounded-full bg-sky-400/20 px-2 py-0.5 text-[10px] text-sky-200">v1.0 Live</span>
            </div>
          </motion.div>

          {/* Main Hero Headline */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="mt-6 max-w-4xl text-4xl font-extrabold tracking-tight sm:text-6xl lg:text-7xl"
          >
            Bridge Your Degree with <br />
            <span className="text-gradient">Industry AI Superpowers</span>
          </motion.h1>

          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="mt-6 max-w-2xl text-base text-slate-300 sm:text-lg"
          >
            Synthesizes your academic coursework, OCR-verified certifications, and GitHub repositories into
            living adaptive roadmaps, RAG-grounded learning, and recruiter-grade ATS resume intelligence.
          </motion.p>

          {/* Action CTAs */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="mt-8 flex flex-wrap items-center justify-center gap-4"
          >
            <Link to="/onboarding">
              <MagneticButton variant="primary" className="text-base px-7 py-3.5 shadow-neon-blue">
                <span>Start Free Profiling</span>
                <ArrowRight className="h-4 w-4" />
              </MagneticButton>
            </Link>
            <Link to="/dashboard">
              <MagneticButton variant="secondary" className="text-base px-7 py-3.5 border-slate-700/80">
                <Play className="h-4 w-4 text-sky-400 fill-sky-400" />
                <span>Explore Live Demo</span>
              </MagneticButton>
            </Link>
          </motion.div>

          {/* Trust stats pill bar */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="mt-10 grid grid-cols-2 gap-4 sm:grid-cols-4 sm:gap-8 border-y border-white/[0.06] py-6 w-full max-w-4xl"
          >
            <div>
              <div className="text-2xl sm:text-3xl font-black text-white">98.4%</div>
              <div className="text-xs text-slate-400 mt-0.5">ATS Alignment Rate</div>
            </div>
            <div>
              <div className="text-2xl sm:text-3xl font-black text-sky-400">12,400+</div>
              <div className="text-xs text-slate-400 mt-0.5">RAG Grounded Resources</div>
            </div>
            <div>
              <div className="text-2xl sm:text-3xl font-black text-violet-400">60 FPS</div>
              <div className="text-xs text-slate-400 mt-0.5">3D Skill Galaxy Engine</div>
            </div>
            <div>
              <div className="text-2xl sm:text-3xl font-black text-emerald-400">0s Delay</div>
              <div className="text-xs text-slate-400 mt-0.5">Instant Adaptive Feedback</div>
            </div>
          </motion.div>
        </div>

        {/* Signature 3D Skill Galaxy Canvas */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          className="mt-14"
        >
          <SkillGalaxyHero />
        </motion.div>
      </section>

      {/* 6 Core Feature Modules Showcase */}
      <section className="relative mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto">
          <Badge variant="ready" className="mb-3">6 Core Modules Included</Badge>
          <h2 className="text-3xl font-extrabold sm:text-4xl text-white">
            Everything Required for <span className="text-gradient">Placement Supremacy</span>
          </h2>
          <p className="mt-3 text-slate-400 text-sm sm:text-base">
            Engineered specifically to fulfill all 6 competitive criteria with zero external API dependencies.
          </p>
        </div>

        <div className="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Card 1: Skill Profiling */}
          <GlassCard glowColor="blue" className="p-6">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-sky-500/10 border border-sky-400/30 text-sky-400 shadow-neon-blue">
              <Brain className="h-6 w-6" />
            </div>
            <h3 className="mt-4 text-lg font-bold text-white">1. Intelligent Skill Profiling</h3>
            <p className="mt-2 text-xs leading-relaxed text-slate-300">
              Drag-and-drop resume parser and certificate CV/OCR extraction pipeline. Instantly discovers proven competencies and creates verified student credential badges.
            </p>
            <div className="mt-4 flex flex-wrap gap-1.5">
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-sky-300">PyMuPDF</span>
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-sky-300">CV/OCR Pipeline</span>
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-sky-300">Auto-Taxonomy</span>
            </div>
          </GlassCard>

          {/* Card 2: Roadmap Generator */}
          <GlassCard glowColor="violet" className="p-6">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-violet-500/10 border border-violet-400/30 text-violet-400 shadow-neon-violet">
              <Compass className="h-6 w-6" />
            </div>
            <h3 className="mt-4 text-lg font-bold text-white">2. Interactive Adaptive Roadmap</h3>
            <p className="mt-2 text-xs leading-relaxed text-slate-300">
              Topological DAG generator mapping prerequisites, estimated milestone hours, and hands-on capstone projects tailored to your target career role.
            </p>
            <div className="mt-4 flex flex-wrap gap-1.5">
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-violet-300">Graph DAG</span>
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-violet-300">Prerequisite Trees</span>
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-violet-300">Dynamic Milestones</span>
            </div>
          </GlassCard>

          {/* Card 3: RAG Resource Recommender */}
          <GlassCard glowColor="emerald" className="p-6">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-500/10 border border-emerald-400/30 text-emerald-400">
              <Terminal className="h-6 w-6" />
            </div>
            <h3 className="mt-4 text-lg font-bold text-white">3. RAG Resource Recommender</h3>
            <p className="mt-2 text-xs leading-relaxed text-slate-300">
              Vector-retrieved curated study feed with provenance citations. Filter by video blitz, deep-dive research papers, or interactive coding sandboxes.
            </p>
            <div className="mt-4 flex flex-wrap gap-1.5">
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-emerald-300">Vector Search</span>
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-emerald-300">Grounded Citations</span>
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-emerald-300">Zero Hallucination</span>
            </div>
          </GlassCard>

          {/* Card 4: Adaptive Assessment */}
          <GlassCard glowColor="blue" className="p-6">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-sky-500/10 border border-sky-400/30 text-sky-400">
              <Award className="h-6 w-6" />
            </div>
            <h3 className="mt-4 text-lg font-bold text-white">4. Adaptive Assessment Engine</h3>
            <p className="mt-2 text-xs leading-relaxed text-slate-300">
              Real-time difficulty meter scaling dynamically from Easy to Expert based on consecutive precision, with code execution and instant conceptual debriefs.
            </p>
            <div className="mt-4 flex flex-wrap gap-1.5">
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-sky-300">Real-time Adaptation</span>
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-sky-300">Code Snippets</span>
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-sky-300">Instant XP Rewards</span>
            </div>
          </GlassCard>

          {/* Card 5: Resume Intelligence */}
          <GlassCard glowColor="violet" className="p-6">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-violet-500/10 border border-violet-400/30 text-violet-400">
              <FileCheck className="h-6 w-6" />
            </div>
            <h3 className="mt-4 text-lg font-bold text-white">5. Resume & ATS Intelligence</h3>
            <p className="mt-2 text-xs leading-relaxed text-slate-300">
              Comprehensive ATS score audit with impact metrics analyzer, keyword gap highlighter, and 1-click action to inject missing skills into your learning roadmap.
            </p>
            <div className="mt-4 flex flex-wrap gap-1.5">
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-violet-300">ATS Score Gauge</span>
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-violet-300">Impact Verbs</span>
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-violet-300">Gap Highlighter</span>
            </div>
          </GlassCard>

          {/* Card 6: Project & Cert Recommender */}
          <GlassCard glowColor="emerald" className="p-6">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-500/10 border border-emerald-400/30 text-emerald-400">
              <TrendingUp className="h-6 w-6" />
            </div>
            <h3 className="mt-4 text-lg font-bold text-white">6. Project & Cert Recommender</h3>
            <p className="mt-2 text-xs leading-relaxed text-slate-300">
              Curated capstone projects, industry-standard certifications (AWS, DeepLearning.AI), and matching internships with explainable "Why this matches" RAG cards.
            </p>
            <div className="mt-4 flex flex-wrap gap-1.5">
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-emerald-300">Explainable AI</span>
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-emerald-300">Portfolio Proof</span>
              <span className="rounded-md bg-slate-800/80 px-2 py-0.5 text-[10px] text-emerald-300">Internship Spec</span>
            </div>
          </GlassCard>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative mx-auto max-w-7xl px-4 py-20 sm:px-6 lg:px-8">
        <GlassCard glowColor="blue" className="relative p-10 md:p-14 text-center overflow-hidden">
          <div className="pointer-events-none absolute inset-0 bg-gradient-to-r from-sky-500/10 via-indigo-500/10 to-violet-500/10" />
          <h2 className="relative z-10 text-3xl sm:text-5xl font-extrabold text-white">
            Experience the Future of AI Mentorship
          </h2>
          <p className="relative z-10 mx-auto mt-4 max-w-xl text-slate-300 text-sm sm:text-base">
            One-click demonstration ready for judges and recruiters. Preloaded with Aarav Sharma's AI Engineer profile.
          </p>
          <div className="relative z-10 mt-8 flex flex-wrap justify-center gap-4">
            <Link to="/dashboard">
              <MagneticButton variant="primary" className="text-base px-8 py-3.5 shadow-neon-blue">
                Launch Live Platform Dashboard
              </MagneticButton>
            </Link>
            <Link to="/onboarding">
              <MagneticButton variant="secondary" className="text-base px-8 py-3.5">
                Upload Custom Resume
              </MagneticButton>
            </Link>
          </div>
        </GlassCard>
      </section>
    </div>
  );
};

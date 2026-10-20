import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Map,
  FileCheck,
  Sparkles,
  CheckCircle2,
  Lock,
  ArrowRight,
  TrendingUp,
  Brain,
  Award,
  Zap,
  Clock,
  Layers,
  ChevronRight,
  Bot,
  ExternalLink,
  ShieldCheck,
  Flame,
  Target
} from 'lucide-react';
import { GlassCard } from '../ui/GlassCard';
import { MagneticButton } from '../ui/MagneticButton';
import { Badge } from '../ui/Badge';
import { useLanguage } from '../../context/LanguageContext';

export const PlatformShowcase: React.FC = () => {
  const { t } = useLanguage();
  const [activeTab, setActiveTab] = useState<'roadmap' | 'ats' | 'mentor'>('roadmap');

  // Tab 1 (Roadmap) active selected node
  const [selectedMilestone, setSelectedMilestone] = useState<number>(1);

  // Tab 2 (ATS) selected role
  const [selectedRole, setSelectedRole] = useState<'AI Engineer' | 'Data Engineer' | 'Cybersecurity'>('AI Engineer');

  // Tab 3 (Mentor) active prompt demo
  const [activeMentorPrompt, setActiveMentorPrompt] = useState<number>(0);

  const milestones = [
    {
      id: 0,
      title: '01. Python & Applied Math Foundations',
      status: 'completed',
      mastery: 100,
      hours: 25,
      xp: 150,
      skills: ['Python 3.12', 'Linear Algebra', 'Calculus Optimization', 'Git Workflows'],
      desc: 'Mastery of matrix decomposition, gradients, tensor broadcasting, and deterministic Python coding standard.',
      capstone: 'Custom Autograd Engine from Scratch'
    },
    {
      id: 1,
      title: '02. PyTorch & Deep Neural Networks',
      status: 'in_progress',
      mastery: 74,
      hours: 35,
      xp: 250,
      skills: ['PyTorch Modules', 'Backpropagation', 'ViT Attention', 'Multi-GPU DDP'],
      desc: 'Deep architecture construction with multi-head self-attention mechanisms and mixed-precision gradient accumulation.',
      capstone: 'Vision Transformer (ViT) Classifier with >85% Top-1 Accuracy'
    },
    {
      id: 2,
      title: '03. Vector Databases & Hybrid RAG',
      status: 'ready',
      mastery: 0,
      hours: 20,
      xp: 200,
      skills: ['FAISS & Milvus', 'Dense Embeddings', 'Cross-Encoder Re-ranking', 'Chunking Strategy'],
      desc: 'Engineering high-accuracy retrieval systems with hybrid dense/sparse search, MMR diversification, and minimal hallucination.',
      capstone: 'Autonomous Technical PDF RAG Engine with Cross-Encoder'
    },
    {
      id: 3,
      title: '04. High-Throughput MLOps & TensorRT',
      status: 'locked',
      mastery: 0,
      hours: 40,
      xp: 300,
      skills: ['TensorRT FP16', 'Triton Server', 'Docker Containerization', 'Kubernetes Orchestration'],
      desc: 'Production inference optimization, FP16 quantization, microservice latency SLAs, and scalable Kubernetes pods.',
      capstone: 'Sub-15ms Real-Time Inference Microservice with Docker'
    }
  ];

  const currentMilestoneData = milestones[selectedMilestone];

  const roleAtsData = {
    'AI Engineer': {
      score: 84,
      extracted: ['PyTorch', 'FastAPI', 'Docker', 'CUDA', 'Python', 'Git', 'Linux'],
      missing: ['Vector Databases (Milvus/FAISS)', 'TensorRT FP16 Quantization', 'Distributed Model Serving'],
      bridgeSteps: [
        'Complete Vector Database & RAG module (+8% ATS match)',
        'Build sub-15ms TensorRT serving capstone (+5% ATS match)',
        'Pass Module 3 Verification Quiz (+50 XP)'
      ]
    },
    'Data Engineer': {
      score: 79,
      extracted: ['SQL Internals', 'Python', 'PostgreSQL', 'Docker', 'Git'],
      missing: ['Apache Spark Cluster Tuning', 'Kafka Event Streaming', 'Snowflake & dbt Modeling'],
      bridgeSteps: [
        'Complete Apache Spark ETL Pipelines module (+9% ATS match)',
        'Deploy Kafka streaming producer/consumer pipeline (+8% ATS match)',
        'Pass Data Engineering Placement Retake (+50 XP)'
      ]
    },
    'Cybersecurity': {
      score: 81,
      extracted: ['Linux Hardening', 'Python', 'Wireshark', 'TCP/IP', 'Git'],
      missing: ['SIEM Splunk / Elastic Rule Tuning', 'MITRE ATT&CK Matrix Mapping', 'Penetration Testing (Burp)'],
      bridgeSteps: [
        'Complete SOC Operations & Threat Hunting module (+10% ATS match)',
        'Simulate MITRE ATT&CK detection lab (+6% ATS match)',
        'Earn SOC Analyst Readiness Certification'
      ]
    }
  };

  const currentRoleAts = roleAtsData[selectedRole];

  const mentorDemos = [
    {
      chip: 'Critical Skill Gap Analysis',
      query: 'What is my top skill gap and how do I bridge it for AI Engineer roles?',
      response:
        'Hi Aarav! Based on your latest resume audit, your ATS alignment is 84%. Your most critical missing gap is Vector Databases & Hybrid RAG. Companies like NVIDIA and OpenAI prioritize candidates who understand dense vector indexing and latency-conscious retrieval. Starting Module 3 today will close this gap and raise your alignment to 92%+!'
    },
    {
      chip: 'Vision Transformer Concept',
      query: 'How does patch projection work in Vision Transformers (ViT)?',
      response:
        'In ViT, instead of standard convolution filters, we divide a 2D image into fixed patches (e.g., 16x16 pixels). Each patch is flattened into a 1D vector and multiplied by a trainable linear projection matrix to produce a token embedding of dimension D. We then prepend a learnable [CLS] token and add 1D positional embeddings before feeding it into standard Transformer Encoder blocks!'
    },
    {
      chip: 'Multilingual (తెలుగు / Hindi)',
      query: 'Explain RAG in Telugu & Hindi briefly',
      response:
        'నమస్కారం Aarav! RAG (Retrieval-Augmented Generation) అంటే మీ AI మోడల్ కేవలం అంతర్గత మెమరీపై ఆధారపడకుండా, వెక్టర్ డేటాబేస్ నుండి ఖచ్చితమైన డాక్యుమెంట్లను వెతికి నిజమైన సమాధానాలను రూపొందించడం.\n\nनमस्ते! RAG में मॉडल अपने आंतरिक ज्ञान के बजाय वेक्टर डेटाबेस से प्रासंगिक दस्तावेज़ खोजकर सटीक और बिना किसी भ्रांति (Zero-Hallucination) के उत्तर देता है।'
    }
  ];

  const openMentorDrawer = () => {
    window.dispatchEvent(new CustomEvent('open-ai-mentor'));
  };

  return (
    <div className="relative w-full max-w-6xl mx-auto mt-12 mb-16">
      {/* Decorative ambient glowing backdrops */}
      <div className="pointer-events-none absolute -inset-1 rounded-3xl bg-gradient-to-r from-sky-500/20 via-indigo-500/15 to-violet-500/20 blur-xl opacity-70" />

      {/* Main Glass Showcase Container */}
      <div className="relative rounded-3xl border border-white/[0.1] bg-slate-950/80 backdrop-blur-2xl shadow-2xl overflow-hidden">
        {/* Top Window Chrome Bar */}
        <div className="flex flex-wrap items-center justify-between border-b border-white/[0.07] px-5 py-3.5 bg-slate-900/60">
          <div className="flex items-center gap-2">
            <span className="h-3 w-3 rounded-full bg-rose-500/80 inline-block shadow-[0_0_8px_rgba(244,63,94,0.5)]" />
            <span className="h-3 w-3 rounded-full bg-amber-500/80 inline-block shadow-[0_0_8px_rgba(245,158,11,0.5)]" />
            <span className="h-3 w-3 rounded-full bg-emerald-500/80 inline-block shadow-[0_0_8px_rgba(16,185,129,0.5)]" />
            <span className="ml-3 text-xs font-semibold text-slate-400 hidden sm:inline">
              NovaPath Architecture Intelligence Core
            </span>
          </div>

          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 rounded-full border border-emerald-400/30 bg-emerald-500/10 px-3 py-1 text-[11px] font-semibold text-emerald-300">
              <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>OmniRoute AI Gateway • 100% Operational</span>
            </div>
          </div>
        </div>

        {/* Feature Selector Tabs */}
        <div className="flex border-b border-white/[0.06] bg-slate-900/40 p-2 gap-2 overflow-x-auto">
          <button
            onClick={() => setActiveTab('roadmap')}
            className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-xs font-bold transition-all whitespace-nowrap ${
              activeTab === 'roadmap'
                ? 'bg-sky-500/20 text-sky-300 border border-sky-400/40 shadow-neon-blue'
                : 'text-slate-400 hover:text-white hover:bg-white/[0.04]'
            }`}
          >
            <Map className="h-4 w-4 text-sky-400" />
            <span>1. Adaptive Learning Roadmap DAG</span>
            <span className="rounded-md bg-sky-400/15 px-1.5 py-0.5 text-[10px] text-sky-300">Live DAG</span>
          </button>

          <button
            onClick={() => setActiveTab('ats')}
            className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-xs font-bold transition-all whitespace-nowrap ${
              activeTab === 'ats'
                ? 'bg-violet-500/20 text-violet-300 border border-violet-400/40 shadow-neon-violet'
                : 'text-slate-400 hover:text-white hover:bg-white/[0.04]'
            }`}
          >
            <FileCheck className="h-4 w-4 text-violet-400" />
            <span>2. ATS Resume Audit & Bridge Engine</span>
            <span className="rounded-md bg-violet-400/15 px-1.5 py-0.5 text-[10px] text-violet-300">ML Scoring</span>
          </button>

          <button
            onClick={() => setActiveTab('mentor')}
            className={`flex items-center gap-2 rounded-xl px-4 py-2.5 text-xs font-bold transition-all whitespace-nowrap ${
              activeTab === 'mentor'
                ? 'bg-amber-500/20 text-amber-300 border border-amber-400/40 shadow-[0_0_15px_rgba(245,158,11,0.2)]'
                : 'text-slate-400 hover:text-white hover:bg-white/[0.04]'
            }`}
          >
            <Sparkles className="h-4 w-4 text-amber-400" />
            <span>3. OmniRoute Personalized AI Mentor</span>
            <span className="rounded-md bg-amber-400/15 px-1.5 py-0.5 text-[10px] text-amber-300">Multilingual</span>
          </button>
        </div>

        {/* Tab 1: Adaptive Learning Roadmap */}
        <AnimatePresence mode="wait">
          {activeTab === 'roadmap' && (
            <motion.div
              key="roadmap"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3 }}
              className="p-6 md:p-8"
            >
              <div className="flex flex-col lg:flex-row gap-6">
                {/* Left: 4 Interactive Pipeline Milestone Steps */}
                <div className="lg:w-7/12 space-y-3">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-400">
                      Curriculum Graph (Click any module to inspect)
                    </span>
                    <span className="text-xs text-sky-400 font-semibold">Track: AI Engineer</span>
                  </div>

                  {milestones.map((m, idx) => {
                    const isSelected = selectedMilestone === idx;
                    return (
                      <button
                        key={m.id}
                        onClick={() => setSelectedMilestone(idx)}
                        className={`w-full text-left rounded-2xl p-4 transition-all border flex items-center justify-between ${
                          isSelected
                            ? 'bg-slate-900/90 border-sky-400/50 shadow-[0_0_20px_rgba(56,189,248,0.2)] ring-1 ring-sky-400/30'
                            : 'bg-slate-900/40 border-white/[0.06] hover:bg-slate-900/70 hover:border-white/[0.12]'
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <div
                            className={`flex h-10 w-10 items-center justify-center rounded-xl font-bold text-sm ${
                              m.status === 'completed'
                                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                                : m.status === 'in_progress'
                                ? 'bg-sky-500/20 text-sky-400 border border-sky-500/40 animate-pulse'
                                : m.status === 'ready'
                                ? 'bg-violet-500/20 text-violet-400 border border-violet-500/30'
                                : 'bg-slate-800 text-slate-500 border border-slate-700'
                            }`}
                          >
                            {m.status === 'completed' ? (
                              <CheckCircle2 className="h-5 w-5" />
                            ) : m.status === 'locked' ? (
                              <Lock className="h-4 w-4" />
                            ) : (
                              <span>0{idx + 1}</span>
                            )}
                          </div>
                          <div>
                            <div className="text-sm font-extrabold text-white">{m.title}</div>
                            <div className="flex items-center gap-3 text-[11px] text-slate-400 mt-0.5">
                              <span>⏱ {m.hours} Hours</span>
                              <span>•</span>
                              <span>+{m.xp} XP</span>
                              <span>•</span>
                              <span className="text-slate-300 font-medium">Mastery: {m.mastery}%</span>
                            </div>
                          </div>
                        </div>

                        <div className="flex items-center gap-2">
                          {m.status === 'completed' && <Badge variant="verified">Mastered</Badge>}
                          {m.status === 'in_progress' && <Badge variant="in_progress">Active Focus</Badge>}
                          {m.status === 'ready' && <Badge variant="ready">Unlocked</Badge>}
                          {m.status === 'locked' && <Badge variant="locked">Locked</Badge>}
                          <ChevronRight
                            className={`h-4 w-4 transition-transform ${
                              isSelected ? 'text-sky-400 translate-x-1' : 'text-slate-500'
                            }`}
                          />
                        </div>
                      </button>
                    );
                  })}
                </div>

                {/* Right: Selected Milestone Detail Inspector Card */}
                <div className="lg:w-5/12 flex flex-col justify-between rounded-2xl border border-sky-400/20 bg-gradient-to-b from-slate-900/90 to-slate-950/90 p-6 shadow-xl">
                  <div>
                    <div className="flex items-center justify-between border-b border-white/[0.08] pb-3 mb-4">
                      <span className="text-xs font-bold text-sky-400 uppercase tracking-wide">
                        Inspecting Stage 0{selectedMilestone + 1}
                      </span>
                      <span className="rounded-full bg-sky-500/15 px-2.5 py-0.5 text-xs font-bold text-sky-300">
                        {currentMilestoneData.mastery}% Complete
                      </span>
                    </div>

                    <h3 className="text-lg font-black text-white">{currentMilestoneData.title}</h3>
                    <p className="mt-2 text-xs leading-relaxed text-slate-300">{currentMilestoneData.desc}</p>

                    <div className="mt-4">
                      <div className="text-xs font-bold uppercase text-slate-400 mb-2">Verified Competencies</div>
                      <div className="flex flex-wrap gap-1.5">
                        {currentMilestoneData.skills.map((skill) => (
                          <span
                            key={skill}
                            className="rounded-lg border border-sky-400/20 bg-sky-950/50 px-2.5 py-1 text-[11px] font-medium text-sky-300"
                          >
                            ✓ {skill}
                          </span>
                        ))}
                      </div>
                    </div>

                    <div className="mt-5 rounded-xl border border-white/[0.08] bg-slate-900/70 p-3.5">
                      <div className="flex items-center gap-1.5 text-xs font-bold text-amber-300">
                        <Award className="h-4 w-4" />
                        <span>Capstone Project</span>
                      </div>
                      <div className="mt-1 text-xs text-slate-300">{currentMilestoneData.capstone}</div>
                    </div>
                  </div>

                  <div className="mt-6 flex flex-col sm:flex-row gap-2.5 pt-4 border-t border-white/[0.08]">
                    <Link to="/roadmap" className="flex-1">
                      <MagneticButton variant="primary" className="w-full text-xs justify-center py-2.5 shadow-neon-blue">
                        <span>Open Full Curriculum</span>
                        <ArrowRight className="h-3.5 w-3.5" />
                      </MagneticButton>
                    </Link>
                    <Link to="/roadmap?placement=true">
                      <MagneticButton variant="secondary" className="text-xs justify-center py-2.5">
                        <span>Take Placement Quiz</span>
                      </MagneticButton>
                    </Link>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Tab 2: ATS Resume Intelligence */}
          {activeTab === 'ats' && (
            <motion.div
              key="ats"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3 }}
              className="p-6 md:p-8"
            >
              <div className="flex flex-col lg:flex-row items-center justify-between gap-6 border-b border-white/[0.06] pb-6 mb-6">
                <div>
                  <h3 className="text-xl font-black text-white">5-Component ML ATS Resume Engine</h3>
                  <p className="text-xs text-slate-300 mt-1">
                    Extracts keywords, audits structure, and deterministically scores role alignment with real-time bridge generation.
                  </p>
                </div>

                {/* Target Role Selector */}
                <div className="flex rounded-xl border border-white/[0.08] bg-slate-900/80 p-1">
                  {(['AI Engineer', 'Data Engineer', 'Cybersecurity'] as const).map((role) => (
                    <button
                      key={role}
                      onClick={() => setSelectedRole(role)}
                      className={`rounded-lg px-3 py-1.5 text-xs font-bold transition-all ${
                        selectedRole === role
                          ? 'bg-violet-600 text-white shadow-neon-violet'
                          : 'text-slate-400 hover:text-white'
                      }`}
                    >
                      {role}
                    </button>
                  ))}
                </div>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                {/* Left: ATS Gauge & Quick Metrics (4 cols) */}
                <div className="lg:col-span-4 rounded-2xl border border-violet-400/30 bg-violet-950/20 p-6 flex flex-col items-center justify-center text-center">
                  <div className="relative flex items-center justify-center h-36 w-36">
                    <svg className="h-full w-full -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="42" className="stroke-slate-800" strokeWidth="8" fill="none" />
                      <circle
                        cx="50"
                        cy="50"
                        r="42"
                        className="stroke-violet-400 transition-all duration-1000 ease-out"
                        strokeWidth="8"
                        strokeDasharray={264}
                        strokeDashoffset={264 - (264 * currentRoleAts.score) / 100}
                        strokeLinecap="round"
                        fill="none"
                      />
                    </svg>
                    <div className="absolute flex flex-col items-center">
                      <span className="text-4xl font-black text-white">{currentRoleAts.score}%</span>
                      <span className="text-[10px] uppercase font-bold text-violet-300">ATS Match</span>
                    </div>
                  </div>

                  <div className="mt-4 inline-flex items-center gap-1.5 rounded-full bg-violet-500/20 border border-violet-400/40 px-3 py-1 text-xs font-bold text-violet-200">
                    <Sparkles className="h-3.5 w-3.5" />
                    <span>Tier-1 Recruiter Ready</span>
                  </div>
                  <p className="text-[11px] text-slate-400 mt-2">Target Role: {selectedRole}</p>
                </div>

                {/* Center/Right: Extracted vs Missing Skills & Bridge Steps (8 cols) */}
                <div className="lg:col-span-8 space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Extracted Skills */}
                    <div className="rounded-2xl border border-emerald-500/20 bg-slate-900/60 p-4">
                      <div className="flex items-center gap-2 text-xs font-bold text-emerald-400 mb-2.5">
                        <CheckCircle2 className="h-4 w-4" />
                        <span>Verified Extracted Skills ({currentRoleAts.extracted.length})</span>
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {currentRoleAts.extracted.map((s) => (
                          <span
                            key={s}
                            className="rounded-md border border-emerald-500/30 bg-emerald-950/40 px-2 py-0.5 text-[11px] font-semibold text-emerald-300"
                          >
                            ✓ {s}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Missing Gaps */}
                    <div className="rounded-2xl border border-amber-500/20 bg-slate-900/60 p-4">
                      <div className="flex items-center gap-2 text-xs font-bold text-amber-400 mb-2.5">
                        <Target className="h-4 w-4" />
                        <span>Identified Critical Gaps ({currentRoleAts.missing.length})</span>
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {currentRoleAts.missing.map((s) => (
                          <span
                            key={s}
                            className="rounded-md border border-amber-500/30 bg-amber-950/40 px-2 py-0.5 text-[11px] font-semibold text-amber-300"
                          >
                            ! {s}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Bridge Recommendation Card */}
                  <div className="rounded-2xl border border-white/[0.08] bg-slate-900/70 p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2 text-xs font-bold text-sky-400">
                        <TrendingUp className="h-4 w-4" />
                        <span>Instant AI Bridge Action Roadmap</span>
                      </div>
                      <span className="text-[11px] text-slate-400">Accelerates score to 95%+</span>
                    </div>

                    <div className="space-y-1.5">
                      {currentRoleAts.bridgeSteps.map((step, i) => (
                        <div key={i} className="flex items-center gap-2 text-xs text-slate-300">
                          <span className="flex h-4 w-4 items-center justify-center rounded-full bg-sky-500/20 text-[10px] font-bold text-sky-400">
                            {i + 1}
                          </span>
                          <span>{step}</span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="flex justify-end gap-3 pt-2">
                    <Link to="/resume">
                      <MagneticButton variant="primary" className="text-xs px-5 py-2.5 shadow-neon-violet">
                        <span>Upload Your Resume to Audit</span>
                        <ArrowRight className="h-3.5 w-3.5" />
                      </MagneticButton>
                    </Link>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {/* Tab 3: OmniRoute AI Mentor */}
          {activeTab === 'mentor' && (
            <motion.div
              key="mentor"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3 }}
              className="p-6 md:p-8"
            >
              <div className="flex flex-col lg:flex-row gap-6">
                {/* Left: Context Summary */}
                <div className="lg:w-4/12 rounded-2xl border border-amber-400/20 bg-slate-900/60 p-5 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center gap-2 mb-3">
                      <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-amber-500/20 border border-amber-400/30 text-amber-400">
                        <Bot className="h-4 w-4" />
                      </div>
                      <div>
                        <div className="text-xs font-bold text-white">Student Context Awareness</div>
                        <div className="text-[10px] text-slate-400">Real-time DB metadata injected</div>
                      </div>
                    </div>

                    <div className="space-y-2 mt-4 text-xs">
                      <div className="flex items-center justify-between rounded-xl bg-slate-950/60 p-2.5 border border-white/[0.04]">
                        <span className="text-slate-400">Target Role</span>
                        <span className="font-bold text-white">AI Engineer</span>
                      </div>
                      <div className="flex items-center justify-between rounded-xl bg-slate-950/60 p-2.5 border border-white/[0.04]">
                        <span className="text-slate-400">Placement Level</span>
                        <span className="font-bold text-sky-400">Intermediate (68.5%)</span>
                      </div>
                      <div className="flex items-center justify-between rounded-xl bg-slate-950/60 p-2.5 border border-white/[0.04]">
                        <span className="text-slate-400">Learning Streak</span>
                        <span className="font-bold text-amber-400">🔥 14 Days</span>
                      </div>
                      <div className="flex items-center justify-between rounded-xl bg-slate-950/60 p-2.5 border border-white/[0.04]">
                        <span className="text-slate-400">Primary ATS Gap</span>
                        <span className="font-bold text-rose-400">Vector Databases</span>
                      </div>
                    </div>
                  </div>

                  <div className="mt-6 pt-4 border-t border-white/[0.08]">
                    <button
                      onClick={openMentorDrawer}
                      className="w-full flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-amber-500/20 to-orange-500/20 border border-amber-400/40 py-2.5 text-xs font-bold text-amber-300 hover:brightness-110 transition-all shadow-[0_0_15px_rgba(245,158,11,0.2)]"
                    >
                      <Sparkles className="h-3.5 w-3.5" />
                      <span>Launch Full Interactive Chat</span>
                    </button>
                  </div>
                </div>

                {/* Right: Interactive Terminal Simulator */}
                <div className="lg:w-8/12 flex flex-col rounded-2xl border border-white/[0.08] bg-slate-950/90 overflow-hidden">
                  {/* Prompt chips */}
                  <div className="flex flex-wrap gap-2 p-3.5 border-b border-white/[0.06] bg-slate-900/60">
                    <span className="text-xs font-bold text-slate-400 self-center mr-1">Try Prompts:</span>
                    {mentorDemos.map((demo, idx) => (
                      <button
                        key={idx}
                        onClick={() => setActiveMentorPrompt(idx)}
                        className={`rounded-lg px-2.5 py-1 text-xs font-medium transition-all ${
                          activeMentorPrompt === idx
                            ? 'bg-amber-400/20 text-amber-300 border border-amber-400/40'
                            : 'bg-slate-800/60 text-slate-400 hover:text-white'
                        }`}
                      >
                        {demo.chip}
                      </button>
                    ))}
                  </div>

                  {/* Chat dialog preview */}
                  <div className="p-5 space-y-4 flex-1">
                    {/* User Question */}
                    <div className="flex justify-end">
                      <div className="max-w-lg rounded-2xl bg-sky-600/25 border border-sky-400/30 px-4 py-2.5 text-xs text-sky-100">
                        {mentorDemos[activeMentorPrompt].query}
                      </div>
                    </div>

                    {/* AI Mentor Answer */}
                    <div className="flex items-start gap-3">
                      <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-amber-500/20 text-amber-300 border border-amber-400/30">
                        <Bot className="h-4 w-4" />
                      </div>
                      <div className="max-w-xl rounded-2xl bg-slate-900/90 border border-white/[0.08] p-4 text-xs leading-relaxed text-slate-200 whitespace-pre-line shadow-inner">
                        {mentorDemos[activeMentorPrompt].response}
                      </div>
                    </div>
                  </div>

                  <div className="p-3.5 border-t border-white/[0.06] bg-slate-900/40 flex items-center justify-between text-[11px] text-slate-400">
                    <span>⚡ Supports 7 Indian languages: English, हिन्दी, తెలుగు, தமிழ், ಕನ್ನಡ, বাংলা, मराठी</span>
                    <button
                      onClick={openMentorDrawer}
                      className="text-amber-400 hover:text-amber-300 font-semibold flex items-center gap-1"
                    >
                      Ask custom question <ArrowRight className="h-3 w-3" />
                    </button>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

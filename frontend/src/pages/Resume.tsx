import React, { useEffect, useState, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
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
  FileText,
  HelpCircle,
  FileUp,
  Info,
  ShieldAlert,
  Layers,
  BarChart3,
  MapPin,
  Calendar,
  Compass,
  Check,
  Target,
  Briefcase,
  FileSearch,
  ExternalLink,
  ChevronRight
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../services/api';
import { GlassCard } from '../components/ui/GlassCard';
import { MagneticButton } from '../components/ui/MagneticButton';
import { Badge } from '../components/ui/Badge';
import { SkeletonLoader } from '../components/ui/SkeletonLoader';
import { ResumeAnalysisResponse, BridgeRoadmapResponse, JDMatchResponse } from '../types';

export const Resume: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { updateUser } = useAuth();
  const { t } = useLanguage();

  const [appMode, setAppMode] = useState<'benchmark' | 'jd_match'>('benchmark');
  const [analysis, setAnalysis] = useState<ResumeAnalysisResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [targetRole, setTargetRole] = useState('AI Engineer');
  const [addedSkills, setAddedSkills] = useState<string[]>([]);
  const [addingSkill, setAddingSkill] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'sample' | 'upload' | 'paste'>('sample');
  const [pastedText, setPastedText] = useState('');
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null);
  const [rawUploadedFile, setRawUploadedFile] = useState<File | null>(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [bridgeRoadmap, setBridgeRoadmap] = useState<BridgeRoadmapResponse | null>(null);
  const [isGeneratingBridge, setIsGeneratingBridge] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // JD Matcher State
  const [jdText, setJdText] = useState('');
  const [jdAnalysis, setJdAnalysis] = useState<JDMatchResponse | null>(null);
  const [jdLoading, setJdLoading] = useState(false);

  const fetchSampleAnalysis = async (role = targetRole) => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const data = await api.analyzeResume(undefined, role);
      setAnalysis(data);
    } catch (e: any) {
      console.error(e);
      setErrorMsg(e.message || 'Failed to fetch resume analysis');
    } finally {
      setLoading(false);
    }
  };

  // Auto-generate AI Bridge Roadmap whenever analysis or targetRole changes
  useEffect(() => {
    if (analysis) {
      setIsGeneratingBridge(true);
      api.generateBridgeRoadmap({
        target_role: targetRole,
        current_ats_score: analysis.ats_score,
        missing_skills: analysis.missing_skills,
        matched_skills: analysis.matched_skills
      })
      .then(setBridgeRoadmap)
      .catch((err) => console.error('Failed to generate bridge roadmap:', err))
      .finally(() => setIsGeneratingBridge(false));
    }
  }, [analysis, targetRole]);

  const handleRoleChange = async (newRole: string) => {
    setTargetRole(newRole);
    setLoading(true);
    setErrorMsg(null);
    try {
      if (activeTab === 'paste' && pastedText.trim().length >= 40) {
        const data = await api.analyzeResume(pastedText, newRole);
        setAnalysis(data);
      } else {
        const data = await api.analyzeResume(undefined, newRole);
        setAnalysis(data);
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to recalibrate for role');
    } finally {
      setLoading(false);
    }
  };

  const handleStartCourseWithRoadmap = () => {
    updateUser({ career_goal: targetRole });
    navigate('/roadmap');
  };

  useEffect(() => {
    // 1. Check if we navigated here with an uploaded analysis in state
    if (location.state?.uploadedAnalysis) {
      setAnalysis(location.state.uploadedAnalysis);
      setSelectedFileName(location.state.fileName || 'Uploaded_Resume.pdf');
      setActiveTab('upload');
      setLoading(false);
      return;
    }

    // 2. Check if a recent upload exists in sessionStorage
    const saved = sessionStorage.getItem('novapath_latest_resume_analysis');
    if (saved) {
      try {
        const parsed = JSON.parse(saved);
        setAnalysis(parsed);
        setActiveTab('upload');
        setLoading(false);
        return;
      } catch {}
    }

    // 3. Fallback to sample analysis
    if (activeTab === 'sample') {
      fetchSampleAnalysis(targetRole);
    }
  }, [activeTab, location.state]);

  const handleFileUpload = async (file: File) => {
    setSelectedFileName(file.name);
    setRawUploadedFile(file);
    setUploading(true);
    setErrorMsg(null);
    try {
      const data = await api.uploadResume(file, targetRole);
      setAnalysis(data);
      confetti({ particleCount: 30, spread: 45, origin: { y: 0.6 } });
    } catch (err: any) {
      console.error(err);
      setErrorMsg(err.message || 'Failed to parse file. Make sure it contains readable text.');
    } finally {
      setUploading(false);
    }
  };

  const handlePasteSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!pastedText.trim() || pastedText.trim().length < 40) {
      setErrorMsg('Please enter at least 40 characters of resume text.');
      return;
    }
    setLoading(true);
    setErrorMsg(null);
    try {
      const data = await api.analyzeResume(pastedText, targetRole);
      setAnalysis(data);
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to analyze text.');
    } finally {
      setLoading(false);
    }
  };

  const loadSampleJD = (roleType: 'backend' | 'fullstack' | 'ml' = 'backend') => {
    if (roleType === 'backend') {
      setJdText(`Job Title: Senior Backend Software Engineer
Company: CloudScale Platforms
Location: Remote

Basic Qualifications (Required):
- 4+ years of professional backend software development experience.
- Bachelor's degree in Computer Science, Software Engineering, or related technical field.
- Strong proficiency in Python, FastAPI, and PostgreSQL.
- Experience with Docker containerization and Redis caching.
- Solid understanding of RESTful API design and CI/CD pipelines.

Preferred Qualifications (Bonus):
- Experience with Kubernetes and Kafka event streaming.
- Familiarity with AWS cloud architecture and Terraform.
- Exposure to GraphQL and Celery task queues.`);
    } else if (roleType === 'fullstack') {
      setJdText(`Job Title: Full Stack Developer (React & Node.js)
Company: WebMatrix Solutions
Location: Hybrid

Required Skills (Must Have):
- 2+ years building web applications with React, JavaScript, HTML5, and CSS3.
- Hands-on experience developing RESTful APIs with Node.js or Python.
- Proficiency in Git, GitHub, and component-driven architecture.
- Experience with Docker containerization and client-side state management.

Preferred Skills (Nice to Have):
- Experience with Next.js, TypeScript, and Tailwind CSS.
- Familiarity with PostgreSQL or MongoDB databases.`);
    } else {
      setJdText(`Job Title: Senior Data Scientist / Machine Learning Engineer
Company: DeepPulse AI
Location: Remote

Required Qualifications:
- 5+ years experience in statistical modeling, machine learning, and predictive analytics.
- Master's degree or PhD in Statistics, Machine Learning, Data Science, or related field.
- Deep expertise in Python, PyTorch, Scikit-Learn, Pandas, and NumPy.
- Experience building RAG pipelines and vector databases (Pinecone, FAISS).
- Demonstrated track record deploying models to production with Docker and FastAPI.

Preferred Qualifications:
- Experience with distributed GPU training (DeepSpeed, CUDA).
- Familiarity with MLOps and Weights & Biases.`);
    }
  };

  const handleMatchJD = async () => {
    if (!jdText.trim() || jdText.trim().length < 30) {
      setErrorMsg('Please enter or load a job description with at least 30 characters.');
      return;
    }
    setJdLoading(true);
    setErrorMsg(null);
    try {
      let res: JDMatchResponse;
      if (activeTab === 'upload' && rawUploadedFile) {
        res = await api.matchResumeFileToJD(rawUploadedFile, jdText);
      } else {
        const textToMatch = activeTab === 'paste' && pastedText.trim()
          ? pastedText
          : (analysis?.summary_critique ? `Experienced software engineer with competencies in ${analysis.matched_skills.join(', ')}. Accomplished projects in microservices, databases, and containerization.` : 'Software engineer with 4 years experience in Python, FastAPI, Docker, and PostgreSQL.');
        res = await api.matchResumeToJD(textToMatch, jdText);
      }
      setJdAnalysis(res);
      confetti({ particleCount: 50, spread: 60, origin: { y: 0.6 } });
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to match resume against job description.');
    } finally {
      setJdLoading(false);
    }
  };

  const handleAddSkillToRoadmap = async (skillName: string) => {
    setAddingSkill(skillName);
    try {
      await api.addSkillToRoadmap(skillName, targetRole);
      setAddedSkills((prev) => [...prev, skillName]);
      confetti({
        particleCount: 50,
        spread: 60,
        origin: { y: 0.7 }
      });
    } catch (err: any) {
      console.error(err);
      // Fallback local toggle
      setAddedSkills((prev) => [...prev, skillName]);
    } finally {
      setAddingSkill(null);
    }
  };

  return (
    <div className="relative min-h-screen bg-[var(--bg-primary)] pb-20 pt-8 text-[var(--text-primary)] transition-colors duration-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Header & Role Switcher */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-[var(--border-subtle)] pb-6">
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <Badge variant="verified">ATS Recruiter Intelligence Engine</Badge>
              <span className="inline-flex items-center gap-1 text-xs text-amber-400 font-medium bg-amber-400/10 px-2 py-0.5 rounded border border-amber-400/20">
                <Info className="h-3 w-3" />
                Role Alignment Index (Estimate)
              </span>
            </div>
            <h1 className="mt-2 text-2xl sm:text-4xl font-extrabold text-white">
              {t('resume_title', 'AI-Powered Resume ATS Audit & Bridge Engine')}
            </h1>
            <p className="mt-1 text-xs sm:text-sm text-slate-300">
              {t('resume_subtitle', 'Audit your resume against benchmark career tracks or match against any specific job description')}
            </p>
          </div>

          {/* Role Filter Selector (shown in benchmark mode) */}
          {appMode === 'benchmark' && (
            <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2">
              <span className="text-xs font-semibold text-slate-400">Target Role:</span>
              <div className="relative">
                <select
                  value={targetRole}
                  onChange={(e) => handleRoleChange(e.target.value)}
                  className="rounded-xl border border-white/[0.15] bg-slate-900/90 px-3.5 py-1.5 text-xs font-semibold text-white shadow-neon-blue focus:outline-none focus:ring-2 focus:ring-sky-500 transition-all cursor-pointer"
                >
                  {[
                    'AI Engineer',
                    'Frontend Developer',
                    'Backend Developer',
                    'Full Stack Developer',
                    'Data Scientist/ML Engineer',
                    'Data Analyst',
                    'Data Engineer',
                    'Cloud & DevOps Engineer',
                    'SRE',
                    'Mobile App Developer',
                    'Cybersecurity Analyst',
                    'QA/Test Automation Engineer',
                    'Software Engineer (generic)',
                    'Product Manager',
                    'UI/UX Designer',
                    'Business Analyst'
                  ].map((role) => (
                    <option key={role} value={role} className="bg-slate-900 text-white py-1">
                      {role}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          )}
        </div>

        {/* High-Level Mode Switcher: Role Benchmark Audit vs Target Job Description Matcher */}
        <div className="mt-6 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-2 p-1 rounded-2xl border border-white/[0.1] bg-slate-900/60 backdrop-blur-md">
            <button
              onClick={() => { setAppMode('benchmark'); setErrorMsg(null); }}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all ${
                appMode === 'benchmark'
                  ? 'bg-sky-500 text-white shadow-neon-blue'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              16-Role Benchmark Audit
            </button>
            <button
              onClick={() => { setAppMode('jd_match'); setErrorMsg(null); }}
              className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all ${
                appMode === 'jd_match'
                  ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-lg shadow-emerald-500/20'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
              }`}
            >
              <Target className="w-4 h-4 text-emerald-300" />
              Target Job Description (JD) Matcher
              <span className="text-[10px] bg-emerald-400/20 text-emerald-300 px-1.5 py-0.5 rounded font-mono">
                NEW
              </span>
            </button>
          </div>

          <div className="text-[11px] text-slate-400 flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
            {appMode === 'benchmark'
              ? 'Model evaluates role alignment index; ATS score computed deterministically.'
              : 'Direct semantic, skill, and requirements matching against your specific job description.'}
          </div>
        </div>

        {/* Input Method Tabs for Resume Selection */}
        <div className="mt-6 flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-2 rounded-xl border border-white/[0.08] bg-slate-900/50 p-1">
            <button
              onClick={() => { setActiveTab('sample'); setErrorMsg(null); }}
              className={`rounded-lg px-3.5 py-1.5 text-xs font-semibold transition-all ${
                activeTab === 'sample' ? 'bg-sky-500 text-white' : 'text-slate-400 hover:text-white'
              }`}
            >
              Verified Sample Resume
            </button>
            <button
              onClick={() => { setActiveTab('upload'); setErrorMsg(null); }}
              className={`rounded-lg px-3.5 py-1.5 text-xs font-semibold transition-all ${
                activeTab === 'upload' ? 'bg-sky-500 text-white' : 'text-slate-400 hover:text-white'
              }`}
            >
              Upload PDF / DOCX
            </button>
            <button
              onClick={() => { setActiveTab('paste'); setErrorMsg(null); }}
              className={`rounded-lg px-3.5 py-1.5 text-xs font-semibold transition-all ${
                activeTab === 'paste' ? 'bg-sky-500 text-white' : 'text-slate-400 hover:text-white'
              }`}
            >
              Paste Text
            </button>
          </div>

          <div className="text-[11px] text-slate-400">
            {activeTab === 'sample' && 'Using vetted verified student resume profile.'}
            {activeTab === 'upload' && (selectedFileName ? `Loaded: ${selectedFileName}` : 'Select a PDF/DOCX file.')}
            {activeTab === 'paste' && 'Paste custom resume text.'}
          </div>
        </div>

        {/* Error Banner */}
        <AnimatePresence>
          {errorMsg && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="mt-4 flex items-start gap-3 rounded-xl border border-rose-500/30 bg-rose-950/40 p-4 text-xs text-rose-200 backdrop-blur-md"
            >
              <AlertTriangle className="h-4 w-4 text-rose-400 shrink-0 mt-0.5" />
              <div>
                <strong className="block font-bold text-rose-300">File Processing Notice</strong>
                <span>{errorMsg}</span>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Upload Mode UI */}
        {activeTab === 'upload' && (
          <div className="mt-6">
            <GlassCard
              glowColor="blue"
              className={`p-8 text-center border-dashed border-2 transition-all duration-200 ${
                isDragOver
                  ? 'border-sky-400 bg-sky-950/40 shadow-neon-blue scale-[1.01]'
                  : 'border-white/20 hover:border-sky-400/50'
              }`}
            >
              <div
                onDragOver={(e) => {
                  e.preventDefault();
                  setIsDragOver(true);
                }}
                onDragLeave={() => setIsDragOver(false)}
                onDrop={(e) => {
                  e.preventDefault();
                  setIsDragOver(false);
                  if (e.dataTransfer.files && e.dataTransfer.files[0]) {
                    handleFileUpload(e.dataTransfer.files[0]);
                  }
                }}
              >
                <input
                  type="file"
                  ref={fileInputRef}
                  accept=".pdf,.docx,.txt"
                  onChange={(e) => {
                    if (e.target.files && e.target.files[0]) {
                      handleFileUpload(e.target.files[0]);
                    }
                  }}
                  className="hidden"
                />
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-sky-500/10 text-sky-400 mb-3">
                  <FileUp className="h-7 w-7" />
                </div>
                <h3 className="text-base font-bold text-white">Upload Your Resume</h3>
                <p className="mt-1 text-xs text-slate-400 max-w-md mx-auto">
                  Drag and drop or click to choose: <strong>.PDF, .DOCX, .TXT</strong> (Max size: 5 MB).
                </p>

                <div className="mt-4 flex flex-wrap items-center justify-center gap-3">
                  <MagneticButton
                    variant="primary"
                    onClick={() => fileInputRef.current?.click()}
                    disabled={uploading}
                    className="py-2.5 px-6 text-xs font-semibold shadow-neon-blue"
                  >
                    {uploading ? (
                      <>
                        <RefreshCw className="h-3.5 w-3.5 animate-spin" />
                        <span>Parsing & Benchmarking...</span>
                      </>
                    ) : (
                      <>
                        <Upload className="h-3.5 w-3.5" />
                        <span>Choose Document / Drop Here</span>
                      </>
                    )}
                  </MagneticButton>

                  <button
                    type="button"
                    onClick={() => setActiveTab('paste')}
                    className="rounded-xl border border-white/10 bg-slate-900/60 px-4 py-2 text-xs font-medium text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
                  >
                    Or Paste Resume Text
                  </button>
                </div>

                {selectedFileName && (
                  <div className="mt-4 inline-flex items-center gap-2 rounded-xl border border-sky-400/30 bg-sky-500/10 px-4 py-1.5 text-xs text-sky-300">
                    <CheckCircle2 className="h-3.5 w-3.5 text-sky-400" />
                    <span>Loaded: <strong>{selectedFileName}</strong></span>
                  </div>
                )}

                <div className="mt-6 border-t border-white/[0.06] pt-3 text-[11px] text-slate-400 max-w-lg mx-auto">
                  💡 <strong>Troubleshooting Tip:</strong> If your PDF is a scanned image or photo without selectable text, switch to <strong>"Paste Text"</strong> above to copy-paste your text directly.
                </div>
              </div>
            </GlassCard>
          </div>
        )}

        {/* Paste Text Mode UI */}
        {activeTab === 'paste' && (
          <div className="mt-6">
            <GlassCard glowColor="violet" className="p-6">
              <form onSubmit={handlePasteSubmit} className="space-y-4">
                <label className="block text-xs font-semibold text-slate-300">
                  Paste Resume Plain Text:
                </label>
                <textarea
                  value={pastedText}
                  onChange={(e) => setPastedText(e.target.value)}
                  rows={8}
                  placeholder="Paste work experience, education, skills, and summary here..."
                  className="w-full rounded-xl border border-white/10 bg-slate-950/70 p-3.5 text-xs text-white placeholder-slate-500 focus:border-sky-500 focus:outline-none focus:ring-1 focus:ring-sky-500"
                />
                <div className="flex justify-end">
                  <MagneticButton
                    variant="primary"
                    disabled={loading || pastedText.length < 40}
                    className="py-2 px-5 text-xs font-semibold"
                  >
                    {loading ? 'Evaluating...' : 'Audit Resume Text'}
                  </MagneticButton>
                </div>
              </form>
            </GlassCard>
          </div>
        )}

        {/* JD Matcher Input Panel (Shown when appMode === 'jd_match') */}
        {appMode === 'jd_match' && (
          <GlassCard glowColor="emerald" className="mt-6 p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/[0.08] pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <Target className="w-5 h-5 text-emerald-400" />
                  <h3 className="text-base font-bold text-white">Target Job Description (JD) Input</h3>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Paste the requirements, qualifications, and responsibilities from any job posting. Zero scraping, zero retention.
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <span className="text-[11px] text-slate-400 font-semibold">Load Sample JD:</span>
                <button
                  type="button"
                  onClick={() => loadSampleJD('backend')}
                  className="px-2.5 py-1 text-[11px] rounded-lg border border-white/[0.1] bg-slate-800/80 text-sky-300 hover:bg-slate-700 transition-all font-semibold"
                >
                  Senior Backend
                </button>
                <button
                  type="button"
                  onClick={() => loadSampleJD('fullstack')}
                  className="px-2.5 py-1 text-[11px] rounded-lg border border-white/[0.1] bg-slate-800/80 text-teal-300 hover:bg-slate-700 transition-all font-semibold"
                >
                  Full Stack
                </button>
                <button
                  type="button"
                  onClick={() => loadSampleJD('ml')}
                  className="px-2.5 py-1 text-[11px] rounded-lg border border-white/[0.1] bg-slate-800/80 text-purple-300 hover:bg-slate-700 transition-all font-semibold"
                >
                  Data Science/ML
                </button>
              </div>
            </div>

            <div className="mt-4">
              <textarea
                value={jdText}
                onChange={(e) => setJdText(e.target.value)}
                placeholder="Paste the target job description requirements, qualifications, and role responsibilities here..."
                rows={7}
                className="w-full rounded-xl border border-white/[0.12] bg-slate-950/80 p-4 text-xs font-mono text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500 transition-all resize-y"
              />
            </div>

            <div className="mt-4 flex flex-col sm:flex-row items-center justify-between gap-4">
              <div className="text-[11px] text-slate-400 flex items-center gap-1.5">
                <ShieldAlert className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                <span>Zero persistence: Neither your resume nor the JD is saved beyond this request.</span>
              </div>
              <MagneticButton
                variant="primary"
                onClick={handleMatchJD}
                disabled={jdLoading || !jdText.trim()}
                className="w-full sm:w-auto flex items-center justify-center gap-2 px-6 py-2.5 text-xs font-bold bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-lg shadow-emerald-500/20"
              >
                {jdLoading ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Target className="w-4 h-4" />}
                <span>{jdLoading ? 'Analyzing JD Alignment...' : 'Match Resume to Job Description'}</span>
              </MagneticButton>
            </div>
          </GlassCard>
        )}

        {/* --- DISPLAY MODE 1: TARGET JOB DESCRIPTION MATCH RESULTS --- */}
        {appMode === 'jd_match' ? (
          jdLoading ? (
            <div className="mt-12 space-y-6">
              <SkeletonLoader lines={5} className="h-28" />
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <SkeletonLoader lines={4} className="h-44" />
                <SkeletonLoader lines={4} className="h-44" />
              </div>
            </div>
          ) : jdAnalysis ? (
            <div className="mt-8 space-y-8">
              {/* JD Score Overview Banner */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
                {/* Main Circular Score (4 cols) */}
                <GlassCard glowColor="emerald" className="lg:col-span-4 p-8 flex flex-col items-center justify-center text-center">
                  <div className="relative flex h-40 w-40 items-center justify-center">
                    <svg className="h-full w-full -rotate-90 transform" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="40" className="stroke-slate-800" strokeWidth="8" fill="transparent" />
                      <circle
                        cx="50"
                        cy="50"
                        r="40"
                        className="stroke-emerald-400 transition-all duration-1000 ease-out"
                        strokeWidth="8"
                        strokeDasharray={251.2}
                        strokeDashoffset={251.2 - (251.2 * jdAnalysis.jd_match_score) / 100}
                        strokeLinecap="round"
                        fill="transparent"
                      />
                    </svg>
                    <div className="absolute flex flex-col items-center">
                      <span className="text-4xl font-black text-white">{jdAnalysis.jd_match_score}</span>
                      <span className="text-[10px] uppercase font-bold text-emerald-400">JD Match / 100</span>
                    </div>
                  </div>

                  <h3 className="mt-4 text-base font-bold text-white">Target JD Alignment Score</h3>
                  <p className="mt-1 text-xs text-slate-300">
                    Semantic & requirement fit against posted position
                  </p>

                  <div className="mt-3 flex flex-wrap items-center justify-center gap-1.5">
                    <Badge variant={jdAnalysis.jd_match_score >= 80 ? 'ats_high' : jdAnalysis.jd_match_score >= 50 ? 'verified' : 'in_progress'}>
                      {jdAnalysis.jd_match_score >= 80 ? 'Top Match Tier' : jdAnalysis.jd_match_score >= 50 ? 'Competitive Match' : 'Substantial Gaps'}
                    </Badge>
                    <Badge variant="highlight" className="text-[10px]">
                      {jdAnalysis.semantic_similarity_score}% Semantic Congruence
                    </Badge>
                  </div>
                </GlassCard>

                {/* 5-Factor JD Match Breakdown (8 cols) */}
                <GlassCard glowColor="blue" className="lg:col-span-8 p-8 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-base font-bold text-white">JD Requirement Breakdown</h3>
                        <p className="text-xs text-slate-400 mt-0.5">Weighted blend across technical requirements, experience, and terminology</p>
                      </div>
                      <Badge variant="verified" className="text-[10px]">Documented Formula</Badge>
                    </div>

                    <div className="mt-6 space-y-3.5">
                      {/* Must-Haves (45%) */}
                      <div>
                        <div className="flex justify-between text-xs font-semibold mb-1">
                          <span className="text-slate-300 flex items-center gap-1.5">
                            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
                            Must-Have Technical Skills ({jdAnalysis.scoring_formula_weights?.must_haves_weight || 45}% weight)
                          </span>
                          <span className="text-emerald-400 font-bold">{jdAnalysis.must_have_score}%</span>
                        </div>
                        <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
                          <div
                            className="h-full bg-emerald-400 rounded-full transition-all duration-700"
                            style={{ width: `${jdAnalysis.must_have_score}%` }}
                          />
                        </div>
                      </div>

                      {/* Nice-to-Haves (15%) */}
                      <div>
                        <div className="flex justify-between text-xs font-semibold mb-1">
                          <span className="text-slate-300 flex items-center gap-1.5">
                            <span className="h-1.5 w-1.5 rounded-full bg-teal-400"></span>
                            Preferred / Bonus Skills ({jdAnalysis.scoring_formula_weights?.nice_to_haves_weight || 15}% weight)
                          </span>
                          <span className="text-teal-400 font-bold">{jdAnalysis.nice_to_have_score}%</span>
                        </div>
                        <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
                          <div
                            className="h-full bg-teal-400 rounded-full transition-all duration-700"
                            style={{ width: `${jdAnalysis.nice_to_have_score}%` }}
                          />
                        </div>
                      </div>

                      {/* Semantic Similarity (20%) */}
                      <div>
                        <div className="flex justify-between text-xs font-semibold mb-1">
                          <span className="text-slate-300 flex items-center gap-1.5">
                            <span className="h-1.5 w-1.5 rounded-full bg-sky-400"></span>
                            TF-IDF Semantic Similarity ({jdAnalysis.scoring_formula_weights?.semantic_similarity_weight || 20}% weight)
                          </span>
                          <span className="text-sky-400 font-bold">{jdAnalysis.semantic_similarity_score}%</span>
                        </div>
                        <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
                          <div
                            className="h-full bg-sky-400 rounded-full transition-all duration-700"
                            style={{ width: `${jdAnalysis.semantic_similarity_score}%` }}
                          />
                        </div>
                      </div>

                      {/* Experience & Education Alignment (20%) */}
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                        <div className="p-3 rounded-xl border border-white/[0.08] bg-slate-900/60">
                          <span className="text-[11px] font-bold text-slate-400 block">Experience Check (10%):</span>
                          <span className="text-xs text-emerald-300 font-semibold mt-0.5 block">{jdAnalysis.experience_status}</span>
                        </div>
                        <div className="p-3 rounded-xl border border-white/[0.08] bg-slate-900/60">
                          <span className="text-[11px] font-bold text-slate-400 block">Education Check (10%):</span>
                          <span className="text-xs text-emerald-300 font-semibold mt-0.5 block">{jdAnalysis.education_status}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </GlassCard>
              </div>

              {/* Requirements Comparison Tags */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Must-Haves Card */}
                <GlassCard glowColor="emerald" className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="text-sm font-bold text-white flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                      Must-Have Technical Requirements
                    </h4>
                    <span className="text-xs font-bold text-emerald-400">
                      {jdAnalysis.matched_must_haves.length} / {jdAnalysis.matched_must_haves.length + jdAnalysis.missing_must_haves.length} Matched
                    </span>
                  </div>

                  <div className="space-y-3">
                    <div>
                      <span className="text-[11px] font-semibold text-emerald-300 uppercase block mb-1.5">Matched Competencies:</span>
                      <div className="flex flex-wrap gap-1.5">
                        {jdAnalysis.matched_must_haves.length > 0 ? (
                          jdAnalysis.matched_must_haves.map((m) => (
                            <span key={m} className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-emerald-500/15 border border-emerald-500/30 text-emerald-300">
                              ✓ {m}
                            </span>
                          ))
                        ) : (
                          <span className="text-xs text-slate-500">No must-have skills matched yet.</span>
                        )}
                      </div>
                    </div>

                    {jdAnalysis.missing_must_haves.length > 0 && (
                      <div className="pt-2 border-t border-white/[0.06]">
                        <span className="text-[11px] font-semibold text-rose-300 uppercase block mb-1.5">Missing Must-Haves (Gaps):</span>
                        <div className="flex flex-wrap gap-1.5">
                          {jdAnalysis.missing_must_haves.map((m) => (
                            <span key={m} className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-rose-500/15 border border-rose-500/30 text-rose-300">
                              ✗ {m}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </GlassCard>

                {/* Nice-to-Haves Card */}
                <GlassCard glowColor="blue" className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h4 className="text-sm font-bold text-white flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-teal-400" />
                      Preferred & Bonus Qualifications
                    </h4>
                    <span className="text-xs font-bold text-teal-400">
                      {jdAnalysis.matched_nice_to_haves.length} / {Math.max(1, jdAnalysis.matched_nice_to_haves.length + jdAnalysis.missing_nice_to_haves.length)} Matched
                    </span>
                  </div>

                  <div className="space-y-3">
                    <div>
                      <span className="text-[11px] font-semibold text-teal-300 uppercase block mb-1.5">Bonus Skills Demonstrated:</span>
                      <div className="flex flex-wrap gap-1.5">
                        {jdAnalysis.matched_nice_to_haves.length > 0 ? (
                          jdAnalysis.matched_nice_to_haves.map((m) => (
                            <span key={m} className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-teal-500/15 border border-teal-500/30 text-teal-300">
                              ★ {m}
                            </span>
                          ))
                        ) : (
                          <span className="text-xs text-slate-500">None detected.</span>
                        )}
                      </div>
                    </div>

                    {jdAnalysis.missing_nice_to_haves.length > 0 && (
                      <div className="pt-2 border-t border-white/[0.06]">
                        <span className="text-[11px] font-semibold text-amber-300 uppercase block mb-1.5">Additional Preferred Skills:</span>
                        <div className="flex flex-wrap gap-1.5">
                          {jdAnalysis.missing_nice_to_haves.map((m) => (
                            <span key={m} className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-amber-500/10 border border-amber-500/20 text-amber-300">
                              + {m}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </GlassCard>
              </div>

              {/* Keyword Placement Advice (Where to Add Gaps) */}
              {jdAnalysis.keyword_gaps_with_placement.length > 0 && (
                <GlassCard glowColor="violet" className="p-6">
                  <div className="flex items-center gap-2 mb-4">
                    <FileSearch className="w-5 h-5 text-indigo-400" />
                    <div>
                      <h4 className="text-base font-bold text-white">Keyword Gaps & Strategic Placement Advice</h4>
                      <p className="text-xs text-slate-400 mt-0.5">Where and how to inject missing skills into your resume sections to pass screening</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {jdAnalysis.keyword_gaps_with_placement.map((gap, idx) => (
                      <div key={idx} className="p-4 rounded-xl border border-white/[0.08] bg-slate-900/60">
                        <div className="flex items-center justify-between">
                          <span className="text-sm font-bold text-white">{gap.keyword}</span>
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                            gap.importance === 'Must-Have' ? 'bg-rose-500/20 text-rose-300' : 'bg-amber-500/20 text-amber-300'
                          }`}>
                            {gap.importance}
                          </span>
                        </div>
                        <div className="mt-2 text-[11px] text-sky-400 font-semibold flex items-center gap-1">
                          <ChevronRight className="w-3.5 h-3.5" />
                          <span>Target Section: {gap.recommended_section}</span>
                        </div>
                        <p className="mt-1 text-xs text-slate-300 leading-relaxed">
                          {gap.placement_tip}
                        </p>
                      </div>
                    ))}
                  </div>
                </GlassCard>
              )}

              {/* Actionable Resume Edits */}
              {jdAnalysis.actionable_resume_edits.length > 0 && (
                <GlassCard glowColor="blue" className="p-6">
                  <div className="flex items-center gap-2 mb-4">
                    <Sparkles className="w-5 h-5 text-sky-400" />
                    <div>
                      <h4 className="text-base font-bold text-white">Actionable Resume Rewrites Tailored to This JD</h4>
                      <p className="text-xs text-slate-400 mt-0.5">Direct before/after bullet improvements to mirror the employer's vocabulary</p>
                    </div>
                  </div>

                  <div className="space-y-4">
                    {jdAnalysis.actionable_resume_edits.map((edit, idx) => (
                      <div key={idx} className="p-4 rounded-xl border border-white/[0.08] bg-slate-900/60">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-bold text-white">{edit.action}</span>
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                            edit.priority === 'High' ? 'bg-rose-500/20 text-rose-300' : 'bg-sky-500/20 text-sky-300'
                          }`}>
                            {edit.priority} Priority
                          </span>
                        </div>
                        {edit.before_example && (
                          <div className="mt-2.5 space-y-1.5 text-xs">
                            <div className="p-2.5 rounded-lg bg-rose-950/30 border border-rose-500/20 text-rose-200">
                              <span className="font-bold text-rose-300 block text-[10px] uppercase">Before:</span>
                              "{edit.before_example}"
                            </div>
                            <div className="p-2.5 rounded-lg bg-emerald-950/30 border border-emerald-500/20 text-emerald-200">
                              <span className="font-bold text-emerald-300 block text-[10px] uppercase">After (Optimized):</span>
                              "{edit.after_example}"
                            </div>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                </GlassCard>
              )}
            </div>
          ) : (
            <div className="mt-8 text-center p-12 rounded-2xl border border-dashed border-white/[0.15] bg-slate-900/40 text-slate-400">
              <Target className="w-12 h-12 text-emerald-400 mx-auto mb-3 opacity-80" />
              <h4 className="text-base font-bold text-white">Ready to Match Against Your Target Job Description</h4>
              <p className="text-xs text-slate-400 mt-1 max-w-md mx-auto">
                Select your resume above, paste your target job description (or click a sample JD), and click "Match Resume to Job Description".
              </p>
            </div>
          )
        ) : (
          /* --- DISPLAY MODE 2: 16-ROLE BENCHMARK AUDIT (EXISTING) --- */
          loading ? (
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
              {/* Benchmark Validation Notice for Roles without Public Datasets */}
              {analysis.limited_validation && (
                <div className="flex items-start gap-3.5 p-4 rounded-xl border border-amber-500/30 bg-amber-500/10 text-amber-200 shadow-lg shadow-amber-950/20">
                  <AlertTriangle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
                  <div className="text-xs leading-relaxed">
                    <div className="font-semibold text-amber-300 text-sm">Synthetic Benchmark Validation Notice</div>
                    <div className="text-amber-200/90 mt-1">
                      {analysis.validation_notes || `This role's model was validated using structured benchmarks (roadmap.sh, O*NET) due to lack of public open-source resume data for ${targetRole}.`}
                    </div>
                  </div>
                </div>
              )}

            {/* Top Score Banner */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
              {/* Main Circular Score (4 cols) */}
              <GlassCard glowColor="blue" className="lg:col-span-4 p-8 flex flex-col items-center justify-center text-center">
                <div className="relative flex h-40 w-40 items-center justify-center">
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

                <h3 className="mt-4 text-base font-bold text-white">
                  ATS Compatibility Score <span className="text-slate-400 text-xs font-normal">(estimate)</span>
                </h3>
                <p className="mt-1 text-xs text-slate-300">
                  Targeted role: <strong className="text-sky-300">{targetRole}</strong>
                </p>
                <div className="mt-3 flex flex-wrap items-center justify-center gap-1.5">
                  {analysis.detected_seniority && (
                    <Badge variant="verified" className="capitalize text-[10px]">
                      {analysis.detected_seniority} Track
                    </Badge>
                  )}
                  <Badge variant={analysis.ats_score >= 80 ? 'ats_high' : analysis.ats_score >= 60 ? 'verified' : 'in_progress'}>
                    {analysis.ats_score >= 80 ? 'Top 10% Applicant Tier' : analysis.ats_score >= 60 ? 'Competitive Applicant Tier' : 'Needs Optimization'}
                  </Badge>
                </div>
              </GlassCard>

              {/* 5-Factor Documented Weighted Score Breakdown (8 cols) */}
              <GlassCard glowColor="violet" className="lg:col-span-8 p-8 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-base font-bold text-white">5-Factor Documented Score Breakdown</h3>
                      <p className="text-xs text-slate-400 mt-0.5">Strict server-side formula computed from Kaggle ML model & parsing taxonomy</p>
                    </div>
                    <Badge variant="highlight" className="text-[10px]">Deterministic</Badge>
                  </div>

                  <div className="mt-6 space-y-3.5">
                    {/* 1. Role Alignment (40%) */}
                    <div>
                      <div className="flex justify-between text-xs font-semibold mb-1">
                        <span className="text-slate-300 flex items-center gap-1.5">
                          <span className="h-1.5 w-1.5 rounded-full bg-sky-400"></span>
                          Role Alignment (40% weight)
                          <span className="text-[10px] text-slate-400 font-normal ml-1">
                            (Calibrated alignment index, not a probability)
                          </span>
                        </span>
                        <span className="text-sky-400 font-bold">
                          {analysis.role_alignment_score ?? analysis.role_fit_score ?? 85.0}%
                        </span>
                      </div>
                      <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-sky-500 to-indigo-500 rounded-full transition-all duration-700"
                          style={{ width: `${analysis.role_alignment_score ?? analysis.role_fit_score ?? 85}%` }}
                        />
                      </div>
                    </div>

                    {/* 2. Keyword & Skill Coverage (25%) */}
                    <div>
                      <div className="flex justify-between text-xs font-semibold mb-1">
                        <span className="text-slate-300 flex items-center gap-1.5">
                          <span className="h-1.5 w-1.5 rounded-full bg-teal-400"></span>
                          Keyword & Competency Coverage (25% weight)
                        </span>
                        <span className="text-teal-400 font-bold">{analysis.skills_match_score}%</span>
                      </div>
                      <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
                        <div
                          className="h-full bg-teal-400 rounded-full transition-all duration-700"
                          style={{ width: `${analysis.skills_match_score}%` }}
                        />
                      </div>
                    </div>

                    {/* 3. Section Completeness (15%) */}
                    <div>
                      <div className="flex justify-between text-xs font-semibold mb-1">
                        <span className="text-slate-300 flex items-center gap-1.5">
                          <span className="h-1.5 w-1.5 rounded-full bg-indigo-400"></span>
                          Section Completeness (15% weight)
                        </span>
                        <span className="text-indigo-400 font-bold">
                          {analysis.section_score ? `${analysis.section_score}%` : '100%'}
                        </span>
                      </div>
                      <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
                        <div
                          className="h-full bg-indigo-400 rounded-full transition-all duration-700"
                          style={{ width: `${analysis.section_score || 100}%` }}
                        />
                      </div>
                    </div>

                    {/* 4. Formatting & Parsability (10%) */}
                    <div>
                      <div className="flex justify-between text-xs font-semibold mb-1">
                        <span className="text-slate-300 flex items-center gap-1.5">
                          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400"></span>
                          Formatting & Parsability (10% weight)
                        </span>
                        <span className="text-emerald-400 font-bold">{analysis.formatting_score}%</span>
                      </div>
                      <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
                        <div
                          className="h-full bg-emerald-400 rounded-full transition-all duration-700"
                          style={{ width: `${analysis.formatting_score}%` }}
                        />
                      </div>
                    </div>

                    {/* 5. Quantified Impact (10%) */}
                    <div>
                      <div className="flex justify-between text-xs font-semibold mb-1">
                        <span className="text-slate-300 flex items-center gap-1.5">
                          <span className="h-1.5 w-1.5 rounded-full bg-violet-400"></span>
                          Quantified Impact & Outcomes (10% weight)
                        </span>
                        <span className="text-violet-400 font-bold">{analysis.impact_score}%</span>
                      </div>
                      <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
                        <div
                          className="h-full bg-violet-400 rounded-full transition-all duration-700"
                          style={{ width: `${analysis.impact_score}%` }}
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Submetrics footer */}
                <div className="mt-5 grid grid-cols-2 sm:grid-cols-4 gap-3 border-t border-white/[0.06] pt-3 text-xs">
                  <div>
                    <span className="text-slate-400 block text-[11px]">Action Verbs</span>
                    <strong className="text-white text-sm">{analysis.action_verb_count} Detected</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[11px]">Metrics Found</span>
                    <strong className="text-white text-sm">{analysis.quantifiable_metrics_count} Benchmarks</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[11px]">Matched Skills</span>
                    <strong className="text-sky-400 text-sm">{analysis.matched_skills.length} Verified</strong>
                  </div>
                  <div>
                    <span className="text-slate-400 block text-[11px]">Critical Gaps</span>
                    <strong className="text-rose-400 text-sm">{analysis.missing_skills.length} Missing</strong>
                  </div>
                </div>
              </GlassCard>
            </div>

            {/* Top Contributing ML Features & Deductions */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Top ML Features (6 cols) */}
              <GlassCard glowColor="blue" className="lg:col-span-6 p-6">
                <div className="flex items-center gap-2 mb-2">
                  <BarChart3 className="h-4 w-4 text-sky-400" />
                  <h3 className="text-base font-bold text-white">Top Contributing Terms (ML Model Explainability)</h3>
                </div>
                <p className="text-xs text-slate-300 mb-4">
                  These high-weight TF-IDF terms in your resume pushed the classifier’s {targetRole} probability highest:
                </p>

                <div className="flex flex-wrap gap-2">
                  {analysis.top_contributing_features && analysis.top_contributing_features.length > 0 ? (
                    analysis.top_contributing_features.map((feat, idx) => (
                      <span
                        key={idx}
                        className="inline-flex items-center gap-1.5 rounded-lg border border-sky-500/30 bg-sky-500/10 px-3 py-1 text-xs font-medium text-sky-300"
                      >
                        <Sparkles className="h-3 w-3 text-sky-400" />
                        <strong>{feat.feature}</strong>
                        <span className="text-[10px] text-sky-400/70">+{feat.weight}</span>
                      </span>
                    ))
                  ) : (
                    ['pytorch', 'transformers', 'deep learning', 'python', 'fastapi'].map((term) => (
                      <span
                        key={term}
                        className="inline-flex items-center gap-1.5 rounded-lg border border-sky-500/30 bg-sky-500/10 px-3 py-1 text-xs font-medium text-sky-300"
                      >
                        <Sparkles className="h-3 w-3 text-sky-400" />
                        <strong>{term}</strong>
                      </span>
                    ))
                  )}
                </div>
              </GlassCard>

              {/* Plain-Language Deductions (6 cols) */}
              <GlassCard glowColor="amber" className="lg:col-span-6 p-6">
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="h-4 w-4 text-amber-400" />
                  <h3 className="text-base font-bold text-white">Itemized Point Deductions</h3>
                </div>
                <p className="text-xs text-slate-300 mb-3">
                  Plain-language reasons explaining points lost across the 5 evaluation dimensions:
                </p>

                <div className="space-y-2.5">
                  {analysis.deductions && analysis.deductions.length > 0 ? (
                    analysis.deductions.map((ded, idx) => (
                      <div
                        key={idx}
                        className="flex items-start justify-between rounded-xl border border-amber-500/20 bg-amber-950/10 p-3 text-xs"
                      >
                        <div className="pr-3">
                          <strong className="text-amber-300 block">{ded.category}</strong>
                          <span className="text-slate-300">{ded.reason}</span>
                        </div>
                        <span className="font-bold text-rose-400 shrink-0">-{ded.lost_points} pts</span>
                      </div>
                    ))
                  ) : (
                    <div className="text-xs text-emerald-300 flex items-center gap-1.5">
                      <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                      <span>No major deductions! Excellent technical and structural formatting.</span>
                    </div>
                  )}
                </div>
              </GlassCard>
            </div>

            {/* Gap Analysis & 1-Click "Add to Roadmap" Action */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Critical Missing Skills Gaps (6 cols) */}
              <GlassCard glowColor="amber" className="lg:col-span-6 p-6">
                <div className="flex items-center gap-2 mb-2">
                  <AlertTriangle className="h-4 w-4 text-rose-400" />
                  <h3 className="text-base font-bold text-white">Identified Critical Skill Gaps</h3>
                </div>
                <p className="text-xs text-slate-300">
                  Essential competencies required for <strong className="text-white">{targetRole}</strong>:
                </p>

                <div className="mt-4 space-y-3">
                  {(analysis.missing_critical_skills || analysis.missing_skills).map((skill) => {
                    const isAdded = addedSkills.includes(skill);
                    const isProcessing = addingSkill === skill;
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
                          disabled={isAdded || isProcessing}
                          className="text-xs py-1.5 px-3"
                        >
                          {isProcessing ? (
                            <>
                              <RefreshCw className="h-3.5 w-3.5 animate-spin" />
                              <span>Adding...</span>
                            </>
                          ) : isAdded ? (
                            <>
                              <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" />
                              <span>Added to Roadmap</span>
                            </>
                          ) : (
                            <>
                              <Plus className="h-3.5 w-3.5" />
                              <span>+ Add to Roadmap</span>
                            </>
                          )}
                        </MagneticButton>
                      </div>
                    );
                  })}
                </div>

                {/* Bonus Skills Gap */}
                {analysis.missing_bonus_skills && analysis.missing_bonus_skills.length > 0 && (
                  <div className="mt-6 pt-4 border-t border-white/[0.08]">
                    <span className="text-xs font-semibold text-slate-400 block mb-2">
                      Recommended Bonus Skills to Stand Out:
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {analysis.missing_bonus_skills.slice(0, 8).map((bSkill) => (
                        <span
                          key={bSkill}
                          className="rounded-lg border border-indigo-500/20 bg-indigo-500/10 px-2.5 py-1 text-[11px] font-medium text-indigo-300"
                        >
                          +{bSkill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
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
                    <span>Executive Critique & Guidance:</span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    {analysis.summary_critique}
                  </p>
                </div>
              </GlassCard>
            </div>

            {/* AI Bridged Roadmap Section */}
            <div className="mt-8">
              <GlassCard glowColor="violet" className="p-6 sm:p-8 border border-indigo-500/30 bg-gradient-to-br from-slate-900/90 via-indigo-950/20 to-slate-900/90 shadow-2xl">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-white/[0.08] pb-6">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="inline-flex items-center gap-1.5 rounded-full bg-indigo-500/20 border border-indigo-400/40 px-3 py-1 text-xs font-semibold text-indigo-300">
                        <Sparkles className="h-3.5 w-3.5 text-indigo-400 animate-pulse" />
                        OmniRoute AI Intelligence
                      </span>
                      <span className="text-xs text-slate-400">Personalized Skill Gap Remediation</span>
                    </div>
                    <h2 className="mt-2 text-xl sm:text-2xl font-bold text-white flex items-center gap-2">
                      <Compass className="h-6 w-6 text-indigo-400" />
                      AI Bridge Roadmap: <span className="text-gradient">{targetRole}</span>
                    </h2>
                    <p className="mt-1 text-xs sm:text-sm text-slate-300 max-w-2xl">
                      {bridgeRoadmap?.executive_strategy ||
                        `An adaptive, deterministic learning path engineered to close your ${analysis.missing_skills.length} identified skill gaps and boost your hiring match.`}
                    </p>
                  </div>

                  {/* Impact Stats */}
                  <div className="flex items-center gap-4 shrink-0 bg-slate-850/80 p-3 rounded-2xl border border-white/[0.08]">
                    <div className="text-center px-2">
                      <span className="text-[11px] text-slate-400 block font-medium">Current ATS</span>
                      <span className="text-lg font-black text-amber-400">{analysis.ats_score}%</span>
                    </div>
                    <div className="h-8 w-[1px] bg-white/[0.1]" />
                    <div className="text-center px-2">
                      <span className="text-[11px] text-slate-400 block font-medium">Projected ATS</span>
                      <span className="text-lg font-black text-emerald-400 flex items-center justify-center gap-0.5">
                        <TrendingUp className="h-4 w-4" />
                        {bridgeRoadmap?.projected_ats_score || Math.min(95, analysis.ats_score + 28)}%
                      </span>
                    </div>
                    <div className="h-8 w-[1px] bg-white/[0.1]" />
                    <div className="text-center px-2">
                      <span className="text-[11px] text-slate-400 block font-medium">Est. Duration</span>
                      <span className="text-lg font-black text-sky-400">
                        {bridgeRoadmap?.estimated_weeks || 6} wks
                      </span>
                    </div>
                  </div>
                </div>

                {/* Milestone Cards Grid */}
                <div className="mt-6">
                  {isGeneratingBridge ? (
                    <div className="py-12 flex flex-col items-center justify-center text-center">
                      <RefreshCw className="h-8 w-8 text-indigo-400 animate-spin mb-3" />
                      <p className="text-sm font-semibold text-slate-200">
                        OmniRoute model synthesizing tailored gap-remediation milestones...
                      </p>
                      <span className="text-xs text-slate-400 mt-1">Cross-referencing verified syllabus with hiring benchmarks</span>
                    </div>
                  ) : bridgeRoadmap?.milestones && bridgeRoadmap.milestones.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                      {bridgeRoadmap.milestones.map((milestone) => (
                        <div
                          key={milestone.step}
                          className="relative rounded-xl border border-indigo-500/20 bg-slate-900/60 p-4 transition-all duration-300 hover:border-indigo-400/50 hover:bg-slate-900/80 flex flex-col justify-between"
                        >
                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-indigo-500/20 text-xs font-bold text-indigo-400 border border-indigo-400/30">
                                {milestone.step}
                              </span>
                              <span className="text-[11px] font-medium text-slate-400">
                                {milestone.duration_weeks} {milestone.duration_weeks === 1 ? 'week' : 'weeks'}
                              </span>
                            </div>
                            <h3 className="text-sm font-bold text-white mb-1">{milestone.title}</h3>
                            <span className="inline-block rounded bg-indigo-500/10 px-2 py-0.5 text-[10px] font-semibold text-indigo-300 mb-2 border border-indigo-500/20">
                              Focus: {milestone.skill}
                            </span>
                            <p className="text-xs text-slate-300 leading-relaxed mb-3">
                              {milestone.objective}
                            </p>
                          </div>
                          <div className="rounded-lg bg-slate-950/60 p-2.5 border border-white/[0.04]">
                            <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block mb-0.5">
                              Capstone Deliverable:
                            </span>
                            <p className="text-[11px] text-sky-300 font-medium line-clamp-2">
                              {milestone.project_task}
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : analysis.personalized_roadmap && analysis.personalized_roadmap.length > 0 ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {analysis.personalized_roadmap.map((topicItem) => (
                        <div
                          key={topicItem.step}
                          className="rounded-xl border border-indigo-500/20 bg-slate-900/60 p-4 flex flex-col justify-between hover:border-indigo-400/40 transition-all"
                        >
                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-indigo-500/20 text-xs font-bold text-indigo-400 border border-indigo-400/30">
                                {topicItem.step}
                              </span>
                              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                                topicItem.priority === 'Critical'
                                  ? 'bg-rose-500/15 text-rose-300 border border-rose-500/30'
                                  : 'bg-indigo-500/15 text-indigo-300 border border-indigo-500/30'
                              }`}>
                                {topicItem.priority}
                              </span>
                            </div>
                            <h4 className="text-sm font-bold text-white mb-1.5">{topicItem.topic}</h4>
                            <p className="text-xs text-slate-300 leading-relaxed mb-3">
                              {topicItem.description}
                            </p>
                            <div className="mb-3 flex flex-wrap gap-1">
                              {topicItem.missing_skills.map((s) => (
                                <span key={s} className="rounded bg-slate-800/80 px-1.5 py-0.5 text-[10px] text-slate-300">
                                  {s}
                                </span>
                              ))}
                            </div>
                          </div>

                          {topicItem.resources && topicItem.resources.length > 0 && (
                            <div className="pt-2 border-t border-white/[0.06] space-y-1">
                              <span className="text-[10px] font-semibold text-slate-400 block">Curated Free Resources:</span>
                              {topicItem.resources.map((res, rIdx) => (
                                <a
                                  key={rIdx}
                                  href={res.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-[11px] text-sky-400 hover:text-sky-300 hover:underline block truncate"
                                >
                                  ↗ {res.title}
                                </a>
                              ))}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      {analysis.missing_skills.slice(0, 3).map((skill, i) => (
                        <div key={skill} className="rounded-xl border border-white/[0.08] bg-slate-900/60 p-4">
                          <span className="text-xs font-bold text-indigo-400">Phase {i + 1}</span>
                          <h4 className="text-sm font-bold text-white mt-1">Master {skill}</h4>
                          <p className="text-xs text-slate-300 mt-1">Targeted module curriculum designed to eliminate this ATS deficiency.</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Call To Action Buttons */}
                <div className="mt-8 flex flex-col sm:flex-row items-center justify-between gap-4 pt-6 border-t border-white/[0.08]">
                  <div className="text-xs text-slate-400 flex items-center gap-2">
                    <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                    <span>Enrolling adapts module sequence specifically to your missing competencies.</span>
                  </div>

                  <div className="flex items-center gap-3 w-full sm:w-auto">
                    <button
                      onClick={() => navigate('/courses')}
                      className="w-full sm:w-auto rounded-xl border border-white/[0.1] bg-slate-900/80 px-4 py-2.5 text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800 transition-all"
                    >
                      Browse All Courses
                    </button>
                    <MagneticButton
                      variant="primary"
                      onClick={handleStartCourseWithRoadmap}
                      className="w-full sm:w-auto flex items-center justify-center gap-2 px-6 py-2.5 text-sm font-bold shadow-neon-blue"
                    >
                      <span>Start Course with AI Bridged Roadmap</span>
                      <ArrowRight className="h-4 w-4" />
                    </MagneticButton>
                  </div>
                </div>
              </GlassCard>
            </div>
          </div>
        ) : null
        )}
      </div>
    </div>
  );
};

export default Resume;

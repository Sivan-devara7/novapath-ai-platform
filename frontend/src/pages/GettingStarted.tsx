import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  FileText,
  UploadCloud,
  Compass,
  Sparkles,
  HelpCircle,
  GraduationCap,
  ArrowRight,
  CheckCircle2,
  Award,
  Zap,
  BookOpen,
  Layers,
  ChevronRight,
  AlertCircle,
  Play
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../services/api';
import { GlassCard } from '../components/ui/GlassCard';
import { MagneticButton } from '../components/ui/MagneticButton';
import { Badge } from '../components/ui/Badge';

export const GettingStarted: React.FC = () => {
  const navigate = useNavigate();
  const { user, updateUser } = useAuth();
  const { t } = useLanguage();

  // Path A: Resume Upload State
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);
  const [uploadProgressMsg, setUploadProgressMsg] = useState('');

  // Path B: Course Track & Selection State
  const [selectedTrack, setSelectedTrack] = useState<string>('AI Engineer');

  const tracks = [
    {
      id: 'AI Engineer',
      title: 'AI & Machine Learning Engineer',
      desc: 'Python, Math Foundations, Deep Learning, MLOps & RAG Architecture',
      modulesCount: 6,
      badge: 'Popular Track'
    },
    {
      id: 'Data Engineer',
      title: 'Data Engineering & Modern Lakehouse',
      desc: 'SQL Internals, Apache Spark, Kafka Streaming, Snowflake & dbt',
      modulesCount: 5,
      badge: 'High Enterprise Demand'
    },
    {
      id: 'Cybersecurity Analyst',
      title: 'Cybersecurity Defense & SOC Operations',
      desc: 'Wireshark Packet Analysis, SIEM, MITRE ATT&CK & Penetration Testing',
      modulesCount: 5,
      badge: 'Mission Critical'
    },
    {
      id: 'Full Stack Developer',
      title: 'Full Stack Web & Cloud Architect',
      desc: 'React, TypeScript, FastAPI, Docker & Microservice Design',
      modulesCount: 5,
      badge: 'Industry High Demand'
    },
    {
      id: 'Cloud & DevOps Engineer',
      title: 'Cloud & DevOps Infrastructure',
      desc: 'Kubernetes, Terraform, CI/CD, AWS/GCP Reliability',
      modulesCount: 5,
      badge: 'Enterprise Core'
    }
  ];

  // Handle Resume File Pick
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
      setUploadError(null);
    }
  };

  const [isDragOver, setIsDragOver] = useState(false);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      const ext = file.name.toLowerCase();
      if (ext.endsWith('.pdf') || ext.endsWith('.docx') || ext.endsWith('.txt')) {
        setSelectedFile(file);
        setUploadError(null);
      } else {
        setUploadError('Please select a .pdf, .docx, or .txt file format.');
      }
    }
  };

  // Upload and Parse Resume
  const handleResumeSubmit = async () => {
    if (!selectedFile) {
      setUploadError('Please select a resume file (.pdf, .docx, or .txt)');
      return;
    }

    setIsUploading(true);
    setUploadError(null);
    setUploadProgressMsg('Extracting resume text with PDF/OCR engine...');

    try {
      setTimeout(() => setUploadProgressMsg('Calculating BERT TF-IDF ATS keyword match...'), 600);
      setTimeout(() => setUploadProgressMsg('Calibrating personalized career roadmap...'), 1200);

      const res = await api.uploadResume(selectedFile);
      setIsUploading(false);
      // Save to sessionStorage for persistent session view
      sessionStorage.setItem('novapath_latest_resume_analysis', JSON.stringify(res));
      // Navigate to resume analysis page to view ATS score and matched skills
      navigate('/resume', { state: { uploadedAnalysis: res, fileName: selectedFile.name } });
    } catch (err: any) {
      setIsUploading(false);
      setUploadError(err.message || 'Failed to process resume. Please ensure your file contains readable text.');
    }
  };

  // Quick Demo Resume Handler
  const handleSampleResume = async () => {
    setIsUploading(true);
    setUploadError(null);
    setUploadProgressMsg('Loading sample candidate profile (Aarav Sharma - AI Aspirant)...');

    try {
      const res = await api.analyzeResume(undefined, 'AI Engineer');
      setIsUploading(false);
      sessionStorage.setItem('novapath_latest_resume_analysis', JSON.stringify(res));
      navigate('/resume', { state: { uploadedAnalysis: res, fileName: 'Aarav_Sharma_Resume.pdf' } });
    } catch (err: any) {
      setIsUploading(false);
      setUploadError(err.message || 'Sample load failed');
    }
  };

  // Path B: Option 1 (Quiz)
  const handleStartWithQuiz = () => {
    updateUser({ career_goal: selectedTrack });
    navigate('/roadmap?placement=true');
  };

  // Path B: Option 2 (Scratch Basics)
  const handleStartFromScratch = () => {
    updateUser({ career_goal: selectedTrack });
    navigate('/roadmap/py-foundations');
  };

  return (
    <div className="relative min-h-[calc(100vh-4rem)] bg-[var(--bg-primary)] px-4 py-12 sm:px-6 lg:px-8 text-[var(--text-primary)] transition-colors duration-300">
      {/* Background ambient lighting */}
      <div className="pointer-events-none absolute -top-24 left-1/4 h-96 w-96 rounded-full bg-sky-500/10 blur-[130px]" />
      <div className="pointer-events-none absolute top-1/2 right-1/4 h-96 w-96 rounded-full bg-indigo-500/10 blur-[130px]" />

      <div className="mx-auto max-w-6xl relative z-10">
        {/* Welcome Header */}
        <div className="text-center max-w-2xl mx-auto mb-10">
          <div className="inline-flex items-center gap-2 rounded-full border border-sky-400/30 bg-sky-500/10 px-3.5 py-1 text-xs font-bold text-sky-300 mb-3 shadow-[0_0_15px_rgba(56,189,248,0.2)]">
            <Sparkles className="h-3.5 w-3.5 text-sky-400" />
            <span>{t('gs_step2_title', 'Choose Your Starting Mode')}</span>
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white">
            {t('gs_title', 'Welcome to NovaPath AI')}
          </h1>
          <p className="mt-3 text-sm text-slate-300">
            {t('gs_subtitle', "Let's calibrate your personalized learning journey in 2 quick steps")}
          </p>
        </div>

        {/* Dual Path Cards Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">
          
          {/* ================= PATH A: RESUME UPLOAD ================= */}
          <GlassCard glowColor="blue" className="flex flex-col justify-between p-6 sm:p-8 border-sky-500/30 bg-slate-900/60 shadow-2xl">
            <div>
              <div className="flex items-center justify-between">
                <Badge variant="verified">{t('gs_mode_resume', 'Option A: I Have a Resume')}</Badge>
                <span className="text-xs font-semibold text-sky-400">Path A</span>
              </div>

              <div className="mt-5 flex items-center gap-3.5">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-sky-500/10 border border-sky-400/30 text-sky-400 shadow-neon-blue">
                  <FileText className="h-6 w-6" />
                </div>
                <div>
                  <h2 className="text-xl font-extrabold text-white">I Have a Resume / Transcript</h2>
                  <p className="text-xs text-slate-400">Fast-track by analyzing what you already know</p>
                </div>
              </div>

              <p className="mt-4 text-xs text-slate-300 leading-relaxed">
                Upload your resume or curriculum vitae. Our server-side ATS parser extracts your verified skills, projects, and coursework to automatically customize your roadmap and calculate your candidate readiness score.
              </p>

              {/* Google Sign In / Sync before Uploading */}
              <div className="mt-5 rounded-2xl border border-white/[0.08] bg-slate-950/60 p-3.5">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-bold text-slate-300">Save & Link Your Analysis</span>
                  <span className="text-[10px] text-emerald-400 font-semibold flex items-center gap-1">
                    <CheckCircle2 className="h-3 w-3" />
                    Instant Sync
                  </span>
                </div>
                <button
                  type="button"
                  onClick={handleSampleResume}
                  className="w-full flex items-center justify-center gap-2.5 rounded-xl border border-white/[0.12] bg-slate-900/90 hover:bg-slate-800 px-4 py-2 text-xs font-bold text-white transition-all shadow-md hover:border-sky-400/50"
                >
                  <svg className="h-4 w-4 shrink-0" viewBox="0 0 24 24">
                    <path
                      fill="#4285F4"
                      d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                    />
                    <path
                      fill="#34A853"
                      d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                    />
                    <path
                      fill="#FBBC05"
                      d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
                    />
                    <path
                      fill="#EA4335"
                      d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
                    />
                  </svg>
                  <span>Continue with Google</span>
                </button>
              </div>

              {/* Upload Drop Area */}
              <div
                onClick={() => fileInputRef.current?.click()}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`mt-6 border-2 border-dashed rounded-2xl p-6 text-center cursor-pointer transition-all duration-200 ${
                  isDragOver
                    ? 'border-sky-400 bg-sky-950/40 shadow-neon-blue scale-[1.01]'
                    : 'border-sky-400/30 hover:border-sky-400/60 bg-slate-950/40 hover:bg-sky-950/20'
                }`}
              >
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileChange}
                  accept=".pdf,.docx,.txt"
                  className="hidden"
                />
                <UploadCloud className="mx-auto h-8 w-8 text-sky-400 mb-2 animate-bounce" />
                <span className="block text-xs font-bold text-white">
                  {selectedFile ? selectedFile.name : 'Click to select or drop resume file'}
                </span>
                <span className="block text-[11px] text-slate-400 mt-1">
                  Supports PDF, DOCX, or TXT (Max 5MB)
                </span>
              </div>

              {/* Progress or Error */}
              {isUploading && (
                <div className="mt-4 rounded-xl border border-sky-400/30 bg-sky-950/30 p-3 text-xs text-sky-300 flex items-center gap-2">
                  <div className="h-4 w-4 animate-spin rounded-full border-2 border-sky-400 border-t-transparent" />
                  <span>{uploadProgressMsg}</span>
                </div>
              )}

              {uploadError && (
                <div className="mt-4 rounded-xl border border-rose-500/30 bg-rose-950/30 p-3 text-xs text-rose-300 flex items-center gap-2">
                  <AlertCircle className="h-4 w-4 shrink-0 text-rose-400" />
                  <span>{uploadError}</span>
                </div>
              )}
            </div>

            <div className="mt-8 space-y-3">
              <MagneticButton
                variant="primary"
                onClick={handleResumeSubmit}
                disabled={isUploading}
                className="w-full justify-center py-3 text-xs font-bold shadow-neon-blue"
              >
                <span>{isUploading ? 'Analyzing Resume...' : 'Analyze Resume & Generate Roadmap'}</span>
                <ArrowRight className="h-4 w-4" />
              </MagneticButton>

              <button
                type="button"
                onClick={handleSampleResume}
                disabled={isUploading}
                className="w-full text-center text-xs text-slate-400 hover:text-sky-300 font-semibold py-1.5 transition-colors"
              >
                Don't have a file right now? <u>Try Sample Resume</u>
              </button>
            </div>
          </GlassCard>

          {/* ================= PATH B: START FROM SCRATCH INTO A COURSE ================= */}
          <GlassCard glowColor="violet" className="flex flex-col justify-between p-6 sm:p-8 border-violet-500/30 bg-slate-900/60 shadow-2xl">
            <div>
              <div className="flex items-center justify-between">
                <Badge variant="in_progress">Structured Course Track</Badge>
                <span className="text-xs font-semibold text-violet-400">Path B</span>
              </div>

              <div className="mt-5 flex items-center gap-3.5">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-violet-500/10 border border-violet-400/30 text-violet-400 shadow-[0_0_20px_rgba(168,85,247,0.2)]">
                  <GraduationCap className="h-6 w-6" />
                </div>
                <div>
                  <h2 className="text-xl font-extrabold text-white">Start from Scratch into a Course</h2>
                  <p className="text-xs text-slate-400">No resume needed — enroll directly in a track</p>
                </div>
              </div>

              <p className="mt-4 text-xs text-slate-300 leading-relaxed">
                Choose your career track below, then pick how you'd like to begin: take an adaptive diagnostic quiz to test existing skills, or start from square one.
              </p>

              {/* Track Selector */}
              <div className="mt-5 space-y-2.5">
                <label className="block text-xs font-bold text-slate-300">
                  Select Your Career Track:
                </label>
                {tracks.map((t) => {
                  const isSelected = selectedTrack === t.id;
                  return (
                    <div
                      key={t.id}
                      onClick={() => setSelectedTrack(t.id)}
                      className={`cursor-pointer rounded-xl border p-3 transition-all ${
                        isSelected
                          ? 'border-violet-500 bg-violet-950/40 shadow-[0_0_15px_rgba(168,85,247,0.2)]'
                          : 'border-white/[0.06] bg-slate-950/30 hover:border-white/[0.15]'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-bold text-white">{t.title}</span>
                        <span className="text-[10px] rounded-full bg-violet-500/20 text-violet-300 px-2 py-0.5 border border-violet-500/30">
                          {t.badge}
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 mt-1 line-clamp-1">{t.desc}</p>
                    </div>
                  );
                })}
              </div>

              {/* Course Start Choices Sub-Section */}
              <div className="mt-6">
                <span className="block text-xs font-bold text-white mb-3">
                  How would you like to begin this track?
                </span>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                  {/* Option 1: Diagnostic Quiz */}
                  <div
                    onClick={handleStartWithQuiz}
                    className="cursor-pointer rounded-2xl border border-sky-400/30 bg-slate-950/50 p-4 hover:border-sky-400/70 hover:bg-sky-950/20 transition-all flex flex-col justify-between group"
                  >
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-sky-500/20 text-sky-400">
                          <Zap className="h-4 w-4" />
                        </div>
                        <span className="text-xs font-bold text-white group-hover:text-sky-300 transition-colors">
                          Option 1: Placement Quiz
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 leading-relaxed">
                        Test what you already know! 20 adaptive questions. High scores skip foundation modules with bonus XP.
                      </p>
                    </div>
                    <div className="mt-3 flex items-center text-xs font-bold text-sky-400 group-hover:translate-x-1 transition-transform">
                      <span>Take Quiz</span>
                      <ChevronRight className="h-3.5 w-3.5 ml-1" />
                    </div>
                  </div>

                  {/* Option 2: Basics from Scratch */}
                  <div
                    onClick={handleStartFromScratch}
                    className="cursor-pointer rounded-2xl border border-emerald-400/30 bg-slate-950/50 p-4 hover:border-emerald-400/70 hover:bg-emerald-950/20 transition-all flex flex-col justify-between group"
                  >
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-emerald-500/20 text-emerald-400">
                          <BookOpen className="h-4 w-4" />
                        </div>
                        <span className="text-xs font-bold text-white group-hover:text-emerald-300 transition-colors">
                          Option 2: Basics from Scratch
                        </span>
                      </div>
                      <p className="text-[11px] text-slate-400 leading-relaxed">
                        Zero prior knowledge needed. Start directly with Module 1 (Python & Algorithmic Foundations).
                      </p>
                    </div>
                    <div className="mt-3 flex items-center text-xs font-bold text-emerald-400 group-hover:translate-x-1 transition-transform">
                      <span>Start from Scratch</span>
                      <ChevronRight className="h-3.5 w-3.5 ml-1" />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-white/[0.06] text-center">
              <span className="text-[11px] text-slate-400">
                You can switch between learning modes or retake quizzes anytime from the Roadmap.
              </span>
            </div>
          </GlassCard>

        </div>
      </div>
    </div>
  );
};

export default GettingStarted;

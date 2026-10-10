import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  UploadCloud,
  FileText,
  Award,
  CheckCircle2,
  Sparkles,
  ArrowRight,
  ShieldCheck,
  Brain,
  Check
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { useAuth } from '../context/AuthContext';
import { GlassCard } from '../components/ui/GlassCard';
import { MagneticButton } from '../components/ui/MagneticButton';
import { Badge } from '../components/ui/Badge';

export const Onboarding: React.FC = () => {
  const navigate = useNavigate();
  const { user, updateUser } = useAuth();

  const [step, setStep] = useState(1);
  const [careerGoal, setCareerGoal] = useState('AI Engineer');
  const [resumeUploaded, setResumeUploaded] = useState(false);
  const [certUploaded, setCertUploaded] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [extractedSkills, setExtractedSkills] = useState([
    'Python',
    'PyTorch',
    'FastAPI',
    'Docker',
    'Linear Algebra',
    'Git',
    'CUDA',
  ]);

  const handleSimulatedResumeUpload = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setResumeUploaded(true);
      setIsProcessing(false);
      setExtractedSkills((prev) => [
        ...new Set([...prev, 'Transformers', 'Hugging Face', 'Linux']),
      ]);
    }, 1200);
  };

  const handleSimulatedCertUpload = () => {
    setIsProcessing(true);
    setTimeout(() => {
      setCertUploaded(true);
      setIsProcessing(false);
      setExtractedSkills((prev) => [
        ...new Set([...prev, 'Deep Learning Specialization', 'AWS Cloud Practitioner']),
      ]);
    }, 1200);
  };

  const handleComplete = () => {
    confetti({
      particleCount: 100,
      spread: 70,
      origin: { y: 0.6 },
    });

    updateUser({
      career_goal: careerGoal,
      verified_skills: extractedSkills,
    });

    setTimeout(() => {
      navigate('/dashboard');
    }, 800);
  };

  return (
    <div className="relative min-h-screen bg-[var(--bg-primary)] pb-20 pt-10 text-[var(--text-primary)] transition-colors duration-300">
      <div className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
        {/* Progress Dots */}
        <div className="flex items-center justify-center gap-3 mb-8">
          <div
            className={`h-2 rounded-full transition-all duration-300 ${
              step >= 1 ? 'w-10 bg-sky-400' : 'w-2 bg-slate-800'
            }`}
          />
          <div
            className={`h-2 rounded-full transition-all duration-300 ${
              step >= 2 ? 'w-10 bg-sky-400' : 'w-2 bg-slate-800'
            }`}
          />
          <div
            className={`h-2 rounded-full transition-all duration-300 ${
              step >= 3 ? 'w-10 bg-sky-400' : 'w-2 bg-slate-800'
            }`}
          />
        </div>

        {/* Step 1: Career Target */}
        {step === 1 && (
          <GlassCard glowColor="blue" className="p-8 sm:p-10">
            <Badge variant="verified">Step 1 of 3: Target Role</Badge>
            <h1 className="mt-3 text-2xl sm:text-3xl font-extrabold text-white">
              What is your primary <span className="text-gradient">career trajectory?</span>
            </h1>
            <p className="mt-2 text-xs sm:text-sm text-slate-300">
              Your curriculum roadmap, RAG research papers, and ATS benchmarks will be calibrated against this target.
            </p>

            <div className="mt-8 space-y-3">
              {[
                {
                  id: 'AI Engineer',
                  desc: 'Focus on PyTorch, fine-tuning LLMs, transformers, vector DBs, and high-performance inference serving.',
                },
                {
                  id: 'Full Stack Developer',
                  desc: 'Focus on TypeScript, React 19, distributed backend microservices, Next.js, and cloud systems.',
                },
                {
                  id: 'Cloud & DevOps Engineer',
                  desc: 'Focus on Kubernetes orchestration, Terraform IaC, multi-cloud security, and CI/CD pipelines.',
                },
              ].map((role) => (
                <div
                  key={role.id}
                  onClick={() => setCareerGoal(role.id)}
                  className={`flex items-start gap-4 rounded-2xl border p-5 cursor-pointer transition-all ${
                    careerGoal === role.id
                      ? 'border-sky-400 bg-sky-500/10 shadow-neon-blue'
                      : 'border-white/[0.08] bg-slate-900/50 hover:bg-white/[0.04]'
                  }`}
                >
                  <div
                    className={`mt-1 flex h-5 w-5 items-center justify-center rounded-full border ${
                      careerGoal === role.id
                        ? 'border-sky-400 bg-sky-400 text-slate-950'
                        : 'border-slate-600 bg-slate-800'
                    }`}
                  >
                    {careerGoal === role.id && <Check className="h-3 w-3 stroke-[3]" />}
                  </div>
                  <div>
                    <h3 className="text-base font-bold text-white">{role.id}</h3>
                    <p className="mt-1 text-xs text-slate-400 leading-relaxed">{role.desc}</p>
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-8 flex justify-end">
              <MagneticButton variant="primary" onClick={() => setStep(2)}>
                <span>Next: Document Ingestion</span>
                <ArrowRight className="h-4 w-4" />
              </MagneticButton>
            </div>
          </GlassCard>
        )}

        {/* Step 2: Resume & Certificate Upload */}
        {step === 2 && (
          <GlassCard glowColor="violet" className="p-8 sm:p-10">
            <Badge variant="rag">Step 2 of 3: AI Document Processing</Badge>
            <h1 className="mt-3 text-2xl sm:text-3xl font-extrabold text-white">
              Upload Resume & <span className="text-gradient">Certifications</span>
            </h1>
            <p className="mt-2 text-xs sm:text-sm text-slate-300">
              Our PyMuPDF and Computer Vision OCR pipelines parse coursework, GPA, project tech stacks, and credentials.
            </p>

            <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-6">
              {/* Resume Ingestion Box */}
              <div
                onClick={handleSimulatedResumeUpload}
                className={`relative flex flex-col items-center justify-center rounded-2xl border-2 border-dashed p-6 text-center transition-all cursor-pointer ${
                  resumeUploaded
                    ? 'border-emerald-500/60 bg-emerald-500/10'
                    : 'border-sky-500/30 bg-slate-900/40 hover:border-sky-400/60'
                }`}
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-sky-500/10 text-sky-400 mb-3">
                  {resumeUploaded ? <CheckCircle2 className="h-6 w-6 text-emerald-400" /> : <FileText className="h-6 w-6" />}
                </div>
                <h4 className="text-sm font-bold text-white">
                  {resumeUploaded ? 'Resume Parsed Successfully' : 'Upload Candidate Resume'}
                </h4>
                <p className="mt-1 text-xs text-slate-400">
                  {resumeUploaded ? 'Extracted 12 technical competencies' : 'Click to load Aarav_Sharma_Resume.pdf'}
                </p>
                <span className="mt-3 rounded-full bg-slate-800 px-2.5 py-0.5 text-[10px] text-slate-300">
                  PyMuPDF Pipeline
                </span>
              </div>

              {/* Certificate Ingestion Box */}
              <div
                onClick={handleSimulatedCertUpload}
                className={`relative flex flex-col items-center justify-center rounded-2xl border-2 border-dashed p-6 text-center transition-all cursor-pointer ${
                  certUploaded
                    ? 'border-emerald-500/60 bg-emerald-500/10'
                    : 'border-violet-500/30 bg-slate-900/40 hover:border-violet-400/60'
                }`}
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-violet-500/10 text-violet-400 mb-3">
                  {certUploaded ? <CheckCircle2 className="h-6 w-6 text-emerald-400" /> : <Award className="h-6 w-6" />}
                </div>
                <h4 className="text-sm font-bold text-white">
                  {certUploaded ? 'Certificates Cryptographically Verified' : 'Upload Marksheet or Certificate'}
                </h4>
                <p className="mt-1 text-xs text-slate-400">
                  {certUploaded ? 'DeepLearning.AI + AWS Verified' : 'Click to test CV / OCR verification pipeline'}
                </p>
                <span className="mt-3 rounded-full bg-slate-800 px-2.5 py-0.5 text-[10px] text-slate-300">
                  OCR Hash Engine
                </span>
              </div>
            </div>

            {isProcessing && (
              <div className="mt-6 flex items-center justify-center gap-2 text-xs text-sky-400">
                <Sparkles className="h-4 w-4 animate-spin" />
                <span>Running document parsing and semantic taxonomy matching...</span>
              </div>
            )}

            <div className="mt-8 flex justify-between">
              <MagneticButton variant="ghost" onClick={() => setStep(1)}>
                Back
              </MagneticButton>
              <MagneticButton variant="primary" onClick={() => setStep(3)}>
                <span>Next: Skill Verification</span>
                <ArrowRight className="h-4 w-4" />
              </MagneticButton>
            </div>
          </GlassCard>
        )}

        {/* Step 3: Verified Skills Summary */}
        {step === 3 && (
          <GlassCard glowColor="emerald" className="p-8 sm:p-10">
            <Badge variant="verified">Step 3 of 3: Credential Confirmation</Badge>
            <h1 className="mt-3 text-2xl sm:text-3xl font-extrabold text-white">
              Profile Summary & <span className="text-gradient">Extracted Skills</span>
            </h1>
            <p className="mt-2 text-xs sm:text-sm text-slate-300">
              Your baseline profile is calibrated for <strong className="text-sky-400">{careerGoal}</strong>. Review your recognized competencies:
            </p>

            <div className="mt-6 flex flex-wrap gap-2">
              {extractedSkills.map((skill) => (
                <span
                  key={skill}
                  className="inline-flex items-center gap-1.5 rounded-xl border border-sky-400/30 bg-sky-500/10 px-3.5 py-1.5 text-xs font-semibold text-sky-300 shadow-[0_0_15px_rgba(56,189,248,0.15)]"
                >
                  <CheckCircle2 className="h-3.5 w-3.5 text-sky-400" />
                  {skill}
                </span>
              ))}
            </div>

            <div className="mt-8 rounded-2xl border border-white/[0.08] bg-slate-900/60 p-5">
              <div className="flex items-center gap-2 text-xs font-bold text-sky-300 mb-1">
                <Brain className="h-4 w-4 text-sky-400" />
                <span>Initial Calibration Ready</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                Foundational Python & Linear Algebra milestones are automatically credited as complete.
                Your learning path will launch directly at <strong>PyTorch & Deep Neural Networks</strong>.
              </p>
            </div>

            <div className="mt-8 flex justify-between">
              <MagneticButton variant="ghost" onClick={() => setStep(2)}>
                Back
              </MagneticButton>
              <MagneticButton variant="primary" onClick={handleComplete} className="shadow-neon-blue">
                <span>Enter Personalized Platform</span>
                <ArrowRight className="h-4 w-4" />
              </MagneticButton>
            </div>
          </GlassCard>
        )}
      </div>
    </div>
  );
};

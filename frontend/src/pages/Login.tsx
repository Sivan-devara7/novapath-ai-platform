import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Compass, Sparkles, ArrowRight, Lock, Mail, Play } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { GlassCard } from '../components/ui/GlassCard';
import { MagneticButton } from '../components/ui/MagneticButton';
import { Badge } from '../components/ui/Badge';

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [email, setEmail] = useState('aarav.sharma@vizag.edu');
  const [password, setPassword] = useState('••••••••••••');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    await login();
    setLoading(false);
    navigate('/dashboard');
  };

  const handleDemoQuickLogin = async () => {
    setLoading(true);
    await login();
    setLoading(false);
    navigate('/dashboard');
  };

  return (
    <div className="relative min-h-[calc(100vh-4rem)] flex items-center justify-center bg-[var(--bg-primary)] px-4 py-16 text-[var(--text-primary)] transition-colors duration-300">
      {/* Background glow */}
      <div className="pointer-events-none absolute -top-32 left-1/2 -translate-x-1/2 h-96 w-96 rounded-full bg-sky-500/10 blur-[120px]" />

      <div className="w-full max-w-md">
        <GlassCard glowColor="blue" className="p-8 sm:p-10">
          <div className="text-center">
            <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 shadow-neon-blue mb-4">
              <Compass className="h-6 w-6 text-white" />
            </div>
            <h1 className="text-2xl font-extrabold text-white">Sign In to NovaPath</h1>
            <p className="mt-1 text-xs text-slate-400">
              Access your personalized AI career roadmap & mentor
            </p>
          </div>

          {/* Quick Demo One-Click Access for Judges */}
          <div className="mt-6 rounded-2xl border border-sky-500/30 bg-sky-950/30 p-4 text-center">
            <div className="flex items-center justify-center gap-1.5 text-xs font-bold text-sky-300 mb-1">
              <Sparkles className="h-3.5 w-3.5 text-sky-400" />
              <span>Hackathon Judge Quick-Access</span>
            </div>
            <p className="text-[11px] text-slate-300 mb-3">
              Skip typing and launch directly as <strong>Aarav Sharma (AI Engineer Aspirant)</strong>
            </p>
            <MagneticButton
              variant="primary"
              onClick={handleDemoQuickLogin}
              disabled={loading}
              className="w-full justify-center text-xs py-2 shadow-neon-blue"
            >
              <Play className="h-3.5 w-3.5 fill-white" />
              <span>1-Click Instant Demo Login</span>
            </MagneticButton>
          </div>

          <div className="relative my-6 flex items-center justify-center">
            <div className="border-t border-white/[0.08] w-full" />
            <span className="bg-slate-900 px-3 text-[11px] text-slate-500 uppercase tracking-wider absolute">
              Or with credentials
            </span>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Student Email
              </label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="w-full rounded-xl border border-white/[0.1] bg-slate-900/60 py-2.5 pl-10 pr-4 text-xs text-white placeholder-slate-500 focus:border-sky-400 focus:outline-none"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="w-full rounded-xl border border-white/[0.1] bg-slate-900/60 py-2.5 pl-10 pr-4 text-xs text-white placeholder-slate-500 focus:border-sky-400 focus:outline-none"
                />
              </div>
            </div>

            <MagneticButton
              type="submit"
              variant="secondary"
              disabled={loading}
              className="w-full justify-center mt-2"
            >
              <span>{loading ? 'Authenticating...' : 'Sign In'}</span>
              <ArrowRight className="h-4 w-4" />
            </MagneticButton>
          </form>

          <p className="mt-6 text-center text-xs text-slate-400">
            Don't have an account yet?{' '}
            <Link to="/onboarding" className="text-sky-400 hover:text-sky-300 font-semibold">
              Begin profiling
            </Link>
          </p>
        </GlassCard>
      </div>
    </div>
  );
};

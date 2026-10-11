import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Check, ShieldCheck, User, ArrowRight, Loader2 } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

interface GoogleAuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess?: () => void;
  targetRole?: string;
}

export const GoogleAuthModal: React.FC<GoogleAuthModalProps> = ({
  isOpen,
  onClose,
  onSuccess,
  targetRole = 'AI Engineer'
}) => {
  const { googleLogin } = useAuth();
  const [customEmail, setCustomEmail] = useState('');
  const [customName, setCustomName] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Quick-select preset accounts for instant testing
  const presetAccounts = [
    {
      name: 'Sivan Devara',
      email: 'sivan.devara@gmail.com',
      avatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=120&auto=format&fit=crop&q=80',
    },
    {
      name: 'Google Student',
      email: 'student.novapath@gmail.com',
      avatar: 'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=120&auto=format&fit=crop&q=80',
    }
  ];

  const handleSelectAccount = async (account: { name: string; email: string; avatar?: string }) => {
    setIsSubmitting(true);
    setErrorMessage(null);
    try {
      await googleLogin({
        email: account.email,
        name: account.name,
        avatar: account.avatar,
        careerGoal: targetRole
      });
      setIsSubmitting(false);
      onClose();
      if (onSuccess) onSuccess();
    } catch (err: any) {
      setIsSubmitting(false);
      setErrorMessage(err.message || 'Google sign-in failed');
    }
  };

  const handleCustomSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!customEmail.trim() || !customEmail.includes('@')) {
      setErrorMessage('Please enter a valid Google email address');
      return;
    }
    const nameToUse = customName.trim() || customEmail.split('@')[0].replace('.', ' ').replace(/\b\w/g, c => c.toUpperCase());
    await handleSelectAccount({
      name: nameToUse,
      email: customEmail.trim(),
      avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${encodeURIComponent(customEmail.trim())}`
    });
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-md p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 10 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 10 }}
          className="relative w-full max-w-md rounded-3xl border border-white/[0.12] bg-slate-900/95 p-6 sm:p-7 text-white shadow-2xl backdrop-blur-2xl"
        >
          {/* Close button */}
          <button
            onClick={onClose}
            disabled={isSubmitting}
            className="absolute right-4 top-4 rounded-xl p-1.5 text-slate-400 hover:bg-white/[0.06] hover:text-white transition-colors"
          >
            <X className="h-4 w-4" />
          </button>

          {/* Header */}
          <div className="flex items-center gap-3 border-b border-white/[0.08] pb-4">
            <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-2xl bg-white shadow-md">
              <svg className="h-6 w-6" viewBox="0 0 24 24">
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
            </div>
            <div>
              <h2 className="text-base font-bold text-white">Sign in with Google</h2>
              <p className="text-xs text-slate-400">Choose an account to continue to NovaPath AI</p>
            </div>
          </div>

          {errorMessage && (
            <div className="mt-4 rounded-xl border border-rose-500/30 bg-rose-950/40 p-2.5 text-xs text-rose-300">
              {errorMessage}
            </div>
          )}

          {/* Quick select verified accounts */}
          <div className="mt-4 space-y-2">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
              Select Google Account:
            </span>
            {presetAccounts.map((acc) => (
              <button
                key={acc.email}
                disabled={isSubmitting}
                onClick={() => handleSelectAccount(acc)}
                className="w-full flex items-center justify-between rounded-2xl border border-white/[0.08] bg-slate-950/60 p-3 hover:border-sky-400/50 hover:bg-slate-800/60 transition-all text-left group"
              >
                <div className="flex items-center gap-3">
                  <img
                    src={acc.avatar}
                    alt={acc.name}
                    className="h-9 w-9 rounded-full object-cover border border-white/[0.1]"
                  />
                  <div>
                    <span className="text-xs font-bold text-white block group-hover:text-sky-300 transition-colors">
                      {acc.name}
                    </span>
                    <span className="text-[11px] text-slate-400">{acc.email}</span>
                  </div>
                </div>
                <div className="rounded-lg bg-sky-500/10 border border-sky-400/20 px-2 py-0.5 text-[10px] font-semibold text-sky-300">
                  Google SSO
                </div>
              </button>
            ))}
          </div>

          <div className="relative my-4 flex items-center justify-center">
            <div className="w-full border-t border-white/[0.08]" />
            <span className="absolute bg-slate-900 px-3 text-[10px] font-bold uppercase tracking-wider text-slate-400">
              or use another google account
            </span>
          </div>

          {/* Enter another Google Account */}
          <form onSubmit={handleCustomSubmit} className="space-y-3">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Your Full Name (Optional)
              </label>
              <input
                type="text"
                value={customName}
                onChange={(e) => setCustomName(e.target.value)}
                placeholder="e.g. Alex Morgan"
                disabled={isSubmitting}
                className="w-full rounded-xl border border-white/[0.1] bg-slate-950/60 py-2 px-3 text-xs text-white placeholder-slate-500 focus:border-sky-400 focus:outline-none"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Google Email Address
              </label>
              <input
                type="email"
                value={customEmail}
                onChange={(e) => setCustomEmail(e.target.value)}
                placeholder="name@gmail.com"
                required
                disabled={isSubmitting}
                className="w-full rounded-xl border border-white/[0.1] bg-slate-950/60 py-2 px-3 text-xs text-white placeholder-slate-500 focus:border-sky-400 focus:outline-none"
              />
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 py-2.5 text-xs font-bold text-white shadow-neon-blue transition-all hover:scale-[1.02] disabled:opacity-50"
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Authenticating with Google...</span>
                </>
              ) : (
                <>
                  <span>Sign In with this Google Account</span>
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </button>
          </form>

          {/* Privacy badge */}
          <div className="mt-4 flex items-center justify-center gap-1.5 text-[11px] text-slate-400 border-t border-white/[0.06] pt-3">
            <ShieldCheck className="h-3.5 w-3.5 text-emerald-400" />
            <span>Secure OAuth 2.0 Academic Identity Verification</span>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};

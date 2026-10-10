import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'verified' | 'in_progress' | 'ready' | 'locked' | 'highlight' | 'ats_high' | 'rag';
  className?: string;
  icon?: React.ReactNode;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'verified',
  className = '',
  icon,
}) => {
  const styles = {
    verified: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30 shadow-[0_0_12px_rgba(16,185,129,0.2)]',
    in_progress: 'bg-sky-500/10 text-sky-400 border-sky-500/30 shadow-[0_0_12px_rgba(56,189,248,0.2)]',
    ready: 'bg-violet-500/10 text-violet-400 border-violet-500/30 shadow-[0_0_12px_rgba(168,85,247,0.2)]',
    locked: 'bg-slate-800/40 text-slate-400 border-slate-700/40',
    highlight: 'bg-gradient-to-r from-amber-500/20 to-rose-500/20 text-amber-300 border-amber-500/30',
    ats_high: 'bg-emerald-500/15 text-emerald-300 border-emerald-400/40 font-semibold shadow-[0_0_15px_rgba(16,185,129,0.3)]',
    rag: 'bg-indigo-500/15 text-indigo-300 border-indigo-400/30 shadow-[0_0_12px_rgba(99,102,241,0.25)]',
  };

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 text-xs font-medium backdrop-blur-md transition-all ${styles[variant]} ${className}`}
    >
      {icon}
      {children}
    </span>
  );
};

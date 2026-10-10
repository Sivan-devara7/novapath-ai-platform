import React from 'react';
import { Compass, Shield, Sparkles, Heart } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-[var(--border-subtle)] bg-[var(--footer-bg)] py-12 text-[var(--text-secondary)] transition-colors duration-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-3">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-tr from-sky-500 to-indigo-600 p-0.5 shadow-neon-blue">
              <div className="flex h-full w-full items-center justify-center rounded-[6px] bg-slate-950">
                <Compass className="h-4 w-4 text-sky-400" />
              </div>
            </div>
            <div>
              <span className="text-sm font-bold text-white">NovaPath AI</span>
              <span className="text-xs text-slate-500 block">Personalized Learning & Career Intelligence Platform</span>
            </div>
          </div>

          <div className="flex items-center gap-6 text-xs">
            <span className="flex items-center gap-1.5 text-sky-400/90">
              <Sparkles className="h-3.5 w-3.5" />
              Built for Google Antigravity Hackathon 2026
            </span>
            <span className="flex items-center gap-1.5">
              <Shield className="h-3.5 w-3.5 text-emerald-400" />
              RAG Grounded Intelligence
            </span>
          </div>

          <div className="text-xs text-slate-500 flex items-center gap-1">
            <span>Crafted with</span>
            <Heart className="h-3.5 w-3.5 fill-rose-500 text-rose-500 inline" />
            <span>in React 19 + FastAPI</span>
          </div>
        </div>
      </div>
    </footer>
  );
};

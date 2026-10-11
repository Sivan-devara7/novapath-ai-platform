import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  Compass,
  Map,
  BookOpen,
  CheckCircle2,
  FileText,
  Sparkles,
  Flame,
  Zap,
  User,
  LogOut,
  LayoutDashboard
} from 'lucide-react';
import { Globe } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage, SUPPORTED_LANGUAGES, SupportedLanguage } from '../../context/LanguageContext';
import { MagneticButton } from '../ui/MagneticButton';
import { ThemeSwitcher } from '../ui/ThemeSwitcher';

export const Navbar: React.FC = () => {
  const location = useLocation();
  const { user, isAuthenticated, logout } = useAuth();
  const { language, setLanguage, t } = useLanguage();
  const [langMenuOpen, setLangMenuOpen] = React.useState(false);

  const navLinks = [
    { name: t('nav_dashboard', 'Dashboard'), path: '/dashboard', icon: LayoutDashboard },
    { name: t('nav_roadmap', 'Roadmap'), path: '/roadmap', icon: Map },
    { name: t('nav_ats', 'Resume ATS'), path: '/resume', icon: FileText },
    { name: t('nav_projects', 'AI Matches'), path: '/recommendations', icon: Sparkles },
  ];

  return (
    <header className="sticky top-0 z-40 w-full border-b border-[var(--border-subtle)] bg-[var(--navbar-bg)] backdrop-blur-xl transition-colors duration-300">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand Logo */}
        <Link to="/" className="flex items-center gap-2.5 group">
          <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-tr from-sky-500 via-indigo-500 to-violet-500 p-0.5 shadow-[0_0_20px_rgba(56,189,248,0.4)] transition-transform group-hover:scale-105">
            <div className="flex h-full w-full items-center justify-center rounded-[10px] bg-slate-950">
              <Compass className="h-5 w-5 text-sky-400 group-hover:rotate-45 transition-transform duration-300" />
            </div>
          </div>
          <div className="flex flex-col">
            <span className="text-base font-extrabold tracking-tight text-white">
              Nova<span className="text-gradient">Path</span>
            </span>
            <span className="text-[10px] uppercase tracking-wider text-sky-400/80 font-semibold -mt-1">
              AI Career Intelligence
            </span>
          </div>
        </Link>

        {/* Navigation Items (when logged in or browsing) */}
        {isAuthenticated && (
          <nav className="hidden md:flex items-center gap-1 rounded-full border border-white/[0.06] bg-slate-900/60 p-1 backdrop-blur-md">
            {navLinks.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname.startsWith(item.path);
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-2 rounded-full px-3.5 py-1.5 text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-sky-500/20 to-indigo-500/20 text-sky-300 border border-sky-400/30 shadow-[0_0_15px_rgba(56,189,248,0.2)]'
                      : 'text-slate-400 hover:text-white hover:bg-white/[0.04]'
                  }`}
                >
                  <Icon className="h-3.5 w-3.5" />
                  {item.name}
                </Link>
              );
            })}
          </nav>
        )}

        {/* Right Action Area */}
        <div className="flex items-center gap-2.5">
          {/* Visual Theme Selector */}
          <ThemeSwitcher />

          {/* Indian Language Selector Dropdown */}
          <div className="relative">
            <button
              onClick={() => setLangMenuOpen(!langMenuOpen)}
              className="flex items-center gap-1.5 rounded-xl border border-white/[0.08] bg-slate-900/70 px-2.5 py-1.5 text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800 transition-all"
              title="Change Language"
            >
              <Globe className="h-3.5 w-3.5 text-sky-400" />
              <span>{SUPPORTED_LANGUAGES.find((l) => l.code === language)?.nativeName || 'English'}</span>
            </button>

            {langMenuOpen && (
              <div className="absolute right-0 mt-2 w-44 rounded-2xl border border-white/[0.1] bg-slate-900/95 p-1.5 shadow-2xl backdrop-blur-xl z-50">
                <div className="px-2 py-1 text-[10px] font-bold uppercase text-slate-400">
                  Languages of India
                </div>
                {SUPPORTED_LANGUAGES.map((l) => (
                  <button
                    key={l.code}
                    onClick={() => {
                      setLanguage(l.code);
                      setLangMenuOpen(false);
                    }}
                    className={`flex items-center justify-between w-full rounded-xl px-2.5 py-1.5 text-xs text-left transition-colors ${
                      language === l.code
                        ? 'bg-sky-500/20 text-sky-300 font-bold border border-sky-400/30'
                        : 'text-slate-300 hover:bg-white/[0.06] hover:text-white'
                    }`}
                  >
                    <span>{l.nativeName}</span>
                    <span className="text-[10px] text-slate-400">{l.name}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {isAuthenticated && user ? (
            <>
              {/* Streak Tracker */}
              <div
                title="Learning Streak: 14 consecutive days"
                className="flex items-center gap-1.5 rounded-full border border-amber-500/30 bg-amber-500/10 px-3 py-1 text-xs font-semibold text-amber-300 shadow-[0_0_12px_rgba(245,158,11,0.2)]"
              >
                <Flame className="h-3.5 w-3.5 fill-amber-400 text-amber-400 animate-pulse" />
                <span>{user.streak}d Streak</span>
              </div>

              {/* Points Badge */}
              <div
                title="Earned Academic XP"
                className="flex items-center gap-1.5 rounded-full border border-violet-500/30 bg-violet-500/10 px-3 py-1 text-xs font-semibold text-violet-300 shadow-[0_0_12px_rgba(168,85,247,0.2)]"
              >
                <Zap className="h-3.5 w-3.5 text-violet-400 fill-violet-400" />
                <span>{user.points} XP</span>
              </div>

              {/* User Avatar & Logout */}
              <div className="flex items-center gap-2 pl-2">
                <Link
                  to="/profile"
                  className="flex h-8 w-8 items-center justify-center rounded-full border border-sky-400/40 bg-slate-800 text-xs font-bold text-sky-300 shadow-[0_0_10px_rgba(56,189,248,0.3)] hover:scale-105 transition-transform"
                >
                  {user.name.slice(0, 2).toUpperCase()}
                </Link>
                <button
                  onClick={logout}
                  title="Log out"
                  className="rounded-lg p-1.5 text-slate-400 hover:bg-white/[0.06] hover:text-rose-400 transition-colors"
                >
                  <LogOut className="h-4 w-4" />
                </button>
              </div>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <Link to="/login">
                <MagneticButton variant="ghost">{t('nav_login', 'Sign In')}</MagneticButton>
              </Link>
              <Link to="/getting-started">
                <MagneticButton variant="primary">{t('nav_get_started', 'Get Started')}</MagneticButton>
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

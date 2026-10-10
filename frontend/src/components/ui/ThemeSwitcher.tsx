import React, { useState, useRef, useEffect } from 'react';
import { Palette, Sun, Moon, Check, Sparkles } from 'lucide-react';
import { useTheme, THEMES, ThemeId } from '../../context/ThemeContext';

export const ThemeSwitcher: React.FC = () => {
  const { theme, themeMeta, setTheme, isDark, toggleQuickMode } = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const [filter, setFilter] = useState<'all' | 'dark' | 'light'>('all');
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown on outside click
  useEffect(() => {
    const handleOutsideClick = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    if (isOpen) {
      document.addEventListener('mousedown', handleOutsideClick);
    }
    return () => {
      document.removeEventListener('mousedown', handleOutsideClick);
    };
  }, [isOpen]);

  const filteredThemes = THEMES.filter((t) => {
    if (filter === 'all') return true;
    return t.mode === filter;
  });

  return (
    <div className="relative" ref={dropdownRef}>
      {/* Trigger Button Group */}
      <div className="flex items-center gap-1 rounded-full border border-[var(--border-subtle)] bg-[var(--bg-card)] p-0.5 backdrop-blur-md shadow-sm">
        {/* Quick Mode Toggle (Sun/Moon) */}
        <button
          onClick={toggleQuickMode}
          title={isDark ? 'Switch to Nordic Frost (Light)' : 'Switch to Cyber Aurora (Dark)'}
          className="flex h-7 w-7 items-center justify-center rounded-full text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-black/5 dark:hover:bg-white/[0.08] transition-all"
        >
          {isDark ? (
            <Moon className="h-3.5 w-3.5 text-[var(--accent-secondary)]" />
          ) : (
            <Sun className="h-3.5 w-3.5 text-[var(--accent-secondary)]" />
          )}
        </button>

        {/* Theme Palette Dropdown Button */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold text-[var(--text-primary)] hover:bg-black/5 dark:hover:bg-white/[0.06] transition-all"
        >
          {/* Theme Color Dots */}
          <span className="flex items-center -space-x-1">
            <span
              className="h-2.5 w-2.5 rounded-full ring-1 ring-black/20 shadow-sm"
              style={{ backgroundColor: themeMeta.primaryColor }}
            />
            <span
              className="h-2.5 w-2.5 rounded-full ring-1 ring-black/20 shadow-sm"
              style={{ backgroundColor: themeMeta.secondaryColor }}
            />
          </span>
          <span className="hidden sm:inline-block max-w-[90px] truncate text-[11px]">
            {themeMeta.name}
          </span>
          <Palette className="h-3 w-3 text-[var(--text-muted)]" />
        </button>
      </div>

      {/* Floating Theme Selection Menu */}
      {isOpen && (
        <div className="absolute right-0 top-full mt-2 w-72 sm:w-80 rounded-2xl border border-[var(--border-card)] bg-[var(--bg-card)] p-3.5 shadow-2xl backdrop-blur-2xl z-50 text-[var(--text-primary)] animate-in fade-in zoom-in-95 duration-150">
          {/* Header */}
          <div className="flex items-center justify-between pb-3 border-b border-[var(--border-subtle)]">
            <div className="flex items-center gap-1.5">
              <Sparkles className="h-4 w-4 text-[var(--accent-primary)]" />
              <span className="text-xs font-bold uppercase tracking-wider text-[var(--text-primary)]">
                Visual Themes
              </span>
            </div>
            <span className="text-[10px] rounded-full bg-[var(--glow-primary)] px-2 py-0.5 font-semibold text-[var(--accent-primary)] border border-[var(--accent-primary)]/20">
              {THEMES.length} Themes
            </span>
          </div>

          {/* Filter Tabs */}
          <div className="flex rounded-lg bg-[var(--bg-secondary)] p-1 my-2.5 border border-[var(--border-subtle)]">
            <button
              onClick={() => setFilter('all')}
              className={`flex-1 rounded-md py-1 text-[11px] font-medium transition-all ${
                filter === 'all'
                  ? 'bg-[var(--bg-card)] text-[var(--text-primary)] font-semibold shadow-sm'
                  : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilter('dark')}
              className={`flex-1 rounded-md py-1 text-[11px] font-medium transition-all ${
                filter === 'dark'
                  ? 'bg-[var(--bg-card)] text-[var(--text-primary)] font-semibold shadow-sm'
                  : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              Dark (3)
            </button>
            <button
              onClick={() => setFilter('light')}
              className={`flex-1 rounded-md py-1 text-[11px] font-medium transition-all ${
                filter === 'light'
                  ? 'bg-[var(--bg-card)] text-[var(--text-primary)] font-semibold shadow-sm'
                  : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              Light (2)
            </button>
          </div>

          {/* Theme List */}
          <div className="space-y-1.5 max-h-72 overflow-y-auto pr-0.5">
            {filteredThemes.map((item) => {
              const isSelected = item.id === theme;
              return (
                <button
                  key={item.id}
                  onClick={() => {
                    setTheme(item.id as ThemeId);
                    setIsOpen(false);
                  }}
                  className={`w-full flex items-center justify-between rounded-xl p-2.5 text-left transition-all group ${
                    isSelected
                      ? 'border border-[var(--accent-primary)]/40 bg-[var(--glow-primary)] shadow-sm'
                      : 'border border-transparent hover:border-[var(--border-subtle)] hover:bg-black/5 dark:hover:bg-white/[0.04]'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    {/* Swatch preview */}
                    <div
                      className="flex h-8 w-8 items-center justify-center rounded-lg p-0.5 shadow-md border border-white/[0.1]"
                      style={{ background: item.gradient }}
                    >
                      <div className="h-full w-full rounded-[6px] bg-black/30 backdrop-blur-xs flex items-center justify-center">
                        {item.mode === 'dark' ? (
                          <Moon className="h-3 w-3 text-white/90" />
                        ) : (
                          <Sun className="h-3 w-3 text-white/90" />
                        )}
                      </div>
                    </div>

                    {/* Details */}
                    <div>
                      <div className="flex items-center gap-1.5">
                        <span className="text-xs font-semibold text-[var(--text-primary)]">
                          {item.name}
                        </span>
                        <span
                          className={`text-[9px] font-bold px-1.5 py-0.2 rounded-full uppercase tracking-wider ${
                            item.badge === 'DEFAULT'
                              ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                              : item.mode === 'light'
                              ? 'bg-amber-500/20 text-amber-500 border border-amber-500/30'
                              : 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30'
                          }`}
                        >
                          {item.badge}
                        </span>
                      </div>
                      <span className="text-[10px] text-[var(--text-secondary)] block line-clamp-1">
                        {item.tagline}
                      </span>
                    </div>
                  </div>

                  {/* Active Checkmark */}
                  {isSelected && (
                    <div className="flex h-5 w-5 items-center justify-center rounded-full bg-[var(--accent-primary)] text-white shadow-sm">
                      <Check className="h-3 w-3 stroke-[3]" />
                    </div>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
};

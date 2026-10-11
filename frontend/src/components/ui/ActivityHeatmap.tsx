import React, { useState } from 'react';
import { Calendar, Flame, Zap, Trophy, ChevronRight } from 'lucide-react';
import { GlassCard } from './GlassCard';
import { useLanguage } from '../../context/LanguageContext';

interface DayActivity {
  date: string;
  count: number;
  xp: number;
  level: 0 | 1 | 2 | 3 | 4;
}

interface ActivityHeatmapProps {
  totalActiveDays?: number;
  currentStreak?: number;
  longestStreak?: number;
  totalXp?: number;
}

export const ActivityHeatmap: React.FC<ActivityHeatmapProps> = ({
  totalActiveDays = 48,
  currentStreak = 14,
  longestStreak = 21,
  totalXp = 860
}) => {
  const { t } = useLanguage();
  const [hoveredDay, setHoveredDay] = useState<{ date: string; xp: number; count: number } | null>(null);

  // Generate 26 weeks (6 months) of activity data ending today
  const generateActivityDays = (): DayActivity[][] => {
    const weeks: DayActivity[][] = [];
    const today = new Date();
    const daysCount = 26 * 7; // 182 days
    const allDays: DayActivity[] = [];

    // Seed deterministic yet realistic activity pattern
    for (let i = daysCount - 1; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(d.getDate() - i);
      const dateStr = d.toISOString().split('T')[0];

      // Realistic streak active for recent 14 days, with regular past activity
      let count = 0;
      let xp = 0;
      let level: 0 | 1 | 2 | 3 | 4 = 0;

      const dayOfWeek = d.getDay();
      const isRecentStreak = i < 14;
      const pseudoRandom = (d.getDate() * 17 + d.getMonth() * 31) % 100;

      if (isRecentStreak) {
        count = 1 + (pseudoRandom % 4);
        xp = 25 + (pseudoRandom % 35);
        level = (1 + (pseudoRandom % 4)) as any;
      } else if (pseudoRandom > 38 && dayOfWeek !== 0) {
        count = 1 + (pseudoRandom % 3);
        xp = 15 + (pseudoRandom % 25);
        level = (1 + (pseudoRandom % 3)) as any;
      }

      allDays.push({
        date: dateStr,
        count,
        xp,
        level
      });
    }

    // Chunk into 26 columns of 7 days
    for (let w = 0; w < 26; w++) {
      weeks.push(allDays.slice(w * 7, (w + 1) * 7));
    }
    return weeks;
  };

  const weeks = generateActivityDays();
  const months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'];

  const getLevelColor = (level: number) => {
    switch (level) {
      case 1:
        return 'bg-sky-500/30 border-sky-400/40';
      case 2:
        return 'bg-sky-500/60 border-sky-400/60 shadow-[0_0_6px_rgba(56,189,248,0.3)]';
      case 3:
        return 'bg-sky-400 border-sky-300 shadow-[0_0_10px_rgba(56,189,248,0.5)]';
      case 4:
        return 'bg-emerald-400 border-emerald-300 shadow-[0_0_12px_rgba(52,211,153,0.7)]';
      default:
        return 'bg-slate-800/60 border-white/[0.04]';
    }
  };

  return (
    <GlassCard glowColor="blue" className="p-6">
      {/* Header and Stats */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-white/[0.06] pb-4">
        <div>
          <div className="flex items-center gap-2">
            <Calendar className="h-4 w-4 text-sky-400" />
            <h3 className="text-base font-extrabold text-white">{t('profile_heatmap_title', 'Daily Learning Activity Heatmap')}</h3>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Verified study sessions, quiz submissions, and AI lessons completed across the last 6 months.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="rounded-xl border border-amber-500/30 bg-amber-500/10 px-3.5 py-1.5 text-center">
            <span className="text-[10px] uppercase font-bold text-amber-400/80 block">{t('label_streak', 'Current Streak')}</span>
            <span className="text-xs font-black text-amber-300 flex items-center justify-center gap-1">
              <Flame className="h-3.5 w-3.5 fill-amber-400 text-amber-400" />
              {currentStreak} {t('label_days', 'Days')}
            </span>
          </div>

          <div className="rounded-xl border border-sky-400/30 bg-sky-500/10 px-3.5 py-1.5 text-center">
            <span className="text-[10px] uppercase font-bold text-sky-400/80 block">{t('profile_active_days', 'Total Active')}</span>
            <span className="text-xs font-black text-sky-300">
              {totalActiveDays} {t('label_days', 'Days')}
            </span>
          </div>

          <div className="rounded-xl border border-violet-500/30 bg-violet-500/10 px-3.5 py-1.5 text-center hidden md:block">
            <span className="text-[10px] uppercase font-bold text-violet-400/80 block">Longest Streak</span>
            <span className="text-xs font-black text-violet-300 flex items-center justify-center gap-1">
              <Trophy className="h-3 w-3 text-violet-400" />
              {longestStreak} Days
            </span>
          </div>
        </div>
      </div>

      {/* Months Label Row */}
      <div className="mt-4 flex justify-between text-[10px] font-semibold text-slate-400 px-6 max-w-full overflow-hidden">
        {months.map((m, idx) => (
          <span key={idx}>{m}</span>
        ))}
      </div>

      {/* Grid Container */}
      <div className="mt-2 flex items-start gap-1 overflow-x-auto pb-2 scrollbar-none">
        {/* Day-of-week labels */}
        <div className="flex flex-col gap-1 text-[9px] font-semibold text-slate-500 pr-1.5 select-none pt-0.5">
          <span>Mon</span>
          <span className="opacity-0">Tue</span>
          <span>Wed</span>
          <span className="opacity-0">Thu</span>
          <span>Fri</span>
          <span className="opacity-0">Sat</span>
          <span className="opacity-0">Sun</span>
        </div>

        {/* 26 Week Columns */}
        {weeks.map((week, wIdx) => (
          <div key={wIdx} className="flex flex-col gap-1">
            {week.map((day, dIdx) => (
              <div
                key={dIdx}
                onMouseEnter={() => setHoveredDay(day)}
                onMouseLeave={() => setHoveredDay(null)}
                className={`h-3 w-3 rounded-[3px] border transition-all cursor-pointer hover:scale-125 hover:z-20 ${getLevelColor(
                  day.level
                )}`}
              />
            ))}
          </div>
        ))}
      </div>

      {/* Footer Legend & Hover Tooltip */}
      <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 border-t border-white/[0.04] pt-3">
        <div className="flex items-center gap-1.5">
          <span>{t('profile_heatmap_less', 'Less')}</span>
          <span className="h-2.5 w-2.5 rounded-[2px] bg-slate-800 border border-white/[0.04]" />
          <span className="h-2.5 w-2.5 rounded-[2px] bg-sky-500/30 border border-sky-400/40" />
          <span className="h-2.5 w-2.5 rounded-[2px] bg-sky-500/60 border border-sky-400/60" />
          <span className="h-2.5 w-2.5 rounded-[2px] bg-sky-400 border border-sky-300" />
          <span className="h-2.5 w-2.5 rounded-[2px] bg-emerald-400 border border-emerald-300" />
          <span>{t('profile_heatmap_more', 'More Active')}</span>
        </div>

        <div>
          {hoveredDay ? (
            <span className="text-white font-semibold">
              📅 {hoveredDay.date}: <strong className="text-sky-300">{hoveredDay.xp} XP</strong> ({hoveredDay.count} sessions)
            </span>
          ) : (
            <span>💡 Consistent daily activity builds higher recall retention</span>
          )}
        </div>
      </div>
    </GlassCard>
  );
};

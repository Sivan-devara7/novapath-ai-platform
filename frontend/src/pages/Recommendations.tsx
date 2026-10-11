import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import {
  Sparkles,
  Award,
  Briefcase,
  Layers,
  ExternalLink,
  ShieldCheck,
  Clock,
  ArrowRight,
  TrendingUp,
  Target
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { api } from '../services/api';
import { GlassCard } from '../components/ui/GlassCard';
import { MagneticButton } from '../components/ui/MagneticButton';
import { Badge } from '../components/ui/Badge';
import { SkeletonLoader } from '../components/ui/SkeletonLoader';
import { RecommendationItem } from '../types';

export const Recommendations: React.FC = () => {
  const { user } = useAuth();
  const { t } = useLanguage();
  const [recommendations, setRecommendations] = useState<RecommendationItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState('all');
  const [selectedTrack, setSelectedTrack] = useState<string>(() => {
    const goal = (user?.career_goal || '').toLowerCase();
    if (goal.includes('data')) return 'Data Engineer';
    if (goal.includes('cyber') || goal.includes('security')) return 'Cybersecurity Analyst';
    return 'AI Engineer';
  });
  const [selectedLevel, setSelectedLevel] = useState<string>(() => user?.placement_level || 'Intermediate');

  const fetchRecs = async (track = selectedTrack, level = selectedLevel) => {
    setLoading(true);
    try {
      const data = await api.getRecommendations(track, level);
      setRecommendations(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRecs(selectedTrack, selectedLevel);
  }, [selectedTrack, selectedLevel]);

  const filtered = filterType === 'all'
    ? recommendations
    : recommendations.filter(r => r.type === filterType);

  const tabs = [
    { id: 'all', label: 'All Opportunities', icon: Sparkles },
    { id: 'project', label: 'Capstone Projects', icon: Layers },
    { id: 'certification', label: 'Industry Certifications', icon: Award },
    { id: 'internship', label: 'Targeted Internships', icon: Briefcase },
  ];

  return (
    <div className="relative min-h-screen bg-[var(--bg-primary)] pb-20 pt-8 text-[var(--text-primary)] transition-colors duration-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-[var(--border-subtle)] pb-6">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="verified">RAG Profile Matching Engine</Badge>
              <span className="text-xs text-[var(--text-muted)]">Zero-hallucination career intelligence</span>
            </div>
            <h1 className="mt-2 text-2xl sm:text-4xl font-extrabold text-[var(--text-heading)]">
              {t('recom_title', 'Personalized Project & Career Recommendations')}
            </h1>
            <p className="mt-1 text-xs sm:text-sm text-[var(--text-secondary)]">
              {t('recom_subtitle', 'Curated projects, internships, and capstones matched to your track and skill level')}
            </p>
          </div>

          {/* Track & Opportunity Type Switchers */}
          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2.5">
            {/* Track Switcher */}
            <div className="flex rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-card)] p-1">
              {['AI Engineer', 'Data Engineer', 'Cybersecurity Analyst'].map((track) => (
                <button
                  key={track}
                  onClick={() => setSelectedTrack(track)}
                  className={`rounded-lg px-2.5 py-1 text-xs font-semibold transition-all ${
                    selectedTrack === track
                      ? 'bg-[image:var(--accent-gradient)] text-white shadow-neon-blue'
                      : 'text-[var(--text-muted)] hover:text-white'
                  }`}
                >
                  {track}
                </button>
              ))}
            </div>

            {/* Opportunity Type Filter Tabs */}
            <div className="flex flex-wrap items-center gap-1 rounded-xl border border-[var(--border-subtle)] bg-[var(--bg-card)] p-1">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setFilterType(tab.id)}
                    className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold transition-all ${
                      filterType === tab.id
                        ? 'bg-[image:var(--accent-gradient)] text-white shadow-[0_0_15px_var(--glow-primary)]'
                        : 'text-[var(--text-muted)] hover:text-[var(--text-primary)] hover:bg-black/5 dark:hover:bg-white/5'
                    }`}
                  >
                    <Icon className="h-3.5 w-3.5" />
                    {tab.label}
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Content Grid */}
        <div className="mt-8">
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3].map((i) => (
                <GlassCard key={i} className="p-6 h-72 flex flex-col justify-between">
                  <SkeletonLoader lines={4} />
                  <SkeletonLoader lines={1} className="w-1/2 mt-4" />
                </GlassCard>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {filtered.map((item, index) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.08 }}
                >
                  <GlassCard glowColor="violet" className="p-6 h-full flex flex-col justify-between group">
                    <div>
                      {/* Top Badges */}
                      <div className="flex items-center justify-between">
                        <span className="rounded-full bg-[var(--bg-secondary)] border border-[var(--border-subtle)] px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider text-[var(--accent-primary)]">
                          {item.type}
                        </span>
                        <div className="flex items-center gap-1 rounded-full border border-[var(--accent-secondary)]/30 bg-[var(--glow-secondary)] px-2.5 py-0.5 text-xs font-bold text-[var(--accent-secondary)]">
                          <Target className="h-3 w-3 text-[var(--accent-secondary)]" />
                          <span>{item.match_percentage}% Match</span>
                        </div>
                      </div>

                      {/* Title & Organization */}
                      <h3 className="mt-3 text-base font-bold text-[var(--text-heading)] group-hover:text-[var(--accent-secondary)] transition-colors">
                        {item.title}
                      </h3>
                      <div className="mt-1 flex items-center gap-2 text-xs text-[var(--text-muted)]">
                        <span className="text-[var(--text-secondary)] font-medium">{item.organization}</span>
                        <span>•</span>
                        <span className="flex items-center gap-1">
                          <Clock className="h-3 w-3" />
                          {item.duration}
                        </span>
                      </div>

                      {/* Explainable RAG Grounding Box */}
                      <div className="mt-4 rounded-xl border border-[var(--accent-primary)]/20 bg-[var(--bg-secondary)] p-3.5 text-xs">
                        <div className="flex items-center gap-1.5 text-[var(--accent-primary)] font-semibold mb-1">
                          <ShieldCheck className="h-3.5 w-3.5" />
                          <span>Why this matches your profile:</span>
                        </div>
                        <p className="text-[11px] text-[var(--text-secondary)] leading-normal">
                          {item.why_this_matches}
                        </p>
                      </div>

                      {/* Tags */}
                      <div className="mt-4 flex flex-wrap gap-1.5">
                        {item.tags.map((tag) => (
                          <span
                            key={tag}
                            className="rounded-md border border-[var(--border-subtle)] bg-[var(--bg-secondary)] px-2 py-0.5 text-[10px] text-[var(--text-muted)]"
                          >
                            {tag}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* Action Button */}
                    <div className="mt-6 pt-4 border-t border-[var(--border-subtle)]">
                      <a href={item.action_url} className="w-full inline-block">
                        <MagneticButton variant="primary" className="w-full justify-between">
                          <span className="text-xs">
                            {item.type === 'project'
                              ? 'View in Roadmap'
                              : item.type === 'certification'
                              ? 'Official Certification Page'
                              : 'Apply with Optimized Resume'}
                          </span>
                          <ArrowRight className="h-3.5 w-3.5" />
                        </MagneticButton>
                      </a>
                    </div>
                  </GlassCard>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

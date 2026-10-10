import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import {
  BookOpen,
  Search,
  Video,
  FileText,
  Code,
  Sparkles,
  ExternalLink,
  Filter,
  CheckCircle2,
  Clock,
  Star,
  ShieldCheck
} from 'lucide-react';
import { api } from '../services/api';
import { GlassCard } from '../components/ui/GlassCard';
import { MagneticButton } from '../components/ui/MagneticButton';
import { Badge } from '../components/ui/Badge';
import { SkeletonLoader } from '../components/ui/SkeletonLoader';
import { ResourceItem } from '../types';

export const Resources: React.FC = () => {
  const [resources, setResources] = useState<ResourceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeType, setActiveType] = useState('all');
  const [activeSkill, setActiveSkill] = useState('all');

  const fetchResources = async () => {
    setLoading(true);
    try {
      const data = await api.getResources(activeSkill, searchQuery, activeType);
      setResources(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchResources();
    }, 250);
    return () => clearTimeout(timer);
  }, [searchQuery, activeType, activeSkill]);

  const typeTabs = [
    { id: 'all', label: 'All Formats', icon: BookOpen },
    { id: 'video', label: 'Video Blitz', icon: Video },
    { id: 'doc', label: 'Official Docs', icon: FileText },
    { id: 'interactive', label: 'Interactive / Blitz', icon: Code },
    { id: 'paper', label: 'Research Papers', icon: Sparkles },
  ];

  return (
    <div className="relative min-h-screen bg-[var(--bg-primary)] pb-20 pt-8 text-[var(--text-primary)] transition-colors duration-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="border-b border-[var(--border-subtle)] pb-6">
          <div className="flex items-center gap-2">
            <Badge variant="rag">Vector RAG Retrieval Engine</Badge>
            <span className="text-xs text-slate-400">Semantic cosine matching</span>
          </div>
          <h1 className="mt-2 text-2xl sm:text-4xl font-extrabold text-white">
            Grounded Learning <span className="text-gradient">Resources</span>
          </h1>
          <p className="mt-1 text-xs sm:text-sm text-slate-300">
            Every study resource is grounded in verified course syllabi and aligned with your target AI milestones.
          </p>
        </div>

        {/* Search & Filter Bar */}
        <div className="mt-8 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
          {/* Search Input */}
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search concepts, CUDA, LoRA, Attention, RAG..."
              className="w-full rounded-xl border border-white/[0.1] bg-slate-900/70 py-2.5 pl-10 pr-4 text-xs sm:text-sm text-white placeholder-slate-500 focus:border-sky-400 focus:outline-none focus:ring-1 focus:ring-sky-400 backdrop-blur-md"
            />
          </div>

          {/* Type Filter Buttons */}
          <div className="flex flex-wrap items-center gap-1.5 rounded-xl border border-white/[0.07] bg-slate-900/60 p-1">
            {typeTabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveType(tab.id)}
                  className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-semibold transition-all ${
                    activeType === tab.id
                      ? 'bg-sky-500/20 text-sky-300 border border-sky-400/40 shadow-neon-blue'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  <Icon className="h-3.5 w-3.5" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* Resource Cards Grid */}
        <div className="mt-8">
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <GlassCard key={i} className="p-6 h-64 flex flex-col justify-between">
                  <SkeletonLoader lines={4} />
                  <SkeletonLoader lines={1} className="w-1/2 mt-4" />
                </GlassCard>
              ))}
            </div>
          ) : resources.length === 0 ? (
            <div className="py-20 text-center">
              <BookOpen className="mx-auto h-12 w-12 text-slate-600 mb-3" />
              <h3 className="text-lg font-bold text-white">No exact vector matches found</h3>
              <p className="text-xs text-slate-400 mt-1">Try relaxing your search terms or selecting 'All Formats'.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {resources.map((item, index) => (
                <motion.div
                  key={item.id}
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                >
                  <GlassCard glowColor="blue" className="p-6 h-full flex flex-col justify-between group">
                    <div>
                      {/* Top Badges */}
                      <div className="flex items-center justify-between">
                        <span className="rounded-full bg-slate-800/80 border border-white/[0.06] px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider text-sky-400">
                          {item.type}
                        </span>
                        <div className="flex items-center gap-1 text-xs text-amber-400 font-bold">
                          <Star className="h-3 w-3 fill-amber-400" />
                          <span>{item.rating}</span>
                          <span className="text-[10px] text-slate-400 font-normal ml-1">({item.match_score}% Match)</span>
                        </div>
                      </div>

                      {/* Title */}
                      <h3 className="mt-3 text-base font-bold text-white group-hover:text-sky-300 transition-colors line-clamp-2">
                        {item.title}
                      </h3>

                      {/* Provider & Estimated Time */}
                      <div className="mt-1 flex items-center gap-3 text-xs text-slate-400">
                        <span>{item.provider}</span>
                        <span>•</span>
                        <span className="flex items-center gap-1">
                          <Clock className="h-3 w-3" />
                          {item.estimated_time}
                        </span>
                        <span>•</span>
                        <span className="text-slate-300">{item.difficulty}</span>
                      </div>

                      {/* Summary */}
                      <p className="mt-3 text-xs text-slate-300 leading-relaxed line-clamp-3">
                        {item.summary}
                      </p>

                      {/* RAG Grounding Provenance Box */}
                      <div className="mt-4 rounded-xl border border-sky-400/20 bg-sky-950/20 p-3 text-xs">
                        <div className="flex items-center gap-1.5 text-sky-300 font-semibold mb-1">
                          <ShieldCheck className="h-3.5 w-3.5 text-sky-400" />
                          <span>RAG Grounding Rationale:</span>
                        </div>
                        <p className="text-[11px] text-slate-300 leading-normal">
                          {item.grounding_reason}
                        </p>
                      </div>
                    </div>

                    {/* Launch External Link Button */}
                    <div className="mt-6 pt-4 border-t border-white/[0.06]">
                      <a
                        href={item.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="w-full inline-block"
                      >
                        <MagneticButton variant="secondary" className="w-full justify-between">
                          <span className="text-xs">Access Verified Resource</span>
                          <ExternalLink className="h-3.5 w-3.5 text-sky-400" />
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

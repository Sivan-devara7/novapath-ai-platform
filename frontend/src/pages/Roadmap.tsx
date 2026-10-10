import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import confetti from 'canvas-confetti';
import {
  Map,
  CheckCircle2,
  Clock,
  Sparkles,
  Lock,
  ArrowRight,
  Layers,
  ChevronRight,
  BookOpen,
  Award,
  ExternalLink,
  RotateCcw
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../services/api';
import { GlassCard } from '../components/ui/GlassCard';
import { MagneticButton } from '../components/ui/MagneticButton';
import { Badge } from '../components/ui/Badge';
import { SkillNode, SkillGraphResponse } from '../types';

export const Roadmap: React.FC = () => {
  const { user, addPoints, incrementStreak } = useAuth();
  const [roadmap, setRoadmap] = useState<SkillGraphResponse | null>(null);
  const [activeTab, setActiveTab] = useState<'timeline' | 'graph'>('timeline');
  const [selectedNode, setSelectedNode] = useState<SkillNode | null>(null);
  const [careerGoal, setCareerGoal] = useState(user?.career_goal || 'AI Engineer');
  const [isUpdating, setIsUpdating] = useState(false);

  useEffect(() => {
    api.getRoadmap(careerGoal).then((data) => {
      setRoadmap(data);
      if (data.nodes.length > 0 && !selectedNode) {
        setSelectedNode(data.nodes[2] || data.nodes[0]);
      }
    });
  }, [careerGoal]);

  const handleRoleChange = (newRole: string) => {
    setCareerGoal(newRole);
  };

  const handleCompleteMilestone = async (node: SkillNode) => {
    setIsUpdating(true);
    // Fire festive celebration confetti!
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 }
    });

    addPoints(150);
    incrementStreak();

    // Update local state for immediate feedback
    if (roadmap) {
      const updatedNodes = roadmap.nodes.map(n => {
        if (n.id === node.id) {
          return { ...n, status: 'completed' as const, mastery_level: 100 };
        }
        return n;
      });
      setRoadmap({ ...roadmap, nodes: updatedNodes, completion_rate: Math.min(100, roadmap.completion_rate + 15) });
      setSelectedNode(prev => prev ? { ...prev, status: 'completed', mastery_level: 100 } : null);
    }
    setIsUpdating(false);
  };

  return (
    <div className="relative min-h-screen bg-[var(--bg-primary)] pb-20 pt-8 text-[var(--text-primary)] transition-colors duration-300">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        {/* Header & Career Goal Selector */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 border-b border-[var(--border-subtle)] pb-6">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="in_progress">Topological DAG Graph</Badge>
              <span className="text-xs text-slate-400">Personalized to your background</span>
            </div>
            <h1 className="mt-2 text-2xl sm:text-4xl font-extrabold text-white">
              Adaptive Learning <span className="text-gradient">Roadmap</span>
            </h1>
            <p className="mt-1 text-xs sm:text-sm text-slate-300">
              Topologically sorted sequence of competencies with automated prerequisite enforcement.
            </p>
          </div>

          {/* Goal Selector & View Toggle */}
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-1 rounded-xl border border-white/[0.08] bg-slate-900/60 p-1">
              {['AI Engineer', 'Full Stack Developer'].map((role) => (
                <button
                  key={role}
                  onClick={() => handleRoleChange(role)}
                  className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-all ${
                    careerGoal === role
                      ? 'bg-gradient-to-r from-sky-500 to-indigo-600 text-white shadow-neon-blue'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {role}
                </button>
              ))}
            </div>

            {/* View switcher */}
            <div className="flex items-center gap-1 rounded-xl border border-white/[0.08] bg-slate-900/60 p-1">
              <button
                onClick={() => setActiveTab('timeline')}
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-all ${
                  activeTab === 'timeline'
                    ? 'bg-slate-800 text-sky-400 border border-sky-400/20'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Timeline View
              </button>
              <button
                onClick={() => setActiveTab('graph')}
                className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-all ${
                  activeTab === 'graph'
                    ? 'bg-slate-800 text-sky-400 border border-sky-400/20'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                Graph View
              </button>
            </div>
          </div>
        </div>

        {/* Progress Bar Header */}
        <div className="mt-6 flex items-center justify-between rounded-2xl border border-white/[0.06] bg-slate-900/40 p-4 backdrop-blur-md">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-sky-500/10 text-sky-400 border border-sky-400/20">
              <Map className="h-5 w-5" />
            </div>
            <div>
              <span className="text-xs font-bold text-white block">
                {careerGoal} Specialization Path
              </span>
              <span className="text-xs text-slate-400">
                {roadmap?.nodes.filter(n => n.status === 'completed').length} of {roadmap?.nodes.length} Milestones Cleared
              </span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="hidden sm:block text-right">
              <span className="text-xs text-slate-400 block">Overall Trajectory</span>
              <span className="text-sm font-extrabold text-sky-400">{roadmap?.completion_rate || 66}%</span>
            </div>
            <div className="h-3 w-32 sm:w-48 overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full rounded-full bg-gradient-to-r from-sky-400 to-indigo-500 transition-all duration-700"
                style={{ width: `${roadmap?.completion_rate || 66}%` }}
              />
            </div>
          </div>
        </div>

        {/* Main Content Layout */}
        <div className="mt-8 grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Left Column: Timeline or Graph Nodes (7 cols) */}
          <div className="lg:col-span-7">
            {activeTab === 'timeline' ? (
              <div className="relative border-l border-white/[0.1] pl-6 ml-4 space-y-8">
                {roadmap?.nodes.map((node, index) => {
                  const isSelected = selectedNode?.id === node.id;
                  return (
                    <motion.div
                      key={node.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: index * 0.1 }}
                      onClick={() => setSelectedNode(node)}
                      className="relative cursor-pointer group"
                    >
                      {/* Timeline Dot */}
                      <div
                        className={`absolute -left-[35px] top-4 flex h-7 w-7 items-center justify-center rounded-full border transition-all duration-300 ${
                          node.status === 'completed'
                            ? 'bg-sky-500 border-sky-300 shadow-[0_0_15px_#38bdf8] text-slate-950'
                            : node.status === 'in_progress'
                            ? 'bg-violet-600 border-violet-400 shadow-[0_0_15px_#a855f7] text-white animate-pulse'
                            : node.status === 'ready'
                            ? 'bg-emerald-500/20 border-emerald-400 text-emerald-300'
                            : 'bg-slate-900 border-slate-700 text-slate-600'
                        }`}
                      >
                        {node.status === 'completed' ? (
                          <CheckCircle2 className="h-4 w-4" />
                        ) : node.status === 'locked' ? (
                          <Lock className="h-3 w-3" />
                        ) : (
                          <span className="text-[10px] font-black">{index + 1}</span>
                        )}
                      </div>

                      {/* Milestone Card */}
                      <GlassCard
                        glowColor={node.status === 'completed' ? 'blue' : node.status === 'in_progress' ? 'violet' : 'none'}
                        className={`p-5 transition-all ${
                          isSelected
                            ? 'border-sky-400/50 shadow-[0_0_25px_rgba(56,189,248,0.25)] ring-1 ring-sky-400/40'
                            : 'hover:border-white/20'
                        }`}
                      >
                        <div className="flex items-center justify-between">
                          <Badge
                            variant={
                              node.status === 'completed'
                                ? 'verified'
                                : node.status === 'in_progress'
                                ? 'in_progress'
                                : node.status === 'ready'
                                ? 'ready'
                                : 'locked'
                            }
                          >
                            {node.category} • {node.status.replace('_', ' ').toUpperCase()}
                          </Badge>
                          <span className="text-xs text-slate-400 flex items-center gap-1">
                            <Clock className="h-3 w-3" />
                            {node.estimated_hours}h
                          </span>
                        </div>

                        <h3 className="mt-2 text-lg font-bold text-white group-hover:text-sky-300 transition-colors">
                          {node.name}
                        </h3>

                        {node.verified_via && (
                          <p className="mt-1 text-xs text-sky-400/90 font-medium">
                            ✓ {node.verified_via}
                          </p>
                        )}

                        <div className="mt-4 flex items-center justify-between border-t border-white/[0.05] pt-3 text-xs text-slate-400">
                          <span>Mastery: <strong className="text-white">{node.mastery_level}%</strong></span>
                          <span className="text-sky-400 flex items-center gap-1 font-semibold">
                            Inspect Details <ChevronRight className="h-3.5 w-3.5" />
                          </span>
                        </div>
                      </GlassCard>
                    </motion.div>
                  );
                })}
              </div>
            ) : (
              /* Graph View Mode */
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {roadmap?.nodes.map((node) => (
                  <GlassCard
                    key={node.id}
                    onClick={() => setSelectedNode(node)}
                    glowColor={node.status === 'completed' ? 'blue' : 'violet'}
                    className={`p-5 cursor-pointer ${
                      selectedNode?.id === node.id ? 'border-sky-400 ring-1 ring-sky-400' : ''
                    }`}
                  >
                    <div className="flex justify-between items-start">
                      <Badge variant={node.status === 'completed' ? 'verified' : 'in_progress'}>
                        {node.category}
                      </Badge>
                      <span className="text-xs text-slate-400">{node.estimated_hours}h</span>
                    </div>
                    <h4 className="mt-2 font-bold text-white text-base">{node.name}</h4>
                    <p className="mt-1 text-xs text-slate-300 line-clamp-2">
                      {node.milestone_project || 'Comprehensive foundational module'}
                    </p>
                  </GlassCard>
                ))}
              </div>
            )}
          </div>

          {/* Right Column: Selected Milestone Detail Panel (5 cols) */}
          <div className="lg:col-span-5">
            <div className="sticky top-24">
              {selectedNode ? (
                <GlassCard glowColor="blue" className="p-6">
                  <div className="flex items-center justify-between">
                    <span className="text-xs uppercase font-bold tracking-wider text-sky-400">
                      Milestone Deep-Dive
                    </span>
                    <Badge
                      variant={
                        selectedNode.status === 'completed'
                          ? 'verified'
                          : selectedNode.status === 'in_progress'
                          ? 'in_progress'
                          : selectedNode.status === 'ready'
                          ? 'ready'
                          : 'locked'
                      }
                    >
                      {selectedNode.status.replace('_', ' ')}
                    </Badge>
                  </div>

                  <h2 className="mt-3 text-2xl font-bold text-white">
                    {selectedNode.name}
                  </h2>
                  <p className="mt-1 text-xs text-slate-400">
                    Category: <strong className="text-slate-200">{selectedNode.category}</strong> • Duration: <strong className="text-slate-200">{selectedNode.estimated_hours} Hours</strong>
                  </p>

                  {/* Prerequisites */}
                  <div className="mt-5 rounded-xl border border-white/[0.06] bg-slate-900/60 p-4">
                    <span className="text-xs font-bold text-slate-300 block mb-2">Prerequisites Required:</span>
                    {selectedNode.prerequisites.length > 0 ? (
                      <div className="flex flex-wrap gap-2">
                        {selectedNode.prerequisites.map((prereq) => (
                          <span
                            key={prereq}
                            className="rounded-lg border border-sky-400/20 bg-sky-500/10 px-2.5 py-1 text-xs font-medium text-sky-300"
                          >
                            ✓ {prereq.replace('-', ' ').toUpperCase()}
                          </span>
                        ))}
                      </div>
                    ) : (
                      <span className="text-xs text-slate-500">None (Foundational Entry Milestone)</span>
                    )}
                  </div>

                  {/* Required Milestone Capstone */}
                  <div className="mt-4 rounded-xl border border-white/[0.06] bg-slate-900/60 p-4">
                    <div className="flex items-center gap-2 text-xs font-bold text-amber-300 mb-1">
                      <Sparkles className="h-4 w-4" />
                      <span>Portfolio Validation Capstone:</span>
                    </div>
                    <p className="text-xs text-slate-300 leading-relaxed">
                      {selectedNode.milestone_project || 'Comprehensive algorithmic implementation repository.'}
                    </p>
                  </div>

                  {/* Action Buttons */}
                  <div className="mt-6 flex flex-col gap-3">
                    <Link to="/assessment" className="w-full">
                      <MagneticButton variant="primary" className="w-full justify-center">
                        <Award className="h-4 w-4" />
                        <span>Launch Adaptive Assessment for this Skill</span>
                      </MagneticButton>
                    </Link>

                    <Link to="/resources" className="w-full">
                      <MagneticButton variant="secondary" className="w-full justify-center">
                        <BookOpen className="h-4 w-4 text-sky-400" />
                        <span>Explore Grounded Study Resources</span>
                      </MagneticButton>
                    </Link>

                    {selectedNode.status !== 'completed' && (
                      <MagneticButton
                        onClick={() => handleCompleteMilestone(selectedNode)}
                        disabled={isUpdating}
                        variant="glow"
                        className="w-full justify-center"
                      >
                        <CheckCircle2 className="h-4 w-4" />
                        <span>Mark Milestone as Cleared (+150 XP)</span>
                      </MagneticButton>
                    )}
                  </div>
                </GlassCard>
              ) : (
                <GlassCard className="p-8 text-center text-slate-400">
                  Select any milestone node on the timeline to inspect syllabus details.
                </GlassCard>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

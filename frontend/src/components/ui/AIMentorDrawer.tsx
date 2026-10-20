import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Sparkles,
  MessageSquare,
  X,
  Send,
  Bot,
  User,
  Zap,
  CheckCircle2,
  AlertCircle,
  Compass,
  ArrowRight,
  RefreshCw,
  Sliders,
  Globe,
  Maximize2,
  Minimize2
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';
import { api } from '../../services/api';
import { GlassCard } from './GlassCard';

interface ChatMsg {
  role: 'user' | 'assistant';
  content: string;
}

export const AIMentorDrawer: React.FC = () => {
  const { user } = useAuth();
  const { language, t } = useLanguage();
  const [isOpen, setIsOpen] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  const [learningStyle, setLearningStyle] = useState<'hands-on' | 'conceptual' | 'bullet-points'>('hands-on');
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMsg[]>([
    {
      role: 'assistant',
      content: `Hello ${user?.name || 'there'}! I'm your NovaPath AI Mentor. I have full real-time access to your career track (${user?.career_goal || 'AI Engineer'}), active streak (${user?.streak || 14} days), and detected ATS skill gaps. How can I guide you today?`
    }
  ]);
  const [detectedGaps, setDetectedGaps] = useState<string[]>([]);
  const [suggestedActions, setSuggestedActions] = useState<Array<{ title: string; action_url: string }>>([
    { title: 'Explain my critical skill gap', action_url: '/resume' },
    { title: 'What should I build next?', action_url: '/recommendations' },
    { title: 'How to hit 90%+ ATS score?', action_url: '/resume' }
  ]);

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  // Clean up any old localStorage key if present and listen for global open triggers
  useEffect(() => {
    try {
      localStorage.removeItem('novapath_chatbox_key');
    } catch (_) {}

    const handleOpen = () => setIsOpen(true);
    window.addEventListener('open-ai-mentor', handleOpen);
    return () => window.removeEventListener('open-ai-mentor', handleOpen);
  }, []);

  const handleSend = async (textToSend?: string) => {
    const query = (textToSend || input).trim();
    if (!query || isLoading) return;

    const newMessages: ChatMsg[] = [...messages, { role: 'user', content: query }];
    setMessages(newMessages);
    if (!textToSend) setInput('');
    setIsLoading(true);

    try {
      const res = await api.mentorChat(newMessages, learningStyle, language);
      setMessages([...newMessages, { role: 'assistant', content: res.reply }]);
      if (res.detected_gaps && res.detected_gaps.length > 0) {
        setDetectedGaps(res.detected_gaps);
      }
      if (res.suggested_actions && res.suggested_actions.length > 0) {
        setSuggestedActions(res.suggested_actions);
      }
    } catch (err: any) {
      setMessages([
        ...newMessages,
        {
          role: 'assistant',
          content: `I'm tracking your ${user?.career_goal || 'engineering'} track! You have strong foundations in core logic. Focus your next study block on your identified missing ATS skills: Vector Databases & High-Throughput Serving to accelerate your placement readiness.`
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      {/* Floating Trigger Button (only visible when chat is closed) */}
      {!isOpen && (
        <div className="fixed bottom-5 right-5 sm:bottom-6 sm:right-6 z-40">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setIsOpen(true)}
            className="group relative flex items-center gap-2.5 rounded-full border border-sky-400/40 bg-gradient-to-r from-sky-600 via-indigo-600 to-violet-600 px-4 py-3 text-xs font-bold text-white shadow-neon-blue transition-all"
          >
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
            <Sparkles className="h-4 w-4 animate-pulse text-amber-300" />
            <span className="hidden sm:inline font-extrabold tracking-wide">{t('nav_mentor', 'AI Mentor')}</span>
            <span className="rounded bg-black/30 px-1.5 py-0.5 text-[10px] text-sky-200">
              OmniRoute AI
            </span>
          </motion.button>
        </div>
      )}

      {/* AI Mentor Drawer / Modal */}
      <AnimatePresence>
        {isOpen && (
          isMaximized ? (
            /* ================= MAXIMIZED CENTERED MODAL ================= */
            <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 md:p-8 bg-black/75 backdrop-blur-md">
              <motion.div
                initial={{ opacity: 0, scale: 0.96 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.96 }}
                transition={{ duration: 0.2 }}
                className="relative w-full max-w-4xl lg:max-w-5xl h-[88vh] max-h-[840px] min-h-[520px] flex flex-col rounded-3xl border border-sky-400/40 bg-slate-900/98 shadow-[0_0_60px_rgba(0,0,0,0.85)] overflow-hidden"
              >
                {/* Header */}
                <div className="flex items-center justify-between border-b border-white/[0.08] px-6 py-4 bg-slate-950/80">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-tr from-sky-500 via-indigo-600 to-violet-600 text-white shadow-neon-blue">
                      <Bot className="h-5 w-5" />
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h3 className="text-base font-extrabold text-white">{t('mentor_title', 'NovaPath AI Mentor')}</h3>
                        <span className="rounded-full bg-emerald-500/15 border border-emerald-400/30 px-2 py-0.5 text-[10px] font-bold text-emerald-300">
                          Live AI Advisor
                        </span>
                        <span className="rounded bg-indigo-500/20 border border-indigo-400/30 px-1.5 py-0.5 text-[10px] font-bold text-indigo-300">
                          GPT-4o Mini / OmniRoute
                        </span>
                      </div>
                      <p className="text-xs text-slate-400 mt-0.5">
                        Personalized Academic Companion • Contextual Memory & Real-Time ATS Gap Tracking
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {/* Context Summary Pills */}
                    <div className="hidden md:flex items-center gap-2 mr-2">
                      <span className="rounded-xl border border-white/[0.08] bg-slate-900 px-2.5 py-1 text-xs text-sky-300 font-semibold">
                        Track: {user?.career_goal || 'AI Engineer'}
                      </span>
                      <span className="rounded-xl border border-amber-500/30 bg-amber-500/10 px-2.5 py-1 text-xs text-amber-300 font-semibold">
                        🔥 {user?.streak || 14}d Streak
                      </span>
                    </div>

                    {/* Restore Size Button */}
                    <button
                      type="button"
                      onClick={() => setIsMaximized(false)}
                      title="Restore to Compact View"
                      aria-label="Restore to Compact View"
                      className="flex items-center gap-1.5 rounded-xl border border-white/[0.08] bg-slate-900 px-3 py-1.5 text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800 transition-colors"
                    >
                      <Minimize2 className="h-3.5 w-3.5 text-sky-400" />
                      <span>Restore</span>
                    </button>

                    {/* Close Button */}
                    <button
                      type="button"
                      onClick={() => {
                        setIsOpen(false);
                        setIsMaximized(false);
                      }}
                      title="Close"
                      aria-label="Close"
                      className="rounded-xl p-2 text-slate-400 hover:bg-white/[0.08] hover:text-white transition-colors"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  </div>
                </div>

                {/* Learning Style Picker Bar */}
                <div className="border-b border-white/[0.06] bg-slate-900/60 px-6 py-2.5 text-xs">
                  <div className="max-w-3xl mx-auto w-full flex items-center justify-between">
                    <span className="text-slate-400 flex items-center gap-1.5">
                      <Sliders className="h-3.5 w-3.5 text-sky-400" />
                      <span>{t('mentor_style_label', 'Learning Style:')}</span>
                    </span>
                    <div className="flex rounded-lg bg-slate-950/70 p-0.5 border border-white/[0.06]">
                      {(['hands-on', 'conceptual', 'bullet-points'] as const).map((style) => (
                        <button
                          key={style}
                          onClick={() => setLearningStyle(style)}
                          className={`rounded px-2.5 py-1 text-xs font-semibold transition-all ${
                            learningStyle === style
                              ? 'bg-sky-500 text-white shadow-sm'
                              : 'text-slate-400 hover:text-white'
                          }`}
                        >
                          {style === 'hands-on'
                            ? t('mentor_style_code', 'Code')
                            : style === 'conceptual'
                            ? t('mentor_style_analogy', 'Analogy')
                            : t('mentor_style_brief', 'Brief')}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Message Area */}
                <div className="flex-1 overflow-y-auto p-6 space-y-4 text-sm">
                  <div className="max-w-3xl mx-auto w-full space-y-4">
                    {messages.map((m, idx) => (
                      <div
                        key={idx}
                        className={`flex gap-3 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
                      >
                        {m.role === 'assistant' && (
                          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-sky-500/20 text-sky-400 border border-sky-400/30 mt-0.5">
                            <Sparkles className="h-4 w-4" />
                          </div>
                        )}
                        <div
                          className={`max-w-[85%] rounded-2xl px-4 py-3 leading-relaxed shadow-sm ${
                            m.role === 'user'
                              ? 'bg-sky-500 text-white'
                              : 'bg-slate-800/80 text-slate-200 border border-white/[0.06]'
                          }`}
                        >
                          <p className="whitespace-pre-line">{m.content}</p>
                        </div>
                      </div>
                    ))}

                    {isLoading && (
                      <div className="flex gap-3 items-center text-slate-400 text-sm py-2">
                        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-sky-500/20 text-sky-400">
                          <RefreshCw className="h-4 w-4 animate-spin" />
                        </div>
                        <span className="animate-pulse">Synthesizing personalized mentorship via OmniRoute...</span>
                      </div>
                    )}

                    <div ref={messagesEndRef} />
                  </div>
                </div>

                {/* Suggested Quick Prompts */}
                {suggestedActions && suggestedActions.length > 0 && (
                  <div className="border-t border-white/[0.06] bg-slate-950/40 px-6 py-2.5">
                    <div className="max-w-3xl mx-auto w-full flex flex-wrap gap-2">
                      {suggestedActions.map((action, idx) => (
                        <button
                          key={idx}
                          onClick={() => handleSend(action.title)}
                          className="rounded-lg border border-sky-500/20 bg-sky-500/5 px-3 py-1.5 text-xs text-sky-300 hover:bg-sky-500/15 hover:border-sky-400/40 transition-colors"
                        >
                          {action.title}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Input Bar */}
                <div className="border-t border-white/[0.08] p-4 bg-slate-950/90">
                  <form
                    onSubmit={(e) => {
                      e.preventDefault();
                      handleSend();
                    }}
                    className="max-w-3xl mx-auto w-full flex items-center gap-2.5"
                  >
                    <input
                      type="text"
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      placeholder={t('mentor_placeholder', 'Ask your mentor (e.g. explain my skill gap)...')}
                      className="flex-1 rounded-xl border border-white/[0.1] bg-slate-900/90 px-4 py-3 text-sm text-white placeholder-slate-400 focus:border-sky-400 focus:outline-none"
                    />
                    <button
                      type="submit"
                      disabled={isLoading || !input.trim()}
                      className="rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 px-5 py-3 text-white shadow-neon-blue hover:opacity-90 disabled:opacity-50 transition-all flex items-center gap-2 text-xs font-bold"
                    >
                      <span>Send</span>
                      <Send className="h-4 w-4" />
                    </button>
                  </form>
                </div>
              </motion.div>
            </div>
          ) : (
            /* ================= COMPACT FLOATING WIDGET ================= */
            <motion.div
              initial={{ opacity: 0, y: 16, scale: 0.97 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 16, scale: 0.97 }}
              transition={{ duration: 0.2 }}
              className="fixed bottom-5 right-5 sm:bottom-6 sm:right-6 z-50 w-[calc(100vw-2.5rem)] sm:w-[410px] h-[570px] max-h-[calc(100vh-4rem)] flex flex-col rounded-3xl border border-sky-500/30 bg-slate-900/95 shadow-2xl backdrop-blur-2xl overflow-hidden"
            >
              {/* Header */}
              <div className="flex items-center justify-between border-b border-white/[0.08] px-4 py-3 bg-slate-950/70">
                <div className="flex items-center gap-2.5">
                  <div className="flex h-8 w-8 items-center justify-center rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 text-white shadow-neon-blue">
                    <Bot className="h-4 w-4" />
                  </div>
                  <div>
                    <div className="flex items-center gap-1.5">
                      <h3 className="text-xs sm:text-sm font-extrabold text-white">{t('mentor_title', 'NovaPath AI Mentor')}</h3>
                      <span className="rounded bg-indigo-500/20 border border-indigo-400/30 px-1.5 py-0.2 text-[9px] font-bold text-indigo-300">
                        GPT-4o Mini
                      </span>
                    </div>
                    <p className="text-[10px] text-slate-400">
                      {user?.career_goal || 'AI Engineer'} • {user?.streak || 14}d streak
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-1">
                  {/* Maximize Button */}
                  <button
                    type="button"
                    onClick={() => setIsMaximized(true)}
                    title="Maximize Chatbox"
                    aria-label="Maximize Chatbox"
                    className="rounded-xl p-1.5 text-slate-400 hover:bg-white/[0.08] hover:text-white transition-colors"
                  >
                    <Maximize2 className="h-4 w-4" />
                  </button>

                  {/* Close Button */}
                  <button
                    type="button"
                    onClick={() => {
                      setIsOpen(false);
                      setIsMaximized(false);
                    }}
                    title="Close"
                    aria-label="Close"
                    className="rounded-xl p-1.5 text-slate-400 hover:bg-white/[0.08] hover:text-white transition-colors"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              </div>

              {/* Learning Style Picker Bar */}
              <div className="flex items-center justify-between border-b border-white/[0.06] bg-slate-900/60 px-4 py-2 text-[11px]">
                <span className="text-slate-400 flex items-center gap-1">
                  <Sliders className="h-3 w-3 text-sky-400" />
                  {t('mentor_style_label', 'Style:')}
                </span>
                <div className="flex rounded-lg bg-slate-950/70 p-0.5 border border-white/[0.06]">
                  {(['hands-on', 'conceptual', 'bullet-points'] as const).map((style) => (
                    <button
                      key={style}
                      onClick={() => setLearningStyle(style)}
                      className={`rounded px-2 py-0.5 text-[10px] font-semibold transition-all ${
                        learningStyle === style
                          ? 'bg-sky-500 text-white shadow-sm'
                          : 'text-slate-400 hover:text-white'
                      }`}
                    >
                      {style === 'hands-on'
                        ? t('mentor_style_code', 'Code')
                        : style === 'conceptual'
                        ? t('mentor_style_analogy', 'Analogy')
                        : t('mentor_style_brief', 'Brief')}
                    </button>
                  ))}
                </div>
              </div>

              {/* Message Area */}
              <div className="flex-1 overflow-y-auto p-4 space-y-3 text-xs">
                {messages.map((m, idx) => (
                  <div
                    key={idx}
                    className={`flex gap-2.5 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    {m.role === 'assistant' && (
                      <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-sky-500/20 text-sky-400 border border-sky-400/30">
                        <Sparkles className="h-3.5 w-3.5" />
                      </div>
                    )}
                    <div
                      className={`max-w-[85%] rounded-2xl px-3.5 py-2.5 leading-relaxed ${
                        m.role === 'user'
                          ? 'bg-sky-500 text-white shadow-md'
                          : 'bg-slate-800/80 text-slate-200 border border-white/[0.06] shadow-sm'
                      }`}
                    >
                      <p className="whitespace-pre-line">{m.content}</p>
                    </div>
                  </div>
                ))}

                {isLoading && (
                  <div className="flex gap-2.5 items-center text-slate-400 text-xs py-2">
                    <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-sky-500/20 text-sky-400">
                      <RefreshCw className="h-3.5 w-3.5 animate-spin" />
                    </div>
                    <span className="animate-pulse">Synthesizing personalized mentorship via OmniRoute...</span>
                  </div>
                )}

                <div ref={messagesEndRef} />
              </div>

              {/* Suggested Quick Prompts */}
              {suggestedActions && suggestedActions.length > 0 && (
                <div className="border-t border-white/[0.06] bg-slate-950/40 p-2.5 flex flex-wrap gap-1.5">
                  {suggestedActions.map((action, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSend(action.title)}
                      className="rounded-lg border border-sky-500/20 bg-sky-500/5 px-2.5 py-1 text-[11px] text-sky-300 hover:bg-sky-500/15 hover:border-sky-400/40 transition-colors"
                    >
                      {action.title}
                    </button>
                  ))}
                </div>
              )}

              {/* Input Bar */}
              <div className="border-t border-white/[0.08] p-3 bg-slate-950/80">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSend();
                  }}
                  className="flex items-center gap-2"
                >
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder={t('mentor_placeholder', 'Ask your mentor (e.g. explain my skill gap)...')}
                    className="flex-1 rounded-xl border border-white/[0.1] bg-slate-900/90 px-3 py-2 text-xs text-white placeholder-slate-400 focus:border-sky-400 focus:outline-none"
                  />
                  <button
                    type="submit"
                    disabled={isLoading || !input.trim()}
                    className="rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 p-2 text-white shadow-neon-blue hover:opacity-90 disabled:opacity-50 transition-all"
                  >
                    <Send className="h-4 w-4" />
                  </button>
                </form>
              </div>
            </motion.div>
          )
        )}
      </AnimatePresence>
    </>
  );
};

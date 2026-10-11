import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertTriangle, XCircle, Maximize2, Clock, ShieldAlert, Check } from 'lucide-react';

interface QuizProctoringModalsProps {
  showWarningModal: boolean;
  showCancelledModal: boolean;
  onAcknowledgeWarning: () => void;
  onCloseCancelledModal: () => void;
  lockoutRemainingText: string;
}

export const QuizProctoringModals: React.FC<QuizProctoringModalsProps> = ({
  showWarningModal,
  showCancelledModal,
  onAcknowledgeWarning,
  onCloseCancelledModal,
  lockoutRemainingText
}) => {
  return (
    <>
      {/* Violation 1 Warning Modal */}
      <AnimatePresence>
        {showWarningModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/85 backdrop-blur-md p-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 20 }}
              className="relative w-full max-w-lg rounded-3xl border-2 border-amber-500/50 bg-slate-950 p-7 text-white shadow-[0_0_50px_rgba(245,158,11,0.3)] backdrop-blur-2xl"
            >
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-amber-500/20 border border-amber-500/40 text-amber-400 mb-4 animate-pulse">
                <AlertTriangle className="h-8 w-8" />
              </div>

              <div className="text-center">
                <span className="inline-block rounded-full border border-amber-400/40 bg-amber-400/10 px-3 py-1 text-xs font-bold uppercase tracking-wider text-amber-300">
                  Proctoring Alert • Violation 1 of 2
                </span>
                <h3 className="mt-3 text-xl sm:text-2xl font-black text-white">
                  Fullscreen Mode Exited!
                </h3>
                <p className="mt-3 text-xs sm:text-sm text-slate-300 leading-relaxed">
                  You have exited the full screen examination environment or switched tabs.
                  NovaPath AI academic proctoring requires continuous full screen mode.
                </p>
                <div className="mt-4 rounded-2xl border border-rose-500/30 bg-rose-950/40 p-3.5 text-xs text-rose-300 font-semibold">
                  ⚠️ <strong>Final Warning:</strong> You have 1 violation remaining.
                  Exiting full screen one more time will <strong>immediately cancel your test</strong> and enforce a mandatory <strong>24-hour lockout</strong> before you can retake it.
                </div>
              </div>

              <div className="mt-6 flex justify-center">
                <button
                  type="button"
                  onClick={onAcknowledgeWarning}
                  className="w-full flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-amber-500 to-orange-600 px-6 py-3 text-xs sm:text-sm font-bold text-slate-950 shadow-lg hover:scale-[1.02] transition-all"
                >
                  <Maximize2 className="h-4 w-4" />
                  <span>Re-enter Fullscreen & Continue Test</span>
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>

      {/* Violation 2 Test Cancelled Modal */}
      <AnimatePresence>
        {showCancelledModal && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-md p-4">
            <motion.div
              initial={{ opacity: 0, scale: 0.9, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9, y: 20 }}
              className="relative w-full max-w-lg rounded-3xl border-2 border-rose-500/50 bg-slate-950 p-7 text-white shadow-[0_0_60px_rgba(244,63,94,0.35)] backdrop-blur-2xl"
            >
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-rose-500/20 border border-rose-500/40 text-rose-400 mb-4">
                <XCircle className="h-9 w-9" />
              </div>

              <div className="text-center">
                <span className="inline-block rounded-full border border-rose-400/40 bg-rose-500/20 px-3 py-1 text-xs font-bold uppercase tracking-wider text-rose-300">
                  Test Cancelled • 2 Violations Exceeded
                </span>
                <h3 className="mt-3 text-xl sm:text-2xl font-black text-white">
                  Assessment Terminated
                </h3>
                <p className="mt-3 text-xs sm:text-sm text-slate-300 leading-relaxed">
                  You exited full screen mode twice during this examination session.
                  In accordance with exam policy, your test has been <strong>cancelled</strong>.
                </p>

                {/* 24-hour lockout notice */}
                <div className="mt-5 rounded-2xl border border-rose-500/40 bg-gradient-to-b from-rose-950/60 to-slate-900/80 p-4 text-center">
                  <div className="flex items-center justify-center gap-2 text-xs font-bold text-rose-300 uppercase tracking-wider mb-1">
                    <Clock className="h-4 w-4" />
                    <span>24-Hour Lockout Active</span>
                  </div>
                  <p className="text-xs text-slate-300">
                    This test will be conducted again after 24 hours.
                  </p>
                  <div className="mt-2 text-lg sm:text-xl font-extrabold text-amber-400 font-mono">
                    {lockoutRemainingText || '24h 00m 00s remaining'}
                  </div>
                </div>
              </div>

              <div className="mt-6 flex justify-center">
                <button
                  type="button"
                  onClick={onCloseCancelledModal}
                  className="w-full rounded-xl bg-slate-800 hover:bg-slate-700 px-6 py-3 text-xs sm:text-sm font-bold text-white transition-all border border-white/[0.1]"
                >
                  Acknowledge & Exit
                </button>
              </div>
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
};

export const QuizLockoutBanner: React.FC<{ remainingText: string }> = ({ remainingText }) => {
  return (
    <div className="rounded-2xl border border-rose-500/30 bg-gradient-to-b from-rose-950/40 to-slate-900/80 p-6 text-center max-w-xl mx-auto backdrop-blur-xl">
      <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-rose-500/20 text-rose-400 border border-rose-500/30 mb-3">
        <ShieldAlert className="h-6 w-6" />
      </div>
      <span className="rounded-full border border-rose-500/40 bg-rose-500/10 px-3 py-0.5 text-[11px] font-bold text-rose-300 uppercase tracking-wider">
        Test Cancelled Due to Fullscreen Violations
      </span>
      <h3 className="mt-3 text-lg font-bold text-white">
        Retake Conducted After 24 Hours
      </h3>
      <p className="mt-2 text-xs text-slate-300 leading-relaxed">
        This test session was cancelled because the user came out of full screen mode twice.
        To maintain testing integrity, retakes are unlocked 24 hours after cancellation.
      </p>
      <div className="mt-4 flex items-center justify-center gap-2 rounded-xl bg-slate-950/70 p-3 border border-white/[0.08]">
        <Clock className="h-4 w-4 text-amber-400" />
        <span className="text-xs text-slate-400">Time Until Retake:</span>
        <strong className="text-sm font-mono font-bold text-amber-300">{remainingText}</strong>
      </div>
    </div>
  );
};

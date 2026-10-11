import { useState, useEffect, useCallback, useRef } from 'react';

interface UseQuizProctoringOptions {
  quizId: string;
  isQuizActive: boolean;
  onCancelQuiz: () => void;
}

export function useQuizProctoring({
  quizId,
  isQuizActive,
  onCancelQuiz
}: UseQuizProctoringOptions) {
  const [violations, setViolations] = useState<number>(0);
  const [showWarningModal, setShowWarningModal] = useState<boolean>(false);
  const [showCancelledModal, setShowCancelledModal] = useState<boolean>(false);
  const [isLockedOut, setIsLockedOut] = useState<boolean>(false);
  const [lockoutRemainingText, setLockoutRemainingText] = useState<string>('');
  const [lockoutExpiresAt, setLockoutExpiresAt] = useState<number | null>(null);

  const storageKey = `novapath_quiz_lockout_${quizId}`;
  const isCleanExitRef = useRef<boolean>(false);

  // Helper to format remaining time
  const formatRemaining = (ms: number): string => {
    if (ms <= 0) return '0s';
    const totalSecs = Math.floor(ms / 1000);
    const hours = Math.floor(totalSecs / 3600);
    const minutes = Math.floor((totalSecs % 3600) / 60);
    const seconds = totalSecs % 60;
    return `${hours}h ${minutes}m ${seconds}s`;
  };

  // Check 24-hour lockout status
  const checkLockout = useCallback(() => {
    try {
      const stored = localStorage.getItem(storageKey);
      if (stored) {
        const expiresAt = parseInt(stored, 10);
        const now = Date.now();
        if (now < expiresAt) {
          setIsLockedOut(true);
          setLockoutExpiresAt(expiresAt);
          setLockoutRemainingText(formatRemaining(expiresAt - now));
          return true;
        } else {
          // Cooldown expired
          localStorage.removeItem(storageKey);
          setIsLockedOut(false);
          setLockoutExpiresAt(null);
          setLockoutRemainingText('');
          return false;
        }
      }
    } catch (e) {
      console.warn('Error reading lockout storage:', e);
    }
    setIsLockedOut(false);
    return false;
  }, [storageKey]);

  // Keep countdown timer updated every second if locked out
  useEffect(() => {
    checkLockout();
    const interval = setInterval(() => {
      checkLockout();
    }, 1000);
    return () => clearInterval(interval);
  }, [checkLockout]);

  // Request fullscreen
  const requestFullscreen = useCallback(async () => {
    try {
      const docEl = document.documentElement as any;
      if (docEl.requestFullscreen) {
        await docEl.requestFullscreen();
      } else if (docEl.webkitRequestFullscreen) {
        await docEl.webkitRequestFullscreen();
      } else if (docEl.msRequestFullscreen) {
        await docEl.msRequestFullscreen();
      }
    } catch (err) {
      console.warn('Fullscreen request rejected or not permitted:', err);
    }
  }, []);

  // Exit fullscreen cleanly (when test submitted legitimately)
  const exitFullscreenCleanly = useCallback(() => {
    isCleanExitRef.current = true;
    try {
      if (document.fullscreenElement || (document as any).webkitFullscreenElement) {
        if (document.exitFullscreen) {
          document.exitFullscreen().catch(() => {});
        } else if ((document as any).webkitExitFullscreen) {
          (document as any).webkitExitFullscreen();
        }
      }
    } catch (e) {}
  }, []);

  // Handle re-entering fullscreen from warning modal
  const handleAcknowledgeWarning = useCallback(async () => {
    setShowWarningModal(false);
    await requestFullscreen();
  }, [requestFullscreen]);

  // Monitor Fullscreen and Tab Visibility
  useEffect(() => {
    if (!isQuizActive) {
      setViolations(0);
      setShowWarningModal(false);
      return;
    }

    isCleanExitRef.current = false;

    const handleViolationTrigger = () => {
      if (isCleanExitRef.current || !isQuizActive) return;

      const isStillFullscreen = !!(document.fullscreenElement || (document as any).webkitFullscreenElement);
      const isDocumentHidden = document.hidden;

      // If user came out of fullscreen or hid document
      if (!isStillFullscreen || isDocumentHidden) {
        setViolations((prev) => {
          const nextCount = prev + 1;
          if (nextCount === 1) {
            // First violation: Show Warning Modal
            setShowWarningModal(true);
          } else if (nextCount >= 2) {
            // Second violation: Cancel test and lock for 24 hours
            const lockoutUntil = Date.now() + 24 * 60 * 60 * 1000;
            localStorage.setItem(storageKey, lockoutUntil.toString());
            setIsLockedOut(true);
            setLockoutExpiresAt(lockoutUntil);
            setLockoutRemainingText(formatRemaining(24 * 60 * 60 * 1000));
            setShowWarningModal(false);
            setShowCancelledModal(true);
            onCancelQuiz();
            exitFullscreenCleanly();
          }
          return nextCount;
        });
      }
    };

    const onFullscreenChange = () => {
      const isStillFullscreen = !!(document.fullscreenElement || (document as any).webkitFullscreenElement);
      if (!isStillFullscreen) {
        handleViolationTrigger();
      }
    };

    const onVisibilityChange = () => {
      if (document.hidden) {
        handleViolationTrigger();
      }
    };

    document.addEventListener('fullscreenchange', onFullscreenChange);
    document.addEventListener('webkitfullscreenchange', onFullscreenChange);
    document.addEventListener('visibilitychange', onVisibilityChange);

    return () => {
      document.removeEventListener('fullscreenchange', onFullscreenChange);
      document.removeEventListener('webkitfullscreenchange', onFullscreenChange);
      document.removeEventListener('visibilitychange', onVisibilityChange);
    };
  }, [isQuizActive, storageKey, onCancelQuiz, exitFullscreenCleanly]);

  return {
    violations,
    showWarningModal,
    showCancelledModal,
    setShowCancelledModal,
    isLockedOut,
    lockoutRemainingText,
    lockoutExpiresAt,
    requestFullscreen,
    exitFullscreenCleanly,
    handleAcknowledgeWarning
  };
}

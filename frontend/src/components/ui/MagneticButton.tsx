import React, { useRef, useState } from 'react';
import { motion } from 'framer-motion';

interface MagneticButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'glow';
  className?: string;
  disabled?: boolean;
  type?: 'button' | 'submit' | 'reset';
}

export const MagneticButton: React.FC<MagneticButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  className = '',
  disabled = false,
  type = 'button',
}) => {
  const buttonRef = useRef<HTMLButtonElement>(null);
  const [position, setPosition] = useState({ x: 0, y: 0 });

  const handleMouseMove = (e: React.MouseEvent<HTMLButtonElement>) => {
    if (!buttonRef.current || disabled) return;
    const { clientX, clientY } = e;
    const { left, top, width, height } = buttonRef.current.getBoundingClientRect();
    const centerX = left + width / 2;
    const centerY = top + height / 2;
    
    // Magnetic pull strength
    const deltaX = (clientX - centerX) * 0.25;
    const deltaY = (clientY - centerY) * 0.25;
    setPosition({ x: deltaX, y: deltaY });
  };

  const handleMouseLeave = () => {
    setPosition({ x: 0, y: 0 });
  };

  const variantStyles = {
    primary:
      'bg-[image:var(--accent-gradient)] text-white font-semibold shadow-[0_0_25px_var(--glow-primary)] hover:opacity-95 border border-white/20',
    secondary:
      'bg-[var(--bg-card)] hover:bg-[var(--bg-secondary)] text-[var(--text-primary)] border border-[var(--border-subtle)] backdrop-blur-md shadow-sm',
    outline:
      'bg-transparent hover:bg-[var(--glow-primary)] text-[var(--accent-primary)] border border-[var(--accent-primary)]/40 hover:border-[var(--accent-primary)]',
    ghost:
      'bg-transparent hover:bg-black/5 dark:hover:bg-white/5 text-[var(--text-secondary)] hover:text-[var(--text-primary)]',
    glow:
      'bg-[var(--accent-primary)] hover:opacity-90 text-white shadow-[0_0_30px_var(--glow-primary)] border border-white/20',
  };

  return (
    <motion.button
      ref={buttonRef}
      type={type}
      disabled={disabled}
      onClick={onClick}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      animate={{ x: position.x, y: position.y }}
      transition={{ type: 'spring', stiffness: 350, damping: 25 }}
      whileTap={{ scale: 0.96 }}
      className={`relative inline-flex items-center justify-center gap-2 rounded-xl px-5 py-2.5 text-sm font-semibold transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed ${variantStyles[variant]} ${className}`}
    >
      {children}
    </motion.button>
  );
};

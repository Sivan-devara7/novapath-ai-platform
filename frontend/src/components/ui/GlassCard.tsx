import React, { useRef, useState } from 'react';
import { motion } from 'framer-motion';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  glowColor?: 'blue' | 'violet' | 'emerald' | 'amber' | 'none';
  interactive?: boolean;
  onClick?: () => void;
}

export const GlassCard: React.FC<GlassCardProps> = ({
  children,
  className = '',
  glowColor = 'blue',
  interactive = true,
  onClick,
}) => {
  const cardRef = useRef<HTMLDivElement>(null);
  const [rotateX, setRotateX] = useState(0);
  const [rotateY, setRotateY] = useState(0);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [isHovered, setIsHovered] = useState(false);

  const glowStyles = {
    blue: 'hover:border-[var(--accent-secondary)] hover:shadow-[0_0_30px_var(--glow-secondary)]',
    violet: 'hover:border-[var(--accent-primary)] hover:shadow-[0_0_30px_var(--glow-primary)]',
    emerald: 'hover:border-emerald-500/40 hover:shadow-[0_0_30px_rgba(16,185,129,0.2)]',
    amber: 'hover:border-amber-500/40 hover:shadow-[0_0_30px_rgba(245,158,11,0.2)]',
    none: '',
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!interactive || !cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const centerX = rect.width / 2;
    const centerY = rect.height / 2;
    
    // Subtle tilt angle capped at +/- 6 degrees
    setRotateX(((y - centerY) / centerY) * -5);
    setRotateY(((x - centerX) / centerX) * 5);
    setMousePos({ x, y });
  };

  const handleMouseEnter = () => {
    if (interactive) setIsHovered(true);
  };

  const handleMouseLeave = () => {
    if (interactive) {
      setIsHovered(false);
      setRotateX(0);
      setRotateY(0);
    }
  };

  return (
    <motion.div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={onClick}
      style={{
        transform: interactive
          ? `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`
          : undefined,
        transition: isHovered ? 'transform 0.1s ease-out' : 'transform 0.5s ease-out',
      }}
      className={`relative overflow-hidden rounded-2xl border border-[var(--border-card)] bg-[var(--bg-card)] backdrop-blur-xl shadow-[var(--card-shadow)] text-[var(--text-primary)] transition-all duration-300 ${
        interactive ? 'cursor-pointer' : ''
      } ${glowStyles[glowColor]} ${className}`}
    >
      {/* Dynamic Cursor Spotlight Beam on Card Surface */}
      {interactive && isHovered && (
        <div
          className="pointer-events-none absolute -inset-px transition-opacity duration-300"
          style={{
            background: `radial-gradient(400px circle at ${mousePos.x}px ${mousePos.y}px, var(--glow-secondary), transparent 80%)`,
          }}
        />
      )}
      <div className="relative z-10">{children}</div>
    </motion.div>
  );
};

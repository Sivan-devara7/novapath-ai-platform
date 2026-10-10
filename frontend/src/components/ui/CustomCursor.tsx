import React, { useEffect, useState } from 'react';

export const CustomCursor: React.FC = () => {
  const [position, setPosition] = useState({ x: -100, y: -100 });
  const [trailing, setTrailing] = useState({ x: -100, y: -100 });
  const [isHovering, setIsHovering] = useState(false);
  const [isClicking, setIsClicking] = useState(false);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Only show custom cursor on non-touch devices
    if (window.matchMedia('(pointer: coarse)').matches) return;

    const handleMouseMove = (e: MouseEvent) => {
      setPosition({ x: e.clientX, y: e.clientY });
      if (!isVisible) setIsVisible(true);

      const target = e.target as HTMLElement | null;
      if (
        target?.closest('button') ||
        target?.closest('a') ||
        target?.closest('input') ||
        target?.closest('[role="button"]') ||
        target?.closest('.cursor-pointer')
      ) {
        setIsHovering(true);
      } else {
        setIsHovering(false);
      }
    };

    const handleMouseDown = () => setIsClicking(true);
    const handleMouseUp = () => setIsClicking(false);
    const handleMouseLeave = () => setIsVisible(false);
    const handleMouseEnter = () => setIsVisible(true);

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mousedown', handleMouseDown);
    window.addEventListener('mouseup', handleMouseUp);
    document.addEventListener('mouseleave', handleMouseLeave);
    document.addEventListener('mouseenter', handleMouseEnter);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mousedown', handleMouseDown);
      window.removeEventListener('mouseup', handleMouseUp);
      document.removeEventListener('mouseleave', handleMouseLeave);
      document.removeEventListener('mouseenter', handleMouseEnter);
    };
  }, [isVisible]);

  // Smooth lerp for trailing ring
  useEffect(() => {
    let animationFrameId: number;
    const loop = () => {
      setTrailing(prev => ({
        x: prev.x + (position.x - prev.x) * 0.18,
        y: prev.y + (position.y - prev.y) * 0.18,
      }));
      animationFrameId = requestAnimationFrame(loop);
    };
    animationFrameId = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(animationFrameId);
  }, [position]);

  if (!isVisible) return null;

  return (
    <div className="pointer-events-none fixed inset-0 z-50 overflow-hidden">
      {/* Outer Trailing Glow Ring */}
      <div
        className={`absolute rounded-full transition-transform duration-100 ease-out will-change-transform ${
          isHovering
            ? 'scale-150'
            : isClicking
            ? 'scale-90'
            : 'scale-100'
        }`}
        style={{
          width: '32px',
          height: '32px',
          left: `${trailing.x - 16}px`,
          top: `${trailing.y - 16}px`,
          borderColor: 'var(--cursor-ring)',
          borderWidth: '1px',
          borderStyle: 'solid',
          backgroundColor: isHovering ? 'var(--selection-bg)' : 'transparent',
          boxShadow: isHovering ? '0 0 20px var(--cursor-ring)' : 'none',
        }}
      />
      {/* Inner Dot */}
      <div
        className={`absolute rounded-full transition-transform duration-75 will-change-transform ${
          isHovering ? 'scale-150' : isClicking ? 'scale-75' : 'scale-100'
        }`}
        style={{
          width: '6px',
          height: '6px',
          left: `${position.x - 3}px`,
          top: `${position.y - 3}px`,
          backgroundColor: 'var(--cursor-dot)',
          boxShadow: '0 0 10px var(--cursor-dot)',
        }}
      />
    </div>
  );
};

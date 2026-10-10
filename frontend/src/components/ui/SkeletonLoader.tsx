import React from 'react';

interface SkeletonProps {
  className?: string;
  lines?: number;
}

export const SkeletonLoader: React.FC<SkeletonProps> = ({ className = '', lines = 1 }) => {
  return (
    <div className="space-y-2.5">
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className={`relative overflow-hidden rounded-lg bg-slate-800/40 before:absolute before:inset-0 before:-translate-x-full before:animate-[shimmer_1.8s_infinite] before:bg-gradient-to-r before:from-transparent before:via-white/[0.07] before:to-transparent ${className}`}
        />
      ))}
    </div>
  );
};

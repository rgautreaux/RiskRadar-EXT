import React from 'react';
import { motion, easeInOut } from 'framer-motion';

export type GolbyExpression = 
  | 'happy' 
  | 'thinking' 
  | 'surprised' 
  | 'puzzled' 
  | 'waving'
  | 'winking'
  | 'laughing'
  | 'excited';

export type GolbySize = 'sm' | 'md' | 'lg' | 'xl';

interface GolbyIconProps {
  expression?: GolbyExpression;
  size?: GolbySize;
  animate?: boolean;
  className?: string;
}

const sizeMap = {
  sm: 'w-8 h-8',
  md: 'w-12 h-12',
  lg: 'w-16 h-16',
  xl: 'w-24 h-24'
};

export function GolbyIcon({ 
  expression = 'happy', 
  size = 'md', 
  animate = true,
  className = ''
}: GolbyIconProps) {
  // Animation variants based on expression
  // Always return all keys for framer-motion animate prop
  const getAnimationVariant = () => {
    switch (expression) {
      case 'waving':
        return {
          scale: [1, 1, 1, 1, 1, 1],
          rotate: [0, -10, 10, -10, 10, 0],
          y: [0, 0, 0, 0, 0, 0],
          transition: { duration: 1, repeat: Infinity, repeatDelay: 2 }
        };
      case 'thinking':
        return {
          scale: [1, 1, 1],
          rotate: [0, 0, 0],
          y: [0, -5, 0],
          transition: { duration: 2, repeat: Infinity, ease: easeInOut }
        };
      case 'excited':
        return {
          scale: [1, 1.1, 1],
          rotate: [0, -5, 5, -5, 5, 0],
          y: [0, 0, 0, 0, 0, 0],
          transition: { duration: 0.6, repeat: Infinity, repeatDelay: 1 }
        };
      case 'winking':
        return {
          scale: [1, 0.95, 1],
          rotate: [0, 0, 0],
          y: [0, 0, 0],
          transition: { duration: 0.5, repeat: Infinity, repeatDelay: 3 }
        };
      case 'laughing':
        return {
          scale: [1, 1, 1, 1, 1],
          rotate: [0, -3, 3, -3, 0],
          y: [0, -3, 0, -3, 0],
          transition: { duration: 0.8, repeat: Infinity, repeatDelay: 1 }
        };
      default:
        return {
          scale: [1, 1.05, 1],
          rotate: [0, 0, 0],
          y: [0, 0, 0],
          transition: { duration: 2, repeat: Infinity, ease: easeInOut }
        };
    }
  };

  const staticPose = { scale: 1, rotate: 0, y: 0 };
  return (
    <motion.div
      className={`relative inline-flex items-center justify-center ${sizeMap[size]} ${className}`}
      initial={{ scale: 0, rotate: -180, y: 0 }}
      animate={animate ? getAnimationVariant() : staticPose}
      transition={{ duration: 0.5, type: 'spring' }}
      role="img"
      aria-label={`Golby the assistant looking ${expression}`}
    >
      {/* Base Golby SVG - replace with your SVG import or inline SVG */}
      <svg viewBox="0 0 100 100" className="w-full h-full object-contain" aria-hidden="true">
        <circle cx="50" cy="50" r="48" fill="#ffe6b3" stroke="#e0b060" strokeWidth="4" />
      </svg>
      {/* Facial expression overlays - drawn as SVG on top */}
      <FacialExpressionOverlay expression={expression} size={size} />
    </motion.div>
  );
}

function FacialExpressionOverlay({ expression, size }: { expression: GolbyExpression; size: GolbySize }) {
  const sizeScale = {
    sm: 0.5,
    md: 0.75,
    lg: 1,
    xl: 1.5
  };
  const scale = sizeScale[size];
  return (
    <svg 
      className="absolute inset-0 w-full h-full pointer-events-none" 
      viewBox="0 0 100 100"
      style={{ transform: `scale(${scale})` }}
    >
      {/* Eyes and mouth positioned on Golby's face */}
      {expression === 'happy' && (
        <>
          <circle cx="35" cy="42" r="4" fill="#1a1a1a" />
          <circle cx="65" cy="42" r="4" fill="#1a1a1a" />
          <path d="M 35 58 Q 50 68 65 58" stroke="#1a1a1a" strokeWidth="3" fill="none" strokeLinecap="round" />
        </>
      )}
      {expression === 'thinking' && (
        <>
          <circle cx="35" cy="40" r="3.5" fill="#1a1a1a" />
          <circle cx="65" cy="40" r="3.5" fill="#1a1a1a" />
          <path d="M 38 60 Q 50 57 62 60" stroke="#1a1a1a" strokeWidth="2.5" fill="none" strokeLinecap="round" />
        </>
      )}
      {/* Add other expressions as needed */}
    </svg>
  );
}

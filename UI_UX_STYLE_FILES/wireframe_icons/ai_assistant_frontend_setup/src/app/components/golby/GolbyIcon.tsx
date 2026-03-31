import React from 'react';
import { motion } from 'motion/react';
import golbySvg from '../../../imports/ai-assistant.svg';

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
  const getAnimationVariant = () => {
    switch (expression) {
      case 'waving':
        return {
          rotate: [0, -10, 10, -10, 10, 0],
          transition: { duration: 1, repeat: Infinity, repeatDelay: 2 }
        };
      case 'thinking':
        return {
          y: [0, -5, 0],
          transition: { duration: 2, repeat: Infinity, ease: 'easeInOut' }
        };
      case 'excited':
        return {
          scale: [1, 1.1, 1],
          rotate: [0, -5, 5, -5, 5, 0],
          transition: { duration: 0.6, repeat: Infinity, repeatDelay: 1 }
        };
      case 'winking':
        return {
          scale: [1, 0.95, 1],
          transition: { duration: 0.5, repeat: Infinity, repeatDelay: 3 }
        };
      case 'laughing':
        return {
          y: [0, -3, 0, -3, 0],
          rotate: [0, -3, 3, -3, 0],
          transition: { duration: 0.8, repeat: Infinity, repeatDelay: 1 }
        };
      default:
        return {
          scale: [1, 1.05, 1],
          transition: { duration: 2, repeat: Infinity, ease: 'easeInOut' }
        };
    }
  };

  return (
    <motion.div
      className={`relative inline-flex items-center justify-center ${sizeMap[size]} ${className}`}
      initial={{ scale: 0, rotate: -180 }}
      animate={animate ? { 
        scale: 1, 
        rotate: 0,
        ...getAnimationVariant()
      } : { scale: 1, rotate: 0 }}
      transition={{ duration: 0.5, type: 'spring' }}
      role="img"
      aria-label={`Golby the assistant looking ${expression}`}
    >
      {/* Base Golby SVG */}
      <img 
        src={golbySvg} 
        alt=""
        className="w-full h-full object-contain"
        aria-hidden="true"
      />
      
      {/* Facial expression overlays - drawn as SVG on top */}
      <FacialExpressionOverlay expression={expression} size={size} />
    </motion.div>
  );
}

function FacialExpressionOverlay({ expression, size }: { expression: GolbyExpression; size: GolbySize }) {
  // Scale factors for different sizes
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
          {/* Happy eyes */}
          <circle cx="35" cy="42" r="4" fill="#1a1a1a" />
          <circle cx="65" cy="42" r="4" fill="#1a1a1a" />
          {/* Happy smile */}
          <path 
            d="M 35 58 Q 50 68 65 58" 
            stroke="#1a1a1a" 
            strokeWidth="3" 
            fill="none" 
            strokeLinecap="round"
          />
        </>
      )}
      
      {expression === 'thinking' && (
        <>
          {/* Thoughtful eyes looking up */}
          <circle cx="35" cy="40" r="3.5" fill="#1a1a1a" />
          <circle cx="65" cy="40" r="3.5" fill="#1a1a1a" />
          {/* Slight frown */}
          <path 
            d="M 38 60 Q 50 57 62 60" 
            stroke="#1a1a1a" 
            strokeWidth="2.5" 
            fill="none" 
            strokeLinecap="round"
          />
          {/* Thought bubble */}
          <motion.text
            x="75"
            y="25"
            fontSize="16"
            animate={{ y: [25, 20, 25], opacity: [0.5, 1, 0.5] }}
            transition={{ duration: 1.5, repeat: Infinity }}
          >
            💭
          </motion.text>
        </>
      )}
      
      {expression === 'surprised' && (
        <>
          {/* Wide open eyes */}
          <circle cx="35" cy="42" r="6" fill="white" stroke="#1a1a1a" strokeWidth="2" />
          <circle cx="35" cy="42" r="3" fill="#1a1a1a" />
          <circle cx="65" cy="42" r="6" fill="white" stroke="#1a1a1a" strokeWidth="2" />
          <circle cx="65" cy="42" r="3" fill="#1a1a1a" />
          {/* O-shaped mouth */}
          <circle cx="50" cy="62" r="6" fill="none" stroke="#1a1a1a" strokeWidth="3" />
        </>
      )}
      
      {expression === 'puzzled' && (
        <>
          {/* Confused eyes */}
          <circle cx="35" cy="42" r="3.5" fill="#1a1a1a" />
          <circle cx="65" cy="42" r="3.5" fill="#1a1a1a" />
          {/* Wavy confused mouth */}
          <path 
            d="M 35 60 Q 42 62 50 60 Q 58 58 65 60" 
            stroke="#1a1a1a" 
            strokeWidth="2.5" 
            fill="none" 
            strokeLinecap="round"
          />
          {/* Question mark */}
          <motion.text
            x="73"
            y="30"
            fontSize="14"
            animate={{ rotate: [0, 15, -15, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            ❓
          </motion.text>
        </>
      )}
      
      {expression === 'waving' && (
        <>
          {/* Friendly eyes */}
          <circle cx="35" cy="42" r="4" fill="#1a1a1a" />
          <circle cx="65" cy="42" r="4" fill="#1a1a1a" />
          {/* Big smile */}
          <path 
            d="M 32 56 Q 50 70 68 56" 
            stroke="#1a1a1a" 
            strokeWidth="3.5" 
            fill="none" 
            strokeLinecap="round"
          />
        </>
      )}
      
      {expression === 'winking' && (
        <>
          {/* One eye open */}
          <circle cx="35" cy="42" r="4" fill="#1a1a1a" />
          {/* One eye winking (line) */}
          <motion.path 
            d="M 60 42 L 70 42" 
            stroke="#1a1a1a" 
            strokeWidth="3" 
            strokeLinecap="round"
            animate={{ scaleY: [1, 0.2, 1] }}
            transition={{ duration: 0.5, repeat: Infinity, repeatDelay: 3 }}
          />
          {/* Playful smile */}
          <path 
            d="M 35 58 Q 50 66 65 58" 
            stroke="#1a1a1a" 
            strokeWidth="3" 
            fill="none" 
            strokeLinecap="round"
          />
        </>
      )}
      
      {expression === 'laughing' && (
        <>
          {/* Eyes closed from laughing */}
          <motion.path 
            d="M 30 40 Q 35 45 40 40" 
            stroke="#1a1a1a" 
            strokeWidth="3" 
            fill="none" 
            strokeLinecap="round"
            animate={{ y: [0, 2, 0] }}
            transition={{ duration: 0.4, repeat: Infinity }}
          />
          <motion.path 
            d="M 60 40 Q 65 45 70 40" 
            stroke="#1a1a1a" 
            strokeWidth="3" 
            fill="none" 
            strokeLinecap="round"
            animate={{ y: [0, 2, 0] }}
            transition={{ duration: 0.4, repeat: Infinity }}
          />
          {/* Wide open laughing mouth */}
          <path 
            d="M 32 55 Q 50 72 68 55" 
            stroke="#1a1a1a" 
            strokeWidth="4" 
            fill="rgba(0,0,0,0.1)" 
            strokeLinecap="round"
          />
        </>
      )}
      
      {expression === 'excited' && (
        <>
          {/* Sparkly eyes */}
          <circle cx="35" cy="42" r="5" fill="#1a1a1a" />
          <circle cx="32" cy="40" r="1.5" fill="white" />
          <circle cx="65" cy="42" r="5" fill="#1a1a1a" />
          <circle cx="62" cy="40" r="1.5" fill="white" />
          {/* Excited smile */}
          <path 
            d="M 30 56 Q 50 72 70 56" 
            stroke="#1a1a1a" 
            strokeWidth="4" 
            fill="none" 
            strokeLinecap="round"
          />
          {/* Sparkle effect */}
          <motion.text
            x="48"
            y="25"
            fontSize="12"
            textAnchor="middle"
            animate={{ 
              y: [25, 15, 25],
              opacity: [0.5, 1, 0.5],
              scale: [0.8, 1.2, 0.8]
            }}
            transition={{ duration: 1, repeat: Infinity }}
          >
            ✨
          </motion.text>
        </>
      )}
    </svg>
  );
}
import React from 'react';
import { AnimatePresence, easeInOut, motion, useReducedMotion } from 'framer-motion';

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

const GOLBY_EXPRESSION_ASSET: Record<GolbyExpression, string> = {
  happy: '/assets/icons/ai-assistant.svg',
  thinking: '/assets/icons/Golby-Thinking.svg',
  surprised: '/assets/icons/Golby-Surprised.svg',
  puzzled: '/assets/icons/Golby-Puzzled.svg',
  waving: '/assets/icons/Golby-Waving.svg',
  winking: '/assets/icons/Golby-Wink.svg',
  laughing: '/assets/icons/Golby-Laugh.svg',
  excited: '/assets/icons/Golby-Excited.svg'
};

const GOLBY_FALLBACK_ASSET = GOLBY_EXPRESSION_ASSET.happy;
const EXPRESSION_SWAP_DEBOUNCE_MS = 70;

function resolveExpressionAsset(expression: GolbyExpression): string {
  return GOLBY_EXPRESSION_ASSET[expression] ?? GOLBY_FALLBACK_ASSET;
}

export function GolbyIcon({ 
  expression = 'happy', 
  size = 'md', 
  animate = true,
  className = ''
}: GolbyIconProps) {
  const prefersReducedMotion = useReducedMotion();
  const [displayExpression, setDisplayExpression] = React.useState<GolbyExpression>(expression);
  const loadRequestId = React.useRef(0);
  const debounceTimerRef = React.useRef<number | null>(null);

  React.useEffect(() => {
    const uniqueAssets = Array.from(new Set(Object.values(GOLBY_EXPRESSION_ASSET)));
    uniqueAssets.forEach((src) => {
      const img = new Image();
      img.src = src;
    });
  }, []);

  React.useEffect(() => {
    if (expression === displayExpression) return;

    const requestId = ++loadRequestId.current;
    const nextAsset = resolveExpressionAsset(expression);
    const preload = new Image();

    const commitExpression = () => {
      // Latest-wins guard for rapid expression changes.
      if (requestId === loadRequestId.current) {
        if (debounceTimerRef.current !== null) {
          window.clearTimeout(debounceTimerRef.current);
        }

        const delay = prefersReducedMotion ? 0 : EXPRESSION_SWAP_DEBOUNCE_MS;
        debounceTimerRef.current = window.setTimeout(() => {
          if (requestId === loadRequestId.current) {
            setDisplayExpression(expression);
          }
        }, delay);
      }
    };

    preload.onload = commitExpression;
    preload.onerror = commitExpression;
    preload.src = nextAsset;

    if (preload.complete) {
      commitExpression();
    }

    return () => {
      preload.onload = null;
      preload.onerror = null;
    };
  }, [displayExpression, expression, prefersReducedMotion]);

  React.useEffect(() => {
    return () => {
      if (debounceTimerRef.current !== null) {
        window.clearTimeout(debounceTimerRef.current);
      }
    };
  }, []);

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
  const displayedAsset = resolveExpressionAsset(displayExpression);
  return (
    <motion.div
      className={`relative inline-flex items-center justify-center ${sizeMap[size]} ${className}`}
      initial={{ scale: 0, rotate: -180, y: 0 }}
      animate={animate ? getAnimationVariant() : staticPose}
      transition={{ duration: 0.5, type: 'spring' }}
      role="img"
      aria-label={`Golby the assistant looking ${expression}`}
    >
      <AnimatePresence mode="sync" initial={false}>
        <motion.img
          key={displayExpression}
          src={displayedAsset}
          alt=""
          aria-hidden="true"
          className="absolute inset-0 w-full h-full object-contain pointer-events-none"
          initial={
            prefersReducedMotion
              ? { opacity: 1, scale: 1 }
              : { opacity: 0, scale: 0.98 }
          }
          animate={{ opacity: 1, scale: 1 }}
          exit={
            prefersReducedMotion
              ? { opacity: 1, scale: 1 }
              : { opacity: 0, scale: 1.02 }
          }
          transition={
            prefersReducedMotion
              ? { duration: 0 }
              : { duration: 0.22, ease: easeInOut }
          }
          onError={(event) => {
            const target = event.currentTarget;
            if (target.dataset.fallbackApplied === 'true') return;
            target.dataset.fallbackApplied = 'true';
            target.src = GOLBY_FALLBACK_ASSET;
          }}
        />
      </AnimatePresence>
    </motion.div>
  );
}

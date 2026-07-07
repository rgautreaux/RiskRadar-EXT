import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { GolbyIcon } from './GolbyIcon';
import { X } from 'lucide-react';

interface ContextualHelpProps {
  tip: string;
  position?: 'top' | 'bottom' | 'left' | 'right';
  onDismiss?: () => void;
  onLearnMore?: () => void;
  autoShow?: boolean;
}

export function ContextualHelp({ 
  tip, 
  position = 'top',
  onDismiss,
  onLearnMore,
  autoShow = true
}: ContextualHelpProps) {
  const [isVisible, setIsVisible] = useState(autoShow);

  const handleDismiss = () => {
    setIsVisible(false);
    onDismiss?.();
  };

  const positionClasses = {
    top: 'bottom-full mb-2',
    bottom: 'top-full mt-2',
    left: 'right-full mr-2',
    right: 'left-full ml-2'
  };

  const arrowClasses = {
    top: 'top-full left-1/2 -ml-2 border-l-8 border-r-8 border-t-8 border-transparent border-t-white',
    bottom: 'bottom-full left-1/2 -ml-2 border-l-8 border-r-8 border-b-8 border-transparent border-b-white',
    left: 'left-full top-1/2 -mt-2 border-t-8 border-b-8 border-l-8 border-transparent border-l-white',
    right: 'right-full top-1/2 -mt-2 border-t-8 border-b-8 border-r-8 border-transparent border-r-white'
  };

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, scale: 0.8, y: position === 'bottom' ? -10 : 10 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.8 }}
          transition={{ duration: 0.3 }}
          className={`absolute ${positionClasses[position]} z-50`}
          role="tooltip"
          aria-live="polite"
        >
          <div className="relative bg-white rounded-xl shadow-lg border border-gray-200 p-4 max-w-xs">
            {/* Close button */}
            <button
              onClick={handleDismiss}
              className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 
                transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
              aria-label="Dismiss tip"
            >
              <X className="w-4 h-4" />
            </button>

            {/* Content */}
            <div className="flex gap-3">
              <div className="flex-shrink-0 pt-1">
                <GolbyIcon expression="excited" size="sm" />
              </div>
              <div className="flex-1 pr-6">
                <p className="text-sm text-gray-700 leading-relaxed mb-3">
                  {tip}
                </p>
                <div className="flex gap-2">
                  <button
                    onClick={handleDismiss}
                    className="px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-700 
                      rounded-lg text-xs font-medium transition-colors
                      focus:outline-none focus:ring-2 focus:ring-gray-300"
                  >
                    Got it!
                  </button>
                  {onLearnMore && (
                    <button
                      onClick={() => {
                        onLearnMore();
                        handleDismiss();
                      }}
                      className="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white 
                        rounded-lg text-xs font-medium transition-colors
                        focus:outline-none focus:ring-2 focus:ring-blue-300"
                    >
                      Tell me more
                    </button>
                  )}
                </div>
              </div>
            </div>

            {/* Arrow */}
            <div 
              className={`absolute w-0 h-0 ${arrowClasses[position]}`}
              aria-hidden="true"
            />
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

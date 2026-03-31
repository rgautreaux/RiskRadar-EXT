import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { GolbyIcon } from './GolbyIcon';
import { X } from 'lucide-react';

interface FloatingWidgetProps {
  onOpen?: () => void;
  position?: 'bottom-right' | 'bottom-left';
  showTooltip?: boolean;
}

export function FloatingWidget({ 
  onOpen, 
  position = 'bottom-right',
  showTooltip = true 
}: FloatingWidgetProps) {
  const [isHovered, setIsHovered] = useState(false);
  const [tooltipVisible, setTooltipVisible] = useState(true);

  const positionClasses = {
    'bottom-right': 'bottom-6 right-6',
    'bottom-left': 'bottom-6 left-6'
  };

  return (
    <div className={`fixed ${positionClasses[position]} z-50`}>
      {/* Tooltip */}
      <AnimatePresence>
        {showTooltip && tooltipVisible && !isHovered && (
          <motion.div
            initial={{ opacity: 0, x: position === 'bottom-right' ? 20 : -20, scale: 0.8 }}
            animate={{ opacity: 1, x: 0, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            className={`absolute bottom-full mb-3 ${position === 'bottom-right' ? 'right-0' : 'left-0'} 
              bg-white px-4 py-2 rounded-lg shadow-lg border border-gray-200 whitespace-nowrap`}
            role="tooltip"
          >
            <p className="text-sm font-medium text-gray-900">Need help? Ask Golby!</p>
            <button
              onClick={() => setTooltipVisible(false)}
              className="absolute -top-1 -right-1 bg-gray-100 rounded-full p-0.5 hover:bg-gray-200"
              aria-label="Dismiss tooltip"
            >
              <X className="w-3 h-3 text-gray-600" />
            </button>
            {/* Arrow */}
            <div 
              className={`absolute top-full ${position === 'bottom-right' ? 'right-4' : 'left-4'} 
                w-0 h-0 border-l-8 border-r-8 border-t-8 border-transparent border-t-white`}
              style={{ marginTop: '-1px' }}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Floating Button */}
      <motion.button
        className="relative w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full 
          shadow-lg hover:shadow-xl focus:outline-none focus:ring-4 focus:ring-blue-300 
          flex items-center justify-center group"
        onHoverStart={() => setIsHovered(true)}
        onHoverEnd={() => setIsHovered(false)}
        onClick={onOpen}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.95 }}
        animate={{
          y: [0, -5, 0],
        }}
        transition={{
          y: {
            duration: 2,
            repeat: Infinity,
            ease: 'easeInOut'
          }
        }}
        aria-label="Open Golby assistant"
      >
        <div className="w-12 h-12">
          <GolbyIcon 
            expression={isHovered ? 'waving' : 'happy'} 
            size="md"
            animate={isHovered}
          />
        </div>
        
        {/* Notification pulse */}
        <motion.div
          className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full border-2 border-white"
          animate={{
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 1.5,
            repeat: Infinity,
          }}
          aria-hidden="true"
        />
      </motion.button>
    </div>
  );
}

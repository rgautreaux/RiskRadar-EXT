import React from 'react';
import { motion } from 'motion/react';
import { GolbyIcon } from './GolbyIcon';
import { RefreshCw, Home, HelpCircle } from 'lucide-react';

interface ErrorStateProps {
  title?: string;
  message?: string;
  suggestions?: string[];
  onRetry?: () => void;
  onGoHome?: () => void;
  onAskGolby?: () => void;
}

export function ErrorState({
  title = "Oops! Something went wrong",
  message = "I couldn't find that info. Want to try again or ask something else?",
  suggestions = [
    "Try searching for a different location",
    "Check your internet connection",
    "Explore other RiskRadar features"
  ],
  onRetry,
  onGoHome,
  onAskGolby
}: ErrorStateProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col items-center justify-center p-8 text-center max-w-md mx-auto"
      role="alert"
      aria-live="polite"
    >
      {/* Golby with puzzled expression */}
      <motion.div
        initial={{ rotate: -10 }}
        animate={{ rotate: [10, -10, 10, -10, 0] }}
        transition={{ duration: 1, delay: 0.2 }}
        className="mb-6"
      >
        <GolbyIcon expression="puzzled" size="xl" />
      </motion.div>

      {/* Error message */}
      <h2 className="text-2xl text-gray-900 mb-3">{title}</h2>
      <p className="text-gray-600 leading-relaxed mb-6">
        {message}
      </p>

      {/* Action buttons */}
      <div className="flex flex-wrap gap-3 justify-center mb-6">
        {onRetry && (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onRetry}
            className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white 
              px-5 py-2.5 rounded-full font-medium transition-colors shadow-md
              focus:outline-none focus:ring-4 focus:ring-blue-300"
          >
            <RefreshCw className="w-4 h-4" />
            Try Again
          </motion.button>
        )}
        
        {onGoHome && (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onGoHome}
            className="flex items-center gap-2 bg-gray-100 hover:bg-gray-200 text-gray-700 
              px-5 py-2.5 rounded-full font-medium transition-colors
              focus:outline-none focus:ring-4 focus:ring-gray-300"
          >
            <Home className="w-4 h-4" />
            Go Home
          </motion.button>
        )}

        {onAskGolby && (
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={onAskGolby}
            className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white 
              px-5 py-2.5 rounded-full font-medium transition-colors shadow-md
              focus:outline-none focus:ring-4 focus:ring-green-300"
          >
            <HelpCircle className="w-4 h-4" />
            Ask Golby
          </motion.button>
        )}
      </div>

      {/* Suggestions */}
      {suggestions.length > 0 && (
        <div className="w-full bg-gray-50 rounded-xl p-4 border border-gray-200">
          <p className="text-sm font-medium text-gray-700 mb-3">Here are some suggestions:</p>
          <ul className="space-y-2">
            {suggestions.map((suggestion, index) => (
              <motion.li
                key={index}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
                className="flex items-start gap-2 text-sm text-gray-600"
              >
                <span className="text-blue-600 mt-0.5">•</span>
                <span>{suggestion}</span>
              </motion.li>
            ))}
          </ul>
        </div>
      )}
    </motion.div>
  );
}

export function NoDataState({ 
  title = "No Data Available",
  message = "Hmm, I don't have information for this location yet.",
  onExploreOther
}: { 
  title?: string;
  message?: string;
  onExploreOther?: () => void;
}) {
  return (
    <ErrorState
      title={title}
      message={message}
      suggestions={[
        "This area might not be in our database yet",
        "Try a nearby location instead",
        "Check back later for updates"
      ]}
      onGoHome={onExploreOther}
    />
  );
}
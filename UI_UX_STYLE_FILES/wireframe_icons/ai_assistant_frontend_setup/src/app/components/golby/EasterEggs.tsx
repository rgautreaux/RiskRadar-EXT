import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { GolbyIcon } from './GolbyIcon';

interface EasterEggResponse {
  text: string;
  expression: 'happy' | 'laughing' | 'excited' | 'winking';
}

const jokes = [
  { 
    text: "Why don't meteorologists like to go to parties? Because they always predict a chance of precipitation! ☔",
    expression: 'laughing' as const
  },
  { 
    text: "What's a tornado's favorite game to play? Twister! 🌪️",
    expression: 'laughing' as const
  },
  {
    text: "Why did the cloud date the fog? Because he was so down to earth! ☁️",
    expression: 'winking' as const
  },
  {
    text: "How do hurricanes see? With one eye! 👁️",
    expression: 'laughing' as const
  },
  {
    text: "What did the thermometer say to the graduated cylinder? You may have graduated, but I've got more degrees! 🌡️",
    expression: 'excited' as const
  }
];

const greetings = [
  {
    text: "Hi there, superstar! Ready to explore the world safely? 🌟",
    expression: 'waving' as const
  },
  {
    text: "Hey there, adventure seeker! What can I help you discover today? 🗺️",
    expression: 'excited' as const
  },
  {
    text: "Hello, friend! Let's make your travels safer together! 👋",
    expression: 'happy' as const
  }
];

const funFacts = [
  {
    text: "Did you know? Earth's atmosphere is about 300 miles thick, but most of it is within 10 miles of the surface! 🌍",
    expression: 'excited' as const
  },
  {
    text: "Fun fact: Lightning strikes the Earth about 100 times every second! ⚡",
    expression: 'surprised' as const
  },
  {
    text: "Here's something cool: The coldest temperature ever recorded on Earth was -128.6°F in Antarctica! 🥶",
    expression: 'surprised' as const
  }
];

interface JokeButtonProps {
  onJoke?: (joke: string) => void;
}

export function JokeButton({ onJoke }: JokeButtonProps) {
  const [showJoke, setShowJoke] = useState(false);
  const [currentJoke, setCurrentJoke] = useState<EasterEggResponse | null>(null);

  const tellJoke = () => {
    const randomJoke = jokes[Math.floor(Math.random() * jokes.length)];
    setCurrentJoke(randomJoke);
    setShowJoke(true);
    onJoke?.(randomJoke.text);
  };

  return (
    <>
      <motion.button
        onClick={tellJoke}
        className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 
          hover:to-pink-600 text-white px-4 py-2 rounded-full font-medium shadow-md
          focus:outline-none focus:ring-4 focus:ring-purple-300 flex items-center gap-2"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        aria-label="Tell me a joke"
      >
        😄 Tell me a joke!
      </motion.button>

      <AnimatePresence>
        {showJoke && currentJoke && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: -20 }}
            className="fixed inset-0 flex items-center justify-center z-50 p-4 bg-black/40"
            onClick={() => setShowJoke(false)}
          >
            <motion.div
              initial={{ rotate: -5 }}
              animate={{ rotate: [5, -5, 5, 0] }}
              transition={{ duration: 0.5 }}
              className="bg-white rounded-2xl shadow-2xl p-8 max-w-md relative"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex flex-col items-center text-center">
                <GolbyIcon expression={currentJoke.expression} size="lg" />
                <p className="mt-6 text-lg text-gray-800 leading-relaxed">
                  {currentJoke.text}
                </p>
                <button
                  onClick={() => setShowJoke(false)}
                  className="mt-6 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 
                    rounded-full font-medium transition-colors"
                >
                  Thanks, Golby! 😊
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

export function FunFactButton() {
  const [showFact, setShowFact] = useState(false);
  const [currentFact, setCurrentFact] = useState<EasterEggResponse | null>(null);

  const showRandomFact = () => {
    const randomFact = funFacts[Math.floor(Math.random() * funFacts.length)];
    setCurrentFact(randomFact);
    setShowFact(true);
  };

  return (
    <>
      <motion.button
        onClick={showRandomFact}
        className="bg-gradient-to-r from-yellow-400 to-orange-500 hover:from-yellow-500 
          hover:to-orange-600 text-white px-4 py-2 rounded-full font-medium shadow-md
          focus:outline-none focus:ring-4 focus:ring-yellow-300 flex items-center gap-2"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        aria-label="Show me a fun fact"
      >
        ✨ Fun Fact
      </motion.button>

      <AnimatePresence>
        {showFact && currentFact && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: -20 }}
            className="fixed inset-0 flex items-center justify-center z-50 p-4 bg-black/40"
            onClick={() => setShowFact(false)}
          >
            <motion.div
              className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-2xl 
                shadow-2xl p-8 max-w-md relative border-2 border-yellow-200"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex flex-col items-center text-center">
                <GolbyIcon expression={currentFact.expression} size="lg" />
                <p className="mt-6 text-lg text-gray-800 leading-relaxed">
                  {currentFact.text}
                </p>
                <button
                  onClick={() => setShowFact(false)}
                  className="mt-6 bg-orange-600 hover:bg-orange-700 text-white px-6 py-2 
                    rounded-full font-medium transition-colors"
                >
                  Wow, thanks Golby! 🤓
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

// Hook to detect special greetings
export function useGolbyGreeting(message: string): EasterEggResponse | null {
  const lowerMessage = message.toLowerCase();
  
  if (lowerMessage.includes('hi golby') || lowerMessage.includes('hello golby')) {
    return greetings[Math.floor(Math.random() * greetings.length)];
  }
  
  return null;
}

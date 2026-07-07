import React from 'react';
import { motion } from 'motion/react';
import { GolbyIcon } from './GolbyIcon';
import { Sparkles, MessageCircle, Bell, Map } from 'lucide-react';

interface WelcomeTabProps {
  onGetStarted?: () => void;
}

export function WelcomeTab({ onGetStarted }: WelcomeTabProps) {
  const tips = [
    {
      icon: Map,
      text: "Click anywhere on the map to see location-specific environmental risks!"
    },
    {
      icon: Bell,
      text: "Set up custom alerts to stay informed about risks in your area."
    },
    {
      icon: MessageCircle,
      text: "Ask me anything about environmental data, travel safety, or how to use RiskRadar."
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="max-w-4xl mx-auto p-8"
    >
      {/* Header with Golby */}
      <div className="flex flex-col items-center text-center mb-8">
        <motion.div
          initial={{ scale: 0, rotate: -180 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ 
            duration: 0.8, 
            type: 'spring',
            delay: 0.2 
          }}
          className="mb-6"
        >
          <GolbyIcon expression="waving" size="xl" />
        </motion.div>

        {/* Speech Bubble */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5 }}
          className="relative bg-gradient-to-br from-blue-500 to-blue-600 text-white 
            rounded-3xl px-8 py-6 shadow-lg max-w-2xl mb-8"
          role="region"
          aria-label="Welcome message from Golby"
        >
          <h1 className="text-2xl mb-2">Hi, I'm Golby!</h1>
          <p className="text-lg opacity-95">
            Your friendly AI travel assistant. Ask me anything about environmental risks, 
            travel safety, or how to use RiskRadar!
          </p>
          {/* Speech bubble tail */}
          <div 
            className="absolute -bottom-3 left-1/2 -ml-3 w-0 h-0 
              border-l-[12px] border-r-[12px] border-t-[12px] 
              border-transparent border-t-blue-600"
          />
        </motion.div>

        {/* Get Started Button */}
        <motion.button
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
          onClick={onGetStarted}
          className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full 
            font-medium shadow-md hover:shadow-lg transition-all flex items-center gap-2
            focus:outline-none focus:ring-4 focus:ring-blue-300"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          aria-label="Get started with Golby"
        >
          <Sparkles className="w-5 h-5" />
          Get Started
        </motion.button>
      </div>

      {/* Did You Know Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.9 }}
        className="bg-gradient-to-br from-orange-50 to-yellow-50 rounded-2xl p-6 mb-6"
      >
        <h2 className="text-xl text-orange-900 mb-3 flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-orange-600" />
          Did You Know?
        </h2>
        <p className="text-orange-800 leading-relaxed">
          I can help you understand complex environmental data, get real-time risk assessments 
          for any location, and even tell you a joke when you need a break! Just ask me anything.
        </p>
      </motion.div>

      {/* Quick Tips */}
      <div className="grid gap-4 md:grid-cols-3">
        {tips.map((tip, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1 + index * 0.1 }}
            className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm hover:shadow-md 
              transition-shadow"
          >
            <div className="flex items-start gap-3">
              <div className="bg-blue-100 rounded-lg p-2 flex-shrink-0">
                <tip.icon className="w-5 h-5 text-blue-600" />
              </div>
              <p className="text-sm text-gray-700 leading-relaxed">{tip.text}</p>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}

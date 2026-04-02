import React from 'react';
import { motion } from 'framer-motion';
import { GolbyIcon } from './GolbyIcon';

interface WelcomeTabProps {
	onGetStarted?: () => void;
}

export function WelcomeTab({ onGetStarted }: WelcomeTabProps) {
	const tips = [
		"Did you know? You can set up custom alerts for your area!",
		"Golby can answer questions about environmental risks, forecasts, and more.",
		"Try asking: 'Show me today’s forecast' or 'How do I set alerts?'"
	];

	return (
		<motion.div
			initial={{ opacity: 0, y: 20 }}
			animate={{ opacity: 1, y: 0 }}
			transition={{ duration: 0.5 }}
			className="max-w-4xl mx-auto p-8"
			role="region"
			aria-label="Welcome to Golby AI Assistant"
		>
			{/* Golby Icon with animation */}
			<div className="flex flex-col items-center text-center mb-8">
				<motion.div
					initial={{ scale: 0, rotate: -180 }}
					animate={{ scale: 1, rotate: 0 }}
					transition={{ duration: 0.8, type: 'spring', delay: 0.2 }}
					className="mb-6"
				>
					<GolbyIcon expression="waving" size="xl" aria-label="Golby waving hello" />
				</motion.div>
				{/* Speech Bubble */}
				<motion.div
					initial={{ opacity: 0, scale: 0.9 }}
					animate={{ opacity: 1, scale: 1 }}
					transition={{ delay: 0.5 }}
					className="relative bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-3xl px-8 py-6 shadow-lg max-w-2xl mb-8"
					role="region"
					aria-label="Welcome message from Golby"
				>
					<h1 className="text-2xl mb-2">Hi, I'm Golby!</h1>
					<p className="text-lg opacity-95">
						Your friendly AI travel assistant. Ask me anything about environmental risks or how to use RiskRadar!
					</p>
				</motion.div>
			</div>
			{/* Tips/Fun Facts */}
			<ul className="mb-8 space-y-2" aria-label="Golby tips and fun facts">
				{tips.map((tip, idx) => (
					<li key={idx} className="flex items-center justify-center text-base text-blue-900 bg-blue-50 rounded-xl px-4 py-2 shadow-sm">
						<span role="img" aria-label="Golby tip">💡</span>
						<span className="ml-2">{tip}</span>
					</li>
				))}
			</ul>
			{/* Get Started Button */}
			<button
				onClick={onGetStarted}
				className="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-3 rounded-full shadow transition"
				aria-label="Get started with Golby"
			>
				Get Started
			</button>
		</motion.div>
	);
}

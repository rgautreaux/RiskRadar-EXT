import React from 'react';
import { motion } from 'framer-motion';
import { GolbyIcon } from './GolbyIcon';

interface PageWelcomeProps {
	onGetStarted?: () => void;
}

export function PageWelcome({ onGetStarted }: PageWelcomeProps) {
	const tips = [
		"Did you know? You can set up custom alerts for your area!",
		"Golby can answer questions about environmental risks, forecasts, and more.",
		"Try asking: 'Show me today's forecast' or 'How do I set alerts?'"
	];

	return (
		<motion.div
			initial={{ opacity: 0 }}
			animate={{ opacity: 1 }}
			transition={{ duration: 0.5 }}
			className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-slate-100 p-8"
		>
			<motion.div
				initial={{ opacity: 0, y: 20, scale: 0.95 }}
				animate={{ opacity: 1, y: 0, scale: 1 }}
				transition={{ duration: 0.6, delay: 0.1 }}
				className="max-w-3xl w-full"
				role="region"
				aria-label="Welcome to Golby AI Assistant"
			>
				{/* Golby Icon with animation */}
				<div className="flex flex-col items-center text-center mb-12">
					<motion.div
						initial={{ scale: 0, rotate: -180 }}
						animate={{ scale: 1, rotate: 0 }}
						transition={{ duration: 0.8, type: 'spring', delay: 0.3 }}
						className="mb-10"
					>
						<GolbyIcon expression="waving" size="xl" aria-label="Golby waving hello" />
					</motion.div>

					{/* Speech Bubble */}
					<motion.div
						initial={{ opacity: 0, scale: 0.85 }}
						animate={{ opacity: 1, scale: 1 }}
						transition={{ delay: 0.6, duration: 0.5 }}
						className="relative bg-gradient-to-br from-teal-500 to-teal-600 text-white rounded-3xl px-12 py-8 shadow-xl max-w-2xl mb-10"
						role="region"
						aria-label="Welcome message from Golby"
					>
						<h1 className="text-4xl font-bold mb-3">Hi, I'm Golby!</h1>
						<p className="text-lg opacity-95 leading-relaxed">
							Your friendly AI travel assistant. Ask me anything about environmental risks, travel safety, or how to use RiskRadar!
						</p>
						{/* Speech bubble arrow */}
						<div className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-t-8 border-l-transparent border-r-transparent border-t-teal-600"></div>
					</motion.div>
				</div>

				{/* Tips/Fun Facts */}
				<motion.ul
					className="mb-10 space-y-3 max-w-2xl mx-auto"
					aria-label="Golby tips and fun facts"
				>
					{tips.map((tip, idx) => (
						<motion.li
							key={idx}
							initial={{ opacity: 0, x: -20 }}
							animate={{ opacity: 1, x: 0 }}
							transition={{ delay: 0.8 + idx * 0.1, duration: 0.4 }}
							className="flex items-start text-base text-teal-900 bg-teal-50 border border-teal-100 rounded-2xl px-6 py-4 shadow-sm"
						>
							<span role="img" aria-label="Golby tip" className="mr-3 text-xl flex-shrink-0">
								💡
							</span>
							<span className="leading-relaxed">{tip}</span>
						</motion.li>
					))}
				</motion.ul>

				{/* Get Started Button */}
				<motion.div
					className="text-center"
					initial={{ opacity: 0 }}
					animate={{ opacity: 1 }}
					transition={{ delay: 1.1, duration: 0.4 }}
				>
					<button
						onClick={onGetStarted}
						className="inline-flex items-center gap-2 bg-teal-500 hover:bg-teal-600 active:scale-95 text-white font-bold px-8 py-4 rounded-full shadow-lg transition-all duration-200 text-lg"
						aria-label="Get started with Golby"
					>
						<span>✨</span>
						Get Started
					</button>
					<p className="mt-6 text-sm text-gray-600">
						The Golby assistant is also available from anywhere in the app via the floating widget.
					</p>
				</motion.div>
			</motion.div>
		</motion.div>
	);
}

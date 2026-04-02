import React from 'react';
import { motion } from 'framer-motion';
import { GolbyIcon } from './GolbyIcon';

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
				className="mb-4"
			>
				<GolbyIcon expression="puzzled" size="lg" aria-label="Golby puzzled" />
			</motion.div>
			<h2 className="text-xl font-semibold mb-2 text-blue-900">{title}</h2>
			<p className="mb-4 text-gray-700">{message}</p>
			<ul className="mb-4 space-y-1">
				{suggestions.map((s, i) => (
					<li key={i} className="text-sm text-blue-700">• {s}</li>
				))}
			</ul>
			<div className="flex gap-2 justify-center">
				{onRetry && <button onClick={onRetry} className="bg-blue-600 text-white px-4 py-2 rounded-full shadow hover:bg-blue-700 transition" aria-label="Try again">Try again</button>}
				{onGoHome && <button onClick={onGoHome} className="bg-gray-200 text-blue-900 px-4 py-2 rounded-full shadow hover:bg-gray-300 transition" aria-label="Go home">Go home</button>}
				{onAskGolby && <button onClick={onAskGolby} className="bg-blue-100 text-blue-900 px-4 py-2 rounded-full shadow hover:bg-blue-200 transition" aria-label="Ask Golby">Ask Golby</button>}
			</div>
		</motion.div>
	);
}

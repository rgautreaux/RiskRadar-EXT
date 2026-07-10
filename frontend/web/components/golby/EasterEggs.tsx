import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { GolbyIcon } from './GolbyIcon';

interface EasterEggResponse {
	text: string;
	expression: 'happy' | 'laughing' | 'excited' | 'winking';
}

const jokes: EasterEggResponse[] = [
	{ text: "Why don't meteorologists like to go to parties? Because they always predict a chance of precipitation! ☔", expression: 'laughing' },
	{ text: "What's a tornado's favorite game to play? Twister! 🌪️", expression: 'laughing' },
	{ text: "Why did the cloud date the fog? Because he was so down to earth! ☁️", expression: 'winking' },
	{ text: "How do hurricanes see? With one eye! 👁️", expression: 'laughing' },
	{ text: "What did the thermometer say to the graduated cylinder? You may have graduated, but I've got more degrees! 🌡️", expression: 'excited' }
];

const greetings: EasterEggResponse[] = [
	{ text: "Hi there, superstar! Ready to explore the world safely? 🌟", expression: 'waving' },
	{ text: "Hey there, adventure seeker! What can I help you discover today? 🗺️", expression: 'excited' },
	{ text: "Hello! I'm Golby, your friendly AI assistant. Ask me anything!", expression: 'happy' }
];

export function EasterEggs({ type = 'joke' }: { type?: 'joke' | 'greeting' }) {
	const [show, setShow] = useState(true);
	const responses = type === 'joke' ? jokes : greetings;
	const response = responses[Math.floor(Math.random() * responses.length)];

	if (!show) return null;

	return (
		<AnimatePresence>
			<motion.div
				initial={{ opacity: 0, y: 10 }}
				animate={{ opacity: 1, y: 0 }}
				exit={{ opacity: 0, y: 10 }}
				className="flex items-center gap-3 bg-yellow-50 border border-yellow-200 rounded-xl shadow-lg p-4 max-w-md mx-auto mt-4"
				role="status"
				aria-label="Golby fun response"
			>
				<GolbyIcon expression={response.expression} size="md" aria-label="Golby fun" />
				<span className="text-yellow-900 text-base">{response.text}</span>
				<button onClick={() => setShow(false)} className="ml-auto text-yellow-700 hover:underline text-sm" aria-label="Dismiss">Dismiss</button>
			</motion.div>
		</AnimatePresence>
	);
}

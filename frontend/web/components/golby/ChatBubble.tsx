import React from 'react';
import { motion } from 'framer-motion';

interface ChatBubbleProps {
	message: string;
	isGolby?: boolean;
	children?: React.ReactNode;
	className?: string;
}

export function ChatBubble({ message, isGolby = false, children, className = '' }: ChatBubbleProps) {
	return (
		<motion.div
			initial={{ opacity: 0, y: 10, scale: 0.95 }}
			animate={{ opacity: 1, y: 0, scale: 1 }}
			transition={{ duration: 0.3, ease: 'easeOut' }}
			className={`max-w-md rounded-2xl px-4 py-3 shadow-sm ${
				isGolby 
					? 'bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-tl-sm' 
					: 'bg-gray-100 text-gray-900 rounded-tr-sm'
			} ${className}`}
			role="article"
			aria-label={isGolby ? "Message from Golby" : "Your message"}
		>
			{children || <p className="text-sm leading-relaxed">{message}</p>}
		</motion.div>
	);
}

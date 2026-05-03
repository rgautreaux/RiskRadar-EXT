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
			className={`${isGolby ? 'golby-bubble-golby' : 'golby-bubble-user'} ${className}`}
			role="article"
			aria-label={isGolby ? "Message from Golby" : "Your message"}
		>
			{children || <p className="text-sm leading-relaxed">{message}</p>}
		</motion.div>
	);
}

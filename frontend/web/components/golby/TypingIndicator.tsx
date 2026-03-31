import React from 'react';
import { motion } from 'framer-motion';

export function TypingIndicator() {
	return (
		<div 
			className="flex items-center gap-2 px-4 py-3 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl rounded-tl-sm max-w-[100px] shadow-sm"
			role="status"
			aria-label="Golby is typing"
		>
			{[0, 1, 2].map((index) => (
				<motion.div
					key={index}
					className="w-2 h-2 bg-white rounded-full"
					animate={{
						y: [0, -8, 0],
						opacity: [0.5, 1, 0.5]
					}}
					transition={{
						duration: 0.8,
						repeat: Infinity,
						delay: index * 0.2,
						ease: 'easeInOut'
					}}
				/>
			))}
			<span className="sr-only">Golby is thinking...</span>
		</div>
	);
}

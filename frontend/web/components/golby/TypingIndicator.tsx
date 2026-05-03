import React from 'react';
import { motion } from 'framer-motion';

export function TypingIndicator() {
	return (
		<div
			className="golby-typing-indicator"
			role="status"
			aria-label="Golby is typing"
		>
			{[0, 1, 2].map((index) => (
				<motion.div
					key={index}
					className="golby-typing-dot"
					animate={{ y: [0, -6, 0], opacity: [0.35, 1, 0.35] }}
					transition={{
						duration: 0.9,
						repeat: Infinity,
						delay: index * 0.18,
						ease: 'easeInOut',
					}}
				/>
			))}
			<span className="sr-only">Golby is thinking…</span>
		</div>
	);
}

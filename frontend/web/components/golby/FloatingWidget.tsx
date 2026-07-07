import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { GolbyIcon } from './GolbyIcon';

interface FloatingWidgetProps {
	onOpen?: () => void;
	position?: 'bottom-right' | 'bottom-left';
	showTooltip?: boolean;
}

export function FloatingWidget({
	onOpen,
	position = 'bottom-right',
	showTooltip = true
}: FloatingWidgetProps) {
	const [isHovered, setIsHovered] = useState(false);
	const [tooltipVisible, setTooltipVisible] = useState(true);

	const positionClasses = {
		'bottom-right': 'bottom-6 right-6',
		'bottom-left': 'bottom-6 left-6'
	};

	return (
		<div className={`fixed ${positionClasses[position]} z-50`}>
			{/* Tooltip */}
			<AnimatePresence>
				{showTooltip && tooltipVisible && !isHovered && (
					<motion.div
						initial={{ opacity: 0, x: position === 'bottom-right' ? 20 : -20, scale: 0.8 }}
						animate={{ opacity: 1, x: 0, scale: 1 }}
						exit={{ opacity: 0, scale: 0.8 }}
						className={`absolute bottom-full mb-3 ${position === 'bottom-right' ? 'right-0' : 'left-0'} bg-white px-4 py-2 rounded-lg shadow-lg border border-gray-200 whitespace-nowrap`}
						role="tooltip"
						aria-label="Need help? Ask Golby!"
					>
						<p className="text-sm font-medium text-gray-900">Need help? Ask Golby!</p>
						<button
							onClick={() => setTooltipVisible(false)}
							className="absolute -top-1 -right-1 bg-gray-100 rounded-full p-0.5 hover:bg-gray-200"
							aria-label="Dismiss tooltip"
						>
							×
						</button>
						{/* Arrow */}
						<div
							className={`absolute top-full ${position === 'bottom-right' ? 'right-4' : 'left-4'} w-0 h-0 border-l-8 border-r-8 border-t-8 border-transparent border-t-white`}
							style={{ marginTop: '-1px' }}
						/>
					</motion.div>
				)}
			</AnimatePresence>
			{/* Floating Button */}
			<motion.button
				className="golby-float-btn"
				aria-label="Open Golby AI Assistant"
				onClick={onOpen}
				onMouseEnter={() => setIsHovered(true)}
				onMouseLeave={() => setIsHovered(false)}
				tabIndex={0}
			>
				<GolbyIcon expression={isHovered ? 'winking' : 'waving'} size="lg" animate />
				<span className="sr-only">Open Golby AI Assistant</span>
			</motion.button>
		</div>
	);
}

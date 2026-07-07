import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { GolbyIcon } from './GolbyIcon';

interface ContextualHelpProps {
	tip: string;
	position?: 'top' | 'bottom' | 'left' | 'right';
	onDismiss?: () => void;
	onLearnMore?: () => void;
	autoShow?: boolean;
}

export function ContextualHelp({ 
	tip, 
	position = 'top',
	onDismiss,
	onLearnMore,
	autoShow = true
}: ContextualHelpProps) {
	const [isVisible, setIsVisible] = useState(autoShow);

	const handleDismiss = () => {
		setIsVisible(false);
		onDismiss?.();
	};

	const positionClasses = {
		top: 'bottom-full mb-2',
		bottom: 'top-full mt-2',
		left: 'right-full mr-2',
		right: 'left-full ml-2'
	};

	const arrowClasses = {
		top: 'top-full left-1/2 -ml-2 border-l-8 border-r-8 border-t-8 border-transparent border-t-white',
		bottom: 'bottom-full left-1/2 -ml-2 border-l-8 border-r-8 border-b-8 border-transparent border-b-white',
		left: 'left-full top-1/2 -mt-2 border-t-8 border-b-8 border-l-8 border-transparent border-l-white',
		right: 'right-full top-1/2 -mt-2 border-t-8 border-b-8 border-r-8 border-transparent border-r-white'
	};

	if (!isVisible) return null;

	return (
		<AnimatePresence>
			<motion.div
				initial={{ opacity: 0, y: 10 }}
				animate={{ opacity: 1, y: 0 }}
				exit={{ opacity: 0, y: 10 }}
				className={`absolute z-50 bg-white border border-gray-200 rounded-xl shadow-lg p-4 flex items-center gap-3 ${positionClasses[position]}`}
				role="dialog"
				aria-label="Golby tip"
			>
				<GolbyIcon expression="happy" size="sm" aria-label="Golby tip icon" />
				<span className="text-gray-900 text-base">{tip}</span>
				<div className="flex gap-2 ml-4">
					<button onClick={handleDismiss} className="text-blue-600 hover:underline text-sm" aria-label="Got it">Got it!</button>
					{onLearnMore && <button onClick={onLearnMore} className="text-blue-600 hover:underline text-sm" aria-label="Tell me more">Tell me more</button>}
				</div>
				<div className={`absolute ${arrowClasses[position]}`} />
			</motion.div>
		</AnimatePresence>
	);
}

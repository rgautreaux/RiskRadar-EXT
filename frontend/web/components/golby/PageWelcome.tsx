import React from 'react';
import { motion, useReducedMotion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';
import { GolbyIcon } from './GolbyIcon';

interface PageWelcomeProps {
	onGetStarted?: () => void;
}

const capabilities = [
	'Current alerts and severity levels for any region',
	'Forecast conditions along your planned route',
	'Guidance on reading and acting on RiskRadar alerts',
];

export function PageWelcome({ onGetStarted }: PageWelcomeProps) {
	const prefersReducedMotion = useReducedMotion();

	const dur = (d: number) => (prefersReducedMotion ? 0 : d);
	const del = (d: number) => (prefersReducedMotion ? 0 : d);

	const fadeUp = (delay: number) => ({
		initial: { opacity: 0, y: prefersReducedMotion ? 0 : 18 },
		animate: { opacity: 1, y: 0 },
		transition: { duration: dur(0.52), delay: del(delay), ease: [0.16, 1, 0.3, 1] as const },
	});

	return (
		<div className="golby-welcome" role="main" aria-label="Welcome to Golby AI Assistant">
			<div className="golby-welcome-inner">
				{/* Content column */}
				<div>
					<motion.span className="golby-welcome-badge" {...fadeUp(0.05)}>
						AI Assistant · RiskRadar
					</motion.span>

					<motion.h1 className="golby-welcome-heading" {...fadeUp(0.12)}>
						Ask Golby anything<br />about your route.
					</motion.h1>

					<motion.p className="golby-welcome-sub" {...fadeUp(0.2)}>
						Environmental risks, forecast conditions, and alert explanations — drawn from live
						RiskRadar data so you can make informed decisions with confidence.
					</motion.p>

					<motion.ul
						className="golby-welcome-capabilities"
						initial={{ opacity: 0 }}
						animate={{ opacity: 1 }}
						transition={{ duration: dur(0.35), delay: del(0.28) }}
						aria-label="What Golby can help with"
					>
						{capabilities.map((cap, idx) => (
							<motion.li
								key={idx}
								initial={{ opacity: 0, x: prefersReducedMotion ? 0 : -14 }}
								animate={{ opacity: 1, x: 0 }}
								transition={{ duration: dur(0.42), delay: del(0.33 + idx * 0.08), ease: [0.16, 1, 0.3, 1] as const }}
							>
								{cap}
							</motion.li>
						))}
					</motion.ul>

					<motion.div {...fadeUp(0.54)}>
						<button
							onClick={onGetStarted}
							className="golby-cta-btn"
							aria-label="Start a conversation with Golby"
						>
							Start a conversation
							<ArrowRight size={17} aria-hidden="true" />
						</button>
						<p className="golby-welcome-footnote">
							Golby is also available from the floating widget anywhere in RiskRadar.
						</p>
					</motion.div>
				</div>

				{/* Golby visual column */}
				<motion.div
					className="golby-welcome-visual"
					aria-hidden="true"
					initial={{ opacity: 0, scale: prefersReducedMotion ? 1 : 0.85 }}
					animate={{ opacity: 1, scale: 1 }}
					transition={{ duration: dur(0.65), delay: del(0.08), ease: [0.16, 1, 0.3, 1] as const }}
				>
					<div className="golby-visual-circle">
						<GolbyIcon expression="waving" size="xl" />
					</div>
				</motion.div>
			</div>
		</div>
	);
}

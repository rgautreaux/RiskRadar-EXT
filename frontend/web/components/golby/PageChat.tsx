import React from 'react';
import { motion } from 'framer-motion';
import { ChatInterface } from './ChatInterface';

interface PageChatProps {
	pageContext?: string;
	isAdmin?: boolean;
	currentUserId?: number;
	onBack?: () => void;
}

export function PageChat({
	pageContext = 'assistant',
	isAdmin = false,
	currentUserId,
	onBack
}: PageChatProps) {
	return (
		<motion.div
			initial={{ opacity: 0 }}
			animate={{ opacity: 1 }}
			transition={{ duration: 0.3 }}
			className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 flex flex-col"
		>
			{/* Header with back button */}
			<div className="bg-gradient-to-r from-teal-600 to-teal-700 text-white px-6 py-4 shadow-md flex items-center justify-between">
				<div className="flex items-center gap-4 flex-1">
					<div className="flex-1">
						<h1 className="text-2xl font-bold">Chat with Golby</h1>
						<p className="text-teal-100 text-sm">Your AI Travel Assistant</p>
					</div>
				</div>
				{onBack && (
					<button
						onClick={onBack}
						className="text-white hover:text-teal-100 text-lg font-bold px-4 py-2 rounded-lg transition-colors hover:bg-teal-700/50"
						aria-label="Back to welcome"
						title="Back to welcome screen"
					>
						←
					</button>
				)}
			</div>

			{/* Chat container */}
			<div className="flex-1 p-6 overflow-hidden">
				<div className="mx-auto max-w-4xl h-full">
					<style>{`
						.page-chat-container {
							display: flex;
							flex-direction: column;
							height: 100%;
							background: white;
							border-radius: 16px;
							box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
							overflow: hidden;
						}
						.page-chat-container > div {
							flex: 1;
							overflow: hidden;
						}
					`}</style>
					<div className="page-chat-container">
						<ChatInterface
							onClose={onBack}
							pageContext={pageContext}
							isAdmin={isAdmin}
							currentUserId={currentUserId}
						/>
					</div>
				</div>
			</div>
		</motion.div>
	);
}

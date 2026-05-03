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
			transition={{ duration: 0.25 }}
			className="golby-page-chat"
		>
			<ChatInterface
				onClose={onBack}
				pageContext={pageContext}
				isAdmin={isAdmin}
				currentUserId={currentUserId}
				fullPage
			/>
		</motion.div>
	);
}

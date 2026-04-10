import React, { useState, useRef, useEffect } from 'react';
import { fetchUserGuide, searchDocForAnswer } from './docSearch';
import { fetchCurrentAlerts, fetchRiskOverlay, fetchForecast, sendGolbyFeedback } from './apiClient';
import { motion } from 'framer-motion';
import { GolbyIcon } from './GolbyIcon';
import { ChatBubble } from './ChatBubble';
import { TypingIndicator } from './TypingIndicator';
import { Send, ThumbsUp, ThumbsDown, Smile } from 'lucide-react';

type ResponseCategory = 'docs' | 'page' | 'live' | 'playful' | 'static';
type FeedbackReaction = 'thumbs_up' | 'thumbs_down' | 'smile';

interface AssistantProfile {
	docs: number;
	page: number;
	live: number;
	playful: number;
	static: number;
}

interface Message {
	id: string;
	text: string;
	isGolby: boolean;
	timestamp: Date;
	responseCategory?: ResponseCategory;
}

interface ChatInterfaceProps {
	suggestions?: string[];
	onClose?: () => void;
	pageContext?: string;
}

const defaultSuggestions = [
	"Show me today's forecast",
	"How do I set alerts?",
	"Tell me a joke!",
	"What are the risks in my area?"
];

// Fun Easter Egg responses
const golbyJokes = [
	"Why did the weather map break up with the compass? Because it found someone more climate! 😄",
	"What's a tornado's favorite game? Twister! 🌪️",
	"Why did the cloud stay home from school? It was feeling under the weather! ☁️",
	"What do you call dangerous precipitation? A rain of terror! ☔️",
	"Why did the sun go to school? To get a little brighter! ☀️",
	"How do hurricanes see? With one eye! 🌀",
	"Why don’t mountains get cold in the winter? They wear snowcaps! 🏔️",
	"What’s a snowman’s favorite snack? Ice Krispies! ⛄️",
	"Why did the bicycle fall over on its trip? It was two-tired! 🚲",
	"Why did the traveler bring a ladder to the bar? Because they heard the drinks were on the house! 🍹",
	"Why did the airplane get sent to its room? For having a bad altitude! ✈️",
	"What do you call a bear caught in the rain? A drizzly bear! 🐻",
	"Why did the river never get lost? It always followed its current! 🏞️"
];

const golbyGreetings = [
	"Hi there, superstar! 🌟 How can I help you today?",
	"Hey there! Ready to explore some environmental insights? 🌍",
	"Hello, traveler! Where are you headed today? 🧳",
	"Greetings, explorer! Need a weather update or a fun fact? ☀️",
	"Welcome back! Let’s make your journey safe and fun. 🚦",
	"Hey! Golby here, your trusty travel buddy. How can I assist? 🐟",
	"Hi! Want a forecast, a risk check, or just a good laugh? 😄"
];

const golbyResponses: Record<string, string> = {
	"help": "I'm here to help! You can ask me about environmental risks, how to use RiskRadar, weather forecasts, or even just chat. What would you like to know?",
	"default": "Great question! I can help you with that. RiskRadar provides comprehensive environmental risk data to help you make informed travel decisions. What specific information are you looking for?"
};

const DEFAULT_PROFILE: AssistantProfile = {
	docs: 0,
	page: 0,
	live: 0,
	playful: 0,
	static: 0,
};

const PROFILE_STORAGE_KEY = 'golby-assistant-profile';
const SESSION_STORAGE_KEY = 'golby-session-id';

function createMessageId() {
	if (typeof window !== 'undefined' && window.crypto?.randomUUID) {
		return window.crypto.randomUUID();
	}

	return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function readStoredProfile(): AssistantProfile {
	if (typeof window === 'undefined') {
		return { ...DEFAULT_PROFILE };
	}

	try {
		const rawProfile = window.localStorage.getItem(PROFILE_STORAGE_KEY);
		if (!rawProfile) {
			return { ...DEFAULT_PROFILE };
		}

		return { ...DEFAULT_PROFILE, ...JSON.parse(rawProfile) };
	} catch {
		return { ...DEFAULT_PROFILE };
	}
}

function persistProfile(profile: AssistantProfile) {
	if (typeof window === 'undefined') {
		return;
	}

	try {
		window.localStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(profile));
	} catch {
		// Ignore storage failures so chat remains usable.
	}
}

function getSessionId() {
	if (typeof window === 'undefined') {
		return 'server-session';
	}

	const existing = window.localStorage.getItem(SESSION_STORAGE_KEY);
	if (existing) {
		return existing;
	}

	const sessionId = createMessageId();
	window.localStorage.setItem(SESSION_STORAGE_KEY, sessionId);
	return sessionId;
}

function reactionToRating(reaction: FeedbackReaction) {
	switch (reaction) {
		case 'thumbs_up':
			return 5;
		case 'smile':
			return 4;
		case 'thumbs_down':
		default:
			return 1;
	}
}

function reactionDelta(reaction: FeedbackReaction) {
	return reactionToRating(reaction) - 3;
}

function classifyTopic(message: string): 'forecast' | 'alert' | 'risk' | 'joke' | 'greeting' | 'help' | 'general' {
	if (message.includes('joke')) {
		return 'joke';
	}
	if (message.includes('hello') || message.includes('hi')) {
		return 'greeting';
	}
	if (message.includes('forecast') || message.includes('weather')) {
		return 'forecast';
	}
	if (message.includes('alert')) {
		return 'alert';
	}
	if (message.includes('risk')) {
		return 'risk';
	}
	if (message.includes('help')) {
		return 'help';
	}
	return 'general';
}

function getOrderedCategories(topic: ReturnType<typeof classifyTopic>, profile: AssistantProfile): ResponseCategory[] {
	const candidateOrders: Record<typeof topic, ResponseCategory[]> = {
		forecast: ['docs', 'page', 'live', 'static'],
		alert: ['docs', 'page', 'live', 'static'],
		risk: ['docs', 'page', 'live', 'static'],
		joke: ['playful', 'static'],
		greeting: ['playful', 'static'],
		help: ['docs', 'static', 'page', 'live'],
		general: ['docs', 'page', 'live', 'static'],
	};

	return candidateOrders[topic]
		.slice()
		.sort((left, right) => {
			const scoreDelta = profile[right] - profile[left];
			if (scoreDelta !== 0) {
				return scoreDelta;
			}

			return candidateOrders[topic].indexOf(left) - candidateOrders[topic].indexOf(right);
		});
}

function applyFeedback(profile: AssistantProfile, category: ResponseCategory, reaction: FeedbackReaction) {
	const nextProfile = { ...profile };
	nextProfile[category] += reactionDelta(reaction);
	return nextProfile;
}

export function ChatInterface({ suggestions = defaultSuggestions, onClose, pageContext = 'unknown' }: ChatInterfaceProps) {
	const [messages, setMessages] = useState<Message[]>([
		{
			id: '1',
			text: "Hey there! I'm Golby, your travel safety buddy. What can I help you discover today?",
			isGolby: true,
			timestamp: new Date(),
			responseCategory: 'playful'
		}
	]);
	const [inputValue, setInputValue] = useState('');
	const [isTyping, setIsTyping] = useState(false);
	const [userGuide, setUserGuide] = useState<string | null>(null);
	const [assistantProfile, setAssistantProfile] = useState<AssistantProfile>(() => readStoredProfile());
	const messagesEndRef = useRef<HTMLDivElement>(null);
	const sessionIdRef = useRef(getSessionId());
	// Fetch USER_GUIDE.md on mount
	useEffect(() => {
		fetchUserGuide().then(setUserGuide).catch(() => setUserGuide(null));
	}, []);

	const scrollToBottom = () => {
		messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
	};

	useEffect(() => {
		scrollToBottom();
	}, [messages, isTyping]);

	useEffect(() => {
		persistProfile(assistantProfile);
	}, [assistantProfile]);




	// Async: Try to answer from docs, page context, live data, and then fallback to static.
	const getGolbyResponse = async (userMessage: string): Promise<{ text: string; category: ResponseCategory }> => {
		const lowerMessage = userMessage.toLowerCase();
		const topic = classifyTopic(lowerMessage);
		const orderedCategories = getOrderedCategories(topic, assistantProfile);

		for (const category of orderedCategories) {
			if (category === 'docs') {
				if (userGuide && topic !== 'joke' && topic !== 'greeting') {
					const docAnswer = searchDocForAnswer(userGuide, userMessage);
					if (!docAnswer.startsWith('Sorry')) {
						return { text: docAnswer, category: 'docs' };
					}
				}
				continue;
			}

			if (category === 'page') {
				if (pageContext === 'map' && lowerMessage.includes('risk')) {
					return {
						text: "You're on the map view! Click any location to see detailed risk scores and environmental data for that area.",
						category: 'page',
					};
				}
				if (pageContext === 'alerts' && lowerMessage.includes('alert')) {
					return {
						text: "You're viewing alerts. Here you can see all current environmental alerts for your selected region. Want help setting up custom alerts?",
						category: 'page',
					};
				}
				if (pageContext === 'dashboard') {
					return {
						text: "This is your dashboard, where you can get a quick overview of your travel safety, recent alerts, and personalized recommendations.",
						category: 'page',
					};
				}
				if (pageContext === 'profile') {
					return {
						text: "You're on your profile page. Here you can update your information, preferences, and notification settings.",
						category: 'page',
					};
				}
				if (pageContext === 'settings') {
					return {
						text: "You're in settings. Adjust your preferences, manage alerts, and customize your RiskRadar experience here.",
						category: 'page',
					};
				}
				if (pageContext === 'forecast' && lowerMessage.includes('forecast')) {
					return {
						text: "You're on the forecast page. Enter a location or use your current location to get the latest environmental forecast.",
						category: 'page',
					};
				}
				continue;
			}

			if (category === 'live') {
				try {
					if (lowerMessage.includes('current alert') || lowerMessage.includes('latest alert')) {
						const alerts = await fetchCurrentAlerts();
						if (alerts && alerts.length > 0) {
							return {
								text: `Here are the latest alerts:\n` + alerts.map((a: any) => `• ${a.title || a.alert_type || 'Alert'} (${a.severity || 'unknown'})`).join('\n'),
								category: 'live',
							};
						}
						return { text: 'There are no current alerts.', category: 'live' };
					}
					if (lowerMessage.includes('risk') && lowerMessage.includes('map')) {
						const risk = await fetchRiskOverlay();
						if (risk && risk.risk_zones && risk.risk_zones.length > 0) {
							const high = risk.risk_zones.filter((z: any) => z.risk_level === 'high').length;
							const mod = risk.risk_zones.filter((z: any) => z.risk_level === 'moderate').length;
							const low = risk.risk_zones.filter((z: any) => z.risk_level === 'low').length;
							return { text: `Current map risk overlay:\nHigh risk: ${high}, Moderate: ${mod}, Low: ${low}`, category: 'live' };
						}
						return { text: 'No risk data available for the map.', category: 'live' };
					}
					if (lowerMessage.includes('forecast')) {
						const match = userMessage.match(/forecast for ([\w\s,]+)/i);
						const location = match ? match[1].trim() : '';
						const forecast = await fetchForecast(location);
						if (forecast && forecast.risk_zones && forecast.risk_zones.length > 0) {
							const high = forecast.risk_zones.filter((z: any) => z.risk_level === 'high').length;
							const mod = forecast.risk_zones.filter((z: any) => z.risk_level === 'moderate').length;
							const low = forecast.risk_zones.filter((z: any) => z.risk_level === 'low').length;
							return { text: `Forecast for ${location || 'your area'}:\nHigh risk: ${high}, Moderate: ${mod}, Low: ${low}`, category: 'live' };
						}
						return { text: `No forecast data available${location ? ' for ' + location : ''}.`, category: 'live' };
					}
				} catch {
					return { text: 'Sorry, I had trouble fetching live data.', category: 'live' };
				}
				continue;
			}

			if (category === 'playful') {
				if (topic === 'joke') {
					return { text: golbyJokes[Math.floor(Math.random() * golbyJokes.length)], category: 'playful' };
				}
				if (topic === 'greeting') {
					return { text: golbyGreetings[Math.floor(Math.random() * golbyGreetings.length)], category: 'playful' };
				}
				continue;
			}

			if (category === 'static') {
				if (lowerMessage.includes('help')) {
					return { text: golbyResponses['help'], category: 'static' };
				if (pageContext === 'dashboard') {
					return {
						text: "This is your dashboard, where you can get a quick overview of your travel safety, recent alerts, and personalized recommendations.",
						category: 'page',
					};
				}
				if (pageContext === 'profile') {
					return {
						text: "You're on your profile page. Here you can update your information, preferences, and notification settings.",
						category: 'page',
					};
				}
				if (pageContext === 'settings') {
					return {
						text: "You're in settings. Adjust your preferences, manage alerts, and customize your RiskRadar experience here.",
						category: 'page',
					};
				}
				}
				if (lowerMessage.includes('forecast') || lowerMessage.includes('weather')) {
					return { text: "The forecast looks clear ahead! ☀️ I can pull up detailed environmental data for any location you're interested in. Which area would you like to check?", category: 'static' };
				}
				if (lowerMessage.includes('alert')) {
					return { text: "Setting up alerts is easy! Head to your settings, choose 'Notifications', and you can customize alerts for specific risk types or locations. Want me to guide you there?", category: 'static' };
				}
				if (lowerMessage.includes('risk')) {
					return { text: "I can show you comprehensive risk assessments including air quality, natural disasters, climate risks, and more. Just click on any location on the map, or tell me which area you're curious about!", category: 'static' };
				}
				return { text: golbyResponses['default'], category: 'static' };
			}
		}

		return { text: golbyResponses['default'], category: 'static' };
	};

	const handleFeedback = async (message: Message, reaction: FeedbackReaction) => {
		const category = message.responseCategory ?? 'static';
		setAssistantProfile((currentProfile) => {
			const nextProfile = applyFeedback(currentProfile, category, reaction);
			persistProfile(nextProfile);
			return nextProfile;
		});

		try {
			await sendGolbyFeedback({
				session_id: sessionIdRef.current,
				message_id: message.id,
				reaction,
				rating: reactionToRating(reaction),
				page_context: pageContext,
				response_category: category,
				response_text: message.text,
			});
		} catch {
			// Keep the local learning loop working even if the backend call fails.
		}
	};

	const handleSendMessage = async (text: string) => {
		if (!text.trim()) return;
		// Add user message
		const userMessage: Message = {
			id: createMessageId(),
			text: text,
			isGolby: false,
			timestamp: new Date()
		};
		setMessages(prev => [...prev, userMessage]);
		setInputValue('');
		// Simulate Golby typing
		setIsTyping(true);
		const response = await getGolbyResponse(text);
		setIsTyping(false);
		const golbyMessage: Message = {
			id: createMessageId(),
			text: response.text,
			isGolby: true,
			timestamp: new Date(),
			responseCategory: response.category,
		};
		setMessages(prev => [...prev, golbyMessage]);
	};

	const handleSuggestionClick = (suggestion: string) => {
		handleSendMessage(suggestion);
	};

	return (
		<div className="flex flex-col h-full max-h-[600px] bg-white rounded-2xl shadow-xl overflow-hidden">
			{/* Header */}
			<div className="bg-gradient-to-r from-blue-600 to-blue-700 px-6 py-4 flex items-center gap-3">
				<GolbyIcon expression="happy" size="md" />
				<div className="flex-1">
					<h2 className="text-white font-medium">Chat with Golby</h2>
					<p className="text-blue-100 text-sm">Your AI Travel Assistant</p>
				</div>
				{onClose && (
					<button onClick={onClose} className="text-white hover:text-blue-200 text-xl font-bold ml-2" aria-label="Close chat">×</button>
				)}
			</div>
			{/* Messages */}
			<div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
				{messages.map((message) => (
					<div
						key={message.id}
						className={`flex gap-3 ${message.isGolby ? 'justify-start' : 'justify-end'}`}
					>
						{message.isGolby && (
							<div className="flex-shrink-0">
								<GolbyIcon expression="happy" size="sm" />
							</div>
						)}
						<div className={`flex flex-col ${message.isGolby ? 'items-start' : 'items-end'}`}>
							<ChatBubble message={message.text} isGolby={message.isGolby} />
							{message.isGolby && (
								<div className="flex gap-2 mt-2">
									<button 
										className="text-gray-400 hover:text-green-600 transition-colors"
										onClick={() => handleFeedback(message, 'thumbs_up')}
										aria-label="This was helpful"
									>
										<ThumbsUp className="w-4 h-4" />
									</button>
									<button 
										className="text-gray-400 hover:text-red-600 transition-colors"
										onClick={() => handleFeedback(message, 'thumbs_down')}
										aria-label="This wasn't helpful"
									>
										<ThumbsDown className="w-4 h-4" />
									</button>
									<button 
										className="text-gray-400 hover:text-yellow-600 transition-colors"
										onClick={() => handleFeedback(message, 'smile')}
										aria-label="Rate with emoji"
									>
										<Smile className="w-4 h-4" />
									</button>
								</div>
							)}
						</div>
					</div>
				))}
				{isTyping && (
					<div className="flex gap-3 justify-start">
						<div className="flex-shrink-0">
							<GolbyIcon expression="thinking" size="sm" />
						</div>
						<TypingIndicator />
					</div>
				)}
				<div ref={messagesEndRef} />
			</div>
			{/* Quick Suggestions */}
			{messages.length === 1 && (
				<motion.div 
					initial={{ opacity: 0, y: 10 }}
					animate={{ opacity: 1, y: 0 }}
					className="px-6 py-3 bg-white border-t border-gray-200"
				>
					<p className="text-xs text-gray-500 mb-2">Quick suggestions:</p>
					<div className="flex flex-wrap gap-2">
						{suggestions.map((suggestion, index) => (
							<motion.button
								key={index}
								initial={{ opacity: 0, scale: 0.9 }}
								animate={{ opacity: 1, scale: 1 }}
								transition={{ delay: index * 0.1 }}
								onClick={() => handleSuggestionClick(suggestion)}
								className="bg-blue-50 hover:bg-blue-100 text-blue-700 px-3 py-1.5 rounded-full text-sm transition-colors border border-blue-200"
								whileHover={{ scale: 1.05 }}
								whileTap={{ scale: 0.95 }}
							>
								{suggestion}
							</motion.button>
						))}
					</div>
				</motion.div>
			)}
			{/* Input */}
			<div className="bg-white px-6 py-4 border-t border-gray-200">
				<form 
					onSubmit={(e) => {
						e.preventDefault();
						handleSendMessage(inputValue);
					}}
					className="flex gap-2"
				>
					<input
						type="text"
						value={inputValue}
						onChange={(e) => setInputValue(e.target.value)}
						placeholder="Ask Golby anything..."
						className="flex-1 px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
						aria-label="Message input"
					/>
					<button
						type="submit"
						disabled={!inputValue.trim()}
						className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white p-2 rounded-full transition-colors disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500"
						aria-label="Send message"
					>
						<Send className="w-5 h-5" />
					</button>
				</form>
			</div>
		</div>
	);
}

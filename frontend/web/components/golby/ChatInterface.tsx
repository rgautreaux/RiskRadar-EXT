import React, { useState, useRef, useEffect } from 'react';
import { fetchUserGuide, searchDocForAnswer } from './docSearch';
import { fetchCurrentAlerts, fetchRiskOverlay, fetchForecast } from './apiClient';
import { motion, AnimatePresence } from 'framer-motion';
import { GolbyIcon } from './GolbyIcon';
import { ChatBubble } from './ChatBubble';
import { TypingIndicator } from './TypingIndicator';
import { Send, ThumbsUp, ThumbsDown, Smile } from 'lucide-react';

interface Message {
	id: string;
	text: string;
	isGolby: boolean;
	timestamp: Date;
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

export function ChatInterface({ suggestions = defaultSuggestions, onClose, pageContext = 'unknown' }: ChatInterfaceProps) {
	const [messages, setMessages] = useState<Message[]>([
		{
			id: '1',
			text: "Hey there! I'm Golby, your travel safety buddy. What can I help you discover today?",
			isGolby: true,
			timestamp: new Date()
		}
	]);
	const [inputValue, setInputValue] = useState('');
	const [isTyping, setIsTyping] = useState(false);
	const [userGuide, setUserGuide] = useState<string | null>(null);
	const messagesEndRef = useRef<HTMLDivElement>(null);
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




	// Async: Try to answer from docs, then with page context, then with live data, else fallback to static
	const getGolbyResponse = async (userMessage: string): Promise<string> => {
		const lowerMessage = userMessage.toLowerCase();
		// 1. Try documentation if loaded and not a joke/greeting
		if (userGuide && !lowerMessage.includes('joke') && !lowerMessage.includes('hello') && !lowerMessage.includes('hi')) {
			const docAnswer = searchDocForAnswer(userGuide, userMessage);
			if (!docAnswer.startsWith("Sorry")) {
				return docAnswer;
			}
		}
		// 2. Page-aware answers
		if (pageContext === 'map' && lowerMessage.includes('risk')) {
			return "You're on the map view! Click any location to see detailed risk scores and environmental data for that area.";
		}
		if (pageContext === 'alerts' && lowerMessage.includes('alert')) {
			return "You're viewing alerts. Here you can see all current environmental alerts for your selected region. Want help setting up custom alerts?";
		}
		if (pageContext === 'dashboard') {
			return "This is your dashboard, where you can get a quick overview of your travel safety, recent alerts, and personalized recommendations.";
		}
		if (pageContext === 'profile') {
			return "You're on your profile page. Here you can update your information, preferences, and notification settings.";
		}
		if (pageContext === 'settings') {
			return "You're in settings. Adjust your preferences, manage alerts, and customize your RiskRadar experience here.";
		}
		if (pageContext === 'forecast' && lowerMessage.includes('forecast')) {
			return "You're on the forecast page. Enter a location or use your current location to get the latest environmental forecast.";
		}
		// 3. Live data answers
		try {
			if (lowerMessage.includes('current alert') || lowerMessage.includes('latest alert')) {
				const alerts = await fetchCurrentAlerts();
				if (alerts && alerts.length > 0) {
					return `Here are the latest alerts:\n` + alerts.map((a: any) => `• ${a.title || a.alert_type || 'Alert'} (${a.severity || 'unknown'})`).join('\n');
				} else {
					return 'There are no current alerts.';
				}
			}
			if (lowerMessage.includes('risk') && lowerMessage.includes('map')) {
				const risk = await fetchRiskOverlay();
				if (risk && risk.risk_zones && risk.risk_zones.length > 0) {
					const high = risk.risk_zones.filter((z: any) => z.risk_level === 'high').length;
					const mod = risk.risk_zones.filter((z: any) => z.risk_level === 'moderate').length;
					const low = risk.risk_zones.filter((z: any) => z.risk_level === 'low').length;
					return `Current map risk overlay:\nHigh risk: ${high}, Moderate: ${mod}, Low: ${low}`;
				} else {
					return 'No risk data available for the map.';
				}
			}
			if (lowerMessage.includes('forecast')) {
				const match = userMessage.match(/forecast for ([\w\s,]+)/i);
				const location = match ? match[1].trim() : '';
				const forecast = await fetchForecast(location);
				if (forecast && forecast.risk_zones && forecast.risk_zones.length > 0) {
					const high = forecast.risk_zones.filter((z: any) => z.risk_level === 'high').length;
					const mod = forecast.risk_zones.filter((z: any) => z.risk_level === 'moderate').length;
					const low = forecast.risk_zones.filter((z: any) => z.risk_level === 'low').length;
					return `Forecast for ${location || 'your area'}:\nHigh risk: ${high}, Moderate: ${mod}, Low: ${low}`;
				} else {
					return `No forecast data available${location ? ' for ' + location : ''}.`;
				}
			}
		} catch (e) {
			return 'Sorry, I had trouble fetching live data.';
		}
		// 4. Fallback to static
			if (lowerMessage.includes('joke')) {
				// Random joke
				return golbyJokes[Math.floor(Math.random() * golbyJokes.length)];
			}
			if (lowerMessage.includes('hello') || lowerMessage.includes('hi')) {
				// Random greeting
				return golbyGreetings[Math.floor(Math.random() * golbyGreetings.length)];
			}
		if (lowerMessage.includes('help')) {
			return golbyResponses['help'];
		}
		if (lowerMessage.includes('forecast') || lowerMessage.includes('weather')) {
			return "The forecast looks clear ahead! ☀️ I can pull up detailed environmental data for any location you're interested in. Which area would you like to check?";
		}
		if (lowerMessage.includes('alert')) {
			return "Setting up alerts is easy! Head to your settings, choose 'Notifications', and you can customize alerts for specific risk types or locations. Want me to guide you there?";
		}
		if (lowerMessage.includes('risk')) {
			return "I can show you comprehensive risk assessments including air quality, natural disasters, climate risks, and more. Just click on any location on the map, or tell me which area you're curious about!";
		}
		return golbyResponses['default'];
	};

	const handleSendMessage = async (text: string) => {
		if (!text.trim()) return;
		// Add user message
		const userMessage: Message = {
			id: Date.now().toString(),
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
			id: (Date.now() + 1).toString(),
			text: response,
			isGolby: true,
			timestamp: new Date()
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
										aria-label="This was helpful"
									>
										<ThumbsUp className="w-4 h-4" />
									</button>
									<button 
										className="text-gray-400 hover:text-red-600 transition-colors"
										aria-label="This wasn't helpful"
									>
										<ThumbsDown className="w-4 h-4" />
									</button>
									<button 
										className="text-gray-400 hover:text-yellow-600 transition-colors"
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

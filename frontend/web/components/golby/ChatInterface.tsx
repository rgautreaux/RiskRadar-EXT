import { useState, useRef, useEffect } from 'react';
import { fetchUserGuide, searchDocForAnswer } from './docSearch';
import { fetchAssistantReply, fetchCurrentAlerts, fetchRiskOverlay, fetchForecast, fetchWeeklyFeedbackAnalytics, sendGolbyFeedback, syncGolbyStyleProfile } from './apiClient';
import { motion } from 'framer-motion';
import { GolbyIcon } from './GolbyIcon';
import { ChatBubble } from './ChatBubble';
import { TypingIndicator } from './TypingIndicator';
import { Send, ThumbsUp, ThumbsDown, Smile } from 'lucide-react';

type ResponseCategory = 'docs' | 'page' | 'live' | 'playful' | 'static';
type FeedbackReaction = 'thumbs_up' | 'thumbs_down' | 'smile';
type GuardrailCategory = 'medical' | 'legal' | 'emergency' | 'unsafe';

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

interface WeeklyAnalyticsPoint {
	date: string;
	count: number;
	average_rating: number | null;
}

interface WeeklyAnalyticsSummary {
	window_days: number;
	from_date: string;
	to_date: string;
	total_feedback: number;
	average_rating: number | null;
	by_day: WeeklyAnalyticsPoint[];
}

interface ChatInterfaceProps {
	suggestions?: string[];
	onClose?: () => void;
	pageContext?: string;
	isAdmin?: boolean;
	currentUserId?: number;
	fullPage?: boolean;
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
const FEEDBACK_COUNT_STORAGE_KEY = 'golby-feedback-count';
const STYLE_BIAS_STORAGE_KEY = 'golby-style-bias';

const PROFILE_CAP = 8;
const PROFILE_DECAY = 0.9;
const MIN_FEEDBACK_TO_REORDER = 3;
const MIN_FEEDBACK_TO_STYLE_SHIFT = 4;

type ResponseStyle = 'balanced' | 'concise' | 'detailed';

function clamp(value: number, min: number, max: number) {
	return Math.min(max, Math.max(min, value));
}

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

function readStoredNumber(key: string, fallback: number) {
	if (typeof window === 'undefined') {
		return fallback;
	}

	try {
		const rawValue = window.localStorage.getItem(key);
		if (!rawValue) {
			return fallback;
		}

		const parsed = Number(rawValue);
		if (Number.isNaN(parsed)) {
			return fallback;
		}

		return parsed;
	} catch {
		return fallback;
	}
}

function persistNumber(key: string, value: number) {
	if (typeof window === 'undefined') {
		return;
	}

	try {
		window.localStorage.setItem(key, String(value));
	} catch {
		// Ignore storage failures so chat remains usable.
	}
}

function getSessionId() {
	if (typeof window === 'undefined') {
		return 'server-session';
	}

	try {
		const existing = window.localStorage.getItem(SESSION_STORAGE_KEY);
		if (existing) {
			return existing;
		}

		const sessionId = createMessageId();
		window.localStorage.setItem(SESSION_STORAGE_KEY, sessionId);
		return sessionId;
	} catch {
		return createMessageId();
	}
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

const GUARDED_PATTERNS: Array<{ category: GuardrailCategory; regex: RegExp }> = [
	{ category: 'medical', regex: /\b(diagnose|diagnosis|prescription|dosage|dose|medication|treatment|medical advice)\b/i },
	{ category: 'legal', regex: /\b(legal advice|lawsuit|sue|liability|attorney|lawyer|court)\b/i },
	{ category: 'emergency', regex: /\b(call 911|emergency|evacuate now|life[- ]?threatening|immediate danger)\b/i },
	{ category: 'unsafe', regex: /\b(hack|bypass|exploit|steal|weapon|harm|violence|password|secret key|token)\b/i },
];

function detectGuardrailCategory(message: string): GuardrailCategory | null {
	for (const item of GUARDED_PATTERNS) {
		if (item.regex.test(message)) {
			return item.category;
		}
	}

	return null;
}

function getGuardrailResponse(category: GuardrailCategory): string {
	if (category === 'emergency') {
		return 'I cannot provide emergency-response instructions. If there is immediate danger, contact local emergency services and follow official local alerts.';
	}

	if (category === 'medical') {
		return 'I can explain RiskRadar environmental data, but I cannot provide medical advice, diagnosis, or treatment guidance. Please consult a qualified healthcare professional.';
	}

	if (category === 'legal') {
		return 'I cannot provide legal advice. Please consult a licensed attorney or official legal resources for legal questions.';
	}

	return 'I cannot help with harmful, illegal, or credential-related requests. I can still help interpret RiskRadar alerts, maps, and forecast data.';
}

function getOrderedCategories(topic: ReturnType<typeof classifyTopic>, profile: AssistantProfile, feedbackCount: number): ResponseCategory[] {
	const candidateOrders: Record<typeof topic, ResponseCategory[]> = {
		forecast: ['docs', 'page', 'live', 'static'],
		alert: ['docs', 'page', 'live', 'static'],
		risk: ['docs', 'page', 'live', 'static'],
		joke: ['playful', 'static'],
		greeting: ['playful', 'static'],
		help: ['docs', 'static', 'page', 'live'],
		general: ['docs', 'page', 'live', 'static'],
	};

	if (feedbackCount < MIN_FEEDBACK_TO_REORDER) {
		return candidateOrders[topic];
	}

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
	const nextProfile: AssistantProfile = {
		docs: clamp(profile.docs * PROFILE_DECAY, -PROFILE_CAP, PROFILE_CAP),
		page: clamp(profile.page * PROFILE_DECAY, -PROFILE_CAP, PROFILE_CAP),
		live: clamp(profile.live * PROFILE_DECAY, -PROFILE_CAP, PROFILE_CAP),
		playful: clamp(profile.playful * PROFILE_DECAY, -PROFILE_CAP, PROFILE_CAP),
		static: clamp(profile.static * PROFILE_DECAY, -PROFILE_CAP, PROFILE_CAP),
	};
	nextProfile[category] = clamp(nextProfile[category] + reactionDelta(reaction), -PROFILE_CAP, PROFILE_CAP);
	return nextProfile;
}

function updateStyleBias(currentStyleBias: number, reaction: FeedbackReaction, messageText: string) {
	const delta = reactionDelta(reaction);
	const isLongResponse = messageText.length > 180 || messageText.includes('\n');
	const styleDelta = isLongResponse ? delta : -delta;
	return clamp(currentStyleBias + styleDelta, -PROFILE_CAP, PROFILE_CAP);
}

function getResponseStyle(feedbackCount: number, styleBias: number): ResponseStyle {
	if (feedbackCount < MIN_FEEDBACK_TO_STYLE_SHIFT) {
		return 'balanced';
	}

	if (styleBias <= -2) {
		return 'concise';
	}

	if (styleBias >= 2) {
		return 'detailed';
	}

	return 'balanced';
}

function formatResponseForStyle(text: string, style: ResponseStyle, category: ResponseCategory) {
	if (style === 'balanced' || category === 'playful') {
		return text;
	}

	if (style === 'concise') {
		if (text.includes('\n')) {
			const lines = text.split('\n').filter(Boolean);
			return lines.slice(0, 2).join('\n');
		}
		if (text.length > 180) {
			return `${text.slice(0, 177)}...`;
		}
		return text;
	}

	if (text.length < 160) {
		return `${text} If you want, I can provide a deeper breakdown.`;
	}

	return text;
}

export function ChatInterface({
	suggestions = defaultSuggestions,
	onClose,
	pageContext = 'unknown',
	isAdmin = false,
	currentUserId,
	fullPage = false,
}: ChatInterfaceProps) {
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
	const [feedbackCount, setFeedbackCount] = useState<number>(() => readStoredNumber(FEEDBACK_COUNT_STORAGE_KEY, 0));
	const [styleBias, setStyleBias] = useState<number>(() => readStoredNumber(STYLE_BIAS_STORAGE_KEY, 0));
	const [showDiagnostics, setShowDiagnostics] = useState(false);
	const [runtimeDiagnostics, setRuntimeDiagnostics] = useState<string | null>(null);
	const [weeklyAnalytics, setWeeklyAnalytics] = useState<WeeklyAnalyticsSummary | null>(null);
	const [analyticsLoading, setAnalyticsLoading] = useState(false);
	const [analyticsError, setAnalyticsError] = useState<string | null>(null);
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

	useEffect(() => {
		persistNumber(FEEDBACK_COUNT_STORAGE_KEY, feedbackCount);
	}, [feedbackCount]);

	useEffect(() => {
		persistNumber(STYLE_BIAS_STORAGE_KEY, styleBias);
	}, [styleBias]);

	useEffect(() => {
		if (!isAdmin) {
			setShowDiagnostics(false);
		}
	}, [isAdmin]);

	const refreshWeeklyAnalytics = async () => {
		if (!isAdmin) {
			setAnalyticsError('Admin access required to view analytics.');
			setWeeklyAnalytics(null);
			return;
		}
		setAnalyticsLoading(true);
		setAnalyticsError(null);
		try {
			const analytics = await fetchWeeklyFeedbackAnalytics(7, sessionIdRef.current);
			setWeeklyAnalytics(analytics);
		} catch {
			setAnalyticsError('Unable to load weekly analytics right now.');
		} finally {
			setAnalyticsLoading(false);
		}
	};

	useEffect(() => {
		if (showDiagnostics) {
			refreshWeeklyAnalytics();
		}
	}, [showDiagnostics]);




	// Async: Try to answer from docs, page context, live data, and then fallback to static.
	const getGolbyResponse = async (userMessage: string): Promise<{ text: string; category: ResponseCategory }> => {
		const lowerMessage = userMessage.toLowerCase();
		const guardrailCategory = detectGuardrailCategory(lowerMessage);
		if (guardrailCategory) {
			return {
				text: getGuardrailResponse(guardrailCategory),
				category: 'static',
			};
		}

		const locationMatch = userMessage.match(/(?:for|in)\s+([\w\s,]+)/i);
		const locationHint = locationMatch ? locationMatch[1].trim() : undefined;
		try {
			const backendReply = await fetchAssistantReply({
				message: userMessage,
				page_context: pageContext,
				user_id: currentUserId,
				location: locationHint,
			});
			setRuntimeDiagnostics(null);
			if (backendReply?.reply) {
				const mappedCategory: ResponseCategory = backendReply.category === 'live' ? 'live' : 'static';
				return {
					text: backendReply.reply,
					category: mappedCategory,
				};
			}
		} catch {
			setRuntimeDiagnostics('Live assistant service is unavailable. Golby is using local fallback responses.');
			// Fall back to local response logic when backend assistant is unavailable.
		}

		const topic = classifyTopic(lowerMessage);
		const orderedCategories = getOrderedCategories(topic, assistantProfile, feedbackCount);
		const preferredStyle = getResponseStyle(feedbackCount, styleBias);
		const withStyle = (text: string, category: ResponseCategory) => ({
			text: formatResponseForStyle(text, preferredStyle, category),
			category,
		});

		for (const category of orderedCategories) {
			if (category === 'docs') {
				if (userGuide && topic !== 'joke' && topic !== 'greeting') {
					const docAnswer = searchDocForAnswer(userGuide, userMessage);
					if (!docAnswer.startsWith('Sorry')) {
						return withStyle(docAnswer, 'docs');
					}
				}
				continue;
			}

			if (category === 'page') {
				if (pageContext === 'map' && lowerMessage.includes('risk')) {
					return withStyle("You're on the map view! Click any location to see detailed risk scores and environmental data for that area.", 'page');
				}
				if (pageContext === 'alerts' && lowerMessage.includes('alert')) {
					return withStyle("You're viewing alerts. Here you can see all current environmental alerts for your selected region. Want help setting up custom alerts?", 'page');
				}
				if (pageContext === 'dashboard') {
					return withStyle("This is your dashboard, where you can get a quick overview of your travel safety, recent alerts, and personalized recommendations.", 'page');
				}
				if (pageContext === 'profile') {
					return withStyle("You're on your profile page. Here you can update your information, preferences, and notification settings.", 'page');
				}
				if (pageContext === 'settings') {
					return withStyle("You're in settings. Adjust your preferences, manage alerts, and customize your RiskRadar experience here.", 'page');
				}
				if (pageContext === 'forecast' && lowerMessage.includes('forecast')) {
					return withStyle("You're on the forecast page. Enter a location or use your current location to get the latest environmental forecast.", 'page');
				}
				continue;
			}

			if (category === 'live') {
				try {
					if (lowerMessage.includes('current alert') || lowerMessage.includes('latest alert')) {
						const alerts = await fetchCurrentAlerts();
						if (alerts && alerts.length > 0) {
							return withStyle(`Here are the latest alerts:\n` + alerts.map((a: any) => `• ${a.title || a.alert_type || 'Alert'} (${a.severity || 'unknown'})`).join('\n'), 'live');
						}
						return withStyle('There are no current alerts.', 'live');
					}
					if (lowerMessage.includes('risk') && lowerMessage.includes('map')) {
						const risk = await fetchRiskOverlay();
						if (risk && risk.risk_zones && risk.risk_zones.length > 0) {
							const high = risk.risk_zones.filter((z: any) => z.risk_level === 'high').length;
							const mod = risk.risk_zones.filter((z: any) => z.risk_level === 'moderate').length;
							const low = risk.risk_zones.filter((z: any) => z.risk_level === 'low').length;
							return withStyle(`Current map risk overlay:\nHigh risk: ${high}, Moderate: ${mod}, Low: ${low}`, 'live');
						}
						return withStyle('No risk data available for the map.', 'live');
					}
					if (lowerMessage.includes('forecast')) {
						const match = userMessage.match(/forecast for ([\w\s,]+)/i);
						const location = match ? match[1].trim() : '';
						const forecast = await fetchForecast(location);
						if (forecast && forecast.risk_zones && forecast.risk_zones.length > 0) {
							const high = forecast.risk_zones.filter((z: any) => z.risk_level === 'high').length;
							const mod = forecast.risk_zones.filter((z: any) => z.risk_level === 'moderate').length;
							const low = forecast.risk_zones.filter((z: any) => z.risk_level === 'low').length;
							return withStyle(`Forecast for ${location || 'your area'}:\nHigh risk: ${high}, Moderate: ${mod}, Low: ${low}`, 'live');
						}
						return withStyle(`No forecast data available${location ? ' for ' + location : ''}.`, 'live');
					}
				} catch {
					return withStyle('Sorry, I had trouble fetching live data.', 'live');
				}
				continue;
			}

			if (category === 'playful') {
				if (topic === 'joke') {
					return withStyle(golbyJokes[Math.floor(Math.random() * golbyJokes.length)], 'playful');
				}
				if (topic === 'greeting') {
					return withStyle(golbyGreetings[Math.floor(Math.random() * golbyGreetings.length)], 'playful');
				}
				continue;
			}

			if (category === 'static') {
				if (lowerMessage.includes('help')) {
					return withStyle(golbyResponses['help'], 'static');
				}
				if (lowerMessage.includes('forecast') || lowerMessage.includes('weather')) {
					return withStyle("The forecast looks clear ahead! ☀️ I can pull up detailed environmental data for any location you're interested in. Which area would you like to check?", 'static');
				}
				if (lowerMessage.includes('alert')) {
					return withStyle("Setting up alerts is easy! Head to your settings, choose 'Notifications', and you can customize alerts for specific risk types or locations. Want me to guide you there?", 'static');
				}
				if (lowerMessage.includes('risk')) {
					return withStyle("I can show you comprehensive risk assessments including air quality, natural disasters, climate risks, and more. Just click on any location on the map, or tell me which area you're curious about!", 'static');
				}
				return withStyle(golbyResponses['default'], 'static');
			}
		}

		return withStyle(golbyResponses['default'], 'static');
	};

	const handleFeedback = async (message: Message, reaction: FeedbackReaction) => {
		const category = message.responseCategory ?? 'static';
		const nextProfile = applyFeedback(assistantProfile, category, reaction);
		const nextFeedbackCount = feedbackCount + 1;
		const nextStyleBias = updateStyleBias(styleBias, reaction, message.text);

		setAssistantProfile(nextProfile);
		persistProfile(nextProfile);
		setFeedbackCount(nextFeedbackCount);
		persistNumber(FEEDBACK_COUNT_STORAGE_KEY, nextFeedbackCount);
		setStyleBias(nextStyleBias);
		persistNumber(STYLE_BIAS_STORAGE_KEY, nextStyleBias);

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
			setRuntimeDiagnostics(null);
		} catch {
			setRuntimeDiagnostics('Feedback could not be synced right now. Local learning remains active.');
			// Keep the local learning loop working even if the backend call fails.
		}

		if (currentUserId) {
			try {
				await syncGolbyStyleProfile(currentUserId, nextProfile, nextFeedbackCount, nextStyleBias);
				setRuntimeDiagnostics(null);
			} catch {
				setRuntimeDiagnostics('Profile sync is delayed. Changes will apply locally for this session.');
				// Keep local learning responsive even if profile sync fails.
			}
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
		<div className={`golby-chat-root ${fullPage ? 'full-page' : 'widget-mode'}`}>
			{/* Header */}
			<div className="golby-chat-header">
				<GolbyIcon expression="happy" size="sm" />
				<div className="golby-chat-header-info">
					<h2 className="golby-chat-header-title">Chat with Golby</h2>
					<p className="golby-chat-header-subtitle">Your AI Travel Assistant</p>
				</div>
				{isAdmin && (
					<button
						onClick={() => setShowDiagnostics((current) => !current)}
						className="golby-header-btn"
						aria-label="Toggle diagnostics panel"
					>
						{showDiagnostics ? 'Hide Panels' : 'Show Panels'}
					</button>
				)}
				{onClose && (
					<button
						onClick={onClose}
						className="golby-header-close"
						aria-label={fullPage ? 'Back to welcome' : 'Close chat'}
					>
						{fullPage ? '←' : '×'}
					</button>
				)}
			</div>

			{/* Admin diagnostics */}
			{isAdmin && showDiagnostics && (
				<div className="golby-diagnostics">
					{runtimeDiagnostics && (
						<div className="golby-warning-banner" data-golby-runtime-diagnostic="true">
							{runtimeDiagnostics}
						</div>
					)}
					<div className="golby-diagnostics-card">
						<p className="golby-diagnostics-title">Local Learning Panel</p>
						<div className="golby-diagnostics-grid">
							<span>Session ID</span>
							<span style={{ fontFamily: 'monospace', fontSize: '11px', wordBreak: 'break-all' }}>{sessionIdRef.current}</span>
							<span>Current User ID</span>
							<span>{currentUserId ?? 'Anonymous'}</span>
							<span>Access</span>
							<span>{isAdmin ? 'Admin' : 'Standard user'}</span>
							<span>Feedback Count</span>
							<span>{feedbackCount}</span>
							<span>Style Bias</span>
							<span>{styleBias}</span>
							<span>Active Style</span>
							<span>{getResponseStyle(feedbackCount, styleBias)}</span>
							<span>Category Scores</span>
							<span>
								docs {assistantProfile.docs.toFixed(2)}, page {assistantProfile.page.toFixed(2)}, live {assistantProfile.live.toFixed(2)}, playful {assistantProfile.playful.toFixed(2)}, static {assistantProfile.static.toFixed(2)}
							</span>
						</div>
					</div>
					<div className="golby-diagnostics-card">
						<div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
							<p className="golby-diagnostics-title" style={{ margin: 0 }}>Backend Weekly Analytics Panel</p>
							<button
								onClick={refreshWeeklyAnalytics}
								style={{ fontSize: '0.75rem', color: 'var(--golby-accent)', background: 'none', border: 'none', cursor: 'pointer', textDecoration: 'underline', fontFamily: 'var(--golby-font-body)' }}
								aria-label="Refresh backend analytics"
							>
								Refresh
							</button>
						</div>
						{analyticsLoading && <p style={{ fontSize: '0.75rem', color: 'var(--golby-text-muted)', margin: 0 }}>Loading analytics...</p>}
						{analyticsError && <p style={{ fontSize: '0.75rem', color: 'oklch(0.52 0.18 25)', margin: 0 }}>{analyticsError}</p>}
						{weeklyAnalytics && !analyticsLoading && !analyticsError && (
							<div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
								<div className="golby-diagnostics-grid">
									<span>Window</span>
									<span>{weeklyAnalytics.from_date} to {weeklyAnalytics.to_date}</span>
									<span>Total Feedback</span>
									<span>{weeklyAnalytics.total_feedback}</span>
									<span>Average Rating</span>
									<span>{weeklyAnalytics.average_rating ?? 'N/A'}</span>
								</div>
								<div style={{ border: '1px solid var(--golby-border)', borderRadius: '6px', overflow: 'hidden' }}>
									<table style={{ width: '100%', fontSize: '0.75rem', borderCollapse: 'collapse' }}>
										<thead style={{ background: 'var(--golby-accent-subtle)' }}>
											<tr>
												<th style={{ textAlign: 'left', padding: '6px 10px', color: 'var(--golby-text)', fontWeight: 600 }}>Date</th>
												<th style={{ textAlign: 'left', padding: '6px 10px', color: 'var(--golby-text)', fontWeight: 600 }}>Count</th>
												<th style={{ textAlign: 'left', padding: '6px 10px', color: 'var(--golby-text)', fontWeight: 600 }}>Avg</th>
											</tr>
										</thead>
										<tbody>
											{weeklyAnalytics.by_day.map((day) => (
												<tr key={day.date} style={{ borderTop: '1px solid var(--golby-border-subtle)' }}>
													<td style={{ padding: '5px 10px', color: 'var(--golby-text-secondary)' }}>{day.date}</td>
													<td style={{ padding: '5px 10px', color: 'var(--golby-text-secondary)' }}>{day.count}</td>
													<td style={{ padding: '5px 10px', color: 'var(--golby-text-secondary)' }}>{day.average_rating ?? 'N/A'}</td>
												</tr>
											))}
										</tbody>
									</table>
								</div>
							</div>
						)}
					</div>
				</div>
			)}

			{/* Runtime warning (non-admin view) */}
			{runtimeDiagnostics && !showDiagnostics && (
				<div className="golby-warning-banner" data-golby-runtime-diagnostic="true">
					{runtimeDiagnostics}
				</div>
			)}

			{/* Messages */}
			<div className="golby-messages-area">
				{messages.map((message) => (
					<div
						key={message.id}
						style={{ display: 'flex', gap: '10px', justifyContent: message.isGolby ? 'flex-start' : 'flex-end' }}
					>
						{message.isGolby && (
							<div style={{ flexShrink: 0 }}>
								<GolbyIcon expression="happy" size="sm" />
							</div>
						)}
						<div style={{ display: 'flex', flexDirection: 'column', alignItems: message.isGolby ? 'flex-start' : 'flex-end' }}>
							<ChatBubble message={message.text} isGolby={message.isGolby} />
							{message.isGolby && (
								<div className="golby-feedback-row">
									<button
										className="golby-feedback-btn"
										onClick={() => handleFeedback(message, 'thumbs_up')}
										aria-label="This was helpful"
									>
										<ThumbsUp size={14} />
									</button>
									<button
										className="golby-feedback-btn"
										onClick={() => handleFeedback(message, 'thumbs_down')}
										aria-label="This wasn't helpful"
									>
										<ThumbsDown size={14} />
									</button>
									<button
										className="golby-feedback-btn"
										onClick={() => handleFeedback(message, 'smile')}
										aria-label="Rate with emoji"
									>
										<Smile size={14} />
									</button>
								</div>
							)}
						</div>
					</div>
				))}
				{isTyping && (
					<div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-start' }}>
						<div style={{ flexShrink: 0 }}>
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
					initial={{ opacity: 0, y: 8 }}
					animate={{ opacity: 1, y: 0 }}
					transition={{ duration: 0.25 }}
					className="golby-suggestions"
				>
					<span className="golby-suggestions-label">Quick suggestions</span>
					<div className="golby-suggestions-pills">
						{suggestions.map((suggestion, index) => (
							<motion.button
								key={index}
								initial={{ opacity: 0, scale: 0.92 }}
								animate={{ opacity: 1, scale: 1 }}
								transition={{ delay: index * 0.08, duration: 0.2 }}
								onClick={() => handleSuggestionClick(suggestion)}
								className="golby-suggestion-pill"
								whileHover={{ scale: 1.03 }}
								whileTap={{ scale: 0.97 }}
							>
								{suggestion}
							</motion.button>
						))}
					</div>
				</motion.div>
			)}

			{/* Input */}
			<div className="golby-input-area">
				<form
					onSubmit={(e) => {
						e.preventDefault();
						handleSendMessage(inputValue);
					}}
					className="golby-input-form"
				>
					<input
						type="text"
						value={inputValue}
						onChange={(e) => setInputValue(e.target.value)}
						placeholder="Ask Golby anything..."
						className="golby-input-field"
						aria-label="Message input"
					/>
					<button
						type="submit"
						disabled={!inputValue.trim()}
						className="golby-send-btn"
						aria-label="Send message"
					>
						<Send size={17} />
					</button>
				</form>
			</div>
		</div>
	);
}

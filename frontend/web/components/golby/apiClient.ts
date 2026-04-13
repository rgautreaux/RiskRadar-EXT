// Utility to fetch live data from backend APIs for Golby

export type GolbyFeedbackReaction = 'thumbs_up' | 'thumbs_down' | 'smile';

export interface GolbyFeedbackPayload {
  session_id: string;
  message_id: string;
  reaction: GolbyFeedbackReaction;
  rating: number;
  page_context?: string;
  response_category?: string;
  response_text?: string;
  comment?: string;
}

export interface GolbyLocalProfile {
  docs: number;
  page: number;
  live: number;
  playful: number;
  static: number;
}

export interface AssistantRequestPayload {
  message: string;
  page_context?: string;
  user_id?: number;
  location?: string;
}

declare global {
  interface Window {
    __RISKRADAR_API_BASE__?: string;
  }
}

const DEFAULT_API_BASE = '/api/v1';

function getApiBase(): string {
  if (typeof window === 'undefined') {
    return DEFAULT_API_BASE;
  }

  const configured = (window.__RISKRADAR_API_BASE__ || '').trim();
  if (!configured) {
    return DEFAULT_API_BASE;
  }

  return configured.endsWith('/') ? configured.slice(0, -1) : configured;
}

function buildApiUrl(path: string): string {
  const base = getApiBase();
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;

  if (/^https?:\/\//i.test(base)) {
    return `${base}${normalizedPath}`;
  }

  return `${base}${normalizedPath}`;
}

export interface AssistantResponsePayload {
  reply: string;
  category: 'guardrail' | 'live' | 'fallback';
  used_live_data: boolean;
  sources: string[];
}

export interface WeeklyAnalyticsPoint {
  date: string;
  count: number;
  average_rating: number | null;
}

export interface WeeklyAnalyticsPayload {
  window_days: number;
  from_date: string;
  to_date: string;
  total_feedback: number;
  average_rating: number | null;
  by_day: WeeklyAnalyticsPoint[];
}

export async function fetchCurrentAlerts() {
  const res = await fetch(`${buildApiUrl('/alerts')}?limit=5`, { credentials: 'include' });
  if (!res.ok) throw new Error('Failed to fetch alerts');
  return await res.json();
}

export async function fetchRiskOverlay() {
  const res = await fetch(buildApiUrl('/risk/map'), { credentials: 'include' });
  if (!res.ok) throw new Error('Failed to fetch risk overlay');
  return await res.json();
}

export async function fetchForecast(location = '') {
  const url = location
    ? `${buildApiUrl('/forecast')}?location=${encodeURIComponent(location)}`
    : buildApiUrl('/forecast');
  const res = await fetch(url, { credentials: 'include' });
  if (!res.ok) throw new Error('Failed to fetch forecast');
  return await res.json();
}

export async function fetchAssistantReply(payload: AssistantRequestPayload): Promise<AssistantResponsePayload> {
  const res = await fetch(buildApiUrl('/assistant/respond'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error('Failed to fetch assistant response');
  }

  return await res.json();
}

export async function sendGolbyFeedback(payload: GolbyFeedbackPayload) {
  const res = await fetch(buildApiUrl('/feedback'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error('Failed to send Golby feedback');
  }

  return await res.json();
}

export async function fetchCurrentUser() {
  const res = await fetch(buildApiUrl('/auth/me'), { credentials: 'include' });
  if (!res.ok) {
    throw new Error('Failed to fetch current user');
  }

  return await res.json();
}

export async function fetchWeeklyFeedbackAnalytics(days = 7, sessionId?: string): Promise<WeeklyAnalyticsPayload> {
  const params = new URLSearchParams({ days: String(days) });
  if (sessionId) {
    params.set('session_id', sessionId);
  }

  const res = await fetch(`${buildApiUrl('/feedback/analytics/weekly')}?${params.toString()}`, { credentials: 'include' });
  if (!res.ok) {
    throw new Error('Failed to fetch weekly feedback analytics');
  }

  return await res.json();
}

function clamp(value: number, min = 0, max = 1) {
  return Math.min(max, Math.max(min, value));
}

export async function syncGolbyStyleProfile(
  userId: number,
  profile: GolbyLocalProfile,
  feedbackCount: number,
  styleBias: number,
) {
  const warmth = clamp(0.55 + (profile.static + profile.page) * 0.02 + profile.playful * 0.01);
  const calmness = clamp(0.7 + profile.docs * 0.02 - profile.playful * 0.01);
  const humor = clamp(0.35 + profile.playful * 0.04);
  const conciseness = clamp(0.65 - styleBias * 0.04);
  const detail = clamp(0.45 + styleBias * 0.04);

  const assistantStyleProfile = {
    tone: {
      warmth: Number(warmth.toFixed(4)),
      calmness: Number(calmness.toFixed(4)),
      humor: Number(humor.toFixed(4)),
    },
    delivery: {
      conciseness: Number(conciseness.toFixed(4)),
      detail: Number(detail.toFixed(4)),
      expandability: Number(clamp(0.5 + feedbackCount * 0.01).toFixed(4)),
    },
    voice: {
      formality: Number(clamp(0.35 + profile.docs * 0.02 - profile.playful * 0.02).toFixed(4)),
    },
    learning: {
      feedback_count: feedbackCount,
      last_feedback_at: new Date().toISOString(),
    },
  };

  const res = await fetch(buildApiUrl(`/users/${userId}/preferences`), {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({
      assistant_style_profile: assistantStyleProfile,
    }),
  });

  if (!res.ok) {
    throw new Error('Failed to sync Golby style profile');
  }

  return await res.json();
}

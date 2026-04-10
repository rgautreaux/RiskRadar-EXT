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
  user_id?: number;
}

export interface AssistantRequestPayload {
  message: string;
  page_context?: string;
  user_id?: number;
  location?: string;
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
  const res = await fetch('/api/v1/alerts?limit=5');
  if (!res.ok) throw new Error('Failed to fetch alerts');
  return await res.json();
}

export async function fetchRiskOverlay() {
  const res = await fetch('/api/v1/risk/map');
  if (!res.ok) throw new Error('Failed to fetch risk overlay');
  return await res.json();
}

export async function fetchForecast(location = '') {
  const url = location ? `/api/v1/forecast?location=${encodeURIComponent(location)}` : '/api/v1/forecast';
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch forecast');
  return await res.json();
}

export async function fetchAssistantReply(payload: AssistantRequestPayload): Promise<AssistantResponsePayload> {
  const res = await fetch('/api/v1/assistant/respond', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error('Failed to fetch assistant response');
  }

  return await res.json();
}

export async function sendGolbyFeedback(payload: GolbyFeedbackPayload) {
  const res = await fetch('/api/v1/feedback', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error('Failed to send Golby feedback');
  }

  return await res.json();
}

export async function fetchWeeklyFeedbackAnalytics(days = 7, sessionId?: string, adminUserId?: number): Promise<WeeklyAnalyticsPayload> {
  const params = new URLSearchParams({ days: String(days) });
  if (sessionId) {
    params.set('session_id', sessionId);
  }
  if (adminUserId !== undefined) {
    params.set('admin_user_id', String(adminUserId));
  }

  const res = await fetch(`/api/v1/feedback/analytics/weekly?${params.toString()}`);
  if (!res.ok) {
    throw new Error('Failed to fetch weekly feedback analytics');
  }

  return await res.json();
}

export type RiskScoreResponse = {
  user_id: number;
  score: number;
  level: 'low' | 'medium' | 'high';
  base_score: number;
  multiplier: number;
};

export type PrioritizedAlert = {
  id: number;
  title: string;
  severity: string;
  alert_type: string;
  location_name?: string | null;
  priority_score?: number;
  urgency_label?: 'low' | 'medium' | 'high';
};

const DEFAULT_API_BASE = 'http://127.0.0.1:8000';
const API_PREFIX = '/api/v1';

function buildUrl(path: string, query?: Record<string, string | number | undefined>): string {
  const url = new URL(`${DEFAULT_API_BASE}${API_PREFIX}/${path.replace(/^\/+/, '')}`);
  if (query) {
    Object.entries(query).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        url.searchParams.set(key, String(value));
      }
    });
  }
  return url.toString();
}

async function safeJson<T>(response: Response, fallback: T): Promise<T> {
  try {
    return (await response.json()) as T;
  } catch {
    return fallback;
  }
}

export async function fetchRiskScore(userId: number): Promise<RiskScoreResponse | null> {
  const response = await fetch(buildUrl(`users/${userId}/risk-score`));
  if (!response.ok) {
    return null;
  }
  return safeJson<RiskScoreResponse | null>(response, null);
}

export async function fetchPrioritizedAlerts(userId: number, limit = 10): Promise<PrioritizedAlert[]> {
  const response = await fetch(buildUrl('alerts/prioritized', { user_id: userId, limit }));
  if (!response.ok) {
    return [];
  }
  return safeJson<PrioritizedAlert[]>(response, []);
}

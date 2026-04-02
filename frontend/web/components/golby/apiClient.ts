// Utility to fetch live data from backend APIs for Golby

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

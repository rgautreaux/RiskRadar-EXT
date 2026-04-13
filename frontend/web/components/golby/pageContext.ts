// Utility to detect the current page/view for context-aware Golby answers
// Looks for body class, data attribute, or URL path

export function detectCurrentPage(): string {
  // 1. Check for a body data attribute (preferred)
  const body = document.body;
  if (body.dataset && body.dataset.page) {
    return body.dataset.page;
  }
  // 2. Check for a body class like 'page-map', 'page-alerts', etc.
  const pageClass = Array.from(body.classList).find(cls => cls.startsWith('page-'));
  if (pageClass) {
    return pageClass.replace('page-', '');
  }
  // 3. Fallback: use the URL path
  const path = window.location.pathname;
  if (path.includes('map')) return 'map';
  if (path.includes('alerts')) return 'alerts';
  if (path.includes('dashboard')) return 'dashboard';
  if (path.includes('profile')) return 'profile';
  if (path.includes('settings')) return 'settings';
  if (path.includes('forecast')) return 'forecast';
  if (path.includes('assistant')) return 'assistant';
  return 'unknown';
}

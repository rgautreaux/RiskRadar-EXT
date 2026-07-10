(function () {
  const context = window.__RISKRADAR_CLIENT_CONTEXT__ || {};
  const page = String(context.page || 'unknown');
  const accessContext = String(context.accessContext || 'anonymous');

  const API_BASE = String(window.__RISKRADAR_API_BASE__ || '').replace(/\/$/, '');
  const API_PREFIX = String(window.__RISKRADAR_API_PREFIX__ || '/api/v1').replace(/\/$/, '');
  const FEEDBACK_ENDPOINT = `${API_BASE}${API_PREFIX}/feedback`;

  function storageGet(key, fallback) {
    try {
      const raw = window.localStorage.getItem(key);
      return raw == null ? fallback : JSON.parse(raw);
    } catch {
      return fallback;
    }
  }

  function storageSet(key, value) {
    try {
      window.localStorage.setItem(key, JSON.stringify(value));
    } catch {
      // Ignore storage errors.
    }
  }

  function registerServiceWorker() {
    if (!('serviceWorker' in navigator)) return;
    navigator.serviceWorker.register('/sw.js').catch(() => {
      // Ignore SW registration failure.
    });
  }

  function installOfflineBanner() {
    const banner = document.createElement('div');
    banner.className = 'rr-offline-banner';
    banner.setAttribute('role', 'status');
    banner.setAttribute('aria-live', 'polite');
    banner.textContent = 'Offline mode active. Cached data is shown where available.';
    document.body.appendChild(banner);

    function sync() {
      banner.classList.toggle('is-visible', !navigator.onLine);
    }

    window.addEventListener('online', sync);
    window.addEventListener('offline', sync);
    sync();
  }

  function installFirstRunTip() {
    const key = `rr-first-run-tip-dismissed:${page}`;
    if (storageGet(key, false)) return;

    const tips = {
      dashboard: 'Start here for alert volume and summary context, then open Alerts for details.',
      alerts: 'Use filters first, then open details in a new tab so you can compare risks quickly.',
      map: 'Use layer toggles and the Help button for keyboard shortcuts and overlay tips.',
      forecast: 'Switch timezone display at the top-right to compare forecast timing while traveling.',
      assistant: 'Ask Golby to compare locations, then save your preferred trip rules in Travel.',
      travel: 'Add multiple trip stops and set per-trip delivery channels before you leave.'
    };

    if (!tips[page]) return;

    const box = document.createElement('section');
    box.className = 'rr-first-run-tip';
    box.setAttribute('aria-label', 'First-run tip');
    box.innerHTML = `
      <h2>Quick tip for this page</h2>
      <p>${tips[page]}</p>
      <div class="rr-first-run-tip-actions">
        <button type="button" class="rr-tip-primary" data-rr-open-help>Open guided help</button>
        <button type="button" data-rr-dismiss-tip>Dismiss</button>
      </div>
    `;

    box.querySelector('[data-rr-open-help]').addEventListener('click', () => {
      if (typeof window.openGolbyOnboarding === 'function') {
        window.openGolbyOnboarding();
      } else {
        window.dispatchEvent(new Event('golby:show-onboarding'));
      }
    });

    box.querySelector('[data-rr-dismiss-tip]').addEventListener('click', () => {
      storageSet(key, true);
      box.remove();
    });

    document.body.appendChild(box);
  }

  function installFeedbackPanel() {
    if (page === 'login' || page === 'register') return;

    const launcher = document.createElement('button');
    launcher.type = 'button';
    launcher.className = 'rr-feedback-launcher';
    launcher.setAttribute('aria-label', 'Open feedback panel');
    launcher.textContent = 'Feedback';

    const panel = document.createElement('aside');
    panel.className = 'rr-feedback-panel';
    panel.setAttribute('aria-label', 'Feedback panel');
    panel.innerHTML = `
      <h2>How was this page?</h2>
      <div class="rr-feedback-reactions">
        <button type="button" data-reaction="thumbs_up">Helpful</button>
        <button type="button" data-reaction="smile">Clear</button>
        <button type="button" data-reaction="thumbs_down">Needs work</button>
      </div>
      <textarea id="rr-feedback-comment" maxlength="280" placeholder="Optional comment (up to 280 chars)"></textarea>
      <div class="rr-feedback-actions">
        <button type="button" data-close>Close</button>
        <button type="button" class="rr-send" data-send>Send</button>
      </div>
    `;

    let reaction = 'smile';

    panel.querySelectorAll('[data-reaction]').forEach((btn) => {
      btn.addEventListener('click', () => {
        reaction = btn.getAttribute('data-reaction') || 'smile';
      });
    });

    panel.querySelector('[data-close]').addEventListener('click', () => {
      panel.classList.remove('is-open');
    });

    panel.querySelector('[data-send]').addEventListener('click', async () => {
      const comment = String(panel.querySelector('#rr-feedback-comment').value || '').trim();
      const now = Date.now();
      const payload = {
        session_id: `web-${accessContext}`,
        message_id: `ux-${page}-${now}`,
        reaction,
        rating: reaction === 'thumbs_up' ? 5 : reaction === 'thumbs_down' ? 2 : 4,
        page_context: page,
        response_category: 'web_ux',
        response_text: `${page} feedback`,
        comment
      };

      try {
        await fetch(FEEDBACK_ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(payload)
        });
      } catch {
        // Keep local analytics even if backend feedback fails.
      }

      const metrics = storageGet('rr-web-analytics', { pages: {}, feedback: 0 });
      metrics.feedback = Number(metrics.feedback || 0) + 1;
      storageSet('rr-web-analytics', metrics);

      panel.classList.remove('is-open');
    });

    launcher.addEventListener('click', () => {
      panel.classList.toggle('is-open');
    });

    document.body.appendChild(launcher);
    document.body.appendChild(panel);
  }

  function trackUsage() {
    const metrics = storageGet('rr-web-analytics', { pages: {}, feedback: 0 });
    metrics.pages[page] = Number(metrics.pages[page] || 0) + 1;
    storageSet('rr-web-analytics', metrics);
  }

  function installI18nScaffold() {
    const translations = {
      en: {
        language: 'Language',
        timezone: 'Timezone'
      },
      es: {
        language: 'Idioma',
        timezone: 'Zona horaria'
      }
    };

    const languageSelect = document.getElementById('rr-language');
    const timezoneSelect = document.getElementById('rr-timezone');
    if (!languageSelect || !timezoneSelect) return;

    const storedLanguage = storageGet('rr-language', 'en');
    const storedTimezone = storageGet('rr-timezone', 'local');

    languageSelect.value = storedLanguage;
    timezoneSelect.value = storedTimezone;

    function applyLanguage(lang) {
      const dict = translations[lang] || translations.en;
      document.documentElement.setAttribute('lang', lang);
      document.querySelectorAll('label[for="rr-language"]').forEach((el) => {
        el.textContent = dict.language;
      });
      document.querySelectorAll('label[for="rr-timezone"]').forEach((el) => {
        el.textContent = dict.timezone;
      });
    }

    function applyTimezone(mode) {
      const zone = mode === 'UTC' ? 'UTC' : Intl.DateTimeFormat().resolvedOptions().timeZone;
      document.querySelectorAll('[data-rr-utc]').forEach((el) => {
        const raw = String(el.getAttribute('data-rr-utc') || '');
        const date = new Date(raw);
        if (Number.isNaN(date.getTime())) return;
        const formatter = new Intl.DateTimeFormat(languageSelect.value || 'en', {
          dateStyle: 'medium',
          timeStyle: 'short',
          timeZone: zone
        });
        el.textContent = formatter.format(date);
      });
    }

    languageSelect.addEventListener('change', () => {
      storageSet('rr-language', languageSelect.value);
      applyLanguage(languageSelect.value);
      applyTimezone(timezoneSelect.value);
    });

    timezoneSelect.addEventListener('change', () => {
      storageSet('rr-timezone', timezoneSelect.value);
      applyTimezone(timezoneSelect.value);
    });

    applyLanguage(storedLanguage);
    applyTimezone(storedTimezone);
  }

  registerServiceWorker();
  installOfflineBanner();
  installFirstRunTip();
  installFeedbackPanel();
  trackUsage();
  installI18nScaffold();
})();

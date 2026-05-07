<?php rr_render_layout_start('Travel Alerts', 'travel'); ?>

<section class="panel" style="display:grid;gap:16px;">
  <div class="panel-header">
    <div>
      <p class="eyebrow">Travel mode</p>
      <h1>Trips and saved locations</h1>
    </div>
  </div>
  <p>Build trip-specific alert rules, batch-monitor multiple locations, and choose how high-priority alerts are delivered while traveling.</p>
</section>

<section class="panel" style="display:grid;gap:14px;">
  <h2 style="margin:0;">Create a trip rule</h2>
  <form id="travel-rule-form" style="display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));align-items:end;">
    <label>
      <span>Trip name</span>
      <input type="text" id="trip-name" required maxlength="60" placeholder="Spring Gulf Route">
    </label>
    <label>
      <span>Locations (comma-separated)</span>
      <input type="text" id="trip-locations" required placeholder="Baton Rouge, Houston, Gulfport">
    </label>
    <label>
      <span>Start date</span>
      <input type="date" id="trip-start" required>
    </label>
    <label>
      <span>End date</span>
      <input type="date" id="trip-end" required>
    </label>
    <label>
      <span>Minimum severity</span>
      <select id="trip-severity">
        <option value="low">Low</option>
        <option value="medium" selected>Medium</option>
        <option value="high">High</option>
      </select>
    </label>
    <fieldset style="border:1px solid var(--line,#ddd);border-radius:10px;padding:8px 10px;">
      <legend>Delivery options (opt-in)</legend>
      <label><input type="checkbox" id="delivery-push"> Push</label>
      <label><input type="checkbox" id="delivery-email"> Email</label>
      <label><input type="checkbox" id="delivery-sms"> SMS</label>
    </fieldset>
    <button type="submit" class="button-primary">Save trip rule</button>
  </form>
</section>

<section class="panel" style="display:grid;gap:10px;">
  <div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;">
    <h2 style="margin:0;">Saved trip rules</h2>
    <button id="refresh-trip-risks" type="button" class="button-secondary">Check latest risk by trip</button>
  </div>
  <p class="muted" style="margin:0;">This view is designed for fast travel planning and batch-location monitoring.</p>
  <div id="trip-empty" class="muted">No trip rules saved yet.</div>
  <ul id="trip-list" style="list-style:none;padding:0;margin:0;display:grid;gap:10px;"></ul>
</section>

<script>
(function () {
  const STORAGE_KEY = 'riskradar-travel-rules-v1';
  const form = document.getElementById('travel-rule-form');
  const list = document.getElementById('trip-list');
  const empty = document.getElementById('trip-empty');
  const refresh = document.getElementById('refresh-trip-risks');

  function readRules() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    } catch {
      return [];
    }
  }

  function writeRules(next) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
  }

  function deliveryLabel(rule) {
    const channels = [];
    if (rule.delivery && rule.delivery.push) channels.push('push');
    if (rule.delivery && rule.delivery.email) channels.push('email');
    if (rule.delivery && rule.delivery.sms) channels.push('sms');
    return channels.length ? channels.join(', ') : 'none';
  }

  function renderRules() {
    const rules = readRules();
    list.innerHTML = '';
    empty.style.display = rules.length ? 'none' : 'block';

    rules.forEach((rule, index) => {
      const item = document.createElement('li');
      item.className = 'card';
      item.style.marginBottom = '0';
      item.innerHTML = `
        <div style="display:flex;justify-content:space-between;gap:10px;align-items:flex-start;flex-wrap:wrap;">
          <div>
            <h3 style="margin:0 0 6px;">${rule.name}</h3>
            <p style="margin:0 0 6px;">Locations: ${rule.locations.join(', ')}</p>
            <p style="margin:0 0 6px;">Window: <span data-rr-utc="${rule.start}T00:00:00Z">${rule.start}</span> to <span data-rr-utc="${rule.end}T00:00:00Z">${rule.end}</span></p>
            <p style="margin:0;">Severity >= ${rule.severity}; delivery: ${deliveryLabel(rule)}</p>
            <p style="margin:6px 0 0;" class="muted" id="trip-risk-${index}">Risk check pending.</p>
          </div>
          <button type="button" class="button-secondary" data-delete="${index}">Delete</button>
        </div>
      `;
      list.appendChild(item);
    });

    list.querySelectorAll('[data-delete]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const idx = Number(btn.getAttribute('data-delete'));
        const rules = readRules();
        rules.splice(idx, 1);
        writeRules(rules);
        renderRules();
      });
    });
  }

  async function checkTripRisks() {
    const base = String(window.__RISKRADAR_API_BASE__ || '').replace(/\/$/, '');
    const prefix = String(window.__RISKRADAR_API_PREFIX__ || '/api/v1').replace(/\/$/, '');
    const alertsUrl = `${base}${prefix}/alerts?limit=100`;

    let alerts = [];
    try {
      const response = await fetch(alertsUrl, { credentials: 'include' });
      const payload = response.ok ? await response.json() : null;
      alerts = Array.isArray(payload) ? payload : Array.isArray(payload && payload.alerts) ? payload.alerts : [];
    } catch {
      alerts = [];
    }

    readRules().forEach((rule, index) => {
      const destinationCount = rule.locations.length;
      const severityMatches = alerts.filter((alert) => {
        const severity = String(alert.severity || '').toLowerCase();
        if (rule.severity === 'high') return severity === 'high' || severity === 'severe' || severity === 'extreme';
        if (rule.severity === 'medium') return severity === 'medium' || severity === 'moderate' || severity === 'high' || severity === 'severe' || severity === 'extreme';
        return true;
      });

      const matched = severityMatches.filter((alert) => {
        const haystack = `${alert.location_name || ''} ${alert.region || ''}`.toLowerCase();
        return rule.locations.some((loc) => haystack.includes(loc.toLowerCase()));
      });

      const label = document.getElementById(`trip-risk-${index}`);
      if (label) {
        label.textContent = matched.length
          ? `${matched.length} matching high-priority alerts across ${destinationCount} saved locations.`
          : `No matching alerts for current rules across ${destinationCount} saved locations.`;
      }
    });
  }

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const rule = {
      name: document.getElementById('trip-name').value.trim(),
      locations: document.getElementById('trip-locations').value.split(',').map((x) => x.trim()).filter(Boolean),
      start: document.getElementById('trip-start').value,
      end: document.getElementById('trip-end').value,
      severity: document.getElementById('trip-severity').value,
      delivery: {
        push: document.getElementById('delivery-push').checked,
        email: document.getElementById('delivery-email').checked,
        sms: document.getElementById('delivery-sms').checked
      }
    };

    if (!rule.name || !rule.locations.length || !rule.start || !rule.end) {
      return;
    }

    const rules = readRules();
    rules.push(rule);
    writeRules(rules);
    form.reset();
    renderRules();
  });

  refresh.addEventListener('click', () => {
    checkTripRisks();
  });

  renderRules();
})();
</script>

<?php rr_render_layout_end(); ?>

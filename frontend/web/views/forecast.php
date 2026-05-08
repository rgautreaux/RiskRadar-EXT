<?php $forecastApiBase = rtrim((string) ($config['api']['base_url'] ?? ''), '/'); ?>
<?php $forecastApiPrefix = '/' . trim((string) ($config['api']['prefix'] ?? '/api/v1'), '/'); ?>

<link rel="stylesheet" href="/assets/app.css">
<link rel="stylesheet" href="/assets/theme.css">

<script>
window.__RISKRADAR_FORECAST_API_BASE__ = <?php echo json_encode($forecastApiBase); ?>;
window.__RISKRADAR_FORECAST_API_PREFIX__ = <?php echo json_encode($forecastApiPrefix); ?>;
</script>
<script src="/assets/forecast-location.js"></script>
<?php rr_render_layout_start('Forecast', 'forecast'); ?>

<style>
/* =============================================================
   Forecast page — fc- namespace
   ============================================================= */

.fc-hero { margin-bottom: 40px; }

.fc-eyebrow {
    font-family: 'Geist Mono', 'Courier New', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: oklch(0.52 0.14 150);
    margin: 0 0 8px;
}

.fc-headline {
    font-family: 'Bricolage Grotesque', system-ui, sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--ink, #122231);
    margin: 0 0 10px;
    line-height: 1.15;
    letter-spacing: -0.025em;
}

.fc-sub {
    font-size: 1rem;
    color: var(--muted, #33485d);
    margin: 0;
    max-width: 54ch;
    line-height: 1.6;
}

/* --- Search --- */

.fc-search-wrap { margin-bottom: 40px; }

.fc-search-form {
    display: flex;
    gap: 8px;
    align-items: stretch;
    max-width: 680px;
}

.fc-input-group {
    flex: 1;
    position: relative;
    min-width: 0;
}

.fc-search-input {
    width: 100%;
    padding: 12px 16px 12px 44px;
    border: 1.5px solid var(--line, rgba(18, 34, 49, 0.24));
    border-radius: 10px;
    background: var(--panel-strong, #fff5e6);
    font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', system-ui, sans-serif;
    font-size: 1rem;
    color: var(--ink, #122231);
    transition: border-color 0.18s, box-shadow 0.18s;
    box-sizing: border-box;
}

.fc-search-input::placeholder {
    color: var(--muted, #33485d);
    opacity: 0.5;
}

.fc-search-input:focus {
    outline: none;
    border-color: oklch(0.52 0.14 150);
    box-shadow: 0 0 0 3px oklch(0.52 0.14 150 / 0.14);
}

.fc-search-icon {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--muted, #33485d);
    opacity: 0.38;
    pointer-events: none;
}

.fc-btn {
    padding: 12px 20px;
    border-radius: 10px;
    font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', system-ui, sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: background 0.14s, box-shadow 0.14s, transform 0.1s;
    white-space: nowrap;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.fc-btn:active { transform: translateY(1px); }

.fc-btn-primary {
    background: oklch(0.52 0.14 150);
    color: #fff;
}

.fc-btn-primary:hover {
    background: oklch(0.47 0.14 150);
    box-shadow: 0 3px 14px oklch(0.52 0.14 150 / 0.3);
}

.fc-btn-ghost {
    background: var(--panel-strong, #fff5e6);
    color: var(--ink, #122231);
    border: 1.5px solid var(--line, rgba(18, 34, 49, 0.24));
}

.fc-btn-ghost:hover {
    background: oklch(0.96 0.01 150);
    border-color: oklch(0.52 0.14 150 / 0.45);
}

/* --- Status line --- */

.fc-status {
    margin: 10px 0 0;
    font-size: 0.875rem;
    color: var(--muted, #33485d);
    min-height: 1.3em;
    line-height: 1.55;
}

.fc-status-badge {
    display: inline-block;
    font-family: 'Geist Mono', monospace;
    font-size: 0.67rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    background: oklch(0.52 0.14 150 / 0.12);
    color: oklch(0.38 0.11 150);
    padding: 2px 7px;
    border-radius: 4px;
    margin-right: 6px;
    vertical-align: middle;
}

.fc-status-time {
    color: var(--muted, #33485d);
    opacity: 0.52;
    font-size: 0.8rem;
    margin-left: 6px;
}

/* --- Stat strip --- */

.fc-stat-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    background: var(--panel-strong, #fff5e6);
    border: 1px solid oklch(0.88 0.02 150);
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 20px;
}

.fc-stat-cell {
    padding: 16px 20px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.fc-stat-cell + .fc-stat-cell {
    border-left: 1px solid oklch(0.88 0.02 150);
}

.fc-stat-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.66rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted, #33485d);
    margin: 0;
    opacity: 0.68;
}

.fc-stat-value {
    font-family: 'Bricolage Grotesque', system-ui, sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: var(--ink, #122231);
    margin: 0;
    line-height: 1.1;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.01em;
}

/* --- Chart section --- */

.fc-chart-section {
    background: var(--panel-strong, #fff5e6);
    border: 1px solid oklch(0.88 0.02 150);
    border-radius: 14px;
    padding: 22px 22px 14px;
    margin-bottom: 20px;
}

.fc-section-label {
    font-family: 'Geist Mono', monospace;
    font-size: 0.67rem;
    font-weight: 500;
    color: var(--muted, #33485d);
    margin: 0 0 14px;
    text-transform: uppercase;
    letter-spacing: 0.11em;
    opacity: 0.62;
}

.fc-chart-legend {
    display: flex;
    gap: 18px;
    margin-top: 10px;
    font-size: 0.77rem;
    color: var(--muted, #33485d);
    opacity: 0.72;
}

.fc-legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
}

.fc-legend-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

/* --- Point list --- */

.fc-points-section { margin-bottom: 20px; }

.fc-point-list {
    list-style: none;
    padding: 0;
    margin: 8px 0 0;
    background: var(--panel-strong, #fff5e6);
    border: 1px solid oklch(0.88 0.02 150);
    border-radius: 12px;
    overflow: hidden;
}

.fc-point-item {
    display: grid;
    grid-template-columns: 52px 1fr auto auto;
    align-items: center;
    gap: 12px;
    padding: 11px 18px;
}

.fc-point-item + .fc-point-item {
    border-top: 1px solid oklch(0.91 0.01 150);
}

.fc-point-hour {
    font-family: 'Geist Mono', monospace;
    font-size: 0.76rem;
    color: var(--muted, #33485d);
    font-variant-numeric: tabular-nums;
    opacity: 0.62;
}

.fc-point-type {
    font-size: 0.875rem;
    color: var(--ink, #122231);
    text-transform: capitalize;
}

.fc-point-score {
    font-family: 'Geist Mono', monospace;
    font-size: 0.79rem;
    font-variant-numeric: tabular-nums;
    color: var(--muted, #33485d);
    opacity: 0.62;
}

/* --- Locked overlay for guests --- */
.forecast-locked { pointer-events: none; opacity: 0.5; }

.fc-risk-badge {
    font-family: 'Geist Mono', monospace;
    font-size: 0.66rem;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.fc-risk-high     { background: rgba(180, 55, 34, 0.13); color: #5a1b10; }
.fc-risk-moderate { background: rgba(142, 82, 0, 0.14);  color: #4a2b00; }
.fc-risk-low      { background: rgba(61, 120, 82, 0.13); color: #1f5235; }

/* --- Zone fallback --- */

.fc-zone-section {
    background: var(--panel-strong, #fff5e6);
    border: 1px solid oklch(0.88 0.02 150);
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 20px;
}

.fc-zone-desc {
    font-size: 0.875rem;
    color: var(--muted, #33485d);
    margin: 0 0 12px;
    line-height: 1.5;
}

.fc-zone-pills {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.fc-zone-pill {
    font-family: 'Geist Mono', monospace;
    font-size: 0.78rem;
    padding: 5px 12px;
    border-radius: 6px;
    font-variant-numeric: tabular-nums;
}

/* --- Empty state --- */

.fc-empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 60px 24px;
    text-align: center;
}

.fc-empty-icon {
    width: 52px;
    height: 52px;
    background: oklch(0.52 0.14 150 / 0.1);
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
    color: oklch(0.52 0.14 150);
}

.fc-empty-title {
    font-family: 'Bricolage Grotesque', system-ui, sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--ink, #122231);
    margin: 0 0 6px;
}

.fc-empty-body {
    font-size: 0.875rem;
    color: var(--muted, #33485d);
    max-width: 38ch;
    margin: 0;
    line-height: 1.55;
    opacity: 0.72;
}

/* --- Entrance animation --- */

@keyframes fc-rise {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0);   }
}

.fc-stat-strip    { animation: fc-rise 0.26s ease-out both; }
.fc-chart-section { animation: fc-rise 0.26s ease-out 0.04s both; }
.fc-points-section,
.fc-zone-section  { animation: fc-rise 0.26s ease-out 0.08s both; }

/* --- Responsive --- */

@media (max-width: 640px) {
    .fc-headline { font-size: 1.7rem; }

    .fc-search-form { flex-wrap: wrap; }
    .fc-btn-ghost .fc-btn-text { display: none; }

    .fc-stat-strip { grid-template-columns: repeat(2, 1fr); }
    .fc-stat-cell:nth-child(3) {
        border-left: none;
        border-top: 1px solid oklch(0.88 0.02 150);
    }
    .fc-stat-cell:nth-child(4) {
        border-top: 1px solid oklch(0.88 0.02 150);
    }

    .fc-point-item { grid-template-columns: 44px 1fr auto; }
    .fc-point-score { display: none; }
}

@media (prefers-reduced-motion: reduce) {
    .fc-stat-strip,
    .fc-chart-section,
    .fc-points-section,
    .fc-zone-section  { animation: none; }
    .fc-btn,
    .fc-search-input  { transition: none; }
}
</style>

<?php $isGuest = (function_exists('rr_access_context') && rr_access_context() === 'guest'); ?>

<?php if ($isGuest) : ?>
    <div class="locked-overlay" role="dialog" aria-modal="true" aria-labelledby="forecast-lockout-title">
        <div class="locked-modal-panel">
            <div class="locked-modal-header">
                <svg class="locked-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" width="32" height="32" aria-hidden="true">
                    <rect x="3" y="11" width="18" height="10" rx="1" stroke="currentColor" stroke-width="1.5"/><path d="M7 11V8a5 5 0 0 1 10 0v3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                <h2 id="forecast-lockout-title" class="locked-modal-title">48-Hour Forecast for Registered Users</h2>
            </div>
            <p class="locked-modal-body">
                Get data-driven risk forecasts tailored to your location. Our predictive models analyze environmental trends 24-48 hours ahead to help you stay informed.
            </p>
            <ul class="locked-modal-benefits" aria-label="Forecast benefits">
                <li>Personalized 48-hour risk projections</li>
                <li>Per-condition breakdowns (air, fire, pollen, etc.)</li>
                <li>Trend direction and confidence levels</li>
                <li>Integrated with your location and health profile</li>
            </ul>
            <div class="locked-modal-actions">
                <a href="/login.php" class="button-primary" role="button">Sign In</a>
                <a href="/register.php" class="button-secondary" role="button">Create Account</a>
            </div>
        </div>
    </div>
<?php endif; ?>

<section class="fc-hero<?php echo $isGuest ? ' forecast-locked' : ''; ?>">
    <p class="fc-eyebrow">24–48 Hour Outlook</p>
    <h1 class="fc-headline">Predictive Risk Forecast</h1>
    <p class="fc-sub">Enter a location to see environmental risk projections for the next 48 hours — trend direction, confidence levels, and per-condition breakdowns.</p>
</section>

<section class="fc-search-wrap<?php echo $isGuest ? ' forecast-locked' : ''; ?>">
    <form id="forecast-location-form" class="fc-search-form">
        <div class="fc-input-group">
            <svg class="fc-search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="11" cy="11" r="8"/>
                <line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input
                id="forecast-location-input"
                class="fc-search-input"
                type="text"
                placeholder="ZIP code or City, State"
                autocomplete="off"
                aria-label="Location search"
            />
        </div>
        <button type="submit" class="fc-btn fc-btn-primary">Get Forecast</button>
        <button type="button" id="use-my-location-btn" class="fc-btn fc-btn-ghost" title="Use device location">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/>
            </svg>
            <span class="fc-btn-text">Use my location</span>
        </button>
    </form>
    <p id="forecast-location-status" class="fc-status" aria-live="polite"></p>
</section>

<div id="forecast-results" aria-live="polite">
    <div class="fc-empty-state">
        <div class="fc-empty-icon" aria-hidden="true">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>
            </svg>
        </div>
        <p class="fc-empty-title">Locating your forecast</p>
        <p class="fc-empty-body">Allow location access, or enter a ZIP code or city above to load your 48-hour risk outlook.</p>
    </div>
</div>

<?php rr_render_layout_end(); ?>

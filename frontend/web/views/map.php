<?php
if (!isset($config) || !is_array($config)) {
    $config = require __DIR__ . '/../config/app.php';
}
require_once __DIR__ . '/../services/api_client.php';
$alerts_url = rr_api_url($config, 'alerts/map');
$risk_url   = rr_api_url($config, 'risk/map');
rr_render_layout_start('Risk Map', 'map');
?>

<style>
/* ═══════════════════════════════════════════
   Risk Map — Page-scoped Design Extension
   Forest green accent replaces coral.
   ═══════════════════════════════════════════ */
:root {
  --map-green:         oklch(0.55 0.145 150);
  --map-green-hover:   oklch(0.50 0.145 150);
  --map-green-tint:    oklch(0.96 0.025 150);
  --map-green-text:    oklch(0.34 0.10 150);
  --map-purple:        oklch(0.42 0.12 285);
  --map-purple-hover:  oklch(0.37 0.12 285);
  --map-purple-tint:   oklch(0.95 0.022 285);
  --ease-out-expo:     cubic-bezier(0.16, 1, 0.3, 1);
}

/* ── Controls Panel ──────────────────────── */
.map-controls-panel {
  background: linear-gradient(180deg,
    var(--panel-strong, #fffaf2),
    var(--panel, rgba(255,246,234,0.92)));
  border: 1px solid var(--line, rgba(18,34,49,0.18));
  border-radius: 20px;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 2px 12px rgba(18,34,49,0.05);
}

.map-controls-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.controls-label {
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.09em;
  text-transform: uppercase;
  color: var(--muted, #33485d);
  flex-shrink: 0;
  line-height: 1;
}

.region-filter-group {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

/* ── Region Pills ────────────────────────── */
.region-pills {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.region-pill {
  padding: 5px 14px;
  min-height: 32px;
  border-radius: 999px;
  border: 1.5px solid var(--line, rgba(18,34,49,0.18));
  background: transparent;
  color: var(--ink, #122231);
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  line-height: 1;
  transition:
    background 0.12s var(--ease-out-expo),
    border-color 0.12s var(--ease-out-expo),
    color 0.12s var(--ease-out-expo);
}

.region-pill:hover {
  background: var(--map-green-tint);
  border-color: oklch(0.55 0.145 150 / 0.45);
  color: var(--map-green-text);
}

.region-pill.active,
.region-pill[aria-pressed="true"] {
  background: var(--map-green);
  border-color: var(--map-green);
  color: oklch(0.98 0.006 150);
}

.region-pill:focus-visible {
  outline: 2px solid var(--map-green);
  outline-offset: 2px;
}

/* ── Help Button ─────────────────────────── */
.map-help-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 14px;
  min-height: 32px;
  border-radius: 8px;
  border: 1.5px solid var(--line, rgba(18,34,49,0.18));
  background: transparent;
  color: var(--muted, #33485d);
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  transition:
    background 0.12s var(--ease-out-expo),
    color 0.12s var(--ease-out-expo),
    border-color 0.12s var(--ease-out-expo);
}

.map-help-btn:hover {
  background: var(--map-green-tint);
  color: var(--map-green-text);
  border-color: oklch(0.55 0.145 150 / 0.45);
}

.map-help-btn:focus-visible {
  outline: 2px solid var(--map-green);
  outline-offset: 2px;
}

/* ── Layer Controls ──────────────────────── */
.layer-controls {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.layer-chips {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
  align-items: center;
}

.layer-chip {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 5px 12px;
  min-height: 30px;
  border-radius: 999px;
  border: 1.5px solid var(--line, rgba(18,34,49,0.18));
  background: transparent;
  color: var(--muted, #33485d);
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.82rem;
  font-weight: 500;
  cursor: pointer;
  user-select: none;
  white-space: nowrap;
  position: relative;
  transition:
    background 0.12s var(--ease-out-expo),
    border-color 0.12s var(--ease-out-expo),
    color 0.12s var(--ease-out-expo);
}

.layer-chip input[type="checkbox"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
  pointer-events: none;
}

.layer-chip:hover {
  background: var(--map-green-tint);
  border-color: oklch(0.55 0.145 150 / 0.4);
  color: var(--map-green-text);
}

.layer-chip:has(input:checked) {
  background: var(--map-green);
  border-color: var(--map-green);
  color: oklch(0.98 0.006 150);
}

.layer-chip:has(input:checked):hover {
  background: var(--map-green-hover);
  border-color: var(--map-green-hover);
}

.layer-chip:focus-within {
  outline: 2px solid var(--map-green);
  outline-offset: 2px;
}

/* Personalized chip — purple to signal distinct mode */
.layer-chip-personalized:has(input:checked) {
  background: var(--map-purple);
  border-color: var(--map-purple);
  color: oklch(0.98 0.006 285);
}

.layer-chip-personalized:has(input:checked):hover {
  background: var(--map-purple-hover);
  border-color: var(--map-purple-hover);
}

.layer-chip-personalized:focus-within {
  outline-color: var(--map-purple);
}

.layer-divider {
  width: 1.5px;
  height: 18px;
  background: var(--line, rgba(18,34,49,0.18));
  border-radius: 2px;
  flex-shrink: 0;
  align-self: center;
}

/* ── Personalized Config (grid-template-rows reveal) */
.personalized-config {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.3s var(--ease-out-expo);
}

.personalized-config.is-open {
  grid-template-rows: 1fr;
}

.personalized-config-inner {
  overflow: hidden;
  min-height: 0;
}

.personalized-config-body {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  margin-top: 4px;
  background: oklch(0.95 0.018 285 / 0.5);
  border: 1px solid oklch(0.42 0.12 285 / 0.28);
  border-radius: 12px;
  flex-wrap: wrap;
}

.personalized-input-label {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.personalized-input-label > span:first-child {
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--ink, #122231);
}

.controls-help {
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.77rem;
  color: var(--muted, #33485d);
  font-weight: 400;
}

.personalized-input {
  padding: 6px 12px;
  border-radius: 8px;
  border: 1.5px solid oklch(0.42 0.12 285 / 0.4);
  background: var(--panel-strong, #fffaf2);
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.875rem;
  color: var(--ink, #122231);
  width: 120px;
  -moz-appearance: textfield;
  appearance: textfield;
}

.personalized-input::-webkit-inner-spin-button,
.personalized-input::-webkit-outer-spin-button {
  -webkit-appearance: none;
}

.personalized-input:focus-visible {
  outline: 2px solid var(--map-purple);
  outline-offset: 2px;
  border-color: var(--map-purple);
}

/* ── Map Container ───────────────────────── */
#risk-map-container {
  width: 100%;
  height: 600px;
  position: relative;
  background: oklch(0.97 0.008 150);
  border: 1.5px solid oklch(0.55 0.145 150 / 0.32);
  border-radius: 16px;
  box-shadow:
    0 12px 36px rgba(18,34,49,0.09),
    0 3px 10px rgba(18,34,49,0.05);
  overflow: hidden;
}

#risk-map {
  width: 100%;
  height: 100%;
}

/* ── Legend (absolute overlay — bottom-left) */
.map-legend {
  position: absolute !important;
  bottom: 20px;
  left: 16px;
  top: auto !important;
  z-index: 500;
  background: rgba(253, 248, 242, 0.93);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 12px;
  border: 1px solid rgba(18,34,49,0.13);
  box-shadow: 0 4px 18px rgba(18,34,49,0.11);
  min-width: 172px;
  max-width: 212px;
}

.legend-header-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted, #33485d);
  border-radius: 12px;
  transition: color 0.12s;
}

.legend-header-btn:hover {
  color: var(--map-green-text);
}

.legend-header-btn:focus-visible {
  outline: 2px solid var(--map-green);
  outline-offset: -2px;
}

.legend-chevron {
  flex-shrink: 0;
  color: inherit;
  transition: transform 0.25s var(--ease-out-expo);
}

.legend-header-btn[aria-expanded="false"] .legend-chevron {
  transform: rotate(-90deg);
}

.legend-body {
  display: grid;
  grid-template-rows: 1fr;
  overflow: hidden;
  transition: grid-template-rows 0.28s var(--ease-out-expo);
}

.legend-body.is-collapsed {
  grid-template-rows: 0fr;
}

.legend-body-inner {
  min-height: 0;
  overflow: hidden;
}

.legend-list {
  list-style: none;
  padding: 0 12px 10px;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.79rem;
  color: var(--ink, #122231);
  line-height: 1.3;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--dot-color, #888);
  flex-shrink: 0;
}

.legend-swatch {
  width: 14px;
  height: 9px;
  border-radius: 2px;
  background: var(--swatch-fill, rgba(100,100,100,0.2));
  border: 1.5px solid var(--swatch-border, #888);
  flex-shrink: 0;
}

.legend-personalized-note {
  padding: 7px 12px 10px;
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.74rem;
  color: var(--muted, #33485d);
  border-top: 1px solid rgba(18,34,49,0.09);
  line-height: 1.4;
}

/* ── Loading overlay ─────────────────────── */
.map-loading-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: oklch(0.97 0.008 150 / 0.86);
  z-index: 200;
}

.map-loading-stack {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.map-loading-spinner {
  width: 36px;
  height: 36px;
  border: 3px solid oklch(0.55 0.145 150 / 0.2);
  border-top-color: var(--map-green);
  border-radius: 50%;
  animation: map-spin 0.7s linear infinite;
}

@keyframes map-spin { to { transform: rotate(360deg); } }

.map-loading-text {
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.875rem;
  color: var(--muted, #33485d);
}

/* ── Fallback ────────────────────────────── */
.map-fallback {
  display: none;
  position: absolute;
  inset: 0;
  align-items: center;
  justify-content: center;
  background: oklch(0.97 0.008 150 / 0.9);
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.9rem;
  color: var(--muted, #33485d);
  text-align: center;
  padding: 24px;
  z-index: 200;
}

/* ── Map Popup Card ──────────────────────── */
.map-popup-card {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 450;
  background: var(--panel-strong, #fffaf2);
  border-radius: 14px;
  border: 1px solid var(--line, rgba(18,34,49,0.14));
  box-shadow: 0 8px 28px rgba(18,34,49,0.14);
  padding: 16px 18px 14px;
  min-width: 200px;
  max-width: 260px;
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
}

.map-popup-heading,
.map-popup-subheading {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  color: var(--ink, #122231);
  margin-bottom: 8px;
  padding-right: 24px;
}

.map-popup-card > div {
  font-size: 0.84rem;
  color: var(--muted, #33485d);
  line-height: 1.5;
  margin-bottom: 2px;
}

.map-popup-card > div b {
  color: var(--ink, #122231);
  font-weight: 600;
}

.popup-close {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: 1px solid var(--line, rgba(18,34,49,0.14));
  background: transparent;
  color: var(--muted, #33485d);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  line-height: 1;
  transition: background 0.12s;
}

.popup-close:hover { background: var(--map-green-tint); }

/* ── Toast ───────────────────────────────── */
.map-toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 800;
  background: oklch(0.22 0.02 150);
  color: oklch(0.96 0.01 150);
  padding: 10px 18px;
  border-radius: 10px;
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.875rem;
  box-shadow: 0 4px 20px rgba(18,34,49,0.22);
  display: none;
  opacity: 0;
  transition: opacity 0.2s ease;
  max-width: 320px;
  line-height: 1.4;
}

/* ── Help Modal ──────────────────────────── */
.help-modal {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(18,34,49,0.45);
  z-index: 700;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.help-modal.is-open { display: flex; }

.modal-panel {
  background: var(--panel-strong, #fffaf2);
  border-radius: 20px;
  padding: 28px 28px 24px;
  max-width: 440px;
  width: calc(100% - 40px);
  border: 1px solid var(--line, rgba(18,34,49,0.14));
  box-shadow: 0 20px 60px rgba(18,34,49,0.18);
  position: relative;
}

.modal-title {
  font-family: 'Bricolage Grotesque', sans-serif;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--ink, #122231);
  margin: 0 0 16px;
  padding-right: 32px;
}

.modal-close {
  position: absolute;
  top: 18px;
  right: 18px;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 1px solid var(--line, rgba(18,34,49,0.14));
  background: transparent;
  color: var(--muted, #33485d);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.12s, color 0.12s;
}

.modal-close:hover {
  background: var(--map-green-tint);
  color: var(--map-green-text);
}

.modal-close:focus-visible {
  outline: 2px solid var(--map-green);
  outline-offset: 2px;
}

.help-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.help-list li {
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.9rem;
  color: var(--ink, #122231);
  line-height: 1.5;
  padding-left: 18px;
  position: relative;
}

.help-list li::before {
  content: '→';
  position: absolute;
  left: 0;
  color: var(--map-green);
  font-size: 0.8rem;
  top: 2px;
}

/* ── Caption ─────────────────────────────── */
.map-caption {
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
  font-size: 0.8rem;
  color: var(--muted, #33485d);
  text-align: center;
  margin-top: 4px;
}

/* ── Noscript ────────────────────────────── */
.map-noscript {
  text-align: center;
  padding: 48px;
  color: var(--muted, #33485d);
  font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', sans-serif;
}

/* ── Reduced motion ──────────────────────── */
@media (prefers-reduced-motion: reduce) {
  .personalized-config,
  .legend-body,
  .legend-chevron,
  .region-pill,
  .layer-chip,
  .map-help-btn,
  .map-loading-spinner {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}

/* ── Responsive ──────────────────────────── */
@media (max-width: 960px) {
  #risk-map-container { height: 480px; }
}

@media (max-width: 768px) {
  .map-controls-header { flex-direction: column; align-items: flex-start; gap: 10px; }
  #risk-map-container { height: 380px; }
}

@media (max-width: 640px) {
  .map-controls-panel { padding: 14px 16px; gap: 10px; }
  .region-pill { padding: 4px 12px; font-size: 0.82rem; }
  .layer-chip  { padding: 4px 10px;  font-size: 0.78rem; }
  .layer-divider { display: none; }
  #risk-map-container { height: 320px; }
  .map-legend { max-width: 180px; }
}

@media (max-width: 480px) {
  #risk-map-container { height: 260px; }
  .map-legend { min-width: 152px; max-width: 164px; }
  .personalized-config-body { flex-direction: column; align-items: flex-start; }
  .map-popup-card {
    top: auto;
    right: auto;
    bottom: 16px;
    left: 16px;
    max-width: calc(100% - 32px);
  }
}
</style>


<!-- ════════════════════════════════════
     Page Heading
     ════════════════════════════════════ -->
<section class="page-heading">
  <div>
    <p class="eyebrow">Live Risk Overview</p>
    <h1>Interactive Risk Map</h1>
  </div>
  <p>Explore real-time alerts and risk zones across the Gulf Coast region. Click any marker for details.</p>
</section>


<!-- ════════════════════════════════════
     Map Controls
     ════════════════════════════════════ -->
<section class="map-controls-panel" aria-label="Map controls">

  <div class="map-controls-header">
    <div class="region-filter-group">
      <span class="controls-label" id="region-label">Region</span>
      <div class="region-pills" role="group" aria-labelledby="region-label">
        <button class="region-pill active" data-region="" aria-pressed="true">All Regions</button>
        <button class="region-pill" data-region="LA" aria-pressed="false">Louisiana</button>
        <button class="region-pill" data-region="TX" aria-pressed="false">Texas</button>
        <button class="region-pill" data-region="MS" aria-pressed="false">Mississippi</button>
      </div>
    </div>
    <button class="map-help-btn" id="help-btn" aria-haspopup="dialog" aria-controls="help-modal">
      <svg width="15" height="15" viewBox="0 0 15 15" fill="none" aria-hidden="true">
        <circle cx="7.5" cy="7.5" r="6.5" stroke="currentColor" stroke-width="1.4"/>
        <path d="M6 5.6C6 4.71 6.7 4 7.5 4C8.38 4 9 4.71 9 5.6C9 6.6 7.5 7.3 7.5 8.4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
        <circle cx="7.5" cy="10.5" r="0.7" fill="currentColor"/>
      </svg>
      Help
    </button>
  </div>

  <div class="layer-controls" role="group" aria-label="Map layers">
    <span class="controls-label">Layers</span>
    <div class="layer-chips">

      <label class="layer-chip" title="Alert markers">
        <input type="checkbox" id="toggle-alerts" checked aria-label="Alerts" accesskey="1">
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
          <circle cx="6.5" cy="6.5" r="5.5" stroke="currentColor" stroke-width="1.4"/>
          <path d="M6.5 3.5v4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
          <circle cx="6.5" cy="9.5" r="0.65" fill="currentColor"/>
        </svg>
        Alerts
      </label>

      <label class="layer-chip" title="Risk zone overlays">
        <input type="checkbox" id="toggle-risk" checked aria-label="Risk Zones" accesskey="2">
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
          <path d="M1.5 11.5L6.5 2L11.5 11.5H1.5Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
        </svg>
        Risk Zones
      </label>

      <label class="layer-chip" title="Air quality index">
        <input type="checkbox" id="toggle-aqi" aria-label="AQI" accesskey="3">
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
          <path d="M1.5 6.5C3 4.5 4.5 8.5 6.5 6.5C8.5 4.5 10 8.5 11.5 6.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
        </svg>
        AQI
      </label>

      <label class="layer-chip" title="Wildfire activity">
        <input type="checkbox" id="toggle-wildfire" aria-label="Wildfire" accesskey="4">
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
          <path d="M6.5 11.5C6.5 11.5 2.5 8.5 2.5 5.5C2.5 4 4.5 2 6.5 4C8.5 2 10.5 4 10.5 5.5C10.5 8.5 6.5 11.5 6.5 11.5Z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
        </svg>
        Wildfire
      </label>

      <label class="layer-chip" title="Seismic activity">
        <input type="checkbox" id="toggle-earthquake" aria-label="Seismic" accesskey="5">
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
          <path d="M1 6.5H3.5L5 4L6.5 9L8.5 5.5L10 7.5H12" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Seismic
      </label>

      <label class="layer-chip" title="Weather conditions">
        <input type="checkbox" id="toggle-weather" aria-label="Weather" accesskey="6">
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
          <path d="M9.5 8.5a3 3 0 10-6 0" stroke="currentColor" stroke-width="1.4"/>
          <path d="M3.5 8.5H9.5" stroke="currentColor" stroke-width="1.4"/>
          <path d="M4.5 10.5H8.5M5.5 12H7.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
        </svg>
        Weather
      </label>

      <label class="layer-chip" title="Pollution levels">
        <input type="checkbox" id="toggle-pollution" aria-label="Pollution" accesskey="7">
        <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
          <circle cx="6.5" cy="6.5" r="5.5" stroke="currentColor" stroke-width="1.4"/>
          <path d="M4.5 4.5L8.5 8.5M8.5 4.5L4.5 8.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
        </svg>
        Pollution
      </label>

    </div>

    <div class="layer-divider" aria-hidden="true"></div>

    <label class="layer-chip layer-chip-personalized" title="Risk scores based on your profile">
      <input type="checkbox" id="toggle-personalized" aria-label="Personalized risk map">
      <svg width="13" height="13" viewBox="0 0 13 13" fill="none" aria-hidden="true">
        <circle cx="6.5" cy="4.5" r="2.25" stroke="currentColor" stroke-width="1.4"/>
        <path d="M2 12c0-2.5 2-4 4.5-4s4.5 1.5 4.5 4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
      </svg>
      Personalized
    </label>
  </div>

  <!-- User ID config — inline reveal via grid-template-rows -->
  <div class="personalized-config" id="personalized-config" aria-live="polite">
    <div class="personalized-config-inner">
      <div class="personalized-config-body">
        <label class="personalized-input-label" for="user-id-input">
          <span>User ID</span>
          <span class="controls-help" id="user-id-desc">Enter your numeric ID for personalized risk overlays</span>
        </label>
        <input class="personalized-input"
               type="number"
               id="user-id-input"
               min="1"
               value="1"
               aria-describedby="user-id-desc"
               accesskey="u">
      </div>
    </div>
  </div>

</section>


<!-- ════════════════════════════════════
     Map Canvas
     ════════════════════════════════════ -->
<div id="risk-map-container"
     tabindex="0"
     role="region"
     aria-label="Interactive risk map. Arrow keys pan, +/− zoom, click markers for details."
     aria-describedby="risk-map-instructions">

  <div id="risk-map" role="application" aria-label="Risk map with overlays and markers"></div>

  <div class="map-loading-overlay" id="map-loading">
    <div class="map-loading-stack">
      <div class="map-loading-spinner" id="map-loading-spinner" role="status" aria-label="Loading map data"></div>
      <div class="map-loading-text">Loading map data…</div>
    </div>
  </div>

  <div class="map-fallback" id="map-fallback" role="alert" aria-live="assertive"></div>

  <!-- Legend overlay — bottom-left of map -->
  <div class="map-legend" id="risk-map-legend" aria-label="Map legend">
    <button class="legend-header-btn" id="legend-toggle" aria-expanded="true" aria-controls="legend-body">
      <svg class="legend-chevron" width="11" height="11" viewBox="0 0 11 11" fill="none" aria-hidden="true">
        <path d="M2 3.5L5.5 7L9 3.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Legend
    </button>
    <div class="legend-body" id="legend-body">
      <div class="legend-body-inner">
        <ul class="legend-list">
          <li class="legend-item">
            <span class="legend-dot" style="--dot-color:#e74c3c" aria-hidden="true"></span>
            High severity
          </li>
          <li class="legend-item">
            <span class="legend-dot" style="--dot-color:#f39c12" aria-hidden="true"></span>
            Medium severity
          </li>
          <li class="legend-item">
            <span class="legend-dot" style="--dot-color:#27ae60" aria-hidden="true"></span>
            Low severity
          </li>
          <li class="legend-item">
            <span class="legend-swatch" style="--swatch-fill:rgba(255,87,34,0.22);--swatch-border:#ff5722" aria-hidden="true"></span>
            High risk zone
          </li>
          <li class="legend-item">
            <span class="legend-swatch" style="--swatch-fill:rgba(255,193,7,0.22);--swatch-border:#ffc107" aria-hidden="true"></span>
            Medium risk zone
          </li>
          <li class="legend-item">
            <span class="legend-swatch" style="--swatch-fill:rgba(76,175,80,0.22);--swatch-border:#4caf50" aria-hidden="true"></span>
            Low risk zone
          </li>
        </ul>
        <div class="legend-personalized-note" id="personalized-legend-msg" style="display:none">
          <strong>Personalized mode:</strong> zones reflect your profile's risk score.
        </div>
      </div>
    </div>
  </div>

  <span id="risk-map-instructions" class="sr-only">
    Tab to focus. Arrow keys pan, + and − zoom. Click or press Enter on a marker for details. Escape closes cards.
  </span>
</div>

<noscript><p class="map-noscript">JavaScript is required to view the interactive risk map.</p></noscript>

<p class="muted map-caption">Live alert markers and risk overlays update as data becomes available. All controls are keyboard and screen reader accessible.</p>


<!-- ════════════════════════════════════
     Help Modal
     ════════════════════════════════════ -->
<div class="help-modal" id="help-modal" role="dialog" aria-modal="true" aria-labelledby="help-modal-title" tabindex="-1">
  <div class="modal-panel">
    <button class="modal-close" id="help-close" aria-label="Close help">
      <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true">
        <path d="M3 3L11 11M11 3L3 11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
    </button>
    <h2 class="modal-title" id="help-modal-title">How to Use This Map</h2>
    <ul class="help-list">
      <li>Pan and zoom with your mouse, touch gestures, or keyboard arrows and +/−.</li>
      <li>Click or tap any marker to see alert or risk zone details.</li>
      <li>Use the region pills to focus on Louisiana, Texas, or Mississippi.</li>
      <li>Toggle layers to show or hide specific alert types and risk overlays.</li>
      <li>Enable Personalized to see risk scores tailored to your user profile.</li>
      <li>Keyboard: Tab to controls, Enter/Space to activate, Escape to close panels.</li>
    </ul>
  </div>
</div>

<!-- Toast (errors only) -->
<div class="map-toast" id="toast" aria-live="assertive" aria-atomic="true"></div>


<!-- ════════════════════════════════════
     Scripts
     ════════════════════════════════════ -->
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<script>
const MAP_ALERTS_URL            = <?php echo json_encode($alerts_url); ?>;
const MAP_RISK_URL               = <?php echo json_encode($risk_url); ?>;
const MAP_PERSONALIZED_RISK_URL  = <?php echo json_encode(rr_api_url($config, 'risk/map/personalized/')); ?>;

window.RISKRADAR_MAP_ALERTS_URL = MAP_ALERTS_URL;
window.RISKRADAR_MAP_RISK_URL   = MAP_RISK_URL;

// ── Toast (errors only) ───────────────
function showToast(msg, duration = 3500) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    toast.textContent = msg;
    toast.style.display = 'block';
    requestAnimationFrame(() => { toast.style.opacity = '1'; });
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => { toast.style.display = 'none'; }, 250);
    }, duration);
}

// ── Helpers ───────────────────────────
function getCurrentUserId() {
    const input = document.getElementById('user-id-input');
    const val = input ? parseInt(input.value, 10) : 1;
    return (val && val > 0) ? val : 1;
}

function getSeverityColor(severity) {
    const cs = getComputedStyle(document.documentElement);
    switch ((severity || '').toLowerCase()) {
        case 'high':   return cs.getPropertyValue('--alert-high').trim()   || '#e74c3c';
        case 'medium': return cs.getPropertyValue('--alert-medium').trim() || '#f39c12';
        case 'low':    return cs.getPropertyValue('--alert-low').trim()    || '#27ae60';
        default:       return '#2980b9';
    }
}

function getRiskLevelColor(level, alpha = 1) {
    let cssVar = '--risk-low';
    switch ((level || '').toLowerCase()) {
        case 'extreme': case 'high': cssVar = '--risk-extreme'; break;
        case 'medium':               cssVar = '--risk-medium';  break;
    }
    const color = getComputedStyle(document.documentElement).getPropertyValue(cssVar).trim();
    if (color.startsWith('#')) {
        const n = parseInt(color.slice(1), 16);
        return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${alpha})`;
    }
    return color;
}

// ── Data → Plotly traces ──────────────
function alertsToScatterTraces(alerts) {
    if (!Array.isArray(alerts)) return [];
    const cs = getComputedStyle(document.documentElement);
    return alerts
        .map(a => ({
            ...a,
            lat: a.lat != null ? a.lat : a.latitude,
            lon: a.lon != null ? a.lon : a.longitude,
        }))
        .filter(a => Number.isFinite(a.lat) && Number.isFinite(a.lon))
        .map(alert => {
            let color = getSeverityColor(alert.severity);
            const type = (alert.type || alert.alert_type || 'Alert').toLowerCase();
            if      (type.includes('air'))                               color = cs.getPropertyValue('--overlay-aqi').trim()        || '#7e57c2';
            else if (type.includes('wildfire') || type.includes('fire')) color = cs.getPropertyValue('--overlay-wildfire').trim()   || '#ff7043';
            else if (type.includes('earthquake'))                        color = cs.getPropertyValue('--overlay-earthquake').trim() || '#009688';
            else if (type.includes('weather'))                           color = cs.getPropertyValue('--overlay-weather').trim()    || '#1976d2';
            else if (type.includes('pollution'))                         color = cs.getPropertyValue('--overlay-pollution').trim()  || '#c62828';

            let details = `<strong style='color:${color}'>${alert.title || type}</strong><br>`;
            details += `Severity: <b>${alert.severity || 'N/A'}</b><br>`;
            if (type.includes('earthquake') && alert.magnitude) details += `Magnitude: <b>${alert.magnitude}</b><br>`;
            if (alert.description) details += `${alert.description}<br>`;
            details += `Region: ${alert.region || alert.location_name || 'N/A'}<br>`;
            if (alert.event_start) details += `Observed: ${alert.event_start}<br>`;
            if (alert.source)      details += `Source: ${alert.source}<br>`;

            return {
                type: 'scattermapbox',
                lat: [alert.lat],
                lon: [alert.lon],
                mode: 'markers',
                marker: {
                    size: (type.includes('earthquake') && alert.magnitude)
                        ? Math.max(13, Math.min(30, alert.magnitude * 4))
                        : 13,
                    color,
                    opacity: 0.85,
                    symbol: 'circle',
                },
                text: details,
                name: alert.type || alert.alert_type || 'Alert',
                customdata: [alert],
                hoverinfo: 'text',
            };
        });
}

function riskToOverlayTraces(riskZones) {
    if (!Array.isArray(riskZones) || !riskZones.length) return [];
    return riskZones
        .filter(zone => Array.isArray(zone.polygon) && zone.polygon.length > 2)
        .map(zone => {
            const normalized = zone.polygon
                .map(pt => {
                    if (Array.isArray(pt) && pt.length >= 2)                                               return { lat: pt[0], lon: pt[1] };
                    if (pt && typeof pt === 'object' && Number.isFinite(pt.lat) && Number.isFinite(pt.lon)) return pt;
                    return null;
                })
                .filter(Boolean);
            if (normalized.length < 3) return null;
            const lats = normalized.map(p => p.lat);
            const lons = normalized.map(p => p.lon);
            return {
                type: 'scattermapbox',
                lat: lats.concat([lats[0]]),
                lon: lons.concat([lons[0]]),
                mode: 'lines',
                fill: 'toself',
                fillcolor: getRiskLevelColor(zone.risk_level, 0.25),
                line: { color: getRiskLevelColor(zone.risk_level, 1), width: 2 },
                name: `Risk: ${zone.risk_level || 'N/A'}`,
                text: `Risk: ${zone.risk_level || 'N/A'}<br>Score: ${zone.score ?? zone.risk_score ?? 'N/A'}`,
                hoverinfo: 'text',
                customdata: [zone],
            };
        })
        .filter(Boolean);
}

// ── Fetch ─────────────────────────────
async function fetchMapData(personalized = false) {
    try {
        if (!MAP_ALERTS_URL || !MAP_RISK_URL) {
            showToast('Map API configuration is missing.');
            return null;
        }
        const riskUrl = personalized
            ? MAP_PERSONALIZED_RISK_URL + getCurrentUserId()
            : MAP_RISK_URL;
        const [alertsRes, riskRes] = await Promise.all([fetch(MAP_ALERTS_URL), fetch(riskUrl)]);
        if (!alertsRes.ok && !riskRes.ok) {
            showToast('Failed to load map data from the backend.');
            return null;
        }
        return {
            alerts: alertsRes.ok ? await alertsRes.json() : null,
            risk:   riskRes.ok  ? await riskRes.json()   : null,
        };
    } catch {
        showToast('Network error while loading map data.');
        return null;
    }
}

async function fetchOverlayAlerts(alertType) {
    try {
        const res = await fetch(MAP_ALERTS_URL + '?alert_type=' + encodeURIComponent(alertType));
        if (!res.ok) { showToast('Failed to load ' + alertType.replace('_', ' ') + ' overlay.'); return []; }
        const data = await res.json();
        return (data && data.alerts) || [];
    } catch {
        showToast('Network error loading ' + alertType.replace('_', ' ') + ' overlay.');
        return [];
    }
}

// ── Render ────────────────────────────
function renderMap(alertsData, riskData) {
    const traces = [
        ...alertsToScatterTraces((alertsData && alertsData.alerts) || []),
        ...riskToOverlayTraces((riskData && riskData.risk_zones) || []),
    ];

    if (!traces.length) {
        showMapFallback('No map data available for this region.');
        return;
    }
    hideMapFallback();

    const persLegend = document.getElementById('personalized-legend-msg');
    if (persLegend) persLegend.style.display = personalizedMode ? 'block' : 'none';

    Plotly.newPlot('risk-map', traces, {
        mapbox: {
            style: 'open-street-map',
            center: { lat: 30.45, lon: -91.15 },
            zoom: 6,
        },
        margin: { t: 0, b: 0, l: 0, r: 0 },
        showlegend: true,
    }, { responsive: true });

    document.getElementById('risk-map').on('plotly_click', function(data) {
        removePopup();
        if (!data || !data.points || !data.points.length) return;
        const pt = data.points[0];
        if (!pt.customdata || !pt.customdata[0]) return;
        const d = pt.customdata[0];
        let html = '';

        if (d.type || d.alert_type) {
            const type = (d.type || d.alert_type || '').toLowerCase();
            html = `<div class="map-popup-card" id="map-popup-card" tabindex="0" role="dialog" aria-modal="true"
                         aria-label="${d.title || type} alert. Severity: ${d.severity || 'N/A'}. Region: ${d.region || d.location_name || 'N/A'}.">
                <button class="popup-close" aria-label="Close detail card" onclick="this.parentNode.remove()">×</button>
                <div class="map-popup-heading">${d.title || type}</div>
                <div><b>Severity:</b> ${d.severity || 'N/A'}</div>
                ${d.magnitude  ? `<div><b>Magnitude:</b> ${d.magnitude}</div>` : ''}
                ${d.description ? `<div style='margin:4px 0'>${d.description}</div>` : ''}
                <div><b>Region:</b> ${d.region || d.location_name || 'N/A'}</div>
                ${d.event_start ? `<div><b>Observed:</b> ${d.event_start}</div>` : ''}
                ${d.source      ? `<div><b>Source:</b> ${d.source}</div>`       : ''}
            </div>`;
        } else if (d.risk_level) {
            html = `<div class="map-popup-card" id="map-popup-card" tabindex="0" role="dialog" aria-modal="true"
                         aria-label="Risk Zone. Level: ${d.risk_level}. Region: ${d.region || 'N/A'}.">
                <button class="popup-close" aria-label="Close detail card" onclick="this.parentNode.remove()">×</button>
                <div class="map-popup-subheading">Risk Zone Details</div>
                <div><b>Risk Level:</b> ${d.risk_level || 'N/A'}</div>
                ${d.risk_score != null ? `<div><b>Personalized Score:</b> ${d.risk_score}</div>` : ''}
                ${d.score      != null ? `<div><b>Score:</b> ${d.score}</div>`                   : ''}
                <div><b>Region:</b> ${d.region || 'N/A'}</div>
            </div>`;
        }

        if (!html) return;
        document.getElementById('risk-map-container').insertAdjacentHTML('beforeend', html);
        const popup = document.getElementById('map-popup-card');
        if (!popup) return;
        popup.focus();
        popup.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') { popup.remove(); return; }
            if (e.key === 'Tab') {
                const focusable = popup.querySelectorAll('button,[tabindex]:not([tabindex="-1"])');
                if (!focusable.length) return;
                const first = focusable[0], last = focusable[focusable.length - 1];
                if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
                else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
            }
        });
    });
}

function removePopup()        { const el = document.getElementById('map-popup-card'); if (el) el.remove(); }
function showMapFallback(msg) {
    const fb = document.getElementById('map-fallback');
    fb.textContent = msg;
    fb.style.display = 'flex';
    document.getElementById('map-loading').style.display = 'none';
    showToast(msg);
}
function hideMapFallback() { document.getElementById('map-fallback').style.display = 'none'; }
function hideMapLoading()  { document.getElementById('map-loading').style.display  = 'none'; }

// ── State ─────────────────────────────
let latestMapData    = null;
let currentRegion    = '';
let showAlerts       = true;
let showRisk         = true;
let showAQI          = false;
let showWildfire     = false;
let showEarthquake   = false;
let showWeather      = false;
let showPollution    = false;
let personalizedMode = false;

function filterByRegion(data, region) {
    if (!region || !Array.isArray(data)) return data;
    return data.filter(item => (item.region || '').toUpperCase() === region.toUpperCase());
}

async function renderFilteredMap() {
    if (!latestMapData) return;
    let alerts = showAlerts
        ? filterByRegion((latestMapData.alerts && latestMapData.alerts.alerts) || [], currentRegion)
        : [];
    const risks = showRisk
        ? filterByRegion((latestMapData.risk && latestMapData.risk.risk_zones) || [], currentRegion)
        : [];

    if (showAQI)        alerts = alerts.concat(filterByRegion(await fetchOverlayAlerts('air_quality'), currentRegion));
    if (showWildfire)   alerts = alerts.concat(filterByRegion(await fetchOverlayAlerts('wildfire'),    currentRegion));
    if (showEarthquake) alerts = alerts.concat(filterByRegion(await fetchOverlayAlerts('earthquake'),  currentRegion));
    if (showWeather)    alerts = alerts.concat(filterByRegion(await fetchOverlayAlerts('weather'),     currentRegion));
    if (showPollution)  alerts = alerts.concat(filterByRegion(await fetchOverlayAlerts('pollution'),   currentRegion));

    renderMap({ alerts }, { risk_zones: risks });
}

// ── Keyboard: arrow pan, +/− zoom ─────
document.addEventListener('DOMContentLoaded', function() {
    const mapContainer = document.getElementById('risk-map-container');
    const riskMap      = document.getElementById('risk-map');

    if (mapContainer && riskMap) {
        mapContainer.addEventListener('keydown', function(e) {
            const layout  = riskMap.layout || {};
            const center  = (layout.mapbox && layout.mapbox.center) || { lat: 30.45, lon: -91.15 };
            const step    = 0.5;
            const updates = {};

            if (e.key === 'ArrowLeft')  updates['mapbox.center.lon'] = center.lon - step;
            if (e.key === 'ArrowRight') updates['mapbox.center.lon'] = center.lon + step;
            if (e.key === 'ArrowUp')    updates['mapbox.center.lat'] = center.lat + step;
            if (e.key === 'ArrowDown')  updates['mapbox.center.lat'] = center.lat - step;
            if (e.key === '+' || e.key === '=') {
                updates['mapbox.zoom'] = (layout.mapbox && layout.mapbox.zoom ? layout.mapbox.zoom : 6) + 0.5;
            }
            if (e.key === '-' || e.key === '_') {
                updates['mapbox.zoom'] = Math.max(1, (layout.mapbox && layout.mapbox.zoom ? layout.mapbox.zoom : 6) - 0.5);
            }
            if (Object.keys(updates).length) {
                Plotly.relayout('risk-map', updates);
                e.preventDefault();
            }
        });

        // Touch pan / pinch-zoom
        let lastTouch = null, lastDist = null;
        riskMap.addEventListener('touchstart', function(e) {
            if (e.touches.length === 1) {
                lastTouch = { x: e.touches[0].clientX, y: e.touches[0].clientY };
            } else if (e.touches.length === 2) {
                const dx = e.touches[0].clientX - e.touches[1].clientX;
                const dy = e.touches[0].clientY - e.touches[1].clientY;
                lastDist = Math.sqrt(dx*dx + dy*dy);
            }
        });
        riskMap.addEventListener('touchmove', function(e) {
            const layout = riskMap.layout || {};
            if (e.touches.length === 1 && lastTouch) {
                const dx = e.touches[0].clientX - lastTouch.x;
                const dy = e.touches[0].clientY - lastTouch.y;
                if (layout.mapbox && layout.mapbox.center) {
                    Plotly.relayout('risk-map', {
                        'mapbox.center.lon': layout.mapbox.center.lon - dx * 0.01,
                        'mapbox.center.lat': layout.mapbox.center.lat + dy * 0.01,
                    });
                }
                lastTouch = { x: e.touches[0].clientX, y: e.touches[0].clientY };
            } else if (e.touches.length === 2 && lastDist) {
                const dx = e.touches[0].clientX - e.touches[1].clientX;
                const dy = e.touches[0].clientY - e.touches[1].clientY;
                const dist = Math.sqrt(dx*dx + dy*dy);
                if (Math.abs(dist - lastDist) > 5) {
                    const zoom = layout.mapbox && layout.mapbox.zoom ? layout.mapbox.zoom : 6;
                    Plotly.relayout('risk-map', { 'mapbox.zoom': Math.max(1, Math.min(20, zoom + (dist - lastDist) * 0.01)) });
                    lastDist = dist;
                }
            }
        });
        riskMap.addEventListener('touchend', () => { lastTouch = null; lastDist = null; });
    }
});

// ── Controls init ─────────────────────
document.addEventListener('DOMContentLoaded', async function() {
    const mapDiv = document.getElementById('risk-map');
    if (!window.Plotly || !mapDiv) return;

    const mapData = await fetchMapData();
    hideMapLoading();
    if (!mapData) return;
    latestMapData = mapData;
    renderFilteredMap();

    // Region pills
    document.querySelectorAll('.region-pill').forEach(function(btn) {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.region-pill').forEach(p => {
                p.classList.remove('active');
                p.setAttribute('aria-pressed', 'false');
            });
            btn.classList.add('active');
            btn.setAttribute('aria-pressed', 'true');
            currentRegion = btn.dataset.region;
            renderFilteredMap();
        });
    });

    // User ID reload
    document.getElementById('user-id-input').addEventListener('change', async function() {
        document.getElementById('map-loading').style.display = 'flex';
        const data = await fetchMapData(personalizedMode);
        hideMapLoading();
        if (!data) return;
        latestMapData = data;
        renderFilteredMap();
    });

    // Layer toggles
    const layers = {
        'toggle-alerts':     () => { showAlerts     = !showAlerts;     },
        'toggle-risk':       () => { showRisk       = !showRisk;       },
        'toggle-aqi':        () => { showAQI        = !showAQI;        },
        'toggle-wildfire':   () => { showWildfire   = !showWildfire;   },
        'toggle-earthquake': () => { showEarthquake = !showEarthquake; },
        'toggle-weather':    () => { showWeather    = !showWeather;    },
        'toggle-pollution':  () => { showPollution  = !showPollution;  },
    };
    Object.entries(layers).forEach(([id, fn]) => {
        const el = document.getElementById(id);
        if (el) el.addEventListener('change', () => { fn(); renderFilteredMap(); });
    });

    // Personalized toggle
    document.getElementById('toggle-personalized').addEventListener('change', async function(e) {
        personalizedMode = e.target.checked;
        document.getElementById('personalized-config').classList.toggle('is-open', personalizedMode);
        document.getElementById('map-loading').style.display = 'flex';
        const data = await fetchMapData(personalizedMode);
        hideMapLoading();
        if (!data) return;
        latestMapData = data;
        renderFilteredMap();
    });

    // Legend toggle
    const legendToggle = document.getElementById('legend-toggle');
    const legendBody   = document.getElementById('legend-body');
    if (legendToggle && legendBody) {
        legendToggle.addEventListener('click', function() {
            const expanded = legendToggle.getAttribute('aria-expanded') === 'true';
            legendToggle.setAttribute('aria-expanded', String(!expanded));
            legendBody.classList.toggle('is-collapsed', expanded);
        });
    }

    // Help modal
    const helpBtn   = document.getElementById('help-btn');
    const helpModal = document.getElementById('help-modal');
    const helpClose = document.getElementById('help-close');
    if (helpBtn && helpModal && helpClose) {
        helpBtn.addEventListener('click', function() {
            helpModal.classList.add('is-open');
            helpModal.focus();
        });
        helpClose.addEventListener('click', function() {
            helpModal.classList.remove('is-open');
            helpBtn.focus();
        });
        helpModal.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                helpModal.classList.remove('is-open');
                helpBtn.focus();
            }
        });
    }
});
</script>

<?php rr_render_layout_end(); ?>

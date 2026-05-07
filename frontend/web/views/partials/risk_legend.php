<?php
// Shared Risk Legend Partial for Map and Forecast UIs
// Usage: include or require this file in map.php, forecast.php, etc.
?>
<div class="legend-wrap" id="risk-legend" aria-label="Risk Level Legend">
  <button class="legend-toggle" aria-expanded="true" aria-controls="legend-list">
    <span class="legend-toggle-icon" aria-hidden="true">&#9776;</span>
    <span>Legend</span>
  </button>
  <ul class="legend-list" id="legend-list">
    <li><span class="icon-slot icon-bg-high" aria-label="High Risk"></span> High Risk</li>
    <li><span class="icon-slot icon-bg-medium" aria-label="Medium Risk"></span> Medium Risk</li>
    <li><span class="icon-slot icon-bg-low" aria-label="Low Risk"></span> Low Risk</li>
    <li><span class="icon-slot icon-bg-extreme" aria-label="Extreme Risk"></span> Extreme Risk</li>
    <li><span class="icon-slot icon-bg-aqi" aria-label="Air Quality"></span> Air Quality</li>
    <li><span class="icon-slot icon-bg-wildfire" aria-label="Wildfire"></span> Wildfire</li>
    <li><span class="icon-slot icon-bg-earthquake" aria-label="Earthquake"></span> Earthquake</li>
    <li><span class="icon-slot icon-bg-weather" aria-label="Weather"></span> Weather</li>
    <li><span class="icon-slot icon-bg-risk-medium" aria-label="Pollen"></span> Pollen</li>
    <li><span class="icon-slot icon-bg-pollution" aria-label="Pollution"></span> Pollution</li>
  </ul>
  <div class="legend-msg sr-only" aria-live="polite">Risk levels and types are color-coded for clarity. Use Tab to navigate.</div>
</div>

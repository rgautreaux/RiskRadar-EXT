

<link rel="stylesheet" href="/assets/app.css">
<link rel="stylesheet" href="/assets/theme.css">
<?php rr_render_layout_start('Forecast', 'forecast'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Stage 4 Preview</p>
        <h1>Predictive Risk Forecast</h1>
    </div>
    <p class="muted">This page will surface 24-48 hour environmental risk forecasts and confidence/trend visuals.</p>
</section>



<?php
// Stage 4: Dynamic forecast data integration (planned)
// This block will fetch forecast data from the backend once available.
// Example usage:
// $forecastResult = rr_api_get_forecast($config);
// if ($forecastResult['ok']) {
//     $forecastData = $forecastResult['data'];
//     // Render dynamic forecast chart and details here
// } else {
//     // Render fallback or error message
// }
?>
<section class="panel" style="background: var(--card); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); padding: 2rem 1.5rem; max-width: 700px; margin: 0 auto;">
    <h2 class="mb-2" style="color: var(--primary); font-family: 'Space Grotesk', Inter, Arial, sans-serif;">24–48 Hour Risk Forecast</h2>
    <?php // TODO: Replace static mockup below with dynamic rendering when backend is ready ?>
    <!-- Forecasted condition icons row (static for now) -->
    <div class="flex items-center justify-between mb-2" style="gap: 0.5rem; max-width: 560px; margin: 0 auto 1.5rem auto;">
        <img src="/assets/illustrations/weather.svg" alt="Weather" title="Weather" style="width: 38px; height: 38px;" />
        <img src="/assets/illustrations/fire.svg" alt="Fire" title="Fire" style="width: 38px; height: 38px;" />
        <img src="/assets/illustrations/air-quality.svg" alt="Air Quality" title="Air Quality" style="width: 38px; height: 38px;" />
        <img src="/assets/illustrations/flood.svg" alt="Flood" title="Flood" style="width: 38px; height: 38px;" />
        <img src="/assets/illustrations/pollen.svg" alt="Pollen" title="Pollen" style="width: 38px; height: 38px;" />
        <img src="/assets/illustrations/earthquake.svg" alt="Earthquake" title="Earthquake" style="width: 38px; height: 38px;" />
    </div>
    <svg width="100%" height="220" viewBox="0 0 560 220" aria-labelledby="forecastTitle forecastDesc" role="img" style="background: var(--accent); border-radius: var(--radius-md); box-shadow: var(--shadow-sm);">
        <title id="forecastTitle">Risk Forecast Timeline</title>
        <desc id="forecastDesc">Shows predicted risk levels and confidence bands for the next 48 hours</desc>
        <!-- Axes -->
        <line x1="50" y1="180" x2="520" y2="180" stroke="var(--muted)" stroke-width="2" />
        <line x1="50" y1="40" x2="50" y2="180" stroke="var(--muted)" stroke-width="2" />
        <!-- Confidence band (static for now) -->
        <polygon points="50,150 90,120 130,110 170,100 210,90 250,100 290,120 330,130 370,140 410,150 450,160 490,170 520,175 520,180 50,180" fill="var(--chart-1)" fill-opacity="0.18" />
        <!-- Forecast line (static for now) -->
        <polyline points="50,150 90,120 130,110 170,100 210,90 250,100 290,120 330,130 370,140 410,150 450,160 490,170 520,175" fill="none" stroke="var(--primary)" stroke-width="3" />
        <!-- Trend arrow -->
        <polygon points="520,175 510,170 510,180" fill="var(--primary)" />
        <!-- Y-axis labels -->
        <text x="40" y="180" font-size="12" fill="var(--muted-foreground)">Low</text>
        <text x="35" y="100" font-size="12" fill="var(--muted-foreground)">High</text>
        <!-- X-axis labels (hours) -->
        <text x="50" y="200" font-size="12" fill="var(--muted-foreground)">Now</text>
        <text x="210" y="200" font-size="12" fill="var(--muted-foreground)">+12h</text>
        <text x="370" y="200" font-size="12" fill="var(--muted-foreground)">+24h</text>
        <text x="520" y="200" font-size="12" fill="var(--muted-foreground)">+48h</text>
        <!-- Confidence indicator -->
        <rect x="400" y="50" width="120" height="28" rx="8" fill="var(--chart-1)" fill-opacity="0.12" />
        <text x="410" y="70" font-size="14" fill="var(--primary)" font-weight="bold">Confidence: 85%</text>
    </svg>
    <div class="flex items-center gap-4 mt-3" style="font-size: 14px; color: var(--muted-foreground);">
        <span style="display: inline-block; width: 12px; height: 12px; background: var(--primary); border-radius: 2px; margin-right: 6px;"></span>
        Forecasted Risk Level
        <span style="display: inline-block; width: 12px; height: 12px; background: var(--chart-1); border-radius: 2px; margin: 0 6px 0 18px; opacity: 0.18;"></span>
        Confidence Band
    </div>
    <div class="mt-4" style="color: var(--destructive); font-size: 13px;">
        <strong>Note:</strong> This is a static mockup. Actual data and interactivity will be added once the backend is ready.
    </div>
</section>

<?php rr_render_layout_end(); ?>

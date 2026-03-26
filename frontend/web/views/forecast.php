
<?php rr_render_layout_start('Forecast', 'forecast'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Stage 4 Preview</p>
        <h1>Predictive Risk Forecast</h1>
    </div>
    <p class="muted">This page will surface 24-48 hour environmental risk forecasts and confidence/trend visuals.</p>
</section>

<section class="panel" style="background: var(--card); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); padding: 2rem 1.5rem; max-width: 700px; margin: 0 auto;">
    <h2 class="mb-2" style="color: var(--primary); font-family: 'Space Grotesk', Inter, Arial, sans-serif;">24–48 Hour Risk Forecast</h2>
    <svg width="100%" height="220" viewBox="0 0 560 220" aria-labelledby="forecastTitle forecastDesc" role="img" style="background: var(--accent); border-radius: var(--radius-md); box-shadow: var(--shadow-sm);">
        <title id="forecastTitle">Risk Forecast Timeline</title>
        <desc id="forecastDesc">Shows predicted risk levels and confidence bands for the next 48 hours</desc>
        <!-- Axes -->
        <line x1="50" y1="180" x2="520" y2="180" stroke="var(--muted)" stroke-width="2" />
        <line x1="50" y1="40" x2="50" y2="180" stroke="var(--muted)" stroke-width="2" />
        <!-- Confidence band -->
        <polygon points="50,150 90,120 130,110 170,100 210,90 250,100 290,120 330,130 370,140 410,150 450,160 490,170 520,175 520,180 50,180" fill="var(--chart-1)" fill-opacity="0.18" />
        <!-- Forecast line -->
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

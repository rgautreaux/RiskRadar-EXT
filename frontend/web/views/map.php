
<?php rr_render_layout_start('Risk Map', 'map'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Stage 3 scaffold</p>
        <h1>Interactive Risk Map</h1>
    </div>
    <p>This page is reserved for the Stage 3 interactive map extension (Plotly), including zoom/pan support and click-through risk details.</p>
</section>

<section class="panel">
    <h2>Interactive Map</h2>
    <div id="risk-map-container" style="width:100%;height:480px;max-width:1000px;margin:0 auto 24px auto;background:#fff8ee;border-radius:12px;box-shadow:0 2px 12px rgba(18,34,49,0.08);overflow:hidden;">
        <div id="risk-map" style="width:100%;height:100%;"></div>
    </div>
    <noscript><p style="color:#b65c00">JavaScript is required to view the interactive map.</p></noscript>
    <p class="muted">The map will display live alert markers and risk overlays as data becomes available.</p>
</section>

<!-- Plotly.js CDN -->
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<script>
// Initial static map placeholder (Los Angeles)
document.addEventListener('DOMContentLoaded', function() {
    var mapDiv = document.getElementById('risk-map');
    if (window.Plotly && mapDiv) {
        Plotly.newPlot(mapDiv, [{
            type: 'scattermapbox',
            lat: ['34.0522'],
            lon: ['-118.2437'],
            mode: 'markers',
            marker: { size: 18, color: '#ef6f51' },
            text: ['Los Angeles (placeholder)'],
        }], {
            mapbox: {
                style: 'open-street-map',
                center: { lat: 34.0522, lon: -118.2437 },
                zoom: 7
            },
            margin: { t: 0, b: 0, l: 0, r: 0 },
            showlegend: false,
        }, {responsive: true, displayModeBar: false});
    }
});
</script>

<?php rr_render_layout_end(); ?>

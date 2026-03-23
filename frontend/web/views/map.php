
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
        <div id="risk-map" style="width:100%;height:100%;position:relative;"></div>
        <div id="map-loading" style="position:absolute;top:0;left:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,0.7);z-index:2;font-size:1.2rem;color:#b65c00;">Loading map data...</div>
        <div id="map-fallback" style="display:none;position:absolute;top:0;left:0;width:100%;height:100%;align-items:center;justify-content:center;background:rgba(255,255,255,0.9);z-index:3;font-size:1.1rem;color:#b65c00;text-align:center;"></div>
    </div>
    <noscript><p style="color:#b65c00">JavaScript is required to view the interactive map.</p></noscript>
    <p class="muted">The map will display live alert markers and risk overlays as data becomes available.</p>
</section>

<!-- Plotly.js CDN -->
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<script>
// Backend endpoint URLs (adjust if needed)
const MAP_ALERTS_URL = '/api/v1/alerts/map';
const MAP_RISK_URL = '/api/v1/risk/map';

function showMapFallback(message) {
    document.getElementById('map-fallback').style.display = 'flex';
    document.getElementById('map-fallback').textContent = message;
    document.getElementById('map-loading').style.display = 'none';
}

function hideMapFallback() {
    document.getElementById('map-fallback').style.display = 'none';
}

function hideMapLoading() {
    document.getElementById('map-loading').style.display = 'none';
}

// Severity color mapping
function getSeverityColor(severity) {
    switch ((severity || '').toLowerCase()) {
        case 'high': return '#e74c3c';
        case 'medium': return '#f39c12';
        case 'low': return '#27ae60';
        default: return '#2980b9';
    }
}

// Transform alert data to Plotly scatter points
function alertsToScatterTraces(alerts) {
    if (!Array.isArray(alerts)) return [];
    return alerts.filter(a => a.lat && a.lon).map(alert => ({
        type: 'scattermapbox',
        lat: [alert.lat],
        lon: [alert.lon],
        mode: 'markers',
        marker: {
            size: 13,
            color: getSeverityColor(alert.severity),
            opacity: 0.85,
            symbol: 'circle'
        },
        text: `${alert.type || 'Alert'}<br>Severity: ${alert.severity || 'N/A'}`,
        name: alert.type || 'Alert',
        hoverinfo: 'text'
    }));
}

// Placeholder for risk overlays (to be implemented)
function riskToOverlayTraces(risk) {
    // TODO: Implement risk zone overlays (polygons/heatmap)
    return [];
}

async function fetchMapData() {
    try {
        const [alertsRes, riskRes] = await Promise.all([
            fetch(MAP_ALERTS_URL),
            fetch(MAP_RISK_URL)
        ]);
        if (!alertsRes.ok && !riskRes.ok) {
            showMapFallback('Failed to load map data from the backend.');
            return null;
        }
        const alertsData = alertsRes.ok ? await alertsRes.json() : null;
        const riskData = riskRes.ok ? await riskRes.json() : null;
        return { alerts: alertsData, risk: riskData };
    } catch (e) {
        showMapFallback('Network error while loading map data.');
        return null;
    }
}

function renderMap(alertsData, riskData) {
    const alertTraces = alertsToScatterTraces((alertsData && alertsData.alerts) || []);
    const riskTraces = riskToOverlayTraces((riskData && riskData.risk_zones) || []);
    const traces = [...alertTraces, ...riskTraces];
    if (traces.length === 0) {
        showMapFallback('No valid map data to display.');
        return;
    }
    const layout = {
        mapbox: {
            style: 'open-street-map',
            center: { lat: 30.45, lon: -91.15 }, // Example: Baton Rouge
            zoom: 6
        },
        margin: { t: 0, b: 0, l: 0, r: 0 },
        showlegend: true
    };
    Plotly.newPlot('risk-map', traces, layout, {responsive: true});
}

// Main execution
fetchMapData().then(data => {
    hideMapLoading();
    if (!data || (!data.alerts && !data.risk)) {
        showMapFallback('No map data available.');
        return;
    }
    renderMap(data.alerts, data.risk);
}).catch(() => {
    showMapFallback('Error loading map data.');
        return null;
    }
}

function plotMap(alerts, risk) {
    const mapDiv = document.getElementById('risk-map');
    // Default center (Los Angeles)
    let center = { lat: 34.0522, lon: -118.2437 };
    let zoom = 7;

    // Prepare alert markers
    let alertMarkers = [];
    if (alerts && alerts.alerts && Array.isArray(alerts.alerts) && alerts.alerts.length > 0) {
        const lats = [], lons = [], texts = [], colors = [];
        alerts.alerts.forEach(alert => {
            if (typeof alert.latitude === 'number' && typeof alert.longitude === 'number') {
                lats.push(alert.latitude);
                lons.push(alert.longitude);
                texts.push(`${alert.title || 'Alert'}<br>Severity: ${alert.severity || 'unknown'}`);
                // Color by severity
                let color = '#ef6f51';
                if (alert.severity === 'high' || alert.severity === 'critical') color = '#b65c00';
                else if (alert.severity === 'moderate') color = '#f2b441';
                else if (alert.severity === 'low') color = '#1b8a89';
                colors.push(color);
            }
        });
        if (lats.length > 0) {
            center = { lat: lats[0], lon: lons[0] };
            alertMarkers.push({
                type: 'scattermapbox',
                lat: lats,
                lon: lons,
                mode: 'markers',
                marker: { size: 16, color: colors, opacity: 0.85 },
                text: texts,
                hoverinfo: 'text',
                name: 'Alerts',
            });
        }
    }

    // Prepare risk overlay (as polygons or heatmap)
    let riskOverlay = [];
    if (risk && risk.risk_zones && Array.isArray(risk.risk_zones) && risk.risk_zones.length > 0) {
        // For simplicity, plot as scatter points at polygon centroids (upgrade to polygons later)
        const lats = [], lons = [], scores = [], texts = [], colors = [];
        risk.risk_zones.forEach(zone => {
            if (zone.centroid && typeof zone.centroid.lat === 'number' && typeof zone.centroid.lon === 'number') {
                lats.push(zone.centroid.lat);
                lons.push(zone.centroid.lon);
                scores.push(zone.risk_score || 0);
                texts.push(`Risk: ${zone.risk_level || 'unknown'}<br>Score: ${zone.risk_score ?? ''}`);
                // Color by risk level
                let color = '#f2b441';
                if (zone.risk_level === 'high') color = '#b65c00';
                else if (zone.risk_level === 'moderate') color = '#ef6f51';
                else if (zone.risk_level === 'low') color = '#1b8a89';
                colors.push(color);
            }
        });
        if (lats.length > 0) {
            riskOverlay.push({
                type: 'scattermapbox',
                lat: lats,
                lon: lons,
                mode: 'markers',
                marker: { size: 12, color: colors, opacity: 0.5, symbol: 'circle' },
                text: texts,
                hoverinfo: 'text',
                name: 'Risk Zones',
            });
        }
    }

    // Compose all layers
    const data = [...riskOverlay, ...alertMarkers];
    if (data.length === 0) {
        showMapFallback('No map data available for the selected region.');
        return;
    }
    hideMapFallback();
    hideMapLoading();
    Plotly.newPlot(mapDiv, data, {
        mapbox: {
            style: 'open-street-map',
            center: center,
            zoom: zoom
        },
        margin: { t: 0, b: 0, l: 0, r: 0 },
        showlegend: true,
        legend: { orientation: 'h', x: 0, y: 1.02 },
    }, {responsive: true, displayModeBar: false});
}

document.addEventListener('DOMContentLoaded', async function() {
    const mapDiv = document.getElementById('risk-map');
    if (!window.Plotly || !mapDiv) return;
    const mapData = await fetchMapData();
    hideMapLoading();
    if (!mapData) return;
    plotMap(mapData.alerts, mapData.risk);
});
</script>

<?php rr_render_layout_end(); ?>

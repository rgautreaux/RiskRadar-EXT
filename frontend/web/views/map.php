

<?php
// Load config and build API URLs for JS
$config = require __DIR__ . '/../config/app.php';
require_once __DIR__ . '/../services/api_client.php';
$alerts_url = rr_api_url($config, 'alerts/map');
$risk_url = rr_api_url($config, 'risk/map');
rr_render_layout_start('Risk Map', 'map');
?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Stage 3 scaffold</p>
        <h1>Interactive Risk Map</h1>
    </div>
    <p>This page is reserved for the Stage 3 interactive map extension (Plotly), including zoom/pan support and click-through risk details.</p>
</section>


<section class="panel">
    <h2 id="risk-map-heading">Interactive Map</h2>
    <div style="margin-bottom:12px;display:flex;gap:24px;align-items:center;">
        <div>
            <label for="region-filter">Region Filter: </label>
            <select id="region-filter" style="min-width:120px;" aria-label="Region Filter">
                <option value="">All Regions</option>
                <option value="LA">Louisiana</option>
                <option value="TX">Texas</option>
                <option value="MS">Mississippi</option>
            </select>
        </div>
        <div>
            <label><input type="checkbox" id="toggle-alerts" checked> Show Alerts</label>
            <label style="margin-left:12px;"><input type="checkbox" id="toggle-risk" checked> Show Risk Zones</label>
        </div>
        <div style="margin-left:24px;">
            <label><input type="checkbox" id="toggle-personalized"> Personalized Risk Map</label>
        </div>
    </div>
    <div id="risk-map-container" style="width:100%;height:480px;max-width:1000px;margin:0 auto 24px auto;background:#fff8ee;border-radius:12px;box-shadow:0 2px 12px rgba(18,34,49,0.08);overflow:hidden;"
        tabindex="0" aria-label="Risk map showing alerts and risk zones" aria-describedby="risk-map-legend risk-map-heading">
        <div id="risk-map" style="width:100%;height:100%;position:relative;" role="region" aria-label="Interactive risk map"></div>
        <div id="map-loading" style="position:absolute;top:0;left:0;width:100%;height:100%;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,0.7);z-index:2;font-size:1.2rem;color:#b65c00;">Loading map data...</div>
        <div id="map-fallback" style="display:none;position:absolute;top:0;left:0;width:100%;height:100%;align-items:center;justify-content:center;background:rgba(255,255,255,0.9);z-index:3;font-size:1.1rem;color:#b65c00;text-align:center;" role="alert"></div>
    </div>
    <noscript><p style="color:#b65c00">JavaScript is required to view the interactive map.</p></noscript>
    <div id="risk-map-legend" style="margin-top:10px;" aria-live="polite">
        <strong>Legend:</strong>
        <ul>
            <li><span style="color:#e74c3c;font-weight:bold;">●</span> High severity alert</li>
            <li><span style="color:#f39c12;font-weight:bold;">●</span> Medium severity alert</li>
            <li><span style="color:#27ae60;font-weight:bold;">●</span> Low severity alert</li>
            <li><span style="color:#ff5722;font-weight:bold;">■</span> Extreme/High risk zone</li>
            <li><span style="color:#ffc107;font-weight:bold;">■</span> Medium risk zone</li>
            <li><span style="color:#4caf50;font-weight:bold;">■</span> Low risk zone</li>
        </ul>
        <div id="personalized-legend-msg" style="margin-top:6px;color:#b65c00;font-size:0.98em;display:none;">
            <strong>Personalized Mode:</strong> Risk zones reflect <u>your</u> personalized risk score at each location, based on your profile and health data.
        </div>
        <span class="sr-only">Use Tab to focus the map. Use arrow keys to pan and mouse or screen reader to explore overlays. Click or press Enter on a marker for details.</span>
    </div>
    <p class="muted">The map will display live alert markers and risk overlays as data becomes available. All features are keyboard and screen reader accessible.</p>
</section>


<!-- Plotly.js CDN -->
<script src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script>
<script>
// Inject config-driven API URLs from PHP
const MAP_ALERTS_URL = <?php echo json_encode($alerts_url); ?>;
const MAP_RISK_URL = <?php echo json_encode($risk_url); ?>;
const MAP_PERSONALIZED_RISK_URL = <?php echo json_encode(rr_api_url($config, 'risk/map/personalized/')); ?>; // Append user_id
// Helper: Get current user ID (stub, replace with real auth/user logic)
function getCurrentUserId() {
    // TODO: Replace with actual user session/auth logic
    return window.RISKRADAR_USER_ID || 1; // Default to 1 for demo
}

// --- Consolidated Map Logic: Modern, Accessible, Feature-Complete ---
// Accessibility: Keyboard navigation for map focus
document.addEventListener('DOMContentLoaded', function() {
    var mapContainer = document.getElementById('risk-map-container');
    if (mapContainer) {
        mapContainer.addEventListener('keydown', function(e) {
            if ([37,38,39,40].includes(e.keyCode)) {
                var pan = {"mapbox.center.lon": null, "mapbox.center.lat": null};
                var currentLayout = document.getElementById('risk-map').layout || {};
                var step = 0.5;
                if (currentLayout.mapbox && currentLayout.mapbox.center) {
                    pan["mapbox.center.lon"] = currentLayout.mapbox.center.lon;
                    pan["mapbox.center.lat"] = currentLayout.mapbox.center.lat;
                } else {
                    pan["mapbox.center.lon"] = -91.15;
                    pan["mapbox.center.lat"] = 30.45;
                }
                if (e.keyCode === 37) pan["mapbox.center.lon"] -= step;
                if (e.keyCode === 39) pan["mapbox.center.lon"] += step;
                if (e.keyCode === 38) pan["mapbox.center.lat"] += step;
                if (e.keyCode === 40) pan["mapbox.center.lat"] -= step;
                Plotly.relayout('risk-map', pan);
                e.preventDefault();
            }
        });
    }
});

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
function getSeverityColor(severity) {
    switch ((severity || '').toLowerCase()) {
        case 'high': return '#e74c3c';
        case 'medium': return '#f39c12';
        case 'low': return '#27ae60';
        default: return '#2980b9';
    }
}
function getRiskLevelColor(level, alpha=1) {
    let color;
    switch ((level || '').toLowerCase()) {
        case 'extreme': color = '255,0,0'; break;
        case 'high': color = '255,87,34'; break;
        case 'medium': color = '255,193,7'; break;
        case 'low': color = '76,175,80'; break;
        default: color = '33,150,243';
    }
    return `rgba(${color},${alpha})`;
}
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
        text: `${alert.type || 'Alert'}<br>Severity: ${alert.severity || 'N/A'}<br>Region: ${alert.region || 'N/A'}`,
        name: alert.type || 'Alert',
        customdata: [alert],
        hoverinfo: 'text'
    }));
}
function riskToOverlayTraces(riskZones) {
    if (!Array.isArray(riskZones) || riskZones.length === 0) return [];
    const polygonTraces = [];
    riskZones.forEach(zone => {
        if (Array.isArray(zone.polygon) && zone.polygon.length > 2) {
            const lats = zone.polygon.map(pt => pt[0]);
            const lons = zone.polygon.map(pt => pt[1]);
            polygonTraces.push({
                type: 'scattermapbox',
                lat: lats.concat([lats[0]]),
                lon: lons.concat([lons[0]]),
                mode: 'lines',
                fill: 'toself',
                fillcolor: getRiskLevelColor(zone.risk_level, 0.25),
                line: { color: getRiskLevelColor(zone.risk_level, 1), width: 2 },
                name: `Risk: ${zone.risk_level || 'N/A'}`,
                text: `Risk: ${zone.risk_level || 'N/A'}<br>Score: ${zone.score || 'N/A'}`,
                hoverinfo: 'text',
                customdata: [zone]
            });
        }
    });
    return polygonTraces;
}
async function fetchMapData(personalized = false) {
    try {
        let riskUrl = MAP_RISK_URL;
        if (personalized) {
            const userId = getCurrentUserId();
            riskUrl = MAP_PERSONALIZED_RISK_URL + userId;
        }
        const [alertsRes, riskRes] = await Promise.all([
            fetch(MAP_ALERTS_URL),
            fetch(riskUrl)
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
    // Show/hide personalized legend message
    const persLegend = document.getElementById('personalized-legend-msg');
    if (persLegend) persLegend.style.display = personalizedMode ? 'block' : 'none';

    const layout = {
        mapbox: {
            style: 'open-street-map',
            center: { lat: 30.45, lon: -91.15 },
            zoom: 6
        },
        margin: { t: 0, b: 0, l: 0, r: 0 },
        showlegend: true
    };
    Plotly.newPlot('risk-map', traces, layout, {responsive: true});
    var riskMapDiv = document.getElementById('risk-map');
    riskMapDiv.on('plotly_click', function(data) {
        if (data && data.points && data.points.length > 0) {
            const pt = data.points[0];
            if (pt.customdata && pt.customdata[0]) {
                const d = pt.customdata[0];
                if (d.type) {
                    alert("Alert Details:\n" +
                        `Type: ${d.type || 'N/A'}\n` +
                        `Severity: ${d.severity || 'N/A'}\n` +
                        `Region: ${d.region || 'N/A'}\n` +
                        `Source: ${d.source || 'N/A'}\n` +
                        `Time: ${d.generated_at || 'N/A'}`);
                } else if (d.risk_level) {
                    let msg = "Risk Zone Details:\n" +
                        `Risk Level: ${d.risk_level || 'N/A'}\n`;
                    if (typeof d.risk_score !== 'undefined' && d.risk_score !== null) {
                        msg += `Personalized Score: ${d.risk_score}\n`;
                    } else if (typeof d.score !== 'undefined' && d.score !== null) {
                        msg += `Score: ${d.score}\n`;
                    }
                    msg += `Region: ${d.region || 'N/A'}`;
                    alert(msg);
                }
            }
        }
    });
}
let latestMapData = null;
let currentRegion = '';
let showAlerts = true;
let showRisk = true;
let personalizedMode = false;

function filterByRegion(data, region) {
    if (!region) return data;
    if (Array.isArray(data)) {
        return data.filter(item => (item.region || '').toUpperCase() === region.toUpperCase());
    }
    return data;
}

function renderFilteredMap() {
    if (!latestMapData) return;
    const region = currentRegion;
    const alerts = showAlerts ? filterByRegion((latestMapData.alerts && latestMapData.alerts.alerts) || [], region) : [];
    const risks = showRisk ? filterByRegion((latestMapData.risk && latestMapData.risk.risk_zones) || [], region) : [];
    renderMap({alerts}, {risk_zones: risks});
}

document.addEventListener('DOMContentLoaded', async function() {
    const mapDiv = document.getElementById('risk-map');
    if (!window.Plotly || !mapDiv) return;
    const mapData = await fetchMapData();
    hideMapLoading();
    if (!mapData) return;
    latestMapData = mapData;
    renderFilteredMap();

    // Region filter
    document.getElementById('region-filter').addEventListener('change', function(e) {
        currentRegion = e.target.value;
        renderFilteredMap();
    });
    // Overlay toggles
    document.getElementById('toggle-alerts').addEventListener('change', function(e) {
        showAlerts = e.target.checked;
        renderFilteredMap();
    });
    document.getElementById('toggle-risk').addEventListener('change', function(e) {
        showRisk = e.target.checked;
        renderFilteredMap();
    });
    // Personalized Risk Map toggle
    document.getElementById('toggle-personalized').addEventListener('change', async function(e) {
        personalizedMode = e.target.checked;
        document.getElementById('map-loading').style.display = 'flex';
        const mapData = await fetchMapData(personalizedMode);
        hideMapLoading();
        if (!mapData) return;
        latestMapData = mapData;
        renderFilteredMap();
    });
});
// --- End Consolidated Map Logic ---
</script>

<?php rr_render_layout_end(); ?>

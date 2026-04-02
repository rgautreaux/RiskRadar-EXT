// plotly-map.js
// Stage 3: Interactive Risk Map (Plotly)
// Loads alert markers and risk zone polygons from backend and renders them using Plotly.js

// Assumes Plotly.js is loaded via CDN in the HTML

async function fetchJson(url) {
    const resp = await fetch(url);
    if (!resp.ok) throw new Error('Failed to fetch ' + url);
    return await resp.json();
}

// Overlay color/label mapping
const OVERLAY_COLORS = {
    air_quality: '#43a047',
    wildfire: '#e65100',
    weather: '#1976d2',
    pollution: '#6d4c41',
    earthquake: '#b71c1c',
    default: '#2196f3'
};
const OVERLAY_LABELS = {
    air_quality: 'AQI',
    wildfire: 'Wildfire',
    weather: 'Weather',
    pollution: 'Pollution',
    earthquake: 'Earthquake',
    default: 'Risk Zone'
};

async function renderRiskMap(alertsUrl, riskUrl, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
    let alerts = [], riskZones = [];
    try {
        const [alertsData, riskData] = await Promise.all([
            fetchJson(alertsUrl),
            fetchJson(riskUrl)
        ]);
        alerts = alertsData.alerts || [];
        riskZones = riskData.risk_zones || [];
    } catch (e) {
        container.innerHTML = '<div style="color:#b00">Failed to load map data.</div>';
        return;
    }

    // Get overlay toggle states
    const toggles = {
        alerts: document.getElementById('toggle-alerts')?.checked,
        risk: document.getElementById('toggle-risk')?.checked,
        aqi: document.getElementById('toggle-aqi')?.checked,
        wildfire: document.getElementById('toggle-wildfire')?.checked,
        earthquake: document.getElementById('toggle-earthquake')?.checked,
        weather: document.getElementById('toggle-weather')?.checked,
        pollution: document.getElementById('toggle-pollution')?.checked
    };

    // Prepare alert markers
    const alertMarkers = toggles.alerts !== false ? alerts.filter(a => a.latitude && a.longitude).map(a => ({
        type: 'scattermapbox',
        lat: [a.latitude],
        lon: [a.longitude],
        mode: 'markers',
        marker: { size: 12, color: '#ef6f51' },
        name: a.title || a.alert_type,
        text: a.description || '',
        customdata: [a],
        hoverinfo: 'text+name'
    })) : [];

    // Prepare overlays by type
    function overlayEnabled(type) {
        if (type === 'air_quality') return toggles.aqi !== false;
        if (type === 'wildfire') return toggles.wildfire !== false;
        if (type === 'weather') return toggles.weather !== false;
        if (type === 'pollution') return toggles.pollution !== false;
        if (type === 'earthquake') return toggles.earthquake !== false;
        return toggles.risk !== false;
    }

    const riskPolys = riskZones.filter(z => z.polygon && z.polygon.length > 2 && overlayEnabled(z.risk_level || z.label || 'risk')).map(z => {
        const type = (z.label || z.risk_level || 'default').toLowerCase();
        const color = OVERLAY_COLORS[type] || OVERLAY_COLORS.default;
        const label = OVERLAY_LABELS[type] || OVERLAY_LABELS.default;
        return {
            type: 'scattermapbox',
            lat: z.polygon.map(p => p.lat),
            lon: z.polygon.map(p => p.lon),
            mode: 'lines',
            fill: 'toself',
            fillcolor: color + '33', // 20% opacity
            line: { color, width: 2 },
            name: label,
            text: z.risk_level || label,
            hoverinfo: 'text+name'
        };
    });

    const data = [...riskPolys, ...alertMarkers];
    const layout = {
        mapbox: {
            style: 'open-street-map',
            center: { lat: 32.5, lon: -92.5 },
            zoom: 5.5
        },
        margin: { t: 0, b: 0, l: 0, r: 0 },
        showlegend: true,
        autosize: true,
        height: container.offsetHeight || 480
    };
    Plotly.newPlot(container, data, layout, {responsive: true});
}

// Re-render map on overlay toggle, region filter, or user ID change
function setupRiskMapListeners(alertsUrl, riskUrl, containerId) {
    [
        'toggle-alerts','toggle-risk','toggle-aqi','toggle-wildfire','toggle-earthquake','toggle-weather','toggle-pollution','toggle-personalized','region-filter','user-id-input'
    ].forEach(function(id) {
        var el = document.getElementById(id);
        if (el) {
            el.addEventListener('change', function() {
                window.renderRiskMap(alertsUrl, riskUrl, containerId);
            });
        }
    });
}

window.renderRiskMap = renderRiskMap;
window.setupRiskMapListeners = setupRiskMapListeners;

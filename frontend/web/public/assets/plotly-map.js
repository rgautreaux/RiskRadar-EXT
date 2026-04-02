// plotly-map.js
// Stage 3: Interactive Risk Map (Plotly)
// Loads alert markers and risk zone polygons from backend and renders them using Plotly.js

// Assumes Plotly.js is loaded via CDN in the HTML

async function fetchJson(url) {
    const resp = await fetch(url);
    if (!resp.ok) throw new Error('Failed to fetch ' + url);
    return await resp.json();
}

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

    // Prepare alert markers
    const alertMarkers = alerts.filter(a => a.latitude && a.longitude).map(a => ({
        type: 'scattermapbox',
        lat: [a.latitude],
        lon: [a.longitude],
        mode: 'markers',
        marker: { size: 12, color: '#ef6f51' },
        name: a.title || a.alert_type,
        text: a.description || '',
        customdata: [a],
        hoverinfo: 'text+name'
    }));

    // Prepare risk zone polygons
    const riskPolys = riskZones.filter(z => z.polygon && z.polygon.length > 2).map(z => ({
        type: 'scattermapbox',
        lat: z.polygon.map(p => p.lat),
        lon: z.polygon.map(p => p.lon),
        mode: 'lines',
        fill: 'toself',
        fillcolor: 'rgba(33,150,243,0.18)',
        line: { color: '#2196f3', width: 2 },
        name: z.risk_level || 'Risk Zone',
        text: z.risk_level,
        hoverinfo: 'text+name'
    }));

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

window.renderRiskMap = renderRiskMap;

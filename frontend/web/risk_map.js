// risk_map.js
// Interactive Risk Map rendering for map.php
// Requires Plotly.js (CDN or npm)

document.addEventListener('DOMContentLoaded', function() {
    const mapContainer = document.createElement('div');
    mapContainer.id = 'risk-map-container';
    document.querySelector('section.panel').appendChild(mapContainer);

    // Load Plotly.js from CDN if not present
    if (typeof window.Plotly === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdn.plot.ly/plotly-2.27.0.min.js';
        script.onload = renderMap;
        document.head.appendChild(script);
    } else {
        renderMap();
    }

    function renderMap() {
        // Fetch alert and risk zone data
        Promise.all([
            fetch('/api/v1/alerts/map').then(r => r.json()),
            fetch('/api/v1/risk/map').then(r => r.json())
        ]).then(([alertsData, riskData]) => {
            // Prepare alert markers
            const alertMarkers = {
                type: 'scattermapbox',
                lat: alertsData.map(a => a.latitude),
                lon: alertsData.map(a => a.longitude),
                text: alertsData.map(a => `${a.title}: ${a.severity}`),
                mode: 'markers',
                marker: { size: 12, color: 'red' },
                name: 'Alerts',
                customdata: alertsData
            };
            // Prepare risk zone polygons (if present)
            const riskZones = (riskData.risk_zones || []).map(zone => ({
                type: 'scattermapbox',
                lat: (zone.polygon || [zone.centroid]).map(p => p.lat),
                lon: (zone.polygon || [zone.centroid]).map(p => p.lon),
                mode: 'lines+markers',
                fill: 'toself',
                marker: { size: 8, color: zone.risk_level === 'high' ? 'crimson' : zone.risk_level === 'moderate' ? 'orange' : 'green' },
                line: { width: 2 },
                name: `Risk: ${zone.risk_level}`
            }));
            // Layout
            const layout = {
                mapbox: {
                    style: 'open-street-map',
                    center: { lat: 30.9843, lon: -91.9623 },
                    zoom: 5
                },
                margin: { t: 0, b: 0, l: 0, r: 0 },
                showlegend: true,
                autosize: true,
                height: mapContainer.offsetHeight || 480
            };
            Plotly.newPlot('risk-map-container', [alertMarkers, ...riskZones], layout, {responsive: true});
            // Click event for marker details
            mapContainer.on('plotly_click', function(data) {
                if (data.points && data.points[0] && data.points[0].customdata) {
                    const alert = data.points[0].customdata;
                    openMarkerModal(alert.title, alert.description);
                }
            });
        });
    }
});

// Helper for accessible modal (already in map.php)
// function openMarkerModal(title, description) {...}

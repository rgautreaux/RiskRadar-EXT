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

    // Accessibility: set ARIA attributes on map container
    container.setAttribute('role', 'region');
    container.setAttribute('aria-label', 'Interactive Risk Map');
    container.setAttribute('tabindex', '0');
    container.setAttribute('aria-live', 'polite');

    // Keyboard navigation for markers/overlays
    let markerEls = [];
    if (alerts.length > 0 && toggles.alerts !== false) {
        markerEls = alerts.filter(a => a.latitude && a.longitude);
    }
    let focusIdx = -1;

    container.addEventListener('keydown', function(e) {
        // Tab/Shift+Tab: cycle through markers
        if (e.key === 'Tab') {
            if (markerEls.length === 0) return;
            e.preventDefault();
            if (e.shiftKey) {
                focusIdx = (focusIdx <= 0) ? markerEls.length - 1 : focusIdx - 1;
            } else {
                focusIdx = (focusIdx + 1) % markerEls.length;
            }
            announceMarkerFocus(markerEls[focusIdx]);
        }
        // Enter/Space: show marker details
        if ((e.key === 'Enter' || e.key === ' ') && focusIdx >= 0 && markerEls[focusIdx]) {
            showMarkerDetails(markerEls[focusIdx]);
            e.preventDefault();
        }
        // Arrow keys: pan map
        if (["ArrowLeft","ArrowRight","ArrowUp","ArrowDown"].includes(e.key)) {
            // Use Plotly relayout for panning
            let pan = {lon: 0, lat: 0};
            if (e.key === 'ArrowLeft') pan.lon = -0.5;
            if (e.key === 'ArrowRight') pan.lon = 0.5;
            if (e.key === 'ArrowUp') pan.lat = 0.5;
            if (e.key === 'ArrowDown') pan.lat = -0.5;
            const cur = layout.mapbox.center;
            Plotly.relayout(container, {'mapbox.center.lon': cur.lon + pan.lon, 'mapbox.center.lat': cur.lat + pan.lat});
            e.preventDefault();
        }
        // +/- keys: zoom
        if (e.key === '+' || e.key === '=') {
            Plotly.relayout(container, {'mapbox.zoom': layout.mapbox.zoom + 0.5});
            e.preventDefault();
        }
        if (e.key === '-') {
            Plotly.relayout(container, {'mapbox.zoom': layout.mapbox.zoom - 0.5});
            e.preventDefault();
        }
    });

    // Announce marker focus for screen readers
    function announceMarkerFocus(marker) {
        const toast = document.getElementById('toast');
        if (!toast) return;
        toast.textContent = `Focused alert: ${marker.title || marker.alert_type || 'Alert'}`;
        toast.style.display = 'block';
        toast.style.opacity = 1;
        setTimeout(() => { toast.style.opacity = 0; setTimeout(()=>{toast.style.display='none';}, 400); }, 1200);
    }

    // Show marker details (simple alert for now, replace with modal for full accessibility)
    function showMarkerDetails(marker) {
        alert(`Alert: ${marker.title || marker.alert_type || ''}\n${marker.description || ''}`);
    }
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
                announceOverlayChange(id);
            });
        }
    });

    // Keyboard shortcuts for overlay toggles (Alt+1 ... Alt+7)
    document.addEventListener('keydown', function(e) {
        if (e.altKey && !e.shiftKey && !e.ctrlKey && !e.metaKey) {
            const keyMap = {
                '1': 'toggle-alerts',
                '2': 'toggle-risk',
                '3': 'toggle-aqi',
                '4': 'toggle-wildfire',
                '5': 'toggle-earthquake',
                '6': 'toggle-weather',
                '7': 'toggle-pollution'
            };
            if (keyMap[e.key]) {
                const cb = document.getElementById(keyMap[e.key]);
                if (cb) {
                    cb.checked = !cb.checked;
                    cb.focus();
                    cb.dispatchEvent(new Event('change', {bubbles:true}));
                    e.preventDefault();
                }
            }
        }
    });
}

// Announce overlay changes for screen readers
function announceOverlayChange(id) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    let msg = '';
    switch(id) {
        case 'toggle-alerts': msg = 'Alerts overlay toggled.'; break;
        case 'toggle-risk': msg = 'Risk zones overlay toggled.'; break;
        case 'toggle-aqi': msg = 'AQI overlay toggled.'; break;
        case 'toggle-wildfire': msg = 'Wildfire overlay toggled.'; break;
        case 'toggle-earthquake': msg = 'Earthquake overlay toggled.'; break;
        case 'toggle-weather': msg = 'Weather overlay toggled.'; break;
        case 'toggle-pollution': msg = 'Pollution overlay toggled.'; break;
        case 'region-filter': msg = 'Region filter changed.'; break;
        case 'user-id-input': msg = 'User ID changed.'; break;
        default: msg = 'Overlay changed.';
    }
    toast.textContent = msg;
    toast.style.display = 'block';
    toast.style.opacity = 1;
    setTimeout(() => { toast.style.opacity = 0; setTimeout(()=>{toast.style.display='none';}, 400); }, 1200);
}

window.renderRiskMap = renderRiskMap;
window.setupRiskMapListeners = setupRiskMapListeners;

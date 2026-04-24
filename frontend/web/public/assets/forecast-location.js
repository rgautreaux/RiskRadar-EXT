let CURRENT_USER_ID = null;

const forecastState = {
    currentRequestId: 0,
};

function normalizeApiConfig() {
    const explicitBase = (window.__RISKRADAR_FORECAST_API_BASE__ || window.__RISKRADAR_API_BASE__ || '').trim();
    const explicitPrefix = (window.__RISKRADAR_FORECAST_API_PREFIX__ || window.__RISKRADAR_API_PREFIX__ || '/api/v1').trim();
    const prefix = explicitPrefix.startsWith('/') ? explicitPrefix : `/${explicitPrefix}`;

    if (explicitBase) {
        const cleanedBase = explicitBase.endsWith('/') ? explicitBase.slice(0, -1) : explicitBase;
        return { base: cleanedBase, prefix };
    }

    // Safe fallback for same-origin development when no explicit API config is injected.
    return {
        base: window.location.origin,
        prefix,
    };
}

async function initCurrentUser() {
    try {
        const api = normalizeApiConfig();
        const res = await fetch(`${api.base}${api.prefix}/auth/me`, { credentials: 'include' });
        if (res.ok) {
            const user = await res.json();
            if (user && user.id) {
                CURRENT_USER_ID = user.id;
            }
        }
    } catch (_err) {
        // Not authenticated or network error — use anonymous forecast endpoint.
    }
}

document.addEventListener('DOMContentLoaded', async () => {
    await initCurrentUser();
    const locationForm = document.getElementById('forecast-location-form');
    const locationInput = document.getElementById('forecast-location-input');
    const useMyLocationBtn = document.getElementById('use-my-location-btn');
    const status = document.getElementById('forecast-location-status');

    if (locationForm && locationInput) {
        locationForm.addEventListener('submit', event => {
            event.preventDefault();
            const value = locationInput.value.trim();
            if (value) {
                loadForecastForLocation(value);
            }
        });
    }

    if (useMyLocationBtn) {
        useMyLocationBtn.addEventListener('click', () => {
            if (!navigator.geolocation) {
                if (status) {
                    status.textContent = 'Geolocation is not supported in this browser.';
                }
                return;
            }

            navigator.geolocation.getCurrentPosition(
                position => loadForecastForCoordinates(position.coords.latitude, position.coords.longitude),
                () => {
                    if (status) {
                        status.textContent = 'Location permission denied. Enter a location manually.';
                    }
                },
            );
        });
    }

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => loadForecastForCoordinates(position.coords.latitude, position.coords.longitude),
            () => {
                if (status) {
                    status.textContent = 'Enter a ZIP code or city/state to load a forecast.';
                }
            },
        );
    } else if (status) {
        status.textContent = 'Enter a ZIP code or city/state to load a forecast.';
    }
});

function buildForecastUrl(params) {
    const api = normalizeApiConfig();
    const endpoint = CURRENT_USER_ID
        ? `${api.prefix}/forecast/personalized/${CURRENT_USER_ID}`
        : `${api.prefix}/forecast`;
    const url = new URL(`${api.base}${endpoint}`);
    Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== '') {
            url.searchParams.set(key, String(value));
        }
    });
    return url.toString();
}

async function loadForecastForCoordinates(lat, lon) {
    const status = document.getElementById('forecast-location-status');
    if (status) {
        status.textContent = `Loading forecast for your location (${lat.toFixed(2)}, ${lon.toFixed(2)})...`;
    }

    const requestId = ++forecastState.currentRequestId;
    try {
        const response = await fetch(buildForecastUrl({ lat, lon }));
        if (!response.ok) {
            throw new Error('Failed to fetch forecast');
        }

        const data = await response.json();
        if (requestId === forecastState.currentRequestId) {
            renderForecast(data, `Your location (${lat.toFixed(2)}, ${lon.toFixed(2)})`);
        }
    } catch (_error) {
        if (status) {
            status.textContent = 'Failed to load forecast for your location.';
        }
    }
}

async function loadForecastForLocation(location) {
    const status = document.getElementById('forecast-location-status');
    if (status) {
        status.textContent = `Loading forecast for ${location}...`;
    }

    const requestId = ++forecastState.currentRequestId;
    try {
        const response = await fetch(buildForecastUrl({ location }));
        if (!response.ok) {
            throw new Error('Failed to fetch forecast');
        }

        const data = await response.json();
        if (requestId === forecastState.currentRequestId) {
            renderForecast(data, location);
        }
    } catch (_error) {
        if (status) {
            status.textContent = 'Failed to load forecast.';
        }
    }
}

function renderForecast(data, locationLabel) {
    const status = document.getElementById('forecast-location-status');
    const results = document.getElementById('forecast-results');

    if (!results || !status) {
        return;
    }

    if (!data) {
        status.textContent = `No forecast data available for ${locationLabel}.`;
        results.innerHTML = '';
        return;
    }

    const points = Array.isArray(data.forecast_points) ? data.forecast_points : [];
    const zones = Array.isArray(data.risk_zones) ? data.risk_zones : [];

    if (points.length === 0 && zones.length === 0) {
        status.textContent = `No forecast data available for ${locationLabel}.`;
        results.innerHTML = '';
        return;
    }

    status.innerHTML = [
        `<strong>${escapeHtml(data.personalized ? 'Personalized forecast' : 'Forecast')}</strong> for ${escapeHtml(locationLabel)}`,
        data.summary ? `<div style="margin-top:0.35rem;">${escapeHtml(data.summary)}</div>` : '',
        `<div style="margin-top:0.35rem; font-size:0.95rem; color: var(--muted-foreground);">Updated: ${escapeHtml(data.generated_at || '')}</div>`,
    ].join('');

    // Per-risk forecast rendering
    let perRiskMarkup = '';
    if (data.per_risk_forecasts && typeof data.per_risk_forecasts === 'object') {
        perRiskMarkup = '<div class="per-risk-forecast-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-top: 1.2rem;">';
        const riskTypeMeta = {
            weather: { icon: '/assets/illustrations/weather.svg', label: 'Weather', class: 'icon-bg-weather' },
            air_quality: { icon: '/assets/illustrations/air-quality.svg', label: 'Air Quality', class: 'icon-bg-aqi' },
            wildfire: { icon: '/assets/illustrations/fire.svg', label: 'Wildfire', class: 'icon-bg-wildfire' },
            flood: { icon: '/assets/illustrations/flood.svg', label: 'Flood', class: 'icon-bg-extreme' },
            earthquake: { icon: '/assets/illustrations/earthquake.svg', label: 'Earthquake', class: 'icon-bg-earthquake' },
            pollen: { icon: '/assets/illustrations/pollen.svg', label: 'Pollen', class: 'icon-bg-risk-medium' },
            pollution: { icon: '/assets/illustrations/pollution.svg', label: 'Pollution', class: 'icon-bg-pollution' },
        };
        for (const [riskType, forecastList] of Object.entries(data.per_risk_forecasts)) {
            const meta = riskTypeMeta[riskType] || { icon: '', label: riskType, class: '' };
            const first = forecastList && forecastList.length ? forecastList[0] : null;
            const riskLevel = first ? escapeHtml(first.risk_level) : 'N/A';
            const trend = forecastList && forecastList.length > 1 ? (first.risk_score < forecastList[forecastList.length-1].risk_score ? 'increasing' : (first.risk_score > forecastList[forecastList.length-1].risk_score ? 'decreasing' : 'steady')) : 'steady';
            const confidence = first && typeof first.confidence === 'number' ? `${Math.round(first.confidence * 100)}%` : 'N/A';
            perRiskMarkup += `
                <article class="panel" style="display: flex; align-items: center; gap: 1rem; padding: 1rem; border: 1px solid var(--border); border-radius: 14px; background: var(--card);">
                    <span class="icon-slot ${meta.class}" aria-label="${escapeHtml(meta.label)}" style="display: flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 50%;"><img src="${meta.icon}" alt="${escapeHtml(meta.label)}" style="width: 28px; height: 28px;" /></span>
                    <div style="flex:1;">
                        <div style="font-size: 1.1rem; font-weight: 700; color: var(--primary);">${escapeHtml(meta.label)}</div>
                        <div style="font-size: 0.98rem; color: var(--muted-foreground); margin-top: 0.1rem;">${riskLevel} risk, ${confidence} confidence</div>
                        <div style="font-size: 0.95rem; color: var(--muted-foreground); margin-top: 0.1rem;">Trend: ${escapeHtml(trend.charAt(0).toUpperCase() + trend.slice(1))}</div>
                    </div>
                </article>
            `;
        }
        perRiskMarkup += '</div>';
    }

    const confidence = typeof data.confidence === 'number' ? `${Math.round(data.confidence * 100)}%` : 'N/A';
    const trend = data.trend ? data.trend.charAt(0).toUpperCase() + data.trend.slice(1) : 'Steady';
    const forecastHours = data.forecast_hours || 48;

    const cards = [
        { label: 'Confidence', value: confidence },
        { label: 'Trend', value: trend },
        { label: 'Window', value: `${forecastHours}h` },
        { label: 'Baseline risk', value: typeof data.baseline_risk_score === 'number' ? `${data.baseline_risk_score.toFixed(1)}` : 'N/A' },
    ];

    const cardMarkup = cards.map(card => `
        <article class="panel" style="padding: 1rem; border: 1px solid var(--border); border-radius: 14px; background: var(--card);">
            <div style="font-size: 0.85rem; color: var(--muted-foreground);">${escapeHtml(card.label)}</div>
            <div style="font-size: 1.35rem; font-weight: 700; color: var(--primary); margin-top: 0.25rem;">${escapeHtml(card.value)}</div>
        </article>
    `).join('');

    const chartMarkup = points.length > 0 ? renderTimeline(points) : renderZoneFallback(zones);
    const pointListMarkup = points.length > 0 ? renderPointList(points) : '';

    results.innerHTML = `
        ${perRiskMarkup}
        <div class="forecast-summary-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 0.75rem; margin-top: 1rem;">
            ${cardMarkup}
        </div>
        <div style="margin-top: 1rem;">${chartMarkup}</div>
        ${pointListMarkup}
    `;
}

function renderTimeline(points) {
    const maxScore = Math.max(100, ...points.map(point => point.risk_score || 0));
    const minScore = Math.min(0, ...points.map(point => point.risk_score || 0));
    const width = 620;
    const height = 240;
    const leftPad = 48;
    const bottomPad = 38;
    const topPad = 24;
    const usableWidth = width - leftPad - 22;
    const usableHeight = height - topPad - bottomPad;

    const xStep = points.length > 1 ? usableWidth / (points.length - 1) : usableWidth;
    const coords = points.map((point, index) => {
        const x = leftPad + index * xStep;
        const normalized = (point.risk_score - minScore) / Math.max(maxScore - minScore, 1);
        const y = topPad + usableHeight - normalized * usableHeight;
        return { x, y, point };
    });

    const line = coords.map(coord => `${coord.x},${coord.y}`).join(' ');
    const area = [`${coords[0].x},${topPad + usableHeight}`, ...coords.map(coord => `${coord.x},${coord.y}`), `${coords[coords.length - 1].x},${topPad + usableHeight}`].join(' ');

    const labels = points.map((point, index) => {
        const x = leftPad + index * xStep;
        const label = point.hour_offset === 0 ? 'Now' : `+${point.hour_offset}h`;
        return `<text x="${x}" y="${height - 10}" text-anchor="middle" font-size="11" fill="var(--muted-foreground)">${escapeHtml(label)}</text>`;
    }).join('');

    const markers = coords.map(coord => {
        const color = coord.point.risk_level === 'high' ? '#d64545' : coord.point.risk_level === 'moderate' ? '#f4a261' : '#4caf7a';
        return `<circle cx="${coord.x}" cy="${coord.y}" r="5.5" fill="${color}" />`;
    }).join('');

    return `
        <section class="panel" style="padding: 1rem; background: var(--accent); border: 1px solid var(--border); border-radius: 16px;">
            <div style="font-weight: 700; color: var(--primary); margin-bottom: 0.5rem;">Forecast Timeline</div>
            <svg width="100%" viewBox="0 0 ${width} ${height}" role="img" aria-label="Forecast timeline chart">
                <line x1="${leftPad}" y1="${topPad + usableHeight}" x2="${width - 16}" y2="${topPad + usableHeight}" stroke="var(--muted)" stroke-width="1.5" />
                <line x1="${leftPad}" y1="${topPad}" x2="${leftPad}" y2="${topPad + usableHeight}" stroke="var(--muted)" stroke-width="1.5" />
                <polygon points="${area}" fill="var(--chart-1)" fill-opacity="0.18"></polygon>
                <polyline points="${line}" fill="none" stroke="var(--primary)" stroke-width="3"></polyline>
                ${markers}
                <text x="10" y="${topPad + 10}" font-size="11" fill="var(--muted-foreground)">${escapeHtml(String(maxScore.toFixed(0)))}</text>
                <text x="10" y="${topPad + usableHeight}" font-size="11" fill="var(--muted-foreground)">${escapeHtml(String(minScore.toFixed(0)))}</text>
                ${labels}
            </svg>
        </section>
    `;
}

function renderZoneFallback(zones) {
    const counts = zones.reduce(
        (acc, zone) => {
            const level = zone.risk_level || 'low';
            if (acc[level] !== undefined) {
                acc[level] += 1;
            }
            return acc;
        },
        { high: 0, moderate: 0, low: 0 },
    );

    return `
        <section class="panel" style="padding: 1rem; border: 1px solid var(--border); border-radius: 16px; background: var(--accent);">
            <div style="font-weight: 700; color: var(--primary); margin-bottom: 0.5rem;">Regional Risk Breakdown</div>
            <p style="margin: 0; color: var(--muted-foreground);">No forecast timeline points were returned, so the current active alerts are summarized instead.</p>
            <div style="display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 0.75rem;">
                <span class="badge">High: ${counts.high}</span>
                <span class="badge">Moderate: ${counts.moderate}</span>
                <span class="badge">Low: ${counts.low}</span>
            </div>
        </section>
    `;
}

function renderPointList(points) {
    const items = points.map(point => `
        <li style="display: flex; justify-content: space-between; gap: 1rem; padding: 0.65rem 0; border-bottom: 1px solid var(--border);">
            <span><strong>+${point.hour_offset}h</strong>${point.dominant_type ? ` - ${escapeHtml(point.dominant_type.replace(/_/g, ' '))}` : ''}</span>
            <span>${escapeHtml(point.risk_level)} risk, ${escapeHtml(point.risk_score.toFixed(1))}/100, ${escapeHtml(Math.round(point.confidence * 100).toString())}% confidence</span>
        </li>
    `).join('');

    return `
        <section class="panel" style="margin-top: 1rem; padding: 1rem; border: 1px solid var(--border); border-radius: 16px; background: var(--card);">
            <div style="font-weight: 700; color: var(--primary); margin-bottom: 0.5rem;">Forecast Points</div>
            <ul style="list-style: none; padding: 0; margin: 0;">${items}</ul>
        </section>
    `;
}

function escapeHtml(value) {
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

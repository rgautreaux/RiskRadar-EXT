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
        status.textContent = `Loading forecast for your location (${lat.toFixed(2)}, ${lon.toFixed(2)})…`;
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
        status.textContent = `Loading forecast for ${location}…`;
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

    if (!results || !status) return;

    if (!data) {
        status.textContent = `No forecast data available for ${locationLabel}.`;
        results.innerHTML = renderNoDataState();
        return;
    }

    const points = Array.isArray(data.forecast_points) ? data.forecast_points : [];
    const zones = Array.isArray(data.risk_zones) ? data.risk_zones : [];

    if (points.length === 0 && zones.length === 0) {
        status.textContent = `No forecast data available for ${locationLabel}.`;
        results.innerHTML = renderNoDataState();
        return;
    }

    const typeLabel = data.personalized ? 'Personalized' : 'Forecast';
    const summaryStr = data.summary ? ` — ${escapeHtml(data.summary)}` : '';
    const updatedStr = data.generated_at
        ? `<span class="fc-status-time">Updated ${escapeHtml(data.generated_at)}</span>`
        : '';

    status.innerHTML = `<span class="fc-status-badge">${escapeHtml(typeLabel)}</span><strong>${escapeHtml(locationLabel)}</strong>${summaryStr}${updatedStr}`;

    const confidence = typeof data.confidence === 'number' ? `${Math.round(data.confidence * 100)}%` : '—';
    const trend = data.trend ? data.trend.charAt(0).toUpperCase() + data.trend.slice(1) : 'Steady';
    const forecastHours = data.forecast_hours || 48;
    const baselineRisk = typeof data.baseline_risk_score === 'number' ? data.baseline_risk_score.toFixed(1) : '—';

    const statsHtml = `
        <div class="fc-stat-strip">
            <div class="fc-stat-cell">
                <p class="fc-stat-label">Confidence</p>
                <p class="fc-stat-value">${escapeHtml(confidence)}</p>
            </div>
            <div class="fc-stat-cell">
                <p class="fc-stat-label">Trend</p>
                <p class="fc-stat-value">${escapeHtml(trend)}</p>
            </div>
            <div class="fc-stat-cell">
                <p class="fc-stat-label">Window</p>
                <p class="fc-stat-value">${escapeHtml(String(forecastHours))}h</p>
            </div>
            <div class="fc-stat-cell">
                <p class="fc-stat-label">Baseline</p>
                <p class="fc-stat-value">${escapeHtml(baselineRisk)}</p>
            </div>
        </div>
    `;

    const chartHtml = points.length > 0 ? renderTimeline(points) : renderZoneFallback(zones);
    const pointListHtml = points.length > 0 ? renderPointList(points) : '';

    results.innerHTML = statsHtml + chartHtml + pointListHtml;
}

function renderNoDataState() {
    return `
        <div class="fc-empty-state">
            <div class="fc-empty-icon" aria-hidden="true">
                <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="12" y1="8" x2="12" y2="12"/>
                    <line x1="12" y1="16" x2="12.01" y2="16"/>
                </svg>
            </div>
            <p class="fc-empty-title">No forecast data available</p>
            <p class="fc-empty-body">Try a different location, or check back when new data is available.</p>
        </div>
    `;
}

function riskColor(level) {
    if (level === 'high')     return '#c23b2a';
    if (level === 'moderate') return '#b07300';
    return '#3d7a52';
}

function renderTimeline(points) {
    const maxScore = Math.max(100, ...points.map(p => p.risk_score || 0));
    const minScore = Math.min(0, ...points.map(p => p.risk_score || 0));

    const W = 620, H = 200, padL = 44, padB = 36, padT = 20, padR = 16;
    const cW = W - padL - padR;
    const cH = H - padT - padB;
    const xStep = points.length > 1 ? cW / (points.length - 1) : cW;

    const toX = i => padL + i * xStep;
    const toY = score => {
        const norm = (score - minScore) / Math.max(maxScore - minScore, 1);
        return padT + cH - norm * cH;
    };

    const coords = points.map((p, i) => ({
        x: toX(i),
        y: toY(p.risk_score || 0),
        point: p,
    }));

    const linePoints = coords.map(c => `${c.x.toFixed(1)},${c.y.toFixed(1)}`).join(' ');
    const areaPoints = [
        `${coords[0].x.toFixed(1)},${(padT + cH).toFixed(1)}`,
        ...coords.map(c => `${c.x.toFixed(1)},${c.y.toFixed(1)}`),
        `${coords[coords.length - 1].x.toFixed(1)},${(padT + cH).toFixed(1)}`,
    ].join(' ');

    const gridLines = [25, 50, 75].map(pct => {
        const y = toY(pct).toFixed(1);
        return `
            <line x1="${padL}" y1="${y}" x2="${W - padR}" y2="${y}" stroke="#33485d" stroke-width="1" stroke-dasharray="3 5" opacity="0.13"/>
            <text x="${padL - 7}" y="${(parseFloat(y) + 4).toFixed(0)}" font-size="10" fill="#33485d" opacity="0.45" text-anchor="end" font-family="'Geist Mono', monospace">${pct}</text>
        `;
    }).join('');

    const skip = points.length > 8 ? 2 : 1;
    const timeLabels = points.map((p, i) => {
        if (i % skip !== 0 && i !== points.length - 1) return '';
        const label = p.hour_offset === 0 ? 'Now' : `+${p.hour_offset}h`;
        return `<text x="${toX(i).toFixed(1)}" y="${H - 6}" text-anchor="middle" font-size="10" fill="#33485d" opacity="0.52" font-family="'Geist Mono', monospace">${escapeHtml(label)}</text>`;
    }).join('');

    const dots = coords.map(c => {
        const color = riskColor(c.point.risk_level);
        return `<circle cx="${c.x.toFixed(1)}" cy="${c.y.toFixed(1)}" r="4.5" fill="${color}" stroke="#fff5e6" stroke-width="2"/>`;
    }).join('');

    return `
        <section class="fc-chart-section">
            <p class="fc-section-label">Forecast Timeline</p>
            <svg width="100%" viewBox="0 0 ${W} ${H}" role="img" aria-label="48-hour risk forecast timeline">
                ${gridLines}
                <line x1="${padL}" y1="${padT}" x2="${padL}" y2="${padT + cH}" stroke="#33485d" stroke-width="1" opacity="0.18"/>
                <line x1="${padL}" y1="${padT + cH}" x2="${W - padR}" y2="${padT + cH}" stroke="#33485d" stroke-width="1" opacity="0.18"/>
                <polygon points="${areaPoints}" fill="#3d7a52" fill-opacity="0.1"/>
                <polyline points="${linePoints}" fill="none" stroke="#3d7a52" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                ${dots}
                ${timeLabels}
            </svg>
            <div class="fc-chart-legend">
                <span class="fc-legend-item">
                    <span class="fc-legend-dot" style="background:#c23b2a;"></span>High
                </span>
                <span class="fc-legend-item">
                    <span class="fc-legend-dot" style="background:#b07300;"></span>Moderate
                </span>
                <span class="fc-legend-item">
                    <span class="fc-legend-dot" style="background:#3d7a52;"></span>Low
                </span>
            </div>
        </section>
    `;
}

function renderZoneFallback(zones) {
    const counts = zones.reduce(
        (acc, zone) => {
            const level = zone.risk_level || 'low';
            if (acc[level] !== undefined) acc[level] += 1;
            return acc;
        },
        { high: 0, moderate: 0, low: 0 },
    );

    return `
        <section class="fc-zone-section">
            <p class="fc-section-label">Regional Risk Breakdown</p>
            <p class="fc-zone-desc">No timeline points were returned. Showing a summary of current active alerts instead.</p>
            <div class="fc-zone-pills">
                <span class="fc-zone-pill fc-risk-high">${counts.high} High</span>
                <span class="fc-zone-pill fc-risk-moderate">${counts.moderate} Moderate</span>
                <span class="fc-zone-pill fc-risk-low">${counts.low} Low</span>
            </div>
        </section>
    `;
}

function renderPointList(points) {
    const items = points.map(point => {
        const level = point.risk_level || 'low';
        const badgeClass = level === 'high' ? 'fc-risk-high' : level === 'moderate' ? 'fc-risk-moderate' : 'fc-risk-low';
        const label = point.hour_offset === 0 ? 'Now' : `+${point.hour_offset}h`;
        const typeStr = point.dominant_type ? point.dominant_type.replace(/_/g, ' ') : 'mixed';
        const score = typeof point.risk_score === 'number' ? `${point.risk_score.toFixed(1)}/100` : '';
        return `
            <li class="fc-point-item">
                <span class="fc-point-hour">${escapeHtml(label)}</span>
                <span class="fc-point-type">${escapeHtml(typeStr)}</span>
                <span class="fc-point-score">${escapeHtml(score)}</span>
                <span class="fc-risk-badge ${badgeClass}">${escapeHtml(level)}</span>
            </li>
        `;
    }).join('');

    return `
        <section class="fc-points-section">
            <p class="fc-section-label">Hourly Breakdown</p>
            <ul class="fc-point-list">${items}</ul>
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

// forecast-location.js
// Handles geolocation and manual location input for forecast UI

document.addEventListener('DOMContentLoaded', function() {
    const locationForm = document.getElementById('forecast-location-form');
    const locationInput = document.getElementById('forecast-location-input');
    const useMyLocationBtn = document.getElementById('use-my-location-btn');
    const forecastStatus = document.getElementById('forecast-location-status');

    // Try to get user's location on load
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            fetchForecastByCoords(position.coords.latitude, position.coords.longitude);
        }, function() {
            forecastStatus.textContent = 'Location permission denied. Enter a location.';
        });
    } else {
        forecastStatus.textContent = 'Geolocation not supported. Enter a location.';
    }

    // Manual location form submit
    if (locationForm) {
        locationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const value = locationInput.value.trim();
            if (value.length === 0) return;
            fetchForecastByLocation(value);
        });
    }

    // Use my location button
    if (useMyLocationBtn) {
        useMyLocationBtn.addEventListener('click', function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    fetchForecastByCoords(position.coords.latitude, position.coords.longitude);
                }, function() {
                    forecastStatus.textContent = 'Location permission denied.';
                });
            }
        });
    }
});

function fetchForecastByCoords(lat, lon) {
    const statusDiv = document.getElementById('forecast-location-status');
    statusDiv.textContent = `Loading forecast for your location (${lat.toFixed(2)}, ${lon.toFixed(2)})...`;
    fetch(`/api/v1/forecast?lat=${lat}&lon=${lon}`)
        .then(res => res.json())
        .then(data => renderForecast(data, `Your Location (${lat.toFixed(2)}, ${lon.toFixed(2)})`))
        .catch(() => {
            statusDiv.textContent = 'Failed to load forecast.';
        });
}


function renderForecast(data, locationLabel) {
    const statusDiv = document.getElementById('forecast-location-status');
    const timelineDivId = 'forecast-timeline';
    let timelineDiv = document.getElementById(timelineDivId);
    if (!timelineDiv) {
        timelineDiv = document.createElement('div');
        timelineDiv.id = timelineDivId;
        statusDiv.parentNode.insertBefore(timelineDiv, statusDiv.nextSibling);
    }
    if (!data || !data.risk_zones || data.risk_zones.length === 0) {
        statusDiv.textContent = `No forecast data available for ${locationLabel}.`;
        timelineDiv.innerHTML = '';
        return;
    }
    // Summarize risk levels and group by type
    const riskCounts = { high: 0, moderate: 0, low: 0 };
    const riskTypes = {};
    data.risk_zones.forEach(z => {
        if (z.risk_level in riskCounts) riskCounts[z.risk_level]++;
        // Group by alert_type if available (backend should provide for best results)
        const type = z.alert_type || z.type || 'Other';
        if (!riskTypes[type]) riskTypes[type] = { high: 0, moderate: 0, low: 0 };
        if (z.risk_level in riskTypes[type]) riskTypes[type][z.risk_level]++;
    });
    statusDiv.innerHTML = `Forecast for <b>${locationLabel}</b>:<br>
        High risk: <b>${riskCounts.high}</b> | Moderate: <b>${riskCounts.moderate}</b> | Low: <b>${riskCounts.low}</b><br>
        <span style='font-size:0.95em;color:var(--muted-foreground)'>Updated: ${data.generated_at}</span>`;

    // Timeline SVG: grouped by risk type
    let svg = `<svg width="100%" height="${Object.keys(riskTypes).length * 60 + 40}" viewBox="0 0 560 ${Object.keys(riskTypes).length * 60 + 40}" style="background: var(--accent); border-radius: 8px; margin-top: 1rem;">
        <text x="20" y="30" font-size="14" fill="var(--primary)">Risk by Type</text>`;
    const barWidth = 50, gap = 20, baseY = 50, maxBar = 50;
    const levels = ['high', 'moderate', 'low'];
    let row = 0;
    Object.entries(riskTypes).forEach(([type, counts]) => {
        const y = baseY + row * 60;
        svg += `<text x="20" y="${y + 25}" font-size="13" fill="var(--primary)">${type.charAt(0).toUpperCase() + type.slice(1)}</text>`;
        levels.forEach((level, i) => {
            const count = counts[level];
            const barHeight = Math.min(maxBar, count * 10);
            const color = level === 'high' ? '#e63946' : (level === 'moderate' ? '#f4a261' : '#43aa8b');
            svg += `<rect x="${150 + i * (barWidth + gap)}" y="${y + 40 - barHeight}" width="${barWidth}" height="${barHeight}" fill="${color}" rx="6" />`;
            svg += `<text x="${150 + i * (barWidth + gap) + barWidth/2}" y="${y + 60}" font-size="12" fill="var(--muted-foreground)" text-anchor="middle">${level.charAt(0).toUpperCase() + level.slice(1)}</text>`;
            svg += `<text x="${150 + i * (barWidth + gap) + barWidth/2}" y="${y + 35 - barHeight}" font-size="12" fill="${color}" text-anchor="middle">${count}</text>`;
        });
        row++;
    });
    svg += '</svg>';
    timelineDiv.innerHTML = svg;


    // Travel advice (risk-type and severity specific)
    const adviceTemplates = {
        weather: {
            high: {
                icon: '🌩️',
                text: 'Severe weather expected. Pack rain gear, waterproof shoes, and check for local warnings. Delay travel if possible.'
            },
            moderate: {
                icon: '🌦️',
                text: 'Weather may be unsettled. Bring a light jacket or umbrella.'
            },
            low: {
                icon: '☀️',
                text: 'Weather is favorable. Standard travel preparations are sufficient.'
            }
        },
        fire: {
            high: {
                icon: '🔥',
                text: 'Wildfire risk is high. Pack N95 masks, check evacuation routes, and monitor local alerts.'
            },
            moderate: {
                icon: '🔥',
                text: 'Fire risk present. Avoid outdoor burning and stay alert.'
            },
            low: {
                icon: '🔥',
                text: 'Fire risk is low. No special precautions needed.'
            }
        },
        flood: {
            high: {
                icon: '🌊',
                text: 'Flooding possible. Avoid low-lying areas, pack waterproof bags, and check evacuation plans.'
            },
            moderate: {
                icon: '🌊',
                text: 'Flood risk moderate. Monitor weather and avoid risky routes.'
            },
            low: {
                icon: '🌊',
                text: 'Flood risk is low.'
            }
        },
        'air quality': {
            high: {
                icon: '😷',
                text: 'Air quality is poor. Limit outdoor activity, wear a mask, and keep windows closed.'
            },
            moderate: {
                icon: '😷',
                text: 'Air quality is moderate. Sensitive groups should take precautions.'
            },
            low: {
                icon: '😷',
                text: 'Air quality is good.'
            }
        },
        pollen: {
            high: {
                icon: '🌾',
                text: 'High pollen count. Take allergy medication and limit outdoor exposure.'
            },
            moderate: {
                icon: '🌾',
                text: 'Moderate pollen. Sensitive individuals should prepare.'
            },
            low: {
                icon: '🌾',
                text: 'Low pollen count.'
            }
        },
        earthquake: {
            high: {
                icon: '🌎',
                text: 'Earthquake risk is elevated. Review emergency plans and secure loose items.'
            },
            moderate: {
                icon: '🌎',
                text: 'Some seismic activity possible. Stay alert.'
            },
            low: {
                icon: '🌎',
                text: 'Earthquake risk is low.'
            }
        },
        Other: {
            high: { icon: '⚠️', text: 'High risk detected. Take extra precautions.' },
            moderate: { icon: '🛈', text: 'Moderate risk. Prepare for possible disruptions.' },
            low: { icon: '✅', text: 'Low risk. Standard preparations are sufficient.' }
        }
    };

    let adviceHtml = '<div style="margin-top:1rem;font-size:1.05em;color:var(--primary)"><b>Travel Advice:</b><ul style="margin:0;padding-left:1.2em;">';
    Object.entries(riskTypes).forEach(([type, counts]) => {
        let sev = 'low';
        if (counts.high > 0) sev = 'high';
        else if (counts.moderate > 0) sev = 'moderate';
        const tpl = (adviceTemplates[type.toLowerCase()] || adviceTemplates.Other)[sev];
        adviceHtml += `<li>${tpl.icon} <b>${type.charAt(0).toUpperCase() + type.slice(1)}</b>: ${tpl.text}`;
        // Example checklist for high risk
        if (sev === 'high') {
            adviceHtml += '<ul style="margin:0.3em 0 0.5em 1.2em;font-size:0.97em;">';
            if (type.toLowerCase() === 'fire') adviceHtml += '<li>Pack N95 mask</li><li>Check evacuation routes</li><li>Monitor local alerts</li>';
            if (type.toLowerCase() === 'weather') adviceHtml += '<li>Pack rain gear</li><li>Delay travel if possible</li>';
            if (type.toLowerCase() === 'flood') adviceHtml += '<li>Avoid low-lying areas</li><li>Pack waterproof bags</li>';
            if (type.toLowerCase() === 'air quality') adviceHtml += '<li>Wear a mask</li><li>Limit outdoor activity</li>';
            if (type.toLowerCase() === 'pollen') adviceHtml += '<li>Take allergy medication</li>';
            if (type.toLowerCase() === 'earthquake') adviceHtml += '<li>Review emergency plans</li><li>Secure loose items</li>';
            adviceHtml += '</ul>';
        }
        adviceHtml += '</li>';
    });
    adviceHtml += '</ul></div>';
    timelineDiv.innerHTML += adviceHtml;
}
    // Travel advice (simple rules based on risk)
    let advice = '';
    if (riskCounts.high > 0) {
        advice += '⚠️ <b>High risk detected.</b> Consider postponing travel or taking extra precautions. Pack emergency supplies, weather-appropriate clothing, and stay updated on alerts.';
    } else if (riskCounts.moderate > 0) {
        advice += '🛈 <b>Moderate risk.</b> Prepare for possible disruptions. Bring rain gear, masks (for air quality), and check local advisories.';
    } else {
        advice += '✅ <b>Low risk.</b> Conditions are generally safe. Pack as usual, but check for updates before travel.';
    }
    timelineDiv.innerHTML += `<div style="margin-top:1rem;font-size:1.05em;color:var(--primary)">${advice}</div>`;
}

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

function fetchForecastByLocation(location) {
    const statusDiv = document.getElementById('forecast-location-status');
    statusDiv.textContent = `Loading forecast for ${location}...`;
    fetch(`/api/v1/forecast?location=${encodeURIComponent(location)}`)
        .then(res => res.json())
        .then(data => renderForecast(data, location))
        .catch(() => {
            statusDiv.textContent = 'Failed to load forecast.';
        });
}

function renderForecast(data, locationLabel) {
    const statusDiv = document.getElementById('forecast-location-status');
    if (!data || !data.risk_zones || data.risk_zones.length === 0) {
        statusDiv.textContent = `No forecast data available for ${locationLabel}.`;
        return;
    }
    // Summarize risk levels
    const riskCounts = { high: 0, moderate: 0, low: 0 };
    data.risk_zones.forEach(z => {
        if (z.risk_level in riskCounts) riskCounts[z.risk_level]++;
    });
    statusDiv.innerHTML = `Forecast for <b>${locationLabel}</b>:<br>
        High risk: <b>${riskCounts.high}</b> | Moderate: <b>${riskCounts.moderate}</b> | Low: <b>${riskCounts.low}</b><br>
        <span style='font-size:0.95em;color:var(--muted-foreground)'>Updated: ${data.generated_at}</span>`;
}

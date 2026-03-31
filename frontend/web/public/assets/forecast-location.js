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
    // TODO: Implement AJAX call to backend with lat/lon
    // Example: /api/forecast?lat=...&lon=...
    document.getElementById('forecast-location-status').textContent = `Showing forecast for your location (${lat.toFixed(2)}, ${lon.toFixed(2)})`;
    // TODO: Render forecast data
}

function fetchForecastByLocation(location) {
    // TODO: Implement AJAX call to backend with location string
    // Example: /api/forecast?location=...
    document.getElementById('forecast-location-status').textContent = `Showing forecast for ${location}`;
    // TODO: Render forecast data
}

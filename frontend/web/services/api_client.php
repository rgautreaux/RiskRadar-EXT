// Stage 3: Map Data API Client
function rr_api_get_map_alerts(array $config, array $query = []): array
{
    // GET /api/v1/alerts/map
    return rr_http_request($config, 'GET', 'alerts/map', $query);
}

function rr_api_get_map_risk_overlay(array $config, array $query = []): array
{
    // GET /api/v1/risk/map
    return rr_http_request($config, 'GET', 'risk/map', $query);
}
<?php

function rr_api_url(array $config, string $path, array $query = []): string
{
    $baseUrl = rtrim($config['api']['base_url'], '/');
    $prefix = trim($config['api']['prefix'], '/');
    $resource = ltrim($path, '/');

    $url = $baseUrl . '/' . $prefix . '/' . $resource;
    $query = array_filter($query, function ($value) {
        return $value !== null && $value !== '';
    });

    if ($query) {
        $url .= '?' . http_build_query($query);
    }

    return $url;
}

function rr_fallback_result(mixed $fallbackData, string $message, ?int $status = null): array
{
    return [
        'ok' => false,
        'status' => $status,
        'data' => $fallbackData,
        'message' => $message,
    ];
    function rr_api_get_forecast(array $config, array $query = []): array
    {
        // GET /api/v1/forecast
        return rr_http_request($config, 'GET', 'forecast', $query);
    }
}

function rr_success_result(mixed $data, ?int $status = null): array
{
    return [
        'ok' => true,
        'status' => $status,
        'data' => $data,
        'message' => null,
    ];
}

function rr_safe_string(mixed $value, string $default = ''): string
{
    if (is_string($value)) {
        return $value;
    }

    if (is_int($value) || is_float($value)) {
        return (string) $value;
    }

    if (is_bool($value)) {
        return $value ? 'true' : 'false';
    }

    return $default;
}

function rr_safe_nullable_string(mixed $value): ?string
{
    if ($value === null) {
        return null;
    }

    if (is_string($value)) {
        return $value;
    }

    if (is_int($value) || is_float($value)) {
        return (string) $value;
    }

    if (is_bool($value)) {
        return $value ? 'true' : 'false';
    }

    return null;
}

function rr_safe_nullable_float(mixed $value): ?float
{
    if ($value === null || $value === '') {
        return null;
    }

    return is_numeric($value) ? (float) $value : null;
}

function rr_http_request(array $config, string $method, string $path, array $query = [], ?array $body = null): array
{
    $url = rr_api_url($config, $path, $query);
    $timeout = (float) ($config['api']['timeout'] ?? 5.0);
    $method = strtoupper($method);
    $headers = ['Accept: application/json'];
    $payload = null;

    if ($body !== null) {
        $payload = json_encode($body);
        if ($payload === false) {
            return rr_fallback_result(null, 'Failed to encode request body as JSON.');
        }

        $headers[] = 'Content-Type: application/json';
    }

    if (function_exists('curl_init')) {
        $handle = curl_init($url);
        curl_setopt_array($handle, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_CUSTOMREQUEST => $method,
            CURLOPT_HTTPHEADER => $headers,
            CURLOPT_TIMEOUT => $timeout,
            CURLOPT_CONNECTTIMEOUT => $timeout,
            CURLOPT_FOLLOWLOCATION => false,
            CURLOPT_HEADER => true,
        ]);

        if ($payload !== null) {
            curl_setopt($handle, CURLOPT_POSTFIELDS, $payload);
        }

        $rawResponse = curl_exec($handle);
        $curlError = curl_error($handle);
        $status = (int) curl_getinfo($handle, CURLINFO_HTTP_CODE);
        $headerSize = (int) curl_getinfo($handle, CURLINFO_HEADER_SIZE);
        curl_close($handle);

        if ($rawResponse === false) {
            return rr_fallback_result(null, 'The backend API is unavailable right now. Try again shortly.');
        }

        if ($curlError !== '') {
            return rr_fallback_result(null, 'The backend API request timed out or failed.');
        }

        $bodyText = substr($rawResponse, $headerSize);
        $decoded = json_decode($bodyText, true);

        if ($status < 200 || $status >= 300) {
            return rr_fallback_result($decoded, 'The backend returned an error response.', $status);
        }

        if ($bodyText !== '' && $decoded === null) {
            return rr_fallback_result(null, 'The backend returned malformed JSON.', $status);
        }

        return rr_success_result($decoded, $status);
    }

    $contextOptions = [
        'http' => [
            'method' => $method,
            'header' => implode("\r\n", $headers),
            'timeout' => $timeout,
            'ignore_errors' => true,
        ],
    ];

    if ($payload !== null) {
        $contextOptions['http']['content'] = $payload;
    }

    $context = stream_context_create($contextOptions);
    $bodyText = @file_get_contents($url, false, $context);
    $status = null;

    if (!empty($http_response_header[0]) && preg_match('/\s(\d{3})\s/', $http_response_header[0], $matches)) {
        $status = (int) $matches[1];
    }

    if ($bodyText === false) {
        return rr_fallback_result(null, 'The backend API request timed out or failed.', $status);
    }

    $decoded = json_decode($bodyText, true);
    if (($status !== null && ($status < 200 || $status >= 300))) {
        return rr_fallback_result($decoded, 'The backend returned an error response.', $status);
    }

    if ($bodyText !== '' && $decoded === null) {
        return rr_fallback_result(null, 'The backend returned malformed JSON.', $status);
    }

    return rr_success_result($decoded, $status);
}

function rr_normalize_alert(?array $alert): array
{
    if (!is_array($alert)) {
        return [
            'id' => 0,
            'source' => 'Unknown',
            'source_id' => null,
            'alert_type' => 'other',
            'severity' => 'low',
            'title' => 'Untitled alert',
            'description' => null,
            'latitude' => null,
            'longitude' => null,
            'location_name' => null,
            'event_start' => null,
            'event_end' => null,
            'fetched_at' => '',
            'created_at' => '',
        ];
    }

    return [
        'id' => (int) ($alert['id'] ?? 0),
        'source' => rr_safe_string($alert['source'] ?? null, 'Unknown'),
        'source_id' => rr_safe_nullable_string($alert['source_id'] ?? null),
        'alert_type' => rr_safe_string($alert['alert_type'] ?? null, 'other'),
        'severity' => rr_safe_string($alert['severity'] ?? null, 'low'),
        'title' => rr_safe_string($alert['title'] ?? null, 'Untitled alert'),
        'description' => rr_safe_nullable_string($alert['description'] ?? null),
        'latitude' => rr_safe_nullable_float($alert['latitude'] ?? null),
        'longitude' => rr_safe_nullable_float($alert['longitude'] ?? null),
        'location_name' => rr_safe_nullable_string($alert['location_name'] ?? null),
        'event_start' => rr_safe_nullable_string($alert['event_start'] ?? null),
        'event_end' => rr_safe_nullable_string($alert['event_end'] ?? null),
        'fetched_at' => rr_safe_string($alert['fetched_at'] ?? null),
        'created_at' => rr_safe_string($alert['created_at'] ?? null),
        'priority_score' => rr_safe_nullable_float($alert['priority_score'] ?? null),
        'urgency_label' => rr_safe_nullable_string($alert['urgency_label'] ?? null),
        'priority_explanation' => rr_safe_nullable_string($alert['priority_explanation'] ?? null),
    ];
}

function rr_normalize_risk_score(?array $payload): ?array
{
    if (!is_array($payload)) {
        return null;
    }

    $score = rr_safe_nullable_float($payload['score'] ?? null);
    $baseScore = rr_safe_nullable_float($payload['base_score'] ?? null);
    $multiplier = rr_safe_nullable_float($payload['multiplier'] ?? null);

    return [
        'user_id' => (int) ($payload['user_id'] ?? 0),
        'score' => $score,
        'level' => rr_safe_string($payload['level'] ?? null, 'low'),
        'base_score' => $baseScore,
        'multiplier' => $multiplier,
    ];
}

function rr_normalize_summary(?array $summary): ?array
{
    if (!is_array($summary)) {
        return null;
    }

    return [
        'id' => (int) ($summary['id'] ?? 0),
        'title' => rr_safe_string($summary['title'] ?? null, 'Untitled summary'),
        'content' => rr_safe_string($summary['content'] ?? null),
        'summary_type' => rr_safe_string($summary['summary_type'] ?? null, 'general'),
        'region' => rr_safe_nullable_string($summary['region'] ?? null),
        'generated_at' => rr_safe_string($summary['generated_at'] ?? null),
        'model_used' => rr_safe_nullable_string($summary['model_used'] ?? null),
    ];
}

function rr_normalize_user(?array $user): ?array
{
    if (!is_array($user)) {
        return null;
    }

    return [
        'id' => (int) ($user['id'] ?? 0),
        'display_name' => rr_safe_nullable_string($user['display_name'] ?? null),
        'email' => rr_safe_nullable_string($user['email'] ?? null),
        'zip_code' => rr_safe_nullable_string($user['zip_code'] ?? null),
        'alert_types' => rr_safe_nullable_string($user['alert_types'] ?? null),
        'notify_severity' => rr_safe_nullable_string($user['notify_severity'] ?? null),
        'created_at' => rr_safe_string($user['created_at'] ?? null),
    ];
}

function rr_fetch_alert_stats(array $config): array
{
    $result = rr_http_request($config, 'GET', 'alerts/stats');
    $fallback = ['total' => 0, 'by_type' => [], 'by_severity' => []];

    if (!$result['ok'] || !is_array($result['data'])) {
        return rr_fallback_result($fallback, 'Alert stats are unavailable. Showing a zero-state view.', $result['status'] ?? null);
    }

    $data = $result['data'];
    return rr_success_result([
        'total' => (int) ($data['total'] ?? 0),
        'by_type' => is_array($data['by_type'] ?? null) ? $data['by_type'] : [],
        'by_severity' => is_array($data['by_severity'] ?? null) ? $data['by_severity'] : [],
    ], $result['status']);
}

function rr_fetch_alerts(array $config, array $filters = []): array
{
    $result = rr_http_request($config, 'GET', 'alerts', $filters);
    if (!$result['ok'] || !is_array($result['data'])) {
        return rr_fallback_result([], 'Alerts could not be loaded. Showing an empty list instead.', $result['status'] ?? null);
    }

    $alerts = array_map('rr_normalize_alert', $result['data']);
    return rr_success_result($alerts, $result['status']);
}


function rr_fetch_user_risk_score(array $config, int $userId): array
{
    $result = rr_http_request($config, 'GET', 'users/' . $userId . '/risk-score');
    if (!$result['ok']) {
        return rr_fallback_result(null, 'Risk scoring data is unavailable right now.', $result['status'] ?? null);
    }

    return rr_success_result(rr_normalize_risk_score(is_array($result['data']) ? $result['data'] : null), $result['status']);
}

function rr_fetch_latest_summary(array $config): array
{
    $result = rr_http_request($config, 'GET', 'summaries/latest');
    if (!$result['ok']) {
        return rr_fallback_result(null, 'No latest summary is available right now.', $result['status'] ?? null);
    }

    return rr_success_result(rr_normalize_summary($result['data']), $result['status']);
}

function rr_fetch_summaries(array $config, array $filters = []): array
{
    $result = rr_http_request($config, 'GET', 'summaries', $filters);
    if (!$result['ok'] || !is_array($result['data'])) {
        return rr_fallback_result([], 'Summaries could not be loaded. Showing an empty state.', $result['status'] ?? null);
    }

    $summaries = array_map('rr_normalize_summary', $result['data']);
    return rr_success_result(array_values(array_filter($summaries, 'is_array')), $result['status']);
}

function rr_register_user(array $config, array $payload): array
{
    $result = rr_http_request($config, 'POST', 'users/register', [], $payload);
    if (!$result['ok']) {
        $message = ($result['status'] ?? 0) === 400
            ? 'That email address is already registered or the form data is invalid.'
            : 'Registration failed. Please verify the backend is running and try again.';

        return rr_fallback_result(rr_normalize_user(is_array($result['data']) ? $result['data'] : null), $message, $result['status'] ?? null);
    }

    return rr_success_result(rr_normalize_user($result['data']), $result['status']);
}

function rr_fetch_alert_by_id(array $config, int $id): array
{
    $result = rr_http_request($config, 'GET', 'alerts/' . $id);
    if (!$result['ok']) {
        $message = ($result['status'] ?? 0) === 404
            ? 'That alert was not found in the backend.'
            : 'The alert could not be loaded. The backend may be unavailable.';
        return rr_fallback_result(null, $message, $result['status'] ?? null);
    }
    return rr_success_result(rr_normalize_alert($result['data']), $result['status']);
}

function rr_fetch_summary_by_id(array $config, int $id): array
{
    $result = rr_http_request($config, 'GET', 'summaries/' . $id);
    if (!$result['ok']) {
        $message = ($result['status'] ?? 0) === 404
            ? 'That summary was not found in the backend.'
            : 'The summary could not be loaded. The backend may be unavailable.';
        return rr_fallback_result(null, $message, $result['status'] ?? null);
    }
    return rr_success_result(rr_normalize_summary($result['data']), $result['status']);
}

function rr_update_preferences(array $config, int $userId, array $payload): array
{
    $result = rr_http_request($config, 'PUT', 'users/' . $userId . '/preferences', [], $payload);
    if (!$result['ok']) {
        $message = ($result['status'] ?? 0) === 404
            ? 'That user ID does not exist in the backend yet.'
            : 'Preference update failed. Please verify the backend is running and try again.';

        return rr_fallback_result(rr_normalize_user(is_array($result['data']) ? $result['data'] : null), $message, $result['status'] ?? null);
    }

    return rr_success_result(rr_normalize_user($result['data']), $result['status']);
}

function rr_fetch_prioritized_alerts(array $config, int $userId, array $params = []): array
{
    $query = array_filter([
        'radius_km' => $params['radius_km'] ?? null,
        'limit' => $params['limit'] ?? null,
    ], function ($v) { return $v !== null && $v !== ''; });

    $result = rr_http_request($config, 'GET', 'alerts/prioritized/' . $userId, $query);
    if (!$result['ok'] || !is_array($result['data'])) {
        return rr_fallback_result(
            ['user_id' => $userId, 'total_nearby' => 0, 'alerts' => [], 'computed_at' => ''],
            'Prioritized alerts could not be loaded. The backend may be unavailable or user location is not set.',
            $result['status'] ?? null,
        );
    }

    $data = $result['data'];
    $alerts = is_array($data['alerts'] ?? null) ? array_map('rr_normalize_prioritized_alert', $data['alerts']) : [];

    return rr_success_result([
        'user_id' => (int) ($data['user_id'] ?? $userId),
        'total_nearby' => (int) ($data['total_nearby'] ?? 0),
        'alerts' => $alerts,
        'computed_at' => rr_safe_string($data['computed_at'] ?? null),
    ], $result['status']);
}

function rr_normalize_prioritized_alert(?array $alert): array
{
    if (!is_array($alert)) {
        return [
            'alert_id' => 0,
            'source' => 'Unknown',
            'alert_type' => 'other',
            'severity' => 'low',
            'title' => 'Untitled alert',
            'description' => null,
            'location_name' => null,
            'fetched_at' => '',
            'priority_score' => 0.0,
            'priority_level' => 'low',
            'distance_km' => 0.0,
            'priority_factors' => ['distance' => 0, 'severity' => 0, 'sensitivity' => 0, 'recency' => 0],
        ];
    }

    return [
        'alert_id' => (int) ($alert['alert_id'] ?? 0),
        'source' => rr_safe_string($alert['source'] ?? null, 'Unknown'),
        'source_id' => rr_safe_nullable_string($alert['source_id'] ?? null),
        'alert_type' => rr_safe_string($alert['alert_type'] ?? null, 'other'),
        'severity' => rr_safe_string($alert['severity'] ?? null, 'low'),
        'title' => rr_safe_string($alert['title'] ?? null, 'Untitled alert'),
        'description' => rr_safe_nullable_string($alert['description'] ?? null),
        'latitude' => rr_safe_nullable_float($alert['latitude'] ?? null),
        'longitude' => rr_safe_nullable_float($alert['longitude'] ?? null),
        'location_name' => rr_safe_nullable_string($alert['location_name'] ?? null),
        'event_start' => rr_safe_nullable_string($alert['event_start'] ?? null),
        'event_end' => rr_safe_nullable_string($alert['event_end'] ?? null),
        'fetched_at' => rr_safe_string($alert['fetched_at'] ?? null),
        'created_at' => rr_safe_string($alert['created_at'] ?? null),
        'priority_score' => is_numeric($alert['priority_score'] ?? null) ? (float) $alert['priority_score'] : 0.0,
        'priority_level' => rr_safe_string($alert['priority_level'] ?? null, 'low'),
        'distance_km' => is_numeric($alert['distance_km'] ?? null) ? round((float) $alert['distance_km'], 1) : 0.0,
        'priority_factors' => is_array($alert['priority_factors'] ?? null) ? $alert['priority_factors'] : ['distance' => 0, 'severity' => 0, 'sensitivity' => 0, 'recency' => 0],
    ];
}

function rr_fetch_risk_score(array $config, int $userId, array $params = []): array
{
    $query = array_filter([
        'radius_km' => $params['radius_km'] ?? null,
    ], function ($v) { return $v !== null && $v !== ''; });

    $result = rr_http_request($config, 'GET', 'risk/score/' . $userId, $query);
    if (!$result['ok'] || !is_array($result['data'])) {
        return rr_fallback_result(
            null,
            'Risk score could not be loaded. Ensure your location is set in your profile.',
            $result['status'] ?? null,
        );
    }

    return rr_success_result($result['data'], $result['status']);
}
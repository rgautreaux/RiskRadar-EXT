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

function rr_http_request(array $config, string $method, string $path, array $query = [], ?array $body = null): array
{
    $url = rr_api_url($config, $path, $query);
    $timeout = (float) ($config['api']['timeout'] ?? 5.0);
    $method = strtoupper($method);
    $headers = ['Accept: application/json'];
    $payload = null;

    if ($body !== null) {
        $payload = json_encode($body);
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
    return [
        'id' => (int) ($alert['id'] ?? 0),
        'source' => (string) ($alert['source'] ?? 'Unknown'),
        'source_id' => $alert['source_id'] ?? null,
        'alert_type' => (string) ($alert['alert_type'] ?? 'other'),
        'severity' => (string) ($alert['severity'] ?? 'low'),
        'title' => (string) ($alert['title'] ?? 'Untitled alert'),
        'description' => $alert['description'] ?? null,
        'latitude' => isset($alert['latitude']) ? (float) $alert['latitude'] : null,
        'longitude' => isset($alert['longitude']) ? (float) $alert['longitude'] : null,
        'location_name' => $alert['location_name'] ?? null,
        'event_start' => $alert['event_start'] ?? null,
        'event_end' => $alert['event_end'] ?? null,
        'fetched_at' => (string) ($alert['fetched_at'] ?? ''),
        'created_at' => (string) ($alert['created_at'] ?? ''),
    ];
}

function rr_normalize_summary(?array $summary): ?array
{
    if (!is_array($summary)) {
        return null;
    }

    return [
        'id' => (int) ($summary['id'] ?? 0),
        'title' => (string) ($summary['title'] ?? 'Untitled summary'),
        'content' => (string) ($summary['content'] ?? ''),
        'summary_type' => (string) ($summary['summary_type'] ?? 'general'),
        'region' => $summary['region'] ?? null,
        'generated_at' => (string) ($summary['generated_at'] ?? ''),
        'model_used' => $summary['model_used'] ?? null,
    ];
}

function rr_normalize_user(?array $user): ?array
{
    if (!is_array($user)) {
        return null;
    }

    return [
        'id' => (int) ($user['id'] ?? 0),
        'display_name' => $user['display_name'] ?? null,
        'email' => $user['email'] ?? null,
        'zip_code' => $user['zip_code'] ?? null,
        'alert_types' => $user['alert_types'] ?? null,
        'notify_severity' => $user['notify_severity'] ?? null,
        'created_at' => (string) ($user['created_at'] ?? ''),
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
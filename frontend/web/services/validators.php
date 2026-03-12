<?php

function rr_allowed_alert_types(): array
{
    return ['air_quality', 'earthquake', 'flood', 'heat', 'other', 'pollution', 'storm', 'water', 'weather', 'wildfire'];
}

function rr_allowed_severities(): array
{
    return ['low', 'medium', 'moderate', 'high', 'severe', 'extreme'];
}

function rr_read_query_string(string $key, int $maxLength = 80): ?string
{
    if (!isset($_GET[$key])) {
        return null;
    }

    $value = trim((string) $_GET[$key]);
    if ($value === '') {
        return null;
    }

    return substr($value, 0, $maxLength);
}

function rr_read_query_int(string $key, int $default, int $min, int $max): int
{
    $value = filter_input(INPUT_GET, $key, FILTER_VALIDATE_INT);
    if ($value === false || $value === null) {
        return $default;
    }

    return max($min, min($max, $value));
}

function rr_collect_alert_filters(): array
{
    $filters = [
        'alert_type' => rr_read_query_string('alert_type'),
        'severity' => rr_read_query_string('severity'),
        'source' => rr_read_query_string('source'),
        'limit' => rr_read_query_int('limit', 20, 1, 200),
        'offset' => rr_read_query_int('offset', 0, 0, 5000),
    ];

    if ($filters['alert_type'] && !in_array($filters['alert_type'], rr_allowed_alert_types(), true)) {
        $filters['alert_type'] = null;
    }

    if ($filters['severity'] && !in_array(strtolower($filters['severity']), rr_allowed_severities(), true)) {
        $filters['severity'] = null;
    }

    return $filters;
}

function rr_collect_summary_filters(): array
{
    return [
        'summary_type' => rr_read_query_string('summary_type'),
        'limit' => rr_read_query_int('limit', 10, 1, 50),
    ];
}

function rr_validate_registration(array $post): array
{
    $data = [
        'display_name' => trim((string) ($post['display_name'] ?? '')),
        'email' => trim((string) ($post['email'] ?? '')),
        'password' => (string) ($post['password'] ?? ''),
        'zip_code' => trim((string) ($post['zip_code'] ?? '')),
    ];
    $errors = [];

    if ($data['display_name'] === '') {
        $errors['display_name'] = 'Display name is required.';
    }

    if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
        $errors['email'] = 'Enter a valid email address.';
    }

    if (strlen($data['password']) < 8) {
        $errors['password'] = 'Password must be at least 8 characters.';
    }

    if ($data['zip_code'] !== '' && !preg_match('/^\d{5}$/', $data['zip_code'])) {
        $errors['zip_code'] = 'ZIP code must be a 5-digit US ZIP code.';
    }

    if ($data['zip_code'] === '') {
        $data['zip_code'] = null;
    }

    return [$data, $errors];
}

function rr_validate_preferences(array $post): array
{
    $alertTypes = $post['alert_types'] ?? [];
    if (!is_array($alertTypes)) {
        $alertTypes = [];
    }

    $alertTypes = array_values(array_filter($alertTypes, function ($value) {
        return is_string($value) && in_array($value, rr_allowed_alert_types(), true);
    }));

    $data = [
        'user_id' => filter_var($post['user_id'] ?? null, FILTER_VALIDATE_INT),
        'zip_code' => trim((string) ($post['zip_code'] ?? '')),
        'alert_types' => $alertTypes,
        'notify_severity' => trim((string) ($post['notify_severity'] ?? '')),
        'device_token' => trim((string) ($post['device_token'] ?? '')),
    ];
    $errors = [];

    if (!$data['user_id'] || $data['user_id'] < 1) {
        $errors['user_id'] = 'Enter a valid user ID.';
    }

    if ($data['zip_code'] !== '' && !preg_match('/^\d{5}$/', $data['zip_code'])) {
        $errors['zip_code'] = 'ZIP code must be a 5-digit US ZIP code.';
    }

    if ($data['notify_severity'] !== '' && !in_array(strtolower($data['notify_severity']), rr_allowed_severities(), true)) {
        $errors['notify_severity'] = 'Choose a supported severity level.';
    }

    if ($data['zip_code'] === '') {
        $data['zip_code'] = null;
    }

    if ($data['notify_severity'] === '') {
        $data['notify_severity'] = null;
    }

    if ($data['device_token'] === '') {
        $data['device_token'] = null;
    }

    return [$data, $errors];
}
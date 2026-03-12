<?php

function e(?string $value): string
{
    return htmlspecialchars((string) ($value ?? ''), ENT_QUOTES, 'UTF-8');
}

function rr_format_datetime(?string $value): string
{
    if (!$value) {
        return 'Unavailable';
    }

    if (is_numeric($value)) {
        $numericValue = (float) $value;
        if ($numericValue > 1000000000000) {
            $numericValue /= 1000;
        }

        return date('M j, Y g:i A', (int) $numericValue);
    }

    $timestamp = strtotime($value);
    if ($timestamp === false) {
        return $value;
    }

    return date('M j, Y g:i A', $timestamp);
}

function rr_severity_class(?string $severity): string
{
    $normalized = strtolower((string) $severity);
    if ($normalized === 'high' || $normalized === 'severe' || $normalized === 'extreme') {
        return 'severity-high';
    }

    if ($normalized === 'medium' || $normalized === 'moderate') {
        return 'severity-medium';
    }

    return 'severity-low';
}

function rr_parse_alert_types(?string $value): array
{
    if (!$value) {
        return [];
    }

    $decoded = json_decode($value, true);
    if (!is_array($decoded)) {
        return [];
    }

    return array_values(array_filter($decoded, 'is_string'));
}

function rr_build_page_url(string $page): string
{
    return $page;
}
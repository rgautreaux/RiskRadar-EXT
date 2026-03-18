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
        $timestamp = (int) $value;
        // Values above 9_999_999_999 exceed the maximum 10-digit second-precision
        // Unix timestamp (year ~2286), so they must be millisecond-precision.
        if ($timestamp > 9999999999) {
            $timestamp = intdiv($timestamp, 1000);
        }

        return date('M j, Y g:i A', $timestamp);
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

function rr_risk_level_label(?float $score): string
{
    if ($score === null) {
        return 'Unavailable';
    }

    if ($score >= 70.0) {
        return 'High';
    }

    if ($score >= 40.0) {
        return 'Medium';
    }

    return 'Low';
}

function rr_format_risk_score(?float $score): string
{
    if ($score === null) {
        return 'Unavailable';
    }

    return number_format($score, 2);
}

function rr_priority_label(?string $urgency): string
{
    if ($urgency === null) {
        return 'Priority unavailable';
    }

    $value = strtolower($urgency);
    if ($value === 'high') {
        return 'High Priority';
    }

    if ($value === 'medium') {
        return 'Medium Priority';
    }

    if ($value === 'low') {
        return 'Low Priority';
    }

    return 'Priority unavailable';
}
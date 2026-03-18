<?php

require_once __DIR__ . '/../services/bootstrap.php';

$alertId = rr_read_query_int('id', 0, 1, PHP_INT_MAX);

if ($alertId === 0) {
    http_response_code(404);
    $errorTitle = 'Alert not found';
    $errorMessage = 'No valid alert ID was provided.';
    require __DIR__ . '/../views/error.php';
    exit;
}

$alertResult = rr_fetch_alert_by_id($config, $alertId);

if (!$alertResult['ok'] || $alertResult['data'] === null) {
    http_response_code(($alertResult['status'] ?? 0) === 404 ? 404 : 503);
    $errorTitle = 'Alert not found';
    $errorMessage = $alertResult['message'] ?? 'That alert could not be loaded.';
    require __DIR__ . '/../views/error.php';
    exit;
}

$alert = $alertResult['data'];
require __DIR__ . '/../views/alert_detail.php';

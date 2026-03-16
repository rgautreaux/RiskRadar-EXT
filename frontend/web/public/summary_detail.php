<?php

require_once __DIR__ . '/../services/bootstrap.php';

$summaryId = rr_read_query_int('id', 0, 1, PHP_INT_MAX);

if ($summaryId === 0) {
    http_response_code(404);
    $errorTitle = 'Summary not found';
    $errorMessage = 'No valid summary ID was provided.';
    require __DIR__ . '/../views/error.php';
    exit;
}

$summaryResult = rr_fetch_summary_by_id($config, $summaryId);

if (!$summaryResult['ok'] || $summaryResult['data'] === null) {
    http_response_code(($summaryResult['status'] ?? 0) === 404 ? 404 : 503);
    $errorTitle = 'Summary not found';
    $errorMessage = $summaryResult['message'] ?? 'That summary could not be loaded.';
    require __DIR__ . '/../views/error.php';
    exit;
}

$summary = $summaryResult['data'];
require __DIR__ . '/../views/summary_detail.php';

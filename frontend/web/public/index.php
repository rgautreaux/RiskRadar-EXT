<?php

// LOCAL DEBUG: Enable error reporting for troubleshooting
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require_once __DIR__ . '/../services/bootstrap.php';

rr_require_feature_access();

$statsResult = rr_fetch_alert_stats($config);
$alertsResult = rr_fetch_alerts($config, ['limit' => 5, 'offset' => 0]);
$latestSummaryResult = rr_fetch_latest_summary($config);

$topSeverityLabel = 'No data';
if ($statsResult['data']['by_severity']) {
    arsort($statsResult['data']['by_severity']);
    $topSeverityLabel = ucfirst((string) array_key_first($statsResult['data']['by_severity']));
}

$topTypeLabel = 'No data';
if ($statsResult['data']['by_type']) {
    arsort($statsResult['data']['by_type']);
    $topTypeLabel = ucfirst(str_replace('_', ' ', (string) array_key_first($statsResult['data']['by_type'])));
}

require __DIR__ . '/../views/dashboard.php';
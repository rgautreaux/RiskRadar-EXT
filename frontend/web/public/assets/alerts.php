<?php

require_once __DIR__ . '/../services/bootstrap.php';

rr_require_feature_access();

$filters = rr_collect_alert_filters();
$alertsResult = rr_fetch_alerts($config, $filters);

require __DIR__ . '/../views/alerts.php';
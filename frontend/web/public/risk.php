<?php

require_once __DIR__ . '/../services/bootstrap.php';

$userId = rr_read_query_int('user_id', 1, 1, 1000000);

$riskScoreResult = rr_fetch_user_risk_score($config, $userId);
$prioritizedAlertsResult = rr_fetch_prioritized_alerts($config, $userId, 5);

require __DIR__ . '/../views/risk.php';

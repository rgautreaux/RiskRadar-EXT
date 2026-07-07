<?php

require_once __DIR__ . '/../services/bootstrap.php';


rr_require_feature_access();
$isGuest = rr_is_guest_mode();

$userId = rr_read_query_int('user_id', 0, 0, 999999);
$radiusKm = rr_read_query_int('radius_km', 150, 1, 500);

$riskResult = null;
$prioritizedResult = null;

if ($userId > 0) {
    $riskResult = rr_fetch_risk_score($config, $userId, [
        'radius_km' => $radiusKm,
    ]);
    $prioritizedResult = rr_fetch_prioritized_alerts($config, $userId, [
        'radius_km' => $radiusKm,
        'limit' => 5,
    ]);
}

require __DIR__ . '/../views/risk.php';

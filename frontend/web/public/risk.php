<?php

require_once __DIR__ . '/../services/bootstrap.php';

rr_require_feature_access();

$radiusKm = rr_read_query_int('radius_km', 150, 1, 500);

// Resolve user ID from session for authenticated users.
// This avoids asking the user to enter their ID manually and closes a
// BOLA vulnerability where any user could view any other user's risk
// score by supplying an arbitrary user_id query parameter.
$currentUser = null;
if (rr_is_authenticated()) {
    $meResult = rr_fetch_current_user($config);
    if ($meResult['ok'] && is_array($meResult['data'])) {
        $currentUser = $meResult['data'];
    }
}

$userId = $currentUser !== null
    ? (int) ($currentUser['id'] ?? 0)
    : rr_read_query_int('user_id', 0, 0, 999999);

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

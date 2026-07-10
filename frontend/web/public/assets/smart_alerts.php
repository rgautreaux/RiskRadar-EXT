<?php


require_once __DIR__ . '/../services/bootstrap.php';

if (rr_access_context() !== 'authenticated') {
    rr_set_flash('warning', 'You’re currently exploring as a guest. Sign in or create an account to unlock smart alerts and personalized features!');
    header('Location: login.php');
    exit;
}

/*
 * Smart Alert Prioritization page.
 *
 * Requires a user_id query parameter. If the user has a location set in
 * their profile, the backend returns alerts ranked by personalized priority.
 */

$userId = rr_read_query_int('user_id', 0, 0, 999999);
$radiusKm = rr_read_query_int('radius_km', 150, 1, 500);
$limit = rr_read_query_int('limit', 50, 1, 200);

$prioritizedResult = null;
$riskResult = null;
$errorMessage = null;

if ($userId > 0) {
    $prioritizedResult = rr_fetch_prioritized_alerts($config, $userId, [
        'radius_km' => $radiusKm,
        'limit' => $limit,
    ]);
    $riskResult = rr_fetch_risk_score($config, $userId, [
        'radius_km' => $radiusKm,
    ]);
}

require __DIR__ . '/../views/smart_alerts.php';

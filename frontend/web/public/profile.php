<?php

require_once __DIR__ . '/../services/bootstrap.php';

rr_require_feature_access();

// Resolve the authenticated user from the session cookie.
// This avoids asking the user to type their ID manually and prevents
// a BOLA vulnerability where a forged user_id POST value could update
// a different account's preferences.
$currentUser = null;
if (rr_is_authenticated()) {
    $meResult = rr_fetch_current_user($config);
    if ($meResult['ok'] && is_array($meResult['data'])) {
        $currentUser = $meResult['data'];
    }
}
$sessionUserId = $currentUser !== null ? (int) ($currentUser['id'] ?? 0) : 0;

$flash = rr_get_flash();
$preferencesErrors = [];
$preferencesResult = null;
$preferencesForm = [
    'user_id'          => $sessionUserId ?: null,
    'zip_code'         => '',
    'alert_types'      => [],
    'notify_severity'  => '',
    'device_token'     => '',
    'health_conditions'=> [],
];

// Pre-populate from saved preferences on GET requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST' && $currentUser !== null) {
    $preferencesForm['zip_code']          = $currentUser['zip_code'] ?? '';
    $preferencesForm['notify_severity']   = $currentUser['notify_severity'] ?? '';
    $savedAlertTypes = $currentUser['alert_types'] ?? null;
    $preferencesForm['alert_types']       = is_string($savedAlertTypes) && $savedAlertTypes !== ''
        ? (json_decode($savedAlertTypes, true) ?: [])
        : [];
    $savedHealthConditions = $currentUser['health_conditions'] ?? null;
    $preferencesForm['health_conditions'] = is_string($savedHealthConditions) && $savedHealthConditions !== ''
        ? (json_decode($savedHealthConditions, true) ?: [])
        : [];
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = trim((string) ($_POST['action'] ?? ''));
    if (!rr_verify_csrf($_POST['csrf_token'] ?? null)) {
        rr_set_flash('warning', 'The form could not be verified. Refresh the page and try again.');
        header('Location: profile.php');
        exit;
    }

    if ($action !== 'preferences') {
        rr_set_flash('warning', 'Unsupported form action was rejected.');
        header('Location: profile.php');
        exit;
    }

    if ($action === 'preferences') {
        // Always use the session-resolved ID — never trust the POST value.
        $_POST['user_id'] = (string) $sessionUserId;
        [$preferencesForm, $preferencesErrors] = rr_validate_preferences($_POST);
        if (!$preferencesErrors) {
            $userId = $sessionUserId;
            $preferencesPayload = [
                'zip_code' => $preferencesForm['zip_code'],
                'alert_types' => $preferencesForm['alert_types'],
                'notify_severity' => $preferencesForm['notify_severity'],
                'device_token' => $preferencesForm['device_token'],
                'health_conditions' => $preferencesForm['health_conditions'],
            ];
            $preferencesResult = rr_update_preferences($config, $userId, $preferencesPayload);
            if ($preferencesResult['ok']) {
                rr_set_flash('success', 'Preferences updated successfully.');
                header('Location: profile.php');
                exit;
            }
        }
    }
}

require __DIR__ . '/../views/profile.php';
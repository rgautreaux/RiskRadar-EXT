<?php

require_once __DIR__ . '/../services/bootstrap.php';

$flash = rr_get_flash();
$registerErrors = [];
$preferencesErrors = [];
$registerResult = null;
$preferencesResult = null;
$registerForm = [
    'display_name' => '',
    'email' => '',
    'password' => '',
    'zip_code' => '',
];
$preferencesForm = [
    'user_id' => null,
    'zip_code' => '',
    'alert_types' => [],
    'notify_severity' => '',
    'device_token' => '',
];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = trim((string) ($_POST['action'] ?? ''));
    if (!rr_verify_csrf($_POST['csrf_token'] ?? null)) {
        rr_set_flash('warning', 'The form could not be verified. Refresh the page and try again.');
        header('Location: profile.php');
        exit;
    }

    if ($action === 'register') {
        [$registerForm, $registerErrors] = rr_validate_registration($_POST);
        if (!$registerErrors) {
            $registerResult = rr_register_user($config, $registerForm);
            if ($registerResult['ok']) {
                rr_set_flash('success', 'User registration succeeded.');
            }
        }
    }

    if ($action === 'preferences') {
        [$preferencesForm, $preferencesErrors] = rr_validate_preferences($_POST);
        if (!$preferencesErrors) {
            $userId = (int) $preferencesForm['user_id'];
            $preferencesPayload = [
                'zip_code' => $preferencesForm['zip_code'],
                'alert_types' => $preferencesForm['alert_types'],
                'notify_severity' => $preferencesForm['notify_severity'],
                'device_token' => $preferencesForm['device_token'],
            ];
            $preferencesResult = rr_update_preferences($config, $userId, $preferencesPayload);
            if ($preferencesResult['ok']) {
                rr_set_flash('success', 'Preferences updated successfully.');
                $preferencesForm['alert_types'] = rr_parse_alert_types($preferencesResult['data']['alert_types']);
            }
        }
    }
}

require __DIR__ . '/../views/profile.php';
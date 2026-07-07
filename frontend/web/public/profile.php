<?php

require_once __DIR__ . '/../services/bootstrap.php';


rr_require_feature_access();
$isGuest = rr_is_guest_mode();

$flash = rr_get_flash();
$preferencesErrors = [];
$preferencesResult = null;
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

    if ($action !== 'preferences') {
        rr_set_flash('warning', 'Unsupported form action was rejected.');
        header('Location: profile.php');
        exit;
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
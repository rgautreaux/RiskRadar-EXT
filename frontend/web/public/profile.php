<?php


require_once __DIR__ . '/../services/bootstrap.php';

// Only allow authenticated users (not guests or anonymous) to access profile page
if (rr_access_context() !== 'authenticated') {
    rr_set_flash('warning', 'You must be signed in to access your profile.');
    header('Location: login.php');
    exit;
}

$flash = rr_get_flash();
$preferencesErrors = [];
$preferencesResult = null;

$currentUser = null;
$preferencesForm = [
    'zip_code' => '',
    'alert_types' => [],
    'notify_severity' => '',
    'device_token' => '',
    'health_conditions' => [],
];

// Fetch current user from session (API call)
$userResult = rr_fetch_current_user($config);
if ($userResult['ok'] && is_array($userResult['data'])) {
    $currentUser = $userResult['data'];
    // Pre-fill form with user data
    $preferencesForm['zip_code'] = $currentUser['zip_code'] ?? '';
    $preferencesForm['alert_types'] = is_array($currentUser['alert_types']) ? $currentUser['alert_types'] : [];
    $preferencesForm['notify_severity'] = $currentUser['notify_severity'] ?? '';
    $preferencesForm['device_token'] = $currentUser['device_token'] ?? '';
    $preferencesForm['health_conditions'] = is_array($currentUser['health_conditions']) ? $currentUser['health_conditions'] : [];
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

    if ($action === 'preferences' && $currentUser) {
        [$preferencesForm, $preferencesErrors] = rr_validate_preferences($_POST);
        if (!$preferencesErrors) {
            $userId = (int) $currentUser['id'];
            $preferencesPayload = [
                'zip_code' => $preferencesForm['zip_code'],
                'alert_types' => $preferencesForm['alert_types'],
                'notify_severity' => $preferencesForm['notify_severity'],
                'device_token' => $preferencesForm['device_token'],
                'health_conditions' => $preferencesForm['health_conditions'],
            ];
            
            // Parse and include personality profile if present
            $personalityJson = trim((string) ($_POST['personality_profile_json'] ?? ''));
            if ($personalityJson !== '') {
                $personalityProfile = json_decode($personalityJson, true);
                if (is_array($personalityProfile)) {
                    $preferencesPayload['assistant_style_profile'] = $personalityProfile;
                }
            }
            
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
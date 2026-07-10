<?php

require_once __DIR__ . '/../services/bootstrap.php';

rr_require_feature_access();

$userZip = '';
$accessContext = rr_access_context();

if ($accessContext !== 'anonymous' && $accessContext !== 'guest') {
    $currentUserResult = rr_fetch_current_user($config);
    if ($currentUserResult['ok'] && is_array($currentUserResult['data'])) {
        $userZip = (string) ($currentUserResult['data']['zip_code'] ?? '');
    }
}

require __DIR__ . '/../views/create_summary.php';

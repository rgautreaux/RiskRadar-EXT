<?php

require_once __DIR__ . '/../services/bootstrap.php';

if (rr_access_context() !== 'authenticated') {
    header('Location: login.php');
    exit;
}

$sessionToken = $_COOKIE['riskradar_session'] ?? '';
if (is_string($sessionToken) && $sessionToken !== '') {
    rr_http_request($config, 'POST', 'auth/logout', [], null, [
        'Cookie: riskradar_session=' . $sessionToken,
    ]);
}

rr_clear_session_cookie();
rr_set_flash('success', 'You have been signed out.');
header('Location: login.php');
exit;

<?php

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

header('X-Content-Type-Options: nosniff');
header('X-Frame-Options: SAMEORIGIN');
header('Referrer-Policy: strict-origin-when-cross-origin');
header('Permissions-Policy: geolocation=(), microphone=(), camera=()');

$config = require __DIR__ . '/../config/app.php';

require_once __DIR__ . '/security.php';
require_once __DIR__ . '/presentation.php';
require_once __DIR__ . '/validators.php';
require_once __DIR__ . '/api_client.php';
require_once __DIR__ . '/../components/layout.php';
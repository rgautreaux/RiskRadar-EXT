<?php

if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

$config = require __DIR__ . '/../config/app.php';

require_once __DIR__ . '/security.php';
require_once __DIR__ . '/presentation.php';
require_once __DIR__ . '/validators.php';
require_once __DIR__ . '/api_client.php';
require_once __DIR__ . '/../components/layout.php';
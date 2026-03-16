<?php

require_once __DIR__ . '/../services/bootstrap.php';

$flash = rr_get_flash();
$loginErrors = [];
$loginForm = [
    'email' => '',
    'zip_code' => '',
];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!rr_verify_csrf($_POST['csrf_token'] ?? null)) {
        rr_set_flash('warning', 'The form could not be verified. Refresh the page and try again.');
        header('Location: login.php');
        exit;
    }

    [$loginForm, $loginErrors] = rr_validate_login($_POST);

    if (!$loginErrors) {
        // Backend login endpoint is not yet implemented in Stage 1.
        $loginErrors['_form'] = 'Login is not yet supported by the backend in Stage 1. Register a new account or use the Profile page to manage preferences.';
    }

}

require __DIR__ . '/../views/login.php';

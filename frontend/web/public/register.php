<?php

// LOCAL DEBUG: Enable error reporting for troubleshooting registration issues
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

require_once __DIR__ . '/../services/bootstrap.php';

if (rr_access_context() !== 'anonymous') {
    header('Location: index.php');
    exit;
}

$flash = rr_get_flash();
$registerErrors = [];
$registerResult = null;
$registerForm = [
    'display_name' => '',
    'email' => '',
    'password' => '',
    'zip_code' => '',
];

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!rr_verify_csrf($_POST['csrf_token'] ?? null)) {
        rr_set_flash('warning', 'The form could not be verified. Refresh the page and try again.');
        header('Location: register.php');
        exit;
    }

    [$registerForm, $registerErrors] = rr_validate_registration($_POST);

    if (!$registerErrors) {
        $registerResult = rr_register_user($config, $registerForm);
        if ($registerResult['ok']) {
            rr_set_flash('success', 'Account created successfully. You can now sign in.');
            header('Location: login.php');
            exit;
        }
    }
}

require __DIR__ . '/../views/register.php';

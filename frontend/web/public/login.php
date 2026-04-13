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
        $loginResult = rr_login_user($config, [
            'email' => $loginForm['email'],
            'password' => (string) ($_POST['password'] ?? ''),
        ]);

        if ($loginResult['ok']) {
            $sessionToken = $loginResult['data']['session_token'] ?? '';
            $expiresAt = strtotime((string) ($loginResult['data']['expires_at'] ?? '')) ?: time() + 3600;
            if ($sessionToken !== '') {
                rr_set_session_cookie($sessionToken, $expiresAt);
                rr_set_flash('success', 'Signed in successfully.');
                header('Location: assistant.php');
                exit;
            }

            $loginErrors['_form'] = 'Login succeeded but no session token was returned.';
        } else {
            $loginErrors['_form'] = $loginResult['message'] ?? 'Login failed. Please try again.';
        }
    }

}

require __DIR__ . '/../views/login.php';

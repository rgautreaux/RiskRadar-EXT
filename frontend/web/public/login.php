<?php

require_once __DIR__ . '/../services/bootstrap.php';

if (rr_access_context() !== 'anonymous') {
    header('Location: index.php');
    exit;
}

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

    $action = (string) ($_POST['action'] ?? 'login');

    if ($action === 'guest') {
        rr_set_guest_mode(true);
        rr_set_flash('success', 'You are now exploring RiskRadar as a guest.');
        header('Location: index.php');
        exit;
    }

    // Validate email and password
    $loginForm['email'] = trim((string) ($_POST['email'] ?? ''));
    $loginForm['password'] = (string) ($_POST['password'] ?? '');
    if (!filter_var($loginForm['email'], FILTER_VALIDATE_EMAIL)) {
        $loginErrors['email'] = 'A valid email is required.';
    }
    if (strlen($loginForm['password']) < 8) {
        $loginErrors['password'] = 'Password must be at least 8 characters.';
    }

    if (!$loginErrors) {
        // Call backend API for authentication
        $apiUrl = rtrim($config['api']['base_url'], '/') . $config['api']['prefix'] . '/auth/login';
        $payload = json_encode([
            'email' => $loginForm['email'],
            'password' => $loginForm['password'],
        ]);
        $ch = curl_init($apiUrl);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'Accept: application/json',
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
        curl_setopt($ch, CURLOPT_HEADER, true);
        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false);
        $response = curl_exec($ch);
        $headerSize = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
        $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $headers = substr($response, 0, $headerSize);
        $body = substr($response, $headerSize);
        curl_close($ch);

        $data = json_decode($body, true);
        if ($status === 200 && isset($data['session_token'], $data['expires_at'])) {
            // Set session cookie
            $sessionToken = $data['session_token'];
            $expiresAt = strtotime($data['expires_at']) ?: (time() + 3600);
            rr_set_session_cookie($sessionToken, $expiresAt);
            // Debug: Log cookie after setting
            if (isset($_GET['debug_cookie'])) {
                error_log('[login.php] Set session cookie: ' . print_r($_COOKIE, true));
            }
            rr_set_flash('success', 'Signed in successfully.');
            header('Location: index.php');
            exit;
        } else {
            $loginErrors['_form'] = $data['message'] ?? 'Login failed. Please check your credentials.';
        }
    }
}

require __DIR__ . '/../views/login.php';

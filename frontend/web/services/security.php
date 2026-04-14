<?php

function rr_is_authenticated(): bool
{
    $sessionToken = $_COOKIE['riskradar_session'] ?? '';
    return is_string($sessionToken) && $sessionToken !== '';
}

function rr_is_guest_mode(): bool
{
    return !empty($_SESSION['riskradar_guest_mode']);
}

function rr_set_guest_mode(bool $enabled): void
{
    if ($enabled) {
        $_SESSION['riskradar_guest_mode'] = true;
        return;
    }

    unset($_SESSION['riskradar_guest_mode']);
}

function rr_access_context(): string
{
    if (rr_is_authenticated()) {
        return 'authenticated';
    }

    if (rr_is_guest_mode()) {
        return 'guest';
    }

    return 'anonymous';
}

function rr_require_feature_access(): void
{
    $context = rr_access_context();
    if ($context === 'authenticated') {
        return;
    }
    // Guests are not allowed for restricted features
    if ($context === 'guest') {
        rr_set_flash('warning', 'Guest mode: Please sign in or create an account to access this feature.');
        header('Location: login.php');
        exit;
    }
    // Anonymous users
    rr_set_flash('warning', 'Please sign in, create an account, or continue as guest to use RiskRadar.');
    header('Location: login.php');
    exit;
}

function rr_csrf_token(): string
{
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }

    return $_SESSION['csrf_token'];
}

function rr_verify_csrf(?string $token): bool
{
    if (!is_string($token) || $token === '') {
        return false;
    }

    return hash_equals(rr_csrf_token(), $token);
}

function rr_set_flash(string $type, string $message): void
{
    $_SESSION['flash'] = [
        'type' => $type,
        'message' => $message,
    ];
}

function rr_get_flash(): ?array
{
    if (empty($_SESSION['flash']) || !is_array($_SESSION['flash'])) {
        return null;
    }

    $flash = $_SESSION['flash'];
    unset($_SESSION['flash']);

    return $flash;
}

function rr_set_session_cookie(string $token, int $expiresAt): void
{
    setcookie('riskradar_session', $token, [
        'expires' => $expiresAt,
        'path' => '/',
        'httponly' => true,
        'samesite' => 'Lax',
        'secure' => !empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off',
    ]);

    rr_set_guest_mode(false);
}

function rr_clear_session_cookie(): void
{
    setcookie('riskradar_session', '', [
        'expires' => time() - 3600,
        'path' => '/',
        'httponly' => true,
        'samesite' => 'Lax',
        'secure' => !empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off',
    ]);

    rr_set_guest_mode(false);
}
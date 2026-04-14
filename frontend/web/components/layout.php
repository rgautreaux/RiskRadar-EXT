<?php

/*
====================================================
 RiskRadar Web Layout Shell — Layout Lane
 Author: Rebecca (Layout Lane)
 Last Updated: 2026-03-23
----------------------------------------------------
 This file defines the shared shell, navigation, and
 section hierarchy for all web pages. Only update this
 file for global/layout changes. Page content is injected
 via rr_render_layout_start and rr_render_layout_end.
====================================================
*/

function rr_render_layout_start(string $title, string $activePage): void
{
    $GLOBALS['rr_layout_active_page'] = $activePage;

    $accessContext = function_exists('rr_access_context') ? rr_access_context() : 'anonymous';
    $isAnonymous = $accessContext === 'anonymous';
    $isGuest = $accessContext === 'guest';

    $apiBase = 'http://127.0.0.1:8001';
    $apiPrefix = '/api/v1';
    $globalConfig = $GLOBALS['config'] ?? null;
    if (is_array($globalConfig) && function_exists('rr_api_url')) {
        $apiBase = rtrim((string) ($globalConfig['api']['base_url'] ?? $apiBase), '/');
        $apiPrefix = '/' . trim((string) ($globalConfig['api']['prefix'] ?? $apiPrefix), '/');
    }

    $shouldRenderGolbyWidget = $activePage !== 'login';
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title><?php echo e($title); ?> | RiskRadar Web</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="assets/app.css">
        <script>
        window.__RISKRADAR_API_BASE__ = <?php echo json_encode($apiBase); ?>;
        window.__RISKRADAR_API_PREFIX__ = <?php echo json_encode($apiPrefix); ?>;
        </script>
        <?php if ($shouldRenderGolbyWidget) : ?>
        <link rel="stylesheet" href="assets/golby-widget.css">
        <script type="module" src="assets/golby-widget.js" defer></script>
        <?php endif; ?>
    </head>
    <body class="page-<?php echo e($activePage); ?>" data-page="<?php echo e($activePage); ?>">
        <div class="app-shell">
            <header class="topbar">
                <div>
                    <p class="eyebrow">CMPS 357 Web Extension</p>
                    <a class="brand" href="index.php">RiskRadar Web</a>
                    <?php if ($isGuest) : ?>
                    <p class="eyebrow">Guest mode enabled</p>
                    <?php endif; ?>
                </div>
                <nav class="topnav" aria-label="Primary navigation">
                    <?php if ($isAnonymous) : ?>
                    <a class="<?php echo $activePage === 'login' ? 'is-active' : ''; ?>" href="login.php">
                        <img src="assets/icons/profile.svg" alt="Login Icon" class="nav-icon"> Login
                    </a>
                    <a class="<?php echo $activePage === 'register' ? 'is-active' : ''; ?>" href="register.php">
                        <img src="assets/icons/profile.svg" alt="Register Icon" class="nav-icon"> Sign Up
                    </a>
                    <?php else : ?>
                    <a class="<?php echo $activePage === 'dashboard' ? 'is-active' : ''; ?>" href="index.php">
                        <img src="assets/icons/home-green.svg" alt="Dashboard Icon" class="nav-icon"> Dashboard
                    </a>
                    <a class="<?php echo $activePage === 'alerts' ? 'is-active' : ''; ?>" href="alerts.php">
                        <img src="assets/icons/notification.svg" alt="Alerts Icon" class="nav-icon"> Alerts
                    </a>
                    <a class="<?php echo $activePage === 'summaries' ? 'is-active' : ''; ?>" href="summaries.php">
                        <img src="assets/icons/chart.svg" alt="Summaries Icon" class="nav-icon"> Summaries
                    </a>
                    <a class="<?php echo $activePage === 'profile' ? 'is-active' : ''; ?>" href="profile.php">
                        <img src="assets/icons/settings.svg" alt="Profile Icon" class="nav-icon"> Profile
                    </a>
                    <a class="<?php echo $activePage === 'risk' ? 'is-active' : ''; ?>" href="risk.php">
                        <img src="assets/icons/warning.svg" alt="Risk Icon" class="nav-icon"> Risk
                    </a>
                    <a class="<?php echo $activePage === 'map' ? 'is-active' : ''; ?>" href="map.php">
                        <img src="assets/icons/location-pin.svg" alt="Map Icon" class="nav-icon"> Map
                    </a>
                    <a class="<?php echo $activePage === 'forecast' ? 'is-active' : ''; ?>" href="forecast.php">
                        <img src="assets/icons/calendar.svg" alt="Forecast Icon" class="nav-icon"> Forecast
                    </a>
                    <a class="<?php echo $activePage === 'assistant' ? 'is-active' : ''; ?>" href="assistant.php">
                        <img src="assets/icons/ai-assistant.svg" alt="Assistant Icon" class="nav-icon"> Assistant
                    </a>
                    <a href="login.php">
                        <img src="assets/icons/profile.svg" alt="Login Icon" class="nav-icon"><?php echo $isGuest ? ' Sign In' : ' Login'; ?>
                    </a>
                    <?php endif; ?>
                </nav>
            </header>
            <main class="page-shell">
    <?php
}

function rr_render_layout_end(): void
{
    $activePage = (string) ($GLOBALS['rr_layout_active_page'] ?? 'unknown');
    $shouldRenderGolbyWidget = $activePage !== 'login';

    ?>
            </main>
            <?php if ($shouldRenderGolbyWidget) : ?>
            <div id="riskradar-ai-assistant-widget"></div>
            <?php endif; ?>
        </div>
    </body>
    </html>
    <?php
}

function rr_render_message(?string $message, string $tone = 'warning'): void
{
    if (!$message) {
        return;
    }
    ?>
    <section class="message message-<?php echo e($tone); ?>">
        <p><?php echo e($message); ?></p>
    </section>
    <?php
}
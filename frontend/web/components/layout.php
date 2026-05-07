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

function rr_golby_onboarding_page_label(string $activePage): string
{
    return match ($activePage) {
        'dashboard' => 'Dashboard',
        'alerts' => 'Alerts',
        'summaries' => 'Summaries',
        'profile' => 'Profile',
        'risk' => 'Risk',
        'map' => 'Map',
        'forecast' => 'Forecast',
        'assistant' => 'Assistant',
        default => 'this page',
    };
}

function rr_prepare_golby_onboarding_state(array $config, string $activePage): ?array
{
    if ($activePage === 'login' || $activePage === 'register') {
        return null;
    }

    if (!function_exists('rr_access_context') || rr_access_context() !== 'authenticated') {
        return null;
    }

    if (!function_exists('rr_fetch_current_user') || !function_exists('rr_api_url')) {
        return null;
    }

    $userResult = rr_fetch_current_user($config);
    if (empty($userResult['ok']) || !is_array($userResult['data'])) {
        return null;
    }

    $currentUser = $userResult['data'];
    if (!empty($currentUser['has_completed_onboarding'])) {
        return null;
    }

    $userId = (int) ($currentUser['id'] ?? 0);
    if ($userId <= 0) {
        return null;
    }

    return [
        'user_id' => $userId,
        'page_label' => rr_golby_onboarding_page_label($activePage),
        'complete_url' => rr_api_url($config, 'users/' . $userId . '/onboarding'),
    ];
}

function rr_should_render_golby_widget(string $activePage): bool
{
    if ($activePage === 'login' || $activePage === 'register') {
        return false;
    }

    if (!function_exists('rr_access_context')) {
        return false;
    }

    $accessContext = rr_access_context();
    return $accessContext === 'authenticated' || $accessContext === 'guest';
}

function rr_render_golby_onboarding_markup(array $state): void
{
    $pageLabel = e((string) ($state['page_label'] ?? 'this page'));
    ?>
    <div class="golby-onboarding-shell" id="golby-onboarding-shell" hidden data-golby-onboarding-shell>
        <div class="golby-onboarding-backdrop" data-golby-onboarding-dismiss="backdrop" aria-hidden="true"></div>
        <section
            class="golby-onboarding-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="golby-onboarding-title"
            aria-describedby="golby-onboarding-copy"
            data-golby-onboarding-dialog
        >
            <button type="button" class="golby-onboarding-close" data-golby-onboarding-action="dismiss" aria-label="Close tutorial">
                <span aria-hidden="true">&times;</span>
            </button>

            <div class="golby-onboarding-header">
                <div class="golby-onboarding-avatar" aria-hidden="true">
                    <img src="assets/icons/Golby-Laugh.svg" alt="">
                </div>
                <div>
                    <p class="golby-onboarding-eyebrow">Golby-led first-time tour</p>
                    <h2 id="golby-onboarding-title">Welcome to <?php echo $pageLabel; ?></h2>
                    <p id="golby-onboarding-copy" class="golby-onboarding-intro">
                        I’ll walk you through the web app in a minute or two, so your new account feels friendly right away.
                    </p>
                </div>
            </div>

            <div class="golby-onboarding-progress" aria-hidden="true">
                <span class="golby-onboarding-progress-fill" data-golby-onboarding-progress></span>
            </div>
            <div class="golby-onboarding-step-meta">
                <span data-golby-onboarding-counter>Step 1 of 4</span>
                <span class="golby-onboarding-page-pill"><?php echo $pageLabel; ?></span>
            </div>

            <div class="golby-onboarding-body">
                <h3 data-golby-onboarding-step-title>Warm hello from Golby</h3>
                <p data-golby-onboarding-step-body>
                    You’re in the right place. I’ll show you the parts of RiskRadar that matter most so you can feel at home quickly.
                </p>
            </div>

            <ul class="golby-onboarding-highlights" aria-label="Tutorial highlights">
                <li>See live alert volume and severity at a glance.</li>
                <li>Use summaries, map, and forecast pages for quick context.</li>
                <li>Keep your profile tuned so the app feels personal and calm.</li>
            </ul>

            <div class="golby-onboarding-actions">
                <button type="button" class="button-secondary golby-onboarding-ghost" data-golby-onboarding-action="skip">
                    Skip for now
                </button>
                <button type="button" class="button-primary golby-onboarding-primary" data-golby-onboarding-action="next">
                    Next
                </button>
            </div>
        </section>
    </div>
    <?php
}

function rr_render_layout_start(string $title, string $activePage): void
{
    $GLOBALS['rr_layout_active_page'] = $activePage;

    $accessContext = function_exists('rr_access_context') ? rr_access_context() : 'anonymous';
    $isAnonymous = $accessContext === 'anonymous';
    $isGuest = $accessContext === 'guest';
    $golbyOnboardingState = rr_prepare_golby_onboarding_state($GLOBALS['config'] ?? [], $activePage);
    $GLOBALS['rr_golby_onboarding_state'] = $golbyOnboardingState;

    $apiBase = 'http://127.0.0.1:8001';
    $apiPrefix = '/api/v1';
    $globalConfig = $GLOBALS['config'] ?? null;
    if (is_array($globalConfig) && function_exists('rr_api_url')) {
        $apiBase = rtrim((string) ($globalConfig['api']['base_url'] ?? $apiBase), '/');
        $apiPrefix = '/' . trim((string) ($globalConfig['api']['prefix'] ?? $apiPrefix), '/');
    }

    $shouldRenderGolbyWidget = rr_should_render_golby_widget($activePage);
    $isWebExperiencePage = !in_array($activePage, ['login', 'register'], true);
    ?>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title><?php echo e($title); ?> | RiskRadar Web</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=Atkinson+Hyperlegible+Next:wght@400;500;600;700&family=Geist+Mono:wght@400;500;600&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="assets/app.css">
        <script>
        window.__RISKRADAR_API_BASE__ = <?php echo json_encode($apiBase); ?>;
        window.__RISKRADAR_API_PREFIX__ = <?php echo json_encode($apiPrefix); ?>;
        window.__RISKRADAR_CLIENT_CONTEXT__ = <?php echo json_encode([
            'page' => $activePage,
            'accessContext' => $accessContext,
        ], JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE); ?>;
        </script>
        <?php if ($isWebExperiencePage) : ?>
        <link rel="stylesheet" href="assets/rr-web-ux.css">
        <script src="assets/rr-web-ux.js" defer></script>
        <?php endif; ?>
        <?php if (is_array($golbyOnboardingState)) : ?>
        <link rel="stylesheet" href="assets/golby-onboarding.css">
        <script>
        window.__GOLBY_ONBOARDING__ = <?php echo json_encode($golbyOnboardingState, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE); ?>;
        </script>
        <script src="assets/golby-onboarding.js" defer></script>
        <?php endif; ?>
        <?php if ($shouldRenderGolbyWidget) : ?>
        <link rel="stylesheet" href="assets/golby-widget.css">
        <script type="module" src="assets/golby-widget.js" defer></script>
        <?php endif; ?>
    </head>
    <body class="page-<?php echo e($activePage); ?>" data-page="<?php echo e($activePage); ?>">
        <a class="skip-link" href="#main-content">Skip to main content</a>
        <div class="app-shell">
            <header class="topbar">
                <div>
                    <p class="eyebrow">CMPS 357 Web Extension</p>
                    <a class="brand" href="index.php">RiskRadar Web</a>
                    <?php if ($isGuest) : ?>
                    <p class="eyebrow">Guest mode enabled</p>
                    <?php endif; ?>
                </div>
                <?php if ($activePage !== 'login') : ?>
                <nav class="topnav" aria-label="Primary navigation">
                    <?php if ($isAnonymous && $activePage !== 'login') : ?>
                    <a class="<?php echo $activePage === 'login' ? 'is-active' : ''; ?>" href="login.php">
                        <img src="assets/icons/profile.svg" alt="Login Icon" class="nav-icon"> Login
                    </a>
                    <a class="<?php echo $activePage === 'register' ? 'is-active' : ''; ?>" href="register.php">
                        <img src="assets/icons/profile.svg" alt="Register Icon" class="nav-icon"> Sign Up
                    </a>
                    <?php elseif ($isGuest) : ?>
                    <a class="<?php echo $activePage === 'dashboard' ? 'is-active' : ''; ?>" href="index.php">
                        <img src="assets/icons/home-green.svg" alt="Dashboard Icon" class="nav-icon"> Dashboard
                    </a>
                    <a class="<?php echo $activePage === 'alerts' ? 'is-active' : ''; ?>" href="alerts.php">
                        <img src="assets/icons/notification.svg" alt="Alerts Icon" class="nav-icon"> Alerts
                    </a>
                    <a class="<?php echo $activePage === 'summaries' ? 'is-active' : ''; ?>" href="summaries.php">
                        <img src="assets/icons/chart.svg" alt="Summaries Icon" class="nav-icon"> Summaries
                    </a>
                    <a class="<?php echo $activePage === 'assistant' ? 'is-active' : ''; ?>" href="assistant.php">
                        <img src="assets/icons/ai-assistant.svg" alt="Assistant Icon" class="nav-icon"> Assistant
                    </a>
                    <a class="<?php echo $activePage === 'travel' ? 'is-active' : ''; ?>" href="travel.php">
                        <img src="assets/icons/location-pin.svg" alt="Travel Icon" class="nav-icon"> Travel
                    </a>
                    <a class="<?php echo $activePage === 'login' ? 'is-active' : ''; ?>" href="login.php">
                        <img src="assets/icons/profile.svg" alt="Login Icon" class="nav-icon"> Login
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
                    <a class="<?php echo $activePage === 'travel' ? 'is-active' : ''; ?>" href="travel.php">
                        <img src="assets/icons/location-pin.svg" alt="Travel Icon" class="nav-icon"> Travel
                    </a>
                    <a href="logout.php">
                        <img src="assets/icons/profile.svg" alt="Logout Icon" class="nav-icon"> Logout
                    </a>
                    <button class="topnav-help" onclick="(window.openGolbyOnboarding ? window.openGolbyOnboarding() : window.dispatchEvent(new Event('golby:show-onboarding')));" aria-label="Show tutorial"> 
                        <img src="assets/icons/info.svg" alt="Help" class="nav-icon"> Help
                    </button>
                    <?php endif; ?>
                </nav>
                <?php if ($isWebExperiencePage) : ?>
                <div class="topbar-preferences" aria-label="Display preferences">
                    <label for="rr-language" class="topbar-preferences-label">Language</label>
                    <select id="rr-language" class="topbar-preferences-select" aria-label="Select language">
                        <option value="en">English</option>
                        <option value="es">Español</option>
                    </select>
                    <label for="rr-timezone" class="topbar-preferences-label">Timezone</label>
                    <select id="rr-timezone" class="topbar-preferences-select" aria-label="Select timezone">
                        <option value="local">Local browser timezone</option>
                        <option value="UTC">UTC</option>
                    </select>
                </div>
                <?php endif; ?>
                <?php endif; ?>
            </header>
            <main class="page-shell" id="main-content" tabindex="-1">
    <?php
}

function rr_render_layout_end(): void
{
    $activePage = (string) ($GLOBALS['rr_layout_active_page'] ?? 'unknown');
    $shouldRenderGolbyWidget = rr_should_render_golby_widget($activePage);
    $golbyOnboardingState = $GLOBALS['rr_golby_onboarding_state'] ?? null;

    ?>
            </main>
            <?php if (is_array($golbyOnboardingState)) : ?>
            <?php rr_render_golby_onboarding_markup($golbyOnboardingState); ?>
            <?php endif; ?>
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
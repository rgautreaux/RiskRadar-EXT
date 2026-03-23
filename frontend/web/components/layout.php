<?php

function rr_render_layout_start(string $title, string $activePage): void
{
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
    </head>
    <body>
        <div class="app-shell">
            <header class="topbar">
                <div>
                    <p class="eyebrow">CMPS 357 Web Extension</p>
                    <a class="brand" href="index.php">RiskRadar Web</a>
                </div>
                <nav class="topnav" aria-label="Primary navigation">
                    <a class="<?php echo $activePage === 'dashboard' ? 'is-active' : ''; ?>" href="index.php">
                        <img src="/wireframe_icons/dashboard.png" alt="Dashboard Icon" class="nav-icon"> Dashboard
                    </a>
                    <a class="<?php echo $activePage === 'alerts' ? 'is-active' : ''; ?>" href="alerts.php">
                        <img src="/wireframe_icons/alerts.png" alt="Alerts Icon" class="nav-icon"> Alerts
                    </a>
                    <a class="<?php echo $activePage === 'summaries' ? 'is-active' : ''; ?>" href="summaries.php">
                        <img src="/wireframe_icons/summaries.png" alt="Summaries Icon" class="nav-icon"> Summaries
                    </a>
                    <a class="<?php echo $activePage === 'profile' ? 'is-active' : ''; ?>" href="profile.php">
                        <img src="/wireframe_icons/profile.png" alt="Profile Icon" class="nav-icon"> Profile
                    </a>
                    <a class="<?php echo $activePage === 'risk' ? 'is-active' : ''; ?>" href="risk.php">
                        <img src="/wireframe_icons/risk.png" alt="Risk Icon" class="nav-icon"> Risk
                    </a>
                    <a class="<?php echo $activePage === 'map' ? 'is-active' : ''; ?>" href="map.php">
                        <img src="/wireframe_icons/map.png" alt="Map Icon" class="nav-icon"> Map
                    </a>
                    <a class="<?php echo $activePage === 'forecast' ? 'is-active' : ''; ?>" href="forecast.php">
                        <img src="/wireframe_icons/forecast.png" alt="Forecast Icon" class="nav-icon"> Forecast
                    </a>
                    <a class="<?php echo $activePage === 'assistant' ? 'is-active' : ''; ?>" href="assistant.php">
                        <img src="/wireframe_icons/assistant.png" alt="Assistant Icon" class="nav-icon"> Assistant
                    </a>
                    <a class="<?php echo $activePage === 'login' ? 'is-active' : ''; ?>" href="login.php">
                        <img src="/wireframe_icons/login.png" alt="Login Icon" class="nav-icon"> Login
                    </a>
                    <a class="<?php echo $activePage === 'register' ? 'is-active' : ''; ?>" href="register.php">
                        <img src="/wireframe_icons/register.png" alt="Register Icon" class="nav-icon"> Register
                    </a>
                </nav>
            </header>
            <main class="page-shell">
    <?php
}

function rr_render_layout_end(): void
{
    ?>
            </main>
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
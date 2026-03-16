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
                    <a class="<?php echo $activePage === 'dashboard' ? 'is-active' : ''; ?>" href="index.php">Dashboard</a>
                    <a class="<?php echo $activePage === 'alerts' ? 'is-active' : ''; ?>" href="alerts.php">Alerts</a>
                    <a class="<?php echo $activePage === 'summaries' ? 'is-active' : ''; ?>" href="summaries.php">Summaries</a>
                    <a class="<?php echo $activePage === 'profile' ? 'is-active' : ''; ?>" href="profile.php">Profile</a>
                    <a class="<?php echo $activePage === 'risk' ? 'is-active' : ''; ?>" href="risk.php">Risk</a>
                    <a class="<?php echo $activePage === 'map' ? 'is-active' : ''; ?>" href="map.php">Map</a>
                    <a class="<?php echo $activePage === 'forecast' ? 'is-active' : ''; ?>" href="forecast.php">Forecast</a>
                    <a class="<?php echo $activePage === 'assistant' ? 'is-active' : ''; ?>" href="assistant.php">Assistant</a>
                    <a class="<?php echo $activePage === 'login' ? 'is-active' : ''; ?>" href="login.php">Login</a>
                    <a class="<?php echo $activePage === 'register' ? 'is-active' : ''; ?>" href="register.php">Register</a>
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
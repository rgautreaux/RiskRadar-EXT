<?php rr_render_layout_start('Risk Score', 'risk'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Stage 2 — Personal Risk Scoring</p>
        <h1>Personal risk score</h1>
    </div>
    <p>Your personalized environmental risk score based on proximity, severity, health sensitivity, and alert density. Enter your user ID to see results.</p>
</section>

<section class="panel">
    <form class="filter-grid" method="get" action="risk.php">
        <label>
            <span>User ID</span>
            <input type="number" name="user_id" min="1" max="999999" value="<?php echo e((string) $userId); ?>" required placeholder="1">
        </label>
        <label>
            <span>Radius (km)</span>
            <input type="number" name="radius_km" min="1" max="500" value="<?php echo e((string) $radiusKm); ?>">
        </label>
        <button class="button-primary" type="submit">Calculate risk score</button>
    </form>
</section>


<?php if ($isGuest) : ?>
    <section class="panel warning-panel">
        <p class="empty-state">Guest mode: Personalized risk scoring is only available to registered users. <a href="login.php">Sign in</a> or <a href="register.php">create an account</a> for full access.</p>
    </section>
<?php elseif ($userId <= 0) : ?>
    <section class="panel">
        <p class="empty-state">Enter your user ID above to view your personalized risk score. You can find your ID on the <a href="profile.php">Profile</a> page after registering.</p>
    </section>
<?php elseif ($riskResult !== null && $riskResult['ok'] && $riskResult['data']) : ?>

    <section class="stats-grid">
        <article class="stat-card accent-coral">
            <span class="stat-label">Risk Score</span>
            <strong><?php echo e((string) ($riskResult['data']['overall_score'] ?? '0')); ?></strong>
            <p>Your personal environmental risk score (0-100).</p>
        </article>
        <article class="stat-card accent-amber">
            <span class="stat-label">Risk Level</span>
            <strong><?php echo e(ucfirst((string) ($riskResult['data']['risk_level'] ?? 'unknown'))); ?></strong>
            <p>Based on proximity, severity, health sensitivity, and alert density.</p>
        </article>
        <article class="stat-card accent-teal">
            <span class="stat-label">Nearby Alerts</span>
            <strong><?php echo e((string) ($riskResult['data']['nearby_alert_count'] ?? '0')); ?></strong>
            <p>Alerts within <?php echo e((string) $radiusKm); ?> km of your location.</p>
        </article>
    </section>

    <?php if (!empty($riskResult['data']['factors'])) : ?>
        <section class="panel">
            <h2>Risk factor breakdown</h2>
            <div class="factor-grid">
                <?php foreach ($riskResult['data']['factors'] as $factor) : ?>
                    <div class="factor-card">
                        <span class="factor-name"><?php echo e(ucfirst(str_replace('_', ' ', (string) ($factor['name'] ?? '')))); ?></span>
                        <strong class="factor-value"><?php echo e((string) ($factor['value'] ?? '0')); ?></strong>
                        <span class="factor-weight">Weight: <?php echo e((string) (($factor['weight'] ?? 0) * 100)); ?>%</span>
                        <p class="factor-desc"><?php echo e((string) ($factor['description'] ?? '')); ?></p>
                    </div>
                <?php endforeach; ?>
            </div>
        </section>
    <?php endif; ?>

    <?php if ($prioritizedResult !== null && $prioritizedResult['ok'] && !empty($prioritizedResult['data']['alerts'])) : ?>
        <section class="panel">
            <div class="panel-header">
                <div>
                    <p class="eyebrow">Quick preview</p>
                    <h2>Top prioritized alerts</h2>
                </div>
                <a href="smart_alerts.php?user_id=<?php echo e((string) $userId); ?>&radius_km=<?php echo e((string) $radiusKm); ?>">View all smart alerts</a>
            </div>
            <div class="alert-list compact-list">
                <?php foreach ($prioritizedResult['data']['alerts'] as $index => $alert) : ?>
                    <article class="alert-row">
                        <div>
                            <span class="priority-pill <?php echo e(rr_priority_class($alert['priority_level'])); ?>">#<?php echo e((string) ($index + 1)); ?></span>
                            <span class="severity-pill <?php echo e(rr_severity_class($alert['severity'])); ?>"><?php echo e(ucfirst($alert['severity'])); ?></span>
                            <h3><?php echo e($alert['title']); ?></h3>
                            <p><?php echo e($alert['location_name'] ?: 'Location unavailable'); ?> — <?php echo e((string) $alert['distance_km']); ?> km away</p>
                        </div>
                        <div class="row-meta">
                            <span>Score: <?php echo e((string) $alert['priority_score']); ?></span>
                            <span><?php echo e($alert['alert_type']); ?></span>
                        </div>
                    </article>
                <?php endforeach; ?>
            </div>
        </section>
    <?php endif; ?>

<?php elseif ($riskResult !== null) : ?>
    <?php rr_render_message($riskResult['message']); ?>
<?php endif; ?>

<?php rr_render_layout_end(); ?>

<?php rr_render_layout_start('Smart Alerts', 'smart_alerts'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Stage 2 — Smart Alert Prioritization</p>
        <h1>Prioritized alerts</h1>
    </div>
    <p>Alerts ranked by personalized priority using distance, severity, health sensitivity, and recency. Enter a user ID to see results tailored to that user's location and health profile.</p>
</section>

<section class="panel">
    <form class="filter-grid" method="get" action="smart_alerts.php">
        <label>
            <span>User ID</span>
            <input type="number" name="user_id" min="1" max="999999" value="<?php echo e((string) $userId); ?>" required placeholder="1">
        </label>
        <label>
            <span>Radius (km)</span>
            <input type="number" name="radius_km" min="1" max="500" value="<?php echo e((string) $radiusKm); ?>">
        </label>
        <label>
            <span>Limit</span>
            <input type="number" name="limit" min="1" max="200" value="<?php echo e((string) $limit); ?>">
        </label>
        <button class="button-primary" type="submit">Load prioritized alerts</button>
    </form>
</section>


<?php if ($isGuest) : ?>
    <section class="panel warning-panel">
        <p class="empty-state">Guest mode: Prioritized alerts are only available to registered users. <a href="login.php">Sign in</a> or <a href="register.php">create an account</a> for full access.</p>
    </section>
<?php elseif ($userId <= 0) : ?>
    <section class="panel">
        <p class="empty-state">Enter a user ID above to view prioritized alerts. You can find your user ID on the <a href="profile.php">Profile</a> page after registering.</p>
    </section>
<?php else : ?>

    <?php if ($prioritizedResult !== null) : ?>
        <?php rr_render_message($prioritizedResult['message']); ?>
    <?php endif; ?>

    <?php if ($riskResult !== null && $riskResult['ok'] && $riskResult['data']) : ?>
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
    <?php elseif ($riskResult !== null) : ?>
        <?php rr_render_message($riskResult['message']); ?>
    <?php endif; ?>

    <?php if ($prioritizedResult !== null && $prioritizedResult['ok'] && !empty($prioritizedResult['data']['alerts'])) : ?>
        <section class="panel">
            <div class="panel-header">
                <div>
                    <p class="eyebrow">Personalized ranking</p>
                    <h2>Alerts by priority</h2>
                </div>
                <span class="meta-chip"><?php echo e((string) count($prioritizedResult['data']['alerts'])); ?> alert(s)</span>
            </div>

            <div class="alert-list">
                <?php foreach ($prioritizedResult['data']['alerts'] as $index => $alert) : ?>
                    <article class="alert-card prioritized-card">
                        <div class="card-heading">
                            <span class="priority-pill <?php echo e(rr_priority_class($alert['priority_level'])); ?>">
                                #<?php echo e((string) ($index + 1)); ?> — <?php echo e(ucfirst($alert['priority_level'])); ?> priority
                            </span>
                            <span class="priority-score">Score: <?php echo e((string) $alert['priority_score']); ?></span>
                            <span class="severity-pill <?php echo e(rr_severity_class($alert['severity'])); ?>"><?php echo e(ucfirst($alert['severity'])); ?></span>
                            <span class="meta-chip"><?php echo e($alert['source']); ?></span>
                        </div>
                        <h2><?php echo e($alert['title']); ?></h2>
                        <p><?php echo e($alert['description'] ?: 'No description was provided by the source feed.'); ?></p>

                        <dl class="metadata-grid">
                            <div>
                                <dt>Type</dt>
                                <dd><?php echo e($alert['alert_type']); ?></dd>
                            </div>
                            <div>
                                <dt>Distance</dt>
                                <dd><?php echo e((string) $alert['distance_km']); ?> km</dd>
                            </div>
                            <div>
                                <dt>Location</dt>
                                <dd><?php echo e($alert['location_name'] ?: 'Unavailable'); ?></dd>
                            </div>
                            <div>
                                <dt>Fetched</dt>
                                <dd><?php echo e(rr_format_datetime($alert['fetched_at'])); ?></dd>
                            </div>
                        </dl>

                        <details class="priority-details">
                            <summary>Priority factor breakdown</summary>
                            <dl class="metadata-grid">
                                <div>
                                    <dt>Distance factor</dt>
                                    <dd><?php echo e((string) ($alert['priority_factors']['distance'] ?? 0)); ?></dd>
                                </div>
                                <div>
                                    <dt>Severity factor</dt>
                                    <dd><?php echo e((string) ($alert['priority_factors']['severity'] ?? 0)); ?></dd>
                                </div>
                                <div>
                                    <dt>Sensitivity factor</dt>
                                    <dd><?php echo e((string) ($alert['priority_factors']['sensitivity'] ?? 0)); ?></dd>
                                </div>
                                <div>
                                    <dt>Recency factor</dt>
                                    <dd><?php echo e((string) ($alert['priority_factors']['recency'] ?? 0)); ?></dd>
                                </div>
                            </dl>
                        </details>
                    </article>
                <?php endforeach; ?>
            </div>
        </section>
    <?php elseif ($prioritizedResult !== null && $prioritizedResult['ok']) : ?>
        <section class="panel">
            <p class="empty-state">No alerts are within the selected radius for this user, or the user's location is not set. Update your location on the <a href="profile.php">Profile</a> page.</p>
        </section>
    <?php endif; ?>

<?php endif; ?>

<?php rr_render_layout_end(); ?>


<?php
$userId = $userId ?? 0;
$radiusKm = $radiusKm ?? 150;
$limit = $limit ?? 50;
?>
<?php rr_render_layout_start('Smart Alerts', 'smart_alerts'); ?>

<?php $isGuest = (function_exists('rr_access_context') && rr_access_context() === 'guest'); ?>

<?php if ($isGuest) : ?>
    <style>
        .page-heading, .sa-filter-grid, .sa-empty-state, .sa-summary-strip, .sa-summary-cell, .panel, .risk-factor-list, .alert-row { pointer-events: none; opacity: 0.5; }
    </style>
    <div class="locked-overlay" role="dialog" aria-modal="true" aria-labelledby="lockout-title">
        <div class="locked-modal-panel">
            <div class="locked-modal-header">
                <svg class="locked-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" width="32" height="32" aria-hidden="true">
                    <rect x="3" y="11" width="18" height="10" rx="1" stroke="currentColor" stroke-width="1.5"/>
                    <path d="M7 11V8a5 5 0 0 1 10 0v3" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
                <h2 id="lockout-title" class="locked-modal-title">Feature for Registered Users Only</h2>
            </div>
            <p class="locked-modal-body">
                Personalized smart alert prioritization is available to registered users only. 
                Sign in or create a free account to unlock:
            </p>
            <ul class="locked-modal-benefits" aria-label="Benefits of registration">
                <li>Personalized risk scores based on your location</li>
                <li>Custom alerts tailored to your health preferences</li>
                <li>Priority rankings by severity and relevance</li>
                <li>Unlimited smart alerts and monitoring</li>
            </ul>
            <div class="locked-modal-actions">
                <a href="/login.php" class="button-primary" role="button">Sign In</a>
                <a href="/register.php" class="button-secondary" role="button">Create Account</a>
            </div>
        </div>
    </div>
<?php endif; ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Stage 2 — Smart Alert Prioritization</p>
        <h1>Prioritized alerts</h1>
    </div>
    <p>Alerts ranked by personalized priority using distance, severity, health sensitivity, and recency. Enter a user ID to see results tailored to that user's location and health profile.</p>
</section>


<section class="panel">
    <form class="sa-filter-grid" method="get" action="smart_alerts.php">
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

<?php if ($userId <= 0) : ?>
    <div class="sa-empty-state">
        <svg class="sa-empty-icon" viewBox="0 0 48 48" fill="none" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
            <rect x="8" y="8" width="32" height="32" rx="6" stroke="currentColor" stroke-width="2"/>
            <path d="M16 19h16M16 25h11" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <circle cx="31" cy="33" r="5" stroke="currentColor" stroke-width="2"/>
            <path d="M34.5 36.5l2.5 2.5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
        <p class="sa-empty-title">Enter your user ID to begin</p>
        <p class="sa-empty-body">Personalized alert rankings will appear here, calculated from distance, severity, health sensitivity, and recency. Find your ID on the <a href="profile.php">Profile</a> page after registering.</p>
    </div>

<?php else : ?>

    <?php if ($prioritizedResult !== null) : ?>
        <?php rr_render_message($prioritizedResult['message']); ?>
    <?php endif; ?>

    <?php if ($riskResult !== null && $riskResult['ok'] && $riskResult['data']) : ?>
        <?php
            $saScore     = (float) ($riskResult['data']['overall_score'] ?? 0);
            $saScoreDisp = number_format(min(100.0, max(0.0, $saScore)), 1);
            $saLevel     = ucfirst(strtolower((string) ($riskResult['data']['risk_level'] ?? 'unknown')));
            $saNearby    = (int) ($riskResult['data']['nearby_alert_count'] ?? 0);
        ?>
        <div class="sa-summary-strip" aria-label="Risk overview">
            <div class="sa-summary-cell">
                <p class="sa-summary-label">Risk Score</p>
                <p class="sa-summary-value"><?php echo e($saScoreDisp); ?></p>
            </div>
            <div class="sa-summary-cell">
                <p class="sa-summary-label">Risk Level</p>
                <p class="sa-summary-value"><?php echo e($saLevel); ?></p>
            </div>
            <div class="sa-summary-cell">
                <p class="sa-summary-label">Nearby Alerts</p>
                <p class="sa-summary-value"><?php echo e((string) $saNearby); ?></p>
            </div>
        </div>

        <?php if (!empty($riskResult['data']['factors'])) : ?>
            <section class="panel">
                <h2>Risk factor breakdown</h2>
                <div class="risk-factor-list" role="list">
                    <?php foreach ($riskResult['data']['factors'] as $factor) : ?>
                        <?php
                            $fVal     = (float) ($factor['value'] ?? 0);
                            $fValDisp = number_format($fVal, 1);
                            $fPct     = number_format(min(100.0, max(0.0, $fVal)), 2);
                            $fWeight  = (int) round((float) ($factor['weight'] ?? 0) * 100);
                            $fName    = ucfirst(str_replace('_', ' ', (string) ($factor['name'] ?? '')));
                            $fDesc    = (string) ($factor['description'] ?? '');
                        ?>
                        <div class="risk-factor-row" role="listitem" style="--factor-pct: <?php echo e($fPct); ?>%">
                            <div class="risk-factor-top">
                                <span class="risk-factor-name"><?php echo e($fName); ?></span>
                                <span class="risk-factor-weight"><?php echo e((string) $fWeight); ?>% weight</span>
                            </div>
                            <div class="risk-factor-bar-wrap" aria-label="<?php echo e($fName); ?> score: <?php echo e($fValDisp); ?>">
                                <div class="risk-factor-bar"></div>
                                <span class="risk-factor-value"><?php echo e($fValDisp); ?></span>
                            </div>
                            <?php if ($fDesc !== '') : ?>
                                <p class="risk-factor-desc"><?php echo e($fDesc); ?></p>
                            <?php endif; ?>
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

            <div class="sa-alert-list" role="list">
                <?php foreach ($prioritizedResult['data']['alerts'] as $index => $alert) : ?>
                    <?php $saEntryClass = 'sa-priority-' . strtolower((string) ($alert['priority_level'] ?? 'low')); ?>
                    <article class="sa-alert-entry <?php echo e($saEntryClass); ?>" role="listitem">
                        <div class="sa-rank" aria-label="Rank <?php echo e((string) ($index + 1)); ?>"><?php echo e((string) ($index + 1)); ?></div>

                        <div class="sa-alert-body">
                            <div class="sa-alert-chips">
                                <span class="priority-pill <?php echo e(rr_priority_class($alert['priority_level'])); ?>"><?php echo e(ucfirst($alert['priority_level'])); ?> priority</span>
                                <span class="severity-pill <?php echo e(rr_severity_class($alert['severity'])); ?>"><?php echo e(ucfirst($alert['severity'])); ?></span>
                                <span class="sa-source-chip"><?php echo e($alert['source']); ?></span>
                            </div>
                            <h2 class="sa-alert-title"><?php echo e($alert['title']); ?></h2>
                            <p class="sa-alert-desc"><?php echo e($alert['description'] ?: 'No description was provided by the source feed.'); ?></p>
                            <dl class="sa-alert-meta-row">
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
                        </div>

                        <div class="sa-alert-score">
                            <span class="sa-score-value"><?php echo e((string) $alert['priority_score']); ?></span>
                            <span class="sa-score-label">Priority score</span>
                        </div>

                        <details class="sa-breakdown">
                            <summary class="sa-breakdown-toggle">
                                <span>Priority factor breakdown</span>
                                <svg class="sa-chevron" viewBox="0 0 16 16" fill="none" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M4 6l4 4 4-4" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </summary>
                            <div class="sa-breakdown-grid">
                                <div class="sa-factor-cell">
                                    <span class="sa-factor-label">Distance</span>
                                    <span class="sa-factor-val"><?php echo e((string) ($alert['priority_factors']['distance'] ?? 0)); ?></span>
                                </div>
                                <div class="sa-factor-cell">
                                    <span class="sa-factor-label">Severity</span>
                                    <span class="sa-factor-val"><?php echo e((string) ($alert['priority_factors']['severity'] ?? 0)); ?></span>
                                </div>
                                <div class="sa-factor-cell">
                                    <span class="sa-factor-label">Sensitivity</span>
                                    <span class="sa-factor-val"><?php echo e((string) ($alert['priority_factors']['sensitivity'] ?? 0)); ?></span>
                                </div>
                                <div class="sa-factor-cell">
                                    <span class="sa-factor-label">Recency</span>
                                    <span class="sa-factor-val"><?php echo e((string) ($alert['priority_factors']['recency'] ?? 0)); ?></span>
                                </div>
                            </div>
                        </details>
                    </article>
                <?php endforeach; ?>
            </div>
        </section>

    <?php elseif ($prioritizedResult !== null && $prioritizedResult['ok']) : ?>
        <div class="sa-no-alerts">
            <p class="sa-no-alerts-title">No alerts in range</p>
            <p class="sa-no-alerts-body">No alerts are within the selected radius for this user, or the user's location is not set. Update your location on the <a href="profile.php">Profile</a> page.</p>
        </div>
    <?php endif; ?>

<?php endif; ?>

<?php rr_render_layout_end(); ?>

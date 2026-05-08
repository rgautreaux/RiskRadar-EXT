<?php rr_render_layout_start('Risk Score', 'risk'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Stage 2 — Personal Risk Scoring</p>
        <h1>Personal risk score</h1>
    </div>
    <p>Your personalized environmental risk score based on proximity, severity, health sensitivity, and alert density.</p>
</section>

<section class="panel">
    <form class="risk-form" method="get" action="risk.php">
        <?php if ($currentUser !== null) : ?>
            <input type="hidden" name="user_id" value="<?php echo e((string) $userId); ?>">
            <p class="risk-session-user">
                Analyzing risk for <strong><?php echo e((string) ($currentUser['display_name'] ?? $currentUser['email'] ?? 'you')); ?></strong>
            </p>
        <?php else : ?>
            <label>
                <span>User ID</span>
                <input type="number" name="user_id" min="1" max="999999" value="<?php echo e((string) $userId); ?>" required placeholder="1">
            </label>
        <?php endif; ?>
        <label>
            <span>Radius (km)</span>
            <input type="number" name="radius_km" min="1" max="500" value="<?php echo e((string) $radiusKm); ?>">
        </label>
        <button class="button-primary" type="submit">Calculate risk</button>
    </form>
</section>

<?php if ($userId <= 0) : ?>
    <div class="risk-empty-state">
        <svg class="risk-empty-icon" viewBox="0 0 48 48" fill="none" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
            <circle cx="24" cy="24" r="21" stroke="currentColor" stroke-width="2"/>
            <path d="M24 14v13M24 33v2" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
        <?php if ($currentUser !== null) : ?>
            <p class="risk-empty-title">Unable to load your user profile</p>
            <p class="risk-empty-body">Your account could not be resolved from your session. Try signing out and back in.</p>
        <?php else : ?>
            <p class="risk-empty-title">Enter your user ID to begin</p>
            <p class="risk-empty-body">Your personalized risk score will appear here, calculated from nearby alerts, severity levels, and your health sensitivity profile. Find your ID on the <a href="profile.php">Profile</a> page after registering.</p>
        <?php endif; ?>
    </div>

<?php elseif ($riskResult !== null && $riskResult['ok'] && $riskResult['data']) : ?>

    <?php
        $score     = (float) ($riskResult['data']['overall_score'] ?? 0);
        $scoreClamped = min(100.0, max(0.0, $score));
        $scoreDisp = number_format($scoreClamped, 1);
        $scorePct  = number_format($scoreClamped, 2);
        $level     = strtolower((string) ($riskResult['data']['risk_level'] ?? 'unknown'));
        $nearby    = (int) ($riskResult['data']['nearby_alert_count'] ?? 0);

        if (in_array($level, ['high', 'severe', 'extreme'], true)) {
            $levelClass = 'risk-level-high';
            $levelLabel = match ($level) {
                'extreme' => 'Extreme Risk',
                'severe'  => 'Severe Risk',
                default   => 'High Risk',
            };
        } elseif (in_array($level, ['medium', 'moderate'], true)) {
            $levelClass = 'risk-level-medium';
            $levelLabel = 'Moderate Risk';
        } else {
            $levelClass = 'risk-level-low';
            $levelLabel = 'Low Risk';
        }
    ?>

    <section class="risk-verdict <?php echo e($levelClass); ?>"
             style="--score-pct: <?php echo e($scorePct); ?>%"
             aria-label="Risk assessment result">

        <p class="eyebrow">Risk Assessment &middot; User #<?php echo e((string) $userId); ?> &middot; <?php echo e((string) $radiusKm); ?>&thinsp;km radius</p>

        <div class="risk-verdict-top">
            <div class="risk-verdict-primary">
                <p class="risk-verdict-level"><?php echo e($levelLabel); ?></p>
                <p class="risk-verdict-context">
                    Based on <?php echo e((string) $nearby); ?> alert<?php echo $nearby !== 1 ? 's' : ''; ?> within <?php echo e((string) $radiusKm); ?> km of your location
                </p>
            </div>
            <div class="risk-verdict-cells">
                <div class="risk-verdict-cell">
                    <span class="risk-verdict-cell-value"><?php echo e($scoreDisp); ?></span>
                    <span class="risk-verdict-cell-label">Score (0–100)</span>
                </div>
                <div class="risk-verdict-cell">
                    <span class="risk-verdict-cell-value"><?php echo e((string) $nearby); ?></span>
                    <span class="risk-verdict-cell-label">Nearby alerts</span>
                </div>
            </div>
        </div>

        <div class="risk-gauge" role="img" aria-label="Score gauge showing <?php echo e($scoreDisp); ?> out of 100">
            <div class="risk-gauge-track">
                <div class="risk-gauge-fill"></div>
            </div>
            <div class="risk-gauge-legend" aria-hidden="true">
                <span>0 — Low</span>
                <span>40 — Moderate</span>
                <span>70 — High</span>
                <span>100</span>
            </div>
        </div>
    </section>

    <?php if (!empty($riskResult['data']['factors'])) : ?>
        <section class="panel">
            <h2>Risk factor breakdown</h2>
            <div class="risk-factor-list" role="list">
                <?php foreach ($riskResult['data']['factors'] as $factor) : ?>
                    <?php
                        $factorVal    = (float) ($factor['value'] ?? 0);
                        $factorValDisp = number_format($factorVal, 1);
                        $factorPct    = number_format(min(100.0, max(0.0, $factorVal)), 2);
                        $factorWeight = (int) round((float) ($factor['weight'] ?? 0) * 100);
                        $factorName   = ucfirst(str_replace('_', ' ', (string) ($factor['name'] ?? '')));
                        $factorDesc   = (string) ($factor['description'] ?? '');
                    ?>
                    <div class="risk-factor-row" role="listitem" style="--factor-pct: <?php echo e($factorPct); ?>%">
                        <div class="risk-factor-top">
                            <span class="risk-factor-name"><?php echo e($factorName); ?></span>
                            <span class="risk-factor-weight"><?php echo e((string) $factorWeight); ?>% weight</span>
                        </div>
                        <div class="risk-factor-bar-wrap" aria-label="<?php echo e($factorName); ?> score: <?php echo e($factorValDisp); ?>">
                            <div class="risk-factor-bar"></div>
                            <span class="risk-factor-value"><?php echo e($factorValDisp); ?></span>
                        </div>
                        <?php if ($factorDesc !== '') : ?>
                            <p class="risk-factor-desc"><?php echo e($factorDesc); ?></p>
                        <?php endif; ?>
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
                <a class="dash-action" href="smart_alerts.php?user_id=<?php echo e((string) $userId); ?>&radius_km=<?php echo e((string) $radiusKm); ?>">View all smart alerts &rarr;</a>
            </div>
            <div class="risk-alert-log">
                <?php foreach ($prioritizedResult['data']['alerts'] as $index => $alert) : ?>
                    <div class="risk-alert-entry">
                        <div class="risk-alert-rank" aria-hidden="true"><?php echo e((string) ($index + 1)); ?></div>
                        <div class="risk-alert-body">
                            <div class="risk-alert-chips">
                                <span class="severity-pill <?php echo e(rr_severity_class($alert['severity'])); ?>"><?php echo e(ucfirst($alert['severity'])); ?></span>
                                <span class="priority-pill <?php echo e(rr_priority_class($alert['priority_level'])); ?>"><?php echo e(ucfirst($alert['priority_level'])); ?> priority</span>
                            </div>
                            <p class="risk-alert-title"><?php echo e($alert['title']); ?></p>
                            <p class="risk-alert-location"><?php echo e($alert['location_name'] ?: 'Location unavailable'); ?> &mdash; <?php echo e((string) $alert['distance_km']); ?> km away</p>
                        </div>
                        <div class="risk-alert-meta">
                            <span class="risk-alert-score">Score <?php echo e((string) $alert['priority_score']); ?></span>
                            <span class="risk-alert-type"><?php echo e($alert['alert_type']); ?></span>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        </section>
    <?php endif; ?>

<?php elseif ($riskResult !== null) : ?>
    <?php rr_render_message($riskResult['message']); ?>
<?php endif; ?>

<?php rr_render_layout_end(); ?>

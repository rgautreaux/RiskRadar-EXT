<?php rr_render_layout_start('Risk Score', 'risk'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Stage 2 kickoff scaffold</p>
        <h1>Personal Risk Scoring</h1>
    </div>
    <p>This page now consumes the planned Stage 2 routes (`users/{id}/risk-score` and `alerts/prioritized`) and will render live data once backend endpoints are implemented.</p>
</section>

<?php rr_render_message($riskScoreResult['message']); ?>
<?php rr_render_message($prioritizedAlertsResult['message']); ?>

<?php $riskData = is_array($riskScoreResult['data']) ? $riskScoreResult['data'] : []; ?>

<section class="stats-grid">
    <article class="stat-card accent-coral">
        <span class="stat-label">User ID</span>
        <strong><?php echo e((string) ($riskData['user_id'] ?? 0)); ?></strong>
        <p>Selected via query parameter `user_id` (default: 1).</p>
    </article>
    <article class="stat-card accent-amber">
        <span class="stat-label">Risk Score</span>
        <strong><?php echo e(rr_format_risk_score($riskData['score'] ?? null)); ?></strong>
        <p>0-100 normalized weighted score for Stage 2.</p>
    </article>
    <article class="stat-card accent-teal">
        <span class="stat-label">Risk Level</span>
        <strong><?php echo e(rr_risk_level_label($riskData['score'] ?? null)); ?></strong>
        <p>Derived from threshold labels in Stage 2 spec.</p>
    </article>
</section>

<section class="panel">
    <div class="panel-header">
        <div>
            <p class="eyebrow">Prioritization preview</p>
            <h2>Top prioritized alerts</h2>
        </div>
        <a href="alerts.php">Open full alerts list</a>
    </div>

    <?php if (!$prioritizedAlertsResult['data']) : ?>
        <p class="empty-state">No prioritized alerts available yet. This will populate once Stage 2 backend routes are active.</p>
    <?php else : ?>
        <div class="alert-list compact-list">
            <?php foreach ($prioritizedAlertsResult['data'] as $alert) : ?>
                <article class="alert-row">
                    <div>
                        <span class="severity-pill <?php echo e(rr_severity_class($alert['severity'])); ?>"><?php echo e(rr_priority_label($alert['urgency_label'])); ?></span>
                        <h3><?php echo e($alert['title']); ?></h3>
                        <p><?php echo e($alert['location_name'] ?: 'Location unavailable'); ?></p>
                    </div>
                    <div class="row-meta">
                        <span>Score: <?php echo e($alert['priority_score'] !== null ? number_format($alert['priority_score'], 2) : 'n/a'); ?></span>
                        <span><?php echo e(rr_format_datetime($alert['fetched_at'])); ?></span>
                    </div>
                </article>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>
</section>

<?php rr_render_layout_end(); ?>

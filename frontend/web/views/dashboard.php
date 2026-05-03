<?php rr_render_layout_start('Dashboard', 'dashboard'); ?>

<?php /* Golby Onboarding Popup (conditionally rendered) */
if (!empty($user) && !$user['has_completed_onboarding']) {
    define('GOLBY_ONBOARDING_NEEDED', true);
    include __DIR__ . '/partials/golby_onboarding_popup.html';
    echo "<script>window.GOLBY_ONBOARDING_NEEDED = true;</script>";
}

<section class="hero-panel">
    <div>
        <p class="eyebrow">Live backend snapshot</p>
        <h1 class="dash-hero-headline">
            <?php if ($total === 0): ?>
                You're clear
            <?php elseif ($total === 1): ?>
                1 alert active
            <?php else: ?>
                <?php echo e((string) $total); ?> alerts active
            <?php endif; ?>
        </h1>
        <p class="dash-hero-sub">Environmental risk snapshot for your region. Review active alerts and the latest AI-generated summary below.</p>
    </div>
    <div class="dash-hero-data">
        <div class="dash-hero-stat">
            <p class="dash-hero-stat-label">Total Alerts</p>
            <p class="dash-hero-stat-value"><?php echo e((string) $total); ?></p>
        </div>
        <div class="dash-hero-stat">
            <p class="dash-hero-stat-label">
                Loaded Alerts
                <span class="dash-tooltip-wrap">
                    <span class="dash-info" tabindex="0" aria-describedby="tooltip-loaded">ⓘ</span>
                    <span class="dash-tooltip-text" id="tooltip-loaded" role="tooltip">Alerts retrieved in this request. May be fewer than the total count if a fetch limit was applied.</span>
                </span>
            </p>
            <p class="dash-hero-stat-value"><?php echo e((string) $loadedCount); ?></p>
        </div>
    </div>
</section>

<?php rr_render_message($statsResult['message']); ?>
<?php rr_render_message($alertsResult['message']); ?>
<?php rr_render_message($latestSummaryResult['message']); ?>

<div class="dash-stat-strip">
    <div class="dash-stat-cell">
        <p class="dash-stat-cell-label">Total Alerts</p>
        <p class="dash-stat-cell-value"><?php echo e((string) $statsResult['data']['total']); ?></p>
    </div>
    <div class="dash-stat-cell">
        <p class="dash-stat-cell-label">Highest Severity</p>
        <p class="dash-stat-cell-value"><?php echo e(ucfirst($topSeverityLabel ?: '—')); ?></p>
    </div>
    <div class="dash-stat-cell">
        <p class="dash-stat-cell-label">Most Common Type</p>
        <p class="dash-stat-cell-value"><?php echo e(ucwords($topTypeLabel ?: '—')); ?></p>
    </div>
</div>

<section class="content-grid">
    <article class="panel">
        <div class="panel-header">
            <div>
                <p class="eyebrow">Overview module</p>
                <h2>Top alerts now</h2>
            </div>
            <a class="dash-action" href="alerts.php">Open alerts list &rarr;</a>
        </div>

        <?php if (!$alertsResult['data']) : ?>
            <div class="dash-empty">
                <p class="dash-empty-title">You're clear.</p>
                <p class="dash-empty-body">No active alerts in the system right now. Check back when conditions change.</p>
            </div>
        <?php else : ?>
            <div class="dash-alert-log">
                <?php foreach ($alertsResult['data'] as $alert) : ?>
                    <a class="dash-alert-entry" href="alert_detail.php?id=<?php echo e((string) $alert['id']); ?>">
                        <div>
                            <span class="severity-pill <?php echo e(rr_severity_class($alert['severity'])); ?>"><?php echo e(ucfirst($alert['severity'])); ?></span>
                            <p class="dash-alert-title"><?php echo e($alert['title']); ?></p>
                            <p class="dash-alert-location"><?php echo e($alert['location_name'] ?: 'Location unavailable'); ?></p>
                        </div>
                        <div class="dash-alert-meta">
                            <span class="dash-alert-type"><?php echo e($alert['alert_type']); ?></span>
                            <span class="dash-alert-time"><?php echo e(rr_format_datetime($alert['fetched_at'])); ?></span>
                        </div>
                    </a>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
    </article>

    <article class="panel">
        <div class="panel-header">
            <div>
                <p class="eyebrow">Summary module</p>
                <h2>Latest generated summary</h2>
            </div>
            <a class="dash-action" href="summaries.php">Browse summaries &rarr;</a>
        </div>

        <?php if (!$latestSummaryResult['data']) : ?>
            <div class="dash-empty">
                <p class="dash-empty-title">No summary yet.</p>
                <p class="dash-empty-body">Summaries are generated automatically when alerts are active. Check back once there is activity in the system.</p>
            </div>
        <?php else : ?>
            <h3 class="dash-summary-title"><?php echo e($latestSummaryResult['data']['title']); ?></h3>
            <p class="dash-summary-meta">
                <span><?php echo e($latestSummaryResult['data']['summary_type']); ?></span>
                <span><?php echo e(rr_format_datetime($latestSummaryResult['data']['generated_at'])); ?></span>
            </p>
            <p class="dash-summary-body"><?php echo nl2br(e($latestSummaryResult['data']['content'])); ?></p>
        <?php endif; ?>
    </article>
</section>

<?php rr_render_layout_end(); ?>

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
        <h1>Desktop-first environmental awareness.</h1>
        <p class="hero-copy">This dashboard combines current alert volume, severity mix, and the latest generated summary into one web-specific overview.</p>
    </div>
    <div class="hero-meta">
        <div>
            <span>Total Alerts</span>
            <strong><?php echo e((string) $statsResult['data']['total']); ?></strong>
        </div>
        <div>
            <span>Loaded Alerts</span>
            <strong><?php echo e((string) count($alertsResult['data'])); ?></strong>
        </div>
    </div>
</section>

<?php rr_render_message($statsResult['message']); ?>
<?php rr_render_message($alertsResult['message']); ?>
<?php rr_render_message($latestSummaryResult['message']); ?>

<section class="stats-grid">
    <article class="stat-card accent-coral">
        <span class="stat-label">Total Alerts</span>
        <strong><?php echo e((string) $statsResult['data']['total']); ?></strong>
        <p>Backend alert count exposed by the existing stats endpoint.</p>
    </article>
    <article class="stat-card accent-amber">
        <span class="stat-label">Highest Severity Bucket</span>
        <strong><?php echo e($topSeverityLabel); ?></strong>
        <p>Quick severity concentration check for the current feed.</p>
    </article>
    <article class="stat-card accent-teal">
        <span class="stat-label">Most Common Type</span>
        <strong><?php echo e($topTypeLabel); ?></strong>
        <p>Useful for spotting dominant environmental patterns at a glance.</p>
    </article>
</section>

<section class="content-grid">
    <article class="panel">
        <div class="panel-header">
            <div>
                <p class="eyebrow">Overview module</p>
                <h2>Top alerts now</h2>
            </div>
            <a class="content-action" href="alerts.php">Open alerts list</a>
        </div>

        <?php if (!$alertsResult['data']) : ?>
            <p class="empty-state">No alerts are available from the backend right now.</p>
        <?php else : ?>
            <div class="alert-list compact-list">
                <?php foreach ($alertsResult['data'] as $alert) : ?>
                    <article class="alert-row">
                        <div>
                            <span class="severity-pill <?php echo e(rr_severity_class($alert['severity'])); ?>"><?php echo e(ucfirst($alert['severity'])); ?></span>
                            <h3><?php echo e($alert['title']); ?></h3>
                            <p><?php echo e($alert['location_name'] ?: 'Location unavailable'); ?></p>
                        </div>
                        <div class="row-meta">
                            <span><?php echo e($alert['alert_type']); ?></span>
                            <span><?php echo e(rr_format_datetime($alert['fetched_at'])); ?></span>
                        </div>
                    </article>
                <?php endforeach; ?>
            </div>
        <?php endif; ?>
    </article>

    <article class="panel panel-feature">
        <div class="panel-header">
            <div>
                <p class="eyebrow">Summary module</p>
                <h2>Latest generated summary</h2>
            </div>
            <a class="content-action" href="summaries.php">Browse summaries</a>
        </div>

        <?php if (!$latestSummaryResult['data']) : ?>
            <p class="empty-state">No summary is currently available. The backend may not have generated one yet.</p>
        <?php else : ?>
            <h3><?php echo e($latestSummaryResult['data']['title']); ?></h3>
            <p class="summary-meta">
                <span><?php echo e($latestSummaryResult['data']['summary_type']); ?></span>
                <span><?php echo e(rr_format_datetime($latestSummaryResult['data']['generated_at'])); ?></span>
            </p>
            <p class="summary-copy"><?php echo nl2br(e($latestSummaryResult['data']['content'])); ?></p>
        <?php endif; ?>
    </article>
</section>

<?php rr_render_layout_end(); ?>
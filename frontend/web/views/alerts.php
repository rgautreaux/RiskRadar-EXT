<?php rr_render_layout_start('Alerts', 'alerts'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Alert explorer</p>
        <h1>Current alert feed</h1>
    </div>
    <p>These results come directly from the existing backend alert routes, with safe empty-state fallbacks when the API is unavailable.</p>
</section>

<?php rr_render_message($alertsResult['message']); ?>

<section class="panel">
    <form class="filter-grid" method="get" action="alerts.php">
        <label>
            <span>Alert type</span>
            <select name="alert_type">
                <option value="">All</option>
                <?php foreach (rr_allowed_alert_types() as $alertType) : ?>
                    <option value="<?php echo e($alertType); ?>" <?php echo ($filters['alert_type'] === $alertType) ? 'selected' : ''; ?>><?php echo e($alertType); ?></option>
                <?php endforeach; ?>
            </select>
        </label>
        <label>
            <span>Severity</span>
            <select name="severity">
                <option value="">All</option>
                <?php foreach (rr_allowed_severities() as $severity) : ?>
                    <option value="<?php echo e($severity); ?>" <?php echo (strtolower((string) $filters['severity']) === $severity) ? 'selected' : ''; ?>><?php echo e(ucfirst($severity)); ?></option>
                <?php endforeach; ?>
            </select>
        </label>
        <label>
            <span>Source</span>
            <input type="text" name="source" maxlength="80" value="<?php echo e((string) ($filters['source'] ?? '')); ?>" placeholder="epa">
        </label>
        <label>
            <span>Limit</span>
            <input type="number" name="limit" min="1" max="200" value="<?php echo e((string) $filters['limit']); ?>">
        </label>
        <button class="button-primary" type="submit">Apply filters</button>
    </form>
    <?php if (!$alertsResult['data']) : ?>
        <p class="empty-state">No alerts matched the selected filters.</p>
    <?php else : ?>
        <div class="alert-list">
            <?php foreach ($alertsResult['data'] as $alert) : ?>
                <article class="alert-card">
                    <div class="card-heading">
                        <span class="severity-pill <?php echo e(rr_severity_class($alert['severity'])); ?>"><?php echo e(ucfirst($alert['severity'])); ?></span>
                        <span class="meta-chip"><?php echo e($alert['source']); ?></span>
                    </div>
                    <h2><?php echo e($alert['title']); ?></h2>
                    <p><?php echo e($alert['description'] ?: 'No description was provided by the source feed.'); ?></p>
                    <p><a href="alert_detail.php?id=<?php echo e((string) $alert['id']); ?>">View full alert details</a></p>
                    <dl class="metadata-grid">
                        <div>
                            <dt>Type</dt>
                            <dd><?php echo e($alert['alert_type']); ?></dd>
                        </div>
                        <div>
                            <dt>Location</dt>
                            <dd><?php echo e($alert['location_name'] ?: 'Unavailable'); ?></dd>
                        </div>
                        <div>
                            <dt>Fetched</dt>
                            <dd><?php echo e(rr_format_datetime($alert['fetched_at'])); ?></dd>
                        </div>
                        <div>
                            <dt>Event window</dt>
                            <dd><?php echo e(rr_format_datetime($alert['event_start'])); ?> to <?php echo e(rr_format_datetime($alert['event_end'])); ?></dd>
                        </div>
                    </dl>
                </article>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>
</section>

<?php rr_render_layout_end(); ?>
<?php rr_render_layout_start('Alert Detail', 'alerts'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Alert detail</p>
        <h1><?php echo e($alert['title']); ?></h1>
    </div>
    <a class="back-link" href="alerts.php">&larr; Back to alerts</a>
</section>

<article class="panel">
    <div class="card-heading">
        <span class="severity-pill <?php echo e(rr_severity_class($alert['severity'])); ?>"><?php echo e(ucfirst($alert['severity'])); ?></span>
        <span class="meta-chip"><?php echo e($alert['source']); ?></span>
        <span class="meta-chip"><?php echo e($alert['alert_type']); ?></span>
    </div>

    <?php if ($alert['description']) : ?>
        <p><?php echo nl2br(e($alert['description'])); ?></p>
    <?php else : ?>
        <p class="empty-state">No description was provided by the source feed.</p>
    <?php endif; ?>

    <dl class="metadata-grid detail-grid">
        <div>
            <dt>Alert ID</dt>
            <dd><?php echo e((string) $alert['id']); ?></dd>
        </div>
        <div>
            <dt>Source</dt>
            <dd><?php echo e($alert['source']); ?></dd>
        </div>
        <div>
            <dt>Source ID</dt>
            <dd><?php echo e($alert['source_id'] ?: 'Unavailable'); ?></dd>
        </div>
        <div>
            <dt>Alert type</dt>
            <dd><?php echo e($alert['alert_type']); ?></dd>
        </div>
        <div>
            <dt>Severity</dt>
            <dd><?php echo e(ucfirst($alert['severity'])); ?></dd>
        </div>
        <div>
            <dt>Location</dt>
            <dd><?php echo e($alert['location_name'] ?: 'Unavailable'); ?></dd>
        </div>
        <?php if ($alert['latitude'] !== null && $alert['longitude'] !== null) : ?>
        <div>
            <dt>Coordinates</dt>
            <dd><?php echo e(number_format((float) $alert['latitude'], 4)); ?>, <?php echo e(number_format((float) $alert['longitude'], 4)); ?></dd>
        </div>
        <?php endif; ?>
        <div>
            <dt>Event start</dt>
            <dd><?php echo e(rr_format_datetime($alert['event_start'])); ?></dd>
        </div>
        <div>
            <dt>Event end</dt>
            <dd><?php echo e(rr_format_datetime($alert['event_end'])); ?></dd>
        </div>
        <div>
            <dt>Fetched</dt>
            <dd><?php echo e(rr_format_datetime($alert['fetched_at'])); ?></dd>
        </div>
        <div>
            <dt>Created</dt>
            <dd><?php echo e(rr_format_datetime($alert['created_at'])); ?></dd>
        </div>
    </dl>
</article>

<?php rr_render_layout_end(); ?>

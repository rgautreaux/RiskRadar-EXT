<?php rr_render_layout_start('Summary Detail', 'summaries'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Summary detail</p>
        <h1><?php echo e($summary['title']); ?></h1>
    </div>
    <a class="back-link" href="summaries.php">&larr; Back to summaries</a>
</section>

<article class="panel">
    <div class="card-heading">
        <span class="meta-chip"><?php echo e($summary['summary_type']); ?></span>
        <span class="meta-chip"><?php echo e(rr_format_datetime($summary['generated_at'])); ?></span>
    </div>

    <p><?php echo nl2br(e($summary['content'])); ?></p>

    <dl class="metadata-grid detail-grid">
        <div>
            <dt>Summary ID</dt>
            <dd><?php echo e((string) $summary['id']); ?></dd>
        </div>
        <div>
            <dt>Type</dt>
            <dd><?php echo e($summary['summary_type']); ?></dd>
        </div>
        <div>
            <dt>Region</dt>
            <dd><?php echo e($summary['region'] ?: 'General'); ?></dd>
        </div>
        <div>
            <dt>Model</dt>
            <dd><?php echo e($summary['model_used'] ?: 'Unavailable'); ?></dd>
        </div>
        <div>
            <dt>Generated</dt>
            <dd><?php echo e(rr_format_datetime($summary['generated_at'])); ?></dd>
        </div>
    </dl>
</article>

<?php rr_render_layout_end(); ?>

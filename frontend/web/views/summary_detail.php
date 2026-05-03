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

    <?php if ($summary['summary_insight'] || $summary['why_it_matters'] || $summary['key_takeaways'] || $summary['context_notes'] || $summary['confidence'] !== null) : ?>
    <section class="panel" style="margin-top: 1.5rem;">
        <div class="panel-header">
            <div>
                <p class="eyebrow">Golby insight</p>
                <h2>Why this summary matters</h2>
            </div>
        </div>

        <?php if ($summary['summary_insight']) : ?>
            <p><?php echo nl2br(e($summary['summary_insight'])); ?></p>
        <?php endif; ?>

        <?php if ($summary['why_it_matters']) : ?>
            <p><?php echo nl2br(e($summary['why_it_matters'])); ?></p>
        <?php endif; ?>

        <?php if ($summary['key_takeaways']) : ?>
            <h3>Key takeaways</h3>
            <ul>
                <?php foreach ($summary['key_takeaways'] as $takeaway) : ?>
                    <li><?php echo e($takeaway); ?></li>
                <?php endforeach; ?>
            </ul>
        <?php endif; ?>

        <dl class="metadata-grid detail-grid" style="margin-top: 1.25rem;">
            <?php if ($summary['context_notes']) : ?>
            <div>
                <dt>Context notes</dt>
                <dd><?php echo e($summary['context_notes']); ?></dd>
            </div>
            <?php endif; ?>
            <?php if ($summary['confidence'] !== null) : ?>
            <div>
                <dt>Confidence</dt>
                <dd><?php echo e(rr_format_confidence($summary['confidence'])); ?></dd>
            </div>
            <?php endif; ?>
        </dl>
    </section>
    <?php endif; ?>

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

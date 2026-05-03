<?php
$summariesResult = $summariesResult ?? ['data' => [], 'message' => ''];
$filters = $filters ?? ['limit' => 20];
?>
<?php rr_render_layout_start('Summaries', 'summaries'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Summary archive</p>
        <h1>Backend-generated summaries</h1>
    </div>
    <p>This page is ready for the Stage 1 read-focused summary flow and fails closed to an empty state if the API payload is missing or malformed.</p>
</section>

<?php rr_render_message($summariesResult['message']); ?>

<section class="panel">
    <form class="filter-grid summary-filter filter-bar" method="get" action="summaries.php">
        <label>
            <span>Summary type</span>
            <input type="text" name="summary_type" maxlength="80" value="<?php echo e((string) ($filters['summary_type'] ?? '')); ?>" placeholder="daily, regional, travel">
        </label>
        <label>
            <span>Limit</span>
            <input type="number" name="limit" min="1" max="50" value="<?php echo e((string) $filters['limit']); ?>">
        </label>
        <button class="button-primary" type="submit">Refresh list</button>
    </form>

    <?php if (!$summariesResult['data']) : ?>
        <p class="empty-state">No summaries are available for the current filters.</p>
    <?php else : ?>
        <div class="summary-stack">
            <?php foreach ($summariesResult['data'] as $summary) : ?>
                <article class="summary-card">
                    <div class="card-heading">
                        <span class="meta-chip"><?php echo e($summary['summary_type']); ?></span>
                        <span class="meta-chip"><?php echo e(rr_format_datetime($summary['generated_at'])); ?></span>
                        <?php if ($summary['confidence'] !== null) : ?>
                            <span class="meta-chip">Confidence: <?php echo e(rr_format_confidence($summary['confidence'])); ?></span>
                        <?php endif; ?>
                    </div>
                    <h2><?php echo e($summary['title']); ?></h2>
                    <p class="summary-copy"><?php echo nl2br(e($summary['content'])); ?></p>
                    <?php if ($summary['summary_insight'] || $summary['why_it_matters'] || $summary['key_takeaways']) : ?>
                        <section class="panel" style="margin: 1rem 0 0; padding: 1rem 1.1rem;">
                            <p class="eyebrow">Golby insight</p>
                            <?php if ($summary['summary_insight']) : ?>
                                <p class="summary-copy"><?php echo nl2br(e($summary['summary_insight'])); ?></p>
                            <?php endif; ?>
                            <?php if ($summary['why_it_matters']) : ?>
                                <p class="summary-meta-inline"><?php echo e($summary['why_it_matters']); ?></p>
                            <?php endif; ?>
                            <?php if ($summary['key_takeaways']) : ?>
                                <ul>
                                    <?php foreach ($summary['key_takeaways'] as $takeaway) : ?>
                                        <li><?php echo e($takeaway); ?></li>
                                    <?php endforeach; ?>
                                </ul>
                            <?php endif; ?>
                        </section>
                    <?php endif; ?>
                    <p><a class="content-action" href="summary_detail.php?id=<?php echo e((string) $summary['id']); ?>">Open full summary</a></p>
                    <p class="summary-meta-inline">Region: <?php echo e($summary['region'] ?: 'General'); ?> | Model: <?php echo e($summary['model_used'] ?: 'Unavailable'); ?></p>
                </article>
            <?php endforeach; ?>
        </div>
    <?php endif; ?>
</section>

<?php rr_render_layout_end(); ?>
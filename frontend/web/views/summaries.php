<?php rr_render_layout_start('Summaries', 'summaries'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Environmental briefings</p>
        <h1>Summary archive</h1>
    </div>
    <p>AI-generated environmental briefings covering air quality, weather, and regional risk conditions.</p>
</section>

<?php rr_render_message($summariesResult['message']); ?>

<form class="summ-filter-bar" method="get" action="summaries.php">
    <label class="summ-filter-field">
        <span class="summ-filter-label">Summary type</span>
        <input type="text" name="summary_type" maxlength="80" value="<?php echo e((string) ($filters['summary_type'] ?? '')); ?>" placeholder="daily, regional, travel">
    </label>
    <label class="summ-filter-field">
        <span class="summ-filter-label">Limit</span>
        <input type="number" name="limit" min="1" max="50" value="<?php echo e((string) $filters['limit']); ?>">
    </label>
    <button class="button-primary summ-filter-submit" type="submit">Refresh</button>
</form>

<?php if (!$summariesResult['data']) : ?>
    <div class="summ-empty" role="status">
        <svg class="summ-empty-icon" viewBox="0 0 48 48" fill="none" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
            <rect x="8" y="6" width="32" height="36" rx="4" stroke="currentColor" stroke-width="2"/>
            <path d="M15 16h18M15 22h16M15 28h10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <p class="summ-empty-title">No summaries found</p>
        <p class="summ-empty-body">No environmental briefings match the current filters. Try a broader summary type or increase the limit.</p>
    </div>

<?php else : ?>
    <div class="summ-list" role="list">
        <?php foreach ($summariesResult['data'] as $i => $summary) : ?>
            <article class="summ-entry" role="listitem">
                <div class="summ-index" aria-hidden="true"><?php echo str_pad((string) ($i + 1), 2, '0', STR_PAD_LEFT); ?></div>

                <div class="summ-body">
                    <div class="summ-entry-header">
                        <span class="summ-type-badge"><?php echo e($summary['summary_type']); ?></span>
                        <time class="summ-entry-time"><?php echo e(rr_format_datetime($summary['generated_at'])); ?></time>
                    </div>

                    <h2 class="summ-entry-title"><?php echo e($summary['title']); ?></h2>
                    <p class="summ-excerpt"><?php echo nl2br(e($summary['content'])); ?></p>

                    <div class="summ-footer">
                        <dl class="summ-meta">
                            <div>
                                <dt>Region</dt>
                                <dd><?php echo e($summary['region'] ?: 'General'); ?></dd>
                            </div>
                            <div>
                                <dt>Model</dt>
                                <dd><?php echo e($summary['model_used'] ?: 'Unavailable'); ?></dd>
                            </div>
                        </dl>
                        <a class="summ-entry-cta" href="summary_detail.php?id=<?php echo e((string) $summary['id']); ?>">
                            Read full briefing
                            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
                                <path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </a>
                    </div>
                </div>
            </article>
        <?php endforeach; ?>
    </div>
<?php endif; ?>

<?php rr_render_layout_end(); ?>

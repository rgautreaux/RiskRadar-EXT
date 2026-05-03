<?php rr_render_layout_start('Summary Detail', 'summaries'); ?>

<div class="sd-wrapper">

    <a class="sd-back" href="summaries.php">
        <span class="sd-back-icon" aria-hidden="true">
            <svg width="15" height="15" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M13 7.5H2M7 3L2 7.5 7 12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </span>
        Back to briefings
    </a>

    <div class="sd-masthead">
        <span class="sd-type-mark"><?php echo e($summary['summary_type']); ?></span>
        <span class="sd-sep" aria-hidden="true">·</span>
        <span class="sd-region"><?php echo e($summary['region'] ?: 'General'); ?></span>
        <time class="sd-timestamp"><?php echo e(rr_format_datetime($summary['generated_at'])); ?></time>
    </div>

    <h1 class="sd-title"><?php echo e($summary['title']); ?></h1>

    <div class="sd-rule" aria-hidden="true"></div>

    <div class="sd-body">
        <?php
        $sdParagraphs = array_filter(
            array_map('trim', preg_split('/\n{2,}/', $summary['content']))
        );
        if (empty($sdParagraphs)) {
            $sdParagraphs = [trim($summary['content'])];
        }
        foreach ($sdParagraphs as $sdPara) :
        ?>
            <p><?php echo nl2br(e($sdPara)); ?></p>
        <?php endforeach; ?>
    </div>

    <footer class="sd-provenance">
        <dl class="sd-provenance-list">
            <div class="sd-provenance-item">
                <dt>Briefing</dt>
                <dd>#<?php echo e((string) $summary['id']); ?></dd>
            </div>
            <div class="sd-provenance-item">
                <dt>Model</dt>
                <dd><?php echo e($summary['model_used'] ?: 'Unavailable'); ?></dd>
            </div>
            <div class="sd-provenance-item">
                <dt>Type</dt>
                <dd><?php echo e($summary['summary_type']); ?></dd>
            </div>
        </dl>
    </footer>

</div>

<?php rr_render_layout_end(); ?>

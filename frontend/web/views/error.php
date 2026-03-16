<?php rr_render_layout_start('Error', 'dashboard'); ?>

<section class="panel">
    <p class="eyebrow">Request status</p>
    <h1><?php echo e($errorTitle ?? 'Error'); ?></h1>
    <p><?php echo e($errorMessage ?? 'An unexpected error occurred.'); ?></p>
    <p><a class="button-primary inline-button" href="index.php">Return to dashboard</a></p>
</section>

<?php rr_render_layout_end(); ?>

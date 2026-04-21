<?php rr_render_layout_start('AI Assistant', 'assistant'); ?>

<style>
  main.page-shell {
    padding: 0 !important;
  }
</style>

<!-- Assistant Page Welcome & Chat Wrapper -->
<div id="riskradar-assistant-page-welcome"></div>

<script>
window.__RISKRADAR_API_BASE__ = <?php echo json_encode(rtrim(rr_api_url($config, ''), '/')); ?>;
</script>
<link rel="stylesheet" href="/assets/golby-widget.css">
<script type="module" src="/assets/assistant-welcome.js" defer></script>

<noscript>
  <div style="padding: 3rem 2rem; color: oklch(0.46 0.016 148); font-family: system-ui, sans-serif; max-width: 40ch;">
    <p style="margin: 0;">Golby requires JavaScript. Enable it in your browser settings and reload to continue.</p>
  </div>
</noscript>

<?php rr_render_layout_end(); ?>

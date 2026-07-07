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
  <div style="padding: 2rem; text-align: center; color: #9f1239;">
    <p><em>Golby requires JavaScript to run. Enable JavaScript and reload this page.</em></p>
  </div>
</noscript>

<?php rr_render_layout_end(); ?>

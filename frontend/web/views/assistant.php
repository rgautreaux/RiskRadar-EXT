<?php rr_render_layout_start('AI Assistant', 'assistant'); ?>

<style>
  main.page-shell {
    padding: 0 !important;
  }
</style>

<section class="panel" style="margin: 0 0 1.25rem; border-radius: 0 0 18px 18px;">
  <div class="panel-header">
    <div>
      <p class="eyebrow">Safety and privacy</p>
      <h1>How to use Golby safely</h1>
    </div>
  </div>
  <p>Golby is designed to explain alerts, summaries, and forecast context. Use it for guidance, not for sharing secrets or making emergency decisions without a second source.</p>
  <ul>
    <li>Ask about environmental risks, summary takeaways, and how to navigate RiskRadar.</li>
    <li>Do not enter passwords, API keys, or other sensitive account details into chat.</li>
    <li>Verify urgent or high-impact information in the dashboard or alert detail pages.</li>
  </ul>
</section>

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

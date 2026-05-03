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
  <div style="padding: 3rem 2rem; color: oklch(0.46 0.016 148); font-family: system-ui, sans-serif; max-width: 40ch;">
    <p style="margin: 0;">Golby requires JavaScript. Enable it in your browser settings and reload to continue.</p>
  </div>
</noscript>

<?php rr_render_layout_end(); ?>


<?php rr_render_layout_start('AI Assistant', 'assistant'); ?>

<!-- RiskRadar AI Assistant Widget Assets -->
<link rel="stylesheet" href="/public/assets/index.css">
<link rel="modulepreload" href="/public/assets/index-CbcLeLl0.js">
<script type="module" src="/public/assets/index-CbcLeLl0.js" defer></script>

<section class="page-heading">
    <div>
        <p class="eyebrow">Stage 4 scaffold</p>
        <h1>RiskRadar AI Assistant</h1>
    </div>
    <p>This Stage 4 scaffold will support natural-language risk questions and contextual recommendations from backend forecast and alert data.</p>
</section>


<section class="panel" style="max-width: 700px; margin: 0 auto; background: var(--card); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); padding: 2rem 1.5rem;">
    <div class="flex items-center gap-4 mb-4">
        <img src="/UI_UX_STYLE_FILES/wireframe_icons/RiskRadar_Assistant_Icon.png" alt="Golby AI Assistant Icon" title="RiskRadar Golby Assistant" style="width: 56px; height: 56px; border-radius: 12px; background: var(--accent); box-shadow: var(--shadow-sm);" />
        <div>
            <h2 style="margin: 0; color: var(--primary); font-family: 'Space Grotesk', Inter, Arial, sans-serif;">Meet Golby, your AI Assistant</h2>
            <p class="muted" style="margin: 0; font-size: 15px;">Ask about environmental risks, forecasts, and get personalized recommendations.</p>
        </div>
    </div>

    <!-- React AI Assistant Widget Mount Point -->
    <div id="riskradar-ai-assistant-widget"></div>
    <div class="mt-3" style="font-size: 13px; color: var(--muted-foreground);">
        <em>Note: Chat functionality will be enabled once the backend is ready.</em>
    </div>
</section>

<?php rr_render_layout_end(); ?>

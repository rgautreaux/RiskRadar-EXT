<?php rr_render_layout_start('AI Assistant', 'assistant'); ?>

<?php $currentUserResult = rr_fetch_current_user($config); ?>
<?php $currentUser = $currentUserResult['ok'] ? $currentUserResult['data'] : null; ?>
<?php $apiBase = rtrim(rr_api_url($config, ''), '/'); ?>

<script>
window.__RISKRADAR_API_BASE__ = <?php echo json_encode($apiBase); ?>;
</script>

<!-- RiskRadar AI Assistant Widget Assets -->
<link rel="stylesheet" href="/public/assets/index.css">
<link rel="modulepreload" href="/public/assets/index-CbcLeLl0.js">
<script type="module" src="/public/assets/index-CbcLeLl0.js" defer></script>
<script type="module" src="/public/assets/ai-assistant-widget.js" defer></script>

<section class="page-heading">
    <div>
        <p class="eyebrow">Stage 4 scaffold</p>
        <h1>RiskRadar AI Assistant</h1>
    </div>
    <p>This Stage 4 scaffold will support natural-language risk questions and contextual recommendations from backend forecast and alert data.</p>
</section>


<section class="panel" style="max-width: 700px; margin: 0 auto; background: var(--card); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); padding: 2rem 1.5rem;">
    <div class="flex items-center gap-4 mb-4">
        <img src="/assets/icons/ai-assistant.svg" alt="Golby AI Assistant SVG Icon" title="RiskRadar Golby Assistant" style="width: 56px; height: 56px; border-radius: 12px; background: var(--accent); box-shadow: var(--shadow-sm);" />
        <img src="/UI_UX_STYLE_FILES/wireframe_icons/RiskRadar_Assistant_Icon.png" alt="Golby AI Assistant PNG Icon" title="RiskRadar Golby Assistant" style="width: 56px; height: 56px; border-radius: 12px; background: var(--accent); box-shadow: var(--shadow-sm); margin-left: 8px;" />
        <div>
            <h2 style="margin: 0; color: var(--primary); font-family: 'Space Grotesk', Inter, Arial, sans-serif;">Meet Golby, your AI Assistant</h2>
            <p class="muted" style="margin: 0; font-size: 15px;">Ask about environmental risks, forecasts, and get personalized recommendations.</p>
        </div>
    </div>

    <!-- React AI Assistant Widget Mount Point -->
    <div
        id="riskradar-ai-assistant-widget"
        data-current-user-id="<?php echo e((string) ($currentUser['id'] ?? '')); ?>"
        data-is-admin="<?php echo e(!empty($currentUser['is_admin']) ? 'true' : 'false'); ?>"
    ></div>
    <div class="mt-3" style="font-size: 13px; color: var(--muted-foreground);">
        <em>Note: Chat functionality will be enabled once the backend is ready.</em>
    </div>
</section>

<!--
S4-07: Assistant UI Quality, Safety, and Accessibility Checklist
- [x] Golby icon/visuals integrated (SVG and PNG, alt text, contrast)
- [x] Widget mount point present and accessible
- [x] Keyboard navigation and focus management
- [x] Color contrast and font size meet accessibility standards
- [x] Error/fallback UI for assistant widget failures
- [ ] Evaluate assistant response quality and safety (manual review)
- [ ] Collect user feedback for future improvements
-->

<?php rr_render_layout_end(); ?>

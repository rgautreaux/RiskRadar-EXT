<?php rr_render_layout_start('AI Assistant', 'assistant'); ?>

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

    <!-- Chat interface scaffold -->
    <div id="assistant-chat" class="assistant-chat" style="background: var(--muted); border-radius: 10px; min-height: 180px; padding: 1.2rem; margin-bottom: 1.2rem;">
        <div class="assistant-message assistant-message--golby" style="margin-bottom: 1rem;">
            <strong>Golby:</strong> Hi! I’m Golby, your RiskRadar assistant. How can I help you today?
        </div>
        <!-- Future: Loop through chat messages here -->
    </div>
    <form id="assistant-chat-form" class="assistant-chat-form" autocomplete="off" style="display: flex; gap: 0.5rem;">
        <input type="text" name="user_message" id="user_message" placeholder="Type your question..." style="flex: 1; padding: 0.7rem 1rem; border-radius: 8px; border: 1px solid var(--muted-foreground); font-size: 15px;" aria-label="Ask Golby a question" disabled />
        <button type="submit" style="padding: 0.7rem 1.2rem; border-radius: 8px; background: var(--primary); color: #fff; font-weight: bold; border: none; font-size: 15px; opacity: 0.6; cursor: not-allowed;" disabled>Send</button>
    </form>
    <div class="mt-3" style="font-size: 13px; color: var(--muted-foreground);">
        <em>Note: Chat functionality will be enabled once the backend is ready.</em>
    </div>
</section>

<?php rr_render_layout_end(); ?>

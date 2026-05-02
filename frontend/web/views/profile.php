<?php rr_render_layout_start('Profile', 'profile'); ?>

<style>
/* ── Profile / Preferences Page ─────────────────────────────────── */

.pf {
    --pf-green:        oklch(0.52 0.15 148);
    --pf-green-mid:    oklch(0.60 0.13 148);
    --pf-green-light:  oklch(0.94 0.05 148);
    --pf-green-dark:   oklch(0.28 0.12 148);
    --pf-green-border: oklch(0.85 0.08 148);
    --pf-ink:          oklch(0.20 0.04 148);
    --pf-muted:        oklch(0.50 0.05 145);
    --pf-surface:      oklch(0.99 0.005 90);
    --pf-bg:           oklch(0.97 0.008 148);
    --pf-line:         oklch(0.91 0.015 140);

    --pf-err-fg:       oklch(0.46 0.19 25);
    --pf-err-bg:       oklch(0.97 0.04 25);
    --pf-err-border:   oklch(0.87 0.09 25);

    display: grid;
    gap: 20px;
    font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', system-ui, sans-serif;
    font-kerning: normal;
}

/* ── Back nav ──────────────────────────────────────────────────── */

.pf-back {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    width: fit-content;
    padding: 6px 0;
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: 0.01em;
    color: var(--pf-green);
    text-decoration: none;
    transition: opacity 0.15s ease-out;
}

.pf-back:hover,
.pf-back:focus-visible { opacity: 0.7; }

.pf-back:focus-visible {
    outline: 3px solid var(--pf-green);
    outline-offset: 3px;
    border-radius: 3px;
}

.pf-back svg { flex-shrink: 0; transition: transform 0.15s ease-out; }
.pf-back:hover svg { transform: translateX(-2px); }

/* ── Page header ───────────────────────────────────────────────── */

.pf-header { display: grid; gap: 8px; }

.pf-eyebrow {
    font-family: 'Geist Mono', 'Courier New', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--pf-green-mid);
    margin: 0;
}

.pf-title {
    font-family: 'Bricolage Grotesque', 'Arial Black', sans-serif;
    font-size: clamp(1.75rem, 3.5vw, 2.5rem);
    font-weight: 800;
    letter-spacing: -0.038em;
    line-height: 1.05;
    color: var(--pf-ink);
    margin: 0;
}

.pf-subtitle {
    font-size: 1rem;
    line-height: 1.62;
    color: var(--pf-muted);
    max-width: 60ch;
    margin: 0;
}

/* ── Form ──────────────────────────────────────────────────────── */

.pf-form { display: grid; gap: 12px; }

/* ── Section panels ────────────────────────────────────────────── */

.pf-section {
    padding: 28px 32px;
    background: var(--pf-surface);
    border: 1px solid var(--pf-line);
    border-radius: 20px;
    display: grid;
    gap: 22px;
}

.pf-section-head { display: grid; gap: 4px; }

.pf-section-label {
    font-family: 'Geist Mono', 'Courier New', monospace;
    font-size: 0.67rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--pf-green-mid);
    margin: 0;
}

.pf-section-title {
    font-family: 'Bricolage Grotesque', 'Arial Black', sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: -0.022em;
    color: var(--pf-ink);
    margin: 0;
}

.pf-section-desc {
    font-size: 0.9rem;
    line-height: 1.58;
    color: var(--pf-muted);
    max-width: 58ch;
    margin: 0;
}

/* ── Field layout ──────────────────────────────────────────────── */

.pf-field-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 16px;
}

.pf-field { display: grid; gap: 6px; }

.pf-field-label {
    font-size: 0.875rem;
    font-weight: 700;
    color: var(--pf-ink);
    letter-spacing: 0.005em;
}

.pf-field-error {
    font-size: 0.8125rem;
    font-weight: 700;
    color: var(--pf-err-fg);
    margin: 0;
}

/* ── Text inputs ───────────────────────────────────────────────── */

.pf-input {
    font-family: 'Geist Mono', 'Courier New', monospace;
    font-size: 0.9375rem;
    padding: 11px 14px;
    border-radius: 10px;
    border: 1px solid var(--pf-line);
    background: var(--pf-bg);
    color: var(--pf-ink);
    width: 100%;
    box-sizing: border-box;
    transition: border-color 0.15s ease-out, box-shadow 0.15s ease-out;
}

.pf-input:focus {
    outline: none;
    border-color: var(--pf-green);
    box-shadow: 0 0 0 3px oklch(0.52 0.15 148 / 0.12);
}

.pf-input::placeholder { color: var(--pf-muted); opacity: 0.65; }

/* ── Select ────────────────────────────────────────────────────── */

.pf-select {
    font-family: 'Atkinson Hyperlegible', system-ui, sans-serif;
    font-size: 0.9375rem;
    font-weight: 600;
    padding: 11px 40px 11px 14px;
    border-radius: 10px;
    border: 1px solid var(--pf-line);
    background: var(--pf-bg);
    color: var(--pf-ink);
    appearance: none;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8' fill='none'%3E%3Cpath d='M1 1.5L6 6.5L11 1.5' stroke='%23527060' stroke-width='1.75' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: right 14px center;
    cursor: pointer;
    width: 100%;
    box-sizing: border-box;
    transition: border-color 0.15s ease-out, box-shadow 0.15s ease-out;
}

.pf-select:focus {
    outline: none;
    border-color: var(--pf-green);
    box-shadow: 0 0 0 3px oklch(0.52 0.15 148 / 0.12);
}

/* ── Tile checkboxes ───────────────────────────────────────────── */

.pf-tile-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 8px;
}

.pf-tile-grid--health {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
}

.pf-tile {
    position: relative;
    display: block;
    cursor: pointer;
}

.pf-tile input[type="checkbox"] {
    position: absolute;
    opacity: 0;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0 0 0 0);
    clip-path: inset(50%);
    white-space: nowrap;
}

.pf-tile-body {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 14px;
    border: 1px solid var(--pf-line);
    border-radius: 10px;
    background: var(--pf-bg);
    color: var(--pf-muted);
    font-size: 0.875rem;
    font-weight: 600;
    line-height: 1.3;
    transition: border-color 0.12s ease-out, background 0.12s ease-out, color 0.12s ease-out;
    user-select: none;
}

.pf-tile-check {
    flex-shrink: 0;
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 1.5px solid oklch(0.78 0.04 148);
    background: var(--pf-surface);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: border-color 0.12s ease-out, background 0.12s ease-out;
}

.pf-tile-check svg { opacity: 0; transition: opacity 0.12s ease-out; }

/* Checked */
.pf-tile input:checked + .pf-tile-body {
    background: var(--pf-green-light);
    border-color: var(--pf-green-border);
    color: var(--pf-green-dark);
}

.pf-tile input:checked + .pf-tile-body .pf-tile-check {
    background: var(--pf-green);
    border-color: var(--pf-green);
}

.pf-tile input:checked + .pf-tile-body .pf-tile-check svg { opacity: 1; }

/* Focus */
.pf-tile input:focus-visible + .pf-tile-body {
    outline: 3px solid var(--pf-green);
    outline-offset: 2px;
    border-radius: 10px;
}

/* Hover */
.pf-tile:hover .pf-tile-body {
    border-color: var(--pf-green-border);
    color: var(--pf-ink);
}

/* ── Technical details (collapsed) ─────────────────────────────── */

.pf-tech {
    background: var(--pf-surface);
    border: 1px solid var(--pf-line);
    border-radius: 20px;
    overflow: hidden;
}

.pf-tech-summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 32px;
    font-family: 'Geist Mono', 'Courier New', monospace;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--pf-muted);
    cursor: pointer;
    list-style: none;
    user-select: none;
    transition: color 0.15s ease-out;
}

.pf-tech-summary::-webkit-details-marker { display: none; }
.pf-tech-summary:hover { color: var(--pf-ink); }

.pf-tech-toggle {
    font-size: 0.62rem;
    letter-spacing: 0;
    transition: transform 0.2s ease-out;
    display: inline-block;
}

.pf-tech[open] .pf-tech-toggle { transform: rotate(180deg); }

.pf-tech-body {
    padding: 0 32px 28px;
    display: grid;
    gap: 10px;
}

.pf-tech-desc {
    font-size: 0.875rem;
    color: var(--pf-muted);
    line-height: 1.56;
    margin: 0;
}

/* ── Save button ───────────────────────────────────────────────── */

.pf-actions {
    display: flex;
    align-items: center;
    gap: 16px;
    flex-wrap: wrap;
}

.pf-btn {
    font-family: 'Bricolage Grotesque', 'Arial Black', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    padding: 13px 30px;
    border-radius: 12px;
    border: none;
    background: var(--pf-green);
    color: oklch(0.98 0.005 145);
    cursor: pointer;
    transition: background 0.15s ease-out, transform 0.1s ease-out;
    line-height: 1;
}

.pf-btn:hover { background: var(--pf-green-dark); }
.pf-btn:active { transform: scale(0.98); }
.pf-btn:focus-visible {
    outline: 3px solid var(--pf-green);
    outline-offset: 3px;
}

/* ── Result panel ──────────────────────────────────────────────── */

.pf-result {
    padding: 20px 28px;
    background: var(--pf-green-light);
    border: 1px solid var(--pf-green-border);
    border-radius: 14px;
    display: grid;
    gap: 6px;
}

.pf-result-badge {
    font-family: 'Geist Mono', 'Courier New', monospace;
    font-size: 0.66rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--pf-green-mid);
}

.pf-result-row {
    font-size: 0.9375rem;
    color: var(--pf-green-dark);
    font-weight: 600;
    margin: 0;
}

.pf-result-row strong { font-weight: 800; }

/* ── Responsive ────────────────────────────────────────────────── */

@media (max-width: 640px) {
    .pf-section { padding: 20px; }
    .pf-tech-summary { padding: 16px 20px; }
    .pf-tech-body { padding: 0 20px 20px; }

    .pf-tile-grid { grid-template-columns: repeat(2, 1fr); }
    .pf-tile-grid--health { grid-template-columns: repeat(2, 1fr); }

    .pf-actions { flex-direction: column; align-items: stretch; }
    .pf-btn { text-align: center; }
}

@media (max-width: 380px) {
    .pf-tile-grid,
    .pf-tile-grid--health { grid-template-columns: 1fr; }
}
</style>

<div class="pf">

    <header class="pf-header">
        <a class="pf-back" href="dashboard.php">
            <svg width="15" height="15" viewBox="0 0 15 15" fill="none" aria-hidden="true" focusable="false">
                <path d="M9.5 11.5L5.5 7.5L9.5 3.5" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            Back to dashboard
        </a>
        <p class="pf-eyebrow">Your account</p>
        <h1 class="pf-title">Alert profile</h1>
        <p class="pf-subtitle">Configure what you want to hear about, where, and how. Your preferences shape every alert you receive.</p>
    </header>

    <?php if ($flash) : ?>
        <?php rr_render_message($flash['message'], $flash['type']); ?>
    <?php endif; ?>

    <?php if ($preferencesResult && $preferencesResult['message']) : ?>
        <?php rr_render_message($preferencesResult['message']); ?>
    <?php endif; ?>

    <form method="post" action="profile.php" class="pf-form" novalidate>
        <input type="hidden" name="csrf_token" value="<?php echo e(rr_csrf_token()); ?>">
        <input type="hidden" name="action" value="preferences">

        <!-- 01 — Identity -->
        <section class="pf-section">
            <div class="pf-section-head">
                <p class="pf-section-label">01 &mdash; Identity</p>
                <h2 class="pf-section-title">Who you are &amp; where you are</h2>
                <p class="pf-section-desc">Your user ID links these settings to your account. Your ZIP code sets your local alert area.</p>
            </div>
            <div class="pf-field-row">
                <div class="pf-field">
                    <label class="pf-field-label" for="pf-user-id">User ID</label>
                    <input
                        class="pf-input"
                        type="number"
                        id="pf-user-id"
                        name="user_id"
                        min="1"
                        value="<?php echo e((string) ($preferencesForm['user_id'] ?: '')); ?>"
                        required
                        autocomplete="off"
                    >
                    <?php if (isset($preferencesErrors['user_id'])) : ?>
                        <p class="pf-field-error"><?php echo e($preferencesErrors['user_id']); ?></p>
                    <?php endif; ?>
                </div>
                <div class="pf-field">
                    <label class="pf-field-label" for="pf-zip">ZIP code</label>
                    <input
                        class="pf-input"
                        type="text"
                        id="pf-zip"
                        name="zip_code"
                        inputmode="numeric"
                        maxlength="5"
                        placeholder="e.g. 90210"
                        value="<?php echo e((string) ($preferencesForm['zip_code'] ?? '')); ?>"
                        autocomplete="postal-code"
                    >
                    <?php if (isset($preferencesErrors['zip_code'])) : ?>
                        <p class="pf-field-error"><?php echo e($preferencesErrors['zip_code']); ?></p>
                    <?php endif; ?>
                </div>
            </div>
        </section>

        <!-- 02 — Alert types -->
        <section class="pf-section">
            <div class="pf-section-head">
                <p class="pf-section-label">02 &mdash; Alert types</p>
                <h2 class="pf-section-title">What you want to know about</h2>
                <p class="pf-section-desc">Select every category relevant to your routes and environment. Unselected types won't reach you.</p>
            </div>
            <div class="pf-tile-grid" role="group" aria-label="Alert types">
                <?php foreach (rr_allowed_alert_types() as $alertType) : ?>
                    <label class="pf-tile">
                        <input
                            type="checkbox"
                            name="alert_types[]"
                            value="<?php echo e($alertType); ?>"
                            <?php echo in_array($alertType, $preferencesForm['alert_types'], true) ? 'checked' : ''; ?>
                        >
                        <span class="pf-tile-body">
                            <span class="pf-tile-check" aria-hidden="true">
                                <svg width="10" height="8" viewBox="0 0 10 8" fill="none">
                                    <path d="M1.5 4L3.5 6.5L8.5 1.5" stroke="white" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </span>
                            <?php echo e($alertType); ?>
                        </span>
                    </label>
                <?php endforeach; ?>
            </div>
        </section>

        <!-- 03 — Severity -->
        <section class="pf-section">
            <div class="pf-section-head">
                <p class="pf-section-label">03 &mdash; Severity</p>
                <h2 class="pf-section-title">Minimum alert severity</h2>
                <p class="pf-section-desc">Filter out low-stakes alerts so only the ones that matter reach you.</p>
            </div>
            <div class="pf-field" style="max-width: 320px;">
                <label class="pf-field-label" for="pf-severity">Severity threshold</label>
                <select class="pf-select" id="pf-severity" name="notify_severity">
                    <option value="">No preference &mdash; show all</option>
                    <?php foreach (rr_allowed_severities() as $severity) : ?>
                        <option
                            value="<?php echo e($severity); ?>"
                            <?php echo (strtolower((string) $preferencesForm['notify_severity']) === $severity) ? 'selected' : ''; ?>
                        ><?php echo e(ucfirst($severity)); ?></option>
                    <?php endforeach; ?>
                </select>
                <?php if (isset($preferencesErrors['notify_severity'])) : ?>
                    <p class="pf-field-error"><?php echo e($preferencesErrors['notify_severity']); ?></p>
                <?php endif; ?>
            </div>
        </section>

        <!-- 04 — Health profile -->
        <?php
        $healthConditions = [
            'asthma'            => 'Asthma',
            'copd'              => 'COPD',
            'allergies'         => 'Allergies',
            'heart'             => 'Heart Disease',
            'elderly'           => 'Elderly',
            'pregnant'          => 'Pregnant',
            'children'          => 'Children',
            'immunocompromised' => 'Immunocompromised',
        ];
        $selectedHealth = $preferencesForm['health_conditions'] ?? [];
        ?>
        <section class="pf-section">
            <div class="pf-section-head">
                <p class="pf-section-label">04 &mdash; Health profile</p>
                <h2 class="pf-section-title">Sensitivities &amp; conditions</h2>
                <p class="pf-section-desc">Select any that apply to you or your household. RiskRadar surfaces health-relevant alerts at a lower threshold for sensitive groups.</p>
            </div>
            <div class="pf-tile-grid pf-tile-grid--health" role="group" aria-label="Health sensitivities">
                <?php foreach ($healthConditions as $key => $label) : ?>
                    <label class="pf-tile">
                        <input
                            type="checkbox"
                            name="health_conditions[]"
                            value="<?php echo e($key); ?>"
                            <?php echo in_array($key, $selectedHealth, true) ? 'checked' : ''; ?>
                        >
                        <span class="pf-tile-body">
                            <span class="pf-tile-check" aria-hidden="true">
                                <svg width="10" height="8" viewBox="0 0 10 8" fill="none">
                                    <path d="M1.5 4L3.5 6.5L8.5 1.5" stroke="white" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>
                                </svg>
                            </span>
                            <?php echo e($label); ?>
                        </span>
                    </label>
                <?php endforeach; ?>
            </div>
        </section>

        <!-- Advanced — Device token (collapsed) -->
        <details class="pf-tech">
            <summary class="pf-tech-summary">
                Advanced &mdash; Device token
                <span class="pf-tech-toggle" aria-hidden="true">&#9660;</span>
            </summary>
            <div class="pf-tech-body">
                <p class="pf-tech-desc">Your device token enables push notifications. In most cases this is set automatically — you only need to enter it manually if instructed to.</p>
                <div class="pf-field">
                    <label class="pf-field-label" for="pf-device-token">Device token</label>
                    <input
                        class="pf-input"
                        type="text"
                        id="pf-device-token"
                        name="device_token"
                        maxlength="255"
                        placeholder="Leave blank unless instructed"
                        value="<?php echo e((string) ($preferencesForm['device_token'] ?? '')); ?>"
                        autocomplete="off"
                    >
                </div>
            </div>
        </details>

        <!-- Save -->
        <div class="pf-actions">
            <button class="pf-btn" type="submit">Save preferences</button>
        </div>

    </form>

    <?php if ($preferencesResult && $preferencesResult['ok'] && $preferencesResult['data']) : ?>
        <div class="pf-result" role="status" aria-live="polite">
            <p class="pf-result-badge">Preferences saved</p>
            <p class="pf-result-row">Updated user: <strong>#<?php echo e((string) $preferencesResult['data']['id']); ?></strong></p>
            <p class="pf-result-row">Alert types: <?php echo e(implode(', ', rr_parse_alert_types($preferencesResult['data']['alert_types'])) ?: 'None selected'); ?></p>
        </div>
    <?php endif; ?>

</div>

<?php rr_render_layout_end(); ?>

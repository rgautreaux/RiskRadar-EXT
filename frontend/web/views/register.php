<?php rr_render_layout_start('Create account', 'register'); ?>

<?php
// Initialize variables to prevent undefined warnings
$flash = isset($flash) ? $flash : null;
$registerForm = isset($registerForm) ? $registerForm : [];
$registerResult = isset($registerResult) ? $registerResult : null;
$registerErrors = isset($registerErrors) ? $registerErrors : [];
?>

<style>
/* ─── Font imports ────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,700&family=Atkinson+Hyperlegible+Next:wght@400;700&display=swap');

/* ─── Page-level shell overrides ─────────────────────────────────── */
body.page-register {
    background: oklch(0.26 0.045 148);
    min-height: 100vh;
}

body.page-register .app-shell {
    padding: 16px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

body.page-register .topbar {
    background: oklch(0.32 0.06 148 / 0.6);
    border-color: oklch(0.40 0.07 148 / 0.45);
    backdrop-filter: blur(12px);
    flex-shrink: 0;
}

body.page-register .brand {
    color: oklch(0.93 0.025 148);
    font-family: 'Bricolage Grotesque', sans-serif;
}

body.page-register .eyebrow {
    color: #1a202c;
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
}

body.page-register .page-shell {
    flex: 1;
    max-width: 100%;
    margin: 0;
    display: flex;
    align-items: stretch;
    padding: 0;
    gap: 0;
}

/* ─── Two-column split ────────────────────────────────────────────── */
.reg-split {
    display: grid;
    grid-template-columns: 42fr 58fr;
    width: 100%;
    border-radius: 18px;
    overflow: hidden;
    min-height: clamp(580px, calc(100vh - 116px), 940px);
}

/* ─── Brand panel (left) ──────────────────────────────────────────── */
.reg-brand {
    background: oklch(0.38 0.115 148);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: clamp(36px, 4.5vw, 64px) clamp(32px, 4vw, 56px);
    position: relative;
    overflow: hidden;
}

.reg-brand::before {
    content: '';
    position: absolute;
    inset: -40px;
    background:
        radial-gradient(circle at 20% 15%, oklch(0.46 0.12 148 / 0.45) 0%, transparent 52%),
        radial-gradient(circle at 85% 80%, oklch(0.28 0.09 148 / 0.58) 0%, transparent 44%);
    pointer-events: none;
}

.reg-brand-content {
    position: relative;
    z-index: 1;
}

.reg-brand-eyebrow {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.6875rem;
    font-weight: 400;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: oklch(0.72 0.075 148);
    margin: 0 0 44px;
}

.reg-brand-headline {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: clamp(2.4rem, 3.8vw, 3.6rem);
    font-weight: 700;
    line-height: 1.02;
    letter-spacing: -0.03em;
    color: oklch(0.96 0.018 148);
    margin: 0 0 24px;
}

.reg-brand-body {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 1rem;
    line-height: 1.72;
    color: oklch(0.83 0.052 148);
    max-width: 32ch;
    margin: 0;
}

/* ─── Feature callouts ────────────────────────────────────────────── */
.reg-features {
    position: relative;
    z-index: 1;
    display: flex;
    flex-direction: column;
    gap: 0;
}

.reg-feature {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 14px 0;
    border-top: 1px solid oklch(0.46 0.09 148 / 0.5);
}

.reg-feature:last-child {
    border-bottom: 1px solid oklch(0.46 0.09 148 / 0.5);
}

.reg-feature-num {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 0.6875rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: oklch(0.58 0.075 148);
    flex-shrink: 0;
    width: 20px;
    padding-top: 0.2em;
}

.reg-feature-text {
    flex: 1;
}

.reg-feature-label {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.9rem;
    font-weight: 700;
    color: oklch(0.92 0.025 148);
    margin: 0 0 2px;
    line-height: 1.3;
}

.reg-feature-desc {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.8125rem;
    color: oklch(0.74 0.048 148);
    margin: 0;
    line-height: 1.45;
}

/* ─── Form panel (right) ──────────────────────────────────────────── */
.reg-form-panel {
    background: oklch(0.97 0.009 100);
    display: flex;
    align-items: center;
    padding: clamp(36px, 5vw, 72px) clamp(36px, 6vw, 96px);
}

.reg-form-inner {
    width: 100%;
    max-width: 400px;
}

.reg-form-heading {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.875rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.1;
    color: oklch(0.20 0.025 148);
    margin: 0 0 6px;
}

.reg-form-sub {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.9375rem;
    color: oklch(0.36 0.025 148);
    margin: 0 0 32px;
    line-height: 1.5;
}

/* ─── Flash / form-level messages ─────────────────────────────────── */
.reg-message {
    padding: 12px 16px;
    border-radius: 8px;
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-bottom: 24px;
    border: 1px solid transparent;
}

.reg-message-warning,
.reg-message-error {
    background: oklch(0.95 0.025 25);
    color: oklch(0.33 0.18 25);
    border-color: oklch(0.83 0.075 25);
}

.reg-message-success {
    background: oklch(0.94 0.04 148);
    color: oklch(0.28 0.09 148);
    border-color: oklch(0.78 0.075 148);
}

/* ─── Form fields ─────────────────────────────────────────────────── */
.reg-field {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-bottom: 18px;
}

.reg-label {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.875rem;
    font-weight: 700;
    color: oklch(0.22 0.022 148);
    letter-spacing: 0.01em;
    display: flex;
    align-items: center;
    gap: 7px;
}

.reg-label-optional {
    font-weight: 400;
    font-size: 0.8125rem;
    color: oklch(0.48 0.018 148);
    letter-spacing: 0;
}

.reg-input {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 1rem;
    padding: 11px 15px;
    border-radius: 7px;
    border: 1.5px solid oklch(0.80 0.018 148);
    background: oklch(0.99 0.004 100);
    color: oklch(0.20 0.025 148);
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
    width: 100%;
    box-sizing: border-box;
    -webkit-appearance: none;
    appearance: none;
}

.reg-input:hover {
    border-color: oklch(0.60 0.05 148);
}

.reg-input:focus {
    outline: none;
    border-color: oklch(0.38 0.115 148);
    box-shadow: 0 0 0 3px oklch(0.38 0.115 148 / 0.18);
}

.reg-input:focus-visible {
    outline: 2.5px solid oklch(0.38 0.115 148);
    outline-offset: 1px;
}

.reg-input[aria-invalid="true"] {
    border-color: oklch(0.70 0.13 25);
}

.reg-field-error {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.8125rem;
    color: oklch(0.36 0.18 25);
    margin: 0;
    line-height: 1.4;
}

.reg-field-hint {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.8125rem;
    color: oklch(0.46 0.022 148);
    margin: 0;
    line-height: 1.4;
}

/* ─── Password show/hide wrapper ──────────────────────────────────── */
.reg-pw-wrap {
    position: relative;
}

.reg-pw-wrap .reg-input {
    padding-right: 46px;
}

.reg-pw-toggle {
    position: absolute;
    right: 11px;
    top: 50%;
    transform: translateY(-50%);
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
    color: oklch(0.50 0.028 148);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    transition: color 0.12s ease;
    line-height: 0;
}

.reg-pw-toggle:hover {
    color: oklch(0.30 0.06 148);
}

.reg-pw-toggle:focus-visible {
    outline: 2px solid oklch(0.38 0.115 148);
    outline-offset: 2px;
}

/* ─── Password strength meter ────────────────────────────────────── */
.reg-pw-strength {
    display: flex;
    gap: 4px;
    height: 3px;
    margin-top: 1px;
}

.reg-pw-strength-bar {
    flex: 1;
    background: oklch(0.88 0.010 148);
    border-radius: 2px;
    transition: background 0.22s ease;
}

.reg-pw-strength[data-strength="1"] .reg-pw-strength-bar:nth-child(1) {
    background: oklch(0.56 0.17 25);
}

.reg-pw-strength[data-strength="2"] .reg-pw-strength-bar:nth-child(-n+2) {
    background: oklch(0.60 0.14 65);
}

.reg-pw-strength[data-strength="3"] .reg-pw-strength-bar {
    background: oklch(0.52 0.12 148);
}

/* ─── Primary button ──────────────────────────────────────────────── */
.reg-btn-primary {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    padding: 13px 20px;
    border-radius: 7px;
    border: none;
    background: oklch(0.38 0.115 148);
    color: oklch(0.97 0.009 100);
    cursor: pointer;
    width: 100%;
    transition: background 0.15s ease, box-shadow 0.15s ease, transform 0.1s ease;
    margin-top: 10px;
    letter-spacing: 0.01em;
}

.reg-btn-primary:hover {
    background: oklch(0.44 0.125 148);
    box-shadow: 0 4px 14px oklch(0.38 0.115 148 / 0.30);
}

.reg-btn-primary:active {
    transform: translateY(1px);
    box-shadow: none;
}

.reg-btn-primary:focus-visible {
    outline: 2.5px solid oklch(0.38 0.115 148);
    outline-offset: 3px;
}

/* ─── Footer link ─────────────────────────────────────────────────── */
.reg-foot {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.875rem;
    color: oklch(0.38 0.022 148);
    margin: 24px 0 0;
    text-align: center;
}

.reg-foot a {
    color: oklch(0.34 0.115 148);
    font-weight: 700;
    text-decoration: none;
}

.reg-foot a:hover {
    text-decoration: underline;
    text-underline-offset: 0.2em;
}

.reg-foot a:focus-visible {
    outline: 2px solid oklch(0.38 0.115 148);
    outline-offset: 2px;
    border-radius: 2px;
}

/* ─── Reduced motion ──────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
    .reg-btn-primary,
    .reg-input,
    .reg-pw-strength-bar,
    .reg-pw-toggle {
        transition: none;
    }
}

/* ─── Responsive: tablet ──────────────────────────────────────────── */
@media (max-width: 860px) {
    .reg-split {
        grid-template-columns: 1fr;
        min-height: auto;
    }

    .reg-brand {
        padding: 36px 32px;
        gap: 32px;
        min-height: 280px;
    }

    .reg-brand-body {
        max-width: 52ch;
    }

    .reg-features {
        flex-direction: row;
        flex-wrap: wrap;
        gap: 0 24px;
    }

    .reg-feature {
        flex: 1 1 180px;
        border-bottom: none;
        padding: 12px 0;
    }

    .reg-form-panel {
        padding: 48px 36px;
    }

    .reg-form-inner {
        max-width: 100%;
    }
}

/* ─── Responsive: mobile ──────────────────────────────────────────── */
@media (max-width: 480px) {
    body.page-register .app-shell {
        padding: 8px;
        gap: 8px;
    }

    .reg-split {
        border-radius: 12px;
    }

    .reg-brand {
        padding: 28px 24px;
        min-height: 220px;
    }

    .reg-brand-eyebrow {
        margin-bottom: 28px;
    }

    .reg-brand-headline {
        font-size: 2rem;
    }

    .reg-features {
        flex-direction: column;
    }

    .reg-feature {
        min-width: unset;
        flex: unset;
        border-bottom: none;
    }

    .reg-feature:last-child {
        border-bottom: 1px solid oklch(0.46 0.09 148 / 0.5);
    }

    .reg-form-panel {
        padding: 36px 24px;
    }
}
</style>

<div class="reg-split">

    <!-- Left: brand panel -->
    <div class="reg-brand" aria-hidden="true">
        <div class="reg-brand-content">
            <p class="reg-brand-eyebrow">Free to join &middot; No credit card needed</p>
            <h1 class="reg-brand-headline">Your safety<br>profile<br>starts here.</h1>
            <p class="reg-brand-body">Personalized hazard alerts for your routes and locations &mdash; air quality, wildfires, storm warnings, and more.</p>
        </div>

        <div class="reg-features">
            <div class="reg-feature">
                <span class="reg-feature-num">01</span>
                <div class="reg-feature-text">
                    <p class="reg-feature-label">Personalized to your area</p>
                    <p class="reg-feature-desc">Your ZIP sets the default &mdash; alerts relevant to where you actually are.</p>
                </div>
            </div>
            <div class="reg-feature">
                <span class="reg-feature-num">02</span>
                <div class="reg-feature-text">
                    <p class="reg-feature-label">5+ live data sources</p>
                    <p class="reg-feature-desc">NWS, AQI, USGS, and more &mdash; aggregated and updated in real time.</p>
                </div>
            </div>
            <div class="reg-feature">
                <span class="reg-feature-num">03</span>
                <div class="reg-feature-text">
                    <p class="reg-feature-label">Risk in under 10 seconds</p>
                    <p class="reg-feature-desc">Know if conditions are safe before you leave &mdash; no scrolling required.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- Right: form panel -->
    <div class="reg-form-panel">
        <div class="reg-form-inner">

            <h2 class="reg-form-heading">Create your account</h2>
            <p class="reg-form-sub">Join free &mdash; takes under 2 minutes.</p>

            <?php if ($flash) : ?>
                <div class="reg-message reg-message-<?php echo e($flash['type'] ?? 'warning'); ?>" role="alert">
                    <?php echo e($flash['message']); ?>
                </div>
            <?php endif; ?>

            <?php if ($registerResult && $registerResult['message']) : ?>
                <div class="reg-message reg-message-warning" role="alert">
                    <?php echo e($registerResult['message']); ?>
                </div>
            <?php endif; ?>

            <form method="post" action="register.php" novalidate>
                <input type="hidden" name="csrf_token" value="<?php echo e(rr_csrf_token()); ?>">

                <div class="reg-field">
                    <label class="reg-label" for="reg-display-name">Display name</label>
                    <input
                        class="reg-input"
                        type="text"
                        id="reg-display-name"
                        name="display_name"
                        maxlength="80"
                        autocomplete="name"
                        value="<?php echo e($registerForm['display_name']); ?>"
                        required
                        <?php if (isset($registerErrors['display_name'])) : ?>aria-describedby="reg-display-name-error" aria-invalid="true"<?php endif; ?>
                    >
                    <?php if (isset($registerErrors['display_name'])) : ?>
                        <p class="reg-field-error" id="reg-display-name-error" role="alert"><?php echo e($registerErrors['display_name']); ?></p>
                    <?php endif; ?>
                </div>

                <div class="reg-field">
                    <label class="reg-label" for="reg-email">Email</label>
                    <input
                        class="reg-input"
                        type="email"
                        id="reg-email"
                        name="email"
                        maxlength="120"
                        autocomplete="email"
                        value="<?php echo e($registerForm['email']); ?>"
                        required
                        <?php if (isset($registerErrors['email'])) : ?>aria-describedby="reg-email-error" aria-invalid="true"<?php endif; ?>
                    >
                    <?php if (isset($registerErrors['email'])) : ?>
                        <p class="reg-field-error" id="reg-email-error" role="alert"><?php echo e($registerErrors['email']); ?></p>
                    <?php endif; ?>
                </div>

                <div class="reg-field">
                    <label class="reg-label" for="reg-password">Password</label>
                    <div class="reg-pw-wrap">
                        <input
                            class="reg-input"
                            type="password"
                            id="reg-password"
                            name="password"
                            minlength="8"
                            autocomplete="new-password"
                            required
                            <?php if (isset($registerErrors['password'])) : ?>aria-describedby="reg-password-error" aria-invalid="true"<?php else : ?>aria-describedby="reg-pw-hint"<?php endif; ?>
                        >
                        <button type="button" class="reg-pw-toggle" id="reg-pw-toggle" aria-label="Show password">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" id="reg-pw-icon">
                                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                                <circle cx="12" cy="12" r="3"/>
                            </svg>
                        </button>
                    </div>
                    <div class="reg-pw-strength" id="reg-pw-strength" aria-hidden="true">
                        <div class="reg-pw-strength-bar"></div>
                        <div class="reg-pw-strength-bar"></div>
                        <div class="reg-pw-strength-bar"></div>
                    </div>
                    <?php if (isset($registerErrors['password'])) : ?>
                        <p class="reg-field-error" id="reg-password-error" role="alert"><?php echo e($registerErrors['password']); ?></p>
                    <?php else : ?>
                        <p class="reg-field-hint" id="reg-pw-hint">Minimum 8 characters.</p>
                    <?php endif; ?>
                </div>

                <div class="reg-field">
                    <label class="reg-label" for="reg-zip">
                        ZIP code
                        <span class="reg-label-optional">optional</span>
                    </label>
                    <input
                        class="reg-input"
                        type="text"
                        id="reg-zip"
                        name="zip_code"
                        inputmode="numeric"
                        maxlength="5"
                        autocomplete="postal-code"
                        placeholder="e.g. 90210"
                        value="<?php echo e((string) ($registerForm['zip_code'] ?? '')); ?>"
                        <?php if (isset($registerErrors['zip_code'])) : ?>aria-describedby="reg-zip-error" aria-invalid="true"<?php else : ?>aria-describedby="reg-zip-hint"<?php endif; ?>
                    >
                    <?php if (isset($registerErrors['zip_code'])) : ?>
                        <p class="reg-field-error" id="reg-zip-error" role="alert"><?php echo e($registerErrors['zip_code']); ?></p>
                    <?php else : ?>
                        <p class="reg-field-hint" id="reg-zip-hint">Tailors your dashboard to local hazards. You can change this later.</p>
                    <?php endif; ?>
                </div>

                <button class="reg-btn-primary" type="submit">Create my RiskRadar account</button>
            </form>

            <p class="reg-foot">Already have an account? <a href="login.php">Sign in</a></p>

        </div>
    </div>

</div>

<script>
(function () {
    var pwInput   = document.getElementById('reg-password');
    var pwToggle  = document.getElementById('reg-pw-toggle');
    var pwIcon    = document.getElementById('reg-pw-icon');
    var pwStrength = document.getElementById('reg-pw-strength');

    if (!pwInput || !pwToggle || !pwIcon || !pwStrength) return;

    var EYE_OPEN = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
    var EYE_CLOSED = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>';

    pwToggle.addEventListener('click', function () {
        var showing = pwInput.type === 'text';
        pwInput.type = showing ? 'password' : 'text';
        pwToggle.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
        pwIcon.innerHTML = showing ? EYE_OPEN : EYE_CLOSED;
    });

    function getStrength(pw) {
        if (pw.length === 0) return 0;
        var score = 0;
        if (pw.length >= 8)  score++;
        if (pw.length >= 12) score++;
        if (/[A-Z]/.test(pw) && /[0-9!@#$%^&*()\-_=+]/.test(pw)) score++;
        return Math.min(score, 3);
    }

    pwInput.addEventListener('input', function () {
        var s = getStrength(this.value);
        pwStrength.setAttribute('data-strength', s > 0 ? String(s) : '');
    });
}());
</script>

<?php rr_render_layout_end(); ?>

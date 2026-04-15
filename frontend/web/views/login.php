<?php rr_render_layout_start('Sign in', 'login'); ?>

<style>
/* ─── Font imports ────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,700&family=Atkinson+Hyperlegible+Next:wght@400;700&display=swap');

/* ─── Page-level shell overrides ─────────────────────────────────── */
body.page-login {
    background: oklch(0.26 0.045 148);
    min-height: 100vh;
}

body.page-login .app-shell {
    padding: 16px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

body.page-login .topbar {
    background: oklch(0.32 0.06 148 / 0.6);
    border-color: oklch(0.40 0.07 148 / 0.45);
    backdrop-filter: blur(12px);
    flex-shrink: 0;
}

body.page-login .brand {
    color: oklch(0.93 0.025 148);
    font-family: 'Bricolage Grotesque', sans-serif;
}

body.page-login .eyebrow {
    color: oklch(0.60 0.07 148);
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
}

body.page-login .page-shell {
    flex: 1;
    max-width: 100%;
    margin: 0;
    display: flex;
    align-items: stretch;
    padding: 0;
    gap: 0;
}

/* ─── Two-column split ────────────────────────────────────────────── */
.auth-split {
    display: grid;
    grid-template-columns: 42fr 58fr;
    width: 100%;
    border-radius: 18px;
    overflow: hidden;
    min-height: clamp(520px, calc(100vh - 116px), 860px);
}

/* ─── Brand panel (left) ──────────────────────────────────────────── */
.auth-brand {
    background: oklch(0.38 0.115 148);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: clamp(36px, 4.5vw, 64px) clamp(32px, 4vw, 56px);
    position: relative;
    overflow: hidden;
}

.auth-brand::before {
    content: '';
    position: absolute;
    inset: -40px;
    background:
        radial-gradient(circle at 78% 18%, oklch(0.46 0.12 148 / 0.5) 0%, transparent 52%),
        radial-gradient(circle at 12% 88%, oklch(0.30 0.09 148 / 0.55) 0%, transparent 44%);
    pointer-events: none;
}

.auth-brand-content {
    position: relative;
    z-index: 1;
}

.auth-brand-eyebrow {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.6875rem;
    font-weight: 400;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: oklch(0.72 0.075 148);
    margin: 0 0 44px;
}

.auth-brand-headline {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: clamp(2.6rem, 4vw, 4rem);
    font-weight: 700;
    line-height: 1.02;
    letter-spacing: -0.03em;
    color: oklch(0.96 0.018 148);
    margin: 0 0 28px;
}

.auth-brand-body {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 1rem;
    line-height: 1.72;
    color: oklch(0.83 0.052 148);
    max-width: 34ch;
    margin: 0;
}

.auth-brand-foot {
    position: relative;
    z-index: 1;
    padding: 18px 22px;
    background: oklch(0.30 0.085 148);
    border-radius: 10px;
}

.auth-brand-foot-label {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.6875rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: oklch(0.62 0.068 148);
    margin: 0 0 5px;
}

.auth-brand-foot-text {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.9rem;
    color: oklch(0.87 0.042 148);
    margin: 0;
    line-height: 1.5;
}

/* ─── Form panel (right) ──────────────────────────────────────────── */
.auth-form-panel {
    background: oklch(0.97 0.009 100);
    display: flex;
    align-items: center;
    padding: clamp(36px, 5vw, 80px) clamp(36px, 6vw, 96px);
}

.auth-form-inner {
    width: 100%;
    max-width: 380px;
}

.auth-form-heading {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: 1.875rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.1;
    color: oklch(0.20 0.025 148);
    margin: 0 0 6px;
}

.auth-form-sub {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.9375rem;
    color: oklch(0.36 0.025 148);
    margin: 0 0 36px;
    line-height: 1.5;
}

/* ─── Flash / form-level messages ─────────────────────────────────── */
.auth-message {
    padding: 12px 16px;
    border-radius: 8px;
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.9rem;
    line-height: 1.5;
    margin-bottom: 24px;
    border: 1px solid transparent;
}

.auth-message-warning,
.auth-message-error {
    background: oklch(0.95 0.025 25);
    color: oklch(0.33 0.18 25);
    border-color: oklch(0.83 0.075 25);
}

.auth-message-success {
    background: oklch(0.94 0.04 148);
    color: oklch(0.28 0.09 148);
    border-color: oklch(0.78 0.075 148);
}

/* ─── Form fields ─────────────────────────────────────────────────── */
.auth-field {
    display: flex;
    flex-direction: column;
    gap: 6px;
    margin-bottom: 20px;
}

.auth-label {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.875rem;
    font-weight: 700;
    color: oklch(0.26 0.022 148);
    letter-spacing: 0.01em;
}

.auth-input {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 1rem;
    padding: 11px 15px;
    border-radius: 7px;
    border: 1.5px solid oklch(0.80 0.018 148);
    background: oklch(0.99 0.004 100);
    color: oklch(0.20 0.025 148);
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
    width: 100%;
    -webkit-appearance: none;
    appearance: none;
}

.auth-input:hover {
    border-color: oklch(0.60 0.05 148);
}

.auth-input:focus {
    outline: none;
    border-color: oklch(0.38 0.115 148);
    box-shadow: 0 0 0 3px oklch(0.38 0.115 148 / 0.18);
}

.auth-input:focus-visible {
    outline: 2.5px solid oklch(0.38 0.115 148);
    outline-offset: 1px;
}

.auth-input[aria-invalid="true"] {
    border-color: oklch(0.70 0.13 25);
}

.auth-field-error {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.8125rem;
    color: oklch(0.36 0.18 25);
    margin: 0;
    line-height: 1.4;
}

/* ─── Primary button ──────────────────────────────────────────────── */
.auth-btn-primary {
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
    margin-top: 8px;
    letter-spacing: 0.01em;
}

.auth-btn-primary:hover {
    background: oklch(0.44 0.125 148);
    box-shadow: 0 4px 14px oklch(0.38 0.115 148 / 0.30);
}

.auth-btn-primary:active {
    transform: translateY(1px);
    box-shadow: none;
}

.auth-btn-primary:focus-visible {
    outline: 2.5px solid oklch(0.38 0.115 148);
    outline-offset: 3px;
}

/* ─── Divider ─────────────────────────────────────────────────────── */
.auth-divider {
    display: flex;
    align-items: center;
    gap: 14px;
    margin: 24px 0;
}

.auth-divider-line {
    flex: 1;
    height: 1px;
    background: oklch(0.88 0.012 148);
}

.auth-divider-label {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.8125rem;
    color: oklch(0.40 0.018 148);
    white-space: nowrap;
}

/* ─── Ghost button (guest) ────────────────────────────────────────── */
.auth-btn-ghost {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.9375rem;
    font-weight: 400;
    padding: 12px 20px;
    border-radius: 7px;
    border: 1.5px solid oklch(0.78 0.018 148);
    background: transparent;
    color: oklch(0.36 0.045 148);
    cursor: pointer;
    width: 100%;
    transition: border-color 0.15s ease, background 0.15s ease, color 0.15s ease;
}

.auth-btn-ghost:hover {
    border-color: oklch(0.55 0.055 148);
    background: oklch(0.93 0.014 148);
    color: oklch(0.26 0.045 148);
}

.auth-btn-ghost:active {
    transform: translateY(1px);
}

.auth-btn-ghost:focus-visible {
    outline: 2.5px solid oklch(0.38 0.115 148);
    outline-offset: 3px;
}

/* ─── Footer ──────────────────────────────────────────────────────── */
.auth-foot {
    font-family: 'Atkinson Hyperlegible Next', sans-serif;
    font-size: 0.875rem;
    color: oklch(0.38 0.022 148);
    margin: 24px 0 0;
}

.auth-foot a {
    color: oklch(0.34 0.115 148);
    font-weight: 700;
    text-decoration: none;
}

.auth-foot a:hover {
    text-decoration: underline;
    text-underline-offset: 0.2em;
}

.auth-foot a:focus-visible {
    outline: 2px solid oklch(0.38 0.115 148);
    outline-offset: 2px;
    border-radius: 2px;
}

/* ─── Reduced motion ──────────────────────────────────────────────── */
@media (prefers-reduced-motion: reduce) {
    .auth-btn-primary,
    .auth-btn-ghost,
    .auth-input {
        transition: none;
    }
}

/* ─── Responsive: tablet ──────────────────────────────────────────── */
@media (max-width: 820px) {
    .auth-split {
        grid-template-columns: 1fr;
        min-height: auto;
    }

    .auth-brand {
        padding: 36px 32px;
        gap: 32px;
        min-height: 240px;
    }

    .auth-brand-body {
        max-width: 52ch;
    }

    .auth-form-panel {
        padding: 48px 36px;
    }

    .auth-form-inner {
        max-width: 100%;
    }
}

/* ─── Responsive: mobile ──────────────────────────────────────────── */
@media (max-width: 480px) {
    body.page-login .app-shell {
        padding: 8px;
        gap: 8px;
    }

    .auth-split {
        border-radius: 12px;
    }

    .auth-brand {
        padding: 28px 24px;
        gap: 24px;
        min-height: 200px;
    }

    .auth-brand-eyebrow {
        margin-bottom: 28px;
    }

    .auth-brand-headline {
        font-size: 2rem;
    }

    .auth-form-panel {
        padding: 36px 24px;
    }
}
</style>

<div class="auth-split">

    <!-- Left: brand panel -->
    <div class="auth-brand" aria-hidden="true">
        <div class="auth-brand-content">
            <p class="auth-brand-eyebrow">Environmental risk intelligence</p>
            <h1 class="auth-brand-headline">Know before<br>you go.</h1>
            <p class="auth-brand-body">Aggregated hazard data — air quality, weather advisories, wildfire conditions — presented clearly for the people who depend on safe conditions.</p>
        </div>
        <div class="auth-brand-foot">
            <p class="auth-brand-foot-label">Live data</p>
            <p class="auth-brand-foot-text">Pulling from NWS, AQI, USGS, and 5+ environmental sources in real time.</p>
        </div>
    </div>

    <!-- Right: form panel -->
    <div class="auth-form-panel">
        <div class="auth-form-inner">

            <h2 class="auth-form-heading">Sign in</h2>
            <p class="auth-form-sub">Access your environmental risk dashboard.</p>

            <?php if ($flash) : ?>
                <div class="auth-message auth-message-<?php echo e($flash['type'] ?? 'warning'); ?>" role="alert">
                    <?php echo e($flash['message']); ?>
                </div>
            <?php endif; ?>

            <?php if (isset($loginErrors['_form'])) : ?>
                <div class="auth-message auth-message-error" role="alert">
                    <?php echo e($loginErrors['_form']); ?>
                </div>
            <?php endif; ?>

            <form method="post" action="login.php" novalidate>
                <input type="hidden" name="csrf_token" value="<?php echo e(rr_csrf_token()); ?>">
                <input type="hidden" name="action" value="login">

                <div class="auth-field">
                    <label class="auth-label" for="login-email">Email</label>
                    <input
                        class="auth-input"
                        type="email"
                        id="login-email"
                        name="email"
                        maxlength="120"
                        autocomplete="email"
                        value="<?php echo e($loginForm['email']); ?>"
                        required
                        <?php if (isset($loginErrors['email'])) : ?>aria-describedby="login-email-error" aria-invalid="true"<?php endif; ?>
                    >
                    <?php if (isset($loginErrors['email'])) : ?>
                        <p class="auth-field-error" id="login-email-error" role="alert"><?php echo e($loginErrors['email']); ?></p>
                    <?php endif; ?>
                </div>

                <div class="auth-field">
                    <label class="auth-label" for="login-password">Password</label>
                    <input
                        class="auth-input"
                        type="password"
                        id="login-password"
                        name="password"
                        minlength="8"
                        autocomplete="current-password"
                        required
                        <?php if (isset($loginErrors['password'])) : ?>aria-describedby="login-password-error" aria-invalid="true"<?php endif; ?>
                    >
                    <?php if (isset($loginErrors['password'])) : ?>
                        <p class="auth-field-error" id="login-password-error" role="alert"><?php echo e($loginErrors['password']); ?></p>
                    <?php endif; ?>
                </div>

                <button class="auth-btn-primary" type="submit">Sign in to RiskRadar</button>
            </form>

            <div class="auth-divider" aria-hidden="true">
                <span class="auth-divider-line"></span>
                <span class="auth-divider-label">or</span>
                <span class="auth-divider-line"></span>
            </div>

            <form method="post" action="login.php">
                <input type="hidden" name="csrf_token" value="<?php echo e(rr_csrf_token()); ?>">
                <button class="auth-btn-ghost" type="submit" name="action" value="guest">
                    Continue as guest
                </button>
            </form>

            <p class="auth-foot">No account? <a href="register.php">Create one &mdash; it&rsquo;s free</a></p>

        </div>
    </div>

</div>

<?php rr_render_layout_end(); ?>

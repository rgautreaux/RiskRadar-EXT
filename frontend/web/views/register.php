<?php
// Route guard: Only allow access if coming from login.php (via HTTP_REFERER)
if (!isset($_SERVER['HTTP_REFERER']) || strpos($_SERVER['HTTP_REFERER'], 'login.php') === false) {
    header('Location: login.php');
    exit();
}
rr_render_layout_start('Register', 'register'); ?>

<section class="auth-wrap">
    <article class="auth-panel panel">
        <div class="panel-header">
            <div>
                <p class="eyebrow">New account</p>
                <h1>Create a RiskRadar account</h1>
            </div>
        </div>

        <?php if ($flash) : ?>
            <?php rr_render_message($flash['message'], $flash['type']); ?>
        <?php endif; ?>

        <?php if ($registerResult && $registerResult['message']) : ?>
            <?php rr_render_message($registerResult['message']); ?>
        <?php endif; ?>

        <form method="post" action="register.php" class="form-stack">
            <input type="hidden" name="csrf_token" value="<?php echo e(rr_csrf_token()); ?>">
            <label>
                <span>Display name</span>
                <input type="text" name="display_name" maxlength="80" autocomplete="name" value="<?php echo e($registerForm['display_name']); ?>" required>
                <?php if (isset($registerErrors['display_name'])) : ?><small class="field-error"><?php echo e($registerErrors['display_name']); ?></small><?php endif; ?>
            </label>
            <label>
                <span>Email</span>
                <input type="email" name="email" maxlength="120" autocomplete="email" value="<?php echo e($registerForm['email']); ?>" required>
                <?php if (isset($registerErrors['email'])) : ?><small class="field-error"><?php echo e($registerErrors['email']); ?></small><?php endif; ?>
            </label>
            <label>
                <span>Password</span>
                <input type="password" name="password" minlength="8" autocomplete="new-password" required>
                <?php if (isset($registerErrors['password'])) : ?><small class="field-error"><?php echo e($registerErrors['password']); ?></small><?php endif; ?>
            </label>
            <label>
                <span>ZIP code <small>(optional)</small></span>
                <input type="text" name="zip_code" inputmode="numeric" maxlength="5" autocomplete="postal-code" value="<?php echo e((string) ($registerForm['zip_code'] ?? '')); ?>">
                <?php if (isset($registerErrors['zip_code'])) : ?><small class="field-error"><?php echo e($registerErrors['zip_code']); ?></small><?php endif; ?>
            </label>
            <button class="button-primary" type="submit">Create account</button>
        </form>

        <p class="auth-foot">Already have an account? <a href="login.php">Sign in</a></p>
    </article>
</section>

<?php rr_render_layout_end(); ?>

<?php rr_render_layout_start('Login', 'login'); ?>

<section class="auth-wrap">
    <article class="auth-panel panel">
        <div class="panel-header">
            <div>
                <p class="eyebrow">Account access</p>
                <h1>Sign in to RiskRadar</h1>
            </div>
        </div>

        <?php if ($flash) : ?>
            <?php rr_render_message($flash['message'], $flash['type']); ?>
        <?php endif; ?>

        <?php if (isset($loginErrors['_form'])) : ?>
            <?php rr_render_message($loginErrors['_form']); ?>
        <?php endif; ?>

        <form method="post" action="login.php" class="form-stack">
            <input type="hidden" name="csrf_token" value="<?php echo e(rr_csrf_token()); ?>">
            <label>
                <span>Username</span>
                <input type="text" name="username" maxlength="120" autocomplete="username" value="<?php echo e($loginForm['username']); ?>" required>
                <?php if (isset($loginErrors['username'])) : ?><small class="field-error"><?php echo e($loginErrors['username']); ?></small><?php endif; ?>
            </label>
            <label>
                <span>Password</span>
                <input type="password" name="password" minlength="8" autocomplete="current-password" required>
                <?php if (isset($loginErrors['password'])) : ?><small class="field-error"><?php echo e($loginErrors['password']); ?></small><?php endif; ?>
            </label>
            <label>
                <span>ZIP code <small>(optional)</small></span>
                <input type="text" name="zip_code" inputmode="numeric" maxlength="5" autocomplete="postal-code" value="<?php echo e((string) ($loginForm['zip_code'] ?? '')); ?>">
                <?php if (isset($loginErrors['zip_code'])) : ?><small class="field-error"><?php echo e($loginErrors['zip_code']); ?></small><?php endif; ?>
            </label>
            <button class="button-primary" type="submit">Sign in</button>
        </form>

        <p class="auth-foot">Don&rsquo;t have an account? <a href="register.php">Create one</a></p>
    </article>
</section>

<?php rr_render_layout_end(); ?>

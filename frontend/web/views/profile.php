<?php rr_render_layout_start('Profile', 'profile'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">User pathways</p>
        <h1>Registration and preferences</h1>
    </div>
    <p>This Stage 1 page keeps the write-path scaffolding in place for user registration and preference updates against the existing backend.</p>
</section>

<?php if ($flash) : ?>
    <?php rr_render_message($flash['message'], $flash['type']); ?>
<?php endif; ?>

<?php if ($registerResult && $registerResult['message']) : ?>
    <?php rr_render_message($registerResult['message']); ?>
<?php endif; ?>

<?php if ($preferencesResult && $preferencesResult['message']) : ?>
    <?php rr_render_message($preferencesResult['message']); ?>
<?php endif; ?>

<section class="two-column-grid">
    <article class="panel">
        <div class="panel-header">
            <div>
                <p class="eyebrow">Write path</p>
                <h2>Register user</h2>
            </div>
        </div>
        <form method="post" action="profile.php" class="form-stack">
            <input type="hidden" name="csrf_token" value="<?php echo e(rr_csrf_token()); ?>">
            <input type="hidden" name="action" value="register">
            <label>
                <span>Display name</span>
                <input type="text" name="display_name" maxlength="80" value="<?php echo e($registerForm['display_name']); ?>" required>
                <?php if (isset($registerErrors['display_name'])) : ?><small class="field-error"><?php echo e($registerErrors['display_name']); ?></small><?php endif; ?>
            </label>
            <label>
                <span>Email</span>
                <input type="email" name="email" maxlength="120" value="<?php echo e($registerForm['email']); ?>" required>
                <?php if (isset($registerErrors['email'])) : ?><small class="field-error"><?php echo e($registerErrors['email']); ?></small><?php endif; ?>
            </label>
            <label>
                <span>Password</span>
                <input type="password" name="password" minlength="8" required>
                <?php if (isset($registerErrors['password'])) : ?><small class="field-error"><?php echo e($registerErrors['password']); ?></small><?php endif; ?>
            </label>
            <label>
                <span>ZIP code</span>
                <input type="text" name="zip_code" inputmode="numeric" maxlength="5" value="<?php echo e((string) ($registerForm['zip_code'] ?? '')); ?>">
                <?php if (isset($registerErrors['zip_code'])) : ?><small class="field-error"><?php echo e($registerErrors['zip_code']); ?></small><?php endif; ?>
            </label>
            <button class="button-primary" type="submit">Create account</button>
        </form>
        <?php if ($registerResult && $registerResult['ok'] && $registerResult['data']) : ?>
            <div class="result-panel">
                <p>Created user ID: <strong><?php echo e((string) $registerResult['data']['id']); ?></strong></p>
                <p>Created at: <?php echo e(rr_format_datetime($registerResult['data']['created_at'])); ?></p>
            </div>
        <?php endif; ?>
    </article>

    <article class="panel">
        <div class="panel-header">
            <div>
                <p class="eyebrow">Write path</p>
                <h2>Update preferences</h2>
            </div>
        </div>
        <form method="post" action="profile.php" class="form-stack">
            <input type="hidden" name="csrf_token" value="<?php echo e(rr_csrf_token()); ?>">
            <input type="hidden" name="action" value="preferences">
            <label>
                <span>User ID</span>
                <input type="number" name="user_id" min="1" value="<?php echo e((string) ($preferencesForm['user_id'] ?: '')); ?>" required>
                <?php if (isset($preferencesErrors['user_id'])) : ?><small class="field-error"><?php echo e($preferencesErrors['user_id']); ?></small><?php endif; ?>
            </label>
            <label>
                <span>ZIP code</span>
                <input type="text" name="zip_code" inputmode="numeric" maxlength="5" value="<?php echo e((string) ($preferencesForm['zip_code'] ?? '')); ?>">
                <?php if (isset($preferencesErrors['zip_code'])) : ?><small class="field-error"><?php echo e($preferencesErrors['zip_code']); ?></small><?php endif; ?>
            </label>
            <fieldset>
                <legend>Alert types</legend>
                <div class="checkbox-grid">
                    <?php foreach (rr_allowed_alert_types() as $alertType) : ?>
                        <label class="checkbox-item">
                            <input type="checkbox" name="alert_types[]" value="<?php echo e($alertType); ?>" <?php echo in_array($alertType, $preferencesForm['alert_types'], true) ? 'checked' : ''; ?>>
                            <span><?php echo e($alertType); ?></span>
                        </label>
                    <?php endforeach; ?>
                </div>
            </fieldset>
            <label>
                <span>Minimum severity</span>
                <select name="notify_severity">
                    <option value="">No preference</option>
                    <?php foreach (rr_allowed_severities() as $severity) : ?>
                        <option value="<?php echo e($severity); ?>" <?php echo (strtolower((string) $preferencesForm['notify_severity']) === $severity) ? 'selected' : ''; ?>><?php echo e(ucfirst($severity)); ?></option>
                    <?php endforeach; ?>
                </select>
                <?php if (isset($preferencesErrors['notify_severity'])) : ?><small class="field-error"><?php echo e($preferencesErrors['notify_severity']); ?></small><?php endif; ?>
            </label>
            <label>
                <span>Device token</span>
                <input type="text" name="device_token" maxlength="255" value="<?php echo e((string) ($preferencesForm['device_token'] ?? '')); ?>">
            </label>
            <button class="button-primary" type="submit">Save preferences</button>
        </form>

        <?php if ($preferencesResult && $preferencesResult['ok'] && $preferencesResult['data']) : ?>
            <div class="result-panel">
                <p>Updated user: <strong><?php echo e((string) $preferencesResult['data']['id']); ?></strong></p>
                <p>Stored alert types: <?php echo e(implode(', ', rr_parse_alert_types($preferencesResult['data']['alert_types'])) ?: 'None'); ?></p>
            </div>
        <?php endif; ?>
    </article>
</section>

<?php rr_render_layout_end(); ?>
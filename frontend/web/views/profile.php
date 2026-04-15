<?php rr_render_layout_start('Profile', 'profile'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">User preferences</p>
        <h1>Profile preferences</h1>
    </div>
    <p>Use this page to manage alert preferences for an existing user account. Account creation now lives on the dedicated registration page.</p>
</section>

<?php if ($flash) : ?>
    <?php rr_render_message($flash['message'], $flash['type']); ?>
<?php endif; ?>

<?php if ($preferencesResult && $preferencesResult['message']) : ?>
    <?php rr_render_message($preferencesResult['message']); ?>
<?php endif; ?>

<section class="panel">
        <div class="panel-header">
            <div>
                <p class="eyebrow">Write path</p>
                <h2>Update preferences</h2>
            </div>
        </div>
        <form method="post" action="profile.php" class="form-stack">
            <input type="hidden" name="csrf_token" value="<?php echo e(rr_csrf_token()); ?>">
            <input type="hidden" name="action" value="preferences">
            <div class="readonly-userid">
                <span>User ID</span>
                <span class="userid-value" style="font-family:monospace;font-weight:bold;"> 
                    <?php echo isset($currentUser) ? e((string)$currentUser['id']) : '<em>Unknown</em>'; ?>
                </span>
                <small class="field-help">This is your unique User ID. Use it for features that require UserID entry (e.g., Risk Scoring).</small>
            </div>
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
                <small class="field-help">For advanced users: enter your device's push notification token if you want to receive alerts on this device. Leave blank if unsure.</small>
            </label>
            <fieldset>
                <legend>Health sensitivities/preferences</legend>
                <div class="checkbox-grid">
                    <?php
                    // Define available health conditions (should match backend logic)
                    $healthConditions = [
                        'asthma' => 'Asthma',
                        'copd' => 'COPD',
                        'allergies' => 'Allergies',
                        'heart' => 'Heart Disease',
                        'elderly' => 'Elderly',
                        'pregnant' => 'Pregnant',
                        'children' => 'Children',
                        'immunocompromised' => 'Immunocompromised',
                    ];
                    $selectedHealth = $preferencesForm['health_conditions'] ?? [];
                    ?>
                    <?php foreach ($healthConditions as $key => $label) : ?>
                        <label class="checkbox-item">
                            <input type="checkbox" name="health_conditions[]" value="<?php echo e($key); ?>" <?php echo in_array($key, $selectedHealth, true) ? 'checked' : ''; ?>>
                            <span><?php echo e($label); ?></span>
                        </label>
                    <?php endforeach; ?>
                </div>
            </fieldset>
            <button class="button-primary" type="submit">Save preferences</button>
        </form>

        <?php if ($preferencesResult && $preferencesResult['ok'] && $preferencesResult['data']) : ?>
            <div class="result-panel">
                <p>Updated user: <strong><?php echo e((string) $preferencesResult['data']['id']); ?></strong></p>
                <p>Stored alert types: <?php echo e(implode(', ', rr_parse_alert_types($preferencesResult['data']['alert_types'])) ?: 'None'); ?></p>
            </div>
        <?php endif; ?>
</section>

<?php rr_render_layout_end(); ?>
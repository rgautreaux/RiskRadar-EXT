
<?php
$flash = $flash ?? null;
$preferencesForm = $preferencesForm ?? ['alert_types' => [], 'notify_severity' => 'moderate'];
?>
<?php rr_render_layout_start('Profile', 'profile'); ?>

<?php $isGuest = (function_exists('rr_access_context') && rr_access_context() === 'guest'); ?>

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
    <?php if ($isGuest): ?>
        <div class="locked-overlay">
            <div class="locked-message" aria-hidden="false">
                <div class="locked-header">
                    <img src="assets/icons/warning.svg" alt="Locked feature" class="locked-svg" />
                    <div>
                        <strong>User-Only Feature</strong>
                        <button class="info-button" aria-describedby="profile-lockout-info" aria-label="Why is this locked?">
                            <img src="assets/icons/info.svg" alt="Info" class="info-svg" />
                        </button>
                    </div>
                </div>
                <p class="locked-text">You’re currently exploring as a guest. Sign in or create a free account to unlock profile management, health preferences, and more!</p>
                <div class="locked-actions">
                    <a href="login.php" class="button-secondary" aria-label="Sign in to unlock">Sign In to Unlock</a>
                    <a href="register.php" class="button-primary" aria-label="Create account">Create Account</a>
                </div>
            </div>
        </div>
        <form class="form-stack locked" onsubmit="showLockoutPopup(); return false;" aria-disabled="true">
            <div class="readonly-userid">
                <span>User ID</span>
                <span class="userid-value" style="font-family:monospace;font-weight:bold;"> 
                    <em>Guest</em>
                </span>
                <small class="field-help">Sign in to get your unique User ID for personalized features.</small>
            </div>
            <label>
                <span>ZIP code</span>
                <input type="text" name="zip_code" inputmode="numeric" maxlength="5" value="" disabled>
            </label>
            <fieldset>
                <legend>Alert types</legend>
                <div class="checkbox-grid">
                    <?php foreach (rr_allowed_alert_types() as $alertType) : ?>
                        <label class="checkbox-item">
                            <input type="checkbox" name="alert_types[]" value="<?php echo e($alertType); ?>" disabled>
                            <span><?php echo e($alertType); ?></span>
                        </label>
                    <?php endforeach; ?>
                </div>
            </fieldset>
            <label>
                <span>Minimum severity</span>
                <select name="notify_severity" disabled>
                    <option value="">No preference</option>
                    <?php foreach (rr_allowed_severities() as $severity) : ?>
                        <option value="<?php echo e($severity); ?>"><?php echo e(ucfirst($severity)); ?></option>
                    <?php endforeach; ?>
                </select>
            </label>
            <label>
                <span>Device token</span>
                <input type="text" name="device_token" maxlength="255" value="" disabled>
                <small class="field-help">Sign in to enable device notifications.</small>
            </label>
            <fieldset>
                <legend>Health sensitivities/preferences</legend>
                <div class="checkbox-grid">
                    <?php
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
                    ?>
                    <?php foreach ($healthConditions as $key => $label) : ?>
                        <label class="checkbox-item">
                            <input type="checkbox" name="health_conditions[]" value="<?php echo e($key); ?>" disabled>
                            <span><?php echo e($label); ?></span>
                        </label>
                    <?php endforeach; ?>
                </div>
            </fieldset>
            <button class="button-primary" type="submit" disabled>Save preferences</button>
        </form>
        <script>
        // Reuse lockout dialog helper if available, otherwise fallback to alert
        (function(){
            function tryShow() {
                if (window.showLockoutDialog) {
                    window.showLockoutDialog();
                } else {
                    alert('Sign in or create an account to unlock profile management, health preferences, and more!');
                }
            }
            window.showLockoutPopup = tryShow;
            // attach info button inline info (non-modal)
            document.addEventListener('click', function(e){
                const t = e.target;
                if (t.closest && t.closest('.info-button')){
                    e.preventDefault();
                    const id = 'profile-inline-info';
                    if (document.getElementById(id)) return;
                    const el = document.createElement('div');
                    el.id = id;
                    el.className = 'inline-lockout-info';
                    el.setAttribute('role','status');
                    el.innerText = 'Profiles and saved preferences require an account so we can store settings for you.';
                    t.closest('.locked-message').appendChild(el);
                    setTimeout(()=> el.remove(), 8000);
                }
            });
        })();
        </script>
    <?php else: ?>
        <div class="panel-header">
            <div>
                <p class="eyebrow">Write path</p>
                <h2>Update preferences</h2>
            </div>
        </div>
        <form method="post" action="profile.php" class="form-stack" id="profile-form">
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
            <fieldset>
                <legend>Golby assistant personality (optional)</legend>
                <p class="field-help">Tune how Golby communicates with you. These settings shape the assistant's tone, detail level, and style.</p>
                <div class="personality-grid">
                    <div class="personality-slider-group">
                        <label for="warmth">
                            <span>Warmth</span>
                            <small class="slider-hint" id="warmth-hint">Neutral</small>
                        </label>
                        <input type="range" id="warmth" name="personality_warmth" min="0" max="100" value="55" class="personality-slider" data-hint="warmth-hint">
                        <small class="field-help">Friendly ← → Professional</small>
                    </div>
                    <div class="personality-slider-group">
                        <label for="calmness">
                            <span>Calmness</span>
                            <small class="slider-hint" id="calmness-hint">Calm</small>
                        </label>
                        <input type="range" id="calmness" name="personality_calmness" min="0" max="100" value="70" class="personality-slider" data-hint="calmness-hint">
                        <small class="field-help">Energetic ← → Calm</small>
                    </div>
                    <div class="personality-slider-group">
                        <label for="humor">
                            <span>Humor</span>
                            <small class="slider-hint" id="humor-hint">Minimal</small>
                        </label>
                        <input type="range" id="humor" name="personality_humor" min="0" max="100" value="35" class="personality-slider" data-hint="humor-hint">
                        <small class="field-help">Serious ← → Playful</small>
                    </div>
                    <div class="personality-slider-group">
                        <label for="conciseness">
                            <span>Conciseness</span>
                            <small class="slider-hint" id="conciseness-hint">Balanced</small>
                        </label>
                        <input type="range" id="conciseness" name="personality_conciseness" min="0" max="100" value="65" class="personality-slider" data-hint="conciseness-hint">
                        <small class="field-help">Detailed ← → Concise</small>
                    </div>
                    <div class="personality-slider-group">
                        <label for="detail">
                            <span>Detail Level</span>
                            <small class="slider-hint" id="detail-hint">Balanced</small>
                        </label>
                        <input type="range" id="detail" name="personality_detail" min="0" max="100" value="45" class="personality-slider" data-hint="detail-hint">
                        <small class="field-help">Quick ← → Thorough</small>
                    </div>
                </div>
                <input type="hidden" id="personality_profile_json" name="personality_profile_json" value="">
            </fieldset>
            <button class="button-primary" type="submit">Save preferences</button>
        </form>

        <?php if ($preferencesResult && $preferencesResult['ok'] && $preferencesResult['data']) : ?>
            <div class="result-panel">
                <p>Updated user: <strong><?php echo e((string) $preferencesResult['data']['id']); ?></strong></p>
                <p>Stored alert types: <?php echo e(implode(', ', rr_parse_alert_types($preferencesResult['data']['alert_types'])) ?: 'None'); ?></p>
            </div>
        <?php endif; ?>
        <script>
        (function() {
            const hintMap = {
                'warmth': ['Cold', 'Distant', 'Neutral', 'Friendly', 'Warm'],
                'calmness': ['Energetic', 'Lively', 'Balanced', 'Tranquil', 'Calm'],
                'humor': ['Serious', 'Dry', 'Neutral', 'Witty', 'Playful'],
                'conciseness': ['Detailed', 'Elaborate', 'Balanced', 'Brief', 'Concise'],
                'detail': ['Quick', 'Surface', 'Balanced', 'Thorough', 'Deep']
            };

            function updateHint(sliderId) {
                const slider = document.getElementById(sliderId);
                if (!slider) return;
                const hintId = slider.dataset.hint;
                if (!hintId) return;
                const hintEl = document.getElementById(hintId);
                if (!hintEl) return;

                const value = parseInt(slider.value, 10);
                const hints = hintMap[sliderId] || ['Low', 'Medium-Low', 'Medium', 'Medium-High', 'High'];
                const index = Math.floor((value / 100) * (hints.length - 1));
                hintEl.textContent = hints[Math.min(index, hints.length - 1)];
            }

            function serializePersonality() {
                const warmth = (parseInt(document.getElementById('warmth')?.value || '55', 10) / 100) * 0.45 + 0.55;
                const calmness = (parseInt(document.getElementById('calmness')?.value || '70', 10) / 100) * 0.3 + 0.7;
                const humor = (parseInt(document.getElementById('humor')?.value || '35', 10) / 100) * 0.7;
                const conciseness = (parseInt(document.getElementById('conciseness')?.value || '65', 10) / 100) * 0.35 + 0.65;
                const detail = (parseInt(document.getElementById('detail')?.value || '45', 10) / 100) * 0.55;

                const profile = {
                    tone: {
                        warmth: Math.round(warmth * 10000) / 10000,
                        calmness: Math.round(calmness * 10000) / 10000,
                        humor: Math.round(humor * 10000) / 10000
                    },
                    delivery: {
                        conciseness: Math.round(conciseness * 10000) / 10000,
                        detail: Math.round(detail * 10000) / 10000,
                        expandability: 0.5
                    },
                    voice: {
                        formality: Math.round((1 - warmth + conciseness) / 2 * 10000) / 10000
                    },
                    learning: {
                        feedback_count: 0,
                        last_feedback_at: null
                    }
                };

                return profile;
            }

            function handleFormSubmit(e) {
                const profile = serializePersonality();
                document.getElementById('personality_profile_json').value = JSON.stringify(profile);
            }

            // Attach slider listeners for hint updates
            document.querySelectorAll('.personality-slider').forEach(slider => {
                slider.addEventListener('input', function() {
                    updateHint(this.id);
                });
                // Initialize hint
                updateHint(slider.id);
            });

            // Attach form submit listener
            const form = document.getElementById('profile-form');
            if (form) {
                form.addEventListener('submit', handleFormSubmit);
            }
        })();
        </script>
    <?php endif; ?>
</section>

<?php rr_render_layout_end(); ?>
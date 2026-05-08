<?php rr_render_layout_start('Generate Briefing', 'summaries'); ?>

<div class="csg-wrapper">

    <a class="sd-back" href="summaries.php">
        <span class="sd-back-icon" aria-hidden="true">
            <svg width="15" height="15" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M13 7.5H2M7 3L2 7.5 7 12" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        </span>
        Back to summaries
    </a>

    <header class="csg-header">
        <p class="eyebrow">AI briefings</p>
        <h1 class="csg-title">Generate a new briefing</h1>
        <p class="csg-description">RiskRadar will analyze recent environmental alerts and produce a new safety digest using AI.</p>
    </header>

    <div class="csg-action-zone" id="csg-zone" data-csg-state="ready">

        <!-- Ready state -->
        <div class="csg-state" id="csg-ready">

            <!-- Scope selector -->
            <div class="csg-scope-selector" role="group" aria-label="Briefing scope">
                <button class="csg-scope-opt csg-scope-opt--active" id="csg-scope-nationwide" type="button" aria-pressed="true">
                    <span class="csg-scope-label">Nationwide</span>
                    <span class="csg-scope-detail">All active alerts across the US</span>
                </button>
                <button class="csg-scope-opt" id="csg-scope-local" type="button" aria-pressed="false">
                    <span class="csg-scope-label">Local digest</span>
                    <span class="csg-scope-detail">Alerts within your zip code area</span>
                </button>
            </div>

            <!-- Zip code zone — slides in when Local is selected -->
            <div class="csg-zip-zone" id="csg-zip-zone">
                <div class="csg-zip-inner">
                    <label class="csg-zip-label" for="csg-zip-input">Zip code</label>
                    <input
                        class="csg-zip-input"
                        id="csg-zip-input"
                        type="text"
                        inputmode="numeric"
                        pattern="[0-9]{5}"
                        maxlength="5"
                        placeholder="e.g. 90210"
                        autocomplete="postal-code"
                        aria-describedby="csg-zip-error"
                    >
                    <p class="csg-zip-error" id="csg-zip-error" role="alert" hidden>Enter a valid 5-digit US zip code</p>
                </div>
            </div>

            <!-- Rate note + generate button -->
            <p class="csg-rate-note">Briefing generation is rate-limited to keep the service fast for everyone.</p>
            <button class="csg-generate-btn" id="csg-generate-btn" type="button">
                <svg class="csg-btn-icon" width="17" height="17" viewBox="0 0 17 17" fill="none" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8.5 1.5v2.75M8.5 12.75V15.5M1.5 8.5h2.75M12.75 8.5H15.5M3.44 3.44l1.94 1.94M11.62 11.62l1.94 1.94M3.44 13.56l1.94-1.94M11.62 5.38l1.94-1.94" stroke="currentColor" stroke-width="1.65" stroke-linecap="round"/>
                    <circle cx="8.5" cy="8.5" r="2.6" stroke="currentColor" stroke-width="1.65"/>
                </svg>
                <span id="csg-btn-label">Generate briefing</span>
            </button>

        </div>

        <!-- Loading state -->
        <div class="csg-state" id="csg-loading" role="status" aria-label="Generating briefing, please wait">
            <div class="csg-pulse" aria-hidden="true">
                <div class="csg-pulse-ring csg-pulse-ring--1"></div>
                <div class="csg-pulse-ring csg-pulse-ring--2"></div>
                <div class="csg-pulse-ring csg-pulse-ring--3"></div>
                <div class="csg-pulse-core"></div>
            </div>
            <p class="csg-loading-text">Analyzing recent alerts&hellip;</p>
        </div>

        <!-- Error state -->
        <div class="csg-state" id="csg-error" role="alert">
            <div class="csg-error-icon" aria-hidden="true">
                <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="15" cy="15" r="12.5" stroke="currentColor" stroke-width="1.8"/>
                    <path d="M15 9.5v7M15 19.5v1.5" stroke="currentColor" stroke-width="2.1" stroke-linecap="round"/>
                </svg>
            </div>
            <p class="csg-error-title" id="csg-error-title"></p>
            <p class="csg-error-body" id="csg-error-body"></p>
            <div class="csg-error-actions">
                <button class="csg-generate-btn csg-generate-btn--ghost" id="csg-retry-btn" type="button" hidden>Try again</button>
                <a class="csg-back-link" href="summaries.php">Back to summaries</a>
            </div>
        </div>

    </div>
</div>

<script>
(function () {
    var zone            = document.getElementById('csg-zone');
    var genBtn          = document.getElementById('csg-generate-btn');
    var btnLabel        = document.getElementById('csg-btn-label');
    var retryBtn        = document.getElementById('csg-retry-btn');
    var errTitle        = document.getElementById('csg-error-title');
    var errBody         = document.getElementById('csg-error-body');
    var scopeNationwide = document.getElementById('csg-scope-nationwide');
    var scopeLocal      = document.getElementById('csg-scope-local');
    var zipZone         = document.getElementById('csg-zip-zone');
    var zipInput        = document.getElementById('csg-zip-input');
    var zipError        = document.getElementById('csg-zip-error');

    var apiBase   = window.__RISKRADAR_API_BASE__   || 'http://127.0.0.1:8001';
    var apiPrefix = window.__RISKRADAR_API_PREFIX__ || '/api/v1';
    var userZip   = <?php echo json_encode($userZip ?? ''); ?>;

    var currentScope = 'nationwide';

    function setState(state) {
        zone.setAttribute('data-csg-state', state);
    }

    function showError(title, body, canRetry) {
        errTitle.textContent = title;
        errBody.textContent  = body;
        retryBtn.hidden      = !canRetry;
        setState('error');
    }

    function isValidZip(val) {
        return /^\d{5}$/.test(val.trim());
    }

    function syncButton() {
        var needsZip = currentScope === 'local';
        var zipOk    = !needsZip || isValidZip(zipInput.value);
        genBtn.disabled = !zipOk;
        btnLabel.textContent = needsZip ? 'Generate local digest' : 'Generate briefing';
    }

    function setScope(scope) {
        currentScope = scope;
        var isLocal  = scope === 'local';

        scopeNationwide.classList.toggle('csg-scope-opt--active', !isLocal);
        scopeNationwide.setAttribute('aria-pressed', String(!isLocal));
        scopeLocal.classList.toggle('csg-scope-opt--active', isLocal);
        scopeLocal.setAttribute('aria-pressed', String(isLocal));

        zipZone.classList.toggle('csg-zip-zone--open', isLocal);

        if (isLocal && userZip && !zipInput.value) {
            zipInput.value = userZip;
        }

        syncButton();

        if (isLocal && !zipInput.value) {
            setTimeout(function () { zipInput.focus(); }, 290);
        }
    }

    function generate() {
        if (currentScope === 'local') {
            var zip = zipInput.value.trim();
            if (!isValidZip(zip)) {
                zipError.hidden = false;
                zipInput.setAttribute('aria-invalid', 'true');
                zipInput.focus();
                return;
            }
        }

        setState('loading');

        var endpoint, opts;
        if (currentScope === 'local') {
            endpoint = apiBase + apiPrefix + '/summaries/generate/zipcode';
            opts = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ zip_code: zipInput.value.trim() })
            };
        } else {
            endpoint = apiBase + apiPrefix + '/summaries/generate';
            opts = { method: 'POST' };
        }

        fetch(endpoint, opts)
            .then(function (res) {
                if (res.ok) {
                    return res.json().then(function (data) {
                        window.location.href = 'summary_detail.php?id=' + data.id;
                    });
                }
                if (res.status === 429) {
                    showError(
                        'Generation limit reached',
                        'Please wait a moment before requesting another briefing.',
                        true
                    );
                } else if (res.status === 404) {
                    var noAlertsBody = currentScope === 'local'
                        ? 'No alerts found near that zip code. Try a different area or switch to Nationwide.'
                        : 'New briefings can only be generated when fresh alert data is available. Check back once new alerts have been recorded.';
                    showError('No alerts to summarize', noAlertsBody, currentScope === 'local');
                } else {
                    showError(
                        'Something went wrong',
                        'The briefing could not be generated. Please try again.',
                        true
                    );
                }
            })
            .catch(function () {
                showError(
                    'Connection error',
                    'Unable to reach the server. Check your connection and try again.',
                    true
                );
            });
    }

    scopeNationwide.addEventListener('click', function () { setScope('nationwide'); });
    scopeLocal.addEventListener('click', function () { setScope('local'); });

    zipInput.addEventListener('input', function () {
        zipError.hidden = true;
        zipInput.removeAttribute('aria-invalid');
        syncButton();
    });

    zipInput.addEventListener('blur', function () {
        if (zipInput.value && !isValidZip(zipInput.value)) {
            zipError.hidden = false;
            zipInput.setAttribute('aria-invalid', 'true');
        }
    });

    zipInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !genBtn.disabled) { generate(); }
    });

    genBtn.addEventListener('click', generate);
    retryBtn.addEventListener('click', function () { setState('ready'); });
}());
</script>

<?php rr_render_layout_end(); ?>

<?php rr_render_layout_start('Alert Detail', 'alerts'); ?>

<style>
/* ── Alert Detail Page ─────────────────────────────────────────────── */

.ad {
    --ad-green:         oklch(0.52 0.15 148);
    --ad-green-mid:     oklch(0.60 0.13 148);
    --ad-green-light:   oklch(0.94 0.04 148);
    --ad-green-dark:    oklch(0.30 0.12 148);
    --ad-green-border:  oklch(0.86 0.06 148);
    --ad-ink:           oklch(0.22 0.04 145);
    --ad-muted:         oklch(0.50 0.05 145);
    --ad-bg:            oklch(0.99 0.008 95);
    --ad-line:          oklch(0.89 0.015 140);

    /* Severity semantic tokens */
    --ad-high-fg:       oklch(0.46 0.19 25);
    --ad-high-bg:       oklch(0.97 0.04 25);
    --ad-high-border:   oklch(0.87 0.09 25);

    --ad-med-fg:        oklch(0.52 0.16 55);
    --ad-med-bg:        oklch(0.97 0.04 75);
    --ad-med-border:    oklch(0.87 0.09 65);

    --ad-low-fg:        oklch(0.48 0.14 148);
    --ad-low-bg:        oklch(0.96 0.04 148);
    --ad-low-border:    oklch(0.86 0.09 148);

    display: grid;
    gap: 12px;
    font-family: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', system-ui, sans-serif;
    font-kerning: normal;
}

/* ── Back navigation ───────────────────────────────────────────────── */

.ad-back {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    width: fit-content;
    padding: 6px 0;
    font-size: 0.875rem;
    font-weight: 700;
    letter-spacing: 0.01em;
    color: var(--ad-green);
    text-decoration: none;
    transition: opacity 0.15s ease-out;
}

.ad-back:hover,
.ad-back:focus-visible {
    opacity: 0.7;
}

.ad-back:focus-visible {
    outline: 3px solid var(--ad-green);
    outline-offset: 3px;
    border-radius: 3px;
}

.ad-back svg {
    flex-shrink: 0;
    transition: transform 0.15s ease-out;
}

.ad-back:hover svg {
    transform: translateX(-2px);
}

/* ── Main header ───────────────────────────────────────────────────── */

.ad-header {
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 24px;
    align-items: start;
    padding: 28px 32px;
    background: var(--ad-bg);
    border: 1px solid var(--ad-line);
    border-radius: 20px;
}

.ad-header-left {
    display: grid;
    gap: 14px;
    min-width: 0;
}

.ad-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
}

.ad-chip {
    display: inline-flex;
    align-items: center;
    padding: 3px 10px;
    border-radius: 4px;
    font-family: 'Geist Mono', 'Courier New', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    background: var(--ad-green-light);
    color: var(--ad-green-dark);
    border: 1px solid var(--ad-green-border);
    white-space: nowrap;
}

.ad-title {
    font-family: 'Bricolage Grotesque', 'Arial Black', sans-serif;
    font-size: clamp(1.45rem, 2.8vw, 2.15rem);
    font-weight: 800;
    letter-spacing: -0.035em;
    line-height: 1.1;
    color: var(--ad-ink);
    margin: 0;
}

/* ── Severity block ────────────────────────────────────────────────── */

.ad-severity {
    display: grid;
    gap: 5px;
    padding: 18px 22px;
    border-radius: 12px;
    text-align: center;
    min-width: 120px;
}

.ad-severity-label {
    font-family: 'Geist Mono', 'Courier New', monospace;
    font-size: 0.66rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.ad-severity-word {
    font-family: 'Bricolage Grotesque', 'Arial Black', sans-serif;
    font-size: 1.9rem;
    font-weight: 800;
    letter-spacing: -0.04em;
    line-height: 1;
}

/* Severity colour variants */
.ad-sev-high   { background: var(--ad-high-bg); border: 1px solid var(--ad-high-border); }
.ad-sev-medium { background: var(--ad-med-bg);  border: 1px solid var(--ad-med-border);  }
.ad-sev-low    { background: var(--ad-low-bg);  border: 1px solid var(--ad-low-border);  }

.ad-sev-high .ad-severity-label,
.ad-sev-high .ad-severity-word   { color: var(--ad-high-fg); }

.ad-sev-medium .ad-severity-label,
.ad-sev-medium .ad-severity-word { color: var(--ad-med-fg);  }

.ad-sev-low .ad-severity-label,
.ad-sev-low .ad-severity-word    { color: var(--ad-low-fg);  }

/* ── Quick-facts strip ─────────────────────────────────────────────── */

.ad-facts {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    background: var(--ad-bg);
    border: 1px solid var(--ad-line);
    border-radius: 16px;
    overflow: hidden;
}

.ad-fact {
    display: grid;
    gap: 6px;
    padding: 18px 22px;
}

.ad-fact + .ad-fact {
    border-left: 1px solid var(--ad-line);
}

.ad-fact-label {
    font-family: 'Geist Mono', 'Courier New', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ad-muted);
}

.ad-fact-value {
    font-size: 0.9375rem;
    font-weight: 700;
    color: var(--ad-ink);
    line-height: 1.35;
}

.ad-fact-value.is-unavailable {
    font-weight: 400;
    font-style: italic;
    color: var(--ad-muted);
}

/* ── Description ───────────────────────────────────────────────────── */

.ad-description {
    padding: 26px 32px;
    background: var(--ad-bg);
    border: 1px solid var(--ad-line);
    border-radius: 16px;
}

.ad-section-label {
    font-family: 'Geist Mono', 'Courier New', monospace;
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--ad-green-mid);
    margin: 0 0 14px;
}

.ad-body {
    font-size: 1.0625rem;
    line-height: 1.72;
    color: var(--ad-ink);
    max-width: 70ch;
    margin: 0;
}

.ad-empty-text {
    font-style: italic;
    color: var(--ad-muted);
    margin: 0;
}

/* ── Technical metadata ────────────────────────────────────────────── */

.ad-meta {
    background: var(--ad-bg);
    border: 1px solid var(--ad-line);
    border-radius: 16px;
    overflow: hidden;
}

.ad-meta-summary {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 28px;
    font-family: 'Geist Mono', 'Courier New', monospace;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--ad-muted);
    cursor: pointer;
    list-style: none;
    user-select: none;
    transition: color 0.15s ease-out;
}

.ad-meta-summary::-webkit-details-marker { display: none; }

.ad-meta-toggle {
    font-size: 0.62rem;
    letter-spacing: 0;
    transition: transform 0.2s ease-out;
    display: inline-block;
}

.ad-meta[open] .ad-meta-toggle {
    transform: rotate(180deg);
}

.ad-meta-summary:hover { color: var(--ad-ink); }

.ad-meta-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
    margin: 0;
    padding: 0 20px 20px;
}

.ad-meta-item {
    display: grid;
    gap: 5px;
    padding: 12px 8px;
    border-top: 1px solid var(--ad-line);
}

.ad-meta-item dt {
    font-family: 'Geist Mono', 'Courier New', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--ad-muted);
    margin: 0;
}

.ad-meta-item dd {
    font-family: 'Geist Mono', 'Courier New', monospace;
    font-size: 0.8125rem;
    font-weight: 400;
    color: var(--ad-ink);
    margin: 0;
    font-variant-numeric: tabular-nums;
    overflow-wrap: break-word;
}

.ad-meta-item dd.is-unavailable {
    color: var(--ad-muted);
    font-style: italic;
}

/* ── Responsive ────────────────────────────────────────────────────── */

@media (max-width: 700px) {
    .ad-header {
        grid-template-columns: 1fr;
        padding: 20px;
        gap: 16px;
    }

    .ad-severity {
        display: flex;
        align-items: center;
        gap: 14px;
        padding: 12px 16px;
        text-align: left;
        width: fit-content;
    }

    .ad-severity-word { font-size: 1.5rem; }

    .ad-facts {
        grid-template-columns: 1fr;
    }

    .ad-fact + .ad-fact {
        border-left: none;
        border-top: 1px solid var(--ad-line);
    }

    .ad-description {
        padding: 20px;
    }

    .ad-meta-summary {
        padding: 14px 20px;
    }

    .ad-meta-grid {
        padding: 0 12px 16px;
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 420px) {
    .ad-meta-grid {
        grid-template-columns: 1fr;
    }
}
</style>

<?php
    $sevClass = match (strtolower((string) ($alert['severity'] ?? ''))) {
        'high', 'severe', 'critical', 'extreme' => 'ad-sev-high',
        'medium', 'moderate'                    => 'ad-sev-medium',
        default                                 => 'ad-sev-low',
    };
?>

<div class="ad">

    <a class="ad-back" href="alerts.php">
        <svg width="15" height="15" viewBox="0 0 15 15" fill="none" aria-hidden="true" focusable="false">
            <path d="M9.5 11.5L5.5 7.5L9.5 3.5" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Back to alerts
    </a>

    <header class="ad-header">
        <div class="ad-header-left">
            <div class="ad-chips">
                <span class="ad-chip"><?php echo e($alert['source']); ?></span>
                <span class="ad-chip"><?php echo e($alert['alert_type']); ?></span>
            </div>
            <h1 class="ad-title"><?php echo e($alert['title']); ?></h1>
        </div>

        <div class="ad-severity <?php echo e($sevClass); ?>" aria-label="Severity: <?php echo e(ucfirst($alert['severity'])); ?>">
            <span class="ad-severity-label">Severity</span>
            <span class="ad-severity-word"><?php echo e(ucfirst($alert['severity'])); ?></span>
        </div>
    </header>

    <div class="ad-facts" role="list" aria-label="Key alert details">
        <div class="ad-fact" role="listitem">
            <span class="ad-fact-label">Location</span>
            <?php if ($alert['location_name']) : ?>
                <span class="ad-fact-value"><?php echo e($alert['location_name']); ?></span>
            <?php else : ?>
                <span class="ad-fact-value is-unavailable">Unavailable</span>
            <?php endif; ?>
        </div>

        <div class="ad-fact" role="listitem">
            <span class="ad-fact-label">Event window</span>
            <?php if ($alert['event_start'] || $alert['event_end']) : ?>
                <span class="ad-fact-value">
                    <?php if ($alert['event_start']) : ?>
                        <?php echo e(rr_format_datetime($alert['event_start'])); ?>
                    <?php endif; ?>
                    <?php if ($alert['event_start'] && $alert['event_end']) : ?>
                        &nbsp;&rarr;&nbsp;
                    <?php endif; ?>
                    <?php if ($alert['event_end']) : ?>
                        <?php echo e(rr_format_datetime($alert['event_end'])); ?>
                    <?php endif; ?>
                </span>
            <?php else : ?>
                <span class="ad-fact-value is-unavailable">Unavailable</span>
            <?php endif; ?>
        </div>

        <div class="ad-fact" role="listitem">
            <span class="ad-fact-label">Source</span>
            <span class="ad-fact-value"><?php echo e($alert['source']); ?></span>
        </div>
    </div>

    <section class="ad-description">
        <p class="ad-section-label">Description</p>
        <?php if ($alert['description']) : ?>
            <p class="ad-body"><?php echo nl2br(e($alert['description'])); ?></p>
        <?php else : ?>
            <p class="ad-empty-text">No description was provided by the source feed.</p>
        <?php endif; ?>
    </section>

    <details class="ad-meta" open>
        <summary class="ad-meta-summary">
            Technical details
            <span class="ad-meta-toggle" aria-hidden="true">&#9660;</span>
        </summary>
        <dl class="ad-meta-grid">
            <div class="ad-meta-item">
                <dt>Alert ID</dt>
                <dd><?php echo e((string) $alert['id']); ?></dd>
            </div>
            <div class="ad-meta-item">
                <dt>Source</dt>
                <dd><?php echo e($alert['source']); ?></dd>
            </div>
            <div class="ad-meta-item">
                <dt>Source ID</dt>
                <dd class="<?php echo $alert['source_id'] ? '' : 'is-unavailable'; ?>">
                    <?php echo e($alert['source_id'] ?: 'Unavailable'); ?>
                </dd>
            </div>
            <div class="ad-meta-item">
                <dt>Alert type</dt>
                <dd><?php echo e($alert['alert_type']); ?></dd>
            </div>
            <div class="ad-meta-item">
                <dt>Severity</dt>
                <dd><?php echo e(ucfirst($alert['severity'])); ?></dd>
            </div>
            <?php if ($alert['latitude'] !== null && $alert['longitude'] !== null) : ?>
            <div class="ad-meta-item">
                <dt>Coordinates</dt>
                <dd><?php echo e(number_format((float) $alert['latitude'], 4)); ?>, <?php echo e(number_format((float) $alert['longitude'], 4)); ?></dd>
            </div>
            <?php endif; ?>
            <div class="ad-meta-item">
                <dt>Event start</dt>
                <dd><?php echo e(rr_format_datetime($alert['event_start'])); ?></dd>
            </div>
            <div class="ad-meta-item">
                <dt>Event end</dt>
                <dd><?php echo e(rr_format_datetime($alert['event_end'])); ?></dd>
            </div>
            <div class="ad-meta-item">
                <dt>Fetched</dt>
                <dd><?php echo e(rr_format_datetime($alert['fetched_at'])); ?></dd>
            </div>
            <div class="ad-meta-item">
                <dt>Created</dt>
                <dd><?php echo e(rr_format_datetime($alert['created_at'])); ?></dd>
            </div>
        </dl>
    </details>

</div>

<section class="panel" aria-labelledby="risk-score-heading">
    <h2 id="risk-score-heading" tabindex="0">Risk Score Breakdown</h2>
    <?php
    // Example: fetch user ID from session or context
    $userId = $_SESSION['user_id'] ?? null;
    $riskBreakdown = null;
    $riskFormula = null;
    if ($userId) {
        $riskBreakdownJson = @file_get_contents("/api/v1/alerts/risk_breakdown/{$alert['id']}/{$userId}");
        if ($riskBreakdownJson) {
            $riskBreakdown = json_decode($riskBreakdownJson, true);
        }
        $riskFormulaJson = @file_get_contents("/api/v1/alerts/risk_formula");
        if ($riskFormulaJson) {
            $riskFormula = json_decode($riskFormulaJson, true);
        }
    }
    ?>
    <?php if ($riskBreakdown): ?>
        <div class="risk-score-summary" role="region" aria-label="Risk score details">
            <strong>Risk Score:</strong> <span aria-live="polite"><?php echo e($riskBreakdown['risk_score']); ?></span> (<span><?php echo e(ucfirst($riskBreakdown['risk_level'])); ?></span>)
            <ul class="risk-factor-list">
                <li><strong>Distance factor:</strong> <span><?php echo e($riskBreakdown['factor_scores']['distance']); ?></span></li>
                <li><strong>Severity factor:</strong> <span><?php echo e($riskBreakdown['factor_scores']['severity']); ?></span></li>
                <li><strong>Sensitivity factor:</strong> <span><?php echo e($riskBreakdown['factor_scores']['sensitivity']); ?></span></li>
                <li><strong>Recency factor:</strong> <span><?php echo e($riskBreakdown['factor_scores']['recency']); ?></span></li>
            </ul>
        </div>
    <?php else: ?>
        <p class="empty-state" aria-live="polite">Risk score breakdown is unavailable for this alert and user.</p>
    <?php endif; ?>
    <?php if ($riskFormula): ?>
        <details class="risk-formula-details" tabindex="0">
            <summary><span class="visually-hidden">Show explanation: </span>How is this risk score calculated?</summary>
            <p><strong>Formula:</strong> <span><?php echo e($riskFormula['formula']); ?></span></p>
            <ul>
                <li><strong>Distance:</strong> <span><?php echo e($riskFormula['factors']['distance']); ?></span> (weight: <span><?php echo e($riskFormula['weights']['distance'] * 100); ?>%</span>)</li>
                <li><strong>Severity:</strong> <span><?php echo e($riskFormula['factors']['severity']); ?></span> (weight: <span><?php echo e($riskFormula['weights']['severity'] * 100); ?>%</span>)</li>
                <li><strong>Sensitivity:</strong> <span><?php echo e($riskFormula['factors']['sensitivity']); ?></span> (weight: <span><?php echo e($riskFormula['weights']['sensitivity'] * 100); ?>%</span>)</li>
                <li><strong>Recency:</strong> <span><?php echo e($riskFormula['factors']['recency']); ?></span> (weight: <span><?php echo e($riskFormula['weights']['recency'] * 100); ?>%</span>)</li>
            </ul>
            <p><strong>Priority levels:</strong> High (70-100), Medium (40-69), Low (0-39)</p>
        </details>
    <?php endif; ?>
</section>

<style>
.risk-score-summary {
  background: var(--theme-panel-strong, #fff6ea);
  border-radius: var(--radius-md, 12px);
  padding: 1rem 1.5rem;
  margin-bottom: 1rem;
  color: var(--theme-ink, #122231);
}
.risk-factor-list {
  list-style: disc inside;
  margin: 0.5em 0 0 1em;
  padding: 0;
}
.risk-formula-details {
  margin-top: 1em;
  background: var(--theme-panel, #fffbf5);
  border-radius: var(--radius-md, 12px);
  padding: 1rem 1.5rem;
  color: var(--theme-ink, #122231);
}
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0,0,0,0);
  border: 0;
}
</style>

<?php rr_render_layout_end(); ?>

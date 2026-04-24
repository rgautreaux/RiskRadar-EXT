<?php rr_render_layout_start('Alert Detail', 'alerts'); ?>

<section class="page-heading">
    <div>
        <p class="eyebrow">Alert detail</p>
        <h1><?php echo e($alert['title']); ?></h1>
    </div>
    <a class="back-link" href="alerts.php">&larr; Back to alerts</a>
</section>

<article class="panel">
    <div class="card-heading">
        <span class="severity-pill <?php echo e(rr_severity_class($alert['severity'])); ?>"><?php echo e(ucfirst($alert['severity'])); ?></span>
        <span class="meta-chip"><?php echo e($alert['source']); ?></span>
        <span class="meta-chip"><?php echo e($alert['alert_type']); ?></span>
    </div>

    <?php if ($alert['description']) : ?>
        <p><?php echo nl2br(e($alert['description'])); ?></p>
    <?php else : ?>
        <p class="empty-state">No description was provided by the source feed.</p>
    <?php endif; ?>

    <dl class="metadata-grid detail-grid">
        <div>
            <dt>Alert ID</dt>
            <dd><?php echo e((string) $alert['id']); ?></dd>
        </div>
        <div>
            <dt>Source</dt>
            <dd><?php echo e($alert['source']); ?></dd>
        </div>
        <div>
            <dt>Source ID</dt>
            <dd><?php echo e($alert['source_id'] ?: 'Unavailable'); ?></dd>
        </div>
        <div>
            <dt>Alert type</dt>
            <dd><?php echo e($alert['alert_type']); ?></dd>
        </div>
        <div>
            <dt>Severity</dt>
            <dd><?php echo e(ucfirst($alert['severity'])); ?></dd>
        </div>
        <div>
            <dt>Location</dt>
            <dd><?php echo e($alert['location_name'] ?: 'Unavailable'); ?></dd>
        </div>
        <?php if ($alert['latitude'] !== null && $alert['longitude'] !== null) : ?>
        <div>
            <dt>Coordinates</dt>
            <dd><?php echo e(number_format((float) $alert['latitude'], 4)); ?>, <?php echo e(number_format((float) $alert['longitude'], 4)); ?></dd>
        </div>
        <?php endif; ?>
        <div>
            <dt>Event start</dt>
            <dd><?php echo e(rr_format_datetime($alert['event_start'])); ?></dd>
        </div>
        <div>
            <dt>Event end</dt>
            <dd><?php echo e(rr_format_datetime($alert['event_end'])); ?></dd>
        </div>
        <div>
            <dt>Fetched</dt>
            <dd><?php echo e(rr_format_datetime($alert['fetched_at'])); ?></dd>
        </div>
        <div>
            <dt>Created</dt>
            <dd><?php echo e(rr_format_datetime($alert['created_at'])); ?></dd>
        </div>
    </dl>
</article>

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

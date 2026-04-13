# Normalization Guardrails Checklist

Use this checklist to capture staging proof for the low-risk database normalization rollout.

## Environment

- Date:
- Commit SHA:
- Database dialect (`sqlite` or `mariadb`):
- Operator:

## Migration Application

- [ ] Applied `backend/db/migrations/2026-04-11_add_summary_alerts_and_feedback_fk.sql`
- [ ] Applied `backend/db/migrations/2026-04-12_add_user_alert_preferences.sql`
- [ ] Applied `backend/db/migrations/2026-04-12_add_user_health_conditions.sql`

## Backfill Dry Runs

- [ ] `python backend/scripts/backfill_summary_alert_links.py --dry-run`
- [ ] `python backend/scripts/backfill_user_alert_preferences.py --dry-run`
- [ ] `python backend/scripts/backfill_user_health_conditions.py --dry-run`

Attach logs/screenshots:

- Summary links dry-run output:
- User alert preferences dry-run output:
- User health conditions dry-run output:

## Backfill Writes

- [ ] `python backend/scripts/backfill_summary_alert_links.py`
- [ ] `python backend/scripts/backfill_user_alert_preferences.py`
- [ ] `python backend/scripts/backfill_user_health_conditions.py`

Attach logs/screenshots:

- Summary links write output:
- User alert preferences write output:
- User health conditions write output:

## Reconciliation and Guardrails

- [ ] `python backend/scripts/reconcile_summary_alert_links.py`
- [ ] `python backend/scripts/reconcile_summary_alert_links.py --fail-on-mismatch`
- [ ] `python backend/scripts/verify_normalization_guardrails.py --strict`

Attach logs/screenshots:

- Reconciliation output:
- Strict guardrail output:

## Regression Verification

- [ ] `python backend/scripts/run_full_verification.py --include-normalization-guardrails`

Attach logs/screenshots:

- Full verification output:

## Sign-off

- [ ] No summary link drift remains.
- [ ] No user preference/health-condition backfill errors remain.
- [ ] Backend tests pass.
- [ ] Ready for merge.

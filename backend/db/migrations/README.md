# Migration Scripts

This folder will contain migration scripts for email encryption and password hashing upgrades.

- Draft scripts here before executing in production.
- Document each migration step and batch.

## Phase 3 (Migration Logging & Monitoring) Scripts

- `2026-04-11_notification_channels_dispatch_log.sql`
  - Adds persistent notification channel flags on `users`:
    - `notify_push` (default `1`)
    - `notify_email` (default `0`)
    - `notify_sms` (default `0`)
  - Creates `notification_dispatch_log` table for delivery observability:
    - per-dispatch recipient totals, sent/failed counts, provider, status, and timestamp
  - Adds indexes on `notification_dispatch_log.alert_id` and `notification_dispatch_log.created_at`

- `2026-04-10_phase3_email_security_schema.sql`
  - Adds the `users.email_encrypted` and `users.email_hmac` columns required by the email migration.
  - Creates the `migration_log` table used by the Phase 3 logging, validation, and monitoring tools.

- `migrate_email_encryption.py`
  - Encrypts plaintext user emails into `email_encrypted`.
  - Computes and stores `email_hmac` for lookup uniqueness.
  - Clears legacy plaintext `email` values.
  - Writes batch lifecycle logs (`started`, `completed`, `failed`) and per-user logs (`success`, `error`) to `migration_log`.
  - Sanitizes exception text before persisting to prevent sensitive data leakage.

- `validate_email_migration.py`
  - Verifies migration invariants after a run (no plaintext emails, encrypted/HMAC fields present, no failed logs, completed batch record exists).
  - Returns non-zero exit code when checks fail.

- `monitor_migration_log.py`
  - Monitors `migration_log` for `error`/`failed` records.
  - Supports threshold-based alert behavior via `MIGRATION_ERROR_THRESHOLD`.
  - Returns non-zero exit code when threshold is reached.

- `phase3_staging_evidence_template.md`
  - Fill-in worksheet for staging execution evidence collection and SQL spot-check output.
  - Intended to be attached to the Phase 3 review handoff package before approval request.

## Suggested Run Order (Staging)

1. Apply `2026-04-10_phase3_email_security_schema.sql`
2. Apply `2026-04-11_notification_channels_dispatch_log.sql`
3. `python db/migrations/migrate_email_encryption.py`
4. `python db/migrations/validate_email_migration.py`
5. `python db/migrations/monitor_migration_log.py`

Record all outputs in staging validation notes before requesting backend/security lead sign-off.

## Latest Verification Snapshot

See `backend/db/migrations/MIGRATION_NOTES.md` for the dated 2026-04-11 evidence block including migration script results, validator/monitor outputs, query-plan index checks, and full backend pytest confirmation.

# MariaDB Migration Notes

Use `2026-03-03_mariadb_scraper_alignment.sql` to align an existing MariaDB schema with the backend ORM models used by scrapers.

## What it fixes

- `alerts` shape and nullability to match `db.models.Alert`
- `scrape_log` shape to match `db.models.ScrapeLog`
- `summaries.reigon` typo to `summaries.region`
- `users` shape to match `db.models.User`
- Removes constraints/indexes that block recurring scraper inserts

## Additional normalization step

Use `2026-04-11_add_summary_alerts_and_feedback_fk.sql` to introduce the normalized `summary_alerts` junction table and the `feedback.user_id` foreign key without removing the legacy `summaries.alert_ids` JSON column.

After applying the SQL migration, backfill existing summary links:

```bash
python backend/scripts/backfill_summary_alert_links.py --dry-run
python backend/scripts/backfill_summary_alert_links.py
python backend/scripts/reconcile_summary_alert_links.py
```

Use `2026-04-12_add_user_alert_preferences.sql` to add the normalized `user_alert_preferences` mapping table without removing the legacy `users.alert_types` JSON field.

Backfill existing user alert preference rows:

```bash
python backend/scripts/backfill_user_alert_preferences.py --dry-run
python backend/scripts/backfill_user_alert_preferences.py
```

## Apply migration

```sql
SOURCE backend/db/migrations/2026-03-03_mariadb_scraper_alignment.sql;
SOURCE backend/db/migrations/2026-04-11_add_summary_alerts_and_feedback_fk.sql;
SOURCE backend/db/migrations/2026-04-12_add_user_alert_preferences.sql;
```

## Runtime configuration

Set `DATABASE_URL` in `.env` to run backend against MariaDB.

Example:

```env
DATABASE_URL=mysql+pymysql://riskradar_user:your_password@127.0.0.1:3306/riskradar_db
```

If `DATABASE_URL` is not set, backend continues using local SQLite (`DB_PATH`).

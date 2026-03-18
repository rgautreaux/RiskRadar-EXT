# Max — Project Change Log

## March 18, 2026

### Fixed: Duplicate alert crash in location endpoint

**File changed:** `backend/api/location.py`

**Problem:** The `/api/v1/location/alerts` endpoint threw an unhandled `IntegrityError` when fetching alerts for a zip code. This occurred because of a race condition — the endpoint checks for existing alerts before inserting, but between the check and the `db.commit()`, another request or the background scraper could insert the same alert, violating the `uq_source_alert` unique constraint.

**Fix:** Added an `IntegrityError` catch around the commit. On conflict, the transaction is rolled back and the alerts are re-fetched from the database, so the endpoint returns the correct data instead of crashing.

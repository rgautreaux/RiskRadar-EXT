-- 2026-04-19: Add has_completed_onboarding to users table
ALTER TABLE users ADD COLUMN has_completed_onboarding BOOLEAN NOT NULL DEFAULT FALSE;
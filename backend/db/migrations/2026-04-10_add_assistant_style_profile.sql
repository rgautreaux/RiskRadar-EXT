-- Adds persistent style learning profile for Golby assistant communication preferences.
-- Compatible with SQLite and MariaDB/MySQL (TEXT and NULL defaults supported).

ALTER TABLE users
ADD COLUMN assistant_style_profile TEXT;

-- Seed defaults for existing rows if column starts as NULL.
UPDATE users
SET assistant_style_profile = '{"tone":{"warmth":0.55,"calmness":0.75,"humor":0.4},"delivery":{"conciseness":0.7,"detail":0.45,"expandability":0.55},"voice":{"formality":0.35},"learning":{"feedback_count":0,"last_feedback_at":null}}'
WHERE assistant_style_profile IS NULL;

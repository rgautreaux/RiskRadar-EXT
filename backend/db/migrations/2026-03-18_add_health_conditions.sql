-- Stage 2 Step 1: Add health_conditions column to users table for personal risk scoring.
-- Stores a JSON array of condition keys (e.g. '["respiratory","cardiovascular"]').
-- Default empty array preserves backward compatibility for existing users.

-- SQLite
ALTER TABLE users ADD COLUMN health_conditions TEXT DEFAULT '[]';

-- MariaDB/MySQL alternative (uncomment if using MariaDB):
-- ALTER TABLE `users` ADD COLUMN `health_conditions` TEXT DEFAULT '[]' AFTER `notify_severity`;

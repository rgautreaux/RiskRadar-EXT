-- Encrypt existing user emails and add a lookup hash column.
--
-- Execution order:
-- 1. Deploy the updated backend code.
-- 2. Apply the schema changes below to add the new lookup column.
-- 3. Run backend/scripts/migrate_emails_to_encrypted.py against the active database.
--
-- Note: The one-time Python migration is responsible for converting plaintext emails.
-- This SQL file only aligns the schema.

-- SQLite
ALTER TABLE users ADD COLUMN email_lookup_hash TEXT;
CREATE UNIQUE INDEX IF NOT EXISTS uq_users_email_lookup_hash ON users(email_lookup_hash);

-- MariaDB/MySQL alternative:
-- ALTER TABLE `users` ADD COLUMN `email_lookup_hash` TEXT NULL AFTER `email`;
-- ALTER TABLE `users` ADD UNIQUE KEY `uq_users_email_lookup_hash` (`email_lookup_hash`);

-- If you are recreating the users table from scratch, ensure the ORM shape matches:
--   email TEXT NOT NULL
--   email_lookup_hash TEXT NOT NULL UNIQUE

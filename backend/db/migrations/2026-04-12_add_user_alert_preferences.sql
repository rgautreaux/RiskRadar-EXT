-- Add a normalized user alert preference mapping table.
--
-- Keeps users.alert_types JSON for compatibility while enabling relational lookups.

START TRANSACTION;

CREATE TABLE `user_alert_preferences` (
  `user_id` int(11) NOT NULL,
  `alert_type` varchar(64) NOT NULL,
  `created_at` text NOT NULL,
  PRIMARY KEY (`user_id`, `alert_type`),
  KEY `idx_user_alert_preferences_user_id` (`user_id`),
  CONSTRAINT `fk_user_alert_preferences_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
);

COMMIT;

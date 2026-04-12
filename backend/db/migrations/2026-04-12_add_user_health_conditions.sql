-- Add a normalized user health condition mapping table.
--
-- Keeps users.health_conditions JSON for compatibility while enabling relational lookups.

START TRANSACTION;

CREATE TABLE `user_health_conditions` (
  `user_id` int(11) NOT NULL,
  `condition_key` varchar(64) NOT NULL,
  `created_at` text NOT NULL,
  PRIMARY KEY (`user_id`, `condition_key`),
  KEY `idx_user_health_conditions_user_id` (`user_id`),
  CONSTRAINT `fk_user_health_conditions_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
);

COMMIT;

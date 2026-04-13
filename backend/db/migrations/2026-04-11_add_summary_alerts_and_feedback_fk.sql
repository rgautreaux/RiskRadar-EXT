-- Add a normalized summary-alert junction table and a feedback FK.
--
-- Apply after the ORM update lands.
-- Existing summaries keep their JSON alert_ids field for compatibility.

START TRANSACTION;

-- ---------------------------------------------------------------------------
-- summary_alerts
-- ---------------------------------------------------------------------------
CREATE TABLE `summary_alerts` (
  `summary_id` int(11) NOT NULL,
  `alert_id` int(11) NOT NULL,
  `created_at` text NOT NULL,
  PRIMARY KEY (`summary_id`, `alert_id`),
  KEY `idx_summary_alerts_summary_id` (`summary_id`),
  KEY `idx_summary_alerts_alert_id` (`alert_id`),
  CONSTRAINT `fk_summary_alerts_summary`
    FOREIGN KEY (`summary_id`) REFERENCES `summaries` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_summary_alerts_alert`
    FOREIGN KEY (`alert_id`) REFERENCES `alerts` (`id`) ON DELETE CASCADE
);

-- ---------------------------------------------------------------------------
-- feedback
-- ---------------------------------------------------------------------------
ALTER TABLE `feedback`
  ADD CONSTRAINT `fk_feedback_user`
  FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

COMMIT;

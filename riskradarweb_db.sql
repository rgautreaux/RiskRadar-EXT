-- RiskRadar Web Database Schema
-- MariaDB 10.4+
--
-- This is the final-state bootstrap schema with all migrations applied.
-- Do NOT run the individual migration files against this schema.
--
-- Migrations incorporated (in order):
--   2026-03-03_mariadb_scraper_alignment.sql
--   2026-03-18_add_health_conditions.sql
--   2026-04-02_encrypt_user_emails.sql
--   2026-04-10_add_assistant_style_profile.sql
--   2026-04-11_add_summary_alerts_and_feedback_fk.sql
--   2026-04-12_add_user_alert_preferences.sql
--   2026-04-12_add_user_health_conditions.sql
--
-- Source of truth for column shapes: backend/db/models.py

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `riskradar_db`
--

-- ============================================================
-- CORE ORM TABLES (used by backend/db/models.py)
-- Creation order respects FK dependencies.
-- ============================================================

-- --------------------------------------------------------
-- alerts
-- Changes vs original: alert_id→id (AUTO_INCREMENT), dropped article_id and priority,
--   source/source_id/alert_type/severity typed to VARCHAR, several columns made nullable,
--   json_valid CHECK removed, HASH unique replaced with uq_source_alert.
-- --------------------------------------------------------

CREATE TABLE `alerts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` varchar(64) NOT NULL,
  `source_id` varchar(255) NULL,
  `alert_type` varchar(64) NOT NULL,
  `severity` varchar(32) NOT NULL DEFAULT 'moderate',
  `title` text NOT NULL,
  `description` text NULL,
  `raw_data` longtext NULL,
  `latitude` float NULL,
  `longitude` float NULL,
  `location_name` text NULL,
  `event_start` text NULL,
  `event_end` text NULL,
  `fetched_at` text NOT NULL,
  `created_at` text NOT NULL,
  `updated_at` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_source_alert` (`source`, `source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- summaries
-- Changes vs original: fixed typo reigon→region, made alert_ids/region/model_used/
--   token_count nullable, removed json_valid CHECK and HASH unique on alert_ids.
-- --------------------------------------------------------

CREATE TABLE `summaries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` text NOT NULL,
  `content` text NOT NULL,
  `summary_type` text NOT NULL DEFAULT 'daily',
  `alert_ids` longtext NULL,
  `region` text NULL,
  `generated_at` text NOT NULL,
  `model_used` text NULL,
  `token_count` int(11) NULL,
  `created_at` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- users
-- Changes vs original: user_id→id (AUTO_INCREMENT), dropped token_id/is_active/last_login_at,
--   added device_token/email_lookup_hash/health_conditions/assistant_style_profile/is_admin,
--   email changed to varchar(255) nullable, display_name/password_hash/zip_code/
--   latitude/longitude/alert_types/notify_severity made nullable,
--   old unique keys replaced with uq_users_email and uq_users_email_lookup_hash.
-- --------------------------------------------------------

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_token` text NULL,
  `display_name` text NULL,
  `email` varchar(255) NULL,
  `email_lookup_hash` varchar(255) NULL,
  `password_hash` text NULL,
  `is_admin` tinyint(1) NOT NULL DEFAULT 0,
  `zip_code` text NULL,
  `latitude` float NULL,
  `longitude` float NULL,
  `alert_types` longtext NULL,
  `notify_severity` text NULL,
  `health_conditions` text NULL DEFAULT '[]',
  `assistant_style_profile` text NULL DEFAULT '{"tone":{"warmth":0.55,"calmness":0.75,"humor":0.4},"delivery":{"conciseness":0.7,"detail":0.45,"expandability":0.55},"voice":{"formality":0.35},"learning":{"feedback_count":0,"last_feedback_at":null}}',
  `created_at` text NOT NULL,
  `updated_at` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_email` (`email`),
  UNIQUE KEY `uq_users_email_lookup_hash` (`email_lookup_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- feedback
-- New table: defined in models.py; FK to users added in 2026-04-11 migration.
-- --------------------------------------------------------

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `session_id` text NOT NULL,
  `message_id` text NOT NULL,
  `user_id` int(11) NULL,
  `reaction` text NOT NULL,
  `rating` int(11) NOT NULL,
  `page_context` text NULL,
  `response_category` text NULL,
  `response_text` text NULL,
  `comment` text NULL,
  `created_at` text NOT NULL,
  `updated_at` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_feedback_session_message` (`session_id`(255), `message_id`(255)),
  KEY `idx_feedback_user_id` (`user_id`),
  CONSTRAINT `fk_feedback_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- summary_alerts
-- New table: 2026-04-11_add_summary_alerts_and_feedback_fk.sql
-- --------------------------------------------------------

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- user_alert_preferences
-- New table: 2026-04-12_add_user_alert_preferences.sql
-- --------------------------------------------------------

CREATE TABLE `user_alert_preferences` (
  `user_id` int(11) NOT NULL,
  `alert_type` varchar(64) NOT NULL,
  `created_at` text NOT NULL,
  PRIMARY KEY (`user_id`, `alert_type`),
  KEY `idx_user_alert_preferences_user_id` (`user_id`),
  CONSTRAINT `fk_user_alert_preferences_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- user_health_conditions
-- New table: 2026-04-12_add_user_health_conditions.sql
-- --------------------------------------------------------

CREATE TABLE `user_health_conditions` (
  `user_id` int(11) NOT NULL,
  `condition_key` varchar(64) NOT NULL,
  `created_at` text NOT NULL,
  PRIMARY KEY (`user_id`, `condition_key`),
  KEY `idx_user_health_conditions_user_id` (`user_id`),
  CONSTRAINT `fk_user_health_conditions_user`
    FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------
-- scrape_log
-- Changes vs original: log_id→id (AUTO_INCREMENT), dropped scraped_at/http_status/
--   articles_found/articles_inserted, source→varchar(64), status→varchar(32),
--   error_message/duration_ms made nullable, removed HASH unique on source.
-- --------------------------------------------------------

CREATE TABLE `scrape_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` varchar(64) NOT NULL,
  `status` varchar(32) NOT NULL,
  `alerts_fetched` int(11) NOT NULL DEFAULT 0,
  `alerts_new` int(11) NOT NULL DEFAULT 0,
  `error_message` text NULL,
  `duration_ms` int(11) NULL,
  `started_at` text NOT NULL,
  `completed_at` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ============================================================
-- LEGACY TABLES (from original mobile-era schema)
-- Not used by the current backend ORM but retained for
-- compatibility with existing team member databases.
-- ============================================================

CREATE TABLE `articles` (
  `article_id` int(11) NOT NULL AUTO_INCREMENT,
  `source_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `title` varchar(500) NOT NULL,
  `source_url` varchar(1000) NOT NULL,
  `raw_content` text NOT NULL,
  `formatted_body` text NOT NULL,
  `summary` varchar(1000) NOT NULL,
  `read_time_min` smallint(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `scraped_at` date NOT NULL,
  `published_at` date NOT NULL,
  `created_at` date NOT NULL,
  PRIMARY KEY (`article_id`),
  UNIQUE KEY `source_id` (`source_id`, `category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `article_tags` (
  `article_id` int(11) NOT NULL,
  `tag_id` int(11) NOT NULL,
  PRIMARY KEY (`article_id`, `tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `device_tokens` (
  `token_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `device_token` varchar(255) NOT NULL,
  `platform` varchar(10) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`token_id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `notification_settings` (
  `user_id` int(11) NOT NULL,
  `alerts_enabled` tinyint(1) NOT NULL,
  `daily_digest` tinyint(1) NOT NULL,
  `quiet_start` time NOT NULL,
  `quiet_end` time NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `sources` (
  `source_id` int(11) NOT NULL AUTO_INCREMENT,
  `source_name` varchar(100) NOT NULL,
  `base_url` varchar(500) NOT NULL,
  `scrape_freq_min` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `tags` (
  `tag_id` int(11) NOT NULL AUTO_INCREMENT,
  `tag_name` varchar(50) NOT NULL,
  PRIMARY KEY (`tag_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `user_prefernces` (
  `user_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `is_enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`user_id`, `category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `user_reads` (
  `user_id` int(11) NOT NULL,
  `articlle_id` int(11) NOT NULL,
  `read_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `progress_pct` smallint(6) NOT NULL,
  PRIMARY KEY (`user_id`, `articlle_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

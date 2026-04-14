-- 2026-04-20_add_is_guest_to_user.sql
-- Migration: Add is_guest column to users table for guest detection

ALTER TABLE users ADD COLUMN is_guest BOOLEAN NOT NULL DEFAULT FALSE;
-- Migration: Add last_error and last_error_at to ingest_tasks if missing
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

-- Add columns only if they don't exist (SQLite lacks IF NOT EXISTS for ALTER COLUMN, so we guard in runner)
ALTER TABLE ingest_tasks ADD COLUMN last_error TEXT;
ALTER TABLE ingest_tasks ADD COLUMN last_error_at TEXT;

COMMIT;

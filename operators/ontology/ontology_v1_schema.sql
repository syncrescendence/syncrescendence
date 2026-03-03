PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS entities (
  id TEXT PRIMARY KEY,
  kind TEXT NOT NULL,
  slug TEXT NOT NULL,
  title TEXT NOT NULL,
  state TEXT,
  payload_json TEXT NOT NULL DEFAULT '{}',
  source TEXT NOT NULL,
  captured_at TEXT NOT NULL,
  provenance_type TEXT,
  provenance_ref TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_entities_kind_slug
ON entities (kind, slug);

CREATE INDEX IF NOT EXISTS idx_entities_kind_updated
ON entities (kind, updated_at DESC);

CREATE TABLE IF NOT EXISTS relationships (
  id TEXT PRIMARY KEY,
  subject_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
  predicate TEXT NOT NULL,
  object_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
  payload_json TEXT NOT NULL DEFAULT '{}',
  source TEXT NOT NULL,
  captured_at TEXT NOT NULL,
  provenance_type TEXT,
  provenance_ref TEXT,
  created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_relationships_subject
ON relationships (subject_id, predicate);

CREATE INDEX IF NOT EXISTS idx_relationships_object
ON relationships (object_id, predicate);

CREATE TABLE IF NOT EXISTS events (
  id TEXT PRIMARY KEY,
  event_type TEXT NOT NULL,
  source TEXT NOT NULL,
  summary TEXT NOT NULL,
  capture_level TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  emitted_at TEXT NOT NULL,
  reconciled_at TEXT,
  provenance_commit TEXT,
  provenance_path TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_source_emitted
ON events (source, emitted_at DESC);

CREATE INDEX IF NOT EXISTS idx_events_type_emitted
ON events (event_type, emitted_at DESC);

CREATE TABLE IF NOT EXISTS config_snapshots (
  id TEXT PRIMARY KEY,
  snapshot_kind TEXT NOT NULL,
  source TEXT NOT NULL,
  summary TEXT NOT NULL,
  payload_json TEXT NOT NULL,
  captured_at TEXT NOT NULL,
  provenance_commit TEXT,
  provenance_path TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_config_snapshots_kind_captured
ON config_snapshots (snapshot_kind, captured_at DESC);

CREATE TABLE IF NOT EXISTS ingest_checkpoints (
  name TEXT PRIMARY KEY,
  value TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

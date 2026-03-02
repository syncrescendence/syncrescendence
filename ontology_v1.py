#!/usr/bin/env python3
"""Ontology v1 projection store and API surface."""

from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
from contextlib import asynccontextmanager
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent
STATE_DIR = REPO_ROOT / "00-ORCHESTRATION" / "state"
DB_PATH = STATE_DIR / "ontology-v1.sqlite3"
SCHEMA_PATH = REPO_ROOT / "ontology_v1_schema.sql"
LEDGER_PATH = REPO_ROOT / "memory" / "AJNA-EVENT-LEDGER.jsonl"
RUNTIME_SNAPSHOT_PATH = STATE_DIR / "OPENCLAW-RUNTIME-SNAPSHOT.json"
CONFIG_MANIFEST_PATH = REPO_ROOT / "configs" / "manifest.json"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def repo_commit() -> str | None:
    try:
        return (
            subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd=REPO_ROOT,
                text=True,
            )
            .strip()
            or None
        )
    except Exception:
        return None


def db_connect(db_path: Path = DB_PATH) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_path: Path = DB_PATH) -> None:
    schema = SCHEMA_PATH.read_text(encoding="utf-8")
    with closing(db_connect(db_path)) as connection:
        connection.executescript(schema)
        connection.commit()


def slugify(value: str) -> str:
    return "-".join(
        chunk for chunk in "".join(ch.lower() if ch.isalnum() else " " for ch in value).split() if chunk
    )


def ensure_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True)


def upsert_entity(
    connection: sqlite3.Connection,
    *,
    entity_id: str,
    kind: str,
    slug: str,
    title: str,
    state: str | None,
    payload: dict[str, Any],
    source: str,
    captured_at: str,
    provenance_type: str | None,
    provenance_ref: str | None,
) -> None:
    now = utc_now()
    connection.execute(
        """
        INSERT INTO entities (
          id, kind, slug, title, state, payload_json, source, captured_at,
          provenance_type, provenance_ref, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
          kind = excluded.kind,
          slug = excluded.slug,
          title = excluded.title,
          state = excluded.state,
          payload_json = excluded.payload_json,
          source = excluded.source,
          captured_at = excluded.captured_at,
          provenance_type = excluded.provenance_type,
          provenance_ref = excluded.provenance_ref,
          updated_at = excluded.updated_at
        """,
        (
            entity_id,
            kind,
            slug,
            title,
            state,
            ensure_json(payload),
            source,
            captured_at,
            provenance_type,
            provenance_ref,
            now,
            now,
        ),
    )


def upsert_relationship(
    connection: sqlite3.Connection,
    *,
    relationship_id: str,
    subject_id: str,
    predicate: str,
    object_id: str,
    payload: dict[str, Any],
    source: str,
    captured_at: str,
    provenance_type: str | None,
    provenance_ref: str | None,
) -> None:
    connection.execute(
        """
        INSERT INTO relationships (
          id, subject_id, predicate, object_id, payload_json, source,
          captured_at, provenance_type, provenance_ref, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
          subject_id = excluded.subject_id,
          predicate = excluded.predicate,
          object_id = excluded.object_id,
          payload_json = excluded.payload_json,
          source = excluded.source,
          captured_at = excluded.captured_at,
          provenance_type = excluded.provenance_type,
          provenance_ref = excluded.provenance_ref
        """,
        (
            relationship_id,
            subject_id,
            predicate,
            object_id,
            ensure_json(payload),
            source,
            captured_at,
            provenance_type,
            provenance_ref,
            utc_now(),
        ),
    )


def upsert_event_record(
    connection: sqlite3.Connection,
    event: dict[str, Any],
    *,
    provenance_commit: str | None,
    provenance_path: str,
) -> None:
    now = utc_now()
    connection.execute(
        """
        INSERT INTO events (
          id, event_type, source, summary, capture_level, payload_json,
          emitted_at, reconciled_at, provenance_commit, provenance_path,
          created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
          event_type = excluded.event_type,
          source = excluded.source,
          summary = excluded.summary,
          capture_level = excluded.capture_level,
          payload_json = excluded.payload_json,
          emitted_at = excluded.emitted_at,
          reconciled_at = excluded.reconciled_at,
          provenance_commit = excluded.provenance_commit,
          provenance_path = excluded.provenance_path,
          updated_at = excluded.updated_at
        """,
        (
            event["id"],
            event["type"],
            event["source"],
            event["summary"],
            event["capture_level"],
            ensure_json(event.get("payload", {})),
            event["emitted_at"],
            event.get("reconciled_at"),
            provenance_commit,
            provenance_path,
            now,
            now,
        ),
    )


def upsert_config_snapshot(
    connection: sqlite3.Connection,
    *,
    snapshot_id: str,
    snapshot_kind: str,
    source: str,
    summary: str,
    payload: dict[str, Any],
    captured_at: str,
    provenance_commit: str | None,
    provenance_path: str,
) -> None:
    now = utc_now()
    connection.execute(
        """
        INSERT INTO config_snapshots (
          id, snapshot_kind, source, summary, payload_json, captured_at,
          provenance_commit, provenance_path, created_at, updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
          snapshot_kind = excluded.snapshot_kind,
          source = excluded.source,
          summary = excluded.summary,
          payload_json = excluded.payload_json,
          captured_at = excluded.captured_at,
          provenance_commit = excluded.provenance_commit,
          provenance_path = excluded.provenance_path,
          updated_at = excluded.updated_at
        """,
        (
            snapshot_id,
            snapshot_kind,
            source,
            summary,
            ensure_json(payload),
            captured_at,
            provenance_commit,
            provenance_path,
            now,
            now,
        ),
    )


def entity_exists(connection: sqlite3.Connection, entity_id: str) -> bool:
    row = connection.execute("SELECT 1 FROM entities WHERE id = ?", (entity_id,)).fetchone()
    return row is not None


def record_checkpoint(connection: sqlite3.Connection, name: str, value: str) -> None:
    connection.execute(
        """
        INSERT INTO ingest_checkpoints (name, value, updated_at)
        VALUES (?, ?, ?)
        ON CONFLICT(name) DO UPDATE SET
          value = excluded.value,
          updated_at = excluded.updated_at
        """,
        (name, value, utc_now()),
    )


def project_runtime_snapshot(connection: sqlite3.Connection, commit_sha: str | None) -> int:
    if not RUNTIME_SNAPSHOT_PATH.exists():
        return 0
    runtime = load_json(RUNTIME_SNAPSHOT_PATH)
    entity_id = f"agent-state:{runtime['agent']}"
    browser_state = "browser-enabled" if runtime.get("browser_enabled") else "browser-disabled"
    model = runtime.get("model_primary") or "unknown-model"
    payload = {
        "gateway": runtime.get("gateway", {}),
        "channels": runtime.get("channels", {}),
        "tools_deny": runtime.get("tools_deny", []),
        "workspace_path": runtime.get("workspace_path"),
        "skills_installed": runtime.get("skills_installed", []),
    }
    upsert_entity(
        connection,
        entity_id=entity_id,
        kind="AgentState",
        slug=slugify(runtime["agent"]),
        title=f"{runtime['agent']} runtime state ({model})",
        state=browser_state,
        payload=payload,
        source="repo-runtime-snapshot",
        captured_at=runtime["captured_at"],
        provenance_type="repo-path",
        provenance_ref=str(RUNTIME_SNAPSHOT_PATH.relative_to(REPO_ROOT)),
    )
    upsert_config_snapshot(
        connection,
        snapshot_id=f"config-snapshot:runtime:{runtime['agent']}",
        snapshot_kind="runtime_snapshot",
        source="repo-runtime-snapshot",
        summary=f"OpenClaw runtime snapshot for {runtime['agent']}",
        payload=runtime,
        captured_at=runtime["captured_at"],
        provenance_commit=commit_sha,
        provenance_path=str(RUNTIME_SNAPSHOT_PATH.relative_to(REPO_ROOT)),
    )
    return 1


def project_config_manifest(connection: sqlite3.Connection, commit_sha: str | None) -> int:
    if not CONFIG_MANIFEST_PATH.exists():
        return 0
    manifest = load_json(CONFIG_MANIFEST_PATH)
    host = manifest.get("generated_at_host", "unknown-host")
    snapshot_id = f"config-snapshot:manifest:{host}"
    upsert_config_snapshot(
        connection,
        snapshot_id=snapshot_id,
        snapshot_kind="rendered_manifest",
        source="repo-config-manifest",
        summary=f"Rendered harness manifest for {host}",
        payload=manifest,
        captured_at=utc_now(),
        provenance_commit=commit_sha,
        provenance_path=str(CONFIG_MANIFEST_PATH.relative_to(REPO_ROOT)),
    )
    upsert_entity(
        connection,
        entity_id=snapshot_id,
        kind="ConfigSnapshot",
        slug=slugify(host),
        title=f"Rendered config manifest for {host}",
        state="active",
        payload={
            "machine_manifest": manifest.get("machine_manifest"),
            "target_count": len(manifest.get("targets", [])),
            "outputs_root": manifest.get("outputs_root"),
        },
        source="repo-config-manifest",
        captured_at=utc_now(),
        provenance_type="repo-path",
        provenance_ref=str(CONFIG_MANIFEST_PATH.relative_to(REPO_ROOT)),
    )
    return 1


def project_event_entities(connection: sqlite3.Connection, event: dict[str, Any], commit_sha: str | None) -> int:
    count = 0
    event_entity_id = f"exo-event:{event['id']}"
    agent_state_id = "agent-state:ajna"
    event_payload = {
        "surface": event.get("surface"),
        "artifact_class": event.get("artifact_class"),
        "type": event["type"],
        "capture_level": event["capture_level"],
        "durable_capture": event.get("durable_capture"),
        "repo_paths": event.get("repo_paths", []),
        "ontology_entities": event.get("ontology_entities", []),
    }
    upsert_entity(
        connection,
        entity_id=event_entity_id,
        kind="ExoEvent",
        slug=slugify(event["id"]),
        title=event["summary"][:160],
        state=event["type"],
        payload=event_payload,
        source=event["source"],
        captured_at=event["emitted_at"],
        provenance_type="repo-path",
        provenance_ref=str(LEDGER_PATH.relative_to(REPO_ROOT)),
    )
    if not entity_exists(connection, agent_state_id):
        upsert_entity(
            connection,
            entity_id=agent_state_id,
            kind="AgentState",
            slug="ajna",
            title="Ajna runtime state (pending snapshot)",
            state="pending-snapshot",
            payload={},
            source=event["source"],
            captured_at=event["emitted_at"],
            provenance_type="repo-path",
            provenance_ref=str(LEDGER_PATH.relative_to(REPO_ROOT)),
        )
    upsert_relationship(
        connection,
        relationship_id=f"rel:{event_entity_id}:updates:agent-state-ajna",
        subject_id=event_entity_id,
        predicate="updates",
        object_id=agent_state_id,
        payload={"event_type": event["type"]},
        source=event["source"],
        captured_at=event["emitted_at"],
        provenance_type="repo-commit",
        provenance_ref=commit_sha,
    )
    count += 1

    task = event.get("payload", {}).get("task")
    if isinstance(task, dict) and task.get("id") and task.get("title"):
        task_id = f"task:{task['id']}"
        upsert_entity(
            connection,
            entity_id=task_id,
            kind="Task",
            slug=slugify(task["id"]),
            title=task["title"],
            state=task.get("status") or "active",
            payload=task,
            source=event["source"],
            captured_at=event["emitted_at"],
            provenance_type="repo-path",
            provenance_ref=str(LEDGER_PATH.relative_to(REPO_ROOT)),
        )
        upsert_relationship(
            connection,
            relationship_id=f"rel:{event_entity_id}:references:{task_id}",
            subject_id=event_entity_id,
            predicate="references",
            object_id=task_id,
            payload={},
            source=event["source"],
            captured_at=event["emitted_at"],
            provenance_type="repo-commit",
            provenance_ref=commit_sha,
        )
        count += 1

    knowledge_item = event.get("payload", {}).get("knowledge_item")
    if isinstance(knowledge_item, dict) and knowledge_item.get("id") and knowledge_item.get("title"):
        knowledge_id = f"knowledge-item:{knowledge_item['id']}"
        upsert_entity(
            connection,
            entity_id=knowledge_id,
            kind="KnowledgeItem",
            slug=slugify(knowledge_item["id"]),
            title=knowledge_item["title"],
            state=knowledge_item.get("status") or "indexed",
            payload=knowledge_item,
            source=event["source"],
            captured_at=event["emitted_at"],
            provenance_type="repo-path",
            provenance_ref=str(LEDGER_PATH.relative_to(REPO_ROOT)),
        )
        upsert_relationship(
            connection,
            relationship_id=f"rel:{event_entity_id}:references:{knowledge_id}",
            subject_id=event_entity_id,
            predicate="references",
            object_id=knowledge_id,
            payload={},
            source=event["source"],
            captured_at=event["emitted_at"],
            provenance_type="repo-commit",
            provenance_ref=commit_sha,
        )
        count += 1

    return count


def project_repo_state(db_path: Path = DB_PATH) -> dict[str, int]:
    init_db(db_path)
    commit_sha = repo_commit()
    events = load_jsonl(LEDGER_PATH)
    projected = {"events": 0, "entities": 0, "snapshots": 0}

    with closing(db_connect(db_path)) as connection:
        projected["entities"] += project_runtime_snapshot(connection, commit_sha)
        projected["snapshots"] += project_config_manifest(connection, commit_sha)

        for event in events:
            upsert_event_record(
                connection,
                event,
                provenance_commit=commit_sha,
                provenance_path=str(LEDGER_PATH.relative_to(REPO_ROOT)),
            )
            projected["events"] += 1
            projected["entities"] += project_event_entities(connection, event, commit_sha)

        checkpoint_value = json.dumps(
            {
                "event_count": projected["events"],
                "last_projected_at": utc_now(),
                "commit": commit_sha,
            },
            sort_keys=True,
        )
        record_checkpoint(connection, "repo_projection", checkpoint_value)
        connection.commit()

    return projected


def fetch_rows(query: str, params: tuple[Any, ...] = (), db_path: Path = DB_PATH) -> list[dict[str, Any]]:
    with closing(db_connect(db_path)) as connection:
        rows = connection.execute(query, params).fetchall()
    parsed: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        for key in ("payload_json",):
            if key in item and item[key] is not None:
                item[key] = json.loads(item[key])
        parsed.append(item)
    return parsed


def health_payload(db_path: Path = DB_PATH) -> dict[str, Any]:
    with closing(db_connect(db_path)) as connection:
        entity_count = connection.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
        event_count = connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        snapshot_count = connection.execute("SELECT COUNT(*) FROM config_snapshots").fetchone()[0]
    return {
        "status": "ok",
        "db_path": str(db_path),
        "entity_count": entity_count,
        "event_count": event_count,
        "config_snapshot_count": snapshot_count,
    }


def validate_event_payload(event: dict[str, Any]) -> None:
    required = {
        "id",
        "type",
        "source",
        "surface",
        "artifact_class",
        "summary",
        "capture_level",
        "durable_capture",
        "emitted_at",
    }
    missing = sorted(required - event.keys())
    if missing:
        raise ValueError(f"missing event fields: {missing}")


def ingest_event(event: dict[str, Any], db_path: Path = DB_PATH) -> dict[str, Any]:
    validate_event_payload(event)
    init_db(db_path)
    commit_sha = repo_commit()
    normalized = {
        "id": event["id"],
        "type": event["type"],
        "source": event["source"],
        "surface": event["surface"],
        "artifact_class": event["artifact_class"],
        "summary": event["summary"],
        "capture_level": event["capture_level"],
        "durable_capture": event["durable_capture"],
        "payload": event.get("payload", {}),
        "emitted_at": event["emitted_at"],
        "reconciled_at": event.get("reconciled_at", utc_now()),
        "repo_paths": event.get("repo_paths", []),
        "ontology_entities": event.get("ontology_entities", []),
    }
    with closing(db_connect(db_path)) as connection:
        upsert_event_record(
            connection,
            normalized,
            provenance_commit=commit_sha,
            provenance_path="api:/ingest/event",
        )
        projected_entities = project_event_entities(connection, normalized, commit_sha)
        record_checkpoint(
            connection,
            "api_ingest",
            json.dumps({"last_event_id": normalized["id"], "updated_at": utc_now()}, sort_keys=True),
        )
        connection.commit()
    return {"event_id": normalized["id"], "projected_entities": projected_entities}


def build_app(db_path: Path = DB_PATH):
    try:
        from fastapi import FastAPI, HTTPException, Query
    except ImportError as exc:
        raise SystemExit(
            "FastAPI is not installed. Install requirements-ontology.txt before running ontology_v1.py serve."
        ) from exc

    @asynccontextmanager
    async def lifespan(_: Any):
        init_db(db_path)
        yield

    app = FastAPI(title="Syncrescendence Ontology v1", version="0.1.0", lifespan=lifespan)

    @app.get("/health")
    def health() -> dict[str, Any]:
        return health_payload(db_path)

    @app.get("/entities")
    def list_entities(kind: str | None = None, limit: int = Query(default=50, le=200)) -> dict[str, Any]:
        if kind:
            rows = fetch_rows(
                """
                SELECT id, kind, slug, title, state, payload_json, source, captured_at, provenance_type,
                       provenance_ref, created_at, updated_at
                FROM entities
                WHERE kind = ?
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (kind, limit),
                db_path,
            )
        else:
            rows = fetch_rows(
                """
                SELECT id, kind, slug, title, state, payload_json, source, captured_at, provenance_type,
                       provenance_ref, created_at, updated_at
                FROM entities
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (limit,),
                db_path,
            )
        return {"items": rows}

    @app.get("/entities/{entity_id}")
    def get_entity(entity_id: str) -> dict[str, Any]:
        rows = fetch_rows(
            """
            SELECT id, kind, slug, title, state, payload_json, source, captured_at, provenance_type,
                   provenance_ref, created_at, updated_at
            FROM entities
            WHERE id = ?
            """,
            (entity_id,),
            db_path,
        )
        if not rows:
            raise HTTPException(status_code=404, detail="entity not found")
        relationships = fetch_rows(
            """
            SELECT id, subject_id, predicate, object_id, payload_json, source, captured_at,
                   provenance_type, provenance_ref, created_at
            FROM relationships
            WHERE subject_id = ? OR object_id = ?
            ORDER BY created_at DESC
            """,
            (entity_id, entity_id),
            db_path,
        )
        return {"item": rows[0], "relationships": relationships}

    @app.get("/events")
    def list_events(source: str | None = None, limit: int = Query(default=50, le=200)) -> dict[str, Any]:
        if source:
            rows = fetch_rows(
                """
                SELECT id, event_type, source, summary, capture_level, payload_json, emitted_at,
                       reconciled_at, provenance_commit, provenance_path, created_at, updated_at
                FROM events
                WHERE source = ?
                ORDER BY emitted_at DESC
                LIMIT ?
                """,
                (source, limit),
                db_path,
            )
        else:
            rows = fetch_rows(
                """
                SELECT id, event_type, source, summary, capture_level, payload_json, emitted_at,
                       reconciled_at, provenance_commit, provenance_path, created_at, updated_at
                FROM events
                ORDER BY emitted_at DESC
                LIMIT ?
                """,
                (limit,),
                db_path,
            )
        return {"items": rows}

    @app.post("/ingest/event")
    def api_ingest_event(event: dict[str, Any]) -> dict[str, Any]:
        try:
            result = ingest_event(event, db_path)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {"status": "ok", **result}

    @app.post("/project/repo")
    def api_project_repo() -> dict[str, Any]:
        projected = project_repo_state(db_path)
        return {"status": "ok", "projected": projected}

    return app


def smoke_test(db_path: Path = DB_PATH) -> None:
    try:
        from fastapi.testclient import TestClient
    except ImportError as exc:
        raise SystemExit(
            "FastAPI test dependencies are not installed. Install requirements-ontology.txt before smoke testing."
        ) from exc

    init_db(db_path)
    project_repo_state(db_path)
    client = TestClient(build_app(db_path))
    health = client.get("/health")
    if health.status_code != 200:
        raise SystemExit("health endpoint failed")
    entities = client.get("/entities", params={"limit": 5})
    if entities.status_code != 200:
        raise SystemExit("entities endpoint failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--db-path", default=str(DB_PATH))

    project_parser = subparsers.add_parser("project-repo")
    project_parser.add_argument("--db-path", default=str(DB_PATH))

    serve_parser = subparsers.add_parser("serve")
    serve_parser.add_argument("--db-path", default=str(DB_PATH))
    serve_parser.add_argument("--host", default="127.0.0.1")
    serve_parser.add_argument("--port", type=int, default=8787)

    smoke_parser = subparsers.add_parser("smoke")
    smoke_parser.add_argument("--db-path", default=str(DB_PATH))

    args = parser.parse_args()
    db_path = Path(args.db_path).expanduser()

    if args.command == "init":
        init_db(db_path)
        print(f"Initialized ontology schema at {db_path}")
        return 0

    if args.command == "project-repo":
        projected = project_repo_state(db_path)
        print(json.dumps(projected, indent=2, sort_keys=True))
        return 0

    if args.command == "serve":
        try:
            import uvicorn
        except ImportError as exc:
            raise SystemExit(
                "uvicorn is not installed. Install requirements-ontology.txt before running the API."
            ) from exc
        uvicorn.run(build_app(db_path), host=args.host, port=args.port)
        return 0

    if args.command == "smoke":
        smoke_test(db_path)
        print("Ontology v1 smoke test passed")
        return 0

    raise SystemExit(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())

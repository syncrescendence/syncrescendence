#!/usr/bin/env python3
"""Ingest shared agent event files from the OpenClaw workspace into repo state."""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import json
import shutil
import subprocess
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse


REPO_ROOT = Path(__file__).resolve().parent
WORKSPACE_ROOT = Path.home() / ".openclaw" / "workspace"
EVENTS_ROOT = WORKSPACE_ROOT / "events"
INBOX_DIR = EVENTS_ROOT / "inbox"
ARCHIVE_DIR = EVENTS_ROOT / "archive"
FAILED_DIR = EVENTS_ROOT / "failed"
CAPTURE_POLICY_PATH = REPO_ROOT / "00-ORCHESTRATION" / "state" / "EXOCORTEX-CAPTURE-POLICY.json"

LEDGER_PATH = REPO_ROOT / "memory" / "AJNA-EVENT-LEDGER.jsonl"
SUMMARY_PATH = REPO_ROOT / "memory" / "AJNA-EVENT-SUMMARY.md"
STATE_PATH = REPO_ROOT / "00-ORCHESTRATION" / "state" / "AJNA-EVENT-RECONCILIATION.json"
LOCK_PATH = REPO_ROOT / "00-ORCHESTRATION" / "state" / "AJNA-EVENT-RECONCILIATION.lock"

REQUIRED_FIELDS = {
    "id",
    "emitted_at",
    "source",
    "surface",
    "artifact_class",
    "type",
    "summary",
    "capture_level",
    "durable_capture",
    "payload",
}
VALID_CAPTURE_LEVELS = {"pointer", "summary", "full"}
ALLOWED_SOURCES = {"ajna", "manus", "commander", "system"}


def ensure_dirs() -> None:
    for path in (INBOX_DIR, ARCHIVE_DIR, FAILED_DIR, LEDGER_PATH.parent, SUMMARY_PATH.parent, STATE_PATH.parent):
        path.mkdir(parents=True, exist_ok=True)


@contextlib.contextmanager
def reconcile_lock():
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    with LOCK_PATH.open("w", encoding="utf-8") as handle:
        fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_existing_ids() -> set[str]:
    if not LEDGER_PATH.exists():
        return set()
    seen: set[str] = set()
    for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            seen.add(json.loads(line)["id"])
        except Exception:
            continue
    return seen


def load_capture_policy() -> dict:
    return json.loads(CAPTURE_POLICY_PATH.read_text(encoding="utf-8"))


def payload_keys(value) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key))
            keys.update(payload_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(payload_keys(nested))
    return keys


def validate_event(event: dict, path: Path, policy: dict) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_FIELDS - event.keys()
    if missing:
        errors.append(f"{path.name}: missing fields {sorted(missing)}")
    if event.get("source") not in ALLOWED_SOURCES:
        errors.append(f"{path.name}: source must be one of {sorted(ALLOWED_SOURCES)}")
    if event.get("capture_level") not in VALID_CAPTURE_LEVELS:
        errors.append(f"{path.name}: invalid capture_level {event.get('capture_level')!r}")
    if event.get("surface") not in set(policy.get("surfaces", [])):
        errors.append(f"{path.name}: invalid surface {event.get('surface')!r}")
    artifact_class = event.get("artifact_class")
    artifact_policy = policy.get("artifact_classes", {}).get(artifact_class)
    if artifact_policy is None:
        errors.append(f"{path.name}: invalid artifact_class {artifact_class!r}")
    durable_capture = event.get("durable_capture")
    if durable_capture not in set(policy.get("durable_capture_modes", [])):
        errors.append(f"{path.name}: invalid durable_capture {durable_capture!r}")
    elif artifact_policy and durable_capture not in set(artifact_policy.get("allowed_durable_capture", [])):
        errors.append(
            f"{path.name}: durable_capture {durable_capture!r} not allowed for artifact_class {artifact_class!r}"
        )
    if not isinstance(event.get("payload"), dict):
        errors.append(f"{path.name}: payload must be an object")
    if not isinstance(event.get("summary"), str):
        errors.append(f"{path.name}: summary must be a string")
    repo_paths = event.get("repo_paths", [])
    if repo_paths and not isinstance(repo_paths, list):
        errors.append(f"{path.name}: repo_paths must be a list")
    forbidden_substrings = policy.get("forbidden_repo_path_substrings", [])
    for repo_path in repo_paths if isinstance(repo_paths, list) else []:
        if not isinstance(repo_path, str):
            errors.append(f"{path.name}: repo_paths entries must be strings")
            continue
        if not repo_path.startswith(str(REPO_ROOT)):
            errors.append(f"{path.name}: repo_path {repo_path!r} must stay under repo root")
        if any(fragment in repo_path for fragment in forbidden_substrings):
            errors.append(f"{path.name}: repo_path {repo_path!r} points at forbidden local state")
    forbidden_payload = set(artifact_policy.get("forbidden_payload_keys", [])) if artifact_policy else set()
    seen_payload_keys = payload_keys(event.get("payload"))
    for forbidden_key in sorted(forbidden_payload & seen_payload_keys):
        errors.append(f"{path.name}: payload contains forbidden key {forbidden_key!r}")
    return errors


def write_summary(events: list[dict]) -> None:
    lines = [
        "# Agent Event Summary",
        "",
        f"**Updated**: {utc_now()}",
        "",
    ]
    if not events:
        lines.append("- No reconciled events yet.")
    else:
        source_counts: dict[str, int] = {}
        for event in events:
            source = str(event.get("source", "unknown"))
            source_counts[source] = source_counts.get(source, 0) + 1
        lines.extend(["## Source Counts", ""])
        for source, count in sorted(source_counts.items()):
            lines.append(f"- `{source}`: `{count}`")
        lines.extend(["", "## Recent Events", ""])
        for event in events[-10:][::-1]:
            lines.extend(
                [
                    f"### {event['id']}",
                    f"- Emitted: `{event['emitted_at']}`",
                    f"- Type: `{event['type']}`",
                    f"- Surface: `{event.get('surface', 'unknown')}`",
                    f"- Artifact class: `{event.get('artifact_class', 'unknown')}`",
                    f"- Capture level: `{event['capture_level']}`",
                    f"- Durable capture: `{event.get('durable_capture', 'unknown')}`",
                    f"- Summary: {event['summary']}",
                    "",
                ]
            )
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def load_recent_events() -> list[dict]:
    if not LEDGER_PATH.exists():
        return []
    events: list[dict] = []
    for line in LEDGER_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except Exception:
            continue
    return events


def write_state(processed: list[str], failed: list[str], skipped: list[str]) -> None:
    source_counts: dict[str, int] = {}
    for event in load_recent_events():
        source = str(event.get("source", "unknown"))
        source_counts[source] = source_counts.get(source, 0) + 1
    state = {
        "last_run_at": utc_now(),
        "processed_count": len(processed),
        "processed_ids": processed,
        "failed_count": len(failed),
        "failed_files": failed,
        "skipped_duplicates": skipped,
        "source_counts": source_counts,
    }
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def archive_file(path: Path, destination_dir: Path) -> None:
    if not path.exists():
        return
    destination = destination_dir / path.name
    if destination.exists():
        destination = destination_dir / f"{path.stem}-{int(datetime.now().timestamp())}{path.suffix}"
    shutil.move(str(path), str(destination))


def project_event_to_ontology(event: dict, ontology_url: str, timeout_seconds: float) -> tuple[bool, str | None]:
    payload_text = json.dumps(event)
    payload = payload_text.encode("utf-8")
    request = urllib.request.Request(
        ontology_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            response.read()
        return True, None
    except urllib.error.URLError as exc:
        parsed = urlparse(ontology_url)
        host = parsed.hostname
        if host:
            code, stdout, stderr = project_via_edge_resolve(
                host=host,
                ontology_url=ontology_url,
                payload_text=payload_text,
                timeout_seconds=timeout_seconds,
            )
            if code == 0:
                return True, None
            if stdout or stderr:
                return False, (stderr or stdout).strip()
        reason = getattr(exc, "reason", exc)
        return False, str(reason)


def dig_records(host: str, timeout_seconds: float) -> list[str]:
    try:
        result = subprocess.run(
            ["dig", "+short", host],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_seconds,
        )
    except Exception:
        return []
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def project_via_edge_resolve(
    *,
    host: str,
    ontology_url: str,
    payload_text: str,
    timeout_seconds: float,
) -> tuple[int, str, str]:
    for address in dig_records(host, timeout_seconds):
        result = subprocess.run(
            [
                "curl",
                "--silent",
                "--show-error",
                "--output",
                "/dev/null",
                "--write-out",
                "%{http_code}",
                "--max-time",
                str(int(timeout_seconds)),
                "--resolve",
                f"{host}:443:{address}",
                "-H",
                "Content-Type: application/json",
                "--data",
                payload_text,
                ontology_url,
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_seconds,
        )
        if result.returncode == 0 and result.stdout.strip().isdigit():
            status = int(result.stdout.strip())
            if 200 <= status < 300:
                return 0, result.stdout, result.stderr
    return 1, "", "Edge-resolved POST failed"


def reconcile(project_ontology: bool, ontology_url: str, ontology_timeout_seconds: float) -> int:
    ensure_dirs()
    with reconcile_lock():
        policy = load_capture_policy()
        existing_ids = load_existing_ids()
        processed: list[str] = []
        failed: list[str] = []
        skipped: list[str] = []
        projected_to_ontology: list[str] = []
        ontology_failures: list[str] = []

        for path in sorted(INBOX_DIR.glob("*.json")):
            try:
                event = json.loads(path.read_text(encoding="utf-8"))
            except FileNotFoundError:
                continue
            except json.JSONDecodeError:
                failed.append(path.name)
                archive_file(path, FAILED_DIR)
                continue

            errors = validate_event(event, path, policy)
            if errors:
                failed.append(path.name)
                archive_file(path, FAILED_DIR)
                continue

            if event["id"] in existing_ids:
                skipped.append(event["id"])
                archive_file(path, ARCHIVE_DIR)
                continue

            normalized = {
                "id": event["id"],
                "emitted_at": event["emitted_at"],
                "source": event["source"],
                "surface": event["surface"],
                "artifact_class": event["artifact_class"],
                "type": event["type"],
                "capture_level": event["capture_level"],
                "durable_capture": event["durable_capture"],
                "summary": event["summary"],
                "repo_paths": event.get("repo_paths", []),
                "ontology_entities": event.get("ontology_entities", []),
                "payload": event["payload"],
                "reconciled_at": utc_now(),
            }
            with LEDGER_PATH.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(normalized, sort_keys=True) + "\n")
            processed.append(event["id"])
            if project_ontology:
                success, error = project_event_to_ontology(
                    normalized,
                    ontology_url=ontology_url,
                    timeout_seconds=ontology_timeout_seconds,
                )
                if success:
                    projected_to_ontology.append(event["id"])
                else:
                    ontology_failures.append(f"{event['id']}: {error}")
            existing_ids.add(event["id"])
            archive_file(path, ARCHIVE_DIR)

        write_state(processed, failed, skipped)
        write_summary(load_recent_events())

        print(f"Processed: {len(processed)}")
        print(f"Failed: {len(failed)}")
        print(f"Skipped duplicates: {len(skipped)}")
        if project_ontology:
            print(f"Projected to ontology: {len(projected_to_ontology)}")
            if ontology_failures:
                print("Ontology projection failures:")
                for failure in ontology_failures:
                    print(f"- {failure}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ensure-dirs", action="store_true")
    parser.add_argument("--project-ontology", action="store_true")
    parser.add_argument("--ontology-url", default="http://127.0.0.1:8787/ingest/event")
    parser.add_argument("--ontology-timeout-seconds", type=float, default=2.0)
    args = parser.parse_args()
    ensure_dirs()
    if args.ensure_dirs:
        print(f"Ensured event directories under {EVENTS_ROOT}")
        return 0
    return reconcile(
        project_ontology=args.project_ontology,
        ontology_url=args.ontology_url,
        ontology_timeout_seconds=args.ontology_timeout_seconds,
    )


if __name__ == "__main__":
    raise SystemExit(main())

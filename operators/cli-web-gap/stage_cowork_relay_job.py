#!/usr/bin/env python3
"""Stage a Cowork relay job in the designated folder-based queue."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
import re
import shutil


REPO_ROOT = Path(__file__).resolve().parents[2]
RELAY_ROOT = REPO_ROOT / "00-ORCHESTRATION" / "relay" / "cowork-v1"
INBOX_DIR = RELAY_ROOT / "jobs" / "inbox"
RUNNING_DIR = RELAY_ROOT / "jobs" / "running"
COMPLETED_DIR = RELAY_ROOT / "jobs" / "completed"
FAILED_DIR = RELAY_ROOT / "jobs" / "failed"
ARTIFACTS_IN_DIR = RELAY_ROOT / "artifacts" / "incoming"
ARTIFACTS_OUT_DIR = RELAY_ROOT / "artifacts" / "outgoing"
PACKETS_DIR = RELAY_ROOT / "packets"
ATTACHMENTS_DIR = RELAY_ROOT / "attachments"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def compact_timestamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%d-%H%M%S-%f")


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def repo_rel(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def normalize_repo_path(value: str) -> str:
    path = (REPO_ROOT / value).resolve()
    if not str(path).startswith(str(REPO_ROOT)):
        raise SystemExit(f"Path must stay inside repo root: {value}")
    return str(path.relative_to(REPO_ROOT))


def ensure_runtime_dirs() -> None:
    for path in [INBOX_DIR, RUNNING_DIR, COMPLETED_DIR, FAILED_DIR, ARTIFACTS_IN_DIR, ARTIFACTS_OUT_DIR, PACKETS_DIR, ATTACHMENTS_DIR]:
        path.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--surface", required=True, choices=["perplexity", "oracle", "notebooklm", "claude_cowork"])
    parser.add_argument("--job-type", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--packet", required=True, help="Repo-relative path to the source packet or instruction artifact.")
    parser.add_argument("--response", required=True, help="Repo-relative path where the returned response artifact should land.")
    parser.add_argument("--summary", required=True, help="One-line summary used later for the response bridge.")
    parser.add_argument("--instruction", action="append", default=[])
    parser.add_argument("--attachment", action="append", default=[])
    parser.add_argument("--metadata", default="{}")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    ensure_runtime_dirs()

    packet_rel = normalize_repo_path(args.packet)
    response_rel = normalize_repo_path(args.response)
    packet_path = REPO_ROOT / packet_rel
    if not packet_path.exists():
        raise SystemExit(f"Packet does not exist: {packet_path}")

    metadata = json.loads(args.metadata)
    if not isinstance(metadata, dict):
        raise SystemExit("--metadata must decode to a JSON object.")

    attachment_rels = [normalize_repo_path(item) for item in args.attachment]
    for attachment in attachment_rels:
        attachment_path = REPO_ROOT / attachment
        if not attachment_path.exists():
            raise SystemExit(f"Attachment does not exist: {attachment_path}")

    slug = slugify(args.title)
    job_id = f"{args.surface}-{compact_timestamp()}-{slug}"
    job_path = INBOX_DIR / f"{job_id}.json"
    if job_path.exists() and not args.force:
        raise SystemExit(f"Job already exists: {job_path}")

    packet_stage_name = f"{job_id}-{packet_path.name}"
    packet_stage_path = PACKETS_DIR / packet_stage_name
    shutil.copy2(packet_path, packet_stage_path)

    staged_attachments: list[str] = []
    if attachment_rels:
        attachment_stage_dir = ATTACHMENTS_DIR / job_id
        attachment_stage_dir.mkdir(parents=True, exist_ok=True)
        for attachment_rel in attachment_rels:
            source_path = REPO_ROOT / attachment_rel
            staged_path = attachment_stage_dir / source_path.name
            shutil.copy2(source_path, staged_path)
            staged_attachments.append(repo_rel(staged_path))

    response_name = Path(response_rel).name
    artifact_path = ARTIFACTS_OUT_DIR / response_name
    status_path = ARTIFACTS_OUT_DIR / f"{job_id}.status.json"

    job = {
        "id": job_id,
        "created_at": utc_now(),
        "surface": args.surface,
        "job_type": args.job_type,
        "title": args.title,
        "packet": packet_rel,
        "packet_staging_path": repo_rel(packet_stage_path),
        "response_artifact": response_rel,
        "response_staging_path": repo_rel(artifact_path),
        "status_path": repo_rel(status_path),
        "summary_for_bridge": args.summary,
        "attachments": attachment_rels,
        "attachment_staging_paths": staged_attachments,
        "instructions": args.instruction,
        "metadata": metadata,
    }
    job_path.write_text(json.dumps(job, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(job_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

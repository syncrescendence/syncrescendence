#!/usr/bin/env python3
"""Write repo-backed markdown for Obsidian workflows and emit compliant Ajna-style events."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
WORKSPACE_EVENTS_INBOX = Path.home() / ".openclaw" / "workspace" / "events" / "inbox"
FORBIDDEN_SUBPATHS = [REPO_ROOT / ".obsidian"]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def compact_timestamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%d-%H%M%S")


def slugify(value: str) -> str:
    return "-".join(
        piece for piece in "".join(ch.lower() if ch.isalnum() else " " for ch in value).split() if piece
    )


def repo_relative_target(target: str) -> Path:
    path = (REPO_ROOT / target).resolve()
    if not str(path).startswith(str(REPO_ROOT)):
        raise SystemExit("Target path must stay inside the repo root.")
    for forbidden in FORBIDDEN_SUBPATHS:
        if str(path).startswith(str(forbidden)):
            raise SystemExit("Target path must not write into .obsidian/ local state.")
    return path


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def run_obsidian_cli(arguments: list[str]) -> None:
    binary = "obsidian"
    result = subprocess.run([binary, *arguments], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip() or f"{binary} exited {result.returncode}"
        raise SystemExit(f"Obsidian CLI failed: {stderr}")


def emit_event(
    *,
    event_type: str,
    summary: str,
    durable_capture: str,
    repo_paths: list[str],
    payload: dict,
) -> Path:
    WORKSPACE_EVENTS_INBOX.mkdir(parents=True, exist_ok=True)
    stamp = compact_timestamp()
    event_id = f"ajna-{stamp}-{slugify(event_type)}"
    event_path = WORKSPACE_EVENTS_INBOX / f"{event_id}.json"
    event = {
        "id": event_id,
        "emitted_at": utc_now(),
        "source": "ajna",
        "surface": "obsidian",
        "artifact_class": "obsidian_repo_markdown",
        "type": event_type,
        "summary": summary,
        "capture_level": "summary",
        "durable_capture": durable_capture,
        "repo_paths": repo_paths,
        "payload": payload,
    }
    event_path.write_text(json.dumps(event, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return event_path


def cmd_create_note(args) -> int:
    target = repo_relative_target(args.target)
    ensure_parent(target)
    if target.exists() and not args.overwrite:
        raise SystemExit(f"Refusing to overwrite existing file: {target}")
    body = args.body if args.body is not None else ""
    target.write_text(body.rstrip() + ("\n" if body and not body.endswith("\n") else ""), encoding="utf-8")
    event_path = emit_event(
        event_type="obsidian_note_create",
        summary=args.summary or f"Created repo-backed Obsidian note at {target.relative_to(REPO_ROOT)}.",
        durable_capture=args.durable_capture,
        repo_paths=[str(target)],
        payload={
            "action": "create",
            "target": str(target.relative_to(REPO_ROOT)),
            "line_count": len(body.splitlines()) if body else 0,
        },
    )
    if args.run_cli:
        run_obsidian_cli(["open", str(target)])
    print(f"Wrote note: {target}")
    print(f"Emitted event: {event_path}")
    return 0


def cmd_append_note(args) -> int:
    target = repo_relative_target(args.target)
    ensure_parent(target)
    append_text = args.body if args.body is not None else ""
    with target.open("a", encoding="utf-8") as handle:
        if target.stat().st_size > 0 and not append_text.startswith("\n"):
            handle.write("\n")
        handle.write(append_text.rstrip() + ("\n" if append_text and not append_text.endswith("\n") else ""))
    event_path = emit_event(
        event_type="obsidian_note_append",
        summary=args.summary or f"Appended repo-backed Obsidian note at {target.relative_to(REPO_ROOT)}.",
        durable_capture=args.durable_capture,
        repo_paths=[str(target)],
        payload={
            "action": "append",
            "target": str(target.relative_to(REPO_ROOT)),
            "line_count": len(append_text.splitlines()) if append_text else 0,
        },
    )
    if args.run_cli:
        run_obsidian_cli(["open", str(target)])
    print(f"Appended note: {target}")
    print(f"Emitted event: {event_path}")
    return 0


def cmd_emit_event(args) -> int:
    repo_paths = [str(repo_relative_target(target)) for target in args.repo_paths]
    payload = json.loads(args.payload) if args.payload else {}
    event_path = emit_event(
        event_type=args.event_type,
        summary=args.summary,
        durable_capture=args.durable_capture,
        repo_paths=repo_paths,
        payload=payload,
    )
    print(f"Emitted event: {event_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create-note")
    create.add_argument("--target", required=True, help="Repo-relative markdown path to create")
    create.add_argument("--body")
    create.add_argument("--summary")
    create.add_argument("--durable-capture", default="summary_markdown")
    create.add_argument("--overwrite", action="store_true")
    create.add_argument("--run-cli", action="store_true", help="Open the written note with Obsidian CLI")
    create.set_defaults(func=cmd_create_note)

    append = subparsers.add_parser("append-note")
    append.add_argument("--target", required=True, help="Repo-relative markdown path to append")
    append.add_argument("--body")
    append.add_argument("--summary")
    append.add_argument("--durable-capture", default="summary_markdown")
    append.add_argument("--run-cli", action="store_true", help="Open the written note with Obsidian CLI")
    append.set_defaults(func=cmd_append_note)

    emit = subparsers.add_parser("emit-event")
    emit.add_argument("--event-type", required=True)
    emit.add_argument("--summary", required=True)
    emit.add_argument("--repo-paths", nargs="*", default=[])
    emit.add_argument("--payload")
    emit.add_argument("--durable-capture", default="summary_markdown")
    emit.set_defaults(func=cmd_emit_event)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

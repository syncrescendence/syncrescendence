#!/usr/bin/env python3
"""Finalize a sandbox Cowork relay job into sandbox communications and event state."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess


REPO_ROOT = Path(__file__).resolve().parents[2]
RELAY_ROOT = REPO_ROOT / "00-ORCHESTRATION" / "relay" / "cowork-v1"
INBOX_DIR = RELAY_ROOT / "jobs" / "inbox"
RUNNING_DIR = RELAY_ROOT / "jobs" / "running"
COMPLETED_DIR = RELAY_ROOT / "jobs" / "completed"
FAILED_DIR = RELAY_ROOT / "jobs" / "failed"

BRIDGE_SCRIPTS = {
    "perplexity": "operators/cli-web-gap/perplexity_response_bridge.py",
    "oracle": "operators/cli-web-gap/oracle_response_bridge.py",
    "notebooklm": "operators/cli-web-gap/notebooklm_response_bridge.py",
    "claude_cowork": "operators/cli-web-gap/claude_cowork_response_bridge.py",
}


def load_job(job_ref: str) -> tuple[Path, dict]:
    candidates = []
    ref_path = Path(job_ref)
    if ref_path.suffix == ".json":
        candidates.extend(
            [INBOX_DIR / ref_path.name, RUNNING_DIR / ref_path.name, COMPLETED_DIR / ref_path.name, FAILED_DIR / ref_path.name]
        )
    else:
        candidates.extend(
            [
                INBOX_DIR / f"{job_ref}.json",
                RUNNING_DIR / f"{job_ref}.json",
                COMPLETED_DIR / f"{job_ref}.json",
                FAILED_DIR / f"{job_ref}.json",
            ]
        )
    for candidate in candidates:
        if candidate.exists():
            return candidate, json.loads(candidate.read_text(encoding="utf-8"))
    raise SystemExit(f"Job not found: {job_ref}")


def load_status_file(status_ref: str) -> tuple[Path, dict]:
    status_path = Path(status_ref)
    if not status_path.is_absolute():
        status_path = REPO_ROOT / status_path
    status_path = status_path.resolve()
    if not status_path.exists():
        raise SystemExit(f"Status file does not exist: {status_path}")
    if not str(status_path).startswith(str(REPO_ROOT)):
        raise SystemExit(f"Status file must stay inside sandbox root: {status_path}")
    payload = json.loads(status_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("Status file must decode to a JSON object.")
    return status_path, payload


def write_status(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job")
    parser.add_argument("--status-file", help="Sandbox-relative or absolute path to a Cowork-written status JSON.")
    parser.add_argument("--result", choices=["success", "failed"])
    parser.add_argument("--note")
    parser.add_argument("--citation-count", type=int, default=None)
    args = parser.parse_args()

    if not args.job and not args.status_file:
        raise SystemExit("Either --job or --status-file is required.")

    if args.status_file:
        _, status_payload = load_status_file(args.status_file)
        if not args.job:
            args.job = status_payload.get("job_id")
        if not args.result:
            args.result = status_payload.get("result")
        if not args.note:
            args.note = status_payload.get("note")
        if args.citation_count is None:
            parsed_count = status_payload.get("citation_count")
            if isinstance(parsed_count, int):
                args.citation_count = parsed_count

    if not args.job or not args.result or not args.note:
        raise SystemExit("Finalization requires job id, result, and note, directly or via --status-file.")

    job_path, job = load_job(args.job)
    bridge_script = BRIDGE_SCRIPTS.get(job["surface"])
    if bridge_script is None:
        raise SystemExit(f"No bridge script registered for surface: {job['surface']}")

    staging_path = REPO_ROOT / job["response_staging_path"]
    target_path = REPO_ROOT / job["response_artifact"]
    status_path = REPO_ROOT / job["status_path"]

    final_status = {
        "job_id": job["id"],
        "surface": job["surface"],
        "result": args.result,
        "note": args.note,
    }
    if args.citation_count is not None:
        final_status["citation_count"] = args.citation_count

    if args.result == "failed":
        failed_job_path = FAILED_DIR / job_path.name
        if job_path.resolve() != failed_job_path.resolve():
            shutil.move(str(job_path), str(failed_job_path))
        write_status(status_path, final_status)
        print(f"Marked failed: {failed_job_path}")
        return 0

    if not staging_path.exists():
        raise SystemExit(f"Staged response artifact missing: {staging_path}")

    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(staging_path, target_path)
    completed_job_path = COMPLETED_DIR / job_path.name
    if job_path.resolve() != completed_job_path.resolve():
        shutil.move(str(job_path), str(completed_job_path))

    command = [
        "python3",
        str(REPO_ROOT / bridge_script),
        "--dispatch",
        job["packet"],
        "--response",
        job["response_artifact"],
        "--summary",
        job["summary_for_bridge"],
    ]
    if args.citation_count is not None and job["surface"] == "perplexity":
        command.extend(["--citation-count", str(args.citation_count)])
    subprocess.run(command, check=True, cwd=REPO_ROOT)

    final_status["response_artifact"] = job["response_artifact"]
    write_status(status_path, final_status)
    print(f"Completed: {completed_job_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

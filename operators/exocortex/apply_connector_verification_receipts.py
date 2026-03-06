#!/usr/bin/env python3
"""Apply connector verification receipts to the exocortex connector manifest."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MANIFEST = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-CONNECTOR-MANIFEST-CC91.json"
DEFAULT_TRACKER = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-CONNECTOR-VERIFICATION-TRACKER-CC91.json"
DEFAULT_TRACKER_MD = REPO_ROOT / "orchestration" / "state" / "impl" / "EXOCORTEX-CONNECTOR-VERIFICATION-TRACKER-CC91.md"

OUTCOME_TO_STATE = {
    "connected": "verified_connected",
    "not_connected": "verified_not_connected",
    "partial": "verified_partial",
    "blocked": "verification_blocked",
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_receipts(payload: Any) -> tuple[str, list[dict[str, Any]]]:
    if isinstance(payload, dict):
        batch_id = str(payload.get("verification_batch_id") or "")
        rows = payload.get("receipts")
        if not isinstance(rows, list):
            raise SystemExit("Receipt payload must include a 'receipts' list.")
        return batch_id, rows
    if isinstance(payload, list):
        return "", payload
    raise SystemExit("Receipt payload must be a JSON object or list.")


def validate_receipt(row: dict[str, Any], index: int) -> None:
    required = {"connector_id", "outcome", "verified_by", "verified_at"}
    missing = sorted(required - row.keys())
    if missing:
        raise SystemExit(f"Receipt #{index} missing required fields: {missing}")
    outcome = str(row.get("outcome"))
    if outcome not in OUTCOME_TO_STATE:
        raise SystemExit(f"Receipt #{index} has invalid outcome {outcome!r}")
    evidence = row.get("evidence_refs", [])
    if not isinstance(evidence, list):
        raise SystemExit(f"Receipt #{index} field 'evidence_refs' must be a list.")
    for ref_index, ref in enumerate(evidence, start=1):
        if not isinstance(ref, dict):
            raise SystemExit(f"Receipt #{index} evidence_refs[{ref_index}] must be an object.")
        if "label" not in ref or "value" not in ref:
            raise SystemExit(f"Receipt #{index} evidence_refs[{ref_index}] must include label and value.")


def update_manifest(
    manifest: dict[str, Any],
    receipts: list[dict[str, Any]],
    *,
    batch_id: str,
    strict_unknown: bool,
    receipt_path: Path,
) -> dict[str, Any]:
    connectors = manifest.get("connectors")
    if not isinstance(connectors, list):
        raise SystemExit("Manifest has no connector list.")
    by_id = {}
    for row in connectors:
        if isinstance(row, dict):
            connector_id = row.get("id")
            if isinstance(connector_id, str):
                by_id[connector_id] = row

    unknown_connector_ids: list[str] = []
    applied = 0
    outcome_counts: Counter[str] = Counter()
    touched_sources: Counter[str] = Counter()

    for index, receipt in enumerate(receipts, start=1):
        if not isinstance(receipt, dict):
            raise SystemExit(f"Receipt #{index} must be an object.")
        validate_receipt(receipt, index)
        connector_id = str(receipt["connector_id"])
        connector = by_id.get(connector_id)
        if connector is None:
            unknown_connector_ids.append(connector_id)
            continue

        outcome = str(receipt["outcome"])
        state = OUTCOME_TO_STATE[outcome]
        connector["state"] = state
        connector["state_reason"] = str(receipt.get("notes", "")).strip()
        connector["state_updated_at"] = str(receipt["verified_at"])
        connector["state_updated_by"] = str(receipt["verified_by"])
        connector["state_updated_via"] = str(receipt.get("verification_surface", "manual_or_ui"))

        verification_record = {
            "connector_id": connector_id,
            "outcome": outcome,
            "state": state,
            "verified_by": str(receipt["verified_by"]),
            "verified_at": str(receipt["verified_at"]),
            "verification_surface": str(receipt.get("verification_surface", "manual_or_ui")),
            "evidence_refs": receipt.get("evidence_refs", []),
            "notes": str(receipt.get("notes", "")).strip(),
            "receipt_source": str(receipt_path),
            "verification_batch_id": batch_id,
            "applied_at": utc_now(),
        }
        connector["last_verification"] = verification_record
        history = connector.get("verification_history", [])
        if not isinstance(history, list):
            history = []
        history.append(verification_record)
        connector["verification_history"] = history[-20:]
        batch_ids = connector.get("verification_batch_ids", [])
        if not isinstance(batch_ids, list):
            batch_ids = []
        if batch_id and batch_id not in batch_ids:
            batch_ids.append(batch_id)
        connector["verification_batch_ids"] = sorted(batch_ids)

        source_slug = str(connector.get("source_slug", "unknown"))
        outcome_counts[outcome] += 1
        touched_sources[source_slug] += 1
        applied += 1

    if strict_unknown and unknown_connector_ids:
        raise SystemExit(f"Unknown connector IDs in receipt payload: {sorted(set(unknown_connector_ids))}")

    state_counts: Counter[str] = Counter()
    for row in connectors:
        if isinstance(row, dict):
            state_counts[str(row.get("state", "unknown"))] += 1
    verified_count = sum(count for state, count in state_counts.items() if state.startswith("verified_"))
    if verified_count == len(connectors) and connectors:
        manifest_status = "verified"
    elif verified_count > 0:
        manifest_status = "partially_verified"
    elif any(state != "user_claimed_configured_unverified" for state in state_counts):
        manifest_status = "verification_in_progress"
    else:
        manifest_status = "user_claimed_unverified"

    manifest["generated_at"] = utc_now()
    manifest["status"] = manifest_status
    counts = manifest.get("counts", {})
    if not isinstance(counts, dict):
        counts = {}
    counts["connector_count"] = len(connectors)
    counts["verified_connector_count"] = verified_count
    counts["connector_state_counts"] = dict(sorted(state_counts.items()))
    manifest["counts"] = counts
    verification = manifest.get("verification", {})
    if not isinstance(verification, dict):
        verification = {}
    verification["last_batch_id"] = batch_id
    verification["last_batch_applied_at"] = utc_now()
    verification["last_batch_receipt_path"] = str(receipt_path)
    verification["last_batch_applied_count"] = applied
    verification["last_batch_unknown_connector_ids"] = sorted(set(unknown_connector_ids))
    verification["last_batch_outcome_counts"] = dict(sorted(outcome_counts.items()))
    verification["last_batch_touched_sources"] = dict(sorted(touched_sources.items()))
    manifest["verification"] = verification
    return {
        "manifest": manifest,
        "applied_count": applied,
        "unknown_connector_ids": sorted(set(unknown_connector_ids)),
        "outcome_counts": dict(sorted(outcome_counts.items())),
        "touched_sources": dict(sorted(touched_sources.items())),
        "state_counts": dict(sorted(state_counts.items())),
        "verified_count": verified_count,
    }


def update_tracker(
    tracker_path: Path,
    *,
    batch_id: str,
    receipt_path: Path,
    update_summary: dict[str, Any],
    manifest_path: Path,
) -> dict[str, Any]:
    if tracker_path.exists():
        tracker = load_json(tracker_path)
    else:
        tracker = {
            "version": "cc91",
            "status": "active",
            "manifest_path": str(manifest_path),
            "batches": [],
        }
    batches = tracker.get("batches", [])
    if not isinstance(batches, list):
        batches = []
    batch_row = {
        "batch_id": batch_id,
        "receipt_path": str(receipt_path),
        "applied_at": utc_now(),
        "applied_count": update_summary["applied_count"],
        "unknown_connector_ids": update_summary["unknown_connector_ids"],
        "outcome_counts": update_summary["outcome_counts"],
        "touched_sources": update_summary["touched_sources"],
        "state_counts_after_apply": update_summary["state_counts"],
    }
    batches.append(batch_row)
    tracker["batches"] = batches[-50:]
    tracker["generated_at"] = utc_now()
    tracker["summary"] = {
        "batch_count": len(tracker["batches"]),
        "last_batch_id": batch_id,
        "last_applied_count": update_summary["applied_count"],
        "last_unknown_connector_count": len(update_summary["unknown_connector_ids"]),
        "verified_connector_count": update_summary["verified_count"],
        "state_counts": update_summary["state_counts"],
    }
    return tracker


def render_tracker_markdown(tracker: dict[str, Any]) -> str:
    summary = tracker.get("summary", {})
    lines = [
        "# Exocortex Connector Verification Tracker — CC91",
        "",
        f"- Generated: `{tracker.get('generated_at')}`",
        f"- Last batch: `{summary.get('last_batch_id', '')}`",
        f"- Verified connector count: `{summary.get('verified_connector_count', 0)}`",
        "",
        "## Last State Counts",
        "",
    ]
    state_counts = summary.get("state_counts", {})
    if isinstance(state_counts, dict):
        for key, value in sorted(state_counts.items()):
            lines.append(f"- `{key}`: `{value}`")
    else:
        lines.append("- none")
    lines.extend(["", "## Recent Batches", ""])
    batches = tracker.get("batches", [])
    if isinstance(batches, list) and batches:
        for row in batches[-5:][::-1]:
            lines.extend(
                [
                    f"### {row.get('batch_id', '')}",
                    f"- Applied: `{row.get('applied_at', '')}`",
                    f"- Applied count: `{row.get('applied_count', 0)}`",
                    f"- Unknown connector IDs: `{len(row.get('unknown_connector_ids', []))}`",
                    f"- Receipt: `{row.get('receipt_path', '')}`",
                    "",
                ]
            )
    else:
        lines.append("- no batches applied yet")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipts", required=True, help="Path to verification receipt JSON file.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--tracker", default=str(DEFAULT_TRACKER))
    parser.add_argument("--tracker-md", default=str(DEFAULT_TRACKER_MD))
    parser.add_argument("--batch-id", default="", help="Override batch id if receipt file does not provide one.")
    parser.add_argument("--strict-unknown", action="store_true")
    args = parser.parse_args()

    receipt_path = Path(args.receipts).expanduser().resolve()
    manifest_path = Path(args.manifest).expanduser().resolve()
    tracker_path = Path(args.tracker).expanduser().resolve()
    tracker_md_path = Path(args.tracker_md).expanduser().resolve()

    payload = json.loads(receipt_path.read_text(encoding="utf-8"))
    inferred_batch_id, receipts = normalize_receipts(payload)
    batch_id = args.batch_id or inferred_batch_id or f"batch-{utc_now().replace(':', '').replace('-', '')}"

    manifest = load_json(manifest_path)
    update = update_manifest(
        manifest,
        receipts,
        batch_id=batch_id,
        strict_unknown=args.strict_unknown,
        receipt_path=receipt_path,
    )
    manifest_path.write_text(json.dumps(update["manifest"], indent=2, sort_keys=True) + "\n", encoding="utf-8")

    tracker = update_tracker(
        tracker_path,
        batch_id=batch_id,
        receipt_path=receipt_path,
        update_summary=update,
        manifest_path=manifest_path,
    )
    tracker_path.parent.mkdir(parents=True, exist_ok=True)
    tracker_path.write_text(json.dumps(tracker, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tracker_md_path.parent.mkdir(parents=True, exist_ok=True)
    tracker_md_path.write_text(render_tracker_markdown(tracker), encoding="utf-8")

    print(manifest_path)
    print(tracker_path)
    print(tracker_md_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

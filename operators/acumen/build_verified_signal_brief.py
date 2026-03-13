#!/usr/bin/env python3
"""Build a derivative Verified Signal Brief from assessments and queue state."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from .evidence_family import REPO_ROOT, repo_rel
except ImportError:
    OPS_DIR = Path(__file__).resolve().parents[1]
    if str(OPS_DIR) not in sys.path:
        sys.path.insert(0, str(OPS_DIR))
    from evidence_family import REPO_ROOT, repo_rel  # type: ignore[no-redef]


ASSESSMENT_SCHEMA_VERSION = "acumen.augur.return.assessment/v1"
DEFAULT_ASSESSMENT_JSON_DIR = REPO_ROOT / "runtime" / "acumen" / "out" / "augur-return-assessments"
DEFAULT_QUEUE_JSON = REPO_ROOT / "orchestration" / "state" / "ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json"


def utc_day() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def utc_stamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assessment-json-dir", default=str(DEFAULT_ASSESSMENT_JSON_DIR))
    parser.add_argument("--queue-json", default=str(DEFAULT_QUEUE_JSON))
    parser.add_argument("--output", required=True)
    parser.add_argument("--date", default=utc_day())
    return parser.parse_args()


def load_json_object(path: Path, *, label: str) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"{label} at {repo_rel(path)} must be a JSON object")
    return payload


def load_assessments(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if not path.exists():
        raise SystemExit(f"assessment directory missing: {repo_rel(path)}")
    for candidate in sorted(path.glob("*.json")):
        payload = load_json_object(candidate, label="assessment")
        if payload.get("schema_version") != ASSESSMENT_SCHEMA_VERSION:
            continue
        rows.append(payload)
    return rows


def assessment_sort_key(item: dict[str, Any]) -> tuple[int, str, str]:
    status = str(item.get("assessment", {}).get("response_status", ""))
    status_order = {
        "assessed": 0,
        "invalid_return_structure": 1,
        "awaiting_augur_response": 2,
    }
    bridge_item = item.get("bridge_item", {})
    title = str(bridge_item.get("title", ""))
    video_id = str(bridge_item.get("video_id", ""))
    return (status_order.get(status, 3), title.lower(), video_id.lower())


def render_item_block(assessment: dict[str, Any]) -> list[str]:
    bridge_item = assessment.get("bridge_item", {})
    result = assessment.get("assessment", {})
    paths = assessment.get("paths", {})
    title = str(bridge_item.get("title", "Untitled"))
    lines = [
        f"### {title}",
        f"- Video ID: `{bridge_item.get('video_id', 'unknown')}`",
        f"- Triage event: `{bridge_item.get('triage_event_id', 'unknown')}`",
        f"- Decision: `{bridge_item.get('decision', 'unknown')}`",
        f"- Assessment: `{paths.get('assessment_md_path', 'unknown')}`",
        f"- Queue decision: `{result.get('queue_decision', 'unknown')}`",
        f"- Queue rationale: {result.get('queue_rationale', 'n/a')}",
        "",
        "#### Verified Fact Candidates",
    ]

    verified = result.get("verified_fact_candidates", [])
    if isinstance(verified, list) and verified:
        lines.extend(f"- {item}" for item in verified)
    else:
        lines.append("- none extracted")

    lines.extend(["", "#### Inference And Open Readings"])
    inference_points = result.get("inference_points", [])
    if isinstance(inference_points, list) and inference_points:
        lines.extend(f"- {item}" for item in inference_points)
    else:
        lines.append("- none extracted")

    disconfirming = result.get("disconfirming_or_complicating_points", [])
    lines.extend(["", "#### Disconfirming Or Complicating Evidence"])
    if isinstance(disconfirming, list) and disconfirming:
        lines.extend(f"- {item}" for item in disconfirming)
    else:
        lines.append("- none extracted")

    gaps = result.get("confidence_and_gaps", [])
    lines.extend(["", "#### Remaining Gaps"])
    if isinstance(gaps, list) and gaps:
        lines.extend(f"- {item}" for item in gaps)
    else:
        lines.append(f"- {result.get('manual_boundary', 'no additional gaps recorded')}")

    next_sources = result.get("next_source_recommendations", [])
    lines.extend(["", "#### Next-Source Recommendations"])
    if isinstance(next_sources, list) and next_sources:
        lines.extend(f"- {item}" for item in next_sources)
    else:
        lines.append("- none extracted")

    lines.append("")
    return lines


def render_queue_entries(entries: list[dict[str, Any]], *, heading: str, empty_line: str) -> list[str]:
    lines = [heading, ""]
    if not entries:
        lines.append(empty_line)
        lines.append("")
        return lines
    for entry in entries:
        lines.extend(
            [
                f"- **{entry.get('title', 'Untitled')}** (`{entry.get('video_id', 'unknown')}`)",
                f"  - Assessment: `{entry.get('assessment_md_path', 'unknown')}`",
                f"  - Rationale: {entry.get('rationale', 'n/a')}",
            ]
        )
        if entry.get("augur_response_path"):
            lines.append(f"  - Response path: `{entry['augur_response_path']}`")
        if entry.get("recommended_sources"):
            lines.append(f"  - Recommended sources: `{len(entry['recommended_sources'])}`")
    lines.append("")
    return lines


def render_brief(
    *,
    assessments: list[dict[str, Any]],
    queue: dict[str, Any],
    assessment_dir: Path,
    queue_path: Path,
    date: str,
) -> str:
    assessed_items = [
        item
        for item in sorted(assessments, key=assessment_sort_key)
        if item.get("assessment", {}).get("response_status") == "assessed"
    ]
    queue_counts = queue.get("counts", {})
    pending = queue.get("pending_returns", [])
    holds = queue.get("holds", [])
    queued = queue.get("queue", [])
    lines = [
        f"# Verified Signal Brief | {date}",
        "",
        f"- Generated at: `{utc_stamp()}`",
        f"- Assessment source: `{repo_rel(assessment_dir)}`",
        f"- Queue source: `{repo_rel(queue_path)}`",
        f"- Assessed items: `{len(assessed_items)}`",
        f"- Pending returns: `{queue_counts.get('pending_returns', len(pending))}`",
        f"- Held returns: `{queue_counts.get('held', len(holds))}`",
        f"- Primary-source escalations: `{queue_counts.get('queued_for_primary', len(queued))}`",
        "",
        "## Verified Signals",
        "",
    ]

    if assessed_items:
        for assessment in assessed_items:
            lines.extend(render_item_block(assessment))
    else:
        lines.append("- none yet; no landed Augur return currently satisfies assessed verified-signal state.")
        lines.append("")

    lines.extend(
        render_queue_entries(
            list(queued) if isinstance(queued, list) else [],
            heading="## Primary-Source Escalations",
            empty_line="- none queued for primary review yet.",
        )
    )
    lines.extend(
        render_queue_entries(
            list(pending) if isinstance(pending, list) else [],
            heading="## Pending Returns",
            empty_line="- none awaiting response.",
        )
    )
    lines.extend(
        render_queue_entries(
            list(holds) if isinstance(holds, list) else [],
            heading="## Held Returns",
            empty_line="- none held.",
        )
    )
    lines.extend(
        [
            "## Derivative Boundary",
            "",
            "- This brief derives only from repo-side assessment artifacts and the primary-source queue.",
            "- It does not read Augur responses as authority and does not bypass queue admission.",
            f"- Current manual boundary: {queue.get('manual_boundary', 'n/a')}",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    assessment_dir = Path(args.assessment_json_dir).expanduser().resolve()
    queue_path = Path(args.queue_json).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    assessments = load_assessments(assessment_dir)
    queue = load_json_object(queue_path, label="queue")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_brief(
            assessments=assessments,
            queue=queue,
            assessment_dir=assessment_dir,
            queue_path=queue_path,
            date=args.date,
        ).rstrip()
        + "\n",
        encoding="utf-8",
    )
    print(repo_rel(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

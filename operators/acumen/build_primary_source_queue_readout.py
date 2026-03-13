#!/usr/bin/env python3
"""Build a derivative primary-source queue readout from queue and assessment state."""

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


DEFAULT_QUEUE_JSON = REPO_ROOT / "orchestration" / "state" / "ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json"
DEFAULT_ASSESSMENT_JSON_DIR = REPO_ROOT / "runtime" / "acumen" / "out" / "augur-return-assessments"


def utc_day() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def utc_stamp() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue-json", default=str(DEFAULT_QUEUE_JSON))
    parser.add_argument("--assessment-json-dir", default=str(DEFAULT_ASSESSMENT_JSON_DIR))
    parser.add_argument("--output", required=True)
    parser.add_argument("--date", default=utc_day())
    return parser.parse_args()


def load_json_object(path: Path, *, label: str) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"{label} at {repo_rel(path)} must be a JSON object")
    return payload


def load_assessment_index(directory: Path) -> dict[str, dict[str, Any]]:
    if not directory.exists():
        raise SystemExit(f"assessment directory missing: {repo_rel(directory)}")
    index: dict[str, dict[str, Any]] = {}
    for candidate in sorted(directory.glob("*.json")):
        payload = load_json_object(candidate, label="assessment")
        bridge_item = payload.get("bridge_item", {})
        video_id = str(bridge_item.get("video_id", "")).strip()
        if video_id:
            index[video_id] = payload
    return index


def render_queue_entry(entry: dict[str, Any], assessment: dict[str, Any] | None) -> list[str]:
    lines = [
        f"### {entry.get('title', 'Untitled')}",
        f"- Video ID: `{entry.get('video_id', 'unknown')}`",
        f"- Triage event: `{entry.get('triage_event_id', 'unknown')}`",
        f"- Decision: `{entry.get('decision', 'unknown')}`",
        f"- Assessment: `{entry.get('assessment_md_path', 'unknown')}`",
        f"- Queue rationale: {entry.get('rationale', 'n/a')}",
    ]
    recommended = entry.get("recommended_sources", [])
    lines.extend(["", "#### Recommended Sources"])
    if isinstance(recommended, list) and recommended:
        lines.extend(f"- {item}" for item in recommended)
    else:
        lines.append("- none recorded")

    verified = entry.get("verified_fact_candidates", [])
    lines.extend(["", "#### Verified Fact Candidates"])
    if isinstance(verified, list) and verified:
        lines.extend(f"- {item}" for item in verified)
    else:
        lines.append("- none recorded")

    gaps = []
    if assessment is not None:
        result = assessment.get("assessment", {})
        loaded_gaps = result.get("confidence_and_gaps", [])
        if isinstance(loaded_gaps, list):
            gaps = loaded_gaps
        if not gaps and result.get("manual_boundary"):
            gaps = [str(result["manual_boundary"])]
    lines.extend(["", "#### Confidence And Gaps"])
    if gaps:
        lines.extend(f"- {item}" for item in gaps)
    else:
        lines.append("- none recorded")
    lines.append("")
    return lines


def render_pending_entry(entry: dict[str, Any], assessment: dict[str, Any] | None) -> list[str]:
    manual_boundary = None
    if assessment is not None:
        manual_boundary = assessment.get("assessment", {}).get("manual_boundary")
    lines = [
        f"- **{entry.get('title', 'Untitled')}** (`{entry.get('video_id', 'unknown')}`)",
        f"  - Waiting on response: `{entry.get('augur_response_path', 'unknown')}`",
        f"  - Assessment: `{entry.get('assessment_md_path', 'unknown')}`",
        f"  - Rationale: {entry.get('rationale', 'n/a')}",
    ]
    if manual_boundary:
        lines.append(f"  - Manual boundary: {manual_boundary}")
    return lines


def render_hold_entry(entry: dict[str, Any], assessment: dict[str, Any] | None) -> list[str]:
    missing_sections: list[str] = []
    if assessment is not None:
        raw_missing = assessment.get("response", {}).get("missing_sections", [])
        if isinstance(raw_missing, list):
            missing_sections = [str(item) for item in raw_missing]
    lines = [
        f"- **{entry.get('title', 'Untitled')}** (`{entry.get('video_id', 'unknown')}`)",
        f"  - Assessment: `{entry.get('assessment_md_path', 'unknown')}`",
        f"  - Rationale: {entry.get('rationale', 'n/a')}",
    ]
    if missing_sections:
        lines.append(f"  - Missing return sections: {', '.join(missing_sections)}")
    return lines


def render_readout(
    *,
    queue: dict[str, Any],
    queue_path: Path,
    assessment_dir: Path,
    assessment_index: dict[str, dict[str, Any]],
    date: str,
) -> str:
    counts = queue.get("counts", {})
    queued = queue.get("queue", [])
    pending = queue.get("pending_returns", [])
    holds = queue.get("holds", [])
    lines = [
        f"# Primary-Source Queue Readout | {date}",
        "",
        f"- Generated at: `{utc_stamp()}`",
        f"- Queue source: `{repo_rel(queue_path)}`",
        f"- Assessment source: `{repo_rel(assessment_dir)}`",
        f"- Items tracked: `{counts.get('items_tracked', 0)}`",
        f"- Ready for primary review: `{counts.get('queued_for_primary', len(queued) if isinstance(queued, list) else 0)}`",
        f"- Pending returns: `{counts.get('pending_returns', len(pending) if isinstance(pending, list) else 0)}`",
        f"- Held: `{counts.get('held', len(holds) if isinstance(holds, list) else 0)}`",
        "",
        "## Ready For Primary Review",
        "",
    ]

    if isinstance(queued, list) and queued:
        for entry in queued:
            video_id = str(entry.get("video_id", ""))
            lines.extend(render_queue_entry(entry, assessment_index.get(video_id)))
    else:
        lines.append("- none queued for primary review yet.")
        lines.append("")

    lines.extend(["## Pending Returns", ""])
    if isinstance(pending, list) and pending:
        for entry in pending:
            video_id = str(entry.get("video_id", ""))
            lines.extend(render_pending_entry(entry, assessment_index.get(video_id)))
    else:
        lines.append("- none awaiting response.")
    lines.append("")

    lines.extend(["## Holds", ""])
    if isinstance(holds, list) and holds:
        for entry in holds:
            video_id = str(entry.get("video_id", ""))
            lines.extend(render_hold_entry(entry, assessment_index.get(video_id)))
    else:
        lines.append("- none held.")
    lines.append("")

    lines.extend(
        [
            "## Derivative Boundary",
            "",
            "- This readout renders the authoritative queue state and linked repo-side assessments only.",
            "- It does not decide queue admission, doctrine, or response validity on its own.",
            f"- Current manual boundary: {queue.get('manual_boundary', 'n/a')}",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    queue_path = Path(args.queue_json).expanduser().resolve()
    assessment_dir = Path(args.assessment_json_dir).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    queue = load_json_object(queue_path, label="queue")
    assessment_index = load_assessment_index(assessment_dir)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_readout(
            queue=queue,
            queue_path=queue_path,
            assessment_dir=assessment_dir,
            assessment_index=assessment_index,
            date=args.date,
        ).rstrip()
        + "\n",
        encoding="utf-8",
    )
    print(repo_rel(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Ingest landed Augur responses into repo-side assessments and a primary-source queue."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from .evidence_family import (
        REPO_ROOT,
        repo_rel,
        scan_forbidden_content,
        sha256_for_file,
        utc_now,
    )
except ImportError:
    OPS_DIR = Path(__file__).resolve().parents[1]
    if str(OPS_DIR) not in sys.path:
        sys.path.insert(0, str(OPS_DIR))
    from evidence_family import (  # type: ignore[no-redef]
        REPO_ROOT,
        repo_rel,
        scan_forbidden_content,
        sha256_for_file,
        utc_now,
    )


SUPPORTED_BRIDGE_SCHEMA_VERSIONS = {
    "acumen.verification.bridge/v1",
    "acumen.verification.bridge/v2",
}
ASSESSMENT_SCHEMA_VERSION = "acumen.augur.return.assessment/v1"
QUEUE_SCHEMA_VERSION = "acumen.primary_source.queue/v1"

DEFAULT_BRIDGE_JSON = REPO_ROOT / "orchestration" / "state" / "ACUMEN-AUGUR-VERIFICATION-BRIDGE.json"
DEFAULT_ASSESSMENT_JSON_DIR = REPO_ROOT / "runtime" / "acumen" / "out" / "augur-return-assessments"
DEFAULT_ASSESSMENT_MD_DIR = REPO_ROOT / "communications" / "assessments"
DEFAULT_QUEUE_JSON = REPO_ROOT / "orchestration" / "state" / "ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json"
DEFAULT_QUEUE_MD = REPO_ROOT / "orchestration" / "state" / "ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.md"

REQUIRED_SECTIONS = [
    "Source Terrain",
    "Current-Reality Checks",
    "Disconfirming Or Complicating Evidence",
    "Sources To Read Next",
    "Confidence And Gaps",
]
SECTION_MAP = {section.lower(): section for section in REQUIRED_SECTIONS}
URL_RE = re.compile(r"https?://\S+")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
BULLET_RE = re.compile(r"^[-*]\s+(.*)$")
NUMBERED_RE = re.compile(r"^\d+\.\s+(.*)$")
INFERENCE_MARKERS = (
    "inference:",
    "[inference]",
    " likely ",
    " suggests ",
    " appears ",
    " may ",
    " might ",
    " could ",
    " uncertain",
    " ambiguity",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bridge-json", default=str(DEFAULT_BRIDGE_JSON))
    parser.add_argument("--assessment-json-dir", default=str(DEFAULT_ASSESSMENT_JSON_DIR))
    parser.add_argument("--assessment-md-dir", default=str(DEFAULT_ASSESSMENT_MD_DIR))
    parser.add_argument("--queue-json", default=str(DEFAULT_QUEUE_JSON))
    parser.add_argument("--queue-md", default=str(DEFAULT_QUEUE_MD))
    parser.add_argument("--video-id", action="append", dest="video_ids", default=[])
    parser.add_argument("--triage-event-id", action="append", dest="triage_event_ids", default=[])
    return parser.parse_args()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def normalize_space(value: str) -> str:
    return " ".join(value.split())


def resolve_repo_path(raw_value: str | None) -> Path | None:
    if raw_value is None or not str(raw_value).strip():
        return None
    candidate = Path(str(raw_value)).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()
    return (REPO_ROOT / candidate).resolve()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + "\n", encoding="utf-8")


def load_json_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit(f"{repo_rel(path)} must be a JSON object")
    return payload


def normalize_heading(raw_heading: str) -> str | None:
    key = normalize_space(re.sub(r"[*_`#]", "", raw_heading).strip()).lower()
    return SECTION_MAP.get(key)


def extract_items(lines: list[str]) -> list[str]:
    items: list[str] = []
    paragraph: list[str] = []
    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped:
            if paragraph:
                items.append(normalize_space(" ".join(paragraph)))
                paragraph = []
            continue
        bullet_match = BULLET_RE.match(stripped)
        numbered_match = NUMBERED_RE.match(stripped)
        if bullet_match or numbered_match:
            if paragraph:
                items.append(normalize_space(" ".join(paragraph)))
                paragraph = []
            matched = bullet_match.group(1) if bullet_match else numbered_match.group(1)
            items.append(normalize_space(matched))
            continue
        paragraph.append(stripped)
    if paragraph:
        items.append(normalize_space(" ".join(paragraph)))
    return [item for item in items if item]


def parse_response_sections(body: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current_section: str | None = None
    for raw_line in body.splitlines():
        if raw_line.startswith("## "):
            current_section = normalize_heading(raw_line.removeprefix("## ").strip())
            if current_section is not None:
                sections.setdefault(current_section, [])
            continue
        if current_section is not None:
            sections[current_section].append(raw_line)
    return {name: extract_items(lines) for name, lines in sections.items()}


def citation_signal_count(items: list[str]) -> int:
    count = 0
    for item in items:
        count += len(URL_RE.findall(item))
        count += len(MARKDOWN_LINK_RE.findall(item))
    return count


def has_citation_signal(item: str) -> bool:
    return citation_signal_count([item]) > 0


def is_inference_item(item: str) -> bool:
    lowered = f" {item.lower()} "
    return any(marker in lowered for marker in INFERENCE_MARKERS)


def classify_sections(parsed_sections: dict[str, list[str]]) -> tuple[list[str], list[str], list[str], list[str]]:
    verified_facts: list[str] = []
    inference_points: list[str] = []
    disconfirming_points = list(parsed_sections.get("Disconfirming Or Complicating Evidence", []))
    confidence_and_gaps = list(parsed_sections.get("Confidence And Gaps", []))

    for section_name in (
        "Source Terrain",
        "Current-Reality Checks",
        "Disconfirming Or Complicating Evidence",
    ):
        for item in parsed_sections.get(section_name, []):
            if has_citation_signal(item) and not is_inference_item(item):
                verified_facts.append(item)
            else:
                inference_points.append(item)

    for item in confidence_and_gaps:
        if item not in inference_points:
            inference_points.append(item)

    return verified_facts, inference_points, disconfirming_points, confidence_and_gaps


def assessment_paths_for(
    item: dict[str, Any],
    *,
    assessment_json_dir: Path,
    assessment_md_dir: Path,
) -> tuple[str, Path, Path]:
    seed = (
        str(item.get("video_id") or "")
        or str(item.get("triage_event_id") or "")
        or str(item.get("title") or "")
        or "augur-return"
    )
    slug = slugify(seed) or "augur-return"
    json_path = assessment_json_dir / f"{slug}.json"
    md_path = assessment_md_dir / f"ACUMEN-AUGUR-RETURN-ASSESSMENT-{slug}.md"
    return slug, json_path, md_path


def queue_decision_for(
    *,
    response_exists: bool,
    response_valid: bool,
    decision: str,
    next_sources: list[str],
) -> tuple[str, str]:
    if not response_exists:
        return "awaiting_response", "The declared Augur response path has not landed yet."
    if not response_valid:
        return "hold", "The Augur response landed, but it did not satisfy the required return structure."
    if decision == "Flag-for-Primary":
        return "escalate_to_primary", "Acumen already marked the item for primary review and the landed return is now assessed."
    if next_sources:
        return "escalate_to_primary", "The assessed Augur return surfaced reusable next-source recommendations for primary review."
    return "hold", "The assessed response did not surface reusable next-source recommendations for primary review."


def render_assessment_markdown(assessment: dict[str, Any]) -> str:
    item = assessment["bridge_item"]
    paths = assessment["paths"]
    result = assessment["assessment"]
    lines = [
        f"# Acumen Augur Return Assessment — {item['title']}",
        "",
        f"- Generated: `{assessment['generated_at']}`",
        f"- Response status: `{result['response_status']}`",
        f"- Queue decision: `{result['queue_decision']}`",
        f"- Source dossier: `{paths['dossier_path']}`",
        f"- Augur packet: `{paths['augur_packet_path']}`",
        f"- Augur response: `{paths['augur_response_path']}`",
        f"- Assessment JSON: `{paths['assessment_json_path']}`",
        f"- Queue surface: `{paths['queue_json_path']}`",
        f"- Repo sovereignty: `{assessment['repo_sovereignty']['witness_rule']}`",
        "",
        "## Verified Fact Candidates",
        "",
    ]
    verified_facts = result["verified_fact_candidates"]
    if verified_facts:
        lines.extend(f"- {item}" for item in verified_facts)
    else:
        lines.append("- none extracted")

    lines.extend(["", "## Inference And Open Readings", ""])
    inference_points = result["inference_points"]
    if inference_points:
        lines.extend(f"- {item}" for item in inference_points)
    else:
        lines.append("- none extracted")

    lines.extend(["", "## Next-Source Recommendations", ""])
    next_sources = result["next_source_recommendations"]
    if next_sources:
        lines.extend(f"- {item}" for item in next_sources)
    else:
        lines.append("- none extracted")

    lines.extend(["", "## Queue Decision", ""])
    lines.append(f"- Rationale: {result['queue_rationale']}")

    disconfirming_points = result["disconfirming_or_complicating_points"]
    if disconfirming_points:
        lines.extend(["", "## Disconfirming Or Complicating Evidence", ""])
        lines.extend(f"- {item}" for item in disconfirming_points)

    confidence_and_gaps = result["confidence_and_gaps"]
    if confidence_and_gaps:
        lines.extend(["", "## Confidence And Gaps", ""])
        lines.extend(f"- {item}" for item in confidence_and_gaps)

    lines.extend(["", "## Manual Boundary", ""])
    lines.append(f"- {result['manual_boundary']}")
    lines.append("")
    return "\n".join(lines)


def render_queue_markdown(queue: dict[str, Any]) -> str:
    lines = [
        "# Acumen Augur Primary-Source Queue",
        "",
        f"- Generated: `{queue['generated_at']}`",
        f"- Bridge source: `{queue['bridge_json_path']}`",
        f"- Items tracked: `{queue['counts']['items_tracked']}`",
        f"- Pending returns: `{queue['counts']['pending_returns']}`",
        f"- Queued for primary: `{queue['counts']['queued_for_primary']}`",
        f"- Held: `{queue['counts']['held']}`",
        "",
        "## Pending Returns",
        "",
    ]
    pending = queue["pending_returns"]
    if pending:
        for item in pending:
            lines.append(
                f"- `{item['video_id']}` -> awaiting `{item['augur_response_path']}` "
                f"(assessment: `{item['assessment_md_path']}`)"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Queue", ""])
    queued = queue["queue"]
    if queued:
        for item in queued:
            lines.append(
                f"- `{item['video_id']}` -> queued with `{len(item['recommended_sources'])}` next-source recommendations "
                f"(assessment: `{item['assessment_md_path']}`)"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Holds", ""])
    holds = queue["holds"]
    if holds:
        for item in holds:
            lines.append(
                f"- `{item['video_id']}` -> hold: {item['rationale']} "
                f"(assessment: `{item['assessment_md_path']}`)"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Manual Boundary", ""])
    lines.append(f"- {queue['manual_boundary']}")
    lines.append("")
    return "\n".join(lines)


def matches_filters(item: dict[str, Any], *, video_ids: set[str], triage_event_ids: set[str]) -> bool:
    if video_ids and str(item.get("video_id", "")) not in video_ids:
        return False
    if triage_event_ids and str(item.get("triage_event_id", "")) not in triage_event_ids:
        return False
    return True


def main() -> int:
    args = parse_args()
    bridge_path = Path(args.bridge_json).expanduser().resolve()
    assessment_json_dir = Path(args.assessment_json_dir).expanduser().resolve()
    assessment_md_dir = Path(args.assessment_md_dir).expanduser().resolve()
    queue_json_path = Path(args.queue_json).expanduser().resolve()
    queue_md_path = Path(args.queue_md).expanduser().resolve()

    bridge = load_json_object(bridge_path)
    if bridge.get("schema_version") not in SUPPORTED_BRIDGE_SCHEMA_VERSIONS:
        expected = ", ".join(sorted(SUPPORTED_BRIDGE_SCHEMA_VERSIONS))
        raise SystemExit(f"{repo_rel(bridge_path)} must use one of: {expected}")

    items = bridge.get("items")
    if not isinstance(items, list):
        raise SystemExit(f"{repo_rel(bridge_path)}: items must be a list")

    assessment_json_dir.mkdir(parents=True, exist_ok=True)
    assessment_md_dir.mkdir(parents=True, exist_ok=True)

    pending_returns: list[dict[str, Any]] = []
    queued_items: list[dict[str, Any]] = []
    held_items: list[dict[str, Any]] = []
    written_paths: list[Path] = []

    for raw_item in items:
        if not isinstance(raw_item, dict):
            continue
        if not matches_filters(
            raw_item,
            video_ids=set(args.video_ids),
            triage_event_ids=set(args.triage_event_ids),
        ):
            continue

        slug, assessment_json_path, assessment_md_path = assessment_paths_for(
            raw_item,
            assessment_json_dir=assessment_json_dir,
            assessment_md_dir=assessment_md_dir,
        )
        response_path = resolve_repo_path(raw_item.get("augur_response_path"))
        packet_path = resolve_repo_path(raw_item.get("augur_packet_path"))
        dossier_path = resolve_repo_path(raw_item.get("dossier_path"))

        response_exists = bool(response_path and response_path.exists())
        response_format = "missing"
        response_sha256: str | None = None
        parsed_sections: dict[str, list[str]] = {}
        missing_sections = list(REQUIRED_SECTIONS)
        verified_facts: list[str] = []
        inference_points: list[str] = []
        disconfirming_points: list[str] = []
        confidence_and_gaps: list[str] = []
        next_sources: list[str] = []
        citation_count = 0

        if response_exists and response_path is not None:
            response_format = "markdown" if response_path.suffix.lower() == ".md" else response_path.suffix.lower().lstrip(".")
            response_sha256 = sha256_for_file(response_path)
            if response_format == "markdown":
                response_body = response_path.read_text(encoding="utf-8")
                parsed_sections = parse_response_sections(response_body)
                missing_sections = [section for section in REQUIRED_SECTIONS if section not in parsed_sections]
                verified_facts, inference_points, disconfirming_points, confidence_and_gaps = classify_sections(parsed_sections)
                next_sources = list(parsed_sections.get("Sources To Read Next", []))
                citation_count = citation_signal_count(
                    [item for section_items in parsed_sections.values() for item in section_items]
                )

        response_valid = response_exists and response_format == "markdown" and not missing_sections
        queue_decision, queue_rationale = queue_decision_for(
            response_exists=response_exists,
            response_valid=response_valid,
            decision=str(raw_item.get("decision", "")),
            next_sources=next_sources,
        )

        if not response_exists:
            response_status = "awaiting_augur_response"
            manual_boundary = "A cited Augur response still has to be landed in the declared response path before content-bearing assessment can occur."
        elif not response_valid:
            response_status = "invalid_return_structure"
            manual_boundary = "The response exists, but it must satisfy the required return structure before lawful escalation can rely on it."
        else:
            response_status = "assessed"
            manual_boundary = "Human or later primary-source review still decides doctrine. This assessment only classifies the witness response."

        assessment = {
            "schema_version": ASSESSMENT_SCHEMA_VERSION,
            "generated_at": utc_now(),
            "assessment_id": f"acumen-augur-return-assessment-{slug}",
            "bridge_item": {
                "triage_event_id": raw_item.get("triage_event_id"),
                "model_call_event_id": raw_item.get("model_call_event_id"),
                "decision": raw_item.get("decision"),
                "title": raw_item.get("title"),
                "video_id": raw_item.get("video_id"),
            },
            "repo_sovereignty": {
                "witness_rule": "Augur remains a cited witness surface, not constitutional authority.",
                "assessment_rule": "Repo-side assessment classifies the landed witness artifact without converting it into doctrine.",
                "queue_rule": "Primary-source queue admission is a routing decision only.",
            },
            "paths": {
                "bridge_json_path": repo_rel(bridge_path),
                "dossier_path": repo_rel(dossier_path) if dossier_path is not None and dossier_path.exists() else raw_item.get("dossier_path"),
                "augur_packet_path": repo_rel(packet_path) if packet_path is not None and packet_path.exists() else raw_item.get("augur_packet_path"),
                "augur_response_path": repo_rel(response_path) if response_path is not None and response_path.exists() else raw_item.get("augur_response_path"),
                "assessment_json_path": repo_rel(assessment_json_path),
                "assessment_md_path": repo_rel(assessment_md_path),
                "queue_json_path": repo_rel(queue_json_path),
            },
            "response": {
                "exists": response_exists,
                "format": response_format,
                "sha256": response_sha256,
                "required_sections": REQUIRED_SECTIONS,
                "present_sections": sorted(parsed_sections.keys()),
                "missing_sections": missing_sections,
                "citation_signal_count": citation_count,
                "parsed_sections": parsed_sections,
            },
            "assessment": {
                "response_status": response_status,
                "verified_fact_candidates": verified_facts,
                "inference_points": inference_points,
                "next_source_recommendations": next_sources,
                "disconfirming_or_complicating_points": disconfirming_points,
                "confidence_and_gaps": confidence_and_gaps,
                "queue_decision": queue_decision,
                "queue_rationale": queue_rationale,
                "manual_boundary": manual_boundary,
            },
        }
        findings = scan_forbidden_content(assessment, scope="assessment")
        if findings:
            raise SystemExit("\n".join(findings))

        write_json(assessment_json_path, assessment)
        write_text(assessment_md_path, render_assessment_markdown(assessment))
        written_paths.extend([assessment_json_path, assessment_md_path])

        queue_entry = {
            "video_id": raw_item.get("video_id"),
            "triage_event_id": raw_item.get("triage_event_id"),
            "decision": raw_item.get("decision"),
            "title": raw_item.get("title"),
            "augur_response_path": assessment["paths"]["augur_response_path"],
            "assessment_json_path": assessment["paths"]["assessment_json_path"],
            "assessment_md_path": assessment["paths"]["assessment_md_path"],
            "rationale": queue_rationale,
        }

        if queue_decision == "awaiting_response":
            pending_returns.append(queue_entry)
        elif queue_decision == "escalate_to_primary":
            queue_entry["recommended_sources"] = next_sources
            queue_entry["verified_fact_candidates"] = verified_facts
            queued_items.append(queue_entry)
        else:
            held_items.append(queue_entry)

    queue = {
        "schema_version": QUEUE_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "bridge_json_path": repo_rel(bridge_path),
        "assessment_json_dir": repo_rel(assessment_json_dir),
        "assessment_md_dir": repo_rel(assessment_md_dir),
        "queue_json_path": repo_rel(queue_json_path),
        "queue_md_path": repo_rel(queue_md_path),
        "counts": {
            "items_tracked": len(pending_returns) + len(queued_items) + len(held_items),
            "pending_returns": len(pending_returns),
            "queued_for_primary": len(queued_items),
            "held": len(held_items),
        },
        "pending_returns": pending_returns,
        "queue": queued_items,
        "holds": held_items,
        "manual_boundary": "Augur or the human relay must still land the cited response markdown before repo-side assessment can extract facts, inferences, and next-source recommendations.",
    }
    findings = scan_forbidden_content(queue, scope="queue")
    if findings:
        raise SystemExit("\n".join(findings))

    write_json(queue_json_path, queue)
    write_text(queue_md_path, render_queue_markdown(queue))
    written_paths.extend([queue_json_path, queue_md_path])

    for path in written_paths:
        print(repo_rel(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

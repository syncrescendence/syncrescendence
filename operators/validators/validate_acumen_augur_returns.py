#!/usr/bin/env python3
"""Validate the Acumen Augur return assessment and primary-source queue family."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from operators.acumen.evidence_family import repo_rel, scan_forbidden_content


SUPPORTED_BRIDGE_SCHEMA_VERSIONS = {
    "acumen.verification.bridge/v1",
    "acumen.verification.bridge/v2",
}
ASSESSMENT_SCHEMA_VERSION = "acumen.augur.return.assessment/v1"
QUEUE_SCHEMA_VERSION = "acumen.primary_source.queue/v1"

DEFAULT_BRIDGE_JSON = REPO_ROOT / "orchestration" / "state" / "ACUMEN-AUGUR-VERIFICATION-BRIDGE.json"
DEFAULT_ASSESSMENT_JSON_DIR = REPO_ROOT / "runtime" / "acumen" / "out" / "augur-return-assessments"
DEFAULT_QUEUE_JSON = REPO_ROOT / "orchestration" / "state" / "ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json"
DEFAULT_REPORT_MD = REPO_ROOT / "orchestration" / "state" / "ACUMEN-AUGUR-RETURN-REPORT.md"
DEFAULT_REPORT_JSON = REPO_ROOT / "orchestration" / "state" / "ACUMEN-AUGUR-RETURN-REPORT.json"

REQUIRED_SECTIONS = [
    "Source Terrain",
    "Current-Reality Checks",
    "Disconfirming Or Complicating Evidence",
    "Sources To Read Next",
    "Confidence And Gaps",
]
SECTION_MAP = {section.lower(): section for section in REQUIRED_SECTIONS}


@dataclass(frozen=True)
class Finding:
    level: str
    scope: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bridge-json", default=str(DEFAULT_BRIDGE_JSON))
    parser.add_argument("--assessment-json-dir", default=str(DEFAULT_ASSESSMENT_JSON_DIR))
    parser.add_argument("--queue-json", default=str(DEFAULT_QUEUE_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_REPORT_MD))
    parser.add_argument("--output-json", default=str(DEFAULT_REPORT_JSON))
    return parser.parse_args()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def resolve_repo_path(raw_value: str | None) -> Path | None:
    if raw_value is None or not str(raw_value).strip():
        return None
    candidate = Path(str(raw_value))
    if candidate.is_absolute():
        resolved = candidate.resolve()
    else:
        resolved = (REPO_ROOT / candidate).resolve()
    try:
        resolved.relative_to(REPO_ROOT)
    except ValueError:
        return None
    return resolved


def load_json_object(path: Path, findings: list[Finding], scope: str) -> dict[str, Any] | None:
    if not path.exists():
        findings.append(Finding("error", scope, f"missing file: {repo_rel(path)}"))
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        findings.append(Finding("error", scope, f"invalid JSON: {exc}"))
        return None
    if not isinstance(payload, dict):
        findings.append(Finding("error", scope, "must be a JSON object"))
        return None
    return payload


def normalize_heading(raw_heading: str) -> str | None:
    key = " ".join(re.sub(r"[*_`#]", "", raw_heading).strip().split()).lower()
    return SECTION_MAP.get(key)


def parse_response_sections(body: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current_section: str | None = None
    for line in body.splitlines():
        if line.startswith("## "):
            current_section = normalize_heading(line.removeprefix("## ").strip())
            if current_section is not None:
                sections.setdefault(current_section, [])
            continue
        if current_section is not None and line.strip():
            sections[current_section].append(line.strip())
    return sections


def add_forbidden_findings(findings: list[Finding], payload: Any, scope: str) -> None:
    for message in scan_forbidden_content(payload, scope=scope):
        findings.append(Finding("error", scope, message))


def add(level: str, findings: list[Finding], scope: str, message: str) -> None:
    findings.append(Finding(level, scope, message))


def require_mapping(mapping: dict[str, Any], key: str, findings: list[Finding], scope: str) -> dict[str, Any] | None:
    value = mapping.get(key)
    if not isinstance(value, dict):
        add("error", findings, f"{scope}.{key}", "must be an object")
        return None
    return value


def require_list(mapping: dict[str, Any], key: str, findings: list[Finding], scope: str) -> list[Any] | None:
    value = mapping.get(key)
    if not isinstance(value, list):
        add("error", findings, f"{scope}.{key}", "must be a list")
        return None
    return value


def require_string(mapping: dict[str, Any], key: str, findings: list[Finding], scope: str) -> str | None:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        add("error", findings, f"{scope}.{key}", "must be a non-empty string")
        return None
    return value.strip()


def assessment_path_for_item(item: dict[str, Any], assessment_dir: Path) -> Path:
    seed = (
        str(item.get("video_id") or "")
        or str(item.get("triage_event_id") or "")
        or str(item.get("title") or "")
        or "augur-return"
    )
    slug = slugify(seed) or "augur-return"
    return assessment_dir / f"{slug}.json"


def validate_assessment(
    assessment: dict[str, Any],
    *,
    assessment_path: Path,
    item: dict[str, Any],
    queue: dict[str, Any] | None,
    findings: list[Finding],
    scope: str,
) -> None:
    schema_version = require_string(assessment, "schema_version", findings, scope)
    if schema_version and schema_version != ASSESSMENT_SCHEMA_VERSION:
        add("error", findings, f"{scope}.schema_version", f"must equal {ASSESSMENT_SCHEMA_VERSION!r}")

    bridge_item = require_mapping(assessment, "bridge_item", findings, scope)
    paths = require_mapping(assessment, "paths", findings, scope)
    response = require_mapping(assessment, "response", findings, scope)
    result = require_mapping(assessment, "assessment", findings, scope)

    if bridge_item is not None:
        for key in ("decision", "title", "video_id"):
            require_string(bridge_item, key, findings, f"{scope}.bridge_item")

    if paths is not None:
        assessment_json_path = require_string(paths, "assessment_json_path", findings, f"{scope}.paths")
        resolved_assessment = resolve_repo_path(assessment_json_path)
        if resolved_assessment is None or resolved_assessment != assessment_path:
            add("error", findings, f"{scope}.paths.assessment_json_path", "must point to the current assessment file")

    response_exists = False
    response_missing_sections: list[Any] = []
    if response is not None:
        exists = response.get("exists")
        if not isinstance(exists, bool):
            add("error", findings, f"{scope}.response.exists", "must be a boolean")
        else:
            response_exists = exists
        require_list(response, "required_sections", findings, f"{scope}.response")
        present_sections = require_list(response, "present_sections", findings, f"{scope}.response")
        missing_sections = require_list(response, "missing_sections", findings, f"{scope}.response")
        response_missing_sections = missing_sections or []
        if present_sections is not None and response_exists:
            present_names = {str(value) for value in present_sections}
            if item.get("augur_response_path"):
                response_path = resolve_repo_path(str(item.get("augur_response_path")))
                if response_path is not None and response_path.exists():
                    response_body = response_path.read_text(encoding="utf-8")
                    parsed_sections = parse_response_sections(response_body)
                    expected_names = set(parsed_sections.keys())
                    if expected_names != present_names:
                        add("error", findings, f"{scope}.response.present_sections", "does not match the landed markdown headings")

    queue_decision: str | None = None
    if result is not None:
        response_status = require_string(result, "response_status", findings, scope)
        queue_decision = require_string(result, "queue_decision", findings, scope)
        for key in ("verified_fact_candidates", "inference_points", "next_source_recommendations"):
            require_list(result, key, findings, f"{scope}.assessment")
        if response_status == "awaiting_augur_response" and response_exists:
            add("error", findings, f"{scope}.assessment.response_status", "cannot be awaiting when the response file exists")
        if response_status == "invalid_return_structure" and not response_exists:
            add("error", findings, f"{scope}.assessment.response_status", "cannot be invalid when the response file is absent")
        if response_status == "assessed" and response_missing_sections:
            add("error", findings, f"{scope}.assessment.response_status", "cannot be assessed while required sections are missing")

    if queue is not None and queue_decision is not None:
        video_id = str(item.get("video_id"))
        pending = {str(row.get("video_id")) for row in queue.get("pending_returns", []) if isinstance(row, dict)}
        queued = {str(row.get("video_id")) for row in queue.get("queue", []) if isinstance(row, dict)}
        held = {str(row.get("video_id")) for row in queue.get("holds", []) if isinstance(row, dict)}
        if queue_decision == "awaiting_response" and video_id not in pending:
            add("error", findings, f"{scope}.assessment.queue_decision", "awaiting-response items must appear in queue.pending_returns")
        if queue_decision == "escalate_to_primary" and video_id not in queued:
            add("error", findings, f"{scope}.assessment.queue_decision", "queued items must appear in queue.queue")
        if queue_decision == "hold" and video_id not in held:
            add("error", findings, f"{scope}.assessment.queue_decision", "held items must appear in queue.holds")

    add_forbidden_findings(findings, assessment, scope)


def render_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Acumen Augur Return Report",
        "",
        f"- Bridge JSON: `{report['bridge_json']}`",
        f"- Queue JSON: `{report['queue_json']}`",
        f"- Checked at: `{report['checked_at']}`",
        f"- OK: `{str(report['ok']).lower()}`",
        f"- Bridge items: `{report['bridge_items']}`",
        f"- Assessments checked: `{report['assessments_checked']}`",
        f"- Findings: `{len(report['findings'])}`",
        "",
        "## Findings",
        "",
    ]
    if report["findings"]:
        for finding in report["findings"]:
            lines.append(f"- [{finding['level']}] `{finding['scope']}` {finding['message']}")
    else:
        lines.append("- no findings")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    bridge_path = Path(args.bridge_json).expanduser().resolve()
    assessment_dir = Path(args.assessment_json_dir).expanduser().resolve()
    queue_path = Path(args.queue_json).expanduser().resolve()
    output_md = Path(args.output_md).expanduser().resolve()
    output_json = Path(args.output_json).expanduser().resolve()

    findings: list[Finding] = []
    bridge = load_json_object(bridge_path, findings, "bridge")
    queue = load_json_object(queue_path, findings, "queue")
    assessments_checked = 0
    bridge_items = 0

    if queue is not None:
        schema_version = require_string(queue, "schema_version", findings, "queue")
        if schema_version and schema_version != QUEUE_SCHEMA_VERSION:
            add("error", findings, "queue.schema_version", f"must equal {QUEUE_SCHEMA_VERSION!r}")
        counts = require_mapping(queue, "counts", findings, "queue")
        pending = require_list(queue, "pending_returns", findings, "queue") or []
        queued = require_list(queue, "queue", findings, "queue") or []
        held = require_list(queue, "holds", findings, "queue") or []
        if counts is not None:
            expected = {
                "items_tracked": len(pending) + len(queued) + len(held),
                "pending_returns": len(pending),
                "queued_for_primary": len(queued),
                "held": len(held),
            }
            for key, expected_value in expected.items():
                actual = counts.get(key)
                if actual != expected_value:
                    add("error", findings, f"queue.counts.{key}", f"must equal {expected_value}")
        add_forbidden_findings(findings, queue, "queue")

    if bridge is not None:
        schema_version = require_string(bridge, "schema_version", findings, "bridge")
        if schema_version and schema_version not in SUPPORTED_BRIDGE_SCHEMA_VERSIONS:
            allowed = ", ".join(sorted(SUPPORTED_BRIDGE_SCHEMA_VERSIONS))
            add("error", findings, "bridge.schema_version", f"must be one of: {allowed}")
        items = bridge.get("items")
        if not isinstance(items, list):
            add("error", findings, "bridge.items", "must be a list")
            items = []
        bridge_items = len(items)

        for index, item in enumerate(items):
            scope = f"bridge.items[{index}]"
            if not isinstance(item, dict):
                add("error", findings, scope, "must be an object")
                continue

            assessment_path = assessment_path_for_item(item, assessment_dir)
            assessment = load_json_object(assessment_path, findings, f"{scope}.assessment_file")
            if assessment is not None:
                assessments_checked += 1
                validate_assessment(
                    assessment,
                    assessment_path=assessment_path,
                    item=item,
                    queue=queue,
                    findings=findings,
                    scope=f"{scope}.assessment",
                )

            response_path = resolve_repo_path(str(item.get("augur_response_path", "")))
            if response_path is None:
                add("error", findings, f"{scope}.augur_response_path", "must resolve inside repo")
                continue
            if not response_path.exists():
                add("warning", findings, f"{scope}.augur_response_path", f"response not landed yet: {repo_rel(response_path)}")
                continue
            if response_path.suffix.lower() != ".md":
                add("error", findings, f"{scope}.augur_response_path", "response must be markdown")
                continue
            parsed_sections = parse_response_sections(response_path.read_text(encoding="utf-8"))
            missing_sections = [section for section in REQUIRED_SECTIONS if section not in parsed_sections]
            if missing_sections:
                add(
                    "error",
                    findings,
                    f"{scope}.augur_response_path",
                    f"missing required sections: {', '.join(missing_sections)}",
                )

    report = {
        "bridge_json": repo_rel(bridge_path) if bridge_path.exists() else str(bridge_path),
        "queue_json": repo_rel(queue_path) if queue_path.exists() else str(queue_path),
        "checked_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "ok": not any(finding.level == "error" for finding in findings),
        "bridge_items": bridge_items,
        "assessments_checked": assessments_checked,
        "findings": [asdict(finding) for finding in findings],
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown_report(report), encoding="utf-8")
    print(repo_rel(output_json))
    print(repo_rel(output_md))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

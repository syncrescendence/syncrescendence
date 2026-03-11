#!/usr/bin/env python3
"""Validate the office-harness exocortex projection and its append-only snapshot ledger."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = REPO_ROOT / "orchestration" / "state"
BRIDGE_PATH = REPO_ROOT / "operators" / "exocortex" / "office_harness_projection_bridge.py"
DEFAULT_REGISTRY = REPO_ROOT / "orchestration" / "state" / "registry" / "office-harness-bindings.effective.json"
DEFAULT_SURFACE_REGISTRY = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-SURFACE-REGISTRY-CC90.json"
DEFAULT_TELEOLOGY_REGISTRY = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-TELEOLOGY-REGISTRY-CC90.json"
DEFAULT_CONTROL_PLANE_STATUS = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json"
DEFAULT_PROJECTION = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-OFFICE-HARNESS-PROJECTION-CC92.json"
DEFAULT_LEDGER = REPO_ROOT / "orchestration" / "state" / "registry" / "office-harness-exocortex-projection-ledger.jsonl"
DEFAULT_JSON_REPORT = STATE_DIR / "OFFICE-HARNESS-EXOCORTEX-PROJECTION-REPORT.json"
DEFAULT_MD_REPORT = STATE_DIR / "OFFICE-HARNESS-EXOCORTEX-PROJECTION-REPORT.md"

LEDGER_SCHEMA_VERSION = "office-harness-exocortex-projection-ledger-event/v1"
EXPECTED_EVENT_TYPES = {"projection_seeded", "projection_refresh"}
EVENT_ID_RE = re.compile(r"^ohxp-[0-9]{8}-[0-9]{4}$")
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


@dataclass(frozen=True)
class Finding:
    level: str
    scope: str
    message: str


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def add_finding(findings: list[Finding], scope: str, message: str, *, level: str = "error") -> None:
    findings.append(Finding(level=level, scope=scope, message=message))


def repo_rel(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_json_object(path: Path, findings: list[Finding], scope: str) -> dict[str, Any]:
    if not path.exists():
        add_finding(findings, scope, f"missing file: {repo_rel(path)}")
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_finding(findings, scope, f"invalid JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        add_finding(findings, scope, "expected top-level JSON object")
        return {}
    return data


def require_string_list(
    findings: list[Finding],
    event: dict[str, Any],
    key: str,
    *,
    scope: str,
) -> list[str]:
    value = event.get(key)
    if not isinstance(value, list):
        add_finding(findings, scope, f"{key} must be a list")
        return []
    items: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            add_finding(findings, f"{scope}:{index}", f"{key}[{index}] must be a non-empty string")
            continue
        if item in seen:
            add_finding(findings, f"{scope}:{index}", f"{key}[{index}] duplicates {item!r}")
            continue
        seen.add(item)
        items.append(item)
    return items


def require_non_negative_int(
    findings: list[Finding],
    event: dict[str, Any],
    key: str,
    *,
    scope: str,
) -> int | None:
    value = event.get(key)
    if not isinstance(value, int) or value < 0:
        add_finding(findings, scope, f"{key} must be a non-negative integer")
        return None
    return value


def require_counter(
    findings: list[Finding],
    event: dict[str, Any],
    key: str,
    *,
    scope: str,
) -> dict[str, int]:
    value = event.get(key)
    if not isinstance(value, dict):
        add_finding(findings, scope, f"{key} must be an object")
        return {}
    counter: dict[str, int] = {}
    for nested_key, nested_value in value.items():
        if not isinstance(nested_key, str) or not nested_key:
            add_finding(findings, scope, f"{key} keys must be non-empty strings")
            continue
        if not isinstance(nested_value, int) or nested_value < 0:
            add_finding(findings, f"{scope}.{nested_key}", f"{key}.{nested_key} must be a non-negative integer")
            continue
        counter[nested_key] = nested_value
    return counter


def parse_ledger(
    *,
    path: Path,
    findings: list[Finding],
    bridge: Any,
    projection_path: Path,
    registry_path: Path,
    surface_registry_path: Path,
    teleology_registry_path: Path,
    control_plane_status_path: Path,
) -> list[dict[str, Any]]:
    if not path.exists():
        add_finding(findings, "ledger", f"missing file: {repo_rel(path)}")
        return []

    events: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    previous_timestamp: str | None = None
    expected_paths = {
        "projection_family": bridge.PROJECTION_FAMILY,
        "projection_scope": bridge.SCOPE_ID,
        "projection_contract_path": bridge.CONTRACT_PATH,
        "source_effective_registry_path": repo_rel(registry_path),
        "source_surface_registry_path": repo_rel(surface_registry_path),
        "source_teleology_registry_path": repo_rel(teleology_registry_path),
        "source_control_plane_status_path": repo_rel(control_plane_status_path),
        "projection_path": repo_rel(projection_path),
    }

    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip():
            continue
        scope = f"ledger:{line_number}"
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            add_finding(findings, scope, f"invalid JSON line: {exc}")
            continue
        if not isinstance(event, dict):
            add_finding(findings, scope, "ledger line must be a JSON object")
            continue

        schema_version = event.get("schema_version")
        event_id = event.get("event_id")
        event_type = event.get("event_type")
        recorded_at = event.get("recorded_at")
        actor = event.get("actor")

        if schema_version != LEDGER_SCHEMA_VERSION:
            add_finding(findings, scope, f"schema_version must be {LEDGER_SCHEMA_VERSION!r}")
        if not isinstance(event_id, str) or not EVENT_ID_RE.fullmatch(event_id):
            add_finding(findings, scope, "event_id must match ohxp-YYYYMMDD-NNNN")
        elif event_id in seen_ids:
            add_finding(findings, scope, f"duplicate event_id {event_id!r}")
        else:
            seen_ids.add(event_id)
        if not isinstance(event_type, str) or event_type not in EXPECTED_EVENT_TYPES:
            add_finding(findings, scope, f"event_type must be one of {sorted(EXPECTED_EVENT_TYPES)}")
        if not isinstance(recorded_at, str) or not TIMESTAMP_RE.fullmatch(recorded_at):
            add_finding(findings, scope, "recorded_at must be ISO-8601 UTC with trailing Z")
        elif previous_timestamp is not None and recorded_at < previous_timestamp:
            add_finding(findings, scope, "ledger timestamps must be non-decreasing")
        else:
            previous_timestamp = recorded_at
        if not isinstance(actor, str) or not actor:
            add_finding(findings, scope, "actor must be a non-empty string")

        for key, expected in expected_paths.items():
            if event.get(key) != expected:
                add_finding(findings, scope, f"{key} must be {expected!r}")

        for key in (
            "source_effective_registry_sha256",
            "source_surface_registry_sha256",
            "source_teleology_registry_sha256",
            "source_control_plane_status_sha256",
            "projection_sha256",
        ):
            value = event.get(key)
            if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
                add_finding(findings, scope, f"{key} must be a sha256:... digest")

        projection_record_count = require_non_negative_int(findings, event, "projection_record_count", scope=scope)
        pointer_complete_record_count = require_non_negative_int(
            findings,
            event,
            "pointer_complete_record_count",
            scope=scope,
        )
        operative_record_count = require_non_negative_int(findings, event, "operative_record_count", scope=scope)
        informative_only_record_count = require_non_negative_int(
            findings,
            event,
            "informative_only_record_count",
            scope=scope,
        )
        projected_offices = require_string_list(findings, event, "projected_offices", scope=scope)
        projection_state_counts = require_counter(findings, event, "projection_state_counts", scope=scope)
        binding_state_counts = require_counter(findings, event, "binding_state_counts", scope=scope)

        if projection_record_count is not None and len(projected_offices) != projection_record_count:
            add_finding(findings, scope, "projection_record_count must equal len(projected_offices)")
        if projection_record_count is not None and pointer_complete_record_count is not None:
            if pointer_complete_record_count > projection_record_count:
                add_finding(findings, scope, "pointer_complete_record_count cannot exceed projection_record_count")
        if projection_record_count is not None and operative_record_count is not None and informative_only_record_count is not None:
            if operative_record_count + informative_only_record_count != projection_record_count:
                add_finding(
                    findings,
                    scope,
                    "operative_record_count plus informative_only_record_count must equal projection_record_count",
                )
        if projection_record_count is not None and sum(projection_state_counts.values()) != projection_record_count:
            add_finding(findings, scope, "projection_state_counts must sum to projection_record_count")
        if projection_record_count is not None and binding_state_counts and sum(binding_state_counts.values()) != projection_record_count:
            add_finding(findings, scope, "binding_state_counts must sum to projection_record_count")
        notes = event.get("notes")
        if notes is not None and (not isinstance(notes, str) or not notes.strip()):
            add_finding(findings, scope, "notes must be a non-empty string when present")

        events.append(event)

    return events


def validate_latest_receipt_alignment(
    *,
    events: list[dict[str, Any]],
    findings: list[Finding],
    bridge: Any,
    projection: dict[str, Any],
    projection_path: Path,
    registry_path: Path,
    registry_sha256: str,
    surface_registry_path: Path,
    teleology_registry_path: Path,
    control_plane_status_path: Path,
    report_summary: dict[str, Any],
) -> tuple[str, str | None]:
    if not events:
        add_finding(findings, "ledger", "ledger must contain at least one projection receipt event")
        return "missing_receipt", None

    latest = events[-1]
    latest_event_id = latest.get("event_id") if isinstance(latest.get("event_id"), str) else None
    expected_values: dict[str, Any] = {
        "projection_family": bridge.PROJECTION_FAMILY,
        "projection_scope": bridge.SCOPE_ID,
        "projection_contract_path": bridge.CONTRACT_PATH,
        "source_effective_registry_path": repo_rel(registry_path),
        "source_effective_registry_sha256": registry_sha256,
        "source_surface_registry_path": repo_rel(surface_registry_path),
        "source_surface_registry_sha256": bridge.sha256_file(surface_registry_path),
        "source_teleology_registry_path": repo_rel(teleology_registry_path),
        "source_teleology_registry_sha256": bridge.sha256_file(teleology_registry_path),
        "source_control_plane_status_path": repo_rel(control_plane_status_path),
        "source_control_plane_status_sha256": bridge.sha256_file(control_plane_status_path),
        "projection_path": repo_rel(projection_path),
        "projection_sha256": bridge.sha256_json(projection),
        "projection_record_count": report_summary.get("projection_record_count"),
        "projected_offices": report_summary.get("projected_offices"),
        "pointer_complete_record_count": report_summary.get("pointer_complete_record_count"),
        "operative_record_count": report_summary.get("operative_record_count"),
        "informative_only_record_count": report_summary.get("informative_only_record_count"),
        "projection_state_counts": report_summary.get("projection_state_counts"),
        "binding_state_counts": report_summary.get("binding_state_counts"),
    }

    matched = True
    for key, expected in expected_values.items():
        if latest.get(key) != expected:
            add_finding(findings, "ledger.latest", f"{key} does not match the current projection snapshot")
            matched = False

    return ("current_matches_latest_receipt" if matched else "drift_detected"), latest_event_id


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Office-Harness Exocortex Projection Report",
        "",
        f"- generated_at: `{report['generated_at']}`",
        f"- status: `{summary['status']}`",
        f"- source registry: `{summary['source_registry_path']}`",
        f"- projection path: `{summary['projection_path']}`",
        f"- ledger path: `{summary['ledger_path']}`",
        f"- projection scope: `{summary['projection_scope']}`",
        f"- source registry sha256: `{summary['source_registry_sha256']}`",
        f"- projection sha256: `{summary['projection_sha256']}`",
        f"- expected projection sha256: `{summary['expected_projection_sha256']}`",
        f"- projection alignment: `{summary['projection_alignment_status']}`",
        f"- ledger alignment: `{summary['ledger_alignment_status']}`",
        f"- ledger events: `{summary['ledger_event_count']}`",
        f"- latest receipt event: `{summary['latest_receipt_event_id'] or 'none'}`",
        f"- scoped source rows: `{summary['scoped_source_record_count']}`",
        f"- projection rows: `{summary['projection_record_count']}`",
        f"- projected offices: `{', '.join(summary['projected_offices']) if summary['projected_offices'] else 'none'}`",
        f"- pointer-complete rows: `{summary['pointer_complete_record_count']}`",
        f"- operative rows: `{summary['operative_record_count']}`",
        f"- informative-only rows: `{summary['informative_only_record_count']}`",
        f"- findings: `{summary['finding_count']}`",
        "",
        "## Findings",
        "",
    ]
    findings = report["findings"]
    if not findings:
        lines.append("- none")
    else:
        for finding in findings:
            lines.append(f"- [{finding['level']}] `{finding['scope']}`: {finding['message']}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--surface-registry", type=Path, default=DEFAULT_SURFACE_REGISTRY)
    parser.add_argument("--teleology-registry", type=Path, default=DEFAULT_TELEOLOGY_REGISTRY)
    parser.add_argument("--control-plane-status", type=Path, default=DEFAULT_CONTROL_PLANE_STATUS)
    parser.add_argument("--projection", type=Path, default=DEFAULT_PROJECTION)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output-report-json", type=Path, default=DEFAULT_JSON_REPORT)
    parser.add_argument("--output-report-md", type=Path, default=DEFAULT_MD_REPORT)
    args = parser.parse_args()

    bridge = load_module(BRIDGE_PATH, "office_harness_projection_bridge")
    findings: list[Finding] = []

    registry_path = args.registry.expanduser().resolve()
    surface_registry_path = args.surface_registry.expanduser().resolve()
    teleology_registry_path = args.teleology_registry.expanduser().resolve()
    control_plane_status_path = args.control_plane_status.expanduser().resolve()
    projection_path = args.projection.expanduser().resolve()
    ledger_path = args.ledger.expanduser().resolve()
    output_report_json = args.output_report_json.expanduser().resolve()
    output_report_md = args.output_report_md.expanduser().resolve()

    rows, registry_sha256 = bridge.load_registry(registry_path)
    surface_registry_doc = bridge.load_json(surface_registry_path)
    teleology_registry_doc = bridge.load_json(teleology_registry_path)
    control_plane_status = bridge.load_json(control_plane_status_path)
    surface_registry = {
        str(row.get("slug")): row
        for row in surface_registry_doc.get("surfaces", [])
        if isinstance(row, dict) and isinstance(row.get("slug"), str)
    }
    teleology_registry = {
        str(row.get("slug")): row
        for row in teleology_registry_doc.get("surfaces", [])
        if isinstance(row, dict) and isinstance(row.get("slug"), str)
    }

    committed_projection = read_json_object(projection_path, findings, "projection")
    base_report = bridge.build_report(
        rows=rows,
        projection=committed_projection,
        registry_path=registry_path,
        projection_path=projection_path,
        registry_sha256=registry_sha256,
        surface_registry_path=surface_registry_path,
        surface_registry=surface_registry,
        teleology_registry_path=teleology_registry_path,
        teleology_registry=teleology_registry,
        control_plane_status_path=control_plane_status_path,
        control_plane_status_version=str(control_plane_status.get("version") or "unknown"),
    )
    for finding in base_report.get("findings", []):
        add_finding(
            findings,
            str(finding.get("scope") or "projection"),
            str(finding.get("message") or "invalid projection"),
            level=str(finding.get("level") or "error"),
        )

    expected_projection = bridge.build_projection(
        rows,
        registry_path=registry_path,
        registry_sha256=registry_sha256,
        surface_registry_path=surface_registry_path,
        surface_registry=surface_registry,
        teleology_registry_path=teleology_registry_path,
        teleology_registry=teleology_registry,
        control_plane_status_path=control_plane_status_path,
        control_plane_status=control_plane_status,
    )
    expected_projection_sha256 = bridge.sha256_json(expected_projection)
    projection_sha256 = bridge.sha256_json(committed_projection)
    projection_alignment_status = (
        "matches_repo_native_rebuild"
        if projection_sha256 == expected_projection_sha256
        else "drift_detected"
    )
    if projection_alignment_status != "matches_repo_native_rebuild":
        add_finding(
            findings,
            "projection.rebuild",
            "committed projection does not match deterministic rebuild from repo-native proof state",
        )

    events = parse_ledger(
        path=ledger_path,
        findings=findings,
        bridge=bridge,
        projection_path=projection_path,
        registry_path=registry_path,
        surface_registry_path=surface_registry_path,
        teleology_registry_path=teleology_registry_path,
        control_plane_status_path=control_plane_status_path,
    )
    ledger_alignment_status, latest_receipt_event_id = validate_latest_receipt_alignment(
        events=events,
        findings=findings,
        bridge=bridge,
        projection=committed_projection,
        projection_path=projection_path,
        registry_path=registry_path,
        registry_sha256=registry_sha256,
        surface_registry_path=surface_registry_path,
        teleology_registry_path=teleology_registry_path,
        control_plane_status_path=control_plane_status_path,
        report_summary=base_report["summary"],
    )

    summary = dict(base_report["summary"])
    summary["expected_projection_sha256"] = expected_projection_sha256
    summary["projection_alignment_status"] = projection_alignment_status
    summary["ledger_path"] = repo_rel(ledger_path)
    summary["ledger_event_count"] = len(events)
    summary["latest_receipt_event_id"] = latest_receipt_event_id
    summary["ledger_alignment_status"] = ledger_alignment_status
    summary["finding_count"] = len(findings)
    summary["status"] = "coherent" if not findings else "findings_present"

    report = {
        "schema_version": "office-harness-exocortex-projection-report/v1",
        "generated_at": utc_now(),
        "mode": "report-first",
        "summary": summary,
        "findings": [asdict(finding) for finding in findings],
    }

    output_report_json.parent.mkdir(parents=True, exist_ok=True)
    output_report_json.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")
    output_report_md.parent.mkdir(parents=True, exist_ok=True)
    output_report_md.write_text(render_markdown(report), encoding="utf-8")

    print(output_report_json)
    print(output_report_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

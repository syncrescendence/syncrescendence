#!/usr/bin/env python3
"""Validate the Acumen verification queue, dossier, and Augur bridge artifacts."""

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


BRIDGE_SCHEMA_VERSION = "acumen.verification.bridge/v2"
DOSSIER_SCHEMA_VERSION = "acumen.verification.dossier/v1"
PORTFOLIO_SCHEMA_VERSION = "acumen.verification.portfolio/v1"
ELIGIBLE_DECISIONS = {"Promote", "Flag-for-Primary"}
QUEUE_STATUSES = {
    "awaiting_dispatch",
    "awaiting_response",
    "response_landed_uningested",
    "response_ingested",
}
STATE_DIR = REPO_ROOT / "orchestration" / "state"
DEFAULT_BRIDGE_JSON = STATE_DIR / "ACUMEN-AUGUR-VERIFICATION-BRIDGE.json"
DEFAULT_MD_REPORT = STATE_DIR / "ACUMEN-AUGUR-VERIFICATION-BRIDGE-REPORT.md"
DEFAULT_JSON_REPORT = STATE_DIR / "ACUMEN-AUGUR-VERIFICATION-BRIDGE-REPORT.json"
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


@dataclass(frozen=True)
class Finding:
    level: str
    scope: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bridge-json", default=str(DEFAULT_BRIDGE_JSON))
    parser.add_argument("--output-md", default=str(DEFAULT_MD_REPORT))
    parser.add_argument("--output-json", default=str(DEFAULT_JSON_REPORT))
    return parser.parse_args()


def add_finding(findings: list[Finding], scope: str, message: str, *, level: str = "error") -> None:
    findings.append(Finding(level=level, scope=scope, message=message))


def load_json_object(path: Path, findings: list[Finding], scope: str) -> dict[str, Any] | None:
    if not path.exists():
        add_finding(findings, scope, f"missing file: {repo_rel(path)}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_finding(findings, scope, f"invalid JSON: {exc}")
        return None
    if not isinstance(payload, dict):
        add_finding(findings, scope, "must be a JSON object")
        return None
    return payload


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


def require_string(mapping: dict[str, Any], key: str, findings: list[Finding], scope: str) -> str | None:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        add_finding(findings, f"{scope}.{key}", "must be a non-empty string")
        return None
    return value.strip()


def require_integer(mapping: dict[str, Any], key: str, findings: list[Finding], scope: str) -> int | None:
    value = mapping.get(key)
    if not isinstance(value, int):
        add_finding(findings, f"{scope}.{key}", "must be an integer")
        return None
    return value


def require_boolean(mapping: dict[str, Any], key: str, findings: list[Finding], scope: str) -> bool | None:
    value = mapping.get(key)
    if not isinstance(value, bool):
        add_finding(findings, f"{scope}.{key}", "must be a boolean")
        return None
    return value


def require_mapping(mapping: dict[str, Any], key: str, findings: list[Finding], scope: str) -> dict[str, Any] | None:
    value = mapping.get(key)
    if not isinstance(value, dict):
        add_finding(findings, f"{scope}.{key}", "must be a JSON object")
        return None
    return value


def add_forbidden_findings(findings: list[Finding], payload: Any, scope: str) -> None:
    for message in scan_forbidden_content(payload, scope=scope):
        add_finding(findings, scope, message)


def validate_augur_packet(
    packet_path: Path,
    dossier_path: Path,
    response_path: str,
    findings: list[Finding],
    scope: str,
) -> None:
    if not packet_path.exists():
        add_finding(findings, scope, f"missing Augur packet: {repo_rel(packet_path)}")
        return
    if packet_path.suffix.lower() != ".md":
        add_finding(findings, scope, "Augur packet must be markdown")
        return
    body = packet_path.read_text(encoding="utf-8")
    required_snippets = [
        "Packet type: `acumen_verification_bridge`",
        repo_rel(dossier_path),
        response_path,
        "Acumen remains the intake and triage plane.",
        "Augur is downstream verification only.",
        "Drafting mode: `reconnaissance_only`",
    ]
    for snippet in required_snippets:
        if snippet not in body:
            add_finding(findings, scope, f"packet is missing required snippet: {snippet}")


def validate_dossier(dossier: dict[str, Any], dossier_path: Path, findings: list[Finding], scope: str) -> None:
    schema_version = require_string(dossier, "schema_version", findings, scope)
    generated_at = require_string(dossier, "generated_at", findings, scope)
    if schema_version and schema_version != DOSSIER_SCHEMA_VERSION:
        add_finding(findings, f"{scope}.schema_version", f"must equal {DOSSIER_SCHEMA_VERSION!r}")
    if generated_at and not TIMESTAMP_RE.fullmatch(generated_at):
        add_finding(findings, f"{scope}.generated_at", "must be ISO-8601 UTC")

    decision = require_mapping(dossier, "decision_metadata", findings, scope)
    source = require_mapping(dossier, "source_summary", findings, scope)
    source_packet = require_mapping(dossier, "source_packet", findings, scope)
    policy = require_mapping(dossier, "policy", findings, scope)
    paths = require_mapping(dossier, "paths", findings, scope)
    repo_sovereignty = require_mapping(dossier, "repo_sovereignty", findings, scope)

    if decision is not None:
        decision_value = require_string(decision, "decision", findings, f"{scope}.decision_metadata")
        require_string(decision, "triage_event_id", findings, f"{scope}.decision_metadata")
        require_string(decision, "title", findings, f"{scope}.decision_metadata")
        if decision_value and decision_value not in ELIGIBLE_DECISIONS:
            add_finding(findings, f"{scope}.decision_metadata.decision", "must be Promote or Flag-for-Primary")
    if source is not None:
        for key in ("title", "channel_name", "channel_id", "video_id", "input_summary"):
            require_string(source, key, findings, f"{scope}.source_summary")
    if source_packet is not None:
        packet_path_value = require_string(source_packet, "packet_path", findings, f"{scope}.source_packet")
        exists = source_packet.get("exists")
        if not isinstance(exists, bool):
            add_finding(findings, f"{scope}.source_packet.exists", "must be a boolean")
        packet_path = resolve_repo_path(packet_path_value)
        if packet_path is None:
            add_finding(findings, f"{scope}.source_packet.packet_path", "must resolve inside repo")
        elif exists and not packet_path.exists():
            add_finding(findings, f"{scope}.source_packet.packet_path", f"missing packet: {repo_rel(packet_path)}")
    if policy is not None:
        add_forbidden_findings(findings, policy, f"{scope}.policy")
    if repo_sovereignty is not None:
        for key in ("intake_authority", "external_role", "repo_state_rule"):
            require_string(repo_sovereignty, key, findings, f"{scope}.repo_sovereignty")
    if paths is not None:
        dossier_path_value = require_string(paths, "dossier_path", findings, f"{scope}.paths")
        source_packet_path = require_string(paths, "source_packet_path", findings, f"{scope}.paths")
        augur_packet_path_value = require_string(paths, "augur_packet_path", findings, f"{scope}.paths")
        augur_response_path = require_string(paths, "augur_response_path", findings, f"{scope}.paths")
        require_string(paths, "triage_ledger_path", findings, f"{scope}.paths")
        require_string(paths, "training_ledger_path", findings, f"{scope}.paths")

        resolved_dossier = resolve_repo_path(dossier_path_value)
        if resolved_dossier is None or resolved_dossier != dossier_path:
            add_finding(findings, f"{scope}.paths.dossier_path", "must point to the current dossier file")
        if resolve_repo_path(source_packet_path) is None:
            add_finding(findings, f"{scope}.paths.source_packet_path", "must resolve inside repo")
        augur_packet_path = resolve_repo_path(augur_packet_path_value)
        if augur_packet_path is None:
            add_finding(findings, f"{scope}.paths.augur_packet_path", "must resolve inside repo")
        elif augur_response_path is not None:
            validate_augur_packet(augur_packet_path, dossier_path, augur_response_path, findings, f"{scope}.paths.augur_packet_path")

    add_forbidden_findings(findings, dossier, scope)


def validate_portfolio_surfaces(
    bridge: dict[str, Any],
    bridge_path: Path,
    findings: list[Finding],
    scope: str,
) -> None:
    runtime_surfaces = require_mapping(bridge, "runtime_surfaces", findings, scope)
    if runtime_surfaces is None:
        return
    portfolio_json_value = require_string(runtime_surfaces, "portfolio_json", findings, f"{scope}.runtime_surfaces")
    portfolio_md_value = require_string(runtime_surfaces, "portfolio_md", findings, f"{scope}.runtime_surfaces")
    portfolio_json_path = resolve_repo_path(portfolio_json_value)
    portfolio_md_path = resolve_repo_path(portfolio_md_value)
    if portfolio_json_path is None:
        add_finding(findings, f"{scope}.runtime_surfaces.portfolio_json", "must resolve inside repo")
        return
    if portfolio_md_path is None:
        add_finding(findings, f"{scope}.runtime_surfaces.portfolio_md", "must resolve inside repo")
        return
    portfolio = load_json_object(portfolio_json_path, findings, f"{scope}.runtime_surfaces.portfolio_json")
    if portfolio is not None:
        schema_version = require_string(portfolio, "schema_version", findings, f"{scope}.runtime_surfaces.portfolio_json")
        source_bridge_json = require_string(portfolio, "source_bridge_json", findings, f"{scope}.runtime_surfaces.portfolio_json")
        if schema_version and schema_version != PORTFOLIO_SCHEMA_VERSION:
            add_finding(findings, f"{scope}.runtime_surfaces.portfolio_json.schema_version", f"must equal {PORTFOLIO_SCHEMA_VERSION!r}")
        if source_bridge_json and resolve_repo_path(source_bridge_json) != bridge_path:
            add_finding(findings, f"{scope}.runtime_surfaces.portfolio_json.source_bridge_json", "must point to the validated bridge JSON")
    if not portfolio_md_path.exists():
        add_finding(findings, f"{scope}.runtime_surfaces.portfolio_md", f"missing markdown surface: {repo_rel(portfolio_md_path)}")
    else:
        body = portfolio_md_path.read_text(encoding="utf-8")
        if "Acumen Augur Verification Portfolio" not in body:
            add_finding(findings, f"{scope}.runtime_surfaces.portfolio_md", "markdown surface must carry the portfolio heading")


def validate_counts(bridge: dict[str, Any], items: list[dict[str, Any]], findings: list[Finding], scope: str) -> None:
    counts = require_mapping(bridge, "counts", findings, scope)
    selection = require_mapping(bridge, "selection", findings, scope)
    if counts is None or selection is None:
        return

    expected = {
        "eligible_items_total": len(items),
        "open_items_total": sum(1 for item in items if item.get("is_open") is True),
        "selected_batch_items": sum(1 for item in items if item.get("selected_in_batch") is True),
        "remaining_open_after_batch": sum(1 for item in items if item.get("is_open") is True and item.get("selected_in_batch") is not True),
        "awaiting_dispatch": sum(1 for item in items if item.get("queue_status") == "awaiting_dispatch"),
        "awaiting_response": sum(1 for item in items if item.get("queue_status") == "awaiting_response"),
        "response_landed_uningested": sum(1 for item in items if item.get("queue_status") == "response_landed_uningested"),
        "response_ingested": sum(1 for item in items if item.get("queue_status") == "response_ingested"),
        "promote_open_items": sum(1 for item in items if item.get("is_open") is True and item.get("decision") == "Promote"),
        "primary_flagged_open_items": sum(1 for item in items if item.get("is_open") is True and item.get("decision") == "Flag-for-Primary"),
        "dossiers_written": sum(1 for item in items if item.get("selected_in_batch") is True),
        "augur_packets_written": sum(1 for item in items if item.get("selected_in_batch") is True),
        "eligible_items_written": sum(1 for item in items if item.get("selected_in_batch") is True),
    }
    for key, expected_value in expected.items():
        value = counts.get(key)
        if value != expected_value:
            add_finding(findings, f"{scope}.counts.{key}", f"must equal computed value {expected_value}")

    selected_batch_items = selection.get("selected_batch_items")
    remaining_open_after_batch = selection.get("remaining_open_after_batch")
    if selected_batch_items != expected["selected_batch_items"]:
        add_finding(findings, f"{scope}.selection.selected_batch_items", f"must equal {expected['selected_batch_items']}")
    if remaining_open_after_batch != expected["remaining_open_after_batch"]:
        add_finding(findings, f"{scope}.selection.remaining_open_after_batch", f"must equal {expected['remaining_open_after_batch']}")


def validate_item(item: dict[str, Any], findings: list[Finding], scope: str) -> None:
    require_integer(item, "queue_rank", findings, scope)
    require_integer(item, "batch_priority", findings, scope)
    decision = require_string(item, "decision", findings, scope)
    dossier_path_value = require_string(item, "dossier_path", findings, scope)
    augur_packet_path_value = require_string(item, "augur_packet_path", findings, scope)
    augur_response_path = require_string(item, "augur_response_path", findings, scope)
    require_string(item, "triage_event_id", findings, scope)
    require_string(item, "video_id", findings, scope)
    queue_status = require_string(item, "queue_status", findings, scope)
    is_open = require_boolean(item, "is_open", findings, scope)
    dossier_exists = require_boolean(item, "dossier_exists", findings, scope)
    packet_exists = require_boolean(item, "augur_packet_exists", findings, scope)
    response_exists = require_boolean(item, "augur_response_exists", findings, scope)
    response_event_exists = require_boolean(item, "augur_response_event_exists", findings, scope)
    require_boolean(item, "selected_in_batch", findings, scope)

    if decision and decision not in ELIGIBLE_DECISIONS:
        add_finding(findings, f"{scope}.decision", "must be Promote or Flag-for-Primary")
    if queue_status and queue_status not in QUEUE_STATUSES:
        add_finding(findings, f"{scope}.queue_status", f"must be one of {sorted(QUEUE_STATUSES)}")

    if queue_status == "awaiting_dispatch":
        if is_open is False:
            add_finding(findings, f"{scope}.is_open", "awaiting_dispatch items must remain open")
        if packet_exists is True:
            add_finding(findings, f"{scope}.augur_packet_exists", "awaiting_dispatch items must not already have a packet")
        if response_exists is True or response_event_exists is True:
            add_finding(findings, scope, "awaiting_dispatch items must not carry a response")
    elif queue_status == "awaiting_response":
        if not packet_exists:
            add_finding(findings, f"{scope}.augur_packet_exists", "awaiting_response items must have a packet")
        if response_exists is True or response_event_exists is True:
            add_finding(findings, scope, "awaiting_response items must not already have a landed response")
    elif queue_status == "response_landed_uningested":
        if not packet_exists or not response_exists:
            add_finding(findings, scope, "response_landed_uningested items must have packet and response artifacts")
        if response_event_exists is True:
            add_finding(findings, f"{scope}.augur_response_event_exists", "response_landed_uningested items must not already be ingested")
    elif queue_status == "response_ingested":
        if is_open is True:
            add_finding(findings, f"{scope}.is_open", "response_ingested items must be closed")
        if not packet_exists or not response_exists or not response_event_exists:
            add_finding(findings, scope, "response_ingested items must have packet, response, and ingestion event")

    dossier_path = resolve_repo_path(dossier_path_value)
    augur_packet_path = resolve_repo_path(augur_packet_path_value)
    if dossier_path is None:
        add_finding(findings, f"{scope}.dossier_path", "must resolve inside repo")
        return
    if augur_packet_path is None:
        add_finding(findings, f"{scope}.augur_packet_path", "must resolve inside repo")
        return

    if dossier_exists:
        dossier = load_json_object(dossier_path, findings, f"{scope}.dossier")
        if dossier is not None:
            validate_dossier(dossier, dossier_path, findings, f"{scope}.dossier")
    elif queue_status != "awaiting_dispatch":
        add_finding(findings, f"{scope}.dossier_exists", "non-dispatch items must have a dossier on disk")

    if packet_exists:
        if not dossier_exists:
            add_finding(findings, f"{scope}.dossier_exists", "packet-bearing items must also have a dossier")
        elif augur_response_path is not None:
            validate_augur_packet(augur_packet_path, dossier_path, augur_response_path, findings, f"{scope}.augur_packet_path")

    add_forbidden_findings(findings, item, scope)


def render_markdown_report(report: dict[str, Any]) -> str:
    counts = report["counts"]
    selection = report["selection"]
    lines = [
        "# Acumen Augur Verification Bridge Report",
        "",
        f"- Bridge JSON: `{report['bridge_json']}`",
        f"- Checked at: `{report['checked_at']}`",
        f"- OK: `{str(report['ok']).lower()}`",
        f"- Eligible items: `{counts.get('eligible_items_total', 0)}`",
        f"- Open queue: `{counts.get('open_items_total', 0)}`",
        f"- Selected batch items: `{selection.get('selected_batch_items', 0)}`",
        f"- Remaining open after batch: `{selection.get('remaining_open_after_batch', 0)}`",
        f"- Awaiting dispatch: `{counts.get('awaiting_dispatch', 0)}`",
        f"- Awaiting response: `{counts.get('awaiting_response', 0)}`",
        f"- Response landed, still uningested: `{counts.get('response_landed_uningested', 0)}`",
        f"- Response ingested: `{counts.get('response_ingested', 0)}`",
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
    output_md = Path(args.output_md).expanduser().resolve()
    output_json = Path(args.output_json).expanduser().resolve()

    findings: list[Finding] = []
    bridge = load_json_object(bridge_path, findings, "bridge")
    items: list[dict[str, Any]] = []
    counts: dict[str, Any] = {}
    selection: dict[str, Any] = {}

    if bridge is not None:
        schema_version = require_string(bridge, "schema_version", findings, "bridge")
        generated_at = require_string(bridge, "generated_at", findings, "bridge")
        if schema_version and schema_version != BRIDGE_SCHEMA_VERSION:
            add_finding(findings, "bridge.schema_version", f"must equal {BRIDGE_SCHEMA_VERSION!r}")
        if generated_at and not TIMESTAMP_RE.fullmatch(generated_at):
            add_finding(findings, "bridge.generated_at", "must be ISO-8601 UTC")

        batch_rules = require_mapping(bridge, "batch_rules", findings, "bridge")
        selection = require_mapping(bridge, "selection", findings, "bridge") or {}
        if batch_rules is not None:
            require_string(batch_rules, "selection_surface", findings, "bridge.batch_rules")
            require_string(batch_rules, "default_batch_scope", findings, "bridge.batch_rules")
            require_string(batch_rules, "override_flag", findings, "bridge.batch_rules")
            require_string(batch_rules, "close_condition", findings, "bridge.batch_rules")
            require_string(batch_rules, "sanitization_rule", findings, "bridge.batch_rules")

        raw_items = bridge.get("items")
        if not isinstance(raw_items, list):
            add_finding(findings, "bridge.items", "must be a list")
            raw_items = []
        for index, item in enumerate(raw_items):
            scope = f"bridge.items[{index}]"
            if not isinstance(item, dict):
                add_finding(findings, scope, "must be an object")
                continue
            validate_item(item, findings, scope)
            items.append(item)

        validate_counts(bridge, items, findings, "bridge")
        validate_portfolio_surfaces(bridge, bridge_path, findings, "bridge")
        counts = bridge.get("counts", {}) if isinstance(bridge.get("counts"), dict) else {}
        add_forbidden_findings(findings, bridge, "bridge")

    report = {
        "bridge_json": repo_rel(bridge_path) if bridge_path.exists() else str(bridge_path),
        "checked_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "ok": not any(finding.level == "error" for finding in findings),
        "counts": counts,
        "selection": selection,
        "items_checked": len(items),
        "findings": [asdict(finding) for finding in findings],
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown_report(report), encoding="utf-8")

    print(repo_rel(output_json))
    print(repo_rel(output_md))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

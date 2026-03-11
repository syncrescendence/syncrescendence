#!/usr/bin/env python3
"""Report-only validator for config-surface state, receipt-ledger joins, and rebuild parity."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from rematerialize_config_surface_state import (
    canonical_json_bytes,
    load_events as load_rematerialization_events,
    rematerialize as rematerialize_config_surface_state,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = REPO_ROOT / "orchestration" / "state"
DEFAULT_REGISTRY = REPO_ROOT / "orchestration" / "state" / "registry" / "CONFIG-SURFACE-REGISTRY-v1.json"
DEFAULT_MATRIX = REPO_ROOT / "orchestration" / "state" / "registry" / "CONFIG-SURFACE-PROJECTION-MATRIX-v1.json"
DEFAULT_LEDGER = REPO_ROOT / "orchestration" / "state" / "registry" / "config-surface-state-ledger.jsonl"
DEFAULT_MD_REPORT = STATE_DIR / "CONFIG-SURFACE-STATE-VALIDATION-REPORT.md"
DEFAULT_JSON_REPORT = STATE_DIR / "CONFIG-SURFACE-STATE-VALIDATION-REPORT.json"

EXPECTED_REGISTRY_ID = "config-surface-registry-v1"
EXPECTED_MATRIX_ID = "config-surface-projection-matrix-v1"
EXPECTED_LEDGER_FAMILY = "config_surface_state"
EXPECTED_LEDGER_PATH = "orchestration/state/registry/config-surface-state-ledger.jsonl"
EXPECTED_VALIDATOR_PATH = "operators/validators/validate_config_surface_state.py"
EXPECTED_REMATERIALIZER_PATH = "operators/validators/rematerialize_config_surface_state.py"
SHARED_PROJECTION_CONTRACT_PATH = "orchestration/state/impl/PROJECTION-FAMILY-SOVEREIGNTY-NORMALIZATION-v1.md"
CHAT_CI_PROVIDER_PROFILES_PATH = "orchestration/state/registry/CHAT-CI-PROVIDER-PROFILES-v1.json"
CHAT_CI_PROJECTION_PACK_PATH = "orchestration/state/registry/CHAT-CI-PROJECTION-PACK-v1.json"
EXPECTED_CHAT_CI_GOVERNANCE = {
    "shared_contract_path": SHARED_PROJECTION_CONTRACT_PATH,
    "sovereignty_rule": "repo_ratifies_exocortex_coordinates_projection_derives",
    "capture_policy": "manual_export_only",
    "reliance_ceiling": "informative_only_until_receipted_export",
    "hidden_second_control_plane": "prohibited",
}
EXPECTED_EVENT_TYPES = {"seed_receipt", "receipt_refresh", "drift_receipt", "supersession_receipt"}
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
EVENT_ID_RE = re.compile(r"^csl-[0-9]{8}-[0-9]{4}$")

FIELD_KEY_MAP = {
    "required_families": "required_families",
    "collapsed_families": "collapsed_families",
    "conditional_families": "conditional_families",
    "typically_omitted_families": "omitted_families",
    "structurally_encoded_families": "structurally_encoded_families",
}


@dataclass(frozen=True)
class Finding:
    level: str
    scope: str
    message: str


def add_finding(findings: list[Finding], scope: str, message: str, *, level: str = "error") -> None:
    findings.append(Finding(level=level, scope=scope, message=message))


def repo_rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def sha256_for_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def joint_sha256(registry_sha256: str, matrix_sha256: str) -> str:
    digest = hashlib.sha256()
    digest.update(f"{registry_sha256}\n{matrix_sha256}\n".encode("utf-8"))
    return f"sha256:{digest.hexdigest()}"


def read_json_dict(path: Path, findings: list[Finding], scope: str) -> dict[str, Any]:
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


def ensure_list_of_dicts(
    container: dict[str, Any],
    key: str,
    findings: list[Finding],
    scope: str,
) -> list[dict[str, Any]]:
    value = container.get(key)
    if not isinstance(value, list):
        add_finding(findings, scope, f"{key} must be a list")
        return []
    items: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            add_finding(findings, f"{scope}:{index}", f"{key}[{index}] must be an object")
            continue
        items.append(item)
    return items


def ensure_string_list(
    mapping: dict[str, Any],
    key: str,
    findings: list[Finding],
    scope: str,
) -> list[str]:
    value = mapping.get(key)
    if not isinstance(value, list):
        add_finding(findings, scope, f"{key} must be a list")
        return []
    items: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            add_finding(findings, f"{scope}:{index}", f"{key}[{index}] must be a non-empty string")
            continue
        items.append(item)
    return items


def validate_atom_families(
    registry: dict[str, Any],
    matrix: dict[str, Any],
    findings: list[Finding],
) -> list[str]:
    atom_families = ensure_list_of_dicts(registry, "atom_families", findings, "registry.atom_families")
    family_ids: list[str] = []
    seen: set[str] = set()
    for index, family in enumerate(atom_families):
        family_id = family.get("atom_family_id")
        if not isinstance(family_id, str) or not family_id:
            add_finding(findings, f"registry.atom_families:{index}", "atom_family_id must be a non-empty string")
            continue
        if family_id in seen:
            add_finding(findings, f"registry.atom_families:{index}", f"duplicate atom_family_id {family_id!r}")
            continue
        seen.add(family_id)
        family_ids.append(family_id)

    compression_priority = ensure_string_list(registry, "compression_priority", findings, "registry.compression_priority")
    projection_order = ensure_string_list(matrix, "projection_order", findings, "matrix.projection_order")

    if family_ids and set(compression_priority) != set(family_ids):
        add_finding(
            findings,
            "registry.compression_priority",
            "compression_priority must cover the same atom families as registry.atom_families",
        )
    if family_ids and set(projection_order) != set(family_ids):
        add_finding(
            findings,
            "matrix.projection_order",
            "projection_order must cover the same atom families as registry.atom_families",
        )
    if compression_priority and projection_order and compression_priority != projection_order:
        add_finding(
            findings,
            "matrix.projection_order",
            "projection_order must match registry.compression_priority for the seed-state baseline",
        )

    return family_ids


def validate_surface_classes(
    registry: dict[str, Any],
    matrix: dict[str, Any],
    findings: list[Finding],
) -> None:
    registry_classes = ensure_list_of_dicts(registry, "surface_classes", findings, "registry.surface_classes")
    class_rules = ensure_list_of_dicts(matrix, "class_projection_rules", findings, "matrix.class_projection_rules")
    deferred_rules = ensure_list_of_dicts(matrix, "deferred_surface_classes", findings, "matrix.deferred_surface_classes")

    registry_by_class: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(registry_classes):
        surface_class = entry.get("surface_class")
        if not isinstance(surface_class, str) or not surface_class:
            add_finding(findings, f"registry.surface_classes:{index}", "surface_class must be a non-empty string")
            continue
        if surface_class in registry_by_class:
            add_finding(findings, f"registry.surface_classes:{index}", f"duplicate surface_class {surface_class!r}")
            continue
        registry_by_class[surface_class] = entry

    rule_by_class: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(class_rules):
        surface_class = entry.get("surface_class")
        if not isinstance(surface_class, str) or not surface_class:
            add_finding(findings, f"matrix.class_projection_rules:{index}", "surface_class must be a non-empty string")
            continue
        if surface_class in rule_by_class:
            add_finding(findings, f"matrix.class_projection_rules:{index}", f"duplicate surface_class {surface_class!r}")
            continue
        rule_by_class[surface_class] = entry

    deferred_by_class: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(deferred_rules):
        surface_class = entry.get("surface_class")
        if not isinstance(surface_class, str) or not surface_class:
            add_finding(findings, f"matrix.deferred_surface_classes:{index}", "surface_class must be a non-empty string")
            continue
        if surface_class in deferred_by_class:
            add_finding(findings, f"matrix.deferred_surface_classes:{index}", f"duplicate surface_class {surface_class!r}")
            continue
        deferred_by_class[surface_class] = entry

    for surface_class, registry_entry in registry_by_class.items():
        seed_status = registry_entry.get("seed_status")
        if seed_status == "deferred_external":
            if surface_class not in deferred_by_class:
                add_finding(
                    findings,
                    f"registry.surface_classes:{surface_class}",
                    "deferred registry surface_class must appear in matrix.deferred_surface_classes",
                )
            continue
        if surface_class not in rule_by_class:
            add_finding(
                findings,
                f"registry.surface_classes:{surface_class}",
                "seeded registry surface_class must appear in matrix.class_projection_rules",
            )
            continue
        matrix_rule = rule_by_class[surface_class]
        for registry_key, matrix_key in FIELD_KEY_MAP.items():
            registry_value = registry_entry.get(registry_key)
            if registry_value is None:
                continue
            if matrix_rule.get(matrix_key) != registry_value:
                add_finding(
                    findings,
                    f"matrix.class_projection_rules:{surface_class}",
                    f"{matrix_key} must match registry.{registry_key}",
                )


def path_exists(relpath: str) -> bool:
    return (REPO_ROOT / relpath).exists()


def validate_chat_ci_projection_artifacts(findings: list[Finding]) -> None:
    for relpath in (CHAT_CI_PROVIDER_PROFILES_PATH, CHAT_CI_PROJECTION_PACK_PATH):
        payload = read_json_dict(REPO_ROOT / relpath, findings, relpath)
        governance = payload.get("projection_governance")
        if not isinstance(governance, dict):
            add_finding(findings, relpath, "projection_governance must be a top-level object")
            continue
        for field, expected in EXPECTED_CHAT_CI_GOVERNANCE.items():
            if governance.get(field) != expected:
                add_finding(
                    findings,
                    f"{relpath}:{field}",
                    "projection_governance must follow the shared projection sovereignty contract",
                )

    provider_profiles = read_json_dict(REPO_ROOT / CHAT_CI_PROVIDER_PROFILES_PATH, findings, CHAT_CI_PROVIDER_PROFILES_PATH)
    global_constraints = provider_profiles.get("global_constraints")
    if not isinstance(global_constraints, dict):
        add_finding(
            findings,
            CHAT_CI_PROVIDER_PROFILES_PATH,
            "global_constraints must be a top-level object",
        )
    elif global_constraints.get("manual_export_only") is not True:
        add_finding(
            findings,
            f"{CHAT_CI_PROVIDER_PROFILES_PATH}:global_constraints.manual_export_only",
            "chat_ci provider profiles must stay manual_export_only",
        )

    pack = read_json_dict(REPO_ROOT / CHAT_CI_PROJECTION_PACK_PATH, findings, CHAT_CI_PROJECTION_PACK_PATH)
    provider_pack_rows = pack.get("provider_pack_rows")
    if not isinstance(provider_pack_rows, list):
        add_finding(
            findings,
            CHAT_CI_PROJECTION_PACK_PATH,
            "provider_pack_rows must be a list",
        )
        return
    for index, row in enumerate(provider_pack_rows):
        if not isinstance(row, dict):
            add_finding(
                findings,
                f"{CHAT_CI_PROJECTION_PACK_PATH}:provider_pack_rows[{index}]",
                "provider_pack_rows entries must be objects",
            )
            continue
        if row.get("state") != "projection_ready_manual_export_only":
            add_finding(
                findings,
                f"{CHAT_CI_PROJECTION_PACK_PATH}:provider_pack_rows[{index}].state",
                "chat_ci projection-pack rows must remain projection_ready_manual_export_only",
            )


def validate_concrete_surfaces(
    registry: dict[str, Any],
    matrix: dict[str, Any],
    findings: list[Finding],
) -> tuple[int, int]:
    concrete_surfaces = ensure_list_of_dicts(registry, "concrete_surfaces", findings, "registry.concrete_surfaces")
    matrix_rows = ensure_list_of_dicts(matrix, "surface_projection_rows", findings, "matrix.surface_projection_rows")
    class_rules = ensure_list_of_dicts(matrix, "class_projection_rules", findings, "matrix.class_projection_rules")

    registry_by_id: dict[str, dict[str, Any]] = {}
    registry_paths: set[str] = set()
    for index, entry in enumerate(concrete_surfaces):
        surface_id = entry.get("surface_id")
        path = entry.get("path")
        surface_class = entry.get("surface_class")
        if not isinstance(surface_id, str) or not surface_id:
            add_finding(findings, f"registry.concrete_surfaces:{index}", "surface_id must be a non-empty string")
            continue
        if surface_id in registry_by_id:
            add_finding(findings, f"registry.concrete_surfaces:{index}", f"duplicate surface_id {surface_id!r}")
            continue
        if not isinstance(path, str) or not path:
            add_finding(findings, f"registry.concrete_surfaces:{surface_id}", "path must be a non-empty string")
            continue
        if not isinstance(surface_class, str) or not surface_class:
            add_finding(findings, f"registry.concrete_surfaces:{surface_id}", "surface_class must be a non-empty string")
            continue
        registry_by_id[surface_id] = entry
        registry_paths.add(path)
        if not path_exists(path):
            add_finding(findings, f"registry.concrete_surfaces:{surface_id}", f"missing referenced path {path!r}")
        for ref_key in ("validator_refs", "renderer_refs"):
            refs = entry.get(ref_key)
            if refs is None:
                continue
            if not isinstance(refs, list):
                add_finding(findings, f"registry.concrete_surfaces:{surface_id}", f"{ref_key} must be a list")
                continue
            for ref_index, ref in enumerate(refs):
                if not isinstance(ref, str) or not ref:
                    add_finding(
                        findings,
                        f"registry.concrete_surfaces:{surface_id}:{ref_key}[{ref_index}]",
                        "reference must be a non-empty string",
                    )
                    continue
                if not path_exists(ref):
                    add_finding(
                        findings,
                        f"registry.concrete_surfaces:{surface_id}:{ref_key}[{ref_index}]",
                        f"missing referenced path {ref!r}",
                    )

    matrix_by_id: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(matrix_rows):
        surface_id = row.get("surface_id")
        path = row.get("path")
        surface_class = row.get("surface_class")
        if not isinstance(surface_id, str) or not surface_id:
            add_finding(findings, f"matrix.surface_projection_rows:{index}", "surface_id must be a non-empty string")
            continue
        if surface_id in matrix_by_id:
            add_finding(findings, f"matrix.surface_projection_rows:{index}", f"duplicate surface_id {surface_id!r}")
            continue
        matrix_by_id[surface_id] = row
        registry_entry = registry_by_id.get(surface_id)
        if registry_entry is None:
            add_finding(findings, f"matrix.surface_projection_rows:{surface_id}", "surface_id missing from registry.concrete_surfaces")
            continue
        if row.get("path") != registry_entry.get("path"):
            add_finding(findings, f"matrix.surface_projection_rows:{surface_id}", "path must match registry.concrete_surfaces")
        if row.get("surface_class") != registry_entry.get("surface_class"):
            add_finding(
                findings,
                f"matrix.surface_projection_rows:{surface_id}",
                "surface_class must match registry.concrete_surfaces",
            )
        if not isinstance(path, str) or not path_exists(path):
            add_finding(findings, f"matrix.surface_projection_rows:{surface_id}", f"missing referenced path {path!r}")
        if not isinstance(surface_class, str) or not surface_class:
            add_finding(findings, f"matrix.surface_projection_rows:{surface_id}", "surface_class must be a non-empty string")

    for surface_id in registry_by_id:
        if surface_id not in matrix_by_id:
            add_finding(findings, f"registry.concrete_surfaces:{surface_id}", "surface missing from matrix.surface_projection_rows")

    for index, rule in enumerate(class_rules):
        surface_class = rule.get("surface_class")
        scope = f"matrix.class_projection_rules:{index}"
        concrete_ids = ensure_string_list(rule, "concrete_surface_ids", findings, scope)
        for concrete_id in concrete_ids:
            registry_entry = registry_by_id.get(concrete_id)
            matrix_entry = matrix_by_id.get(concrete_id)
            if registry_entry is None:
                add_finding(findings, scope, f"unknown concrete_surface_id {concrete_id!r}")
                continue
            if matrix_entry is None:
                add_finding(findings, scope, f"concrete_surface_id {concrete_id!r} missing from surface_projection_rows")
                continue
            if registry_entry.get("surface_class") != surface_class:
                add_finding(findings, scope, f"{concrete_id} must carry surface_class {surface_class!r} in registry")

    required_paths = {
        repo_rel(DEFAULT_REGISTRY),
        repo_rel(DEFAULT_MATRIX),
        EXPECTED_LEDGER_PATH,
        EXPECTED_VALIDATOR_PATH,
        EXPECTED_REMATERIALIZER_PATH,
    }
    missing_required = sorted(required_paths - registry_paths)
    for required_path in missing_required:
        add_finding(
            findings,
            "registry.concrete_surfaces",
            f"config-surface seed must explicitly register {required_path}",
        )

    return len(registry_by_id), len(matrix_by_id)


def parse_ledger(path: Path, findings: list[Finding]) -> list[dict[str, Any]]:
    if not path.exists():
        add_finding(findings, "ledger", f"missing file: {repo_rel(path)}")
        return []

    events: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    previous_timestamp: str | None = None
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            add_finding(findings, f"ledger:{line_number}", f"invalid JSON line: {exc}")
            continue
        if not isinstance(event, dict):
            add_finding(findings, f"ledger:{line_number}", "ledger line must be a JSON object")
            continue

        event_id = event.get("event_id")
        event_type = event.get("event_type")
        recorded_at = event.get("recorded_at")
        family_id = event.get("family_id")
        registry_path = event.get("registry_path")
        matrix_path = event.get("projection_matrix_path")
        registry_sha = event.get("registry_sha256")
        matrix_sha = event.get("projection_matrix_sha256")
        combined_sha = event.get("joint_sha256")

        if not isinstance(event_id, str) or not EVENT_ID_RE.fullmatch(event_id):
            add_finding(findings, f"ledger:{line_number}", "event_id must match csl-YYYYMMDD-NNNN")
        elif event_id in seen_ids:
            add_finding(findings, f"ledger:{line_number}", f"duplicate event_id {event_id!r}")
        else:
            seen_ids.add(event_id)

        if not isinstance(event_type, str) or event_type not in EXPECTED_EVENT_TYPES:
            add_finding(findings, f"ledger:{line_number}", f"event_type must be one of {sorted(EXPECTED_EVENT_TYPES)}")

        if not isinstance(recorded_at, str) or not TIMESTAMP_RE.fullmatch(recorded_at):
            add_finding(findings, f"ledger:{line_number}", "recorded_at must be ISO-8601 UTC with trailing Z")
        elif previous_timestamp is not None and recorded_at < previous_timestamp:
            add_finding(findings, f"ledger:{line_number}", "ledger timestamps must be non-decreasing")
        else:
            previous_timestamp = recorded_at

        if family_id != EXPECTED_LEDGER_FAMILY:
            add_finding(findings, f"ledger:{line_number}", f"family_id must be {EXPECTED_LEDGER_FAMILY!r}")
        if registry_path != repo_rel(DEFAULT_REGISTRY):
            add_finding(findings, f"ledger:{line_number}", "registry_path must point to CONFIG-SURFACE-REGISTRY-v1.json")
        if matrix_path != repo_rel(DEFAULT_MATRIX):
            add_finding(
                findings,
                f"ledger:{line_number}",
                "projection_matrix_path must point to CONFIG-SURFACE-PROJECTION-MATRIX-v1.json",
            )
        for field_name, value in (
            ("registry_sha256", registry_sha),
            ("projection_matrix_sha256", matrix_sha),
            ("joint_sha256", combined_sha),
        ):
            if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
                add_finding(findings, f"ledger:{line_number}", f"{field_name} must be a sha256:... digest")

        if isinstance(registry_sha, str) and isinstance(matrix_sha, str) and isinstance(combined_sha, str):
            expected_joint = joint_sha256(registry_sha, matrix_sha)
            if combined_sha != expected_joint:
                add_finding(findings, f"ledger:{line_number}", "joint_sha256 must be derived from registry and matrix digests")

        events.append(event)

    return events


def validate_ledger_alignment(
    events: list[dict[str, Any]],
    registry_sha256: str,
    matrix_sha256: str,
    findings: list[Finding],
) -> tuple[str, str | None]:
    if not events:
        add_finding(findings, "ledger", "ledger must contain at least one receipt event for the seed baseline")
        return "missing_receipt", None

    latest = events[-1]
    latest_id = latest.get("event_id") if isinstance(latest.get("event_id"), str) else None
    expected_joint = joint_sha256(registry_sha256, matrix_sha256)
    if latest.get("registry_sha256") != registry_sha256:
        add_finding(findings, "ledger.latest", "latest receipt does not match the current registry digest")
        return "drift_detected", latest_id
    if latest.get("projection_matrix_sha256") != matrix_sha256:
        add_finding(findings, "ledger.latest", "latest receipt does not match the current projection matrix digest")
        return "drift_detected", latest_id
    if latest.get("joint_sha256") != expected_joint:
        add_finding(findings, "ledger.latest", "latest receipt does not match the current joint digest")
        return "drift_detected", latest_id
    return "current_matches_latest_receipt", latest_id


def validate_rematerialization(
    ledger_path: Path,
    registry: dict[str, Any],
    matrix: dict[str, Any],
    findings: list[Finding],
) -> tuple[str, str | None]:
    try:
        materialized_state = rematerialize_config_surface_state(load_rematerialization_events(ledger_path))
    except ValueError as exc:
        for message in str(exc).splitlines():
            add_finding(findings, "rematerialization", message)
        return "missing_or_invalid_materialization", None

    if canonical_json_bytes(materialized_state.registry) != canonical_json_bytes(registry):
        add_finding(
            findings,
            "rematerialization.registry",
            "rematerialized registry does not match the committed CONFIG-SURFACE-REGISTRY-v1.json payload",
        )
        return "rebuild_mismatch", materialized_state.event_id

    if canonical_json_bytes(materialized_state.projection_matrix) != canonical_json_bytes(matrix):
        add_finding(
            findings,
            "rematerialization.projection_matrix",
            "rematerialized projection matrix does not match the committed CONFIG-SURFACE-PROJECTION-MATRIX-v1.json payload",
        )
        return "rebuild_mismatch", materialized_state.event_id

    return "rebuild_matches_latest_materialization", materialized_state.event_id


def write_reports(
    *,
    registry_path: Path,
    matrix_path: Path,
    ledger_path: Path,
    registry: dict[str, Any],
    matrix: dict[str, Any],
    events: list[dict[str, Any]],
    registry_sha256: str,
    matrix_sha256: str,
    alignment_status: str,
    latest_receipt_event_id: str | None,
    rematerialization_status: str,
    latest_materialization_event_id: str | None,
    findings: list[Finding],
    md_report: Path,
    json_report: Path,
) -> None:
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    status = "PASS" if not findings else "FAIL"
    summary = {
        "generated_at": generated_at,
        "status": status,
        "registry": repo_rel(registry_path),
        "projection_matrix": repo_rel(matrix_path),
        "ledger": repo_rel(ledger_path),
        "registry_id": registry.get("registry_id"),
        "matrix_id": matrix.get("matrix_id"),
        "atom_families": len(registry.get("atom_families", [])) if isinstance(registry.get("atom_families"), list) else 0,
        "surface_classes": len(registry.get("surface_classes", []))
        if isinstance(registry.get("surface_classes"), list)
        else 0,
        "concrete_surfaces": len(registry.get("concrete_surfaces", []))
        if isinstance(registry.get("concrete_surfaces"), list)
        else 0,
        "class_projection_rules": len(matrix.get("class_projection_rules", []))
        if isinstance(matrix.get("class_projection_rules"), list)
        else 0,
        "surface_projection_rows": len(matrix.get("surface_projection_rows", []))
        if isinstance(matrix.get("surface_projection_rows"), list)
        else 0,
        "receipt_events": len(events),
        "latest_receipt_event_id": latest_receipt_event_id,
        "alignment_status": alignment_status,
        "latest_materialization_event_id": latest_materialization_event_id,
        "rematerialization_status": rematerialization_status,
        "registry_sha256": registry_sha256,
        "projection_matrix_sha256": matrix_sha256,
        "findings": len(findings),
    }
    payload = {"summary": summary, "findings": [asdict(finding) for finding in findings]}
    json_report.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    lines = [
        "# Config-Surface State Validation Report",
        "",
        "Report-only validation of config-surface structure, projection joins, required self-registration, receipt-ledger alignment, and rematerialization parity.",
        "",
        "## Summary",
        "",
        f"- registry: `{summary['registry']}`",
        f"- projection matrix: `{summary['projection_matrix']}`",
        f"- ledger: `{summary['ledger']}`",
        f"- atom families: {summary['atom_families']}",
        f"- surface classes: {summary['surface_classes']}",
        f"- concrete surfaces: {summary['concrete_surfaces']}",
        f"- class projection rules: {summary['class_projection_rules']}",
        f"- surface projection rows: {summary['surface_projection_rows']}",
        f"- receipt events: {summary['receipt_events']}",
        f"- latest receipt event: `{latest_receipt_event_id or 'none'}`",
        f"- alignment status: `{alignment_status}`",
        f"- latest materialization event: `{latest_materialization_event_id or 'none'}`",
        f"- rematerialization status: `{rematerialization_status}`",
        f"- findings: {summary['findings']}",
        f"- status: `{status}`",
        "",
        "## Findings",
        "",
    ]
    if not findings:
        lines.append("- none")
    else:
        for finding in findings:
            lines.append(f"- [{finding.level}] `{finding.scope}`: {finding.message}")
    md_report.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--projection-matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--md-report", type=Path, default=DEFAULT_MD_REPORT)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON_REPORT)
    args = parser.parse_args()

    findings: list[Finding] = []
    registry = read_json_dict(args.registry, findings, "registry")
    matrix = read_json_dict(args.projection_matrix, findings, "projection_matrix")

    if registry.get("registry_id") != EXPECTED_REGISTRY_ID:
        add_finding(findings, "registry.registry_id", f"registry_id must be {EXPECTED_REGISTRY_ID!r}")
    if matrix.get("matrix_id") != EXPECTED_MATRIX_ID:
        add_finding(findings, "projection_matrix.matrix_id", f"matrix_id must be {EXPECTED_MATRIX_ID!r}")
    if matrix.get("registry_ref") != repo_rel(args.registry):
        add_finding(findings, "projection_matrix.registry_ref", "registry_ref must point to CONFIG-SURFACE-REGISTRY-v1.json")

    validate_atom_families(registry, matrix, findings)
    validate_surface_classes(registry, matrix, findings)
    validate_concrete_surfaces(registry, matrix, findings)
    validate_chat_ci_projection_artifacts(findings)

    registry_sha256 = sha256_for_file(args.registry) if args.registry.exists() else "sha256:" + "0" * 64
    matrix_sha256 = sha256_for_file(args.projection_matrix) if args.projection_matrix.exists() else "sha256:" + "0" * 64
    events = parse_ledger(args.ledger, findings)
    alignment_status, latest_receipt_event_id = validate_ledger_alignment(events, registry_sha256, matrix_sha256, findings)
    rematerialization_status, latest_materialization_event_id = validate_rematerialization(
        args.ledger,
        registry,
        matrix,
        findings,
    )

    args.md_report.parent.mkdir(parents=True, exist_ok=True)
    args.json_report.parent.mkdir(parents=True, exist_ok=True)
    write_reports(
        registry_path=args.registry,
        matrix_path=args.projection_matrix,
        ledger_path=args.ledger,
        registry=registry,
        matrix=matrix,
        events=events,
        registry_sha256=registry_sha256,
        matrix_sha256=matrix_sha256,
        alignment_status=alignment_status,
        latest_receipt_event_id=latest_receipt_event_id,
        rematerialization_status=rematerialization_status,
        latest_materialization_event_id=latest_materialization_event_id,
        findings=findings,
        md_report=args.md_report,
        json_report=args.json_report,
    )

    print(args.md_report)
    print(args.json_report)
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())

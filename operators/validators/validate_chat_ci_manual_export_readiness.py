#!/usr/bin/env python3
"""Report-only validator for the chat_ci manual-export readiness family."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = REPO_ROOT / "orchestration" / "state"

DEFAULT_READINESS = REPO_ROOT / "orchestration" / "state" / "registry" / "CHAT-CI-MANUAL-EXPORT-READINESS-v1.json"
DEFAULT_PROFILES = REPO_ROOT / "orchestration" / "state" / "registry" / "CHAT-CI-PROVIDER-PROFILES-v1.json"
DEFAULT_PACK = REPO_ROOT / "orchestration" / "state" / "registry" / "CHAT-CI-PROJECTION-PACK-v1.json"
DEFAULT_LEDGER = REPO_ROOT / "orchestration" / "state" / "registry" / "chat-ci-manual-export-ledger.jsonl"
DEFAULT_CONFIG_REGISTRY = REPO_ROOT / "orchestration" / "state" / "registry" / "CONFIG-SURFACE-REGISTRY-v1.json"
DEFAULT_CONFIG_MATRIX = REPO_ROOT / "orchestration" / "state" / "registry" / "CONFIG-SURFACE-PROJECTION-MATRIX-v1.json"
DEFAULT_CONFIG_LEDGER = REPO_ROOT / "orchestration" / "state" / "registry" / "config-surface-state-ledger.jsonl"
DEFAULT_MD_REPORT = STATE_DIR / "CHAT-CI-MANUAL-EXPORT-READINESS-REPORT.md"
DEFAULT_JSON_REPORT = STATE_DIR / "CHAT-CI-MANUAL-EXPORT-READINESS-REPORT.json"

EXPECTED_READINESS_ID = "chat-ci-manual-export-readiness-v1"
EXPECTED_SURFACE_CLASS = "chat_ci"
EXPECTED_STATUS = "manual_export_ready"
EXPECTED_LEDGER_FAMILY = "chat_ci_manual_export_state"
EXPECTED_READINESS_PATH = "orchestration/state/registry/CHAT-CI-MANUAL-EXPORT-READINESS-v1.json"
EXPECTED_PROFILES_PATH = "orchestration/state/registry/CHAT-CI-PROVIDER-PROFILES-v1.json"
EXPECTED_PACK_PATH = "orchestration/state/registry/CHAT-CI-PROJECTION-PACK-v1.json"
EXPECTED_CONFIG_REGISTRY_PATH = "orchestration/state/registry/CONFIG-SURFACE-REGISTRY-v1.json"
EXPECTED_CONFIG_MATRIX_PATH = "orchestration/state/registry/CONFIG-SURFACE-PROJECTION-MATRIX-v1.json"
EXPECTED_CONFIG_LEDGER_PATH = "orchestration/state/registry/config-surface-state-ledger.jsonl"
EXPECTED_VALIDATOR_PATH = "operators/validators/validate_chat_ci_manual_export_readiness.py"
SHARED_PROJECTION_CONTRACT_PATH = "orchestration/state/impl/PROJECTION-FAMILY-SOVEREIGNTY-NORMALIZATION-v1.md"
EXPECTED_PROJECTION_GOVERNANCE = {
    "shared_contract_path": SHARED_PROJECTION_CONTRACT_PATH,
    "sovereignty_rule": "repo_ratifies_exocortex_coordinates_projection_derives",
    "capture_policy": "manual_export_only",
    "reliance_ceiling": "informative_only_until_receipted_export",
    "hidden_second_control_plane": "prohibited",
}
EXPECTED_EVENT_TYPES = {
    "readiness_receipt",
    "readiness_refresh",
    "manual_export_receipt",
    "supersession_receipt",
}
EVENT_ID_RE = re.compile(r"^cmer-\d{8}-\d{4}$")
TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


@dataclass(frozen=True)
class Finding:
    level: str
    scope: str
    message: str


def add_finding(findings: list[Finding], scope: str, message: str, *, level: str = "error") -> None:
    findings.append(Finding(level=level, scope=scope, message=message))


def repo_rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def path_exists(relpath: str) -> bool:
    return (REPO_ROOT / relpath).exists()


def canonical_json_bytes(payload: Any) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def sha256_for_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return f"sha256:{digest.hexdigest()}"


def joint_sha256(*digests: str) -> str:
    digest = hashlib.sha256()
    digest.update(("".join(f"{item}\n" for item in digests)).encode("utf-8"))
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
    mapping: dict[str, Any],
    key: str,
    findings: list[Finding],
    scope: str,
) -> list[dict[str, Any]]:
    value = mapping.get(key)
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


def validate_projection_governance(mapping: dict[str, Any], scope: str, findings: list[Finding]) -> None:
    governance = mapping.get("projection_governance")
    if not isinstance(governance, dict):
        add_finding(findings, scope, "projection_governance must be an object")
        return
    for field, expected in EXPECTED_PROJECTION_GOVERNANCE.items():
        if governance.get(field) != expected:
            add_finding(
                findings,
                f"{scope}.{field}",
                "projection_governance must follow the shared projection sovereignty contract",
            )


def validate_source_bindings(readiness: dict[str, Any], findings: list[Finding]) -> None:
    source_bindings = readiness.get("source_bindings")
    if not isinstance(source_bindings, dict):
        add_finding(findings, "readiness.source_bindings", "source_bindings must be an object")
        return
    for key in ("contract", "config_current_state", "chat_ci_derivatives", "sigma_refs"):
        refs = ensure_string_list(source_bindings, key, findings, f"readiness.source_bindings.{key}")
        for ref in refs:
            if not path_exists(ref):
                add_finding(findings, f"readiness.source_bindings.{key}", f"missing referenced path {ref!r}")


def validate_readiness(
    readiness: dict[str, Any],
    profiles: dict[str, Any],
    pack: dict[str, Any],
    latest_config_event: dict[str, Any] | None,
    findings: list[Finding],
) -> list[str]:
    if readiness.get("readiness_id") != EXPECTED_READINESS_ID:
        add_finding(findings, "readiness.readiness_id", f"readiness_id must be {EXPECTED_READINESS_ID!r}")
    if readiness.get("surface_class") != EXPECTED_SURFACE_CLASS:
        add_finding(findings, "readiness.surface_class", f"surface_class must be {EXPECTED_SURFACE_CLASS!r}")
    if readiness.get("status") != EXPECTED_STATUS:
        add_finding(findings, "readiness.status", f"status must be {EXPECTED_STATUS!r}")

    validate_projection_governance(readiness, "readiness.projection_governance", findings)
    validate_source_bindings(readiness, findings)

    constraints = readiness.get("manual_export_constraints")
    if not isinstance(constraints, dict):
        add_finding(findings, "readiness.manual_export_constraints", "manual_export_constraints must be an object")
    else:
        expected_false = {
            "provider_runtime_writes_allowed",
            "automation_allowed",
            "hidden_control_plane_allowed",
        }
        expected_true = {"repo_sovereign", "manual_export_only", "receipt_required_before_reliance"}
        for key in expected_true:
            if constraints.get(key) is not True:
                add_finding(findings, f"readiness.manual_export_constraints.{key}", f"{key} must be true")
        for key in expected_false:
            if constraints.get(key) is not False:
                add_finding(findings, f"readiness.manual_export_constraints.{key}", f"{key} must be false")

    proof_binding = readiness.get("config_proof_binding")
    if not isinstance(proof_binding, dict):
        add_finding(findings, "readiness.config_proof_binding", "config_proof_binding must be an object")
    else:
        if proof_binding.get("family_id") != "config_surface_state":
            add_finding(findings, "readiness.config_proof_binding.family_id", "family_id must be 'config_surface_state'")
        if proof_binding.get("registry_path") != EXPECTED_CONFIG_REGISTRY_PATH:
            add_finding(
                findings,
                "readiness.config_proof_binding.registry_path",
                "registry_path must point to CONFIG-SURFACE-REGISTRY-v1.json",
            )
        if proof_binding.get("projection_matrix_path") != EXPECTED_CONFIG_MATRIX_PATH:
            add_finding(
                findings,
                "readiness.config_proof_binding.projection_matrix_path",
                "projection_matrix_path must point to CONFIG-SURFACE-PROJECTION-MATRIX-v1.json",
            )
        if latest_config_event is not None:
            if proof_binding.get("latest_receipt_event_id") != latest_config_event.get("event_id"):
                add_finding(
                    findings,
                    "readiness.config_proof_binding.latest_receipt_event_id",
                    "latest_receipt_event_id must match the latest config-surface ledger event",
                )
            if proof_binding.get("config_state_version") != latest_config_event.get("config_state_version"):
                add_finding(
                    findings,
                    "readiness.config_proof_binding.config_state_version",
                    "config_state_version must match the latest config-surface materialization event",
                )

    readiness_rows = ensure_list_of_dicts(readiness, "provider_readiness", findings, "readiness.provider_readiness")
    profile_rows = ensure_list_of_dicts(profiles, "provider_profiles", findings, "profiles.provider_profiles")
    pack_rows = ensure_list_of_dicts(pack, "provider_pack_rows", findings, "pack.provider_pack_rows")

    readiness_ids: list[str] = []
    for row in readiness_rows:
        provider_id = row.get("provider_id")
        if not isinstance(provider_id, str) or not provider_id:
            add_finding(findings, "readiness.provider_readiness", "provider_id must be a non-empty string")
            continue
        readiness_ids.append(provider_id)
        if row.get("readiness_state") != EXPECTED_STATUS:
            add_finding(
                findings,
                f"readiness.provider_readiness.{provider_id}",
                f"readiness_state must be {EXPECTED_STATUS!r}",
            )
        if row.get("pack_state") != "projection_ready_manual_export_only":
            add_finding(
                findings,
                f"readiness.provider_readiness.{provider_id}",
                "pack_state must be 'projection_ready_manual_export_only'",
            )

    profile_ids = [row.get("provider_id") for row in profile_rows if isinstance(row.get("provider_id"), str)]
    pack_ids = [row.get("provider_id") for row in pack_rows if isinstance(row.get("provider_id"), str)]

    if set(readiness_ids) != set(profile_ids):
        add_finding(findings, "provider_sets", "provider_readiness ids must match provider_profiles ids")
    if set(readiness_ids) != set(pack_ids):
        add_finding(findings, "provider_sets", "provider_readiness ids must match projection pack provider ids")

    return sorted(set(readiness_ids))


def validate_profiles_and_pack(profiles: dict[str, Any], pack: dict[str, Any], findings: list[Finding]) -> None:
    validate_projection_governance(profiles, "profiles.projection_governance", findings)
    validate_projection_governance(pack, "pack.projection_governance", findings)

    constraints = profiles.get("global_constraints")
    if not isinstance(constraints, dict):
        add_finding(findings, "profiles.global_constraints", "global_constraints must be an object")
    else:
        if constraints.get("manual_export_only") is not True:
            add_finding(findings, "profiles.global_constraints.manual_export_only", "manual_export_only must be true")
        if constraints.get("repo_resident_only") is not True:
            add_finding(findings, "profiles.global_constraints.repo_resident_only", "repo_resident_only must be true")

    for row in ensure_list_of_dicts(pack, "provider_pack_rows", findings, "pack.provider_pack_rows"):
        provider_id = row.get("provider_id", "<unknown>")
        if row.get("state") != "projection_ready_manual_export_only":
            add_finding(
                findings,
                f"pack.provider_pack_rows.{provider_id}",
                "state must be 'projection_ready_manual_export_only'",
            )


def validate_config_registration(registry: dict[str, Any], matrix: dict[str, Any], findings: list[Finding]) -> None:
    concrete_surfaces = ensure_list_of_dicts(registry, "concrete_surfaces", findings, "registry.concrete_surfaces")
    matrix_rows = ensure_list_of_dicts(matrix, "surface_projection_rows", findings, "matrix.surface_projection_rows")
    class_rules = ensure_list_of_dicts(matrix, "class_projection_rules", findings, "matrix.class_projection_rules")

    registry_by_path = {entry.get("path"): entry for entry in concrete_surfaces if isinstance(entry.get("path"), str)}
    matrix_by_path = {entry.get("path"): entry for entry in matrix_rows if isinstance(entry.get("path"), str)}
    required = {
        EXPECTED_READINESS_PATH: "chat_ci",
        "orchestration/state/registry/chat-ci-manual-export-ledger.jsonl": "ledger",
        EXPECTED_VALIDATOR_PATH: "hook_policy",
    }
    for path, surface_class in required.items():
        registry_entry = registry_by_path.get(path)
        matrix_entry = matrix_by_path.get(path)
        if registry_entry is None:
            add_finding(findings, "config_registration", f"config registry must register {path!r}")
            continue
        if registry_entry.get("surface_class") != surface_class:
            add_finding(findings, "config_registration", f"{path!r} must carry surface_class {surface_class!r}")
        if matrix_entry is None:
            add_finding(findings, "config_registration", f"config matrix must register {path!r}")
            continue
        if matrix_entry.get("surface_class") != surface_class:
            add_finding(findings, "config_registration", f"config matrix row for {path!r} must carry {surface_class!r}")

    rule_by_class = {entry.get("surface_class"): entry for entry in class_rules if isinstance(entry.get("surface_class"), str)}
    for surface_class, path in (
        ("chat_ci", EXPECTED_READINESS_PATH),
        ("ledger", "orchestration/state/registry/chat-ci-manual-export-ledger.jsonl"),
        ("hook_policy", EXPECTED_VALIDATOR_PATH),
    ):
        rule = rule_by_class.get(surface_class)
        if not isinstance(rule, dict):
            add_finding(findings, "config_registration", f"class_projection_rules must include {surface_class!r}")
            continue
        ids = rule.get("concrete_surface_ids")
        if not isinstance(ids, list):
            add_finding(findings, f"config_registration.{surface_class}", "concrete_surface_ids must be a list")
            continue
        registry_entry = registry_by_path.get(path)
        if registry_entry is not None and registry_entry.get("surface_id") not in ids:
            add_finding(findings, f"config_registration.{surface_class}", f"{path!r} must be listed in concrete_surface_ids")


def parse_jsonl(path: Path, findings: list[Finding], scope: str) -> list[dict[str, Any]]:
    if not path.exists():
        add_finding(findings, scope, f"missing file: {repo_rel(path)}")
        return []
    events: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            add_finding(findings, f"{scope}:{line_number}", f"invalid JSON line: {exc}")
            continue
        if not isinstance(event, dict):
            add_finding(findings, f"{scope}:{line_number}", "JSONL line must be an object")
            continue
        events.append(event)
    return events


def latest_materialized_config_event(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    materialized = [event for event in events if "effective_state" in event and "config_state_version" in event]
    if not materialized:
        return None
    materialized.sort(
        key=lambda event: (
            int(event.get("config_state_version", 0)),
            str(event.get("recorded_at", "")),
            str(event.get("event_id", "")),
        )
    )
    return materialized[-1]


def validate_readiness_ledger(
    readiness: dict[str, Any],
    events: list[dict[str, Any]],
    latest_config_event: dict[str, Any] | None,
    readiness_sha: str,
    profiles_sha: str,
    pack_sha: str,
    config_registry_sha: str,
    config_matrix_sha: str,
    findings: list[Finding],
) -> tuple[str, str | None]:
    if not events:
        add_finding(findings, "readiness_ledger", "ledger must contain at least one readiness receipt")
        return "missing_receipt", None

    seen_ids: set[str] = set()
    previous_timestamp: str | None = None
    for index, event in enumerate(events, start=1):
        event_id = event.get("event_id")
        event_type = event.get("event_type")
        recorded_at = event.get("recorded_at")
        if not isinstance(event_id, str) or not EVENT_ID_RE.fullmatch(event_id):
            add_finding(findings, f"readiness_ledger:{index}", "event_id must match cmer-YYYYMMDD-NNNN")
        elif event_id in seen_ids:
            add_finding(findings, f"readiness_ledger:{index}", f"duplicate event_id {event_id!r}")
        else:
            seen_ids.add(event_id)
        if not isinstance(event_type, str) or event_type not in EXPECTED_EVENT_TYPES:
            add_finding(findings, f"readiness_ledger:{index}", f"event_type must be one of {sorted(EXPECTED_EVENT_TYPES)}")
        if not isinstance(recorded_at, str) or not TIMESTAMP_RE.fullmatch(recorded_at):
            add_finding(findings, f"readiness_ledger:{index}", "recorded_at must be ISO-8601 UTC with trailing Z")
        elif previous_timestamp is not None and recorded_at < previous_timestamp:
            add_finding(findings, f"readiness_ledger:{index}", "ledger timestamps must be non-decreasing")
        else:
            previous_timestamp = recorded_at

    latest = events[-1]
    if latest.get("family_id") != EXPECTED_LEDGER_FAMILY:
        add_finding(findings, "readiness_ledger.latest", f"family_id must be {EXPECTED_LEDGER_FAMILY!r}")
    if latest.get("readiness_path") != EXPECTED_READINESS_PATH:
        add_finding(findings, "readiness_ledger.latest", "readiness_path must point to CHAT-CI-MANUAL-EXPORT-READINESS-v1.json")
    if latest.get("provider_profiles_path") != EXPECTED_PROFILES_PATH:
        add_finding(findings, "readiness_ledger.latest", "provider_profiles_path must point to CHAT-CI-PROVIDER-PROFILES-v1.json")
    if latest.get("projection_pack_path") != EXPECTED_PACK_PATH:
        add_finding(findings, "readiness_ledger.latest", "projection_pack_path must point to CHAT-CI-PROJECTION-PACK-v1.json")
    if latest.get("config_registry_path") != EXPECTED_CONFIG_REGISTRY_PATH:
        add_finding(findings, "readiness_ledger.latest", "config_registry_path must point to CONFIG-SURFACE-REGISTRY-v1.json")
    if latest.get("projection_matrix_path") != EXPECTED_CONFIG_MATRIX_PATH:
        add_finding(findings, "readiness_ledger.latest", "projection_matrix_path must point to CONFIG-SURFACE-PROJECTION-MATRIX-v1.json")

    digest_fields = {
        "readiness_sha256": readiness_sha,
        "provider_profiles_sha256": profiles_sha,
        "projection_pack_sha256": pack_sha,
        "config_registry_sha256": config_registry_sha,
        "projection_matrix_sha256": config_matrix_sha,
    }
    for key, expected in digest_fields.items():
        value = latest.get(key)
        if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
            add_finding(findings, "readiness_ledger.latest", f"{key} must be a sha256 digest")
            continue
        if value != expected:
            add_finding(findings, "readiness_ledger.latest", f"{key} does not match current file digest")

    expected_joint = joint_sha256(
        readiness_sha,
        profiles_sha,
        pack_sha,
        config_registry_sha,
        config_matrix_sha,
    )
    if latest.get("joint_sha256") != expected_joint:
        add_finding(findings, "readiness_ledger.latest", "joint_sha256 does not match current artifact digests")

    if latest.get("effective_state") != readiness:
        add_finding(findings, "readiness_ledger.latest", "effective_state must match the committed readiness JSON payload")

    if latest_config_event is not None:
        if latest.get("config_state_event_id") != latest_config_event.get("event_id"):
            add_finding(findings, "readiness_ledger.latest", "config_state_event_id must match latest config-surface event")
        if latest.get("config_state_version") != latest_config_event.get("config_state_version"):
            add_finding(findings, "readiness_ledger.latest", "config_state_version must match latest config-surface version")

    summary = latest.get("provider_summary")
    if not isinstance(summary, dict):
        add_finding(findings, "readiness_ledger.latest", "provider_summary must be an object")
    else:
        if summary.get("providers") != len(readiness.get("provider_readiness", [])):
            add_finding(findings, "readiness_ledger.latest", "provider_summary.providers must match readiness provider count")

    return "current_matches_latest_receipt", latest.get("event_id") if isinstance(latest.get("event_id"), str) else None


def write_reports(
    *,
    readiness_path: Path,
    profiles_path: Path,
    pack_path: Path,
    ledger_path: Path,
    readiness: dict[str, Any],
    provider_ids: list[str],
    latest_config_event_id: str | None,
    latest_readiness_event_id: str | None,
    findings: list[Finding],
    md_report: Path,
    json_report: Path,
) -> None:
    status = "PASS" if not findings else "FAIL"
    payload = {
        "status": status,
        "readiness_path": repo_rel(readiness_path),
        "provider_profiles_path": repo_rel(profiles_path),
        "projection_pack_path": repo_rel(pack_path),
        "ledger_path": repo_rel(ledger_path),
        "providers": provider_ids,
        "provider_count": len(provider_ids),
        "latest_config_event_id": latest_config_event_id,
        "latest_readiness_event_id": latest_readiness_event_id,
        "findings": [asdict(finding) for finding in findings],
    }
    json_report.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    lines = [
        "# Chat-CI Manual Export Readiness Report",
        "",
        "Report-only validation of the repo-native chat_ci manual-export readiness family.",
        "",
        "## Summary",
        "",
        f"- readiness: `{repo_rel(readiness_path)}`",
        f"- provider profiles: `{repo_rel(profiles_path)}`",
        f"- projection pack: `{repo_rel(pack_path)}`",
        f"- ledger: `{repo_rel(ledger_path)}`",
        f"- providers: {len(provider_ids)}",
        f"- latest config receipt: `{latest_config_event_id or 'missing'}`",
        f"- latest readiness receipt: `{latest_readiness_event_id or 'missing'}`",
        f"- findings: {len(findings)}",
        f"- status: `{status}`",
        "",
        "## Findings",
        "",
    ]
    if findings:
        for finding in findings:
            lines.append(f"- `{finding.level}` `{finding.scope}`: {finding.message}")
    else:
        lines.append("- none")
    md_report.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--readiness", type=Path, default=DEFAULT_READINESS)
    parser.add_argument("--profiles", type=Path, default=DEFAULT_PROFILES)
    parser.add_argument("--pack", type=Path, default=DEFAULT_PACK)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--config-registry", type=Path, default=DEFAULT_CONFIG_REGISTRY)
    parser.add_argument("--config-matrix", type=Path, default=DEFAULT_CONFIG_MATRIX)
    parser.add_argument("--config-ledger", type=Path, default=DEFAULT_CONFIG_LEDGER)
    parser.add_argument("--md-report", type=Path, default=DEFAULT_MD_REPORT)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON_REPORT)
    args = parser.parse_args()

    findings: list[Finding] = []
    readiness = read_json_dict(args.readiness, findings, "readiness")
    profiles = read_json_dict(args.profiles, findings, "profiles")
    pack = read_json_dict(args.pack, findings, "pack")
    config_registry = read_json_dict(args.config_registry, findings, "config_registry")
    config_matrix = read_json_dict(args.config_matrix, findings, "config_matrix")

    config_events = parse_jsonl(args.config_ledger, findings, "config_ledger")
    latest_config_event = latest_materialized_config_event(config_events)
    provider_ids = validate_readiness(readiness, profiles, pack, latest_config_event, findings)
    validate_profiles_and_pack(profiles, pack, findings)
    validate_config_registration(config_registry, config_matrix, findings)

    readiness_events = parse_jsonl(args.ledger, findings, "readiness_ledger")
    latest_readiness_event_id: str | None = None
    if readiness and profiles and pack and config_registry and config_matrix:
        readiness_sha = sha256_for_file(args.readiness)
        profiles_sha = sha256_for_file(args.profiles)
        pack_sha = sha256_for_file(args.pack)
        config_registry_sha = sha256_for_file(args.config_registry)
        config_matrix_sha = sha256_for_file(args.config_matrix)
        _, latest_readiness_event_id = validate_readiness_ledger(
            readiness,
            readiness_events,
            latest_config_event,
            readiness_sha,
            profiles_sha,
            pack_sha,
            config_registry_sha,
            config_matrix_sha,
            findings,
        )

    args.md_report.parent.mkdir(parents=True, exist_ok=True)
    args.json_report.parent.mkdir(parents=True, exist_ok=True)
    write_reports(
        readiness_path=args.readiness,
        profiles_path=args.profiles,
        pack_path=args.pack,
        ledger_path=args.ledger,
        readiness=readiness,
        provider_ids=provider_ids,
        latest_config_event_id=latest_config_event.get("event_id") if isinstance(latest_config_event, dict) else None,
        latest_readiness_event_id=latest_readiness_event_id,
        findings=findings,
        md_report=args.md_report,
        json_report=args.json_report,
    )
    print(args.md_report)
    print(args.json_report)
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())

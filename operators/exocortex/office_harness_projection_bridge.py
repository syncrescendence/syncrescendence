#!/usr/bin/env python3
"""Build the first lawful office-harness exocortex projection from repo-native proof state."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent
DEFAULT_REGISTRY = REPO_ROOT / "orchestration" / "state" / "registry" / "office-harness-bindings.effective.json"
DEFAULT_SURFACE_REGISTRY = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-SURFACE-REGISTRY-CC90.json"
DEFAULT_TELEOLOGY_REGISTRY = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-TELEOLOGY-REGISTRY-CC90.json"
DEFAULT_CONTROL_PLANE_STATUS = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json"
DEFAULT_PROJECTION_JSON = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-OFFICE-HARNESS-PROJECTION-CC92.json"
DEFAULT_LEDGER = REPO_ROOT / "orchestration" / "state" / "registry" / "office-harness-exocortex-projection-ledger.jsonl"
DEFAULT_REPORT_JSON = REPO_ROOT / "orchestration" / "state" / "OFFICE-HARNESS-EXOCORTEX-PROJECTION-REPORT.json"
DEFAULT_REPORT_MD = REPO_ROOT / "orchestration" / "state" / "OFFICE-HARNESS-EXOCORTEX-PROJECTION-REPORT.md"
EVENT_BRIDGE_PATH = SCRIPT_DIR / "exocortex_event_bridge.py"
CONTRACT_PATH = "orchestration/state/impl/OFFICE-HARNESS-EXOCORTEX-PROJECTION-CONTRACT-v1.md"
SCOPE_ID = "persistent-runtime-openclaw-offices"
PROJECTION_FAMILY = "office_harness_exocortex_projection"
SCHEMA_VERSION = "office-harness-exocortex-projection/v1"
LEDGER_SCHEMA_VERSION = "office-harness-exocortex-projection-ledger-event/v1"
CONTROL_PLANE_PATH = "orchestration/state/EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json"
OFFICE_ORDER = ["commander", "adjudicator", "ajna", "cartographer", "psyche"]
PROVIDER_SURFACE_MAP = {
    "anthropic": "claude_anthropic_surface",
    "openai-codex": "chatgpt_openai_surface",
}
REQUIRED_ROW_FIELDS = [
    "office_id",
    "office_title",
    "primary_harness",
    "harness_family",
    "surface_class",
    "provider",
    "model",
    "machine",
    "account_ref",
    "binding_state",
    "contract_state",
    "validator_state",
    "authority_state",
    "metadata_path",
    "source_effective_registry_path",
    "projected_surface_slug",
    "projected_surface_service",
    "projected_surface_class",
    "projected_surface_ontology_entity_id",
    "projected_surface_proper_role",
    "projected_surface_anti_role",
    "control_plane_status_path",
    "control_plane_status_version",
    "projection_state",
    "allowed_reliance",
    "ratification_pointer",
    "ratified_by_artifact_path",
    "ratified_by_artifact_id",
    "ratified_at",
]
POINTER_FIELDS = [
    "ratification_pointer",
    "ratified_by_artifact_path",
    "ratified_by_artifact_id",
    "ratified_at",
]


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sha256_text(text: str) -> str:
    return f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"


def sha256_json(payload: Any) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256_text(canonical)


def sha256_file(path: Path) -> str:
    return sha256_text(path.read_text(encoding="utf-8"))


def repo_rel(path: Path) -> str:
    return str(path.resolve().relative_to(REPO_ROOT))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n", encoding="utf-8")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw_line.strip():
            continue
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"Invalid JSON in {repo_rel(path)} line {line_number}: {exc}") from exc
        if not isinstance(event, dict):
            raise SystemExit(f"Ledger line {line_number} in {repo_rel(path)} must be a JSON object")
        events.append(event)
    return events


def load_registry(path: Path) -> tuple[list[dict[str, Any]], str]:
    raw = path.read_text(encoding="utf-8")
    parsed = json.loads(raw)
    if not isinstance(parsed, list):
        raise SystemExit("Office-harness effective registry must be a top-level JSON array.")
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(parsed, start=1):
        if not isinstance(row, dict):
            raise SystemExit(f"Registry row {index} must be a JSON object.")
        rows.append(row)
    return rows, f"sha256:{hashlib.sha256(raw.encode('utf-8')).hexdigest()}"


def select_scope(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scoped = [
        row
        for row in rows
        if row.get("surface_class") == "persistent-runtime" and row.get("harness_family") == "openclaw"
    ]
    order = {office_id: index for index, office_id in enumerate(OFFICE_ORDER)}
    scoped.sort(key=lambda row: order.get(str(row.get("office_id")), len(order)))
    return scoped


def build_projection_row(
    *,
    row: dict[str, Any],
    surface_registry: dict[str, dict[str, Any]],
    teleology_registry: dict[str, dict[str, Any]],
    control_plane_status_version: str,
    source_effective_registry_path: str,
) -> dict[str, Any]:
    provider = str(row.get("provider") or "")
    projected_surface_slug = PROVIDER_SURFACE_MAP.get(provider)
    if projected_surface_slug is None:
        raise SystemExit(f"No ratified projected surface mapping exists for provider {provider!r}")
    surface_row = surface_registry.get(projected_surface_slug)
    if surface_row is None:
        raise SystemExit(f"Projected surface slug {projected_surface_slug!r} missing from surface registry")
    teleology_row = teleology_registry.get(projected_surface_slug)
    if teleology_row is None:
        raise SystemExit(f"Projected surface slug {projected_surface_slug!r} missing from teleology registry")

    is_operative = (
        row.get("binding_state") == "active"
        and row.get("contract_state") == "operative"
        and row.get("validator_state") == "clean"
        and row.get("authority_state") == "operative"
    )
    projection_state = "operative" if is_operative else "informative_only"

    return {
        "office_id": row.get("office_id"),
        "office_title": row.get("office_title"),
        "primary_harness": row.get("primary_harness"),
        "harness_family": row.get("harness_family"),
        "surface_class": row.get("surface_class"),
        "provider": provider,
        "model": row.get("model"),
        "machine": row.get("machine"),
        "account_ref": row.get("account_ref"),
        "binding_state": row.get("binding_state"),
        "contract_state": row.get("contract_state"),
        "validator_state": row.get("validator_state"),
        "authority_state": row.get("authority_state"),
        "metadata_path": row.get("metadata_path"),
        "source_effective_registry_path": source_effective_registry_path,
        "projected_surface_slug": projected_surface_slug,
        "projected_surface_service": surface_row.get("service"),
        "projected_surface_class": surface_row.get("class"),
        "projected_surface_ontology_entity_id": surface_row.get("ontology_entity_id"),
        "projected_surface_proper_role": teleology_row.get("proper_role"),
        "projected_surface_anti_role": teleology_row.get("anti_role"),
        "control_plane_status_path": CONTROL_PLANE_PATH,
        "control_plane_status_version": control_plane_status_version,
        "projection_state": projection_state,
        "allowed_reliance": projection_state,
        "ratification_pointer": row.get("ratification_pointer"),
        "ratified_by_artifact_path": row.get("ratified_by_artifact_path"),
        "ratified_by_artifact_id": row.get("ratified_by_artifact_id"),
        "ratified_at": row.get("ratified_at"),
    }


def build_projection(
    rows: list[dict[str, Any]],
    *,
    registry_path: Path,
    registry_sha256: str,
    surface_registry_path: Path,
    surface_registry: dict[str, dict[str, Any]],
    teleology_registry_path: Path,
    teleology_registry: dict[str, dict[str, Any]],
    control_plane_status_path: Path,
    control_plane_status: dict[str, Any],
) -> dict[str, Any]:
    source_effective_registry_path = repo_rel(registry_path)
    projection_rows = [
        build_projection_row(
            row=row,
            surface_registry=surface_registry,
            teleology_registry=teleology_registry,
            control_plane_status_version=str(control_plane_status.get("version") or "unknown"),
            source_effective_registry_path=source_effective_registry_path,
        )
        for row in select_scope(rows)
    ]
    return {
        "schema_version": SCHEMA_VERSION,
        "projection_family": PROJECTION_FAMILY,
        "projection_scope": SCOPE_ID,
        "projection_contract_path": CONTRACT_PATH,
        "source_effective_registry_path": source_effective_registry_path,
        "source_effective_registry_sha256": registry_sha256,
        "source_surface_registry_path": repo_rel(surface_registry_path),
        "source_teleology_registry_path": repo_rel(teleology_registry_path),
        "source_control_plane_status_path": repo_rel(control_plane_status_path),
        "rows": projection_rows,
    }


def build_report(
    *,
    rows: list[dict[str, Any]],
    projection: dict[str, Any],
    registry_path: Path,
    projection_path: Path,
    registry_sha256: str,
    surface_registry_path: Path,
    surface_registry: dict[str, dict[str, Any]],
    teleology_registry_path: Path,
    teleology_registry: dict[str, dict[str, Any]],
    control_plane_status_path: Path,
    control_plane_status_version: str,
) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    scoped_rows = select_scope(rows)
    source_by_office = {
        str(row.get("office_id")): row for row in scoped_rows if isinstance(row.get("office_id"), str)
    }

    for field, expected in {
        "schema_version": SCHEMA_VERSION,
        "projection_family": PROJECTION_FAMILY,
        "projection_scope": SCOPE_ID,
        "projection_contract_path": CONTRACT_PATH,
        "source_effective_registry_path": repo_rel(registry_path),
        "source_effective_registry_sha256": registry_sha256,
        "source_surface_registry_path": repo_rel(surface_registry_path),
        "source_teleology_registry_path": repo_rel(teleology_registry_path),
        "source_control_plane_status_path": repo_rel(control_plane_status_path),
    }.items():
        if projection.get(field) != expected:
            findings.append(
                {
                    "level": "error",
                    "scope": field,
                    "message": f"{field} must be `{expected}`",
                }
            )

    projected_rows = projection.get("rows", [])
    if not isinstance(projected_rows, list):
        findings.append({"level": "error", "scope": "rows", "message": "rows must be a list"})
        projected_rows = []

    projected_by_office: dict[str, dict[str, Any]] = {}
    for index, row in enumerate(projected_rows, start=1):
        if not isinstance(row, dict):
            findings.append(
                {
                    "level": "error",
                    "scope": f"rows:{index}",
                    "message": "projection row must be an object",
                }
            )
            continue
        office_id = row.get("office_id")
        if not isinstance(office_id, str) or not office_id:
            findings.append(
                {
                    "level": "error",
                    "scope": f"rows:{index}.office_id",
                    "message": "projection row must carry a non-empty office_id",
                }
            )
            continue
        if office_id in projected_by_office:
            findings.append(
                {
                    "level": "error",
                    "scope": f"rows:{index}.office_id",
                    "message": f"duplicate projected office_id {office_id!r}",
                }
            )
            continue
        projected_by_office[office_id] = row

    extra_offices = sorted(set(projected_by_office) - set(source_by_office))
    for office_id in extra_offices:
        findings.append(
            {
                "level": "error",
                "scope": f"rows:{office_id}",
                "message": "projection row is out of scope for the v1 contract",
            }
        )

    for office_id, source_row in source_by_office.items():
        projected_row = projected_by_office.get(office_id)
        if projected_row is None:
            findings.append(
                {
                    "level": "error",
                    "scope": f"rows:{office_id}",
                    "message": "scoped source office is missing from the projection",
                }
            )
            continue

        for field in REQUIRED_ROW_FIELDS:
            if field not in projected_row:
                findings.append(
                    {
                        "level": "error",
                        "scope": f"rows:{office_id}.{field}",
                        "message": "required field missing from projection row",
                    }
                )

        for field in [
            "office_id",
            "office_title",
            "primary_harness",
            "harness_family",
            "surface_class",
            "provider",
            "model",
            "machine",
            "account_ref",
            "binding_state",
            "contract_state",
            "validator_state",
            "authority_state",
            "metadata_path",
            "ratification_pointer",
            "ratified_by_artifact_path",
            "ratified_by_artifact_id",
            "ratified_at",
        ]:
            if projected_row.get(field) != source_row.get(field):
                findings.append(
                    {
                        "level": "error",
                        "scope": f"rows:{office_id}.{field}",
                        "message": "projection row drifted from the scoped source office-harness row",
                    }
                )

        if projected_row.get("source_effective_registry_path") != repo_rel(registry_path):
            findings.append(
                {
                    "level": "error",
                    "scope": f"rows:{office_id}.source_effective_registry_path",
                    "message": "source_effective_registry_path must point to the repo-native effective registry",
                }
            )

        projected_surface_slug = projected_row.get("projected_surface_slug")
        expected_slug = PROVIDER_SURFACE_MAP.get(str(source_row.get("provider") or ""))
        if projected_surface_slug != expected_slug:
            findings.append(
                {
                    "level": "error",
                    "scope": f"rows:{office_id}.projected_surface_slug",
                    "message": "projected surface slug must follow the ratified provider mapping",
                }
            )
            continue

        surface_row = surface_registry.get(expected_slug or "")
        teleology_row = teleology_registry.get(expected_slug or "")
        if surface_row is None or teleology_row is None:
            findings.append(
                {
                    "level": "error",
                    "scope": f"rows:{office_id}.projected_surface_slug",
                    "message": "projected surface slug must resolve in both CC90 registries",
                }
            )
            continue

        for field, expected in {
            "projected_surface_service": surface_row.get("service"),
            "projected_surface_class": surface_row.get("class"),
            "projected_surface_ontology_entity_id": surface_row.get("ontology_entity_id"),
            "projected_surface_proper_role": teleology_row.get("proper_role"),
            "projected_surface_anti_role": teleology_row.get("anti_role"),
            "control_plane_status_path": CONTROL_PLANE_PATH,
            "control_plane_status_version": control_plane_status_version,
        }.items():
            if projected_row.get(field) != expected:
                findings.append(
                    {
                        "level": "error",
                        "scope": f"rows:{office_id}.{field}",
                        "message": f"{field} does not match the joined contract source",
                    }
                )

        expected_projection_state = (
            "operative"
            if source_row.get("binding_state") == "active"
            and source_row.get("contract_state") == "operative"
            and source_row.get("validator_state") == "clean"
            and source_row.get("authority_state") == "operative"
            else "informative_only"
        )
        if projected_row.get("projection_state") != expected_projection_state:
            findings.append(
                {
                    "level": "error",
                    "scope": f"rows:{office_id}.projection_state",
                    "message": "projection_state must follow the derivative-only obligations in the contract",
                }
            )
        if projected_row.get("allowed_reliance") != expected_projection_state:
            findings.append(
                {
                    "level": "error",
                    "scope": f"rows:{office_id}.allowed_reliance",
                    "message": "allowed_reliance must match projection_state in v1",
                }
            )

    summary = {
        "source_registry_path": repo_rel(registry_path),
        "source_registry_sha256": registry_sha256,
        "projection_path": repo_rel(projection_path),
        "projection_sha256": sha256_json(projection),
        "projection_scope": SCOPE_ID,
        "scoped_source_record_count": len(source_by_office),
        "projection_record_count": len(projected_by_office),
        "projected_offices": [row.get("office_id") for row in projection.get("rows", []) if isinstance(row, dict)],
        "pointer_complete_record_count": sum(
            1
            for row in projected_by_office.values()
            if all(isinstance(row.get(field), str) and row.get(field) for field in POINTER_FIELDS)
        ),
        "operative_record_count": sum(1 for row in projected_by_office.values() if row.get("projection_state") == "operative"),
        "informative_only_record_count": sum(
            1 for row in projected_by_office.values() if row.get("projection_state") == "informative_only"
        ),
        "projection_state_counts": dict(
            sorted(Counter(str(row.get("projection_state", "unknown")) for row in projected_by_office.values()).items())
        ),
        "binding_state_counts": dict(
            sorted(Counter(str(row.get("binding_state", "unknown")) for row in projected_by_office.values()).items())
        ),
        "finding_count": len(findings),
        "status": "coherent" if not findings else "findings_present",
    }
    return {
        "schema_version": "office-harness-exocortex-projection-report/v1",
        "generated_at": utc_now(),
        "mode": "report-first",
        "summary": summary,
        "findings": findings,
    }


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Office-Harness Exocortex Projection Report",
        "",
        f"- generated_at: `{report['generated_at']}`",
        f"- status: `{summary['status']}`",
        f"- source registry: `{summary['source_registry_path']}`",
        f"- projection path: `{summary['projection_path']}`",
        f"- projection scope: `{summary['projection_scope']}`",
        f"- source registry sha256: `{summary['source_registry_sha256']}`",
        f"- projection sha256: `{summary['projection_sha256']}`",
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


def build_event_payload(report: dict[str, Any]) -> dict[str, Any]:
    summary = report["summary"]
    return {
        "projection_version": "v1",
        "projection_family": PROJECTION_FAMILY,
        "projection_scope": summary["projection_scope"],
        "projection_status": summary["status"],
        "projection_sha256": summary["projection_sha256"],
        "projection_record_count": summary["projection_record_count"],
        "projected_offices": summary["projected_offices"],
        "operative_record_count": summary["operative_record_count"],
        "informative_only_record_count": summary["informative_only_record_count"],
        "projection_state_counts": summary["projection_state_counts"],
        "binding_state_counts": summary["binding_state_counts"],
    }


def emit_projection_event(
    *,
    report: dict[str, Any],
    registry_path: Path,
    projection_path: Path,
    report_json_path: Path,
    report_md_path: Path,
) -> Path:
    exocortex = load_module(EVENT_BRIDGE_PATH, "exocortex_event_bridge")
    payload = build_event_payload(report)
    policy = exocortex.load_policy()
    repo_paths = exocortex.normalize_repo_paths(
        [
            repo_rel(registry_path),
            repo_rel(projection_path),
            repo_rel(report_json_path),
            repo_rel(report_md_path),
        ]
    )
    exocortex.validate_request(
        surface="exocortex",
        artifact_class="exocortex_office_harness_projection",
        durable_capture="summary_and_typed_record",
        payload=payload,
        policy=policy,
    )
    return exocortex.emit_event(
        source="system",
        surface="exocortex",
        artifact_class="exocortex_office_harness_projection",
        event_type="office_harness_exocortex_projection_snapshot",
        summary="Office-harness exocortex projection synchronized from repo-native proof state.",
        capture_level="summary",
        durable_capture="summary_and_typed_record",
        repo_paths=repo_paths,
        ontology_entities=["ExoEvent", "ConfigSnapshot"],
        payload=payload,
    )


def next_ledger_event_id(events: list[dict[str, Any]], recorded_at: str) -> str:
    date_part = recorded_at[:10].replace("-", "")
    return f"ohxp-{date_part}-{len(events) + 1:04d}"


def build_ledger_event(
    *,
    report: dict[str, Any],
    projection: dict[str, Any],
    projection_path: Path,
    surface_registry_path: Path,
    teleology_registry_path: Path,
    control_plane_status_path: Path,
    recorded_at: str,
    event_type: str,
    actor: str,
    event_id: str,
) -> dict[str, Any]:
    summary = report["summary"]
    return {
        "schema_version": LEDGER_SCHEMA_VERSION,
        "event_id": event_id,
        "event_type": event_type,
        "recorded_at": recorded_at,
        "actor": actor,
        "projection_family": PROJECTION_FAMILY,
        "projection_scope": summary["projection_scope"],
        "projection_contract_path": CONTRACT_PATH,
        "source_effective_registry_path": projection["source_effective_registry_path"],
        "source_effective_registry_sha256": projection["source_effective_registry_sha256"],
        "source_surface_registry_path": projection["source_surface_registry_path"],
        "source_surface_registry_sha256": sha256_file(surface_registry_path),
        "source_teleology_registry_path": projection["source_teleology_registry_path"],
        "source_teleology_registry_sha256": sha256_file(teleology_registry_path),
        "source_control_plane_status_path": projection["source_control_plane_status_path"],
        "source_control_plane_status_sha256": sha256_file(control_plane_status_path),
        "projection_path": repo_rel(projection_path),
        "projection_sha256": summary["projection_sha256"],
        "projection_record_count": summary["projection_record_count"],
        "projected_offices": summary["projected_offices"],
        "pointer_complete_record_count": summary["pointer_complete_record_count"],
        "operative_record_count": summary["operative_record_count"],
        "informative_only_record_count": summary["informative_only_record_count"],
        "projection_state_counts": summary["projection_state_counts"],
        "binding_state_counts": summary["binding_state_counts"],
        "notes": (
            "Initial append-only snapshot receipt for the first repo-native office-harness exocortex projection family."
            if event_type == "projection_seeded"
            else "Projection receipt refresh after a repo-native proof-state or projection snapshot change."
        ),
    }


def should_append_event(latest: dict[str, Any], current: dict[str, Any]) -> bool:
    for key in (
        "projection_family",
        "projection_scope",
        "projection_contract_path",
        "source_effective_registry_path",
        "source_effective_registry_sha256",
        "source_surface_registry_path",
        "source_surface_registry_sha256",
        "source_teleology_registry_path",
        "source_teleology_registry_sha256",
        "source_control_plane_status_path",
        "source_control_plane_status_sha256",
        "projection_path",
        "projection_sha256",
        "projection_record_count",
        "projected_offices",
        "pointer_complete_record_count",
        "operative_record_count",
        "informative_only_record_count",
        "projection_state_counts",
        "binding_state_counts",
    ):
        if latest.get(key) != current.get(key):
            return True
    return False


def append_projection_receipt(
    *,
    ledger_path: Path,
    report: dict[str, Any],
    projection: dict[str, Any],
    projection_path: Path,
    surface_registry_path: Path,
    teleology_registry_path: Path,
    control_plane_status_path: Path,
    actor: str,
) -> tuple[bool, str | None]:
    events = load_jsonl(ledger_path)
    recorded_at = utc_now()
    event_type = "projection_seeded" if not events else "projection_refresh"
    event_id = next_ledger_event_id(events, recorded_at)
    event = build_ledger_event(
        report=report,
        projection=projection,
        projection_path=projection_path,
        surface_registry_path=surface_registry_path,
        teleology_registry_path=teleology_registry_path,
        control_plane_status_path=control_plane_status_path,
        recorded_at=recorded_at,
        event_type=event_type,
        actor=actor,
        event_id=event_id,
    )
    if events and not should_append_event(events[-1], event):
        latest_event_id = events[-1].get("event_id")
        return False, latest_event_id if isinstance(latest_event_id, str) else None

    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, separators=(",", ":"), ensure_ascii=True) + "\n")
    return True, event_id


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--surface-registry", type=Path, default=DEFAULT_SURFACE_REGISTRY)
    parser.add_argument("--teleology-registry", type=Path, default=DEFAULT_TELEOLOGY_REGISTRY)
    parser.add_argument("--control-plane-status", type=Path, default=DEFAULT_CONTROL_PLANE_STATUS)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_PROJECTION_JSON)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--ledger-actor", default="office_harness_projection_bridge")
    parser.add_argument("--output-report-json", type=Path, default=DEFAULT_REPORT_JSON)
    parser.add_argument("--output-report-md", type=Path, default=DEFAULT_REPORT_MD)
    parser.add_argument("--emit-event", action="store_true")
    args = parser.parse_args()

    registry_path = args.registry.expanduser().resolve()
    surface_registry_path = args.surface_registry.expanduser().resolve()
    teleology_registry_path = args.teleology_registry.expanduser().resolve()
    control_plane_status_path = args.control_plane_status.expanduser().resolve()
    output_json = args.output_json.expanduser().resolve()
    ledger_path = args.ledger.expanduser().resolve()
    output_report_json = args.output_report_json.expanduser().resolve()
    output_report_md = args.output_report_md.expanduser().resolve()

    rows, registry_sha256 = load_registry(registry_path)
    surface_registry_doc = load_json(surface_registry_path)
    teleology_registry_doc = load_json(teleology_registry_path)
    control_plane_status = load_json(control_plane_status_path)
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

    projection = build_projection(
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
    report = build_report(
        rows=rows,
        projection=projection,
        registry_path=registry_path,
        projection_path=output_json,
        registry_sha256=registry_sha256,
        surface_registry_path=surface_registry_path,
        surface_registry=surface_registry,
        teleology_registry_path=teleology_registry_path,
        teleology_registry=teleology_registry,
        control_plane_status_path=control_plane_status_path,
        control_plane_status_version=str(control_plane_status.get("version") or "unknown"),
    )

    write_json(output_json, projection)
    write_json(output_report_json, report)
    output_report_md.parent.mkdir(parents=True, exist_ok=True)
    output_report_md.write_text(render_markdown(report), encoding="utf-8")
    append_projection_receipt(
        ledger_path=ledger_path,
        report=report,
        projection=projection,
        projection_path=output_json,
        surface_registry_path=surface_registry_path,
        teleology_registry_path=teleology_registry_path,
        control_plane_status_path=control_plane_status_path,
        actor=str(args.ledger_actor),
    )

    print(output_json)
    print(ledger_path)
    print(output_report_json)
    print(output_report_md)
    if args.emit_event:
        event_path = emit_projection_event(
            report=report,
            registry_path=registry_path,
            projection_path=output_json,
            report_json_path=output_report_json,
            report_md_path=output_report_md,
        )
        print(event_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

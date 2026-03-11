#!/usr/bin/env python3
"""Report-first audit for live-ledger domain register coherence."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = REPO_ROOT / "orchestration" / "state"
REGISTER_PATH = REPO_ROOT / "orchestration" / "state" / "registry" / "live-ledger-domain-register.csv"
JSON_REPORT_PATH = STATE_DIR / "LIVE-LEDGER-DOMAIN-REGISTER-AUDIT-REPORT.json"
MD_REPORT_PATH = STATE_DIR / "LIVE-LEDGER-DOMAIN-REGISTER-AUDIT-REPORT.md"

EXPECTED_HEADERS = [
    "domain_id",
    "domain_label",
    "schema_version",
    "domain_status",
    "sovereign_artifact_path",
    "current_state_surface",
    "append_only_surface",
    "target_family_shape",
    "gate_profile",
    "rollout_state",
    "notes",
]
PHASE_ORDER = {
    "phase0_lawful_seed": 0,
    "phase1_repo_proof": 1,
    "phase2_family_default_ready": 2,
    "phase3_projection_open": 3,
}


@dataclass(frozen=True)
class Finding:
    level: str
    class_name: str
    domain_id: str
    scope: str
    message: str


def add_finding(
    findings: list[Finding],
    *,
    level: str,
    class_name: str,
    domain_id: str,
    scope: str,
    message: str,
) -> None:
    findings.append(
        Finding(
            level=level,
            class_name=class_name,
            domain_id=domain_id,
            scope=scope,
            message=message,
        )
    )


def repo_rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def resolve_repo_path(raw_value: str) -> Path:
    path = Path(raw_value.strip())
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def path_exists(raw_value: str) -> bool:
    return resolve_repo_path(raw_value).exists()


def read_json_dict(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def load_rows(path: Path, findings: list[Finding]) -> list[dict[str, str]]:
    if not path.exists():
        add_finding(
            findings,
            level="error",
            class_name="missing_register",
            domain_id="register",
            scope="register",
            message=f"missing register: {repo_rel(path)}",
        )
        return []

    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != EXPECTED_HEADERS:
            add_finding(
                findings,
                level="error",
                class_name="header_drift",
                domain_id="register",
                scope="register.headers",
                message=f"register headers must match {EXPECTED_HEADERS!r}",
            )
        rows = list(reader)

    seen: set[str] = set()
    for index, row in enumerate(rows, start=2):
        domain_id = row.get("domain_id", "").strip() or f"row-{index}"
        if domain_id in seen:
            add_finding(
                findings,
                level="error",
                class_name="duplicate_domain_id",
                domain_id=domain_id,
                scope=f"register:{index}",
                message=f"duplicate domain_id {domain_id!r}",
            )
        seen.add(domain_id)
    return rows


def config_rematerialization_artifacts() -> tuple[list[str], list[str]]:
    law_patterns = ("*CONFIG*REMATERIALIZATION*.md", "*CONFIG*DERIVATION*.md")
    operator_patterns = (
        "*config*surface*rematerial*.py",
        "*rematerialize*config*surface*.py",
        "*config*surface*build*.py",
    )
    laws: list[str] = []
    operators: list[str] = []

    impl_dir = REPO_ROOT / "orchestration" / "state" / "impl"
    operator_dir = REPO_ROOT / "operators"

    for pattern in law_patterns:
        laws.extend(repo_rel(path) for path in sorted(impl_dir.glob(pattern)))
    for pattern in operator_patterns:
        operators.extend(repo_rel(path) for path in sorted(operator_dir.rglob(pattern)))

    return sorted(set(laws)), sorted(set(operators))


def office_projection_phase_artifacts() -> tuple[bool, bool, list[str], list[str]]:
    phase2_paths = [
        "orchestration/state/impl/OFFICE-HARNESS-EXOCORTEX-PROJECTION-CONTRACT-v1.md",
        "operators/exocortex/office_harness_projection_bridge.py",
    ]
    phase3_paths = [
        "orchestration/state/EXOCORTEX-OFFICE-HARNESS-PROJECTION-CC92.json",
        "orchestration/state/OFFICE-HARNESS-EXOCORTEX-PROJECTION-REPORT.json",
    ]
    phase2_ready = all(path_exists(path) for path in phase2_paths)
    report = read_json_dict(REPO_ROOT / "orchestration" / "state" / "OFFICE-HARNESS-EXOCORTEX-PROJECTION-REPORT.json")
    summary = report.get("summary", {})
    phase3_ready = (
        phase2_ready
        and all(path_exists(path) for path in phase3_paths)
        and summary.get("status") == "coherent"
        and summary.get("finding_count") == 0
        and int(summary.get("projection_record_count", 0) or 0) > 0
    )
    return phase2_ready, phase3_ready, phase2_paths, phase3_paths


def append_surface_drift_message(domain_id: str, actual_surface: str, claimed_surface: str) -> str:
    if claimed_surface == "pending":
        return (
            f"{domain_id} still claims append_only_surface `pending`, but "
            f"`{actual_surface}` exists in landed repo state"
        )
    return (
        f"{domain_id} claims append_only_surface `{claimed_surface}`, but the landed surface is "
        f"`{actual_surface}`"
    )


def evaluate_domain(row: dict[str, str], findings: list[Finding]) -> dict[str, Any]:
    domain_id = row["domain_id"].strip()
    domain_findings_before = len(findings)

    sovereign_exists = path_exists(row["sovereign_artifact_path"])
    current_state_exists = path_exists(row["current_state_surface"])
    claimed_append_surface = row["append_only_surface"].strip()
    claimed_append_exists = claimed_append_surface != "pending" and path_exists(claimed_append_surface)

    actual_append_surface = ""
    materialization_law_paths: list[str] = []
    materialization_operator_paths: list[str] = []
    proof_support = False
    evidence_summary = ""
    family_default_ready = False
    projection_open = False

    if not sovereign_exists:
        add_finding(
            findings,
            level="error",
            class_name="missing_sovereign_artifact",
            domain_id=domain_id,
            scope="sovereign_artifact_path",
            message=f"missing sovereign artifact `{row['sovereign_artifact_path']}`",
        )
    if not current_state_exists:
        add_finding(
            findings,
            level="error",
            class_name="missing_current_state_surface",
            domain_id=domain_id,
            scope="current_state_surface",
            message=f"missing current-state surface `{row['current_state_surface']}`",
        )
    if claimed_append_surface != "pending" and not claimed_append_exists:
        add_finding(
            findings,
            level="error",
            class_name="missing_claimed_append_only_surface",
            domain_id=domain_id,
            scope="append_only_surface",
            message=f"claimed append-only surface `{claimed_append_surface}` is missing",
        )

    if domain_id == "tributary_disposition":
        actual_append_surface = "orchestration/state/registry/tributary-disposition-ledger.jsonl"
        compatibility_receipt = "orchestration/state/registry/TRIBUTARY-DISPOSITION-COMPATIBILITY-RECEIPT-v1.md"
        validation_report = read_json_dict(
            REPO_ROOT / "orchestration" / "state" / "TRIBUTARY-DISPOSITION-VALIDATION-REPORT.json"
        )
        report_passes = validation_report.get("status") == "PASS"
        receipt_exists = path_exists(compatibility_receipt)
        actual_append_exists = path_exists(actual_append_surface)
        proof_support = actual_append_exists and receipt_exists and report_passes
        evidence_summary = "append-only ledger, compatibility receipt, and PASS validator report"
        if not receipt_exists:
            add_finding(
                findings,
                level="error",
                class_name="missing_proof_receipt",
                domain_id=domain_id,
                scope="proof_receipt",
                message=f"missing compatibility receipt `{compatibility_receipt}`",
            )
        if not report_passes:
            add_finding(
                findings,
                level="error",
                class_name="missing_clean_validation_report",
                domain_id=domain_id,
                scope="validator_report",
                message="tributary proof row lacks a PASS validator report",
            )
    elif domain_id == "office_harness_state":
        actual_append_surface = "orchestration/state/registry/office-harness-binding-ledger.jsonl"
        materialization_law_paths = ["orchestration/state/impl/OFFICE-HARNESS-LEDGER-REMATERIALIZATION-v1.md"]
        materialization_operator_paths = ["operators/validators/rematerialize_office_harness_bindings.py"]
        validation_report = read_json_dict(REPO_ROOT / "orchestration" / "state" / "OFFICE-HARNESS-COHERENCE-REPORT.json")
        report_passes = validation_report.get("summary", {}).get("system_state") == "coherent"
        actual_append_exists = path_exists(actual_append_surface)
        laws_exist = all(path_exists(path) for path in materialization_law_paths)
        operators_exist = all(path_exists(path) for path in materialization_operator_paths)
        proof_support = actual_append_exists and laws_exist and operators_exist and report_passes
        evidence_summary = "append-only ledger, rematerialization law, rematerializer, and coherent report"
        family_default_ready, projection_open, _, _ = office_projection_phase_artifacts()
        if proof_support and family_default_ready:
            evidence_summary = (
                "append-only ledger, rematerialization law, rematerializer, coherent report, "
                "projection contract, and projection bridge"
            )
        if proof_support and projection_open:
            evidence_summary = (
                "append-only ledger, rematerialization law, rematerializer, coherent report, "
                "projection contract, projection bridge, projection artifact, and coherent projection report"
            )
        if "still absent" in row["notes"].lower() and actual_append_exists and laws_exist:
            add_finding(
                findings,
                level="warning",
                class_name="stale_family_state_note",
                domain_id=domain_id,
                scope="notes",
                message="notes still deny office-harness substrate or rebuild law after both landed",
            )
    elif domain_id == "config_surface_state":
        actual_append_surface = "orchestration/state/registry/config-surface-state-ledger.jsonl"
        materialization_law_paths, materialization_operator_paths = config_rematerialization_artifacts()
        validation_report = read_json_dict(
            REPO_ROOT / "orchestration" / "state" / "CONFIG-SURFACE-STATE-VALIDATION-REPORT.json"
        )
        report_passes = validation_report.get("summary", {}).get("status") == "PASS"
        actual_append_exists = path_exists(actual_append_surface)
        laws_exist = bool(materialization_law_paths)
        operators_exist = bool(materialization_operator_paths)
        proof_support = actual_append_exists and laws_exist and operators_exist and report_passes
        evidence_summary = "append-only ledger, rematerialization law, rematerializer, and PASS validator report"
        note_text = row["notes"].lower()
        if actual_append_exists and claimed_append_surface == "pending":
            add_finding(
                findings,
                level="warning",
                class_name="append_only_surface_claim_drift",
                domain_id=domain_id,
                scope="append_only_surface",
                message=append_surface_drift_message(domain_id, actual_append_surface, claimed_append_surface),
            )
        if actual_append_exists and "no config-surface append-only ledger" in note_text:
            add_finding(
                findings,
                level="warning",
                class_name="stale_family_state_note",
                domain_id=domain_id,
                scope="notes",
                message="notes still deny a landed config-surface append-only ledger",
            )
    else:
        actual_append_exists = claimed_append_exists
        proof_support = sovereign_exists and current_state_exists and claimed_append_exists
        evidence_summary = "generic row evidence only"

    if actual_append_surface and claimed_append_surface not in {"pending", actual_append_surface}:
        add_finding(
            findings,
            level="warning",
            class_name="append_only_surface_claim_drift",
            domain_id=domain_id,
            scope="append_only_surface",
            message=append_surface_drift_message(domain_id, actual_append_surface, claimed_append_surface),
        )

    expected_rollout_state = "phase0_lawful_seed"
    if sovereign_exists and current_state_exists and proof_support:
        expected_rollout_state = "phase1_repo_proof"
        if family_default_ready:
            expected_rollout_state = "phase2_family_default_ready"
        if projection_open:
            expected_rollout_state = "phase3_projection_open"
    expected_domain_status = "active_family" if expected_rollout_state == "phase1_repo_proof" else "candidate_family"
    if expected_rollout_state in {"phase2_family_default_ready", "phase3_projection_open"}:
        expected_domain_status = "active_family"

    claimed_rollout_state = row["rollout_state"].strip()
    claimed_domain_status = row["domain_status"].strip()

    claimed_phase_rank = PHASE_ORDER.get(claimed_rollout_state, -1)
    expected_phase_rank = PHASE_ORDER.get(expected_rollout_state, -1)

    if claimed_phase_rank > expected_phase_rank:
        add_finding(
            findings,
            level="error",
            class_name="phase_overclaim",
            domain_id=domain_id,
            scope="rollout_state",
            message=(
                f"claimed rollout_state `{claimed_rollout_state}` outruns landed evidence; "
                f"strongest justified state is `{expected_rollout_state}`"
            ),
        )
    elif claimed_phase_rank < expected_phase_rank:
        add_finding(
            findings,
            level="warning",
            class_name="phase_underclaim",
            domain_id=domain_id,
            scope="rollout_state",
            message=(
                f"claimed rollout_state `{claimed_rollout_state}` understates landed evidence; "
                f"strongest justified state is `{expected_rollout_state}`"
            ),
        )

    if claimed_domain_status != expected_domain_status:
        level = "error" if expected_domain_status == "candidate_family" else "warning"
        add_finding(
            findings,
            level=level,
            class_name="family_state_claim_drift",
            domain_id=domain_id,
            scope="domain_status",
            message=(
                f"claimed domain_status `{claimed_domain_status}` does not match the strongest justified "
                f"family state `{expected_domain_status}`"
            ),
        )

    if claimed_rollout_state != "phase0_lawful_seed" and claimed_append_surface == "pending":
        add_finding(
            findings,
            level="error",
            class_name="gate_violation_lg03",
            domain_id=domain_id,
            scope="append_only_surface",
            message="rows beyond phase0_lawful_seed may not leave append_only_surface as `pending`",
        )

    domain_findings = findings[domain_findings_before:]
    warning_count = sum(1 for finding in domain_findings if finding.level == "warning")
    error_count = sum(1 for finding in domain_findings if finding.level == "error")

    return {
        "domain_id": domain_id,
        "domain_label": row["domain_label"].strip(),
        "claimed_rollout_state": claimed_rollout_state,
        "expected_rollout_state": expected_rollout_state,
        "claimed_domain_status": claimed_domain_status,
        "expected_domain_status": expected_domain_status,
        "gate_profile": row["gate_profile"].strip(),
        "sovereign_artifact_path": row["sovereign_artifact_path"].strip(),
        "sovereign_artifact_exists": sovereign_exists,
        "current_state_surface": row["current_state_surface"].strip(),
        "current_state_surface_exists": current_state_exists,
        "claimed_append_only_surface": claimed_append_surface,
        "claimed_append_only_surface_exists": claimed_append_exists,
        "actual_append_only_surface": actual_append_surface or claimed_append_surface,
        "actual_append_only_surface_exists": bool(actual_append_surface) and path_exists(actual_append_surface),
        "materialization_law_paths": materialization_law_paths,
        "materialization_operator_paths": materialization_operator_paths,
        "proof_support": proof_support,
        "evidence_summary": evidence_summary,
        "finding_count": len(domain_findings),
        "warning_count": warning_count,
        "error_count": error_count,
    }


def build_report(records: list[dict[str, Any]], findings: list[Finding]) -> dict[str, Any]:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    error_count = sum(1 for finding in findings if finding.level == "error")
    warning_count = sum(1 for finding in findings if finding.level == "warning")
    phase_drift_count = sum(
        1
        for finding in findings
        if finding.class_name in {"phase_underclaim", "phase_overclaim", "family_state_claim_drift"}
    )
    append_only_drift_count = sum(
        1
        for finding in findings
        if finding.class_name in {"append_only_surface_claim_drift", "missing_claimed_append_only_surface", "gate_violation_lg03"}
    )
    note_drift_count = sum(1 for finding in findings if finding.class_name == "stale_family_state_note")
    coherent_rows = sum(1 for record in records if record["finding_count"] == 0)

    status = "PASS" if not findings else "WARN"
    if error_count:
        status = "FAIL"

    return {
        "schema_version": "live-ledger-domain-register-audit-report/v1",
        "generated_at": generated_at,
        "mode": "report-first",
        "repo_root": str(REPO_ROOT),
        "summary": {
            "status": status,
            "register": repo_rel(REGISTER_PATH),
            "rows": len(records),
            "coherent_rows": coherent_rows,
            "finding_count": len(findings),
            "error_count": error_count,
            "warning_count": warning_count,
            "phase_drift_count": phase_drift_count,
            "append_only_drift_count": append_only_drift_count,
            "note_drift_count": note_drift_count,
        },
        "records": records,
        "findings": [asdict(finding) for finding in findings],
    }


def write_reports(report: dict[str, Any], json_out: Path, md_out: Path) -> None:
    json_out.write_text(f"{json.dumps(report, indent=2)}\n", encoding="utf-8")

    summary = report["summary"]
    lines = [
        "# Live-Ledger Domain Register Audit Report",
        "",
        "Report-first audit of register coherence against landed family artifacts.",
        "",
        "## Summary",
        "",
        f"- register: `{summary['register']}`",
        f"- rows: {summary['rows']}",
        f"- coherent rows: {summary['coherent_rows']}",
        f"- findings: {summary['finding_count']}",
        f"- errors: {summary['error_count']}",
        f"- warnings: {summary['warning_count']}",
        f"- phase drift findings: {summary['phase_drift_count']}",
        f"- append-only drift findings: {summary['append_only_drift_count']}",
        f"- stale note findings: {summary['note_drift_count']}",
        f"- status: `{summary['status']}`",
        "",
        "## Domain Readout",
        "",
        "| Domain | Claimed Phase | Expected Phase | Claimed Append Surface | Actual Append Surface | Findings |",
        "|---|---|---|---|---|---|",
    ]

    for record in report["records"]:
        lines.append(
            "| "
            f"{record['domain_id']} | "
            f"`{record['claimed_rollout_state']}` | "
            f"`{record['expected_rollout_state']}` | "
            f"`{record['claimed_append_only_surface']}` | "
            f"`{record['actual_append_only_surface']}` | "
            f"{record['finding_count']} |"
        )

    lines.extend(["", "## Findings", ""])
    if not report["findings"]:
        lines.append("- none")
    else:
        for finding in report["findings"]:
            lines.append(
                f"- [{finding['level']}] `{finding['domain_id']}` `{finding['class_name']}`: {finding['message']}"
            )

    md_out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--register", type=Path, default=REGISTER_PATH)
    parser.add_argument("--json-out", type=Path, default=JSON_REPORT_PATH)
    parser.add_argument("--md-out", type=Path, default=MD_REPORT_PATH)
    args = parser.parse_args()

    findings: list[Finding] = []
    rows = load_rows(args.register, findings)
    records = [evaluate_domain(row, findings) for row in rows]
    report = build_report(records, findings)
    write_reports(report, args.json_out, args.md_out)

    print(
        f"{report['summary']['status']}: "
        f"{report['summary']['finding_count']} findings "
        f"({report['summary']['error_count']} errors, {report['summary']['warning_count']} warnings)"
    )
    return 1 if report["summary"]["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

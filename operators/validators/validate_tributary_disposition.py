#!/usr/bin/env python3
"""Report-only validator for tributary disposition registry and ledger joins."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = REPO_ROOT / "orchestration" / "state"
DEFAULT_REGISTRY = REPO_ROOT / "orchestration" / "state" / "registry" / "tributary-disposition-registry.csv"
DEFAULT_LEDGER = REPO_ROOT / "orchestration" / "state" / "registry" / "tributary-disposition-ledger.jsonl"
DEFAULT_MD_REPORT = STATE_DIR / "TRIBUTARY-DISPOSITION-VALIDATION-REPORT.md"
DEFAULT_JSON_REPORT = STATE_DIR / "TRIBUTARY-DISPOSITION-VALIDATION-REPORT.json"

EXPECTED_HEADER = [
    "candidate_id",
    "schema_version",
    "source_tributary",
    "source_path",
    "source_relpath_hash",
    "artifact_class",
    "artifact_format",
    "lineage_witness",
    "provenance_sensitivity",
    "authority_score",
    "present_relevance",
    "compaction_yield",
    "duplication_status",
    "review_basis",
    "chosen_disposition",
    "destination_lane",
    "destination_artifact_path",
    "archive_manifest_path",
    "receipt_path",
    "external_pointer",
    "merge_family_id",
    "justification",
    "record_state",
    "intake_batch_id",
    "last_action_at",
    "last_action_by",
    "dest_artifact_hash",
    "supersedes_candidate_id",
    "notes",
]

ENUMS = {
    "source_tributary": {
        "live_shell",
        "syncrescendence_old",
        "syncrescendence_pre_schematic_design",
    },
    "artifact_class": {
        "law",
        "reference",
        "playbook",
        "operator",
        "executive",
        "office_state",
        "manifest",
        "source",
        "log",
        "other",
    },
    "artifact_format": {
        "md",
        "json",
        "yaml",
        "py",
        "sh",
        "directory_manifest",
        "binary",
        "mixed",
        "other",
    },
    "provenance_sensitivity": {"low", "medium", "high", "restricted"},
    "duplication_status": {"unique", "duplicate_family", "superseded", "derived", "unknown"},
    "review_basis": {"manual_read", "family_sample", "validator_scan", "merged_adjudication", "other"},
    "chosen_disposition": {
        "none",
        "promote_live_law",
        "promote_sigma",
        "promote_sigma_reference",
        "promote_playbook",
        "promote_operator",
        "retain_pedigree_rehoused",
        "retain_archive_manifest_only",
        "externalize_to_exocortex",
        "cull_with_receipt",
    },
    "record_state": {
        "intake_pending",
        "triaged",
        "adjudicated",
        "scheduled",
        "executed",
        "verified",
        "closed",
        "exception",
    },
}

TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
CANDIDATE_ID_RE = re.compile(r"^tdc-[a-z0-9-]+-[0-9]{4}$")
REPO_PATH_FIELDS = (
    "source_path",
    "destination_lane",
    "destination_artifact_path",
    "archive_manifest_path",
    "receipt_path",
)
LEDGER_EVENT_ID_RE = re.compile(r"^tdl-[0-9]{8}-[0-9]{4}$")
LEDGER_EVENT_TYPES = {
    "row_intake",
    "row_triaged",
    "row_adjudicated",
    "row_scheduled",
    "row_executed",
    "row_verified",
    "row_closed",
    "row_exception",
    "row_corrected",
}
STATE_ORDER = {
    "intake_pending": 0,
    "triaged": 1,
    "adjudicated": 2,
    "scheduled": 3,
    "executed": 4,
    "verified": 5,
    "closed": 6,
    "exception": -1,
}
SCORE_FIELDS = ("authority_score", "present_relevance", "compaction_yield")
PROMOTION_DISPOSITIONS = {
    "promote_live_law",
    "promote_sigma",
    "promote_sigma_reference",
    "promote_playbook",
    "promote_operator",
}
HASH_REQUIRED_DISPOSITIONS = PROMOTION_DISPOSITIONS | {"retain_pedigree_rehoused"}
LEGAL_TRANSITIONS = {
    ("intake_pending", "triaged"),
    ("triaged", "adjudicated"),
    ("adjudicated", "scheduled"),
    ("scheduled", "executed"),
    ("executed", "verified"),
    ("verified", "closed"),
    ("intake_pending", "exception"),
    ("triaged", "exception"),
    ("adjudicated", "exception"),
    ("scheduled", "exception"),
    ("executed", "exception"),
    ("verified", "exception"),
    ("exception", "triaged"),
    ("exception", "adjudicated"),
}
EXPECTED_EVENT_STATE_AFTER = {
    "row_triaged": "triaged",
    "row_adjudicated": "adjudicated",
    "row_scheduled": "scheduled",
    "row_executed": "executed",
    "row_verified": "verified",
    "row_closed": "closed",
    "row_exception": "exception",
}


@dataclass(frozen=True)
class Finding:
    scope: str
    message: str


def add_finding(findings: list[Finding], scope: str, message: str) -> None:
    findings.append(Finding(scope=scope, message=message))


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def read_registry_rows(path: Path, findings: list[Finding]) -> list[dict[str, str]]:
    if not path.exists():
        add_finding(findings, "registry", f"registry file missing: {display_path(path)}")
        return []

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines:
        add_finding(findings, "registry", "registry CSV is empty")
        return []

    header = next(csv.reader([lines[0]]))
    if header != EXPECTED_HEADER:
        add_finding(findings, "registry", "CSV header does not match the exact normative v1 header")
        return []

    rows = list(csv.DictReader(lines))
    for index, row in enumerate(rows, start=2):
        if row is None:
            add_finding(findings, f"registry:{index}", "row could not be parsed")
    return rows


def is_repo_relative_path(value: str, *, allow_none: bool) -> bool:
    if allow_none and value == "none":
        return True
    if not value or value != value.strip():
        return False
    if value.startswith("/") or "\\" in value:
        return False
    parts = PurePosixPath(value).parts
    if not parts:
        return False
    return all(part not in {"..", "."} for part in parts)


def validate_timestamp(findings: list[Finding], scope: str, field: str, value: str) -> None:
    if not TIMESTAMP_RE.fullmatch(value):
        add_finding(findings, scope, f"{field} must be ISO-8601 UTC with trailing Z: {value!r}")


def validate_enum(findings: list[Finding], scope: str, field: str, value: str) -> None:
    allowed = ENUMS[field]
    if value not in allowed:
        add_finding(findings, scope, f"{field} has illegal value {value!r}")


def validate_score(findings: list[Finding], scope: str, field: str, value: str) -> None:
    try:
        parsed = int(value)
    except ValueError:
        add_finding(findings, scope, f"{field} must be an integer in 0..5, found {value!r}")
        return
    if not 0 <= parsed <= 5:
        add_finding(findings, scope, f"{field} must be an integer in 0..5, found {value!r}")


def validate_required_paths(findings: list[Finding], scope: str, row: dict[str, str]) -> None:
    state = row["record_state"]
    disposition = row["chosen_disposition"]
    state_rank = STATE_ORDER.get(state, -99)

    if disposition == "none" and state not in {"intake_pending", "triaged", "exception"}:
        add_finding(findings, scope, "chosen_disposition=none is only allowed in intake_pending, triaged, or exception")

    if state_rank < STATE_ORDER["executed"]:
        return

    if row["receipt_path"] == "none":
        add_finding(findings, scope, "receipt_path must be populated by executed")

    if disposition in PROMOTION_DISPOSITIONS:
        if row["destination_lane"] == "none":
            add_finding(findings, scope, "promotion disposition requires destination_lane by executed")
        if row["destination_artifact_path"] == "none":
            add_finding(findings, scope, "promotion disposition requires destination_artifact_path by executed")
    elif disposition == "retain_pedigree_rehoused":
        if row["destination_lane"] != "pedigree/rehoused":
            add_finding(findings, scope, "retain_pedigree_rehoused requires destination_lane=pedigree/rehoused")
        if row["destination_artifact_path"] == "none":
            add_finding(findings, scope, "retain_pedigree_rehoused requires destination_artifact_path by executed")
    elif disposition == "retain_archive_manifest_only":
        if row["archive_manifest_path"] == "none":
            add_finding(findings, scope, "retain_archive_manifest_only requires archive_manifest_path by executed")
        if row["destination_lane"] != "none":
            add_finding(findings, scope, "retain_archive_manifest_only requires destination_lane=none")
        if row["destination_artifact_path"] != "none":
            add_finding(findings, scope, "retain_archive_manifest_only requires destination_artifact_path=none")
    elif disposition == "externalize_to_exocortex":
        if row["external_pointer"] == "none":
            add_finding(findings, scope, "externalize_to_exocortex requires external_pointer by executed")
        if row["destination_lane"] != "none":
            add_finding(findings, scope, "externalize_to_exocortex requires destination_lane=none")
        if row["destination_artifact_path"] != "none":
            add_finding(findings, scope, "externalize_to_exocortex requires destination_artifact_path=none")
    elif disposition == "cull_with_receipt":
        if row["destination_lane"] != "none":
            add_finding(findings, scope, "cull_with_receipt requires destination_lane=none")
        if row["destination_artifact_path"] != "none":
            add_finding(findings, scope, "cull_with_receipt requires destination_artifact_path=none")
        if row["archive_manifest_path"] != "none":
            add_finding(findings, scope, "cull_with_receipt requires archive_manifest_path=none")
        if row["external_pointer"] != "none":
            add_finding(findings, scope, "cull_with_receipt requires external_pointer=none")

    dest_hash = row["dest_artifact_hash"]
    if dest_hash != "none" and not SHA256_RE.fullmatch(dest_hash):
        add_finding(findings, scope, f"dest_artifact_hash must be sha256:<64 lowercase hex> or 'none', found {dest_hash!r}")

    if state_rank >= STATE_ORDER["verified"] and disposition in HASH_REQUIRED_DISPOSITIONS:
        if dest_hash == "none":
            add_finding(findings, scope, "verified promotion or rehousing disposition requires dest_artifact_hash")
        elif not SHA256_RE.fullmatch(dest_hash):
            add_finding(findings, scope, f"verified promotion or rehousing disposition has illegal dest_artifact_hash {dest_hash!r}")


def validate_registry(findings: list[Finding], rows: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    by_candidate: dict[str, dict[str, str]] = {}
    seen_hashes: dict[str, str] = {}

    for line_number, row in enumerate(rows, start=2):
        scope = f"registry:{line_number}"
        candidate_id = row["candidate_id"]

        if candidate_id in by_candidate:
            add_finding(findings, scope, f"duplicate candidate_id {candidate_id!r}")
        else:
            by_candidate[candidate_id] = row

        if not CANDIDATE_ID_RE.fullmatch(candidate_id):
            add_finding(findings, scope, f"candidate_id has illegal form {candidate_id!r}")

        if row["schema_version"] != "v1":
            add_finding(findings, scope, f"schema_version must be 'v1', found {row['schema_version']!r}")

        for field in ENUMS:
            validate_enum(findings, scope, field, row[field])

        for field in SCORE_FIELDS:
            validate_score(findings, scope, field, row[field])

        for field in REPO_PATH_FIELDS:
            allow_none = field != "source_path"
            if not is_repo_relative_path(row[field], allow_none=allow_none):
                add_finding(findings, scope, f"{field} must be repo-relative or 'none', found {row[field]!r}")

        validate_timestamp(findings, scope, "last_action_at", row["last_action_at"])

        expected_hash = "sha256:" + hashlib.sha256(
            f"{row['source_tributary']}|{row['source_path']}".encode("utf-8")
        ).hexdigest()
        if row["source_relpath_hash"] != expected_hash:
            add_finding(findings, scope, "source_relpath_hash does not match sha256(<source_tributary>|<source_path>)")

        if row["source_relpath_hash"] in seen_hashes and row["supersedes_candidate_id"] == "none":
            prior_candidate = seen_hashes[row["source_relpath_hash"]]
            add_finding(
                findings,
                scope,
                f"source_relpath_hash duplicates {prior_candidate!r} without supersedes_candidate_id",
            )
        else:
            seen_hashes.setdefault(row["source_relpath_hash"], candidate_id)

        validate_required_paths(findings, scope, row)

        if row["archive_manifest_path"] != "none":
            manifest_path = REPO_ROOT / row["archive_manifest_path"]
            if not manifest_path.exists():
                add_finding(findings, scope, f"archive_manifest_path does not exist: {row['archive_manifest_path']}")

        if row["receipt_path"] != "none":
            receipt_path = REPO_ROOT / row["receipt_path"]
            if not receipt_path.exists():
                add_finding(findings, scope, f"receipt_path does not exist: {row['receipt_path']}")

    return by_candidate


def read_ledger_events(path: Path, findings: list[Finding]) -> list[dict[str, object]]:
    if not path.exists():
        add_finding(findings, "ledger", f"ledger file missing: {display_path(path)}")
        return []

    events: list[dict[str, object]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    seen_event_ids: set[str] = set()

    for line_number, raw_line in enumerate(lines, start=1):
        if not raw_line.strip():
            continue
        scope = f"ledger:{line_number}"
        try:
            event = json.loads(raw_line)
        except json.JSONDecodeError as exc:
            add_finding(findings, scope, f"invalid JSON object: {exc.msg}")
            continue
        if not isinstance(event, dict):
            add_finding(findings, scope, "ledger line must be a JSON object")
            continue

        event_id = str(event.get("event_id", ""))
        if not LEDGER_EVENT_ID_RE.fullmatch(event_id):
            add_finding(findings, scope, f"event_id has illegal form {event_id!r}")
        elif event_id in seen_event_ids:
            add_finding(findings, scope, f"duplicate event_id {event_id!r}")
        else:
            seen_event_ids.add(event_id)

        if event.get("schema_version") != "v1":
            add_finding(findings, scope, f"schema_version must be 'v1', found {event.get('schema_version')!r}")

        event_type = str(event.get("event_type", ""))
        if event_type not in LEDGER_EVENT_TYPES:
            add_finding(findings, scope, f"event_type has illegal value {event_type!r}")

        occurred_at = str(event.get("occurred_at", ""))
        validate_timestamp(findings, scope, "occurred_at", occurred_at)

        receipt_path = str(event.get("receipt_path", "none"))
        if not is_repo_relative_path(receipt_path, allow_none=True):
            add_finding(findings, scope, f"receipt_path must be repo-relative or 'none', found {receipt_path!r}")
        elif receipt_path != "none" and not (REPO_ROOT / receipt_path).exists():
            add_finding(findings, scope, f"receipt_path does not exist: {receipt_path}")

        row_version = event.get("row_version")
        if not isinstance(row_version, int) or row_version < 1:
            add_finding(findings, scope, f"row_version must be a positive integer, found {row_version!r}")

        events.append(event)

    return events


def validate_latest_ledger_parity(
    findings: list[Finding],
    rows_by_candidate: dict[str, dict[str, str]],
    events: list[dict[str, object]],
) -> None:
    events_by_candidate: dict[str, list[dict[str, object]]] = defaultdict(list)
    for event in events:
        candidate_id = str(event.get("candidate_id", ""))
        if not candidate_id:
            continue
        events_by_candidate[candidate_id].append(event)

    for candidate_id, row in sorted(rows_by_candidate.items()):
        scope = f"registry:{candidate_id}"
        candidate_events = events_by_candidate.get(candidate_id, [])
        if not candidate_events:
            add_finding(findings, scope, "row has no ledger history to validate against")
            continue

        valid_versions = [event for event in candidate_events if isinstance(event.get("row_version"), int)]
        if not valid_versions:
            add_finding(findings, scope, "row has ledger history but no event with a valid integer row_version")
            continue
        ordered_events = sorted(
            valid_versions,
            key=lambda event: (
                int(event["row_version"]),
                str(event.get("occurred_at", "")),
                str(event.get("event_id", "")),
            ),
        )

        expected_versions = list(range(1, len(ordered_events) + 1))
        observed_versions = [int(event["row_version"]) for event in ordered_events]
        if observed_versions != expected_versions:
            add_finding(findings, scope, f"row_version sequence is not contiguous: {observed_versions}")

        saw_verified = False
        prior_after: str | None = None
        for index, event in enumerate(ordered_events, start=1):
            event_scope = f"ledger:{candidate_id}:v{event['row_version']}"
            event_type = str(event.get("event_type", ""))
            before_raw = event.get("record_state_before")
            before = None if before_raw is None else str(before_raw)
            after = str(event.get("record_state_after", ""))

            if after not in STATE_ORDER:
                add_finding(findings, event_scope, f"record_state_after has illegal value {after!r}")
            if before is not None and before not in STATE_ORDER:
                add_finding(findings, event_scope, f"record_state_before has illegal value {before!r}")

            expected_after = EXPECTED_EVENT_STATE_AFTER.get(event_type)
            if expected_after and after != expected_after:
                add_finding(findings, event_scope, f"{event_type} must set record_state_after={expected_after!r}, found {after!r}")

            if event_type == "row_intake":
                if int(event["row_version"]) != 1:
                    add_finding(findings, event_scope, "row_intake is only legal as row_version=1")
                if after not in {"intake_pending", "triaged"}:
                    add_finding(findings, event_scope, f"row_intake may only create intake_pending or triaged, found {after!r}")
                if before not in {None, "", "none"}:
                    add_finding(findings, event_scope, f"row_intake requires null prior state, found {before!r}")
            elif event_type == "row_corrected":
                if before is None:
                    add_finding(findings, event_scope, "row_corrected requires record_state_before to preserve state")
                elif before != after:
                    add_finding(findings, event_scope, f"row_corrected must preserve record_state {before!r}, found {after!r}")
            elif before is None:
                add_finding(findings, event_scope, f"{event_type} requires record_state_before")
            elif (before, after) not in LEGAL_TRANSITIONS:
                add_finding(findings, event_scope, f"illegal state transition {before!r} -> {after!r}")

            if prior_after is not None and before != prior_after:
                add_finding(
                    findings,
                    event_scope,
                    f"record_state_before {before!r} does not match prior ledger state {prior_after!r}",
                )

            if after == "verified":
                saw_verified = True
            if after == "closed" and not saw_verified:
                add_finding(findings, event_scope, "closed rows must previously pass through verified")

            prior_after = after

        latest = ordered_events[-1]
        latest_state = str(latest.get("record_state_after", ""))
        latest_actor = str(latest.get("actor", ""))
        latest_time = str(latest.get("occurred_at", ""))

        if latest_state != row["record_state"]:
            add_finding(
                findings,
                scope,
                f"latest ledger record_state_after {latest_state!r} does not match CSV record_state {row['record_state']!r}",
            )
        if latest_actor != row["last_action_by"]:
            add_finding(
                findings,
                scope,
                f"latest ledger actor {latest_actor!r} does not match CSV last_action_by {row['last_action_by']!r}",
            )
        if latest_time != row["last_action_at"]:
            add_finding(
                findings,
                scope,
                f"latest ledger occurred_at {latest_time!r} does not match CSV last_action_at {row['last_action_at']!r}",
            )

    for candidate_id in sorted(events_by_candidate):
        if candidate_id not in rows_by_candidate:
            add_finding(findings, f"ledger:{candidate_id}", "ledger candidate_id is missing from the CSV current-state registry")


def build_report(
    registry_path: Path,
    ledger_path: Path,
    rows: list[dict[str, str]],
    events: list[dict[str, object]],
    findings: list[Finding],
) -> dict[str, Any]:
    return {
        "validator": "Tributary Disposition Validator",
        "mode": "report-only",
        "registry": display_path(registry_path),
        "ledger": display_path(ledger_path),
        "rows": len(rows),
        "ledger_events": len(events),
        "finding_count": len(findings),
        "status": "PASS" if not findings else "FAIL",
        "findings": [asdict(finding) for finding in sorted(findings, key=lambda item: (item.scope, item.message))],
    }


def render_stdout_report(report: dict[str, Any]) -> str:
    lines = [
        str(report["validator"]),
        f"Registry: {report['registry']}",
        f"Ledger: {report['ledger']}",
        f"Rows: {report['rows']}",
        f"Ledger events: {report['ledger_events']}",
        f"Findings: {report['finding_count']}",
        f"Status: {report['status']}",
    ]
    findings = report["findings"]
    if findings:
        lines.append("")
        lines.append("Findings")
        for finding in findings:
            lines.append(f"- [{finding['scope']}] {finding['message']}")
    return "\n".join(lines)


def render_markdown_report(report: dict[str, Any]) -> str:
    lines = [
        "# Tributary Disposition Validation Report",
        "",
        "Report-only validation of tributary disposition structural legality, custody joins, transition law, and verified-state hash obligations.",
        "",
        "## Summary",
        "",
        f"- registry: `{report['registry']}`",
        f"- ledger: `{report['ledger']}`",
        f"- rows: {report['rows']}",
        f"- ledger events: {report['ledger_events']}",
        f"- findings: {report['finding_count']}",
        f"- status: `{report['status']}`",
        "",
        "## Findings",
        "",
    ]
    findings = report["findings"]
    if findings:
        for finding in findings:
            lines.append(f"- [{finding['scope']}] {finding['message']}")
    else:
        lines.append("- none")
    lines.append("")
    return "\n".join(lines)


def write_report_artifacts(md_report: Path, json_report: Path, report: dict[str, Any]) -> None:
    json_report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_report.write_text(render_markdown_report(report), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a deterministic report-only validation pass over tributary disposition artifacts.",
    )
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--md-report", type=Path, default=DEFAULT_MD_REPORT)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON_REPORT)
    args = parser.parse_args()

    findings: list[Finding] = []
    rows = read_registry_rows(args.registry, findings)
    rows_by_candidate = validate_registry(findings, rows)
    events = read_ledger_events(args.ledger, findings)
    validate_latest_ledger_parity(findings, rows_by_candidate, events)
    report = build_report(args.registry, args.ledger, rows, events, findings)
    write_report_artifacts(args.md_report, args.json_report, report)

    print(render_stdout_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

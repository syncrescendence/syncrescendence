#!/usr/bin/env python3
"""Report-first validator for office-harness coherence and effective bindings."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = REPO_ROOT / "orchestration" / "state"
REGISTRY_OUT = STATE_DIR / "registry" / "office-harness-bindings.effective.json"
JSON_OUT = STATE_DIR / "OFFICE-HARNESS-COHERENCE-REPORT.json"
MD_OUT = STATE_DIR / "OFFICE-HARNESS-COHERENCE-REPORT.md"
AGENTS_PATH = REPO_ROOT / "AGENTS.md"
LAW_PATH = STATE_DIR / "impl" / "OFFICE-HARNESS-BINDING-CONTRACT-v1.md"

EXPECTED_SCHEMA_VERSION = "office-harness-metadata/v1"
EXPECTED_RATIFICATION_POINTER = "office-harness-binding-contract/v1"
EXPECTED_RATIFIED_ARTIFACT_ID = "OFFICE-HARNESS-BINDING-CONTRACT-v1"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SECRET_KEY_RE = re.compile(r"(token|secret|cookie|password|api[_-]?key|session)", re.IGNORECASE)
SECRET_VALUE_PATTERNS = (
    re.compile(r"Bearer\s+[A-Za-z0-9._-]{12,}"),
    re.compile(r"\bsk-[A-Za-z0-9]{12,}\b"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bAIza[0-9A-Za-z\-_]{20,}\b"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9._-]{8,}\.[A-Za-z0-9._-]{8,}\b"),
)
HARD_FEDERAL_LANE_ALLOWLIST = {
    "communications",
    "executive",
    "knowledge",
    "offices",
    "operators",
    "orchestration",
    "pedigree",
    "playbooks",
    "program",
    "runtime",
    "validated-patterns",
}
ALLOWED_HARNESS_FAMILIES = {
    "claude_code": {"claude_code", "claude"},
    "codex": {"codex"},
    "gemini_cli": {"gemini_cli", "gemini"},
    "openclaw_mac_mini": {"openclaw"},
    "openclaw_macbook_air": {"openclaw"},
}


@dataclass(frozen=True)
class OfficeDefinition:
    office_id: str
    office_title: str
    office_epithet: str
    office_burden: str


@dataclass(frozen=True)
class Finding:
    level: str
    class_name: str
    scope: str
    office_id: str | None
    message: str


def add_finding(
    findings: list[Finding],
    *,
    class_name: str,
    scope: str,
    message: str,
    office_id: str | None = None,
    level: str = "error",
) -> None:
    findings.append(
        Finding(
            level=level,
            class_name=class_name,
            scope=scope,
            office_id=office_id,
            message=message,
        )
    )


def repo_rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_section(text: str, heading: str) -> str:
    marker = f"## {heading}"
    start = text.find(marker)
    if start == -1:
        raise ValueError(f"missing section {heading!r} in AGENTS.md")
    remainder = text[start + len(marker) :]
    next_heading = remainder.find("\n## ")
    if next_heading == -1:
        return remainder.strip()
    return remainder[:next_heading].strip()


def parse_federal_offices(agents_text: str) -> list[OfficeDefinition]:
    section = extract_section(agents_text, "Federal Offices")
    offices: list[OfficeDefinition] = []
    pattern = re.compile(r"- `([^`]+)` — \*\*([^*]+)\*\*: (.+)")
    for line in section.splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        title, epithet, burden = match.groups()
        offices.append(
            OfficeDefinition(
                office_id=title.lower(),
                office_title=title,
                office_epithet=epithet.strip(),
                office_burden=burden.strip(),
            )
        )
    if not offices:
        raise ValueError("no federal offices parsed from AGENTS.md")
    return offices


def parse_certified_harnesses(agents_text: str) -> dict[str, str]:
    if "Certified harness avatars:" not in agents_text:
        raise ValueError("missing certified harness avatar section in AGENTS.md")
    section = agents_text.split("Certified harness avatars:", 1)[1]
    section = section.split("Stage0 provisional surface avatars:", 1)[0]
    harnesses: dict[str, str] = {}
    pattern = re.compile(r"- `([^`]+)` -> `([^`]+)`")
    for line in section.splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        harness, office_title = match.groups()
        harnesses[harness] = office_title
    if not harnesses:
        raise ValueError("no certified harness avatars parsed from AGENTS.md")
    return harnesses


def parse_lane_roots(agents_text: str) -> set[str]:
    section = extract_section(agents_text, "Lane Roles")
    lanes: set[str] = set()
    pattern = re.compile(r"- `([^`]+)`:")
    for line in section.splitlines():
        match = pattern.match(line.strip())
        if not match:
            continue
        lane = match.group(1).rstrip("/")
        if lane:
            lanes.add(lane)
    return lanes | HARD_FEDERAL_LANE_ALLOWLIST


def resolve_repo_path(raw_value: str) -> Path:
    value = raw_value.strip()
    path = Path(value)
    if path.is_absolute():
        return path
    return REPO_ROOT / value


def nested_get(mapping: dict[str, Any], *keys: str) -> Any:
    current: Any = mapping
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def ensure_string(
    findings: list[Finding],
    data: dict[str, Any],
    dotted_path: str,
    *,
    office_id: str,
) -> str | None:
    value = nested_get(data, *dotted_path.split("."))
    if isinstance(value, date):
        return value.isoformat()
    if not isinstance(value, str) or not value.strip():
        add_finding(
            findings,
            class_name="missing_required_field",
            scope=dotted_path,
            office_id=office_id,
            message=f"{dotted_path} must be a non-empty string",
        )
        return None
    return value.strip()


def ensure_string_list(
    findings: list[Finding],
    data: dict[str, Any],
    dotted_path: str,
    *,
    office_id: str,
) -> list[str]:
    value = nested_get(data, *dotted_path.split("."))
    if not isinstance(value, list) or not value:
        add_finding(
            findings,
            class_name="missing_required_field",
            scope=dotted_path,
            office_id=office_id,
            message=f"{dotted_path} must be a non-empty list",
        )
        return []
    items: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            add_finding(
                findings,
                class_name="missing_required_field",
                scope=f"{dotted_path}[{index}]",
                office_id=office_id,
                message=f"{dotted_path}[{index}] must be a non-empty string",
            )
            continue
        items.append(item.strip())
    return items


def expected_harness_family(primary_harness: str) -> str:
    if primary_harness.startswith("openclaw_"):
        return "openclaw"
    return primary_harness


def scan_secret_like_material(
    value: Any,
    *,
    findings: list[Finding],
    office_id: str,
    scope: str,
) -> None:
    if isinstance(value, dict):
        for key, inner in value.items():
            key_str = str(key)
            if SECRET_KEY_RE.search(key_str):
                if isinstance(inner, str) and inner.strip():
                    add_finding(
                        findings,
                        class_name="secret_like_material",
                        scope=f"{scope}.{key_str}",
                        office_id=office_id,
                        message=f"{scope}.{key_str} uses a secret-like field name",
                    )
                continue
            scan_secret_like_material(inner, findings=findings, office_id=office_id, scope=f"{scope}.{key_str}")
        return
    if isinstance(value, list):
        for index, inner in enumerate(value):
            scan_secret_like_material(inner, findings=findings, office_id=office_id, scope=f"{scope}[{index}]")
        return
    if isinstance(value, str):
        for pattern in SECRET_VALUE_PATTERNS:
            if pattern.search(value):
                add_finding(
                    findings,
                    class_name="secret_like_material",
                    scope=scope,
                    office_id=office_id,
                    message=f"{scope} contains a secret-like token pattern",
                )
                break


def validate_contract(
    *,
    office: OfficeDefinition,
    certified_harnesses: dict[str, str],
    lane_roots: set[str],
    findings: list[Finding],
    generated_at: str,
) -> dict[str, Any] | None:
    office_root = REPO_ROOT / "offices" / office.office_id
    metadata_path = office_root / "platform" / "contracts" / "OFFICE-HARNESS-METADATA.v1.yaml"
    playbook_path = REPO_ROOT / "playbooks" / office.office_id / "PLAYBOOK.md"
    readme_path = office_root / "README.md"

    if not metadata_path.exists():
        add_finding(
            findings,
            class_name="missing_contract",
            scope=repo_rel(metadata_path),
            office_id=office.office_id,
            message="required office-harness metadata contract is missing",
        )
        return None

    start_index = len(findings)
    raw_contract = read_text(metadata_path)

    try:
        parsed = yaml.safe_load(raw_contract)
    except yaml.YAMLError as exc:
        add_finding(
            findings,
            class_name="invalid_contract",
            scope=repo_rel(metadata_path),
            office_id=office.office_id,
            message=f"YAML parse failed: {exc}",
        )
        return None

    if not isinstance(parsed, dict):
        add_finding(
            findings,
            class_name="invalid_contract",
            scope=repo_rel(metadata_path),
            office_id=office.office_id,
            message="metadata contract must parse to a mapping",
        )
        return None

    scan_secret_like_material(parsed, findings=findings, office_id=office.office_id, scope="contract")

    schema_version = ensure_string(findings, parsed, "schema_version", office_id=office.office_id)
    office_id = ensure_string(findings, parsed, "office_id", office_id=office.office_id)
    office_title = ensure_string(findings, parsed, "office_title", office_id=office.office_id)
    office_epithet = ensure_string(findings, parsed, "office_epithet", office_id=office.office_id)
    federal_role = ensure_string(findings, parsed, "federal_role", office_id=office.office_id)
    office_root_value = ensure_string(findings, parsed, "office_root", office_id=office.office_id)
    playbook_value = ensure_string(findings, parsed, "playbook_path", office_id=office.office_id)
    primary_harness = ensure_string(findings, parsed, "binding.primary_harness", office_id=office.office_id)
    harness_family = ensure_string(findings, parsed, "binding.harness_family", office_id=office.office_id)
    avatar_label = ensure_string(findings, parsed, "binding.avatar_label", office_id=office.office_id)
    surface_class = ensure_string(findings, parsed, "binding.surface_class", office_id=office.office_id)
    may_promote_to = ensure_string_list(findings, parsed, "promotion.may_promote_to", office_id=office.office_id)
    local_only_classes = ensure_string_list(
        findings,
        parsed,
        "promotion.local_only_classes",
        office_id=office.office_id,
    )
    required_sources = ensure_string_list(
        findings,
        parsed,
        "coherence.required_sources",
        office_id=office.office_id,
    )
    required_local_paths = ensure_string_list(
        findings,
        parsed,
        "coherence.required_local_paths",
        office_id=office.office_id,
    )
    ratification_pointer = ensure_string(
        findings,
        parsed,
        "authority.ratification_pointer",
        office_id=office.office_id,
    )
    ratified_path_raw = ensure_string(
        findings,
        parsed,
        "authority.ratified_by_artifact_path",
        office_id=office.office_id,
    )
    ratified_artifact_id = ensure_string(
        findings,
        parsed,
        "authority.ratified_by_artifact_id",
        office_id=office.office_id,
    )
    ratified_at = ensure_string(findings, parsed, "authority.ratified_at", office_id=office.office_id)
    binding_state = ensure_string(findings, parsed, "status.binding_state", office_id=office.office_id)
    contract_state = ensure_string(findings, parsed, "status.contract_state", office_id=office.office_id)
    last_verified_on = ensure_string(findings, parsed, "status.last_verified_on", office_id=office.office_id)

    if schema_version and schema_version != EXPECTED_SCHEMA_VERSION:
        add_finding(
            findings,
            class_name="invalid_contract",
            scope="schema_version",
            office_id=office.office_id,
            message=f"expected {EXPECTED_SCHEMA_VERSION!r}, found {schema_version!r}",
        )

    if office_id and office_id != office.office_id:
        add_finding(
            findings,
            class_name="path_mismatch",
            scope="office_id",
            office_id=office.office_id,
            message=f"office_id {office_id!r} does not match office folder {office.office_id!r}",
        )

    if office_title and office_title != office.office_title:
        add_finding(
            findings,
            class_name="path_mismatch",
            scope="office_title",
            office_id=office.office_id,
            message=f"office_title {office_title!r} does not match AGENTS.md title {office.office_title!r}",
        )

    if office_epithet and office_epithet != office.office_epithet:
        add_finding(
            findings,
            class_name="playbook_contract_contradiction",
            scope="office_epithet",
            office_id=office.office_id,
            message=f"office_epithet {office_epithet!r} does not match AGENTS.md epithet {office.office_epithet!r}",
        )

    if office_root_value:
        resolved_office_root = resolve_repo_path(office_root_value)
        if resolved_office_root != office_root:
            add_finding(
                findings,
                class_name="path_mismatch",
                scope="office_root",
                office_id=office.office_id,
                message=f"office_root must point at {office_root}, found {office_root_value!r}",
            )
        elif not resolved_office_root.exists():
            add_finding(
                findings,
                class_name="path_mismatch",
                scope="office_root",
                office_id=office.office_id,
                message=f"office_root does not exist: {office_root_value!r}",
            )

    if playbook_value:
        resolved_playbook_path = resolve_repo_path(playbook_value)
        if resolved_playbook_path != playbook_path:
            add_finding(
                findings,
                class_name="path_mismatch",
                scope="playbook_path",
                office_id=office.office_id,
                message=f"playbook_path must point at {playbook_path}, found {playbook_value!r}",
            )
        elif not resolved_playbook_path.exists():
            add_finding(
                findings,
                class_name="path_mismatch",
                scope="playbook_path",
                office_id=office.office_id,
                message=f"playbook_path does not exist: {playbook_value!r}",
            )

    if readme_path.exists():
        readme_text = read_text(readme_path)
        if office.office_title not in readme_text or office.office_epithet not in readme_text:
            add_finding(
                findings,
                class_name="playbook_contract_contradiction",
                scope=repo_rel(readme_path),
                office_id=office.office_id,
                message="office README does not repeat the expected title and epithet anchors",
            )
    else:
        add_finding(
            findings,
            class_name="path_mismatch",
            scope=repo_rel(readme_path),
            office_id=office.office_id,
            message="office README is missing",
        )

    if playbook_path.exists():
        playbook_text = read_text(playbook_path)
        if office.office_title not in playbook_text or office.office_epithet not in playbook_text:
            add_finding(
                findings,
                class_name="playbook_contract_contradiction",
                scope=repo_rel(playbook_path),
                office_id=office.office_id,
                message="office playbook does not repeat the expected title and epithet anchors",
            )
    else:
        add_finding(
            findings,
            class_name="path_mismatch",
            scope=repo_rel(playbook_path),
            office_id=office.office_id,
            message="office playbook is missing",
        )

    if primary_harness:
        expected_avatar = certified_harnesses.get(primary_harness)
        if expected_avatar is None:
            add_finding(
                findings,
                class_name="illegal_harness_binding",
                scope="binding.primary_harness",
                office_id=office.office_id,
                message=f"{primary_harness!r} is not a certified harness label from AGENTS.md",
            )
        elif avatar_label and avatar_label != expected_avatar:
            add_finding(
                findings,
                class_name="illegal_harness_binding",
                scope="binding.avatar_label",
                office_id=office.office_id,
                message=f"avatar_label {avatar_label!r} does not match certified avatar {expected_avatar!r}",
            )

        allowed_families = ALLOWED_HARNESS_FAMILIES.get(primary_harness, {expected_harness_family(primary_harness)})
        if harness_family and harness_family not in allowed_families:
            add_finding(
                findings,
                class_name="illegal_harness_binding",
                scope="binding.harness_family",
                office_id=office.office_id,
                message=(
                    f"harness_family {harness_family!r} does not match allowed families "
                    f"{sorted(allowed_families)!r}"
                ),
            )

    if primary_harness and primary_harness.startswith("openclaw_"):
        for dotted_path in ("binding.machine", "binding.provider", "binding.auth_mode"):
            ensure_string(findings, parsed, dotted_path, office_id=office.office_id)

    for lane in may_promote_to:
        if lane not in lane_roots:
            add_finding(
                findings,
                class_name="promotion_scope_drift",
                scope="promotion.may_promote_to",
                office_id=office.office_id,
                message=f"promotion target {lane!r} is not a federal lane root",
            )

    required_source_paths = [resolve_repo_path(value) for value in required_sources]
    if AGENTS_PATH not in required_source_paths:
        add_finding(
            findings,
            class_name="path_mismatch",
            scope="coherence.required_sources",
            office_id=office.office_id,
            message="coherence.required_sources must include AGENTS.md",
        )
    if playbook_path not in required_source_paths:
        add_finding(
            findings,
            class_name="path_mismatch",
            scope="coherence.required_sources",
            office_id=office.office_id,
            message="coherence.required_sources must include the office playbook path",
        )
    for raw_source, source_path in zip(required_sources, required_source_paths, strict=False):
        if not source_path.exists():
            add_finding(
                findings,
                class_name="path_mismatch",
                scope="coherence.required_sources",
                office_id=office.office_id,
                message=f"required source does not exist: {raw_source!r}",
            )

    for rel_path in required_local_paths:
        candidate = office_root / rel_path
        if not candidate.exists():
            add_finding(
                findings,
                class_name="path_mismatch",
                scope="coherence.required_local_paths",
                office_id=office.office_id,
                message=f"required local path missing: {rel_path!r}",
            )

    if ratification_pointer and ratification_pointer != EXPECTED_RATIFICATION_POINTER:
        add_finding(
            findings,
            class_name="authority_pointer_missing",
            scope="authority.ratification_pointer",
            office_id=office.office_id,
            message=(
                f"ratification_pointer must be {EXPECTED_RATIFICATION_POINTER!r}, "
                f"found {ratification_pointer!r}"
            ),
        )

    ratified_path_resolved: Path | None = None
    if ratified_path_raw:
        ratified_path_resolved = resolve_repo_path(ratified_path_raw)
        if ratified_path_resolved != LAW_PATH:
            add_finding(
                findings,
                class_name="authority_pointer_missing",
                scope="authority.ratified_by_artifact_path",
                office_id=office.office_id,
                message=f"ratified_by_artifact_path must point at {LAW_PATH}",
            )
        elif not ratified_path_resolved.exists():
            add_finding(
                findings,
                class_name="authority_pointer_missing",
                scope="authority.ratified_by_artifact_path",
                office_id=office.office_id,
                message=f"ratified_by_artifact_path does not exist: {ratified_path_raw!r}",
            )

    if ratified_artifact_id and ratified_artifact_id != EXPECTED_RATIFIED_ARTIFACT_ID:
        add_finding(
            findings,
            class_name="authority_pointer_missing",
            scope="authority.ratified_by_artifact_id",
            office_id=office.office_id,
            message=(
                f"ratified_by_artifact_id must be {EXPECTED_RATIFIED_ARTIFACT_ID!r}, "
                f"found {ratified_artifact_id!r}"
            ),
        )

    if ratified_at and not DATE_RE.fullmatch(ratified_at):
        add_finding(
            findings,
            class_name="authority_pointer_missing",
            scope="authority.ratified_at",
            office_id=office.office_id,
            message=f"ratified_at must use YYYY-MM-DD, found {ratified_at!r}",
        )

    if last_verified_on and not DATE_RE.fullmatch(last_verified_on):
        add_finding(
            findings,
            class_name="invalid_contract",
            scope="status.last_verified_on",
            office_id=office.office_id,
            message=f"last_verified_on must use YYYY-MM-DD, found {last_verified_on!r}",
        )

    office_findings = findings[start_index:]
    row_errors = [finding for finding in office_findings if finding.level == "error"]
    authority_state = "operative"
    if contract_state != "operative" or row_errors:
        authority_state = "informative_only"

    return {
        "office_id": office.office_id,
        "office_title": office_title or office.office_title,
        "office_epithet": office_epithet or office.office_epithet,
        "federal_role": federal_role,
        "metadata_path": repo_rel(metadata_path),
        "office_root": office_root_value,
        "playbook_path": playbook_value,
        "primary_harness": primary_harness,
        "harness_family": harness_family,
        "avatar_label": avatar_label,
        "surface_class": surface_class,
        "may_promote_to": may_promote_to,
        "local_only_classes": local_only_classes,
        "required_sources": required_sources,
        "required_local_paths": required_local_paths,
        "ratification_pointer": ratification_pointer,
        "ratified_by_artifact_path": ratified_path_raw,
        "ratified_by_artifact_id": ratified_artifact_id,
        "ratified_at": ratified_at,
        "binding_state": binding_state,
        "contract_state": contract_state,
        "validator_state": "clean" if not row_errors else "findings_present",
        "authority_state": authority_state,
        "finding_count": len(office_findings),
        "generated_at": generated_at,
    }


def collect_report() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    agents_text = read_text(AGENTS_PATH)
    offices = parse_federal_offices(agents_text)
    certified_harnesses = parse_certified_harnesses(agents_text)
    lane_roots = parse_lane_roots(agents_text)
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    findings: list[Finding] = []
    records: list[dict[str, Any]] = []

    office_order = {office.office_id: index for index, office in enumerate(offices)}
    for office in offices:
        record = validate_contract(
            office=office,
            certified_harnesses=certified_harnesses,
            lane_roots=lane_roots,
            findings=findings,
            generated_at=generated_at,
        )
        if record is not None:
            records.append(record)

    metadata_glob = REPO_ROOT.glob("offices/*/platform/contracts/OFFICE-HARNESS-METADATA.v1.yaml")
    known_office_ids = {office.office_id for office in offices}
    for path in sorted(metadata_glob):
        office_id = path.parts[-4]
        if office_id not in known_office_ids:
            add_finding(
                findings,
                class_name="path_mismatch",
                scope=repo_rel(path),
                office_id=office_id,
                message="metadata contract exists for an office not declared in AGENTS.md",
            )

    findings_sorted = sorted(
        findings,
        key=lambda item: (
            office_order.get(item.office_id or "", 999),
            item.office_id or "",
            item.class_name,
            item.scope,
            item.message,
        ),
    )
    records_sorted = sorted(records, key=lambda item: office_order.get(item["office_id"], 999))

    errors = [finding for finding in findings_sorted if finding.level == "error"]
    warnings = [finding for finding in findings_sorted if finding.level == "warning"]
    operative_records = [record for record in records_sorted if record["authority_state"] == "operative"]
    informative_records = [record for record in records_sorted if record["authority_state"] == "informative_only"]

    report = {
        "schema_version": "office-harness-coherence-report/v1",
        "generated_at": generated_at,
        "mode": "report-first",
        "repo_root": str(REPO_ROOT),
        "summary": {
            "federal_offices_expected": len(offices),
            "metadata_contracts_found": len(records_sorted),
            "operative_bindings_rendered": len(operative_records),
            "informative_only_bindings_rendered": len(informative_records),
            "finding_count": len(findings_sorted),
            "error_count": len(errors),
            "warning_count": len(warnings),
            "system_state": "report-first-findings-present" if findings_sorted else "coherent",
        },
        "federal_offices": [asdict(office) for office in offices],
        "certified_harnesses": certified_harnesses,
        "lane_roots": sorted(lane_roots),
        "records": records_sorted,
        "findings": [asdict(finding) for finding in findings_sorted],
    }
    return report, records_sorted


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Office-Harness Coherence Report",
        "",
        f"- mode: `{report['mode']}`",
        f"- generated_at: `{report['generated_at']}`",
        f"- federal offices expected: `{summary['federal_offices_expected']}`",
        f"- metadata contracts found: `{summary['metadata_contracts_found']}`",
        f"- operative bindings rendered: `{summary['operative_bindings_rendered']}`",
        f"- informative-only bindings rendered: `{summary['informative_only_bindings_rendered']}`",
        f"- findings: `{summary['finding_count']}`",
        f"- errors: `{summary['error_count']}`",
        f"- warnings: `{summary['warning_count']}`",
        "",
        "## Effective Bindings",
        "",
        "| Office | Harness | Contract State | Authority State | Validator State | Metadata |",
        "|---|---|---|---|---|---|",
    ]

    records: list[dict[str, Any]] = report["records"]
    if not records:
        lines.append("| none | none | none | none | none | none |")
    else:
        for record in records:
            lines.append(
                "| {office_id} | {primary_harness} | {contract_state} | {authority_state} | {validator_state} | `{metadata_path}` |".format(
                    **record
                )
            )

    lines.extend(["", "## Findings", ""])
    findings: list[dict[str, Any]] = report["findings"]
    if not findings:
        lines.append("- none")
    else:
        for finding in findings:
            office_prefix = f"[{finding['office_id']}] " if finding["office_id"] else ""
            lines.append(
                f"- `{finding['class_name']}` {office_prefix}`{finding['scope']}`: {finding['message']}"
            )

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="return non-zero when findings are present")
    args = parser.parse_args()

    report, records = collect_report()
    write_json(REGISTRY_OUT, records)
    write_json(JSON_OUT, report)
    MD_OUT.parent.mkdir(parents=True, exist_ok=True)
    MD_OUT.write_text(render_markdown(report), encoding="utf-8")

    finding_count = report["summary"]["finding_count"]
    error_count = report["summary"]["error_count"]
    warning_count = report["summary"]["warning_count"]
    if args.strict and finding_count:
        for finding in report["findings"]:
            print(
                f"{finding['level'].upper()}: {finding['class_name']}: "
                f"{finding['scope']}: {finding['message']}"
            )
        return 1

    print(
        "Office-harness coherence report written "
        f"({error_count} error(s), {warning_count} warning(s), strict={'on' if args.strict else 'off'})."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

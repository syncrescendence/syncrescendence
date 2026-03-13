#!/usr/bin/env python3
"""Emit verification-ready Acumen dossiers, Augur packets, and queue state."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    from .evidence_family import (
        FORBIDDEN_KEYS,
        FORBIDDEN_SUBSTRINGS,
        REPO_ROOT,
        TRAINING_LEDGER_PATH,
        TRIAGE_LEDGER_PATH,
        load_jsonl,
        repo_rel,
        scan_forbidden_content,
        utc_now,
    )
except ImportError:
    OPS_DIR = Path(__file__).resolve().parents[1]
    if str(OPS_DIR) not in sys.path:
        sys.path.insert(0, str(OPS_DIR))
    from evidence_family import (  # type: ignore[no-redef]
        FORBIDDEN_KEYS,
        FORBIDDEN_SUBSTRINGS,
        REPO_ROOT,
        TRAINING_LEDGER_PATH,
        TRIAGE_LEDGER_PATH,
        load_jsonl,
        repo_rel,
        scan_forbidden_content,
        utc_now,
    )


ELIGIBLE_DECISIONS = {"Promote", "Flag-for-Primary"}
DECISION_PRIORITY = {
    "Flag-for-Primary": 0,
    "Promote": 1,
}
QUEUE_STATUS_ORDER = {
    "awaiting_dispatch": 0,
    "awaiting_response": 1,
    "response_landed_uningested": 2,
    "response_ingested": 3,
}

DOSSIER_SCHEMA_VERSION = "acumen.verification.dossier/v1"
BRIDGE_SCHEMA_VERSION = "acumen.verification.bridge/v2"
PORTFOLIO_SCHEMA_VERSION = "acumen.verification.portfolio/v1"

DEFAULT_DOSSIER_DIR = REPO_ROOT / "runtime" / "acumen" / "out" / "verification-dossiers"
DEFAULT_BRIDGE_STATUS = REPO_ROOT / "orchestration" / "state" / "ACUMEN-AUGUR-VERIFICATION-BRIDGE.json"
DEFAULT_PORTFOLIO_JSON = REPO_ROOT / "runtime" / "acumen" / "out" / "verification-portfolio.json"
DEFAULT_PORTFOLIO_MD = REPO_ROOT / "runtime" / "acumen" / "out" / "verification-portfolio.md"
DEFAULT_SANDBOX_LEDGER = REPO_ROOT / "orchestration" / "state" / "SANDBOX-EVENT-LEDGER.jsonl"

PROMPTS_DIR = REPO_ROOT / "communications" / "prompts"
RESPONSES_DIR = REPO_ROOT / "communications" / "responses"
ASSESSMENTS_DIR = REPO_ROOT / "communications" / "assessments"
ASSESSMENT_JSON_DIR = REPO_ROOT / "runtime" / "acumen" / "out" / "augur-return-assessments"
PRIMARY_QUEUE_JSON = REPO_ROOT / "orchestration" / "state" / "ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.json"
PRIMARY_QUEUE_MD = REPO_ROOT / "orchestration" / "state" / "ACUMEN-AUGUR-PRIMARY-SOURCE-QUEUE.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--triage-ledger", default=str(TRIAGE_LEDGER_PATH))
    parser.add_argument("--training-ledger", default=str(TRAINING_LEDGER_PATH))
    parser.add_argument("--sandbox-ledger", default=str(DEFAULT_SANDBOX_LEDGER))
    parser.add_argument("--dossier-dir", default=str(DEFAULT_DOSSIER_DIR))
    parser.add_argument("--bridge-status-json", default=str(DEFAULT_BRIDGE_STATUS))
    parser.add_argument("--portfolio-json", default=str(DEFAULT_PORTFOLIO_JSON))
    parser.add_argument("--portfolio-md", default=str(DEFAULT_PORTFOLIO_MD))
    parser.add_argument("--decision", action="append", dest="decisions", default=[])
    parser.add_argument("--video-id", action="append", dest="video_ids", default=[])
    parser.add_argument("--triage-event-id", action="append", dest="triage_event_ids", default=[])
    parser.add_argument("--include-ingested", action="store_true")
    parser.add_argument("--max-items", type=int, default=None)
    return parser.parse_args()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def shorten_text(value: str | None, limit: int = 240) -> str | None:
    if value is None:
        return None
    text = " ".join(str(value).split())
    if not text:
        return None
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def resolve_repo_path(raw_value: str | None) -> Path | None:
    if not raw_value:
        return None
    candidate = Path(raw_value)
    if candidate.is_absolute():
        return candidate.resolve()
    return (REPO_ROOT / raw_value).resolve()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def packet_format_for(path: Path | None) -> str:
    if path is None:
        return "missing"
    suffix = path.suffix.lower()
    if suffix == ".json":
        return "json"
    if suffix == ".md":
        return "markdown"
    return suffix.lstrip(".") or "unknown"


def parse_packet_metadata(packet_path: Path | None) -> dict[str, str | None]:
    if packet_path is None or not packet_path.exists():
        return {
            "packet_format": packet_format_for(packet_path),
            "title": None,
            "duration": None,
            "description": None,
            "initial_transcript": None,
            "published_at": None,
            "source_url": None,
        }

    if packet_path.suffix.lower() == ".json":
        payload = json.loads(packet_path.read_text(encoding="utf-8"))
        video = payload.get("video", {}) if isinstance(payload, dict) else {}
        return {
            "packet_format": "json",
            "title": shorten_text(video.get("title")),
            "duration": shorten_text(video.get("duration"), limit=64),
            "description": shorten_text(video.get("description")),
            "initial_transcript": shorten_text(video.get("initial_transcript")),
            "published_at": shorten_text(video.get("published_at"), limit=64),
            "source_url": shorten_text(video.get("source_url")),
        }

    body = packet_path.read_text(encoding="utf-8")
    metadata: dict[str, str | None] = {
        "packet_format": "markdown",
        "title": None,
        "duration": None,
        "description": None,
        "initial_transcript": None,
        "published_at": None,
        "source_url": None,
    }
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("- Title: "):
            metadata["title"] = shorten_text(line.removeprefix("- Title: "))
        elif line.startswith("- Duration: "):
            metadata["duration"] = shorten_text(line.removeprefix("- Duration: "), limit=64)
        elif line.startswith("- Description: "):
            metadata["description"] = shorten_text(line.removeprefix("- Description: "))
        elif line.startswith("- First 60s transcript: "):
            metadata["initial_transcript"] = shorten_text(line.removeprefix("- First 60s transcript: "))
    return metadata


def research_questions_for(decision: str, title: str) -> list[str]:
    title_hint = f" for {title}" if title else ""
    common = [
        f"What official docs, release notes, papers, transcripts, or first-party statements best verify the central claims or framing{title_hint}?",
        "What current-reality context, releases, product-surface changes, or organizational shifts most affect interpretation of this item?",
        "What source-backed corrections, caveats, or disconfirming evidence should the repo carry forward?",
    ]
    if decision == "Flag-for-Primary":
        common.append("What original-form or near-original witnesses should flank the primary review so later synthesis has the right context?")
    else:
        common.append("If the signal holds, what are the strongest follow-on source trails a stronger reasoning surface should read next?")
    return common


def verification_focus_for(decision: str) -> list[str]:
    if decision == "Flag-for-Primary":
        return [
            "perform source discovery around the flagged item",
            "map the primary-source terrain around the flagged item",
            "identify what must be consumed in original form",
            "run current-reality verification on surrounding context without replacing the primary review",
        ]
    return [
        "perform source discovery around the promoted signal",
        "verify whether the promoted signal stands up against primary or near-primary sources",
        "run current-reality checks that strengthen or weaken the escalation rationale",
        "prepare a citation-bearing handoff for later higher-order research passes",
    ]


def prompt_body_for(dossier: dict[str, Any], *, augur_packet_path: Path, augur_response_path: Path) -> str:
    decision = dossier["decision_metadata"]
    source = dossier["source_summary"]
    sovereignty = dossier["repo_sovereignty"]
    title = source.get("title") or decision.get("title") or dossier["dossier_id"]
    lines = [
        f"# Augur Verification Packet — {title}",
        "",
        "- Surface: `perplexity_web_surface`",
        "- Packet type: `acumen_verification_bridge`",
        f"- Created: `{utc_now()}`",
        f"- Source dossier: `{dossier['paths']['dossier_path']}`",
        f"- Source triage packet: `{dossier['paths']['source_packet_path']}`",
        f"- Return artifact: `{repo_rel(augur_response_path)}`",
        f"- Repo assessment artifact: `{dossier['paths']['assessment_md_path']}`",
        f"- Primary-source queue: `{dossier['paths']['queue_md_path']}`",
        f"- Intake sovereignty: `{sovereignty['intake_authority']} {sovereignty['external_role']}`",
        f"- Repo sovereignty: `{sovereignty['repo_state_rule']}`",
        "- Drafting mode: `reconnaissance_only`",
        "",
        "## Decision Context",
        "",
        f"- Decision: `{decision['decision']}`",
        f"- Priority band: `{decision['priority_band']}`",
        f"- Target depth: `{decision['target_depth']}`",
        f"- Target polish: `{decision['target_polish']}`",
        f"- Suggested consumption: `{decision['suggested_consumption']}`",
        f"- Rationale: {decision['rationale']}",
    ]
    if decision.get("primary_flag_reason"):
        lines.append(f"- Primary-flag reason: {decision['primary_flag_reason']}")
    lines.extend(
        [
            "",
            "## Source Summary",
            "",
            f"- Channel: `{source['channel_name']}` (`{source['channel_id']}`)",
            f"- Video ID: `{source['video_id']}`",
            f"- Duration: `{source['duration'] or 'unknown'}`",
            f"- Input summary: {source['input_summary']}",
        ]
    )
    if source.get("description_excerpt"):
        lines.append(f"- Description excerpt: {source['description_excerpt']}")
    if source.get("transcript_excerpt"):
        lines.append(f"- Transcript excerpt: {source['transcript_excerpt']}")
    if source.get("published_at"):
        lines.append(f"- Published at: `{source['published_at']}`")
    if source.get("source_url"):
        lines.append(f"- Source URL: `{source['source_url']}`")

    lines.extend(["", "## Verification Objectives", ""])
    lines.extend(f"- {item}" for item in dossier["verification_focus"])
    lines.extend(["", "## Verification Questions", ""])
    lines.extend(f"- {item}" for item in dossier["research_questions"])
    lines.extend(
        [
            "",
            "## Acceptable Source Classes",
            "",
            "- Primary sources first: official pages, product docs, papers, release notes, transcripts, or first-party statements.",
            "- Source discovery is part of the task; identify the strongest witnesses before drawing conclusions.",
            "- Near-primary reporting only when it materially sharpens source discovery or current-reality checks.",
            "- Distinguish verified fact from inference and name any unresolved ambiguity.",
            "",
            "## Not Requested",
            "",
            "- Do not write a final brief or polished doctrine artifact.",
            "- Do not reinterpret repo state or override Acumen's triage decision.",
            "- Do not treat citation count alone as proof.",
            "",
            "## Return Contract",
            "",
            "- This is a verification input, not a final draft.",
            "- Structure the return so later research passes can reuse it.",
            "- Use exactly this structure:",
            "- 1. Source Terrain",
            "- 2. Current-Reality Checks",
            "- 3. Disconfirming Or Complicating Evidence",
            "- 4. Sources To Read Next",
            "- 5. Confidence And Gaps",
            "- Include verified facts with citations and label any inference clearly.",
            "",
            "## Return Instructions",
            "",
            f"- Save or relay the response back into `{repo_rel(augur_response_path)}`",
            "- Keep citations intact in the returned artifact.",
            "- After the response lands, rebuild the repo-side assessment and primary-source queue.",
            "",
            "## Repo Return Commands",
            "",
            "```bash",
            "python3 operators/cli-web-gap/perplexity_response_bridge.py "
            f"--dispatch {repo_rel(augur_packet_path)} "
            f"--response {repo_rel(augur_response_path)} "
            '--summary "<one-line landing summary>"',
            f"python3 operators/acumen/ingest_augur_returns.py --video-id {source['video_id']}",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def matches_filters(
    event: dict[str, Any],
    *,
    decisions: set[str],
    video_ids: set[str],
    triage_event_ids: set[str],
) -> bool:
    record = event.get("decision_record", {})
    decision = str(record.get("decision", ""))
    if decisions and decision not in decisions:
        return False
    if video_ids and str(record.get("video_id", "")) not in video_ids:
        return False
    if triage_event_ids and str(record.get("triage_event_id", "")) not in triage_event_ids:
        return False
    return True


def load_response_receipts(sandbox_ledger: Path) -> dict[str, dict[str, Any]]:
    receipts: dict[str, dict[str, Any]] = {}
    for row in load_jsonl(sandbox_ledger):
        if not isinstance(row, dict) or row.get("type") != "perplexity_response_landed":
            continue
        payload = row.get("payload", {})
        if not isinstance(payload, dict):
            continue
        response_artifact = payload.get("response_artifact")
        if not isinstance(response_artifact, str) or not response_artifact.strip():
            continue
        emitted_at = str(row.get("emitted_at", "")).strip()
        current = receipts.get(response_artifact)
        if current is None or emitted_at > str(current.get("emitted_at", "")):
            receipts[response_artifact] = row
    return receipts


def inspect_item_state(
    *,
    dossier_path: Path,
    augur_packet_path: Path,
    augur_response_path: Path,
    response_receipts: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    dossier_exists = dossier_path.exists()
    packet_exists = augur_packet_path.exists()
    response_exists = augur_response_path.exists()
    response_repo_path = repo_rel(augur_response_path)
    receipt = response_receipts.get(response_repo_path)
    response_event_exists = receipt is not None
    response_event_emitted_at = str(receipt.get("emitted_at")) if receipt is not None else None

    if response_event_exists:
        queue_status = "response_ingested"
    elif response_exists:
        queue_status = "response_landed_uningested"
    elif packet_exists:
        queue_status = "awaiting_response"
    else:
        queue_status = "awaiting_dispatch"

    return {
        "queue_status": queue_status,
        "is_open": queue_status != "response_ingested",
        "dossier_exists": dossier_exists,
        "augur_packet_exists": packet_exists,
        "augur_response_exists": response_exists,
        "augur_response_event_exists": response_event_exists,
        "augur_response_event_emitted_at": response_event_emitted_at,
    }


def build_dossier(
    triage_event: dict[str, Any],
    training_index: dict[str, dict[str, Any]],
    *,
    dossier_dir: Path,
) -> tuple[dict[str, Any], Path, Path, Path]:
    record = triage_event["decision_record"]
    triage_event_id = str(record["triage_event_id"])
    video_id = str(record.get("video_id") or triage_event_id)
    slug = slugify(video_id or triage_event_id or str(record.get("title", "verification-item")))
    model_call_event_id = str(record.get("model_call_event_id", "")).strip()
    training_event = training_index.get(model_call_event_id, {})
    training_record = training_event.get("training_record", {}) if isinstance(training_event, dict) else {}
    packet_provenance = triage_event.get("packet_provenance", {})
    packet_path = resolve_repo_path(packet_provenance.get("packet_path"))
    packet_metadata = parse_packet_metadata(packet_path)

    augur_packet_path = PROMPTS_DIR / f"PACKET-PERPLEXITY-acumen-{slug}.md"
    augur_response_path = RESPONSES_DIR / f"RESPONSE-PERPLEXITY-acumen-{slug}.md"
    dossier_path = dossier_dir / f"{slug}.json"
    assessment_json_path = ASSESSMENT_JSON_DIR / f"{slug}.json"
    assessment_md_path = ASSESSMENTS_DIR / f"ACUMEN-AUGUR-RETURN-ASSESSMENT-{slug}.md"

    source_summary = {
        "title": shorten_text(packet_metadata.get("title") or record.get("title")),
        "channel_name": shorten_text(record.get("channel_name"), limit=120),
        "channel_id": shorten_text(record.get("channel_id"), limit=128),
        "video_id": shorten_text(record.get("video_id"), limit=160),
        "duration": shorten_text(packet_metadata.get("duration"), limit=64),
        "published_at": shorten_text(packet_metadata.get("published_at"), limit=64),
        "source_url": shorten_text(packet_metadata.get("source_url")),
        "input_summary": shorten_text(
            packet_provenance.get("input_summary")
            or training_record.get("prompt_capture", {}).get("input_summary")
            or record.get("abstract"),
            limit=320,
        ),
        "description_excerpt": shorten_text(packet_metadata.get("description")),
        "transcript_excerpt": shorten_text(packet_metadata.get("initial_transcript")),
    }

    dossier = {
        "schema_version": DOSSIER_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "dossier_id": f"acumen-dossier-{slug}",
        "bridge_surface": "acumen_to_augur_verification",
        "triage_surface": "acumen",
        "verification_surface": "Augur / Perplexity",
        "verification_status": "ready",
        "repo_sovereignty": {
            "intake_authority": "Acumen remains the intake and triage plane.",
            "external_role": "Augur is downstream verification only.",
            "repo_state_rule": "Repo-local decision metadata and source packet provenance remain authoritative for repo state.",
        },
        "decision_metadata": {
            "triage_event_id": triage_event_id,
            "model_call_event_id": model_call_event_id or None,
            "decision": record["decision"],
            "priority_band": record.get("priority_band"),
            "target_depth": record.get("target_depth"),
            "target_polish": record.get("target_polish"),
            "suggested_consumption": record.get("suggested_consumption"),
            "rationale": record.get("rationale"),
            "primary_flag_reason": record.get("primary_flag_reason"),
            "title": record.get("title"),
            "channel_name": record.get("channel_name"),
            "recorded_at": record.get("recorded_at") or triage_event.get("recorded_at"),
        },
        "source_summary": source_summary,
        "source_packet": {
            "packet_path": repo_rel(packet_path) if packet_path is not None and packet_path.exists() else packet_provenance.get("packet_path"),
            "packet_sha256": packet_provenance.get("packet_sha256"),
            "packet_format": packet_metadata["packet_format"],
            "exists": bool(packet_path and packet_path.exists()),
        },
        "training_context": {
            "provider": training_record.get("provider"),
            "model": training_record.get("model"),
            "request_context": training_record.get("request_context", {}),
            "usage": training_record.get("usage", {}),
            "cost": training_record.get("cost", {}),
            "response_capture": training_record.get("response_capture", {}),
        },
        "policy": {
            "triage_policy": triage_event.get("policy", {}),
            "training_policy": training_event.get("policy", {}) if isinstance(training_event, dict) else {},
            "forbidden_keys": sorted(FORBIDDEN_KEYS),
            "forbidden_substring_count": len(FORBIDDEN_SUBSTRINGS),
        },
        "verification_focus": verification_focus_for(str(record["decision"])),
        "research_questions": research_questions_for(str(record["decision"]), str(source_summary["title"] or "")),
        "higher_order_handoff": {
            "recommended_consumers": [
                "Augur verification",
                "later synthesis or research passes that consume the returned citations",
            ],
            "required_reuse_fields": [
                "verified_facts",
                "disputed_or_unresolved_points",
                "sources_to_read_next",
                "follow_on_research_directions",
            ],
        },
        "paths": {
            "dossier_path": repo_rel(dossier_path),
            "source_packet_path": repo_rel(packet_path) if packet_path is not None and packet_path.exists() else packet_provenance.get("packet_path"),
            "augur_packet_path": repo_rel(augur_packet_path),
            "augur_response_path": repo_rel(augur_response_path),
            "assessment_json_path": repo_rel(assessment_json_path),
            "assessment_md_path": repo_rel(assessment_md_path),
            "queue_json_path": repo_rel(PRIMARY_QUEUE_JSON),
            "queue_md_path": repo_rel(PRIMARY_QUEUE_MD),
            "triage_ledger_path": None,
            "training_ledger_path": None,
        },
    }
    findings = scan_forbidden_content(dossier, scope="dossier")
    if findings:
        raise SystemExit("\n".join(findings))
    return dossier, dossier_path, augur_packet_path, augur_response_path


def triage_sort_key(event: dict[str, Any]) -> tuple[int, str, str]:
    record = event.get("decision_record", {})
    decision = str(record.get("decision", ""))
    recorded_at = str(record.get("recorded_at") or event.get("recorded_at") or "")
    triage_event_id = str(record.get("triage_event_id") or event.get("event_id") or "")
    return (DECISION_PRIORITY.get(decision, 99), recorded_at, triage_event_id)


def render_portfolio_markdown(portfolio: dict[str, Any]) -> str:
    counts = portfolio["counts"]
    selection = portfolio["selection"]
    lines = [
        "# Acumen Augur Verification Portfolio",
        "",
        f"- Generated at: `{portfolio['generated_at']}`",
        f"- Source bridge JSON: `{portfolio['source_bridge_json']}`",
        f"- Eligible items: `{counts['eligible_items_total']}`",
        f"- Open queue: `{counts['open_items_total']}`",
        f"- Selected in this batch: `{selection['selected_batch_items']}`",
        f"- Remaining open after this batch: `{selection['remaining_open_after_batch']}`",
        f"- Awaiting dispatch: `{counts['awaiting_dispatch']}`",
        f"- Awaiting response: `{counts['awaiting_response']}`",
        f"- Response landed, still uningested: `{counts['response_landed_uningested']}`",
        f"- Response ingested: `{counts['response_ingested']}`",
        "",
        "## Batch Rules",
        "",
        "- Eligibility: only `Promote` and `Flag-for-Primary` decision records from Acumen may enter this portfolio.",
        "- Ordering: `Flag-for-Primary` items sort ahead of `Promote`, then older triage timestamps drain first.",
        "- Default selection: open items only; already ingested items remain visible in the portfolio but are not rewritten unless `--include-ingested` is used.",
        f"- Current selection mode: `{selection['selection_mode']}`",
        f"- Current max items: `{selection['max_items'] if selection['max_items'] is not None else 'unbounded'}`",
        "",
        "## Queue",
        "",
    ]
    if portfolio["items"]:
        for item in portfolio["items"]:
            lines.append(
                "- "
                f"`#{item['queue_rank']}` "
                f"`{item['video_id']}` "
                f"decision=`{item['decision']}` "
                f"status=`{item['queue_status']}` "
                f"selected_in_batch=`{str(item['selected_in_batch']).lower()}` "
                f"response_ingested=`{str(not item['is_open']).lower()}` "
                f"packet=`{item['augur_packet_path']}` "
                f"response=`{item['augur_response_path']}`"
            )
    else:
        lines.append("- no eligible items")
    lines.append("")
    return "\n".join(lines)


def compute_counts(items: list[dict[str, Any]], *, selected_batch_items: int) -> dict[str, int]:
    counts = {
        "eligible_items_total": len(items),
        "open_items_total": 0,
        "selected_batch_items": selected_batch_items,
        "remaining_open_after_batch": 0,
        "awaiting_dispatch": 0,
        "awaiting_response": 0,
        "response_landed_uningested": 0,
        "response_ingested": 0,
        "promote_open_items": 0,
        "primary_flagged_open_items": 0,
        "dossiers_written": selected_batch_items,
        "augur_packets_written": selected_batch_items,
        "eligible_items_written": selected_batch_items,
    }
    for item in items:
        status = str(item["queue_status"])
        counts[status] += 1
        if item["is_open"]:
            counts["open_items_total"] += 1
            if item["decision"] == "Promote":
                counts["promote_open_items"] += 1
            if item["decision"] == "Flag-for-Primary":
                counts["primary_flagged_open_items"] += 1
            if not item["selected_in_batch"]:
                counts["remaining_open_after_batch"] += 1
    return counts


def main() -> int:
    args = parse_args()
    if args.max_items is not None and args.max_items <= 0:
        raise SystemExit("--max-items must be greater than zero")

    triage_ledger = Path(args.triage_ledger).expanduser().resolve()
    training_ledger = Path(args.training_ledger).expanduser().resolve()
    sandbox_ledger = Path(args.sandbox_ledger).expanduser().resolve()
    dossier_dir = Path(args.dossier_dir).expanduser().resolve()
    bridge_status_path = Path(args.bridge_status_json).expanduser().resolve()
    portfolio_json_path = Path(args.portfolio_json).expanduser().resolve()
    portfolio_md_path = Path(args.portfolio_md).expanduser().resolve()

    decisions = set(args.decisions or ELIGIBLE_DECISIONS)
    invalid_decisions = decisions - ELIGIBLE_DECISIONS
    if invalid_decisions:
        raise SystemExit(f"unsupported decisions: {sorted(invalid_decisions)}")

    triage_rows = load_jsonl(triage_ledger)
    training_rows = load_jsonl(training_ledger)
    response_receipts = load_response_receipts(sandbox_ledger)

    training_index = {
        str(row.get("event_id", "")): row
        for row in training_rows
        if isinstance(row, dict) and row.get("event_type") in {"model_call_recorded", "model_call_failed"}
    }

    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    RESPONSES_DIR.mkdir(parents=True, exist_ok=True)
    dossier_dir.mkdir(parents=True, exist_ok=True)

    eligible_events = [
        row
        for row in triage_rows
        if isinstance(row, dict)
        and row.get("event_type") == "decision_recorded"
        and isinstance(row.get("decision_record"), dict)
        and str(row["decision_record"].get("decision", "")) in ELIGIBLE_DECISIONS
        and matches_filters(
            row,
            decisions=decisions,
            video_ids=set(args.video_ids),
            triage_event_ids=set(args.triage_event_ids),
        )
    ]
    eligible_events.sort(key=triage_sort_key)

    candidates: list[dict[str, Any]] = []
    for event in eligible_events:
        dossier, dossier_path, augur_packet_path, augur_response_path = build_dossier(
            event,
            training_index,
            dossier_dir=dossier_dir,
        )
        dossier["paths"]["triage_ledger_path"] = repo_rel(triage_ledger)
        dossier["paths"]["training_ledger_path"] = repo_rel(training_ledger)
        state = inspect_item_state(
            dossier_path=dossier_path,
            augur_packet_path=augur_packet_path,
            augur_response_path=augur_response_path,
            response_receipts=response_receipts,
        )
        candidates.append(
            {
                "event": event,
                "dossier": dossier,
                "dossier_path": dossier_path,
                "augur_packet_path": augur_packet_path,
                "augur_response_path": augur_response_path,
                "state": state,
            }
        )

    selected_candidates: list[dict[str, Any]] = []
    for candidate in candidates:
        if not args.include_ingested and not candidate["state"]["is_open"]:
            continue
        selected_candidates.append(candidate)
        if args.max_items is not None and len(selected_candidates) >= args.max_items:
            break

    written_paths: list[Path] = []
    selected_ids = {
        str(candidate["dossier"]["decision_metadata"]["triage_event_id"])
        for candidate in selected_candidates
    }
    for candidate in selected_candidates:
        write_json(candidate["dossier_path"], candidate["dossier"])
        packet_body = prompt_body_for(
            candidate["dossier"],
            augur_packet_path=candidate["augur_packet_path"],
            augur_response_path=candidate["augur_response_path"],
        )
        candidate["augur_packet_path"].write_text(packet_body + "\n", encoding="utf-8")
        written_paths.extend([candidate["dossier_path"], candidate["augur_packet_path"]])

    items: list[dict[str, Any]] = []
    for rank, candidate in enumerate(candidates, start=1):
        state = inspect_item_state(
            dossier_path=candidate["dossier_path"],
            augur_packet_path=candidate["augur_packet_path"],
            augur_response_path=candidate["augur_response_path"],
            response_receipts=response_receipts,
        )
        record = candidate["event"]["decision_record"]
        item = {
            "queue_rank": rank,
            "batch_priority": DECISION_PRIORITY.get(str(record.get("decision", "")), 99),
            "triage_event_id": candidate["dossier"]["decision_metadata"]["triage_event_id"],
            "model_call_event_id": candidate["dossier"]["decision_metadata"]["model_call_event_id"],
            "decision": candidate["dossier"]["decision_metadata"]["decision"],
            "priority_band": candidate["dossier"]["decision_metadata"]["priority_band"],
            "recorded_at": candidate["dossier"]["decision_metadata"]["recorded_at"],
            "title": candidate["dossier"]["source_summary"]["title"],
            "video_id": candidate["dossier"]["source_summary"]["video_id"],
            "dossier_path": repo_rel(candidate["dossier_path"]),
            "source_packet_path": candidate["dossier"]["source_packet"]["packet_path"],
            "augur_packet_path": repo_rel(candidate["augur_packet_path"]),
            "augur_response_path": repo_rel(candidate["augur_response_path"]),
            "assessment_json_path": candidate["dossier"]["paths"]["assessment_json_path"],
            "assessment_md_path": candidate["dossier"]["paths"]["assessment_md_path"],
            "selected_in_batch": candidate["dossier"]["decision_metadata"]["triage_event_id"] in selected_ids,
            **state,
        }
        items.append(item)

    counts = compute_counts(items, selected_batch_items=len(selected_candidates))
    selection = {
        "selection_mode": "open_and_ingested_items" if args.include_ingested else "open_items_only",
        "max_items": args.max_items,
        "selected_batch_items": len(selected_candidates),
        "remaining_open_after_batch": counts["remaining_open_after_batch"],
        "selected_triage_event_ids": sorted(selected_ids),
    }
    batch_rules = {
        "eligibility": sorted(ELIGIBLE_DECISIONS),
        "selection_surface": "Acumen remains the intake and triage plane; Augur receives only downstream verification work.",
        "default_batch_scope": "open_items_only",
        "override_flag": "--include-ingested",
        "ordering": [
            "Flag-for-Primary before Promote",
            "older triage timestamps first within the same decision class",
        ],
        "close_condition": "A batch item closes only after the Augur response artifact exists and a `perplexity_response_landed` event records its ingestion.",
        "sanitization_rule": "Packets and dossiers remain sanitized and pointer-carrying; source packet provenance stays authoritative for repo state.",
    }
    runtime_surfaces = {
        "portfolio_json": repo_rel(portfolio_json_path),
        "portfolio_md": repo_rel(portfolio_md_path),
    }

    bridge_status = {
        "schema_version": BRIDGE_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "triage_ledger": repo_rel(triage_ledger),
        "training_ledger": repo_rel(training_ledger),
        "sandbox_event_ledger": repo_rel(sandbox_ledger) if sandbox_ledger.exists() else None,
        "eligible_decisions": sorted(ELIGIBLE_DECISIONS),
        "selected_decisions": sorted(decisions),
        "selected_video_ids": sorted(set(args.video_ids)),
        "selected_triage_event_ids": sorted(set(args.triage_event_ids)),
        "dossier_dir": repo_rel(dossier_dir),
        "batch_rules": batch_rules,
        "selection": selection,
        "runtime_surfaces": runtime_surfaces,
        "counts": counts,
        "items": items,
    }
    findings = scan_forbidden_content(bridge_status, scope="bridge_status")
    if findings:
        raise SystemExit("\n".join(findings))
    write_json(bridge_status_path, bridge_status)
    written_paths.append(bridge_status_path)

    portfolio = {
        "schema_version": PORTFOLIO_SCHEMA_VERSION,
        "generated_at": utc_now(),
        "source_bridge_json": repo_rel(bridge_status_path),
        "batch_rules": batch_rules,
        "selection": selection,
        "counts": counts,
        "items": items,
    }
    findings = scan_forbidden_content(portfolio, scope="portfolio")
    if findings:
        raise SystemExit("\n".join(findings))
    write_json(portfolio_json_path, portfolio)
    portfolio_md_path.parent.mkdir(parents=True, exist_ok=True)
    portfolio_md_path.write_text(render_portfolio_markdown(portfolio), encoding="utf-8")
    written_paths.extend([portfolio_json_path, portfolio_md_path])

    for path in written_paths:
        print(repo_rel(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

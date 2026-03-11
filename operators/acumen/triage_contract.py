#!/usr/bin/env python3
"""Shared contracts for Acumen triage packets and decision records."""

from __future__ import annotations

from datetime import UTC, datetime
import hashlib
import json
from pathlib import Path
from typing import Any

from registry_contract import validate_channel


PACKET_SCHEMA_VERSION = "acumen.triage.packet/v1"
DECISION_SCHEMA_VERSION = "acumen.triage.decision/v1"

DECISION_VALUES = ("Skip", "Headline", "Compress", "Promote", "Flag-for-Primary")
TARGET_DEPTH_VALUES = ("None", "Headline", "Abstract", "Precis", "Synopsis", "Blueprint", "Treatment", "Transcript")
TARGET_POLISH_VALUES = ("clean_verbatim", "charitable", "editorial")
REQUIRED_VIDEO_FIELDS = ("title", "duration", "description", "initial_transcript")

DECISION_SET = set(DECISION_VALUES)
TARGET_DEPTH_SET = set(TARGET_DEPTH_VALUES)
TARGET_POLISH_SET = set(TARGET_POLISH_VALUES)
DEPTH_RANK = {value: index for index, value in enumerate(TARGET_DEPTH_VALUES)}
POLISH_RANK = {value: index for index, value in enumerate(TARGET_POLISH_VALUES)}

SYSTEM_INSTRUCTION = (
    "You are an Acumen triage engine. Read the packet, classify the upload, and return "
    "only strict JSON that matches the supplied schema."
)

USER_PROMPT_TEMPLATE = """Packet ID: {packet_id}

Context from registry:
- Channel: {name} | Genre: {genre} | Priority: {priority_band}
- Default compression: {default_compression} | Default polish: {default_polish}
- Signal density: {signal_density}
- Visual dependency: {visual_dependency} | Voice normalization: {voice_normalization}
- Cadence: {cadence} | Chain alignment: {chain_alignment}
- Domain tags: {domain_tags}
- Resolution vocabulary: {resolution_vocabulary}

Video metadata:
- Title: {title}
- Duration: {duration}
- Description: {description}
- First 60s transcript: {initial_transcript}

Strict output contract:
- Return a JSON object with exactly these keys in this order:
  decision, target_depth, target_polish, rationale, primary_flag_reason
- rationale must be one sentence explaining the signal that was detected or missing.
- primary_flag_reason must be null unless decision is Flag-for-Primary.

Hard coupling rules:
1. Skip => target_depth=None, target_polish=clean_verbatim, primary_flag_reason=null.
2. Headline => target_depth=Headline, target_polish=clean_verbatim, primary_flag_reason=null.
3. Compress => target_depth={default_compression}, target_polish={default_polish}, primary_flag_reason=null.
4. Promote => raise target_depth or target_polish above the channel defaults.
5. Flag-for-Primary => target_depth=Transcript, target_polish=clean_verbatim, and primary_flag_reason must explain why original-form consumption is required.

Decision rules:
1. Skip: Bulletin content restating existing news with no novel signal.
2. Headline: Low-signal content from medium/high-density channels worth logging.
3. Compress: Standard content processed at channel defaults.
4. Promote: Override defaults upward when a lower-tier channel hosts a Tier 1 guest, covers a paradigm shift, or produces unusually deep analysis.
5. Flag-for-Primary: Content where compression destroys signal, such as live debates with performative dynamics, hardware teardowns, visually dependent demonstrations, or events where the practitioner's own judgment is required.
"""

DECISION_JSON_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "decision",
        "target_depth",
        "target_polish",
        "rationale",
        "primary_flag_reason",
    ],
    "propertyOrdering": [
        "decision",
        "target_depth",
        "target_polish",
        "rationale",
        "primary_flag_reason",
    ],
    "properties": {
        "decision": {
            "type": "string",
            "enum": list(DECISION_VALUES),
        },
        "target_depth": {
            "type": "string",
            "enum": list(TARGET_DEPTH_VALUES),
        },
        "target_polish": {
            "type": "string",
            "enum": list(TARGET_POLISH_VALUES),
        },
        "rationale": {
            "type": "string",
            "minLength": 1,
            "maxLength": 240,
        },
        "primary_flag_reason": {
            "type": ["string", "null"],
            "maxLength": 240,
        },
    },
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).expanduser().read_text(encoding="utf-8"))


def write_json(path: str | Path, payload: dict[str, Any]) -> Path:
    output_path = Path(path).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return output_path


def append_jsonl(path: str | Path, payload: dict[str, Any]) -> Path:
    output_path = Path(path).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
    return output_path


def resolve_channel(registry: dict[str, Any], channel_id: str) -> dict[str, Any]:
    for channel in registry.get("channels", []):
        if str(channel.get("channel_id")) == channel_id:
            return dict(channel)
    raise SystemExit(f"channel not found in registry: {channel_id}")


def normalize_video_metadata(video: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(video)
    for field in REQUIRED_VIDEO_FIELDS:
        normalized[field] = str(normalized.get(field, "")).strip()
    return normalized


def validate_video(video: Any, *, require_non_empty: bool = False) -> list[str]:
    if not isinstance(video, dict):
        return ["video metadata must be a JSON object"]

    errors: list[str] = []
    missing = [field for field in REQUIRED_VIDEO_FIELDS if field not in video]
    if missing:
        errors.append(f"video metadata missing required keys: {sorted(missing)}")
        return errors

    if require_non_empty:
        blank = [field for field in REQUIRED_VIDEO_FIELDS if not str(video.get(field, "")).strip()]
        if blank:
            errors.append(f"video metadata has blank required values: {sorted(blank)}")
    return errors


def _packet_id_basis(channel: dict[str, Any], video: dict[str, Any]) -> bytes:
    payload = {
        "channel": {
            "channel_id": channel.get("channel_id"),
            "name": channel.get("name"),
            "genre": channel.get("genre"),
            "cadence": channel.get("cadence"),
            "default_compression": channel.get("default_compression"),
            "default_polish": channel.get("default_polish"),
            "signal_density": channel.get("signal_density"),
            "visual_dependency": channel.get("visual_dependency"),
            "voice_normalization": channel.get("voice_normalization"),
            "domain_tags": channel.get("domain_tags", []),
            "chain_alignment": channel.get("chain_alignment"),
            "resolution_vocabulary": channel.get("resolution_vocabulary", []),
            "priority_band": channel.get("priority_band"),
        },
        "video": video,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def make_packet_id(channel: dict[str, Any], video: dict[str, Any]) -> str:
    digest = hashlib.sha256(_packet_id_basis(channel, video)).hexdigest()[:16]
    return f"acumen-triage-{digest}"


def build_packet(registry: dict[str, Any], channel_id: str, video: dict[str, Any]) -> dict[str, Any]:
    channel = resolve_channel(registry, channel_id)
    normalized_video = normalize_video_metadata(video)
    errors = validate_channel(channel) + validate_video(normalized_video)
    if errors:
        raise SystemExit("\n".join(errors))
    return {
        "schema_version": PACKET_SCHEMA_VERSION,
        "packet_id": make_packet_id(channel, normalized_video),
        "channel": channel,
        "video": normalized_video,
    }


def validate_packet(packet: Any) -> list[str]:
    if not isinstance(packet, dict):
        return ["triage packet must be a JSON object"]

    errors: list[str] = []
    if packet.get("schema_version") != PACKET_SCHEMA_VERSION:
        errors.append(
            f"triage packet schema_version must be {PACKET_SCHEMA_VERSION!r}, got {packet.get('schema_version')!r}"
        )

    channel = packet.get("channel")
    if not isinstance(channel, dict):
        errors.append("triage packet field 'channel' must be an object")
    else:
        errors.extend(validate_channel(channel))

    video = packet.get("video")
    if not isinstance(video, dict):
        errors.append("triage packet field 'video' must be an object")
    else:
        errors.extend(validate_video(video))

    if isinstance(channel, dict) and isinstance(video, dict):
        expected_packet_id = make_packet_id(channel, video)
        if packet.get("packet_id") != expected_packet_id:
            errors.append(
                f"triage packet_id must be {expected_packet_id!r}, got {packet.get('packet_id')!r}"
            )
    return errors


def render_user_prompt(packet: dict[str, Any]) -> str:
    errors = validate_packet(packet)
    if errors:
        raise SystemExit("\n".join(errors))

    channel = packet["channel"]
    video = packet["video"]
    return USER_PROMPT_TEMPLATE.format(
        packet_id=packet["packet_id"],
        name=channel.get("name"),
        genre=channel.get("genre"),
        priority_band=channel.get("priority_band"),
        default_compression=channel.get("default_compression"),
        default_polish=channel.get("default_polish"),
        signal_density=channel.get("signal_density"),
        visual_dependency=channel.get("visual_dependency"),
        voice_normalization=channel.get("voice_normalization"),
        cadence=channel.get("cadence"),
        chain_alignment=channel.get("chain_alignment"),
        domain_tags=", ".join(str(tag) for tag in channel.get("domain_tags", [])),
        resolution_vocabulary=", ".join(str(term) for term in channel.get("resolution_vocabulary", [])),
        title=video["title"],
        duration=video["duration"],
        description=video["description"],
        initial_transcript=video["initial_transcript"],
    )


def render_prompt_preview(packet: dict[str, Any]) -> str:
    return f"System:\n{SYSTEM_INSTRUCTION}\n\nUser:\n{render_user_prompt(packet)}\n"


def normalize_decision_payload(payload: Any) -> Any:
    if not isinstance(payload, dict):
        return payload
    normalized: dict[str, Any] = {}
    for key, value in payload.items():
        normalized[key] = value.strip() if isinstance(value, str) else value
    return normalized


def validate_decision(packet: dict[str, Any], payload: Any) -> list[str]:
    decision = normalize_decision_payload(payload)
    if not isinstance(decision, dict):
        return ["triage decision must be a JSON object"]

    packet_errors = validate_packet(packet)
    if packet_errors:
        return [f"invalid packet: {error}" for error in packet_errors]

    required = {
        "decision",
        "target_depth",
        "target_polish",
        "rationale",
        "primary_flag_reason",
    }
    errors: list[str] = []
    missing = sorted(required - set(decision.keys()))
    if missing:
        errors.append(f"triage decision missing required keys: {missing}")
    extra = sorted(set(decision.keys()) - required)
    if extra:
        errors.append(f"triage decision has unsupported keys: {extra}")

    decision_value = decision.get("decision")
    target_depth = decision.get("target_depth")
    target_polish = decision.get("target_polish")
    rationale = decision.get("rationale")
    primary_flag_reason = decision.get("primary_flag_reason")

    if decision_value not in DECISION_SET:
        errors.append(f"decision must be one of {list(DECISION_VALUES)}, got {decision_value!r}")
    if target_depth not in TARGET_DEPTH_SET:
        errors.append(f"target_depth must be one of {list(TARGET_DEPTH_VALUES)}, got {target_depth!r}")
    if target_polish not in TARGET_POLISH_SET:
        errors.append(f"target_polish must be one of {list(TARGET_POLISH_VALUES)}, got {target_polish!r}")
    if not isinstance(rationale, str) or not rationale.strip():
        errors.append("rationale must be a non-empty string")
    if primary_flag_reason is not None and (not isinstance(primary_flag_reason, str) or not primary_flag_reason.strip()):
        errors.append("primary_flag_reason must be null or a non-empty string")

    channel = packet["channel"]
    default_depth = str(channel.get("default_compression"))
    default_polish = str(channel.get("default_polish"))

    if decision_value == "Skip":
        if target_depth != "None":
            errors.append("Skip must set target_depth to 'None'")
        if target_polish != "clean_verbatim":
            errors.append("Skip must set target_polish to 'clean_verbatim'")
        if primary_flag_reason is not None:
            errors.append("Skip must set primary_flag_reason to null")

    if decision_value == "Headline":
        if target_depth != "Headline":
            errors.append("Headline must set target_depth to 'Headline'")
        if target_polish != "clean_verbatim":
            errors.append("Headline must set target_polish to 'clean_verbatim'")
        if primary_flag_reason is not None:
            errors.append("Headline must set primary_flag_reason to null")

    if decision_value == "Compress":
        if target_depth != default_depth:
            errors.append(f"Compress must keep channel default target_depth={default_depth!r}")
        if target_polish != default_polish:
            errors.append(f"Compress must keep channel default target_polish={default_polish!r}")
        if primary_flag_reason is not None:
            errors.append("Compress must set primary_flag_reason to null")

    if decision_value == "Promote":
        if primary_flag_reason is not None:
            errors.append("Promote must set primary_flag_reason to null")
        if DEPTH_RANK.get(target_depth, -1) < DEPTH_RANK.get(default_depth, -1):
            errors.append("Promote cannot lower target_depth below the channel default")
        if POLISH_RANK.get(target_polish, -1) < POLISH_RANK.get(default_polish, -1):
            errors.append("Promote cannot lower target_polish below the channel default")
        if not (
            DEPTH_RANK.get(target_depth, -1) > DEPTH_RANK.get(default_depth, -1)
            or POLISH_RANK.get(target_polish, -1) > POLISH_RANK.get(default_polish, -1)
        ):
            errors.append("Promote must raise target_depth or target_polish above the channel defaults")

    if decision_value == "Flag-for-Primary":
        if target_depth != "Transcript":
            errors.append("Flag-for-Primary must set target_depth to 'Transcript'")
        if target_polish != "clean_verbatim":
            errors.append("Flag-for-Primary must set target_polish to 'clean_verbatim'")
        if primary_flag_reason is None:
            errors.append("Flag-for-Primary must provide primary_flag_reason")

    if decision_value != "Flag-for-Primary" and primary_flag_reason is not None:
        errors.append(f"{decision_value} must set primary_flag_reason to null")
    return errors


def suggested_consumption(decision_value: str, target_depth: str) -> str:
    mapping = {
        "Flag-for-Primary": "Primary / Original Viewing",
        "Promote": f"Layer 2 / {target_depth}",
        "Compress": f"Layer 2 / {target_depth}",
        "Headline": "Layer 1 / Headline Sweep",
        "Skip": "Archive / No Immediate Action",
    }
    return mapping.get(decision_value, f"Layer 2 / {target_depth}")


def build_decision_record(
    packet: dict[str, Any],
    decision: dict[str, Any],
    *,
    model: str,
    attempts_used: int,
    prompt_chars: int,
    usage_metadata: dict[str, Any],
    budget_guardrails: dict[str, Any],
    source_mode: str,
    abstract: str | None = None,
) -> dict[str, Any]:
    errors = validate_decision(packet, decision)
    if errors:
        raise SystemExit("\n".join(errors))

    normalized = normalize_decision_payload(decision)
    channel = packet["channel"]
    video = packet["video"]
    recorded_at = utc_now()
    record = {
        "schema_version": DECISION_SCHEMA_VERSION,
        "captured_at": recorded_at,
        "recorded_at": recorded_at,
        "packet_id": packet["packet_id"],
        "channel_id": str(channel.get("channel_id", "")),
        "channel_name": str(channel.get("name", "")),
        "decision": normalized["decision"],
        "target_depth": normalized["target_depth"],
        "target_polish": normalized["target_polish"],
        "priority_band": str(channel.get("priority_band", "")),
        "domain_tags": ",".join(str(tag) for tag in channel.get("domain_tags", [])),
        "rationale": normalized["rationale"],
        "primary_flag_reason": normalized["primary_flag_reason"],
        "abstract": abstract or normalized["rationale"],
        "suggested_consumption": suggested_consumption(normalized["decision"], normalized["target_depth"]),
        "source_mode": source_mode,
        "model": model,
        "attempts_used": attempts_used,
        "prompt_chars": prompt_chars,
        "usage_metadata": usage_metadata,
        "budget_guardrails": budget_guardrails,
        "title": str(video.get("title", "")),
        "duration": str(video.get("duration", "")),
        "published_at": str(video.get("published_at", "")),
        "video_id": str(video.get("video_id", video.get("resource_id", ""))),
    }
    return record

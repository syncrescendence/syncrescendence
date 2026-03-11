#!/usr/bin/env python3
"""Build deterministic Acumen triage packets and optional prompt previews."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from triage_contract import (
    build_packet as contract_build_packet,
    load_json,
    normalize_video_metadata,
    render_prompt_preview,
    resolve_channel as contract_resolve_channel,
    validate_video,
    write_json,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--channel-id", required=True)
    parser.add_argument("--video", required=True, help="JSON object with title/duration/description/initial_transcript.")
    parser.add_argument("--output", required=True, help="Path for the JSON triage packet artifact.")
    parser.add_argument("--prompt-output", help="Optional path for a human-readable prompt preview.")
    return parser.parse_args()


def normalize_video_metadata_for_bridge(video: dict[str, Any]) -> dict[str, Any]:
    return normalize_video_metadata(video)


def validate_video_metadata(video: dict[str, Any], *, require_non_empty: bool = False) -> list[str]:
    return validate_video(video, require_non_empty=require_non_empty)


def resolve_channel(registry: dict[str, Any], channel_id: str) -> dict[str, Any]:
    return contract_resolve_channel(registry, channel_id)


def build_triage_packet(registry: dict[str, Any], channel_id: str, video: dict[str, Any]) -> dict[str, Any]:
    return contract_build_packet(registry, channel_id, video)


def render_triage_packet(registry: dict[str, Any], channel_id: str, video: dict[str, Any]) -> str:
    return render_prompt_preview(build_triage_packet(registry, channel_id, video))


def handoff_filename(channel_id: str, resource_id: str) -> str:
    raw = f"{channel_id}-{resource_id}"
    return "".join(ch.lower() if ch.isalnum() or ch in {"-", "_"} else "-" for ch in raw)


def build_bridge_video_metadata(bridge_payload: dict[str, Any], *, summary: str) -> dict[str, Any]:
    metadata = {
        "title": bridge_payload.get("title") or summary,
        "duration": bridge_payload.get("duration") or bridge_payload.get("duration_text") or "",
        "description": bridge_payload.get("description") or summary,
        "initial_transcript": bridge_payload.get("initial_transcript") or bridge_payload.get("transcript_excerpt") or "",
        "channel_id": bridge_payload.get("channel_id"),
        "channel_title": bridge_payload.get("channel_title"),
        "published_at": bridge_payload.get("published_at"),
        "resource_id": bridge_payload.get("resource_id"),
        "source_url": bridge_payload.get("source_url"),
        "summary": summary,
    }
    return normalize_video_metadata(metadata)


def materialize_youtube_bridge_handoff(
    *,
    registry_path: str | Path,
    output_root: str | Path,
    bridge_payload: dict[str, Any],
    summary: str,
) -> dict[str, Any]:
    resource_kind = str(bridge_payload.get("resource_kind", "")).strip()
    if resource_kind != "video":
        return {"status": "skipped", "reason": "resource_kind must be 'video' for Acumen handoff"}

    channel_id = str(bridge_payload.get("channel_id", "")).strip()
    if not channel_id:
        return {"status": "skipped", "reason": "channel_id missing from YouTube bridge payload"}

    registry = load_json(registry_path)
    resource_id = str(bridge_payload.get("resource_id", "")).strip() or "unknown-resource"
    try:
        channel = resolve_channel(registry, channel_id)
    except SystemExit as exc:
        return {
            "status": "skipped",
            "channel_id": channel_id,
            "resource_id": resource_id,
            "reason": str(exc),
        }

    output_root = Path(output_root).expanduser().resolve()
    intake_dir = output_root / "intake" / "youtube"
    triage_dir = output_root / "intake" / "triage-packets"
    prompt_dir = output_root / "intake" / "triage-prompts"
    intake_dir.mkdir(parents=True, exist_ok=True)
    triage_dir.mkdir(parents=True, exist_ok=True)
    prompt_dir.mkdir(parents=True, exist_ok=True)

    stem = handoff_filename(channel_id, resource_id)
    video = build_bridge_video_metadata(bridge_payload, summary=summary)

    metadata_path = intake_dir / f"{stem}.json"
    metadata_path.write_text(json.dumps(video, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    result = {
        "status": "metadata_only",
        "channel_id": channel_id,
        "channel_name": channel.get("name"),
        "resource_id": resource_id,
        "video_metadata_path": str(metadata_path),
    }
    errors = validate_video_metadata(video, require_non_empty=True)
    if errors:
        result["reason"] = errors[0]
        return result

    triage_packet = build_triage_packet(registry, channel_id, video)
    triage_packet_path = write_json(triage_dir / f"{stem}.json", triage_packet)
    triage_prompt_path = prompt_dir / f"{stem}.md"
    triage_prompt_path.write_text(render_prompt_preview(triage_packet), encoding="utf-8")

    result["status"] = "ready_for_triage"
    result["triage_packet_path"] = str(triage_packet_path)
    result["triage_prompt_path"] = str(triage_prompt_path)
    return result


def main() -> int:
    args = parse_args()
    registry = load_json(args.registry)
    video = load_json(args.video)
    packet = build_triage_packet(registry, args.channel_id, video)

    output_path = write_json(args.output, packet)
    print(output_path)
    if args.prompt_output:
        prompt_path = Path(args.prompt_output).expanduser().resolve()
        prompt_path.parent.mkdir(parents=True, exist_ok=True)
        prompt_path.write_text(render_prompt_preview(packet), encoding="utf-8")
        print(prompt_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

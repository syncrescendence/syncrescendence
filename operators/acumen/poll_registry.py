#!/usr/bin/env python3
"""Registry-driven Acumen YouTube polling with cursor discipline and fixture fallback."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
import urllib.request
import xml.etree.ElementTree as ET

from registry_contract import utc_now


ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "media": "http://search.yahoo.com/mrss/",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}
YOUTUBE_FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
CADENCE_WINDOWS = {
    "daily": timedelta(hours=6),
    "weekly": timedelta(hours=24),
    "biweekly": timedelta(hours=48),
    "monthly": timedelta(hours=96),
    "irregular": timedelta(hours=24),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", required=True)
    parser.add_argument("--output", required=True, help="JSONL batch of newly detected uploads.")
    parser.add_argument("--cursor-json", default="runtime/acumen/poll_cursor.json")
    parser.add_argument("--status-json", default="runtime/acumen/poll-status.json")
    parser.add_argument("--fixture-feed", help="Optional JSON fixture used for deterministic smoke runs.")
    parser.add_argument("--mode", choices=("auto", "fixture", "live"), default="auto")
    parser.add_argument("--max-items-per-channel", type=int, default=5)
    parser.add_argument("--timeout-seconds", type=float, default=10.0)
    parser.add_argument("--force", action="store_true", help="Poll even if cadence window says not due.")
    return parser.parse_args()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows)
    path.write_text(payload, encoding="utf-8")


def parse_timestamp(value: str | None) -> datetime | None:
    if not value:
        return None
    text = value.strip()
    if not text:
        return None
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text).astimezone(UTC)
    except ValueError:
        return None


def due_for_poll(channel: dict[str, Any], cursor_entry: dict[str, Any], now: datetime, force: bool) -> bool:
    if force:
        return True
    last_poll = parse_timestamp(str(cursor_entry.get("last_polled_at") or ""))
    if last_poll is None:
        return True
    cadence = str(channel.get("cadence", "irregular"))
    window = CADENCE_WINDOWS.get(cadence, CADENCE_WINDOWS["irregular"])
    return now - last_poll >= window


def fetch_live_feed(channel_id: str, timeout_seconds: float) -> list[dict[str, Any]]:
    url = YOUTUBE_FEED_URL.format(channel_id=channel_id)
    with urllib.request.urlopen(url, timeout=timeout_seconds) as response:
        payload = response.read()
    root = ET.fromstring(payload)
    entries: list[dict[str, Any]] = []
    for entry in root.findall("atom:entry", ATOM_NS):
        video_id = entry.findtext("yt:videoId", default="", namespaces=ATOM_NS).strip()
        title = entry.findtext("atom:title", default="", namespaces=ATOM_NS).strip()
        published_at = entry.findtext("atom:published", default="", namespaces=ATOM_NS).strip()
        description = entry.findtext("media:group/media:description", default="", namespaces=ATOM_NS).strip()
        if not description:
            description = title
        entries.append(
            {
                "video_id": video_id,
                "title": title,
                "published_at": published_at,
                "description": description,
                "duration": "unknown",
                "initial_transcript": description[:280] or title,
                "source_url": f"https://www.youtube.com/watch?v={video_id}" if video_id else url,
            }
        )
    return entries


def load_fixture_items(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    payload = load_json(path, [])
    if isinstance(payload, dict):
        payload = payload.get("items", [])
    if not isinstance(payload, list):
        raise SystemExit("fixture feed must be a list or an object with an 'items' list")
    return [row for row in payload if isinstance(row, dict)]


def fixture_items_for_channel(items: list[dict[str, Any]], channel_id: str) -> list[dict[str, Any]]:
    matched = [row for row in items if str(row.get("channel_id")) == channel_id]
    matched.sort(key=lambda row: str(row.get("published_at", "")), reverse=True)
    return matched


def latest_seen_marker(cursor_entry: dict[str, Any]) -> tuple[datetime | None, set[str]]:
    published_at = parse_timestamp(str(cursor_entry.get("last_seen_published_at") or ""))
    seen_video_ids = {str(item) for item in cursor_entry.get("seen_video_ids", []) if str(item).strip()}
    return published_at, seen_video_ids


def is_new_item(item: dict[str, Any], cursor_entry: dict[str, Any]) -> bool:
    last_seen_published_at, seen_video_ids = latest_seen_marker(cursor_entry)
    video_id = str(item.get("video_id", "")).strip()
    published_at = parse_timestamp(str(item.get("published_at") or ""))
    if video_id and video_id in seen_video_ids:
        return False
    if last_seen_published_at is None:
        return True
    if published_at is None:
        return video_id not in seen_video_ids
    return published_at > last_seen_published_at


def update_cursor_entry(cursor_entry: dict[str, Any], channel_items: list[dict[str, Any]], emitted: list[dict[str, Any]]) -> dict[str, Any]:
    updated = dict(cursor_entry)
    updated["last_polled_at"] = utc_now()
    candidate_times = [parse_timestamp(str(item.get("published_at") or "")) for item in channel_items]
    valid_times = [item for item in candidate_times if item is not None]
    if valid_times:
        updated["last_seen_published_at"] = max(valid_times).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    seen_video_ids = {str(item) for item in updated.get("seen_video_ids", []) if str(item).strip()}
    for item in emitted:
        video_id = str(item.get("video_id", "")).strip()
        if video_id:
            seen_video_ids.add(video_id)
    updated["seen_video_ids"] = sorted(seen_video_ids)[-25:]
    return updated


def normalize_item(channel: dict[str, Any], raw: dict[str, Any], source_mode: str) -> dict[str, Any]:
    title = str(raw.get("title", "")).strip()
    description = str(raw.get("description", "")).strip() or title
    transcript = str(raw.get("initial_transcript", "")).strip() or description[:280] or title
    return {
        "channel_id": str(channel.get("channel_id")),
        "channel_name": str(channel.get("name")),
        "priority_band": str(channel.get("priority_band")),
        "domain_tags": list(channel.get("domain_tags", [])),
        "video_id": str(raw.get("video_id", "")).strip() or title.lower().replace(" ", "-")[:48],
        "title": title,
        "description": description,
        "duration": str(raw.get("duration", "unknown")),
        "initial_transcript": transcript,
        "published_at": str(raw.get("published_at", "")).strip(),
        "source_mode": source_mode,
        "source_url": str(raw.get("source_url", "")).strip(),
        "polled_at": utc_now(),
    }


def main() -> int:
    args = parse_args()
    registry_path = Path(args.registry).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    cursor_path = Path(args.cursor_json).expanduser().resolve()
    status_path = Path(args.status_json).expanduser().resolve()

    registry = load_json(registry_path, {})
    cursor = load_json(cursor_path, {"channels": {}})
    channels = list(registry.get("channels", []))
    fixture_path = Path(args.fixture_feed).expanduser().resolve() if args.fixture_feed else None
    fixture_items = load_fixture_items(fixture_path)

    if args.mode == "fixture" and not fixture_items:
        raise SystemExit("fixture mode requires --fixture-feed with at least one item")

    now = datetime.now(UTC)
    batch_rows: list[dict[str, Any]] = []
    channel_statuses: list[dict[str, Any]] = []
    failures = 0

    for channel in channels:
        channel_id = str(channel.get("channel_id"))
        cursor_entry = dict(cursor.get("channels", {}).get(channel_id, {}))
        if not due_for_poll(channel, cursor_entry, now, args.force):
            channel_statuses.append(
                {
                    "channel_id": channel_id,
                    "channel_name": channel.get("name"),
                    "status": "skipped_not_due",
                }
            )
            continue

        source_mode = "live"
        try:
            if args.mode == "fixture":
                source_mode = "fixture"
                channel_items = fixture_items_for_channel(fixture_items, channel_id)
            elif args.mode == "auto" and fixture_items:
                source_mode = "fixture"
                channel_items = fixture_items_for_channel(fixture_items, channel_id)
            else:
                channel_items = fetch_live_feed(channel_id, args.timeout_seconds)
        except Exception as exc:
            failures += 1
            channel_statuses.append(
                {
                    "channel_id": channel_id,
                    "channel_name": channel.get("name"),
                    "status": "poll_failed",
                    "error": str(exc),
                }
            )
            continue

        channel_items = channel_items[: args.max_items_per_channel]
        normalized = [normalize_item(channel, item, source_mode) for item in channel_items]
        emitted = [item for item in normalized if is_new_item(item, cursor_entry)]
        batch_rows.extend(emitted)
        cursor.setdefault("channels", {})[channel_id] = update_cursor_entry(cursor_entry, normalized, emitted)
        channel_statuses.append(
            {
                "channel_id": channel_id,
                "channel_name": channel.get("name"),
                "status": "ok",
                "source_mode": source_mode,
                "items_seen": len(normalized),
                "new_items": len(emitted),
            }
        )

    write_jsonl(output_path, batch_rows)
    write_json(cursor_path, cursor)

    requires_live = args.mode == "live" or (args.mode == "auto" and not fixture_items)
    status = {
        "captured_at": utc_now(),
        "registry": str(registry_path),
        "output": str(output_path),
        "cursor_json": str(cursor_path),
        "mode": args.mode,
        "fixture_feed": str(fixture_path) if fixture_path else None,
        "channels_total": len(channels),
        "new_uploads": len(batch_rows),
        "failures": failures,
        "ok": failures == 0,
        "external_dependencies": {
            "youtube_feed": {
                "required": requires_live,
                "satisfied": (failures == 0) if requires_live else None,
            }
        },
        "channels": channel_statuses,
    }
    write_json(status_path, status)
    print(output_path)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

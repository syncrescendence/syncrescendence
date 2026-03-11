#!/usr/bin/env python3
"""Poll the Acumen registry against the YouTube Data API with cadence-aware cursors."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from registry_contract import validate_registry


YOUTUBE_API_BASE = "https://www.googleapis.com/youtube/v3"
CADENCE_INTERVALS = {
    "daily": timedelta(hours=4),
    "weekly": timedelta(hours=12),
    "biweekly": timedelta(hours=24),
    "monthly": timedelta(hours=24),
    "irregular": timedelta(hours=24),
}
SEARCH_COST_UNITS = 100
VIDEOS_COST_UNITS = 1
MAX_RECENT_VIDEO_IDS = 50
DEFAULT_RETRY_DELAYS = (30, 60, 120)
RETRYABLE_HTTP_STATUS = {429, 500, 502, 503, 504}
FAILURE_EXIT_CODES = {
    "complete": 0,
    "partial": 3,
    "blocked": 2,
}


class YouTubePollError(RuntimeError):
    """Explicit YouTube poll failure with retry metadata."""

    def __init__(self, code: str, message: str, *, retryable: bool = False, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable
        self.details = details or {}


def utc_now() -> datetime:
    return datetime.now(UTC).replace(microsecond=0)


def isoformat_z(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_timestamp(value: Any, *, field: str) -> datetime:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field} must be non-empty")
    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def parse_optional_timestamp(value: Any, *, field: str) -> datetime | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    return parse_timestamp(text, field=field)


def cadence_interval(cadence: str) -> timedelta:
    return CADENCE_INTERVALS.get(cadence, CADENCE_INTERVALS["irregular"])


def parse_retry_delays(raw: str) -> tuple[int, ...]:
    if not raw.strip():
        return ()
    delays: list[int] = []
    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue
        value = int(item)
        if value < 0:
            raise ValueError("retry delays must be >= 0")
        delays.append(value)
    return tuple(delays)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_cursor(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"channels": {}}
    payload = load_json(path)
    if not isinstance(payload, dict):
        raise SystemExit(f"cursor file must contain an object: {path}")
    channels = payload.get("channels")
    if channels is None:
        payload["channels"] = {}
        return payload
    if not isinstance(channels, dict):
        raise SystemExit(f"cursor file 'channels' must be an object: {path}")
    return payload


def resolve_channels(registry: dict[str, Any], selected_channel_ids: list[str]) -> list[dict[str, Any]]:
    channels = registry.get("channels", [])
    if not selected_channel_ids:
        return list(channels)
    requested = set(selected_channel_ids)
    selected = [channel for channel in channels if str(channel.get("channel_id")) in requested]
    missing = sorted(requested - {str(channel.get("channel_id")) for channel in selected})
    if missing:
        raise SystemExit(f"channel ids not found in registry: {', '.join(missing)}")
    return selected


def load_api_key(env_name: str) -> str:
    value = os.environ.get(env_name, "").strip()
    if not value:
        raise YouTubePollError(
            "missing_api_key",
            f"required API key environment variable is unset: {env_name}",
            retryable=False,
            details={"env_var": env_name},
        )
    return value


def should_poll_channel(
    channel: dict[str, Any],
    cursor_entry: dict[str, Any],
    now: datetime,
    *,
    force: bool,
) -> tuple[bool, str | None, datetime]:
    if force:
        return True, None, now
    interval = cadence_interval(str(channel.get("cadence", "irregular")))
    baseline = parse_optional_timestamp(cursor_entry.get("last_successful_poll"), field="cursor.last_successful_poll")
    if baseline is None:
        baseline = parse_optional_timestamp(channel.get("last_processed"), field=f"{channel.get('channel_id')}.last_processed")
    if baseline is None:
        return True, None, now
    due_at = baseline + interval
    if now < due_at:
        return False, "cadence_not_due", due_at
    return True, None, due_at


def published_after_for_channel(
    channel: dict[str, Any],
    cursor_entry: dict[str, Any],
    *,
    overlap_seconds: int,
) -> tuple[str, str]:
    baseline = parse_optional_timestamp(cursor_entry.get("latest_published_at"), field="cursor.latest_published_at")
    if baseline is None:
        baseline = parse_optional_timestamp(channel.get("last_processed"), field=f"{channel.get('channel_id')}.last_processed")
    if baseline is None:
        raise YouTubePollError(
            "missing_poll_baseline",
            f"channel {channel.get('channel_id')} is missing both cursor.latest_published_at and registry.last_processed",
            retryable=False,
        )
    effective = baseline - timedelta(seconds=max(0, overlap_seconds))
    return isoformat_z(effective), isoformat_z(baseline)


def parse_error_payload(payload: bytes) -> tuple[str, dict[str, Any]]:
    try:
        data = json.loads(payload.decode("utf-8"))
    except Exception:
        return "", {}
    if not isinstance(data, dict):
        return "", {}
    error_obj = data.get("error")
    if not isinstance(error_obj, dict):
        return "", {}
    details = {
        "status": error_obj.get("status"),
        "message": error_obj.get("message"),
    }
    errors = error_obj.get("errors")
    if isinstance(errors, list) and errors:
        first = errors[0]
        if isinstance(first, dict):
            details["reason"] = first.get("reason")
            details["domain"] = first.get("domain")
    return str(details.get("message") or ""), details


def youtube_request(
    endpoint: str,
    params: dict[str, Any],
    *,
    api_key: str,
    timeout_seconds: float,
    retry_delays: tuple[int, ...],
) -> dict[str, Any]:
    params_with_key = dict(params)
    params_with_key["key"] = api_key
    url = f"{YOUTUBE_API_BASE}/{endpoint}?{urlencode(params_with_key, doseq=True)}"
    attempts = len(retry_delays) + 1

    for attempt in range(attempts):
        try:
            with urlopen(url, timeout=timeout_seconds) as response:
                payload = response.read()
            data = json.loads(payload.decode("utf-8"))
            if not isinstance(data, dict):
                raise YouTubePollError("invalid_json", f"{endpoint} response is not a JSON object", retryable=False)
            return data
        except HTTPError as exc:
            payload = exc.read()
            message, details = parse_error_payload(payload)
            retryable = exc.code in RETRYABLE_HTTP_STATUS
            error = YouTubePollError(
                f"http_{exc.code}",
                message or f"{endpoint} returned HTTP {exc.code}",
                retryable=retryable,
                details={"status_code": exc.code, **details},
            )
        except URLError as exc:
            error = YouTubePollError("network_error", f"{endpoint} failed: {exc.reason}", retryable=True)
        except json.JSONDecodeError as exc:
            error = YouTubePollError("invalid_json", f"{endpoint} returned invalid JSON: {exc}", retryable=False)

        if not error.retryable or attempt >= len(retry_delays):
            raise error
        time.sleep(retry_delays[attempt])

    raise AssertionError("unreachable")


def search_videos(
    channel_id: str,
    *,
    published_after: str,
    api_key: str,
    timeout_seconds: float,
    max_results: int,
    retry_delays: tuple[int, ...],
) -> dict[str, Any]:
    return youtube_request(
        "search",
        {
            "part": "snippet",
            "channelId": channel_id,
            "type": "video",
            "order": "date",
            "publishedAfter": published_after,
            "maxResults": max_results,
        },
        api_key=api_key,
        timeout_seconds=timeout_seconds,
        retry_delays=retry_delays,
    )


def fetch_video_details(
    video_ids: list[str],
    *,
    api_key: str,
    timeout_seconds: float,
    retry_delays: tuple[int, ...],
) -> dict[str, Any]:
    if not video_ids:
        return {"items": []}
    return youtube_request(
        "videos",
        {
            "part": "contentDetails,snippet,status,liveStreamingDetails",
            "id": ",".join(video_ids),
            "maxResults": len(video_ids),
        },
        api_key=api_key,
        timeout_seconds=timeout_seconds,
        retry_delays=retry_delays,
    )


def parse_duration_iso8601(raw: str) -> str:
    match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", raw)
    if not match:
        return raw
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    if hours:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{minutes:02d}:{seconds:02d}"


def dedupe_recent_video_ids(items: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        deduped.append(item)
        if len(deduped) >= MAX_RECENT_VIDEO_IDS:
            break
    return deduped


def merge_video_record(
    *,
    channel: dict[str, Any],
    search_item: dict[str, Any],
    detail_item: dict[str, Any] | None,
    poll_captured_at: str,
    poll_published_after: str,
) -> dict[str, Any]:
    search_snippet = search_item.get("snippet", {}) if isinstance(search_item, dict) else {}
    detail_snippet = detail_item.get("snippet", {}) if isinstance(detail_item, dict) else {}
    snippet = detail_snippet if isinstance(detail_snippet, dict) and detail_snippet else search_snippet
    content_details = detail_item.get("contentDetails", {}) if isinstance(detail_item, dict) else {}
    video_id = ""
    item_id = search_item.get("id", {}) if isinstance(search_item, dict) else {}
    if isinstance(item_id, dict):
        video_id = str(item_id.get("videoId") or "")
    if not video_id and isinstance(detail_item, dict):
        video_id = str(detail_item.get("id") or "")

    thumbnails = snippet.get("thumbnails", {}) if isinstance(snippet, dict) else {}
    default_thumbnail = thumbnails.get("high") or thumbnails.get("medium") or thumbnails.get("default") or {}
    thumbnail_url = default_thumbnail.get("url") if isinstance(default_thumbnail, dict) else None

    return {
        "channel_id": str(channel.get("channel_id")),
        "channel_name": str(channel.get("name")),
        "channel_title": str(snippet.get("channelTitle") or channel.get("name")),
        "default_compression": channel.get("default_compression"),
        "default_polish": channel.get("default_polish"),
        "description": str(snippet.get("description") or ""),
        "duration": parse_duration_iso8601(str(content_details.get("duration") or "")),
        "duration_iso8601": str(content_details.get("duration") or ""),
        "genre": channel.get("genre"),
        "initial_transcript": "",
        "live_broadcast_content": snippet.get("liveBroadcastContent"),
        "poll_captured_at": poll_captured_at,
        "poll_published_after": poll_published_after,
        "priority_band": channel.get("priority_band"),
        "published_at": snippet.get("publishedAt"),
        "thumbnail_url": thumbnail_url,
        "title": str(snippet.get("title") or ""),
        "url": f"https://www.youtube.com/watch?v={video_id}" if video_id else "",
        "video_id": video_id,
        "visual_dependency": channel.get("visual_dependency"),
    }


def poll_channel(
    channel: dict[str, Any],
    cursor_entry: dict[str, Any],
    *,
    api_key: str,
    now: datetime,
    force: bool,
    max_results: int,
    overlap_seconds: int,
    retry_delays: tuple[int, ...],
    timeout_seconds: float,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]], dict[str, int]]:
    eligible, skip_reason, due_at = should_poll_channel(channel, cursor_entry, now, force=force)
    result = {
        "cadence": channel.get("cadence"),
        "channel_id": channel.get("channel_id"),
        "channel_name": channel.get("name"),
        "discovered_videos": 0,
        "eligible": eligible,
        "next_eligible_poll_after": isoformat_z(due_at),
        "status": "skipped" if not eligible else "pending",
    }
    updated_cursor = dict(cursor_entry)
    usage = {"search_calls": 0, "videos_calls": 0}

    if not eligible:
        result["skip_reason"] = skip_reason
        return result, updated_cursor, [], usage

    published_after, baseline = published_after_for_channel(channel, cursor_entry, overlap_seconds=overlap_seconds)
    result["published_after"] = published_after
    result["status"] = "polling"
    result["cursor_baseline"] = baseline
    updated_cursor["last_attempted_poll"] = isoformat_z(now)

    search_data = search_videos(
        str(channel.get("channel_id")),
        published_after=published_after,
        api_key=api_key,
        timeout_seconds=timeout_seconds,
        max_results=max_results,
        retry_delays=retry_delays,
    )
    usage["search_calls"] += 1

    search_items = search_data.get("items", [])
    if not isinstance(search_items, list):
        raise YouTubePollError("invalid_search_items", "search response missing items list", retryable=False)

    recent_video_ids = list(cursor_entry.get("recent_video_ids") or [])
    recent_set = {str(item) for item in recent_video_ids}

    discovered_search_items: list[dict[str, Any]] = []
    video_ids: list[str] = []
    for item in search_items:
        if not isinstance(item, dict):
            continue
        item_id = item.get("id", {})
        if not isinstance(item_id, dict):
            continue
        video_id = str(item_id.get("videoId") or "")
        if not video_id or video_id in recent_set:
            continue
        video_ids.append(video_id)
        discovered_search_items.append(item)

    details_by_id: dict[str, dict[str, Any]] = {}
    if video_ids:
        details_payload = fetch_video_details(
            video_ids,
            api_key=api_key,
            timeout_seconds=timeout_seconds,
            retry_delays=retry_delays,
        )
        usage["videos_calls"] += 1
        detail_items = details_payload.get("items", [])
        if not isinstance(detail_items, list):
            raise YouTubePollError("invalid_videos_items", "videos response missing items list", retryable=False)
        for item in detail_items:
            if isinstance(item, dict) and item.get("id"):
                details_by_id[str(item["id"])] = item

    discoveries = [
        merge_video_record(
            channel=channel,
            search_item=item,
            detail_item=details_by_id.get(str(item.get("id", {}).get("videoId") or "")),
            poll_captured_at=isoformat_z(now),
            poll_published_after=published_after,
        )
        for item in discovered_search_items
    ]
    discoveries = [item for item in discoveries if item.get("video_id")]
    discoveries.sort(key=lambda item: str(item.get("published_at") or ""))

    updated_cursor["last_successful_poll"] = isoformat_z(now)
    updated_cursor["next_eligible_poll_after"] = isoformat_z(now + cadence_interval(str(channel.get("cadence", "irregular"))))
    updated_cursor["consecutive_failures"] = 0
    updated_cursor.pop("last_error", None)

    if discoveries:
        latest = discoveries[-1]
        updated_cursor["latest_published_at"] = str(latest.get("published_at"))
        updated_cursor["latest_video_id"] = str(latest.get("video_id"))
        updated_cursor["recent_video_ids"] = dedupe_recent_video_ids(
            [str(item.get("video_id")) for item in reversed(discoveries)] + recent_video_ids
        )
    else:
        updated_cursor["recent_video_ids"] = dedupe_recent_video_ids(recent_video_ids)

    result["status"] = "polled"
    result["discovered_videos"] = len(discoveries)
    return result, updated_cursor, discoveries, usage


def run_identity_probe(args: argparse.Namespace) -> dict[str, Any]:
    if not args.strict_identity:
        return {
            "enforced": False,
            "ok": True,
            "status": "not_enforced",
        }

    cmd = [
        sys.executable,
        str(Path(__file__).resolve().parent / "identity_binding_probe.py"),
        "--binding",
        str(Path(args.identity_binding).expanduser().resolve()),
        "--output",
        str(Path(args.identity_status_json).expanduser().resolve()),
        "--strict",
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    status_path = Path(args.identity_status_json).expanduser().resolve()
    payload: dict[str, Any] = {
        "enforced": True,
        "ok": proc.returncode == 0,
        "status": "passed" if proc.returncode == 0 else "failed",
        "stdout": (proc.stdout or "").strip()[:1200],
        "stderr": (proc.stderr or "").strip()[:1200],
    }
    if status_path.exists():
        try:
            loaded = load_json(status_path)
            if isinstance(loaded, dict):
                payload["details"] = loaded
                payload["ok"] = bool(loaded.get("ok"))
        except Exception as exc:
            payload["details_error"] = str(exc)
    return payload


def build_status_base(args: argparse.Namespace, *, now: datetime) -> dict[str, Any]:
    return {
        "captured_at": isoformat_z(now),
        "credential_state": "unknown",
        "cursor_path": str(Path(args.cursor).expanduser().resolve()),
        "output_jsonl": str(Path(args.output_jsonl).expanduser().resolve()),
        "registry": str(Path(args.registry).expanduser().resolve()),
        "result": "blocked",
        "status_json": str(Path(args.status_json).expanduser().resolve()),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", default="runtime/acumen/registry.json")
    parser.add_argument("--cursor", default="runtime/acumen/poll_cursor.json")
    parser.add_argument("--output-jsonl", default="runtime/acumen/poll-candidates.jsonl")
    parser.add_argument("--status-json", default="orchestration/state/ACUMEN-YOUTUBE-POLL-STATUS.json")
    parser.add_argument("--api-key-env", default="ACUMEN_YOUTUBE_API_KEY")
    parser.add_argument("--max-results-per-channel", type=int, default=10)
    parser.add_argument("--overlap-seconds", type=int, default=120)
    parser.add_argument("--timeout-seconds", type=float, default=20.0)
    parser.add_argument("--retry-delays-seconds", default="30,60,120")
    parser.add_argument("--channel-id", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--strict-identity", action="store_true")
    parser.add_argument("--identity-binding", default="orchestration/state/ACUMEN-IDENTITY-BINDING-CC87.json")
    parser.add_argument("--identity-status-json", default="orchestration/state/ACUMEN-IDENTITY-STATUS.json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    now = utc_now()
    status_path = Path(args.status_json).expanduser().resolve()
    status = build_status_base(args, now=now)

    try:
        retry_delays = parse_retry_delays(args.retry_delays_seconds)
        if args.max_results_per_channel <= 0:
            raise SystemExit("--max-results-per-channel must be > 0")
        if args.overlap_seconds < 0:
            raise SystemExit("--overlap-seconds must be >= 0")

        registry_path = Path(args.registry).expanduser().resolve()
        cursor_path = Path(args.cursor).expanduser().resolve()
        output_path = Path(args.output_jsonl).expanduser().resolve()

        identity_probe = run_identity_probe(args)
        status["identity"] = identity_probe
        if args.strict_identity and not identity_probe.get("ok"):
            status["failure_code"] = "identity_mismatch"
            status["failure_message"] = "strict identity gate failed"
            write_json(status_path, status)
            print(status_path)
            return FAILURE_EXIT_CODES["blocked"]

        registry = load_json(registry_path)
        registry_errors = validate_registry(registry)
        if registry_errors:
            status["failure_code"] = "invalid_registry"
            status["failure_message"] = "; ".join(registry_errors)
            status["registry_errors"] = registry_errors
            write_json(status_path, status)
            print(status_path)
            return FAILURE_EXIT_CODES["blocked"]

        cursor = load_cursor(cursor_path)
        channels = resolve_channels(registry, args.channel_id)

        api_key = load_api_key(args.api_key_env)
        status["credential_state"] = "present"
        status["credential_env_var"] = args.api_key_env

        all_discoveries: list[dict[str, Any]] = []
        channel_results: list[dict[str, Any]] = []
        cursor_channels = dict(cursor.get("channels", {}))
        errors: list[dict[str, Any]] = []
        usage = {"search_calls": 0, "videos_calls": 0}

        for channel in channels:
            channel_id = str(channel.get("channel_id"))
            cursor_entry = dict(cursor_channels.get(channel_id) or {})
            try:
                result, updated_cursor, discoveries, channel_usage = poll_channel(
                    channel,
                    cursor_entry,
                    api_key=api_key,
                    now=now,
                    force=args.force,
                    max_results=args.max_results_per_channel,
                    overlap_seconds=args.overlap_seconds,
                    retry_delays=retry_delays,
                    timeout_seconds=args.timeout_seconds,
                )
                cursor_channels[channel_id] = updated_cursor
                all_discoveries.extend(discoveries)
                channel_results.append(result)
                usage["search_calls"] += channel_usage["search_calls"]
                usage["videos_calls"] += channel_usage["videos_calls"]
            except (YouTubePollError, ValueError) as exc:
                message = exc.message if isinstance(exc, YouTubePollError) else str(exc)
                code = exc.code if isinstance(exc, YouTubePollError) else "invalid_timestamp"
                details = exc.details if isinstance(exc, YouTubePollError) else {}
                failures = int(cursor_entry.get("consecutive_failures", 0)) + 1
                cursor_channels[channel_id] = {
                    **cursor_entry,
                    "consecutive_failures": failures,
                    "last_attempted_poll": isoformat_z(now),
                    "last_error": {
                        "captured_at": isoformat_z(now),
                        "code": code,
                        "message": message,
                        "details": details,
                    },
                }
                channel_results.append(
                    {
                        "cadence": channel.get("cadence"),
                        "channel_id": channel_id,
                        "channel_name": channel.get("name"),
                        "discovered_videos": 0,
                        "eligible": True,
                        "failure_code": code,
                        "failure_message": message,
                        "status": "failed",
                    }
                )
                errors.append({"channel_id": channel_id, "code": code, "message": message, "details": details})

        cursor_payload = {
            "captured_at": isoformat_z(now),
            "channels": cursor_channels,
        }
        write_json(cursor_path, cursor_payload)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        if all_discoveries:
            output_path.write_text(
                "".join(json.dumps(item, sort_keys=True) + "\n" for item in all_discoveries),
                encoding="utf-8",
            )
        else:
            output_path.write_text("", encoding="utf-8")

        result = "complete"
        if errors and channel_results:
            result = "partial"
        if not channel_results:
            result = "blocked"

        status.update(
            {
                "channel_results": channel_results,
                "channels_polled": sum(1 for item in channel_results if item.get("status") == "polled"),
                "channels_skipped": sum(1 for item in channel_results if item.get("status") == "skipped"),
                "channels_total": len(channel_results),
                "discovered_videos": len(all_discoveries),
                "errors": errors,
                "quota_units_estimated": usage["search_calls"] * SEARCH_COST_UNITS + usage["videos_calls"] * VIDEOS_COST_UNITS,
                "result": result,
                "search_calls": usage["search_calls"],
                "videos_calls": usage["videos_calls"],
            }
        )
        write_json(status_path, status)
        print(status_path)
        return FAILURE_EXIT_CODES[result]
    except SystemExit as exc:
        status["failure_code"] = "usage_error"
        status["failure_message"] = str(exc)
        write_json(status_path, status)
        print(status_path)
        return int(exc.code) if isinstance(exc.code, int) else FAILURE_EXIT_CODES["blocked"]
    except YouTubePollError as exc:
        status["credential_state"] = "missing" if exc.code == "missing_api_key" else status["credential_state"]
        status["failure_code"] = exc.code
        status["failure_message"] = exc.message
        status["failure_details"] = exc.details
        write_json(status_path, status)
        print(status_path)
        return FAILURE_EXIT_CODES["blocked"]
    except Exception as exc:  # pragma: no cover - top-level guardrail
        status["failure_code"] = "unexpected_error"
        status["failure_message"] = str(exc)
        write_json(status_path, status)
        print(status_path)
        return FAILURE_EXIT_CODES["blocked"]


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import sys
import unittest
from datetime import UTC, datetime
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parent))

from poll_youtube_registry import (  # noqa: E402
    cadence_interval,
    dedupe_recent_video_ids,
    parse_duration_iso8601,
    published_after_for_channel,
    should_poll_channel,
)


class PollYouTubeRegistryTests(unittest.TestCase):
    def test_cadence_interval_matches_prd(self) -> None:
        self.assertEqual(cadence_interval("daily").total_seconds(), 4 * 3600)
        self.assertEqual(cadence_interval("weekly").total_seconds(), 12 * 3600)
        self.assertEqual(cadence_interval("biweekly").total_seconds(), 24 * 3600)
        self.assertEqual(cadence_interval("monthly").total_seconds(), 24 * 3600)
        self.assertEqual(cadence_interval("irregular").total_seconds(), 24 * 3600)

    def test_should_poll_uses_cursor_before_registry(self) -> None:
        now = datetime(2026, 3, 10, 20, 0, tzinfo=UTC)
        channel = {
            "cadence": "daily",
            "last_processed": "2026-03-08T00:00:00Z",
        }
        cursor_entry = {
            "last_successful_poll": "2026-03-10T17:30:00Z",
        }
        eligible, reason, due_at = should_poll_channel(channel, cursor_entry, now, force=False)
        self.assertFalse(eligible)
        self.assertEqual(reason, "cadence_not_due")
        self.assertEqual(due_at.isoformat().replace("+00:00", "Z"), "2026-03-10T21:30:00Z")

    def test_published_after_applies_overlap_to_cursor_high_water(self) -> None:
        channel = {
            "channel_id": "abc",
            "last_processed": "2026-03-08T00:00:00Z",
        }
        cursor_entry = {
            "latest_published_at": "2026-03-10T20:00:00Z",
        }
        published_after, baseline = published_after_for_channel(channel, cursor_entry, overlap_seconds=120)
        self.assertEqual(baseline, "2026-03-10T20:00:00Z")
        self.assertEqual(published_after, "2026-03-10T19:58:00Z")

    def test_parse_duration_iso8601_formats_clock_string(self) -> None:
        self.assertEqual(parse_duration_iso8601("PT1H2M3S"), "01:02:03")
        self.assertEqual(parse_duration_iso8601("PT42M7S"), "42:07")
        self.assertEqual(parse_duration_iso8601("PT15M"), "15:00")

    def test_dedupe_recent_video_ids_preserves_order_and_limit(self) -> None:
        values = [f"video-{index % 3}" for index in range(8)]
        deduped = dedupe_recent_video_ids(values)
        self.assertEqual(deduped, ["video-0", "video-1", "video-2"])


if __name__ == "__main__":
    unittest.main()

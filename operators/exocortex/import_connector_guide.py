#!/usr/bin/env python3
"""Import a markdown integration guide into a normalized exocortex connector manifest."""

from __future__ import annotations

import argparse
import json
import re
from datetime import UTC, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-SURFACE-REGISTRY-CC90.json"

HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
SUB_HEADING_RE = re.compile(r"^###\s+(.+?)\s*$")
TABLE_ROW_RE = re.compile(r"^\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
CONNECTS_TO_RE = re.compile(r"^\s*-\s+\*\*Connects to:\*\*\s*(.+?)\s*$", re.IGNORECASE)

SOURCE_MAP = {
    "Notion Integrations": ["notion_surface"],
    "Linear Integrations": ["linear_surface"],
    "Atlassian (Jira & Confluence) Integrations": ["jira_surface", "confluence_surface", "atlassian_projects_surface"],
    "ClickUp Integrations": ["clickup_surface"],
    "Airtable Integrations": ["airtable_surface"],
    "Coda Integrations": ["coda_surface"],
    "Figma Integrations": ["figma_surface"],
    "Todoist Integrations": ["todoist_surface"],
}

AI_SOURCE_MAP = {
    "ChatGPT": "chatgpt_openai_surface",
    "Claude": "claude_anthropic_surface",
    "Perplexity": "perplexity_surface",
    "Manus": "manus_surface",
}

TARGET_MAP = {
    "Slack": ("slack_surface", "registry"),
    "Google Drive": ("google_drive_external", "external"),
    "Jira Sync": ("jira_surface", "registry"),
    "Jira": ("jira_surface", "registry"),
    "Figma": ("figma_surface", "registry"),
    "GitHub (Workspace)": ("github_surface", "registry"),
    "GitHub": ("github_surface", "registry"),
    "Canva": ("canva_surface", "registry"),
    "Dropbox": ("dropbox_surface", "registry"),
    "ClickUp": ("clickup_surface", "registry"),
    "Linear": ("linear_surface", "registry"),
    "Notion": ("notion_surface", "registry"),
    "Discord": ("discord_surface", "registry"),
    "Google Sheets": ("google_sheets_external", "external"),
    "Google Workspace": ("google_workspace_external", "external"),
    "Confluence": ("confluence_surface", "registry"),
    "Google Calendar": ("google_calendar_external", "external"),
    "Todoist": ("todoist_surface", "registry"),
    "Gmail": ("gmail_external", "external"),
    "Airtable": ("airtable_surface", "registry"),
    "Google Workspace, Notion, Slack, GitHub": ("composite_external_connector_set", "external"),
}


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def slugify(value: str) -> str:
    return "-".join(piece for piece in re.sub(r"[^a-z0-9]+", " ", value.lower()).split() if piece)


def normalize_target(label: str) -> tuple[str, str]:
    mapped = TARGET_MAP.get(label)
    if mapped:
        return mapped
    return (f"{slugify(label)}_external", "external")


def load_registry(registry_path: Path) -> dict:
    return json.loads(registry_path.read_text(encoding="utf-8"))


def parse_table_target(line: str) -> str | None:
    match = TABLE_ROW_RE.match(line)
    if not match:
        return None
    first_col = match.group(1).strip()
    if first_col.startswith("---") or first_col.lower().startswith("connects to"):
        return None
    bold = BOLD_RE.search(first_col)
    return bold.group(1).strip() if bold else first_col.strip()


def build_manifest(guide_text: str, registry: dict, source_path: str) -> dict:
    registry_surfaces = registry.get("surfaces", [])
    registry_slugs = {
        row.get("slug")
        for row in registry_surfaces
        if isinstance(row, dict) and isinstance(row.get("slug"), str)
    }

    connectors: list[dict] = []
    by_source: dict[str, int] = {}

    current_section: str | None = None
    in_ai_section = False
    ai_source_slug: str | None = None

    for raw_line in guide_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        heading = HEADING_RE.match(line)
        if heading:
            current_section = heading.group(1).strip()
            in_ai_section = current_section.startswith("AI Platform Integrations")
            ai_source_slug = None
            continue

        if in_ai_section:
            sub = SUB_HEADING_RE.match(line)
            if sub:
                ai_name = sub.group(1).strip()
                ai_source_slug = AI_SOURCE_MAP.get(ai_name)
                continue
            conn = CONNECTS_TO_RE.match(line)
            if conn and ai_source_slug:
                targets = [item.strip() for item in conn.group(1).split(",") if item.strip()]
                for target_label in targets:
                    target_slug, target_kind = normalize_target(target_label)
                    idx = by_source.get(ai_source_slug, 0) + 1
                    by_source[ai_source_slug] = idx
                    connectors.append(
                        {
                            "id": f"{ai_source_slug}--{target_slug}--{idx}",
                            "source_slug": ai_source_slug,
                            "target_slug": target_slug,
                            "target_kind": target_kind,
                            "connector_type": "native_app_connector",
                            "auth_mode": "oauth_popup",
                            "state": "user_claimed_configured_unverified",
                            "source_section": current_section,
                            "source_label": ai_source_slug,
                            "target_label": target_label,
                        }
                    )
                continue

        if current_section in SOURCE_MAP:
            target_label = parse_table_target(line)
            if not target_label:
                continue
            for source_slug in SOURCE_MAP[current_section]:
                target_slug, target_kind = normalize_target(target_label)
                idx = by_source.get(source_slug, 0) + 1
                by_source[source_slug] = idx
                connectors.append(
                    {
                        "id": f"{source_slug}--{target_slug}--{idx}",
                        "source_slug": source_slug,
                        "target_slug": target_slug,
                        "target_kind": target_kind,
                        "connector_type": "native_platform_integration",
                        "auth_mode": "oauth_popup",
                        "state": "user_claimed_configured_unverified",
                        "source_section": current_section,
                        "source_label": current_section,
                        "target_label": target_label,
                    }
                )

    source_slugs = sorted({row["source_slug"] for row in connectors})
    source_profiles: list[dict] = []
    for slug in sorted(registry_slugs):
        source_profiles.append(
            {
                "source_slug": slug,
                "profile_state": "documented_in_guide" if slug in source_slugs else "no_native_connector_map_captured_yet",
            }
        )

    unknown_sources = sorted(
        {
            row["source_slug"]
            for row in connectors
            if row["source_slug"] not in registry_slugs
        }
    )
    internal_targets = [row for row in connectors if row["target_kind"] == "registry"]
    unknown_internal_targets = sorted(
        {row["target_slug"] for row in internal_targets if row["target_slug"] not in registry_slugs}
    )

    return {
        "generated_at": utc_now(),
        "status": "user_claimed_unverified",
        "version": "cc91",
        "source_artifact": source_path,
        "canonical_identity": registry.get("canonical_identity"),
        "canonical_workspace_domain": registry.get("canonical_workspace_domain"),
        "connector_auth_baseline": "oauth_popup",
        "counts": {
            "connector_count": len(connectors),
            "source_count": len(source_slugs),
            "source_profile_count": len(source_profiles),
            "external_target_count": sum(1 for row in connectors if row["target_kind"] == "external"),
        },
        "source_profiles": source_profiles,
        "connectors": connectors,
        "gaps": {
            "unknown_sources_not_in_registry": unknown_sources,
            "unknown_internal_targets_not_in_registry": unknown_internal_targets,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--guide", required=True, help="Path to integration guide markdown.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument(
        "--output",
        default=str(REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-CONNECTOR-MANIFEST-CC91.json"),
    )
    args = parser.parse_args()

    guide_path = Path(args.guide).expanduser().resolve()
    registry_path = Path(args.registry).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    registry = load_registry(registry_path)
    manifest = build_manifest(
        guide_text=guide_path.read_text(encoding="utf-8"),
        registry=registry,
        source_path=str(guide_path),
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

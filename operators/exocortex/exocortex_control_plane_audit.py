#!/usr/bin/env python3
"""Audit exocortex control-plane tractability from surface, teleology, and connector manifests."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTRY = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-SURFACE-REGISTRY-CC90.json"
DEFAULT_TELEOLOGY = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-TELEOLOGY-REGISTRY-CC90.json"
DEFAULT_CONNECTOR = REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-CONNECTOR-MANIFEST-CC91.json"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def top_n(counter: Counter[str], n: int = 10) -> list[dict[str, Any]]:
    return [{"slug": slug, "count": count} for slug, count in counter.most_common(n)]


def build_status(registry: dict[str, Any], teleology: dict[str, Any], connector: dict[str, Any]) -> dict[str, Any]:
    registry_surfaces = registry.get("surfaces", [])
    teleology_surfaces = teleology.get("surfaces", [])
    connectors = connector.get("connectors", [])
    profiles = connector.get("source_profiles", [])

    registry_slugs = {
        row.get("slug")
        for row in registry_surfaces
        if isinstance(row, dict) and isinstance(row.get("slug"), str)
    }
    teleology_slugs = {
        row.get("slug")
        for row in teleology_surfaces
        if isinstance(row, dict) and isinstance(row.get("slug"), str)
    }

    source_counter: Counter[str] = Counter()
    target_counter: Counter[str] = Counter()
    state_counter: Counter[str] = Counter()
    external_targets = 0
    unresolved_sources = set()
    unresolved_internal_targets = set()
    source_external_counts: defaultdict[str, int] = defaultdict(int)

    for edge in connectors:
        if not isinstance(edge, dict):
            continue
        source = edge.get("source_slug")
        target = edge.get("target_slug")
        target_kind = edge.get("target_kind")
        state = edge.get("state", "unknown")
        if isinstance(source, str):
            source_counter[source] += 1
            if source not in registry_slugs:
                unresolved_sources.add(source)
        if isinstance(target, str):
            target_counter[target] += 1
            if target_kind == "registry" and target not in registry_slugs:
                unresolved_internal_targets.add(target)
        if target_kind == "external":
            external_targets += 1
            if isinstance(source, str):
                source_external_counts[source] += 1
        state_counter[str(state)] += 1

    profile_missing = sorted(
        {
            row.get("source_slug")
            for row in profiles
            if isinstance(row, dict)
            and row.get("profile_state") == "no_native_connector_map_captured_yet"
            and isinstance(row.get("source_slug"), str)
        }
    )
    teleology_missing = sorted(registry_slugs - teleology_slugs)

    high_fanout = [row for row in top_n(source_counter, n=20) if row["count"] >= 8]
    cross_boundary_heavy = []
    for slug, count in source_counter.items():
        external = source_external_counts.get(slug, 0)
        if count >= 5 and external / max(1, count) >= 0.5:
            cross_boundary_heavy.append(
                {
                    "slug": slug,
                    "connector_count": count,
                    "external_connector_count": external,
                    "external_ratio": round(external / count, 3),
                }
            )

    coverage_pct = round((len(registry_slugs - set(profile_missing)) / max(1, len(registry_slugs))) * 100, 2)
    readiness = {
        "surface_profile_coverage_pct": coverage_pct,
        "teleology_coverage_pct": round((len(registry_slugs & teleology_slugs) / max(1, len(registry_slugs))) * 100, 2),
        "connector_state_distribution": dict(sorted(state_counter.items())),
        "control_plane_readiness": "bounded_unverified"
        if state_counter.get("user_claimed_configured_unverified", 0) > 0
        else "verified",
    }

    recommendations = [
        "verify high-fanout hubs first (Slack, Notion, ClickUp, Linear, Atlassian lanes).",
        "convert user-claimed connector state to evidence-backed state with receipt pointers.",
        "keep external-target connectors under least-privilege scopes and periodic token rotation.",
        "promote connector verification artifacts into repo and re-run ontology projection after each tranche.",
    ]

    return {
        "generated_at": utc_now(),
        "status": "active",
        "version": "cc91",
        "counts": {
            "registry_surface_count": len(registry_slugs),
            "teleology_surface_count": len(teleology_slugs),
            "connector_count": len(connectors),
            "connector_source_count": len(source_counter),
            "external_target_connector_count": external_targets,
            "unresolved_source_count": len(unresolved_sources),
            "unresolved_internal_target_count": len(unresolved_internal_targets),
            "profile_missing_count": len(profile_missing),
            "high_fanout_count": len(high_fanout),
            "cross_boundary_heavy_count": len(cross_boundary_heavy),
        },
        "coverage": {
            "teleology_missing_slugs": teleology_missing,
            "connector_profile_missing_slugs": profile_missing,
            "unresolved_connector_sources": sorted(unresolved_sources),
            "unresolved_internal_targets": sorted(unresolved_internal_targets),
        },
        "hubs": {
            "top_source_fanout": top_n(source_counter),
            "top_target_inflow": top_n(target_counter),
            "high_fanout_sources": high_fanout,
            "cross_boundary_heavy_sources": sorted(cross_boundary_heavy, key=lambda item: item["external_ratio"], reverse=True),
        },
        "readiness": readiness,
        "recommendations": recommendations,
    }


def render_markdown(status: dict[str, Any]) -> str:
    lines = [
        "# Exocortex Control Plane Status — CC91",
        "",
        f"- Generated: `{status['generated_at']}`",
        f"- Control plane readiness: `{status['readiness']['control_plane_readiness']}`",
        f"- Surface profile coverage: `{status['readiness']['surface_profile_coverage_pct']}%`",
        f"- Teleology coverage: `{status['readiness']['teleology_coverage_pct']}%`",
        "",
        "## Counts",
        "",
    ]
    for key, value in sorted(status["counts"].items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## Coverage Gaps", ""])
    for key, value in status["coverage"].items():
        if isinstance(value, list):
            lines.append(f"- `{key}`: `{len(value)}`")
        else:
            lines.append(f"- `{key}`: `{value}`")
    lines.extend(["", "## High Fanout Sources", ""])
    high_fanout = status["hubs"]["high_fanout_sources"]
    if not high_fanout:
        lines.append("- none")
    else:
        for row in high_fanout:
            lines.append(f"- `{row['slug']}`: `{row['count']}` connectors")
    lines.extend(["", "## Recommendations", ""])
    for item in status["recommendations"]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY))
    parser.add_argument("--teleology", default=str(DEFAULT_TELEOLOGY))
    parser.add_argument("--connector-manifest", default=str(DEFAULT_CONNECTOR))
    parser.add_argument(
        "--output-json",
        default=str(REPO_ROOT / "orchestration" / "state" / "EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json"),
    )
    parser.add_argument(
        "--output-md",
        default=str(REPO_ROOT / "orchestration" / "state" / "impl" / "EXOCORTEX-CONTROL-PLANE-STATUS-CC91.md"),
    )
    args = parser.parse_args()

    registry = load_json(Path(args.registry).expanduser().resolve())
    teleology = load_json(Path(args.teleology).expanduser().resolve())
    connector = load_json(Path(args.connector_manifest).expanduser().resolve())
    status = build_status(registry, teleology, connector)

    output_json = Path(args.output_json).expanduser().resolve()
    output_md = Path(args.output_md).expanduser().resolve()
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(status), encoding="utf-8")
    print(output_json)
    print(output_md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

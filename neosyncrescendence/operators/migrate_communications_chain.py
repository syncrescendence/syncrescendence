#!/usr/bin/env python3
"""Absorb a communications chain into neosyncrescendence."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil


SANDBOX_ROOT = Path(__file__).resolve().parents[1]
COMMUNICATIONS_DIR = SANDBOX_ROOT / "communications"
PROMPTS_DIR = COMMUNICATIONS_DIR / "prompts"
RESPONSES_DIR = COMMUNICATIONS_DIR / "responses"
ASSESSMENTS_DIR = COMMUNICATIONS_DIR / "assessments"


def ensure_dirs() -> None:
    for path in (PROMPTS_DIR, RESPONSES_DIR, ASSESSMENTS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def resolve_input(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = (Path.cwd() / path).resolve()
    else:
        path = path.resolve()
    if not path.exists():
        raise SystemExit(f"Input does not exist: {path}")
    if path.suffix.lower() != ".md":
        raise SystemExit(f"Only markdown artifacts are supported: {path}")
    return path


def copy_into(target_dir: Path, source: Path) -> Path:
    target = target_dir / source.name
    if source.resolve() != target.resolve():
        shutil.copy2(source, target)
    return target


def sandbox_link(path: Path) -> str:
    return f"/Users/system/syncrescendence/neosyncrescendence/{path.relative_to(SANDBOX_ROOT)}"


def write_tranche_note(
    *,
    tranche_slug: str,
    prompt_targets: list[Path],
    response_targets: list[Path],
    assessment_targets: list[Path],
    note: str | None,
) -> Path:
    tranche_name = f"COMMUNICATIONS-MIGRATION-{tranche_slug}.md"
    tranche_path = ASSESSMENTS_DIR / tranche_name
    lines = [
        f"# Communications Migration {tranche_slug}",
        "",
        "**Status**: completed",
        "**Purpose**: record a migrated communications lineage absorbed into `neosyncrescendence`",
        "",
        "## Imported Prompts",
        "",
    ]
    if prompt_targets:
        lines.extend(f"- [{path.name}]({sandbox_link(path)})" for path in prompt_targets)
    else:
        lines.append("- none")
    lines.extend(["", "## Imported Responses", ""])
    if response_targets:
        lines.extend(f"- [{path.name}]({sandbox_link(path)})" for path in response_targets)
    else:
        lines.append("- none")
    lines.extend(["", "## Imported Assessments", ""])
    if assessment_targets:
        lines.extend(f"- [{path.name}]({sandbox_link(path)})" for path in assessment_targets)
    else:
        lines.append("- none")
    if note:
        lines.extend(["", "## Note", "", note])
    tranche_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return tranche_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", action="append", default=[])
    parser.add_argument("--response", action="append", default=[])
    parser.add_argument("--assessment", action="append", default=[])
    parser.add_argument("--tranche-slug", required=True, help="Short slug or id, e.g. TRANCHE-02")
    parser.add_argument("--note")
    args = parser.parse_args()

    if not args.prompt and not args.response and not args.assessment:
        raise SystemExit("At least one prompt, response, or assessment is required.")

    ensure_dirs()
    prompt_targets = [copy_into(PROMPTS_DIR, resolve_input(item)) for item in args.prompt]
    response_targets = [copy_into(RESPONSES_DIR, resolve_input(item)) for item in args.response]
    assessment_targets = [copy_into(ASSESSMENTS_DIR, resolve_input(item)) for item in args.assessment]
    tranche_path = write_tranche_note(
        tranche_slug=args.tranche_slug,
        prompt_targets=prompt_targets,
        response_targets=response_targets,
        assessment_targets=assessment_targets,
        note=args.note,
    )
    print(tranche_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

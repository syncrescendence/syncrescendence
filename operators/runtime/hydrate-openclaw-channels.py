#!/usr/bin/env python3
"""Hydrate local OpenClaw channel credentials from macOS Keychain."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
KEYCHAIN_SERVICE = "syncrescendence"


def keychain_password(account: str) -> str | None:
    command = [
        "security",
        "find-generic-password",
        "-s",
        KEYCHAIN_SERVICE,
        "-a",
        account,
        "-w",
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def load_config() -> dict:
    if not OPENCLAW_CONFIG.exists():
        raise SystemExit(f"OpenClaw config not found: {OPENCLAW_CONFIG}")
    return json.loads(OPENCLAW_CONFIG.read_text(encoding="utf-8"))


def hydrate(config: dict) -> tuple[dict, list[str]]:
    changed: list[str] = []
    channels = config.setdefault("channels", {})

    slack = channels.setdefault("slack", {})
    slack_bot = keychain_password("slack-bot-token")
    slack_app = keychain_password("slack-app-token")
    if slack_bot and slack.get("botToken") != slack_bot:
        slack["botToken"] = slack_bot
        changed.append("slack.botToken")
    if slack_app and slack.get("appToken") != slack_app:
        slack["appToken"] = slack_app
        changed.append("slack.appToken")
    if slack_bot and slack_app and not slack.get("enabled"):
        slack["enabled"] = True
        changed.append("slack.enabled")

    discord = channels.setdefault("discord", {})
    discord_bot = keychain_password("discord-bot-token")
    if discord_bot and discord.get("token") != discord_bot:
        discord["token"] = discord_bot
        changed.append("discord.token")
    if discord_bot and not discord.get("enabled"):
        discord["enabled"] = True
        changed.append("discord.enabled")

    return config, changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Only report whether hydration would change config.")
    args = parser.parse_args()

    config = load_config()
    hydrated, changed = hydrate(config)
    if args.check:
        if changed:
            print("Would update:", ", ".join(changed))
        else:
            print("OpenClaw channel credentials already match Keychain.")
        return 0

    if changed:
        OPENCLAW_CONFIG.write_text(json.dumps(hydrated, indent=2) + "\n", encoding="utf-8")
        print("Updated:", ", ".join(changed))
    else:
        print("OpenClaw channel credentials already match Keychain.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

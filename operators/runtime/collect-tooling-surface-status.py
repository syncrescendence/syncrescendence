#!/usr/bin/env python3
"""Collect repo-safe local tooling and domain readiness status."""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent
STATE_DIR = REPO_ROOT / "00-ORCHESTRATION" / "state"
JSON_PATH = STATE_DIR / "LOCAL-SURFACE-STATUS.json"
MD_PATH = STATE_DIR / "LOCAL-SURFACE-STATUS.md"
CLAUDE_CONFIG_PATH = Path.home() / ".claude.json"

KEYCHAIN_CANDIDATES = {
    "gcloud_account": [("syncrescendence", "gcloud-account")],
    "cloudflare_account_id": [("syncrescendence", "cloudflare-account-id")],
    "wrangler_account": [("syncrescendence", "wrangler-account")],
    "manus_api_key": [
        ("manus-api-key", "syncrescendence"),
        ("syncrescendence", "manus-api-key"),
    ],
}

TUNNEL_NAME = "syncrescendence-ontology"
TUNNEL_CONFIG_PATH = Path.home() / ".cloudflared" / "config.yml"
TUNNEL_CERT_PATH = Path.home() / ".cloudflared" / "cert.pem"
TUNNEL_LAUNCHD_LABEL = "com.syncrescendence.cloudflared-ontology"


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def run_command(command: list[str], timeout: float = 5.0) -> tuple[int | None, str, str, bool]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout,
        )
        return result.returncode, result.stdout, result.stderr, False
    except subprocess.TimeoutExpired as exc:
        return None, exc.stdout or "", exc.stderr or "", True


def keychain_item_status(service: str, account: str, timeout: float = 2.0) -> dict[str, Any]:
    code, stdout, stderr, timed_out = run_command(
        [
            "security",
            "find-generic-password",
            "-s",
            service,
            "-a",
            account,
        ],
        timeout=timeout,
    )
    if timed_out:
        return {"present": False, "timed_out": True}
    if code != 0:
        return {"present": False, "error": (stderr or stdout).strip() or None}

    created_at = None
    modified_at = None
    for line in stdout.splitlines():
        if '"cdat"' in line and "202" in line:
            created_at = line.split('"')[-2].replace("\\000", "")
        if '"mdat"' in line and "202" in line:
            modified_at = line.split('"')[-2].replace("\\000", "")
    return {
        "present": True,
        "service": service,
        "account": account,
        "created_at": created_at,
        "modified_at": modified_at,
    }


def resolve_candidate_group(name: str) -> dict[str, Any]:
    candidates = KEYCHAIN_CANDIDATES[name]
    attempts: list[dict[str, Any]] = []
    for service, account in candidates:
        status = keychain_item_status(service, account)
        attempts.append(status)
        if status.get("present"):
            return {"name": name, "present": True, "selected": status, "attempts": attempts}
    return {"name": name, "present": False, "attempts": attempts}


def gcloud_status() -> dict[str, Any]:
    code, stdout, stderr, timed_out = run_command(["gcloud", "auth", "list", "--format=json"])
    if timed_out:
        return {"available": True, "timed_out": True}
    if code != 0:
        return {"available": False, "error": (stderr or stdout).strip() or None}
    rows = json.loads(stdout or "[]")
    active = next((item for item in rows if item.get("status") == "ACTIVE"), None)
    return {
        "available": True,
        "authenticated": bool(active),
        "active_account": active.get("account") if active else None,
        "accounts": rows,
    }


def wrangler_status() -> dict[str, Any]:
    code, stdout, stderr, timed_out = run_command(["wrangler", "whoami", "--json"])
    if timed_out:
        return {"available": True, "timed_out": True}
    if code != 0:
        return {"available": False, "error": (stderr or stdout).strip() or None}
    payload = json.loads(stdout or "{}")
    primary_account = (payload.get("accounts") or [{}])[0]
    return {
        "available": True,
        "authenticated": bool(payload.get("loggedIn")),
        "email": payload.get("email"),
        "auth_type": payload.get("authType"),
        "account_id": primary_account.get("id"),
        "account_name": primary_account.get("name"),
        "token_permissions": payload.get("tokenPermissions", []),
    }


def openclaw_channel_status() -> dict[str, Any]:
    code, stdout, stderr, timed_out = run_command(
        ["openclaw", "channels", "status", "--probe", "--json"],
        timeout=20.0,
    )
    if timed_out:
        return {"available": True, "timed_out": True}
    if code != 0:
        return {"available": False, "error": (stderr or stdout).strip() or None}
    payload = json.loads(stdout or "{}")
    channels = payload.get("channels", {})
    channel_accounts = payload.get("channelAccounts", {})
    return {
        "available": True,
        "captured_at_ms": payload.get("ts"),
        "channels": channels,
        "channel_accounts": channel_accounts,
    }


def http_status(url: str, timeout: float = 5.0) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "syncrescendence-status/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(body)
            except Exception:
                payload = None
            return {
                "reachable": True,
                "status_code": response.status,
                "payload": payload,
            }
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(body)
        except Exception:
            payload = None
        return {"reachable": True, "status_code": exc.code, "payload": payload}
    except Exception as exc:
        return {"reachable": False, "error": str(exc)}


def dns_status(hostname: str) -> dict[str, Any]:
    try:
        host, aliases, addrs = socket.gethostbyname_ex(hostname)
        return {"resolves": True, "host": host, "aliases": aliases, "addresses": addrs}
    except Exception as exc:
        return {"resolves": False, "error": str(exc)}


def dig_status(hostname: str) -> dict[str, Any]:
    code, stdout, stderr, timed_out = run_command(["dig", "+short", hostname], timeout=5.0)
    if timed_out:
        return {"resolves": False, "timed_out": True}
    if code != 0:
        return {"resolves": False, "error": (stderr or stdout).strip() or None}
    records = [line.strip() for line in stdout.splitlines() if line.strip()]
    return {"resolves": bool(records), "records": records}


def curl_resolved_health(hostname: str, address: str) -> dict[str, Any]:
    code, stdout, stderr, timed_out = run_command(
        [
            "curl",
            "--silent",
            "--show-error",
            "--output",
            "/dev/null",
            "--write-out",
            "%{http_code}",
            "--max-time",
            "10",
            "--resolve",
            f"{hostname}:443:{address}",
            f"https://{hostname}/health",
        ],
        timeout=15.0,
    )
    if timed_out:
        return {"reachable": False, "timed_out": True, "address": address}
    if code != 0:
        return {
            "reachable": False,
            "address": address,
            "error": (stderr or stdout).strip() or None,
        }
    try:
        status_code = int((stdout or "0").strip())
    except ValueError:
        status_code = None
    return {
        "reachable": bool(status_code and 200 <= status_code < 500),
        "status_code": status_code,
        "address": address,
    }


def cloudflared_status() -> dict[str, Any]:
    version_code, version_stdout, version_stderr, version_timed_out = run_command(
        ["cloudflared", "--version"],
        timeout=5.0,
    )
    status: dict[str, Any] = {
        "installed": not version_timed_out and version_code == 0,
        "cert_present": TUNNEL_CERT_PATH.exists(),
        "config_present": TUNNEL_CONFIG_PATH.exists(),
    }
    if version_timed_out:
        status["version_timed_out"] = True
    elif version_code == 0:
        status["version"] = (version_stdout or "").strip().splitlines()[0]
    else:
        status["version_error"] = (version_stderr or version_stdout).strip() or None

    info_code, info_stdout, info_stderr, info_timed_out = run_command(
        ["cloudflared", "tunnel", "info", TUNNEL_NAME],
        timeout=5.0,
    )
    if info_timed_out:
        status["tunnel_info_timed_out"] = True
        return status
    if info_code != 0:
        status["tunnel_present"] = False
        status["tunnel_error"] = (info_stderr or info_stdout).strip() or None
        return status

    tunnel_id = None
    connection_lines: list[str] = []
    for line in info_stdout.splitlines():
        if line.startswith("ID:"):
            tunnel_id = line.split(":", 1)[1].strip()
        if line.strip().startswith("a") and "EDGE" in info_stdout:
            connection_lines.append(line.strip())

    status.update(
        {
            "tunnel_present": True,
            "tunnel_name": TUNNEL_NAME,
            "tunnel_id": tunnel_id,
            "connections": connection_lines,
        }
    )
    return status


def launch_agent_status(label: str) -> dict[str, Any]:
    uid = str(__import__("os").getuid())
    code, stdout, stderr, timed_out = run_command(
        ["launchctl", "print", f"gui/{uid}/{label}"],
        timeout=5.0,
    )
    if timed_out:
        return {"loaded": False, "timed_out": True}
    if code != 0:
        return {"loaded": False, "error": (stderr or stdout).strip() or None}

    state = None
    pid = None
    for line in stdout.splitlines():
        stripped = line.strip()
        if stripped.startswith("state = "):
            state = stripped.split("=", 1)[1].strip()
        if stripped.startswith("pid = "):
            pid = stripped.split("=", 1)[1].strip()
    return {
        "loaded": True,
        "state": state,
        "pid": pid,
    }


def manus_status(keychain_status: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {
        "keychain": keychain_status,
    }
    selected = keychain_status.get("selected")
    if not selected or not selected.get("present"):
        result["reachable"] = False
        result["reason"] = "manus_api_key_missing"
        return result

    service = selected["service"]
    account = selected["account"]
    code, stdout, stderr, timed_out = run_command(
        ["security", "find-generic-password", "-s", service, "-a", account, "-w"],
        timeout=2.0,
    )
    if timed_out:
        result["reachable"] = False
        result["reason"] = "manus_key_read_timed_out"
        return result
    if code != 0:
        result["reachable"] = False
        result["reason"] = "manus_key_read_failed"
        result["error"] = (stderr or stdout).strip() or None
        return result

    key = stdout.strip()
    request = urllib.request.Request(
        "https://api.manus.ai/v1/tasks",
        headers={"API_KEY": key, "User-Agent": "syncrescendence-status/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=5.0) as response:
            body = response.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(body)
            except Exception:
                payload = None
            result.update(
                {
                    "reachable": True,
                    "status_code": response.status,
                    "response_shape": type(payload).__name__ if payload is not None else "unknown",
                }
            )
            if isinstance(payload, list):
                result["task_count"] = len(payload)
    except urllib.error.HTTPError as exc:
        result.update({"reachable": True, "status_code": exc.code})
    except Exception as exc:
        result.update({"reachable": False, "reason": "http_error", "error": str(exc)})
    return result


def claude_code_status() -> dict[str, Any]:
    if not CLAUDE_CONFIG_PATH.exists():
        return {"available": False, "reason": "config_missing"}
    try:
        payload = json.loads(CLAUDE_CONFIG_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"available": False, "reason": "config_unreadable", "error": str(exc)}

    account = payload.get("oauthAccount") or {}
    return {
        "available": True,
        "authenticated": bool(account),
        "email": account.get("emailAddress"),
        "display_name": account.get("displayName"),
        "organization_name": account.get("organizationName"),
        "organization_uuid": account.get("organizationUuid"),
        "billing_type": account.get("billingType"),
    }


def collect() -> dict[str, Any]:
    gcloud_keychain = resolve_candidate_group("gcloud_account")
    cloudflare_keychain = resolve_candidate_group("cloudflare_account_id")
    wrangler_keychain = resolve_candidate_group("wrangler_account")
    manus_keychain = resolve_candidate_group("manus_api_key")

    domain_dns = dns_status("syncrescendence.com")
    domain_dig = dig_status("syncrescendence.com")
    domain_health = http_status("https://syncrescendence.com/health")
    domain_health_edge = None
    if domain_dig.get("resolves"):
        records = domain_dig.get("records") or []
        for record in records:
            probe = curl_resolved_health("syncrescendence.com", record)
            if probe.get("reachable"):
                domain_health_edge = probe
                break
        if domain_health_edge is None and records:
            domain_health_edge = curl_resolved_health("syncrescendence.com", records[0])

    return {
        "captured_at": utc_now(),
        "claude_code": claude_code_status(),
        "openclaw_channels": openclaw_channel_status(),
        "gcloud": {
            "cli": gcloud_status(),
            "keychain": gcloud_keychain,
        },
        "wrangler": {
            "cli": wrangler_status(),
            "keychain": {
                "wrangler_account": wrangler_keychain,
                "cloudflare_account_id": cloudflare_keychain,
            },
        },
        "manus": manus_status(manus_keychain),
        "cloudflared": {
            **cloudflared_status(),
            "launch_agent": launch_agent_status(TUNNEL_LAUNCHD_LABEL),
        },
        "ontology": {
            "local_api": http_status("http://127.0.0.1:8787/health"),
            "local_proxy": http_status("http://localhost:8080/health"),
            "domain_dns": domain_dns,
            "domain_dig": domain_dig,
            "domain_health": domain_health,
            "domain_health_edge": domain_health_edge,
        },
    }


def write_report(report: dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    claude_code = report["claude_code"]
    gcloud_cli = report["gcloud"]["cli"]
    wrangler_cli = report["wrangler"]["cli"]
    manus = report["manus"]
    cloudflared = report["cloudflared"]
    openclaw_channels = report["openclaw_channels"]
    ontology = report["ontology"]
    lines = [
        "# Local Surface Status",
        "",
        f"**Captured**: {report['captured_at']}",
        "",
        "## Auth Surfaces",
        "",
        f"- `claude` authenticated: `{claude_code.get('authenticated')}`",
        f"- `claude` email: `{claude_code.get('email')}`",
        f"- `claude` organization: `{claude_code.get('organization_name')}`",
        f"- `claude` billing type: `{claude_code.get('billing_type')}`",
        f"- `gcloud` authenticated: `{gcloud_cli.get('authenticated')}`",
        f"- `gcloud` active account: `{gcloud_cli.get('active_account')}`",
        f"- `gcloud` keychain pointer present: `{report['gcloud']['keychain'].get('present')}`",
        f"- `wrangler` authenticated: `{wrangler_cli.get('authenticated')}`",
        f"- `wrangler` email: `{wrangler_cli.get('email')}`",
        f"- `wrangler` account id: `{wrangler_cli.get('account_id')}`",
        f"- Cloudflare account-id keychain pointer present: `{report['wrangler']['keychain']['cloudflare_account_id'].get('present')}`",
        f"- Manus keychain pointer present: `{manus.get('keychain', {}).get('present')}`",
        f"- Manus API reachable: `{manus.get('reachable')}`",
        "",
        "## OpenClaw Channels",
        "",
    ]
    if openclaw_channels.get("available"):
        for channel in ("slack", "discord"):
            channel_data = (openclaw_channels.get("channels") or {}).get(channel, {})
            account = ((openclaw_channels.get("channel_accounts") or {}).get(channel) or [{}])[0]
            lines.extend(
                [
                    f"- `{channel}` running: `{channel_data.get('running')}`",
                    f"- `{channel}` probe ok: `{(channel_data.get('probe') or {}).get('ok')}`",
                    f"- `{channel}` last inbound observed: `{account.get('lastInboundAt')}`",
                    f"- `{channel}` last outbound observed: `{account.get('lastOutboundAt')}`",
                ]
            )
            if channel == "slack":
                team = (channel_data.get("probe") or {}).get("team", {})
                if team:
                    lines.append(f"- `slack` workspace: `{team.get('name')}` (`{team.get('id')}`)")
            if channel == "discord":
                bot = (channel_data.get("probe") or {}).get("bot", {})
                if bot:
                    lines.append(f"- `discord` bot: `{bot.get('username')}` (`{bot.get('id')}`)")
    else:
        lines.append(f"- OpenClaw channel probe unavailable: `{openclaw_channels.get('error') or 'unknown'}`")
    lines.extend(
        [
            "",
        "## Ontology Domain Readiness",
        "",
        f"- Local API reachable: `{ontology['local_api'].get('reachable')}`",
        f"- Local proxy reachable: `{ontology['local_proxy'].get('reachable')}`",
        f"- macOS resolver sees domain: `{ontology['domain_dns'].get('resolves')}`",
        f"- `dig` sees public records: `{ontology['domain_dig'].get('resolves')}`",
        f"- Direct public edge health reachable: `{(ontology.get('domain_health_edge') or {}).get('reachable')}`",
        f"- Default local domain health reachable: `{ontology['domain_health'].get('reachable')}`",
        "",
        "## Tunnel",
        "",
        f"- `cloudflared` installed: `{cloudflared.get('installed')}`",
        f"- Cloudflare tunnel cert present: `{cloudflared.get('cert_present')}`",
        f"- Local tunnel config present: `{cloudflared.get('config_present')}`",
        f"- Named tunnel present: `{cloudflared.get('tunnel_present')}`",
        f"- Tunnel LaunchAgent loaded: `{cloudflared.get('launch_agent', {}).get('loaded')}`",
        f"- Tunnel LaunchAgent state: `{cloudflared.get('launch_agent', {}).get('state')}`",
        "",
        "## Reading",
        "",
        "- Local auth and serving surfaces can be checked without exposing secrets in repo artifacts.",
        "- Slack and Discord may be healthy and authenticated before any real inbound/outbound traffic is observed.",
        "- If `dig` and direct edge health are green while default local curl still fails, the public cutover is live and only the local resolver is stale.",
        "- CLI and Keychain status should remain pointer-only; credentials stay local.",
        "",
    ])
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    report = collect()
    write_report(report)
    print(f"Wrote tooling surface status to {JSON_PATH} and {MD_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

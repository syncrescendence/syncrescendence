#!/usr/bin/env python3
"""Thin operational webshell for development-time status/docs/callback intake."""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


ALLOWED_CALLBACK_SURFACES = {"github", "slack", "discord", "cloudflare", "generic"}
ALLOWED_ARTIFACT_PREFIXES = (
    "communications/",
    "orchestration/state/",
    "offices/",
    "runtime/",
)
SURFACE_SLUG_RE = re.compile(r"^[a-z0-9_-]+$")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def make_task_envelope(
    *,
    line_id: str,
    surface: str,
    callback_path: str,
    sender: str = "webshell-callback",
) -> str:
    return (
        "# TASK\n\n"
        "**Kind**: TASK\n"
        f"**Line-ID**: {line_id}\n"
        f"**From**: {sender}\n"
        "**To**: commander\n"
        "**Reply-To**: offices/commander/inbox/pending\n"
        "**CC**:\n"
        f"**Issued-At**: {utc_now()}\n"
        "**Priority**: normal\n"
        "**Decision-Envelope**: callback-ingest\n"
        "**Objective-Lock**: classify and route callback safely\n"
        "**Expected-Output**: receipt + routed artifact\n"
        "**Receipts-Required**: Yes\n"
        "**Completion-Condition**: callback reviewed and next action staged\n"
        "**Escalation-Path**: offices/commander/inbox/blocked\n\n"
        "## Payload\n\n"
        f"New `{surface}` callback captured by webshell.\n\n"
        f"- callback artifact: `{callback_path}`\n"
    )


class DevShellHandler(BaseHTTPRequestHandler):
    server: "DevShellServer"

    def log_message(self, fmt: str, *args: object) -> None:
        message = fmt % args
        print(f"[{utc_now()}] webshell {self.address_string()} {message}", flush=True)

    def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, indent=2, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text: str, status: int = 200) -> None:
        body = text.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, html: str, status: int = 200) -> None:
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _artifact_path(self, rel: str) -> Path | None:
        rel = rel.strip().lstrip("/")
        if not rel:
            return None
        if not rel.startswith(ALLOWED_ARTIFACT_PREFIXES):
            return None
        candidate = (self.server.repo_root / rel).resolve()
        try:
            candidate.relative_to(self.server.repo_root)
        except ValueError:
            return None
        return candidate

    def _status_payload(self) -> dict[str, Any]:
        repo_root = self.server.repo_root
        tracker = safe_load_json(repo_root / "orchestration/state/IDENTITY-CUTOVER-TRACKER-CC81.json")
        ledger = safe_load_json(repo_root / "orchestration/state/EXOCORTEX-CENTRALIZATION-LEDGER-CC82.json")
        local_surface = safe_load_json(repo_root / "orchestration/state/LOCAL-SURFACE-STATUS.json")
        return {
            "status": "ok",
            "captured_at": utc_now(),
            "repo_root": str(repo_root),
            "identity_cutover": {
                "phase_status": (tracker or {}).get("phase_status"),
                "active_blockers": (tracker or {}).get("active_blockers"),
                "manus_tasks": {
                    "cc82": (tracker or {}).get("intel", {}).get("manus_cc82_task_status"),
                    "cc82b": (tracker or {}).get("intel", {}).get("manus_cc82b_task_status"),
                },
            },
            "centralization_ledger": {
                "status": (ledger or {}).get("status"),
                "target_identity": (ledger or {}).get("primary_target_identity"),
                "surface_count": len((ledger or {}).get("surfaces", [])),
                "wave_order": (ledger or {}).get("wave_order"),
            },
            "local_surface_snapshot": {
                "captured_at": (local_surface or {}).get("captured_at"),
                "claude_email": (local_surface or {}).get("claude_code", {}).get("email"),
                "manus_reachable": (local_surface or {}).get("manus", {}).get("reachable"),
                "ontology_domain_reachable": (local_surface or {})
                .get("ontology", {})
                .get("domain_health", {})
                .get("reachable"),
            },
        }

    def _ontology_payload(self) -> dict[str, Any]:
        local_surface = safe_load_json(self.server.repo_root / "orchestration/state/LOCAL-SURFACE-STATUS.json") or {}
        probe_result: dict[str, Any] = {"url": self.server.ontology_health_url, "reachable": False}
        try:
            with urllib.request.urlopen(self.server.ontology_health_url, timeout=3) as response:
                body = response.read().decode("utf-8", errors="replace")
                payload = json.loads(body)
                probe_result.update(
                    {
                        "reachable": True,
                        "status_code": response.status,
                        "payload": payload,
                    }
                )
        except urllib.error.HTTPError as exc:
            probe_result.update({"status_code": exc.code, "error": str(exc)})
        except Exception as exc:  # noqa: BLE001
            probe_result["error"] = str(exc)

        return {
            "status": "ok",
            "captured_at": utc_now(),
            "configured_health_url": self.server.ontology_health_url,
            "local_snapshot_ontology": local_surface.get("ontology"),
            "live_probe": probe_result,
        }

    def _docs_html(self) -> str:
        links = [
            ("/health", "service health"),
            ("/status", "cutover + surface status"),
            ("/ontology", "ontology health and probe"),
            (
                "/artifacts/orchestration/state/impl/CC82-EXOCORTEX-CENTRALIZATION-EXECUTION-PLAN-v1.md",
                "cc82 execution plan",
            ),
            (
                "/artifacts/orchestration/state/IDENTITY-CUTOVER-TRACKER-CC81.json",
                "identity cutover tracker",
            ),
            (
                "/artifacts/orchestration/state/EXOCORTEX-CENTRALIZATION-LEDGER-CC82.json",
                "centralization ledger",
            ),
            (
                "/artifacts/communications/responses/RESPONSE-MANUS-cc82-exocortex-account-centralization-execution.md",
                "manus cc82 response index",
            ),
        ]
        items = "\n".join(f'<li><a href="{href}">{label}</a></li>' for href, label in links)
        return (
            "<!doctype html><html><head><meta charset='utf-8'>"
            "<title>Syncrescendence Dev Webshell</title></head><body>"
            "<h1>Syncrescendence Dev Webshell</h1>"
            "<p>Thin operational shell for status, docs, ontology checks, and callback intake.</p>"
            "<h2>Routes</h2><ul>"
            f"{items}"
            "</ul>"
            "<h2>Callback Intake</h2>"
            "<p>POST JSON to <code>/callbacks/{surface}</code> where surface is one of "
            "<code>github</code>, <code>slack</code>, <code>discord</code>, "
            "<code>cloudflare</code>, <code>generic</code>.</p>"
            "</body></html>"
        )

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        route = parsed.path

        if route in {"/", "/docs"}:
            self._send_html(self._docs_html(), status=200)
            return

        if route == "/health":
            self._send_json({"status": "ok", "captured_at": utc_now(), "service": "syncrescendence-dev-webshell"})
            return

        if route == "/status":
            self._send_json(self._status_payload())
            return

        if route == "/ontology":
            self._send_json(self._ontology_payload())
            return

        if route.startswith("/artifacts/"):
            rel = unquote(route[len("/artifacts/") :])
            target = self._artifact_path(rel)
            if target is None or not target.exists() or not target.is_file():
                self._send_json({"status": "error", "error": "artifact_not_found"}, status=404)
                return

            content = target.read_bytes()
            content_type, _ = mimetypes.guess_type(str(target))
            self.send_response(200)
            self.send_header("Content-Type", content_type or "application/octet-stream")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        self._send_json({"status": "error", "error": "route_not_found", "route": route}, status=404)

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        route = parsed.path
        match = re.fullmatch(r"/callbacks/([a-z0-9_-]+)", route)
        if not match:
            self._send_json({"status": "error", "error": "route_not_found"}, status=404)
            return

        surface = match.group(1)
        if not SURFACE_SLUG_RE.fullmatch(surface):
            self._send_json({"status": "error", "error": "invalid_surface"}, status=400)
            return
        if surface not in ALLOWED_CALLBACK_SURFACES:
            self._send_json({"status": "error", "error": "surface_not_allowed", "surface": surface}, status=403)
            return

        expected_token = self.server.callback_token
        if not expected_token:
            self._send_json(
                {
                    "status": "error",
                    "error": "callback_auth_not_configured",
                    "detail": "set --callback-token to enable callback ingestion",
                },
                status=503,
            )
            return

        provided_token = self.headers.get("X-Sync-Token")
        if provided_token != expected_token:
            self._send_json({"status": "error", "error": "unauthorized"}, status=401)
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            content_length = 0
        raw_body = self.rfile.read(content_length) if content_length > 0 else b""

        body_json = None
        body_text = None
        try:
            if raw_body:
                body_json = json.loads(raw_body.decode("utf-8"))
        except Exception:
            body_text = raw_body.decode("utf-8", errors="replace")

        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        line_id = f"callback-{surface}-{ts}"

        callback_dir = self.server.repo_root / "runtime/webshell/callbacks/inbox"
        callback_dir.mkdir(parents=True, exist_ok=True)
        callback_path = callback_dir / f"CALLBACK-{surface}-{ts}.json"

        callback_payload: dict[str, Any] = {
            "captured_at": utc_now(),
            "surface": surface,
            "route": route,
            "remote": self.client_address[0],
            "headers": {k: v for k, v in self.headers.items()},
        }
        if body_json is not None:
            callback_payload["body_json"] = body_json
        else:
            callback_payload["body_text"] = body_text or ""
        callback_path.write_text(json.dumps(callback_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

        inbox_dir = self.server.repo_root / "offices/commander/inbox/pending"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        task_path = inbox_dir / f"TASK-callback-{surface}-{ts}.md"
        task_path.write_text(
            make_task_envelope(
                line_id=line_id,
                surface=surface,
                callback_path=str(callback_path.relative_to(self.server.repo_root)),
            ),
            encoding="utf-8",
        )

        self._send_json(
            {
                "status": "accepted",
                "surface": surface,
                "line_id": line_id,
                "callback_artifact": str(callback_path.relative_to(self.server.repo_root)),
                "task_artifact": str(task_path.relative_to(self.server.repo_root)),
            },
            status=HTTPStatus.ACCEPTED,
        )


class DevShellServer(ThreadingHTTPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        repo_root: Path,
        ontology_health_url: str,
        callback_token: str | None,
    ) -> None:
        super().__init__(server_address, DevShellHandler)
        self.repo_root = repo_root
        self.ontology_health_url = ontology_health_url
        self.callback_token = callback_token


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=str(Path.cwd()), help="Path to syncrescendence repo root")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8890)
    parser.add_argument("--ontology-health-url", default="https://syncrescendence.com/health")
    parser.add_argument(
        "--callback-token",
        default=None,
        help="Optional shared token required via X-Sync-Token header for callback POST routes",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    server = DevShellServer(
        (args.host, args.port),
        repo_root=repo_root,
        ontology_health_url=args.ontology_health_url,
        callback_token=args.callback_token,
    )
    print(
        f"[{utc_now()}] webshell listening on http://{args.host}:{args.port} repo_root={repo_root}",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

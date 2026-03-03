# REF: Self-Healing Constitution

**Version**: 1.0.0
**Created**: 2026-02-10
**Linear**: SYN-8 / IMPL-A-0004
**Status**: CANONICAL

---

## Overview

The Syncrescendence infrastructure employs a 4-tier self-healing architecture that ensures service continuity without human intervention. Each tier escalates when the previous tier's remediation fails.

---

## Architecture

```
L0: launchd KeepAlive     Kernel-level process supervision (automatic)
  ↓ fails
L1: PID Verification      Check process liveness + launchctl kickstart
  ↓ fails
L2: HTTP Health Checks    Verify functional responses + config validation
  ↓ restart loop (>3/hour)
L3: Commander Escalation  P0 task to Commander inbox for diagnosis
```

---

## Tier Specifications

### L0: launchd KeepAlive (Kernel-Level)

**Mechanism**: macOS launchd `KeepAlive` directive in plist files.
**Scope**: All `com.syncrescendence.*` services.
**Behavior**: If a managed process dies, launchd automatically restarts it.
**Latency**: Immediate (kernel-managed).
**Configuration**: `<key>KeepAlive</key><true/>` in each plist.
**Limitation**: Only detects process death, not functional degradation.

### L1: PID Verification + Kickstart

**Implementation**: `watchdog.sh` lines 31-53.
**Schedule**: Every 5 minutes via `com.syncrescendence.watchdog`.
**Mechanism**: `launchctl list | grep <label>` to check PID. If PID is `-` or empty, issue `launchctl kickstart -k`.
**Scope**: Always-on services only:
- `chroma-server` (Chroma vector DB)
- `webhook-receiver` (webhook ingestion)
- `watch-*` (file watchers: dispatch, canon, inbox, sovereign)

**Excluded**: Interval-based services (corpus-health, qmd-update) — these run on schedule, not continuously.

### L2: HTTP Health Checks + Config Validation

**Implementation**: `watchdog.sh` lines 58-112.
**Mechanism**: `curl -s -o /dev/null -w '%{http_code}' --connect-timeout 5 <url>`.

| Service | Port | Endpoint | Management | Auto-restart |
|---------|------|----------|------------|-------------|
| Chroma | 8765 | /health | launchctl | YES |
| Webhook | 8888 | /health | launchctl | YES |
| OpenClaw | 18789 | /health | Docker | NO (info only) |
| Neo4j | 7474 | / | Docker | NO (info only) |
| Graphiti | 8001 | /healthcheck | Docker | NO (info only) |
| Qdrant | 6333 | /healthz | Docker | NO (info only) |

**Config Validation**:
- `openclaw.json` JSON parse check via Python
- Critical repo files existence: `CLAUDE.md`, `COCKPIT.md`, `README.md`

### L3: Escalation (Restart Loop Detection)

**Implementation**: `watchdog.sh` lines 117-147.
**Threshold**: >3 restarts in the last hour.
**Detection**: Counts recent entries in `/tmp/syncrescendence-watchdog-restarts.log`.
**Action**: Creates `TASK-WATCHDOG-YYYYMMDDHHMM.md` in Commander's inbox.
**Task Format**:
- Status: PENDING
- Priority: P0
- Includes: timestamp, restart count, last 10 restart log entries
- Reply-To: watchdog

---

## Service Coverage Matrix

| Service | L0 | L1 | L2 | L3 | Notes |
|---------|----|----|----|----|-------|
| Chroma (8765) | YES | YES | YES | YES | Full coverage |
| Webhook (8888) | YES | YES | YES | YES | Full coverage |
| File watchers (4x) | YES | YES | — | YES | No HTTP endpoint |
| OpenClaw (18789) | — | — | INFO | — | Docker-managed, external |
| Neo4j (7474) | — | — | INFO | — | Docker-managed |
| Graphiti (8001) | — | — | INFO | — | Docker-managed |
| Qdrant (6333) | — | — | INFO | — | Docker-managed |
| Corpus health (6h) | YES | — | — | — | Interval, not always-on |
| QMD update (1h) | YES | — | — | — | Interval, not always-on |

---

## Log Files

| Log | Path | Purpose | Rotation |
|-----|------|---------|----------|
| Main log | `/tmp/syncrescendence-watchdog.log` | All events (INFO, WARN, CRIT) | Manual / reboot |
| Restart log | `/tmp/syncrescendence-watchdog-restarts.log` | Restart events only (for L3 counting) | Manual |

---

## Invocation

```bash
# Manual run
bash ~/.syncrescendence/scripts/watchdog.sh

# launchd (automatic, every 5 minutes)
# Plist: ~/Library/LaunchAgents/com.syncrescendence.watchdog.plist

# Check status
launchctl list | grep watchdog
tail -20 /tmp/syncrescendence-watchdog.log
```

---

## Verification Checklist

- [ ] `launchctl list | grep com.syncrescendence` shows all expected services
- [ ] `curl localhost:8765/health` returns 200 (Chroma)
- [ ] `curl localhost:8888/health` returns 200 (Webhook)
- [ ] `/tmp/syncrescendence-watchdog.log` contains recent "Watchdog run" entries
- [ ] `/tmp/syncrescendence-watchdog-restarts.log` has zero or low entries in last hour
- [ ] Commander inbox has no unprocessed TASK-WATCHDOG-* files (or they've been triaged)
- [ ] `python3 -c "import json; json.load(open('$HOME/.openclaw/openclaw.json'))"` passes

---

## Constitutional Integration

This self-healing system serves **Invariant #4 (Continuation/Deletability)** — system state survives session boundaries — and **Invariant #5 (Repo Sovereignty)** — infrastructure maintains the ground truth repository's accessibility. The watchdog ensures that services supporting the Constellation remain operational between and across sessions.

---

## Cross-References

- `REF-SOVEREIGN_COCKPIT_MANIFEST.md` — Service table and launchd configurations
- `REF-ROSETTA_STONE.md` — Community pattern G1 (Self-Healing Constitution)
- `CLAUDE.md` — Constitutional invariants
- `~/.syncrescendence/scripts/watchdog.sh` — Implementation (153 lines)

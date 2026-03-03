# Syncrescendence OpenClaw Infrastructure — Definitive Treatment

**Concept**: Configuration, synchronization, and state management of the two OpenClaw nodes (Ajna + Psyche) in the Syncrescendence constellation.
**Fused from**: corpus/openclaw/00787, 08382, 00931, 00443
**Nucleosynthesis date**: 2026-03-01 (CC64)
**Reclassification note**: These files are ABOUT Syncrescendence multi-agent infrastructure, not about OpenClaw as a product. May belong in `multi-agent-systems/` rather than `openclaw/`. Flagged for Sovereign.

---

## Architecture: Two Agents, One Platform

The AjnaPsyche Archon is a dual-agent executive brain running on OpenClaw:

| Agent | Ajna (CSO — Strategos) | Psyche (CTO — Synaptarch) |
|-------|------------------------|---------------------------|
| **Machine** | MacBook Air (user `system`) | Mac mini (user `home`) |
| **Model** | Kimi K2.5 (NVIDIA NIM) | GPT-5.3-codex (ChatGPT Plus OAuth) |
| **Role** | Strategic direction, dispatch optimization, macro awareness | System cohesion, automation, policy enforcement |
| **Communication** | `agents/ajna/inbox/` via git sync | `agents/psyche/inbox/` direct filesystem |
| **Cockpit** | NOT in cockpit (remote) | Pane 1 |

**CORRECTION (CC64)**: Source files 00787 and 08382 have machine assignments reversed (Ajna=mini, Psyche=MBA). The authoritative assignment per AGENTS.md and 00443 is Ajna=MBA, Psyche=mini. This contradiction was a live source of confusion.

**Current status (CC64)**: ANESTHETIZED. tmux constellation session offline since CC27. Agent dispatch is manual. The specifications below describe the designed state, not current operations.

---

## Outfitment Synchronization

**Goal**: Both nodes share the same capability surface (skills + plugins) while retaining role differences and keeping secrets local.

### What Syncs (outfitment)
1. OpenClaw version (keep aligned)
2. Workspace skill packs under `~/.openclaw/workspace/skills/` (e.g., supermemory ~373M, hindsight ~321M)
3. `plugins.load.paths` in config (discoverable skills)
4. Enabled/disabled plugin entries (scaffolding, not secrets)
5. LaunchAgents/watcher plists (already split by host persona)

### What NEVER Syncs
- API keys, OAuth tokens, bot secrets, gateway tokens
- `channels.*` provider credentials
- Machine-specific paths outside `~/Desktop/syncrescendence`

### Mechanism
**Canonical**: rsync via SSH allowlist.
```bash
bash orchestration/scripts/sync_openclaw_skills.sh --pull --from psyche --persona ajna
```
- Rsyncs allowlisted skill/plugin directories
- Excludes `node_modules/`, `dist/`
- Never touches `~/.openclaw/openclaw.json` or `~/.openclaw/credentials/`

**SSH trust**: Ajna→Psyche dedicated keypair (`ajna->psyche`, fingerprint `SHA256:XJeE+B/803pJG/rwsfSUm3eHxI9oSrePBVDwYbtCc64`). Psyche authorized in `/Users/system/.ssh/authorized_keys`.

**Blueprint approach** (designed, not fully implemented): Repo stores `openclaw.template.json` (no secrets) + persona overlays (`openclaw.ajna.json`, `openclaw.psyche.json`). Installer merges template + overlay + local secrets → writes `~/.openclaw/openclaw.json`.

### Receipt Piping
Dispatch script (`dispatch.sh`) supports CC: headers. Watcher copies receipts to CC target's inbox. Cross-machine delivery via `scp` (best-effort when SSH alias exists).

### Verification Checklist (post-reinstall)
1. `openclaw --version`
2. `openclaw doctor --fix --non-interactive` (ensure `~/.openclaw/credentials` exists)
3. Run sync script
4. `du -sh ~/.openclaw/workspace/skills/* | sort -h | tail`
5. `openclaw gateway status`
6. Smoke test: `openclaw agent --agent main --message "Reply EXACTLY: SYNC_OK" --timeout 180`
7. CC proof: dispatch task with CC target, confirm receipt appears in inbox

---

## Config State Mirror

OpenClaw configs live at `~/.openclaw/` (system level), violating Invariant #5 (Repo Sovereignty) unless mirrored.

**Protocol**: Config change → update system → update repo mirror → commit.

### System Paths
| Path | Purpose |
|------|---------|
| `~/.openclaw/openclaw.json` | Main config (model, channels, plugins, gateway) |
| `~/.openclaw/SOUL.md` | Agent identity and security boundaries |
| `~/.openclaw/USER.md` | User profile and preferences |
| `~/.openclaw/AGENTS.md` | Agent behavior instructions |
| `~/.openclaw/MEMORY.md` | Long-term memory store |
| `~/.openclaw/agents/main/sessions/` | Session history |
| `~/.openclaw/cron/jobs.json` | Scheduled autonomous tasks |
| `~/.openclaw/credentials/` | API keys and tokens (NEVER MIRROR) |

### Config Parity Gaps (as of Feb 2026, pre-anesthesia)
All seven gaps were identified but NOT resolved before the constellation was anesthetized:
1. SOUL.md — default state, not customized for Syncrescendence roles
2. USER.md — default template, no Sovereign profile
3. AGENTS.md — missing Syncrescendence protocols
4. MEMORY.md — empty, should mirror strategic context
5. Cron heartbeat — not configured (target: 30min cycle)
6. Repo directory awareness — missing
7. Dispatch protocol — not implemented

### Shared Infrastructure (Designed)
- **Mem0** (Apache 2.0): Auto-recall + auto-capture via Qdrant (port 6333)
- **Graphiti** (Apache 2.0): Knowledge graph via Neo4j (port 7474) + API (port 8001)
- **qmd**: BM25 local search over vault .md files
- **MCP Adapter**: Bridges filesystem and Obsidian MCP servers

---

## Known Sharp Edges

1. **Duplicate plugin ID** (`hindsight-openclaw`): exists both as workspace path and deployed extension. Need canonical load path decision.
2. **Stash hygiene**: Always-on node needs policy for handling `git stash` during auto-pulls.
3. **NVIDIA NIM free tier**: 40 RPM, ~1000 credits — constrains Ajna's autonomy.
4. **ChatGPT Plus token budget**: Constrains Psyche's daily capacity.
5. **Anthropic OAuth blocked**: Claude models unavailable to OpenClaw agents (drives Kimi/GPT model choices).

---

## Supersession Narrative

These four documents represent a single design effort in early Feb 2026 to make the dual-agent OpenClaw platform production-ready:
- 08382 was the design document (what to sync, what not to sync, proposed mechanism)
- 00787 was the implementation record (what was actually done, verification receipts)
- 00931 was the config mirror (snapshot of actual system state, gap analysis)
- 00443 was the architectural specification (roles, communication, shared infrastructure)

The effort was partially successful — skill syncing worked, SSH trust established, receipt piping proven — but config customization (SOUL/USER/AGENTS/MEMORY.md) was never completed. The constellation was anesthetized before the gaps were closed.

**Lesson**: The sync infrastructure works. The identity/config customization is the unfinished work. When the constellation reawakens, start with the config parity gaps, not the sync mechanism.

---

## Provenance

| Source | Date | Contribution |
|--------|------|-------------|
| 00443 | Feb 9, 2026 | AjnaPsyche Archon spec — roles, models, machine assignments (AUTHORITATIVE for Ajna=MBA, Psyche=mini), communication protocol, shared infrastructure, known issues |
| 00787 | Feb 5, 2026 | Implementation record — sync sequence, SSH trust, receipt piping, verification checklist, sharp edges (NOTE: machine assignments reversed vs 00443) |
| 08382 | Feb 5, 2026 | Design document — sync policy, what syncs vs doesn't, proposed mechanisms, verification requirements (NOTE: machine assignments reversed vs 00443) |
| 00931 | Feb 5, 2026 | Config mirror — system paths, Ajna config snapshot, 7 config parity gaps, action items |

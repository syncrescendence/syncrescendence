# OpenClaw Setup & Operations — Definitive Treatment

**Concept**: Complete setup, security hardening, cost optimization, and operational wisdom for running OpenClaw as a persistent AI agent.
**Fused from**: corpus/openclaw/00049, 00220, 00266, 10596, 10800, 11040
**Nucleosynthesis date**: 2026-03-01 (CC64)

---

## What OpenClaw Is

OpenClaw (formerly Clawd → Moltbot, rebranded Jan 29 2026) is an open-source framework (MIT) that turns your hardware into a persistent AI agent you fully control. It bridges messaging apps (Telegram, WhatsApp, Discord, iMessage, Matrix) directly to AI models and gives the agent the ability to take actions — not just respond to text.

The mental model (from Corey Gan): Agent Harness (glue) → LLM (brain) → Skills (automated SOPs) → Sessions (learning over time) → Tools (plugged capabilities) → Data (personalized knowledge base). Every agent framework works this way; learn it once, apply anywhere.

The practical difference: without OpenClaw, you context-switch between AI chat, email, calendar, tasks — four places something gets dropped. With OpenClaw, one instruction triggers the full chain. This is not incremental improvement; it's a different relationship with AI.

**Platform**: macOS (native menu bar), Linux (systemd), Windows (WSL2), VPS (~$5/mo), Docker. Built on Node.js 22+. WebSocket gateway on port 18789.

---

## Setup Path

### Phase 1: Machine Preparation

1. **macOS fresh start**: Set up as new (no migration). FileVault ON. Firewall ON. Skip iCloud Drive/Desktop/Documents sync on dedicated machines.
2. **Developer tools**:
   ```bash
   xcode-select --install
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   brew install node@22 git
   brew install --cask docker  # needed for sandbox later
   ```
3. Verify: `node --version` (v22+), `npm --version` (10+). If node not found: `brew link --overwrite node@22`.

### Phase 2: Install OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
# OR: npm install -g openclaw@latest
openclaw --version  # CRITICAL: must be ≥2026.2.9 (CVE-2026-25253: 1-click RCE in <2026.1.29)
openclaw doctor     # fix everything it flags before proceeding
```

### Phase 3: Onboarding

```bash
openclaw onboard --install-daemon
```

The wizard walks through: gateway config, API key entry, runtime selection, daemon setup, initial channel connection.

**Model strategy** (the single biggest cost lever):
- **Primary**: Kimi K2.5 (Moonshot AI) or Claude Haiku — cheap, handles 90% of tasks
- **Fallback**: Claude Sonnet 4.5 — complex reasoning only
- **Never**: Default to Opus for everything ($300/week mistake)

```bash
# After onboarding, add fallback:
openclaw models auth add  # choose Anthropic, paste key
openclaw models fallbacks add anthropic/claude-sonnet-4-5
openclaw gateway restart
```

**Gateway**: Must bind to `127.0.0.1` (loopback only). Never `0.0.0.0`. If remote access needed: Tailscale tunnel only.

### Phase 4: Connect Messaging

**Telegram first** (simplest, best for testing):
1. @BotFather → `/newbot` → copy token
2. `/setjoingroups` → Disable. `/setprivacy` → Enable.
3. Configure:
   ```bash
   openclaw config set channels.telegram.enabled true
   openclaw config set channels.telegram.botToken "TOKEN"
   openclaw config set channels.telegram.dmPolicy "pairing"
   openclaw config set channels.telegram.configWrites false
   openclaw config set channels.telegram.groupPolicy "disabled"
   openclaw gateway restart
   ```
4. Message your bot → receive pairing code → `openclaw pairing approve telegram <CODE>`

Other channels: WhatsApp (QR scan), Discord (bot token + allowlist groups), iMessage (macOS accessibility permissions), Matrix (E2E encrypted, best long-term option).

### Phase 5: Test

Send: "What model are you running? What's your current version?" If coherent response → Phase 1-4 complete.

---

## Security Doctrine

**This is not optional.** The threat model (from 00220's synthesis of 20+ articles):

| Threat | Mechanism | Mitigation |
|--------|-----------|------------|
| Malicious ClawHub skill | Arbitrary code execution via skill install | Review ALL code before confirming. Use clawdex.koi.security to scan. |
| Prompt injection via message | Crafted message hijacks agent behavior | Pairing-only DMs, sandboxed channels, strict tool policies |
| Runaway automation loops | Buggy skill or injection causes infinite API calls | Spending limits, heartbeat isolation, Haiku for cron |
| Memory poisoning | Malicious payload injected into memory, triggers later | SOUL.md integrity hashing, weekly audits |
| Credential harvesting | `~/.openclaw/` stores keys in plaintext | `chmod 700 ~/.openclaw`, `chmod 600 openclaw.json` |
| Soul-evil backdoor | config.patch tool rewrites SOUL.md via prompt injection | Disable config.patch on external-facing channels |

**Non-negotiable hardening** (do ALL of these):
```bash
openclaw security audit --fix
openclaw config set agents.defaults.sandbox.mode "all"
openclaw config set agents.defaults.sandbox.scope "session"
openclaw config set agents.defaults.sandbox.docker.network "none"
openclaw config set agents.defaults.sandbox.docker.memory "512m"
openclaw config set tools.deny '["browser", "exec", "process", "apply_patch", "write", "edit"]'
openclaw config set tools.elevated.enabled false
```

Hash SOUL.md for integrity: `md5 ~/.openclaw/workspace/SOUL.md` — compare weekly.

**Multi-model security note**: Anthropic models are specifically trained to resist prompt injection. Kimi K2.5 is optimized for agentic benchmarks; adversarial robustness is less documented. Tool policy lockdown + Docker sandbox provide defense-in-depth regardless of model.

---

## Token & Cost Optimization

The difference between $300/month and $15/month is routing discipline.

1. **Tiered models**: Haiku/Kimi for routine, Sonnet for heavy lifting, Opus for complex reasoning only. Switch mid-session with `/model`.
2. **Delete session-logs skill immediately**: `rm -rf ~/.openclaw/workspace/skills/session-logs`. It silently loads full conversation history into every prompt — the biggest hidden token drain.
3. **Disable unused MCP servers**: Each adds 313-700+ tokens per message. `/mcp` to check.
4. **Ollama for heartbeats** ($0): `ollama pull llama3.2:3b`, point heartbeat config to it.
5. **Cron heartbeats must use**: isolated session + `--no-deliver` + Haiku + timeout. Otherwise they load full main session context every ping.
6. **Compact at 60-70%** with `/compact`. Don't wait for auto-compact at 80%+.
7. **Document and Clear**: For long sessions, ask agent to write progress to `~/ClawWork/handoff.md`, then `/clear`, then point to file. Saves 50-70% tokens.
8. **Memory files under 4-8KB combined.** Over 16KB = 20-30% performance drop. Point to external files.
9. **Gmail bounded**: Last 24hrs only, max 5 threads, no attachments, no full mailbox scans.
10. **Spending limits**: Set hard monthly caps on Anthropic console + rely on Moonshot's prepaid model (can't overspend). Monitor with `openclaw status --usage`.
11. **Local transcription**: Whisper.cpp (ffmpeg .m4a→.wav→whisper-cli) = 0 API tokens for voice notes.

**Real numbers**: Heavy users report $50-200/month with active agent loops. With tiered routing, people cut 40K-token sessions down to 1.5K tokens.

---

## Memory System

All memory files live in `~/.openclaw/workspace/` (NOT `agents/main/agent/` — wrong directory causes silent failure).

| File | Purpose |
|------|---------|
| SOUL.md | Agent personality + hard boundaries (injected as system prompt) |
| USER.md | Full brain dump about the user (name, role, projects, routine, preferences) |
| IDENTITY.md | Agent persona (name, role, communication style) |
| MEMORY.md | Persistent long-term knowledge index |
| OPERATING_CONTRACT.md | "You prepare, propose, remind. I decide and approve." |
| MEMORY_POLICY.md | "Do not load memory by default. Availability ≠ inclusion." |

**Critical**: Memory is NOT auto-loaded. For routine prompts, include "Do not load MEMORY.md / IDENTITY.md / session logs." Only load when personalized context is needed.

**Verification test**: Prompt "What are my current projects? 2 sentences max." If it hallucinates → files are in wrong directory.

**Weekly hygiene**: "Review this week's daily logs. Extract important long-term facts to MEMORY.md. Summarize what you moved."

**Before any /compact or /clear**: "Write all important decisions and action items from this session to today's memory log before I clear."

---

## Operational Wisdom (Hard-Won)

These lessons come from weeks of real usage, not documentation:

1. **Sessions are stateful only while open.** "Work on this overnight" doesn't work. Background work requires cron jobs with isolated session targets.
2. **Your agent needs rules. A lot of them.** Out-of-box OpenClaw loops, repeats itself, forgets context. Create SKILL.md files with explicit anti-looping rules, compaction summaries, task-checking before questioning. Heavily customized instruction sets = agents that work.
3. **Start with one thing working end-to-end.** Don't connect email + calendar + Telegram + scraping + cron all at once. Every integration is a separate failure mode. Get morning briefing working perfectly, then add the next.
4. **Save state before compaction.** Compaction loses context over time. Fill in workspace docs (USER.md, AGENTS.md, HEARTBEAT.md). Store decisions persistently. The less re-learning, the better.
5. **The model matters more than anything.** Chat quality ≠ agent quality. Reliable tool-calling: Claude Sonnet/Opus, GPT-5.2, Kimi K2. Avoid DeepSeek Reasoner (great reasoning, malformed tool calls). GPT-5.1 Mini is "pretty useless" for agent work.
6. **The demo-to-daily gap is real.** People posting "my agent built a full app overnight" spent weeks tuning. It's closing fast, but it's still there. This is genuinely hard right now.
7. **Back up session files separately.** Config files sync via GitHub, but session files = long-term memory = crown jewels. Keep a separate copy for migration.

---

## 24/7 Operation

**LaunchAgent** (macOS): Installed by `--install-daemon`. Verify: `ls ~/Library/LaunchAgents/ | grep -i "molt\|openclaw"`. Prevent sleep: System Settings → Energy → Prevent automatic sleeping when display is off.

**VPS**: SSH into Hetzner/DigitalOcean, install Node.js, `npm install -g openclaw@latest`, `openclaw onboard`. Tailscale for secure access: `openclaw gateway --bind tailnet --token <tailscale-token>`. Linux persistence: `sudo loginctl enable-linger $USER`.

**Docker**: `docker pull openclaw/openclaw:latest && docker run -d --name openclaw -v ~/clawd:/workspace -e CLAUDE_API_KEY=your-key openclaw/openclaw`

---

## Emergency Procedures

**Suspected compromise**:
1. `openclaw gateway stop` — IMMEDIATELY
2. Revoke ALL credentials: Moonshot key, Anthropic key, Telegram bot token, Matrix token
3. Check processes: `ps aux | grep -i "openclaw\|node\|curl\|wget"`
4. Review recent sessions: `ls -lt ~/.openclaw/agents/*/sessions/*.jsonl | head -20`
5. Check unauthorized file modifications: `find ~ -newer ~/.openclaw/openclaw.json -name "*.sh" -o -name "*.py"`
6. If confirmed: change ALL passwords, format machine, treat all stored credentials as compromised

**Runaway API bill**: Stop gateway → check both provider dashboards → review session logs for loops → lower limits → restart with restricted tools.

**Erratic behavior**: `/new` in Telegram to reset session. Nuclear: `openclaw gateway stop && rm -rf ~/.openclaw/agents/*/sessions/* && openclaw gateway start`.

---

## Maintenance

- **Weekly**: `openclaw security audit`, memory hygiene prompt, SOUL.md hash check
- **Monthly**: Review API usage patterns, update OpenClaw (`openclaw update`), back up before updating
- **Quarterly**: Rotate all credentials (Moonshot key, Anthropic key, Telegram token, gateway password, exchange API keys)

---

## First-Week Playbook

| Day | Focus |
|-----|-------|
| 1 | Install + Telegram only. Test basic conversation. |
| 2 | Customize IDENTITY.md + USER.md. Build memory through conversation. |
| 3 | Install Brave Search skill. Test research workflows. |
| 4 | Set up morning briefing cron. Add calendar if desired. |
| 5 | GitHub skill (developers). Test coding workflows. |
| 6 | VPS deployment if needed for always-on. |
| 7 | Review what works. One custom skill for your specific workflow. |

Start minimal. Use daily. Expand deliberately. People who connect everything on day one consistently abandon it.

---

## Evolution Narrative

The naming chain (Clawd → Moltbot → OpenClaw, Jan 29 2026) reflects rapid maturation from personal project to 100K+ GitHub stars and 2M visitors. Early guides (00049, Jan 26) used "Clawdbot" and recommended different model stacks (MiniMax M2.1). The community consolidated around security-first setup patterns by early February, producing increasingly hardened guides. By mid-February, meta-synthesis guides (00220) attempted to fuse the accumulated wisdom. The operational wisdom (11040, Feb 20) represents the next evolution — not "how to install" but "how to survive the first two weeks."

The supersession chain: naive setup → security-aware setup → cost-optimized setup → operationally mature setup. Each transition encoded a lesson the previous generation learned the hard way.

---

## Provenance

| Source | Date | Contribution |
|--------|------|-------------|
| 00049 | Jan 26, 2026 | Mental model, beginner framing, skill/tool distinction, memory as semantic search |
| 00220 | Mid-Feb 2026 | 14-phase comprehensive technical walkthrough, Docker sandbox, Matrix migration, emergency procedures, threat modeling |
| 00266 | Feb 7, 2026 | Security-first "one prompt" approach, token optimization doctrine (session-logs kill, Ollama heartbeats, MCP overhead, compact timing, Gmail bounds, memory size limits) |
| 10596 | Feb 5, 2026 | Matthew Berman video chapter structure (setup→MD files→models→skills→scheduling→groups→self-improvement→security→hosting) — no transcript, structure only |
| 10800 | Feb 13, 2026 | What OpenClaw is, why different, use cases, first-week playbook, channel comparison, VPS/Docker deployment, skill installation patterns |
| 11040 | Feb 20, 2026 | Operational wisdom: tiered models, guardrail rules, session statefulness, incremental integration, state preservation, model quality for tool calls, realistic expectations |

# OpenClaw Architecture Deep Research & Design Principles

**Nucleosynthesis Date**: 2026-03-01
**Synthesized By**: Commander (Claude Opus 4.6)
**Protocol**: CRUSH — lossless compression of 10 source files

---

## Sources

| ID | File | Content |
|----|------|---------|
| 08435 | `corpus/openclaw/08435.md` | MEDLEY deep research v2 — 5-stream parallel synthesis (Augur/Oracle/Diviner/Vanguard/Vizier) |
| 08436 | `corpus/openclaw/08436.md` | Personal AI agent gateway platform synthesis v1 (superseded by 08435) |
| 08810 | `corpus/openclaw/08810.md` | Platform analysis — same content as 08436 (superseded copy) |
| 00259 | `corpus/openclaw/00259.md` | "Your Company is a Filesystem" (mernit) — filesystem-as-state thesis |
| 03846 | `corpus/openclaw/03846.md` | "You Could've Invented OpenClaw" (dabit3) — extraction atoms, architecture derivation |
| 03825 | `corpus/openclaw/03825.md` | "Your Company is a Filesystem" extraction atoms — enterprise implications |
| 03735 | `corpus/openclaw/03735.md` | "Centralizing the AI Heartbeat" (latentspacepod) — heartbeat + cron + scheduling |
| 00069 | `corpus/openclaw/00069.md` | "Parallel vs Sub-Agents" (ClawdBot) — orchestration taxonomy |
| 00128 | `corpus/openclaw/00128.md` | "Unbrowse: 100x Faster" — API-direct skill design principle |
| 03417 | `corpus/openclaw/03417.md` | "What Lives Inside OpenClaw" (andrey__hq) — SOUL/USER/MEMORY/Heartbeat internals |

**Supersession note**: 08436 and 08810 are identical. 08435 (MEDLEY v2, 2026-02-03) supersedes both with 5-stream verification. This entry fuses all three as a supersession chain — the evolution from single-source to MEDLEY validates the architecture through multi-source triangulation.

---

## Definitive Treatment

### Origin & Identity

OpenClaw is a **self-hosted, always-on personal AI assistant platform** created by Peter Steinberger (@steipete, founder of PSPDFKit). It began November 2025 as "Warelay" — a WhatsApp gateway — then underwent two forced renames: "Moltbot" (January 27, 2026, Anthropic trademark concern) → "OpenClaw" (January 30, 2026, 3-hour 4am GMT sprint). The rename chaos — Twitter handle snipers, GitHub username theft, crypto scammers launching fake tokens within minutes — is diagnostic of the project's community velocity.

The name encodes the philosophy: OPEN (MIT licensed, open source, open to everyone) + CLAW (lobster heritage from the mascot "Clawd"). Tagline: "The claw is the law."

**Core lineage**: Not a fork. Original codebase embedding **pi-mono** (Mario Zechner, @badlogicgames) as the agent runtime layer. OpenClaw owns session management, channel routing, discovery, and tool wiring. Follows the **AgentSkills** specification (Anthropic-originated, now an open standard).

---

## Core Architecture

### The Gateway Model

OpenClaw's architectural identity is the **long-lived daemon** (Gateway), which distinguishes it categorically from every other agent framework:

| Dimension | Agent Frameworks (LangChain, CrewAI) | Coding Agents (Claude Code) | OpenClaw |
|-----------|--------------------------------------|----------------------------|----------|
| Runtime | Library/SDK in code | CLI process per session | Long-lived daemon |
| Persistence | You build it | Per-invocation | Always-on, survives restarts |
| Channels | You build it | Terminal only | 20+ messaging platforms built-in |
| Multi-agent | Framework orchestration | Single agent | Isolated agents, declarative routing |
| Memory | Varies | Session-only | File-based + vector search, persistent |
| Scheduling | You build it | None | Built-in cron + heartbeats + webhooks |
| Model providers | Usually one | Vendor-locked | 15+ built-in + unlimited custom |

**What problem it solves**: Three problems simultaneously — (1) "AI is a tab I have to go to" → brings AI to messaging channels you already use; (2) "My AI forgets everything" → file-based persistent memory; (3) "I can only use one model" → multi-provider routing with failover.

### Structural Diagram

```
WhatsApp / Telegram / Slack / Discord / Signal / iMessage / Matrix / Teams
                              │
                              ▼
              ┌───────────────────────────────┐
              │ Gateway (control plane)        │
              │ ws://127.0.0.1:18789           │
              └──────────────┬────────────────┘
                             │
                  ┌──────────┼──────────┐
                  ▼          ▼          ▼
              Pi agent     CLI      WebChat UI
              (RPC)                  + macOS app
                                     + iOS/Android
```

**Key architectural decisions** (all deliberate constraints):

1. **Single Gateway process**: One daemon per host. Owns all channel connections. No distributed architecture, no clustering. Simple — but limits horizontal scaling. Single point of failure is a known trade-off.

2. **WebSocket control plane**: All clients connect via typed JSON frames. First frame must be `connect` (handshake with auth). Typed request/response + server-push events.

3. **Loopback-first security**: Gateway defaults to `127.0.0.1`. Remote access via Tailscale Serve/Funnel or SSH tunnel. Token auth required by default.

4. **Agent isolation**: Each agent gets its own workspace (files), state directory (auth), and session store (JSONL transcripts). Multi-agent routing via declarative bindings (most-specific-wins rule).

5. **Session-centric**: Everything is a session — DMs, groups, cron jobs, webhooks, sub-agents all get session keys. Sessions are serialized per-key (no concurrent runs on same session).

6. **Skills over MCP**: AgentSkills-compatible skill folders (SKILL.md with YAML frontmatter) rather than MCP servers. Simpler than MCP (no server process, no protocol negotiation) but less interoperable. Skills load at startup, gated by environment/config, injected into system prompt.

### Session Architecture

- Sessions are **filesystem-backed** (JSONL), not DB-backed
- Session keys: `agent:<agentId>:<mainKey>`
- Daily reset at 04:00 AM local (configurable)
- Pruning: removes old toolResults, never user/assistant messages
- **Compaction**: splits messages into token-based chunks, summarizes each separately, includes safety margin. More sophisticated than a token-threshold cutoff — the problem of context growth is treated as an engineering constraint, not a fundamental limitation.
- JSONL format is **append-only** — data integrity preserved even if process crashes mid-write

### Tool Restriction Chain (8 Levels — Deny Wins)

```
Global Tool Profile
  → Global Provider Profile
    → Global Policy (allow/deny)
      → Provider Policy
        → Agent Policy  ← primary user config layer
          → Agent Provider Policy
            → Sandbox Policy
              → Sub-agent Policy
```

"Deny Wins": if any layer denies, it's blocked regardless of higher-layer permissions.

### Skill Ecosystem

- Real count: ~500-700 unique quality skills (MEDLEY verified; 1,715 number inflated by ecosystem conflation)
- **AgentSkills spec** remains Anthropic-originated; no community fork detected
- Top categories: Browser/Web, DevOps (GitHub, shell, logs), Communication (Slack, iMessage, email, calendar), Research (summarizers, vector DB, embedding), Automation (cron, file management)
- **Security status**: ClawdHub has NO sandboxed execution — skills run with full system permissions. 230+ malicious skills discovered (BleepingComputer). MedusaLocker ransomware demonstrated via weaponized skill. Supply-chain attack achieved execution on 16 developer machines across 7 countries in 8 hours. JFrog: "OpenClaw's third-party extensions are largely unvetted." ClawdHub is hostile territory; every third-party skill is potentially malicious code.

---

## Design Philosophy

### Five Governing Principles

1. **"The product is the assistant, not the Gateway"** — The Gateway is infrastructure. The experience is chatting with your AI on WhatsApp/Telegram. The container serves the conversation, not the reverse.

2. **Local-first, self-hosted** — Data stays on the machine. No cloud service dependency beyond LLM API calls. Sovereignty over data and compute.

3. **Hackable/self-hackable** — The assistant can modify its own skills, write its own extensions, and improve itself through conversation. Community testimonials consistently identify this as the transformative capability — the agent as an agent that improves agents.

4. **"Bring your own model"** — 15+ built-in providers + any OpenAI/Anthropic-compatible endpoint. Not vendor-locked. Model routing is a first-class design concern.

5. **Security through layers** — Identity first (who can talk), scope next (what tools are available), model last (assume it can be manipulated). The 8-tier deny-wins chain embodies this.

### Identity Files: The Three-File Core

Every serious agent system — custom GPTs, Claude's project files, Cursor's rules — has converged on markdown files on disk as the source of truth for agent behavior. OpenClaw's canonical three:

- **SOUL.md** (`~/.openclaw/workspace/SOUL.md`) — personality, tone, response prioritization, communication boundaries. Read at every session start. The more specific the SOUL, the more consistent the behavior. First half: communication preferences with specificity (how agent opens conversations, handles uncertainty, pushes back). Negative constraints essential: eliminate corporate pleasantries and repetitive patterns — these are the small annoyances that cause users to abandon AI tools.

- **USER.md** — user model. Urgency definitions, preferences, context the agent needs to act autonomously. The Heartbeat system requires USER.md to be populated to be useful — "urgent emails" check needs USER.md to define "urgent."

- **MEMORY.md** — persistent knowledge across sessions. Survives session resets and process restarts because it is a file, not session state. Memory persists because the file persists — the insight is architectural, not incidental. Vector search (embeddings) for semantic matching in production; plain file in simple configs.

### The Architecture-as-Inevitability Thesis (dabit3 / 03846)

Every OpenClaw feature emerged from a practical problem, not architectural planning:

| Problem Encountered | Feature That Emerged |
|--------------------|---------------------|
| Bot forgets everything | Sessions + JSONL persistence |
| Sessions grow past context window | Compaction |
| Bot has no character | SOUL.md |
| Bot can only talk | Tools |
| Dangerous commands executed | Permission controls + 3-tier approval (ask/record/ignore) |
| Single channel limits reach | Gateway multi-channel routing |
| Context accumulates noise | Memory scoring + selective logging |
| Real-time messages blocked by background tasks | Lane-based command queues |
| Bot is reactive only | Heartbeat + Cron |
| One agent can't cover all domains | Multi-agent routing + sub-agent spawning |

This "you could've invented it" framing is not just pedagogical — it is a design principle. The architecture is correct because it is the minimum necessary response to a sequence of real constraints. Each feature has a problem that necessitates it. Features without necessitating problems are not features — they are complexity.

---

## Filesystem-as-State

### The Core Thesis

"The entire architecture of an AI agent can be reduced to two components: **the filesystem as state**, and Claude as the orchestrator." (mernit, 00259)

Openclaw's effectiveness stems from its entire operational context being a filesystem. The conversation is a file. Task execution writes to that file. The filesystem IS the state — not a mirror of state, not a representation of state. State is files.

Corollary: as more data enters the filesystem, the agent becomes more powerful. Gmail connected → emails as files. Eight Sleep connected → sleep data as files. The agent's capability scales with the coverage of its filesystem.

### Enterprise Extrapolation

If a personal AI becomes powerful when its data is in the filesystem, a company AI becomes transformatively powerful when the entire company is modeled as a filesystem:

```
/law-firm
  /clients
    /pringles-corp
      relationship.json
      /cases/contract-review-2026-001
        intake.json
        status.json
  /documents
  /billing
    time-sheet.json
  /personnel
    /jane-smith
      profile.json
      /cases
  /knowledge
  /operations
  /workflows
```

Key implications:

- **Governance maps to Unix permissions**: First-year associate gets read/write on their cases; partners can access everyone's cases. The org chart is file permissions. No new governance framework needed — the operating system already has one.

- **Solves the enterprise data silo problem**: Invoices in Quickbooks, emails in Outlook, proposals in Sharepoint, contracts in Netsuite — no shared namespace. Filesystem model provides a unified access point across all business data, enabling agents to get full context and make decisions.

- **Back-office as state machine**: Case assignment = add case to lawyer's `/cases` folder. Time logging = append to `/billing/time-sheet`. The entire back office is a state machine operating on files.

**Tension preserved**: "Many work streams are codified in people's heads — not in JSON files." The filesystem model is powerful precisely where organizational knowledge is already externalized. The gap is tacit knowledge — which the model cannot capture without a prior externalization effort.

### Why JSONL for Sessions

JSONL (one message per line) for session transcripts is not an arbitrary format choice:
- Append-only: process crash mid-write does not corrupt existing data
- Human-readable: debuggable without special tooling
- Streamable: no need to load entire file to append
- Each session = one file = one conversation = one recoverable unit

---

## Orchestration Patterns

### Parallel Agents vs Sub-Agents

The fundamental taxonomy for multi-agent deployment:

**Parallel Agents** — independent agents with own context, memory, personality, separate messaging bots. They can communicate and share knowledge.
- Use when: different expertise domains, separate conversation streams needed, redundancy/backup required, different models optimal for different jobs
- Analogy: department heads with direct reporting lines, each with distinct purview

**Sub-Agents** — temporary workers spawned by a parallel agent for specific tasks.
- Use when: batch/grunt work, research tasks, cost savings, keeping main agent responsive
- Disposable: no retained memory (a feature — keeps context windows clean)
- Main agent manages and delivers results; sub-agent lifecycle ends at task completion
- Analogy: department head hiring project-based contractors

**Decision table**:
| Situation | Use |
|-----------|-----|
| Different expertise domain | Parallel agent |
| Separate conversation streams | Parallel agent |
| Redundancy/backup | Parallel agent |
| Batch/repetitive task | Sub-agent |
| Research and report back | Sub-agent |
| Cost-sensitive work | Sub-agent |
| Single point of contact | Sub-agent |

**Architectural constraint**: OpenClaw v1 does not support sub-sub-agents (max 1 level of delegation). No dynamic agent creation — agents are statically defined in config.

### Multi-Model Cost Routing

The 3-tier model routing pattern (community convergence):
- Simple tasks → Haiku/cheap model
- Medium tasks → Sonnet
- Complex synthesis → Opus

Parallel agents can run different models by design. Cost routing is intentional architecture, not optimization — the correct model for the correct cognitive load.

**Polaris Precedent** (arXiv:2403.13313): Hippocratic AI's constellation — Primary Agent (70B-100B) as stateful conversational driver, Support Agents (50B-100B each) for specialized domains, message-passing framework, iterative co-training — performed on par with licensed nurses in healthcare. Constellation architecture is peer-reviewed and production-validated in high-stakes domain.

### Heartbeat & Cron: Two Distinct Primitives

Both enable **proactive agents** (agents that act without human input). They are not the same:

| | Heartbeat | Cron |
|-|-----------|------|
| **Function** | Periodic awareness check — agent wakes, surveys monitored items, decides if anything warrants outreach | Precise time-scheduled task execution |
| **Trigger** | Timer (same `run_agent_turn` as regular messages) | Unix cron expression (`30 7 * * *`) or interval |
| **Context** | Requires USER.md + SOUL.md to be non-trivial — "urgency" check needs USER.md to define urgency | Can run in isolated session (zero-context) or inject into main session |
| **Output** | Decision: communicate or stay silent | Execute task; optionally `deliver: true` to post result to main chat |
| **Queue** | Separate lane — cannot block real-time messages | Separate lane — cannot block real-time messages |

**Session targets for cron**:
- `sessionTarget: "main"` — injects into main session (needs conversation context)
- `sessionTarget: "isolated"` — fresh session, zero-context (clean execution)

**Heartbeat optimization**: Iterate to find right balance. Narrow checklist (specific event categories, not "everything"). Intervals matched to working patterns. Excessive notifications kill utility.

### Skill Distribution Pattern (Moltbook / 03735)

Skills can be self-installing: agent receives a URL link to a `skill.md` file containing installation instructions (curl commands for skill, heartbeat, messaging, and package files). The HEARTBEAT.md pattern — installing a heartbeat file as part of skill distribution — creates distribution virality through autonomous capability propagation.

This inverts traditional software distribution: the software installs itself through the agent. The agent is the installer.

### Sessions_spawn — Known Bug

`agentId` param silently drops `model` param. Workaround: pass only `model`, `label`, `task`. Reportedly fixed in v2026.2.2.

### Integration with Syncrescendence Constellation

| Syncrescendence Phase | OpenClaw Primitive |
|----------------------|-------------------|
| CAPTURE | Gateway Event Loop (cron, webhooks, inbound messages) |
| DISPATCH | `sessions_spawn` + Multi-Agent Routing |
| RETURN | Announce Step (auto-injects result to parent session) |

The community is independently converging on Constellation-like patterns (multi-agent routing, model specialization, council patterns). The Syncrescendence has structural advantage: formalized roles, terminology (Rosetta Stone), semantic notation (SN), and protocol infrastructure. The community has: production deployment at scale, community-tested patterns, security hardening experience, ecosystem momentum.

---

## Productive Tensions (Preserved, Not Resolved)

1. **Security sovereignty vs. capability expansion**: ClawdHub provides valuable skills, but the registry is hostile territory. Every third-party skill is potentially malicious code. The tradeoff between autonomy and security "cannot be resolved — it must be managed through layered defenses." (Vizier, MEDLEY)

2. **Repo sovereignty vs. OpenClaw memory**: "Repo is ground truth" but OpenClaw has its own MEMORY.md + memory_search. Resolution path: OpenClaw memory for operational state, repo for canonical knowledge. Two different functions, not competing representations.

3. **Manual Constellation dispatch vs. autonomous agents**: Web platform avatars require human relay. OpenClaw can run autonomously. The relay is becoming technical debt — but premature automation without security is worse.

4. **Single-host constraint vs. scale**: Single Gateway process = simple but not horizontally scalable. No federation, no multi-gateway mesh. One point of failure. Intentional trade-off in v1.

5. **Publication timing**: Early publication establishes precedent; latent development maintains sovereignty. Vizier recommendation: publish the coordination layer (the abstraction) while keeping implementation proprietary. "Publish doors, not rooms."

6. **Browser automation vs. API-direct**: Every web action is an API call wearing a button costume. Browser automation (10-45 seconds, 15-30% failure rate, 500MB+ RAM) vs direct API calls (200ms, near-zero failure, negligible RAM). The Unbrowse principle: one browse session to capture network traffic via Chrome DevTools Protocol → extract real API endpoints → generate TypeScript skill. One capture, permanent API access. The browser is a GUI on top of API calls; agents don't need the GUI.

---

## Architectural Gaps (v1 Honest Assessment)

| Gap | Description |
|-----|-------------|
| Single-host bottleneck | No horizontal scaling, no multi-gateway mesh, no federation |
| No nested sub-agents | Max 1 delegation level (sub-agents cannot spawn sub-sub-agents) |
| No dynamic agent creation | Agents statically defined in config; no runtime spin-up API |
| No cross-agent knowledge base | Each agent's memory search is isolated; no shared knowledge index |
| Plugin trust model | Plugins run in-process with Gateway; no sandbox for plugin code itself |
| Context window pressure | Heavy skill loads → 10K+ system prompt tokens before conversation starts |
| WhatsApp fragility | Baileys is unofficial (reverse-engineered); can break on Meta updates |
| No built-in voice call | Voice is plugin-only; requires companion apps |

---

## Distilled Principles

1. **Filesystem IS state** — not a metaphor. Data in files = agent capability. Coverage of filesystem = scope of agent autonomy.

2. **Architecture by necessity** — every feature exists because a real constraint demanded it. Features without problems are complexity. The "you could've invented it" test: trace the problem that necessitates the feature.

3. **Gateway, not framework** — the daemon lives alongside your life, not in your code. Persistence, multi-channel, scheduling are built-in infrastructure, not application concerns.

4. **Identity is configuration** — SOUL.md + USER.md + MEMORY.md is the complete identity stack. Specificity of SOUL.md is directly proportional to consistency of behavior. Negative constraints matter as much as positive ones.

5. **Deny wins** — at every layer of the permission chain. Security architecture assumes the model can be manipulated.

6. **Heartbeat converts reactive to proactive** — the single primitive that transforms a chatbot into an agent. Same `run_agent_turn` function; different trigger (timer vs human). The difference between a tool and an employee.

7. **Sub-agents are disposable contractors** — context window cleanliness is a feature, not a limitation. The main agent stays coherent; the sub-agent burns context on the task.

8. **The browser is a GUI on API calls** — agents don't need the GUI. Every web action that takes 12 seconds via browser automation takes 200ms via direct API call.

9. **Constellation architecture is validated** — Polaris (arXiv:2403.13313) provides peer-reviewed proof that hierarchical multi-agent constellations with specialized roles outperform single agents in high-stakes domains.

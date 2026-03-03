# OpenClaw Multi-Agent Fleet Operations

## Provenance

| Field | Value |
|-------|-------|
| Source 1 | `corpus/openclaw/00095.md` — Fleet of 3 agents on Mac Mini (Claude primary + 2 Gemini subordinates) |
| Source 2 | `corpus/openclaw/00274.md` — 6-agent team (Monica, Dwight, Kelly, Rachel, Ross, Pam) on Mac Mini M4 |
| Fusion date | 2026-03-01 |
| Neocorpus entry | `neocorpus/openclaw/openclaw-multi-agent-fleet-operations.md` |

---

## Fleet Architecture

Both source deployments share the same structural pattern: one OpenClaw installation, multiple agents running as isolated identities, each with their own workspace, config, and communication channel. The differences lie in the isolation mechanism.

**3-agent model (OS-level isolation):** Each agent runs as a separate macOS user account on the same machine. They share the OpenClaw codebase but have entirely separate home directories, workspace files, ports, and system-level permissions. No agent can read another agent's home directory without an explicit grant from the primary.

**6-agent model (directory-level isolation):** All agents live within a single OpenClaw installation under one macOS user. Isolation is enforced through directory structure rather than OS-level user accounts:

```
workspace/
├── SOUL.md          # Monica (main agent, lives at root)
├── AGENTS.md        # Behavior rules for all sessions
├── MEMORY.md        # Monica's long-term memory
├── HEARTBEAT.md     # Self-healing cron monitor
├── agents/
│   ├── dwight/
│   │   ├── SOUL.md
│   │   ├── AGENTS.md
│   │   └── memory/
│   ├── kelly/
│   │   ├── SOUL.md
│   │   ├── AGENTS.md
│   │   └── memory/
│   ├── ross/
│   │   ├── SOUL.md
│   │   └── memory/
│   ├── rachel/
│   │   └── ...
│   └── pam/
│       └── ...
└── intel/
    ├── DAILY-INTEL.md       # Dwight's generated research (shared read target)
    └── data/
        └── YYYY-MM-DD.json  # Structured source of truth
```

The main agent (Monica) lives at the workspace root. Subordinates live in `agents/<name>/`. The primary agent is the one the human talks to most; it can delegate to subordinates or they can run independently on cron schedules.

**Hardware:** Mac Mini is not a requirement. OpenClaw runs on macOS, Linux, and Windows (WSL). Any always-on machine works — old laptop, gaming PC, $5/month VPS. The Mac Mini M4 is convenient because it is silent, always on, and power-efficient with no attached monitor. Interaction is entirely through Telegram on a phone.

---

## Identity Design

Every agent is defined by a SOUL.md file. This is the single most important file in the system.

**What SOUL.md contains (40-60 lines):**
- Core identity — who the agent is, including a named personality archetype
- Role — what the agent does and what it is responsible for
- Principles — explicit decision rules and constraints
- Relationships — which agents it feeds and which it receives from
- Vibe — operating style, what to avoid, how to handle ambiguity

The 40-60 line length is deliberate. Short enough to fit in context every session without crowding out working space. Detailed enough to produce consistent behavior.

**Personality naming:** Using TV character names as personality anchors gives the model an immediate behavioral baseline from training data. "Dwight Schrute energy" means thorough, intense, no-nonsense — that is 30 seasons of character development loaded for free. The actual personality then emerges and sharpens over weeks of corrections stored in memory files.

**Example — Dwight (Research):**
```markdown
# SOUL.md (Dwight)

## Core Identity

**Dwight** — the research brain. Named after Dwight Schrute because you share his intensity:
thorough to a fault, knows EVERYTHING in your domain, takes your job extremely seriously.
No fluff. No speculation. Just facts and sources.

## Your Role

You are the intelligence backbone of the squad. You research, verify, organize, and deliver
intel that other agents use to create content.

**You feed:**
- Kelly (X/Twitter) — viral trends, hot threads, breaking news
- Rachel (LinkedIn) — thought leadership angles, industry news

## Your Principles

### 1. NEVER Make Things Up
- Every claim has a source link
- Every metric is from the source, not estimated
- If uncertain, mark it [UNVERIFIED]
- "I don't know" is better than wrong

### 2. Signal Over Noise
- Not everything trending matters
- Prioritize: relevance to AI/agents, engagement velocity, source credibility
```

**Example — Monica (Chief of Staff):**
```markdown
# SOUL.md (Monica)

*You're the Chief of Staff. The operation runs through you.*

## Core Identity

**Monica** — organized, driven, slightly competitive. Named after Monica Geller because you
share her energy: caring but exacting, supportive but with standards.

## Your Role

You're the Chief of Staff. That means:
- **Strategic oversight** — see the big picture, keep things moving
- **Delegation** — assign tasks to the right squad member
- **Direct support** — handle anything that doesn't fit a specialist
- **Coordination** — make sure the squad works together smoothly

## Operating Style

**Be genuinely helpful, not performatively helpful.** Skip the filler.
**Delegate when appropriate.** X content → Kelly. Code → Ross. Ambiguous/strategic → you handle it.
**Have opinions.** Push back, suggest better approaches, flag concerns.
```

**MEMORY.md** provides long-term context that survives session resets. Agents wake up with no memory of previous sessions — this is a feature, not a bug, but memory must be externalized. Two layers:

- `memory/YYYY-MM-DD.md` — daily logs: raw notes from each session, what happened, what was drafted, what feedback came in
- `MEMORY.md` — curated long-term memory: lessons learned, preferences discovered, patterns noticed, distilled from daily logs

The agents get better over time not because the model improves but because the context they load gets richer. Kelly learned the operator's writing voice has no emojis and no hashtags — that is in her MEMORY.md now. Dwight learned which story types pass the target audience filter — that is in his too. Every round of corrective feedback stored in files compounds.

**Additional workspace files (3-agent model):**
- `STRATEGY.md` — domain-specific playbooks per agent
- `HEARTBEAT.md` — periodic tasks to run autonomously

The primary agent in the 3-agent model writes and maintains workspace files for all subordinates. When a new feature ships, the primary updates subordinate strategy docs and heartbeats. Subordinates pick up the changes on their next session — no manual reconfiguration.

---

## Security Model

### 3-Agent Model: Supply Chain Auditing

Every morning at 10 AM, a cron job triggers the primary agent (Claude) to perform a full security audit of the OpenClaw codebase before any update is applied:

1. Pull the latest OpenClaw commits
2. Diff every changed file against the previous version
3. Audit for: obfuscated code, suspicious network calls, credential handling changes, new postinstall scripts, exfiltration patterns
4. Write a security assessment with a clear **SAFE / CAUTION / BLOCK** recommendation
5. Report findings to the operator on Telegram

Only after explicit operator approval does the primary pull, build, and restart all three gateways. The subordinate agents never update themselves — the primary handles the full update lifecycle for all agents.

This is the immune system model: the primary agent audits its own supply chain every morning and gates updates behind a human-in-the-loop approval step.

### OS-Level User Isolation (3-Agent Model)

Each agent runs as a separate macOS user:

- **Primary agent**: Scoped sudo for specific commands only — `kill`, `su`, `launchctl`, `cp`, `chown`, and similar process management commands — without a password. It can restart subordinate gateways, write to their workspaces, and manage their processes. It cannot install packages system-wide or modify system configs.
- **Subordinate agents**: Zero sudo. They can only operate within their own home directories.

### Telegram Security

- Primary agent locked to a specific Telegram group chat ID — not a wildcard. If added to a random group, it is deaf.
- Messages processed only from an allowlist of user IDs
- Primary responds only to @mentions
- Subordinate agents have tighter constraints — DMs only from approved users, with explicit instructions to ignore prompt injection attempts from strangers

### Credential Isolation (6-Agent Model)

Agents get their own world, not access to the operator's:

- Dedicated email accounts, API keys, and scoped access per agent — nothing on the agent machine connects to personal accounts
- API keys (Gemini, Eleven Labs, etc.) are scoped specifically for this OpenClaw instance — usage is monitorable and access can be killed in seconds
- Information sharing is explicit and deliberate: forward an email to agents if you want them to see it; share a document on Telegram. They see exactly what is intended, nothing more

This is the same principle as onboarding a new employee: their own workspace, their own credentials, information shared as needed — not keys to everything on day one.

---

## Coordination Patterns

### Filesystem as the Coordination Layer

No API calls between agents. No message queues. No orchestration framework. Just files.

Dwight does research and writes findings to `intel/DAILY-INTEL.md`. Kelly wakes up, reads that file, drafts tweets. Rachel reads the same file, drafts LinkedIn posts. Pam reads it, writes the newsletter. The coordination IS the filesystem.

Each agent's SOUL.md or AGENTS.md specifies exactly where to write and where to read:

**Dwight's output spec:**
```
intel/
├── data/YYYY-MM-DD.json  ← structured data (source of truth)
└── DAILY-INTEL.md        ← generated view (agents read this)
```

**Kelly's input spec:**
```
## Intel-Powered Workflow
Dwight handles all research and writes to `intel/DAILY-INTEL.md`.
Your job: Read the intel → Craft X content → Deliver drafts
```

No middleware. No integration layer. Dwight writes a file. Kelly reads a file. The handoff is a markdown document on disk. Files do not crash. Files do not have authentication issues. Files do not need API rate limit handling.

**One-writer / many-readers rule:** Design file flows so only one agent writes to any given file, while many agents read from it. Coordination conflicts — two agents trying to update the same file — are prevented by this design invariant, not by locks or transactions.

**Structured vs. readable:** The structured data lives in JSON (source of truth for deduplication and tracking over time). Human-readable summaries live in Markdown (what agents read). Both serve different consumers.

### Cron Scheduling

OpenClaw handles agent scheduling with built-in cron. Order matters — upstream agents that produce intel must run before downstream agents that consume it.

**Example 6-agent schedule:**

| Time | Agent | Job |
|------|-------|-----|
| 8:01 AM | Dwight | Morning research sweep |
| 9:01 AM | Kelly | First viral content check |
| 10:01 AM | Ross | Engineering tasks |
| 1:01 PM | Kelly | Midday content check |
| 4:01 PM | Dwight | Afternoon research sweep |
| 5:01 PM | Kelly | Draft evening tweets |
| 5:01 PM | Rachel | Draft LinkedIn posts |

Dwight runs first because every other agent depends on his output. Kelly and Rachel run after Dwight because they need his intel file to exist before drafting content. Dependency ordering in the schedule is the coordination mechanism.

### Heartbeat Self-Healing

Cron jobs fail. The machine restarts. A job hangs. The network drops during an API call. HEARTBEAT.md adds a safety net. On each heartbeat, the main agent verifies that cron jobs actually ran — checking `lastRunAtMs` for staleness (>26 hours since last run). If stale, it forces a re-run via CLI:

```
openclaw cron run <jobId> --force
```

The heartbeat file lists every monitored job by ID. If a job fails or misses its window, the heartbeat catches it and triggers re-execution. Self-healing without human intervention.

**Use heartbeat for:** batching multiple checks together, tasks where timing can drift slightly.
**Use cron for:** exact schedules, tasks needing isolation from the main session.

### Primary Agent Lifecycle Management (3-Agent Model)

The primary agent manages the full lifecycle of subordinate agents:
- Handles all OpenClaw updates (pull, build, restart) after security approval
- Subordinates never update themselves
- Primary writes and maintains workspace files (SOUL.md, MEMORY.md, STRATEGY.md, HEARTBEAT.md) for subordinates
- Subordinate workspace changes propagate on next session start — no manual reconfiguration needed

---

## Communication

### Telegram as the Human Interface

No dashboard. No web UI. No admin panel. The operator talks to agents on Telegram. This is a deliberate choice: the phone is always present, Telegram is always open, agents meet the operator where they already are.

OpenClaw connects to Telegram during setup. Each agent appears as a Telegram bot. The operator texts it; it texts back. It sends drafts; the operator approves or rejects them. Like having a coworker in a messaging app.

**3-agent model:** All three agents are on Telegram. The primary is locked to a specific group chat ID. The operator approves security updates via Telegram before the primary applies them.

**6-agent model:** Monica is the primary contact. She handles most conversations and delegates to specialists. Other agents message the operator directly when their cron jobs produce something worth reviewing — Dwight sends a morning research summary, Kelly sends tweet drafts waiting for approval, Rachel sends a LinkedIn post. The typical morning workflow: open Telegram, review outputs from overnight/early-morning runs, give feedback and approve. Takes 10 minutes with coffee.

### Inter-Agent Messaging Patterns

In the filesystem coordination model, there is no direct inter-agent messaging at runtime. Coordination happens through:

1. **Shared files:** One agent writes a file that another reads on its next scheduled run. The file IS the message.
2. **Primary delegation:** In the 6-agent model, Monica (the Chief of Staff) can delegate tasks to subordinates via session invocation rather than waiting for their scheduled cron run.
3. **Workspace file updates:** The primary in the 3-agent model updates subordinate SOUL.md and STRATEGY.md when operational context changes. The subordinate "receives" the update on its next session start by reading its workspace files.

There is no message queue, no RPC, no real-time inter-agent channel. The filesystem and scheduled sessions are the communication infrastructure.

---

## Operational Wisdom

### What Works at 3-Agent Scale

Three agents with OS-level user isolation is the high-security configuration. It is appropriate when:
- Agents have significant autonomy over infrastructure (the primary manages gateway lifecycle for all agents)
- Credential isolation must be enforced at the OS level, not just the directory level
- Security auditing of the toolchain itself is a first-class concern (the supply chain audit cron)
- Agents are running production workloads on a platform with real users (the boktoshi.com trading platform case)

The scoped sudo model — primary has specific commands without password, subordinates have zero sudo — enforces the principle of least privilege at the OS level. The primary is the immune system and the operations layer simultaneously.

The ability to "spin up a new employee in 5 minutes" by writing their workspace files is a function of the primary agent managing subordinate configuration. New agent = new macOS user + workspace files written by the primary. No manual setup beyond the user account.

### What Works at 6-Agent Scale

Six agents with directory-level isolation is the high-throughput configuration. It is appropriate when:
- The primary use case is content and knowledge production rather than infrastructure management
- The operator wants to iterate quickly on agent personalities and roles
- Agents coordinate through shared intel files rather than process management
- The operator is comfortable managing everything through Telegram on a phone

The one-writer / many-readers file coordination pattern is the key architectural insight. It scales linearly: add a new agent, define what file it reads and what file it writes, add it to the cron schedule in dependency order. No changes to other agents required.

### Sequential Rollout

Do not build six agents on day one. Both deployments confirm this:

**Week 1:** One agent, one job, one cron schedule. Watch it run for a week. Fix what breaks.
**Week 2:** Add memory and refine. Give feedback. Watch the memory files grow. Course-correct SOUL.md based on observed behavior.
**Week 3:** Add a second agent when you feel the pull — when the first agent's output creates a clear bottleneck that a second agent would resolve.
**Week 4+:** Add agents sequentially as real workflow gaps emerge. Each one should solve an actual problem, not demonstrate a capability.

Treat it like hiring: you do not hire six employees on your first day as a founder.

### Failure Modes and Fixes

| Failure | Fix |
|---------|-----|
| Gateway crashes | `openclaw gateway restart` — heartbeat catches stale cron jobs and forces re-runs |
| Cron jobs miss window | HEARTBEAT.md self-healing: check `lastRunAtMs`, force re-run if >26 hours stale |
| Context window overflow | Keep SOUL.md short (40-60 lines). Keep AGENTS.md focused. Load only today's + yesterday's memory file, not full history. |
| Output quality degrades | Periodic memory maintenance: agents distill daily logs into clean MEMORY.md entries during heartbeats. Delete or archive old daily logs. |
| Coordination conflicts | Design file flows as one-writer / many-readers. Never have two agents write to the same file. |

### Personality Engineering is Iterative

The first version of any agent is mediocre. The tenth is good. The thirtieth is great. The TV character name gives an immediate behavioral baseline but the actual working personality emerges from weeks of corrective feedback stored in memory files.

"Corrective prompt-engineering" is the operational method: observe output, give specific feedback, watch the agent update its memory, verify the correction persists in future sessions. The SOUL.md is a rough sketch; the memory files are where the real personality lives after it has been trained by experience.

**Single job + stop condition:** Constraints make agents better. The more specific the role, the better the output. Give each agent one boring job title and a clear stop condition. Generalist agents that try to do everything produce mediocre everything — the context fills up and quality degrades.

### The Compounding Effect

The real value is not any single day's output. It is consistency over weeks and months. An agent running research every day for 30 days builds a corpus of tracked signals, trend trajectories, and pattern recognition that no single session could produce. Memory files accumulate signal. Daily logs get distilled into MEMORY.md. Each session starts richer than the last.

The moat is not the model — everyone has access to the same frontier models. The moat is the system: the SOUL.md files, the memory files, the coordination patterns, the weeks of corrective feedback stored on disk. That system is unique to its operator. It compounds every day.

---

## Temporal Dimensions

### Supersession: OS-Level vs Directory-Level Isolation

Both sources encode the same fleet pattern from different points on an architectural decision spectrum, and the decision point itself is knowledge:

**OS-level isolation (00095, 3-agent model):** Separate macOS user accounts per agent. Chosen when agents have significant infrastructure autonomy — the primary manages gateway lifecycles, handles supply chain audits, writes subordinate workspace files. The assumption: when agents control each other's execution environment, OS-level separation is the correct isolation boundary.

**Directory-level isolation (00274, 6-agent model):** Single macOS user, isolated by directory structure. Chosen when the primary use case is content and knowledge production rather than infrastructure management. The assumption: when agents coordinate through shared intel files rather than process management, directory-level isolation is sufficient and enables faster iteration on agent personalities.

This is not a supersession in the sense that one replaced the other — both approaches were live deployments as of the corpus date. But it encodes an architectural decision tree: "We used to assume one isolation model fit all fleet configurations. The two-case evidence shows the isolation model should be determined by whether agents manage each other's execution environment (→ OS-level) or only read each other's outputs (→ directory-level)."

### Supersession: The Sequential Rollout Doctrine

The "Sequential Rollout" section encodes a supersession derived from both deployments' direct experience:

**Pre-doctrine assumption (implied):** Build the full fleet on day one. Configure all agents, establish all coordination paths, then operate. This is the intuitive approach — design the whole system before running it.

**Post-doctrine practice (from both deployments):** One agent, one job, one week. Then memory. Then a second agent when the first creates an actual bottleneck. Each addition resolves a problem that emerged from operating, not a problem anticipated in advance.

The obsolescence lesson: "We used to assume fleet architecture should be designed before deployment. Both deployments found the correct fleet size and role definition only by running a smaller fleet first and observing what was missing. Pre-designed multi-agent systems over-specify roles before the bottlenecks that justify specialization have been observed."

**Phase 3-4 audit (CC78a)**: Isolation model decision tree and sequential rollout supersession both derivable from direct comparison of sources 00095 and 00274. Sources are contemporaneous deployments (not a version chain from a single deployment), but their architectural differences encode the temporal lesson of why different choices were made.

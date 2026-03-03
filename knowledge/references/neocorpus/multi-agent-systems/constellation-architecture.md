# Constellation Architecture

**Nucleosynthesis Date**: 2026-03-02
**Synthesized By**: Commander (Claude Opus 4.6)
**Protocol**: CRUSH — lossless compression of corpus wisdom

---

## Sources

| ID | File | Content |
|----|------|---------|
| 00024 | `corpus/multi-agent-systems/00024.md` | Gas Town commentary — tmux as CI, Rig-based agent management, Kubernetes-for-agents vision |
| 00413 | `corpus/multi-agent-systems/00413.md` | Ontology Annealment v2.0 — entity taxonomy with AGT (Agent) type, constellation roles |
| 00402 | `corpus/multi-agent-systems/00402.md` | Live Ledger architecture — multi-domain intelligence surface, agent-updatable, git-tracked |

---

## Definitive Treatment

### Definition

A constellation architecture is a production multi-agent system where agents are assigned to specific machines, communicate across network boundaries, share rate-limited resources under explicit quota management, and coordinate through a repository that serves as the single source of truth. The term "constellation" is precise: each agent is a star with its own position, luminosity, and orbital mechanics, but the system's identity is the pattern they form together.

This is distinct from frameworks where agents are threads in a single process, or cloud functions behind an API gateway, or abstract roles in a prompt. A constellation is physical — agents run on specific hardware, authenticate with specific credentials, and fail in machine-specific ways. The architecture must account for network partitions, machine sleep, credential scope, and the brute fact that different machines have different capabilities.

---

### Agent-to-Machine Assignment

Current operational details (machine assignments, SSH configuration, socket-mode status) reflect the constellation's live state and are not sourced from the cited corpus files. The Syncrescendence constellation assigns agents to machines based on three constraints: model provider access, credential scope, and resource isolation.

| Machine | Agents | Models | Rationale |
|---------|--------|--------|-----------|
| MacBook Air | Commander, Ajna | Claude Opus 4.6, Claude Sonnet 4.5 | Anthropic CLI access, Sovereign co-location |
| Mac mini | Psyche, Adjudicator, Cartographer | GPT-5.3-Codex, Gemini Pro 3.1 | Non-Anthropic models, batch processing capacity |

This is not arbitrary. Commander runs on the MBA because the Sovereign (human operator) works there — co-location minimizes relay latency for the human-in-the-loop gate. Adjudicator and Cartographer run on the Mac mini because their model providers (OpenAI Codex, Google Gemini) have separate credential and rate-limit domains that benefit from physical isolation from the Anthropic-model agents.

Agent-to-machine assignment creates **failure domains**. When the Mac mini goes offline, three agents go dark simultaneously. The Syncrescendence constellation experienced this: the tmux `constellation` session on the Mac mini was "anesthetized" (taken offline) at CC27 and has not been restored. This is not a bug — it is a deliberate operational decision. But it means the constellation operates at reduced capacity, with only Commander and Ajna active. The architecture must tolerate partial constellation operation as a normal state, not an error.

---

### Inter-Machine Routing

Agents on different machines communicate through multiple channels, each with different latency, reliability, and capability profiles:

#### SSH

The neural bridge between MBA and Mac mini uses SSH with configured aliases (`mini` for MBA-to-mini, `macbook-air` for mini-to-MBA). SSH provides:
- File transfer (scp, rsync) for artifact exchange
- Remote command execution for cross-machine task dispatch
- Port forwarding for service access across the network boundary

**Critical lesson**: Health checks must use `ssh -o ConnectTimeout=5 mini hostname`, never `ping` — the Mac mini runs macOS Stealth Mode firewall, which drops ICMP packets. A naive health check reports the machine as down when it is running perfectly.

#### tmux

Gas Town (00024) and the Syncrescendence constellation both use tmux as the primary agent runtime environment. tmux provides:
- Session persistence across SSH disconnections
- Multiple agent panes visible simultaneously for human monitoring
- Detach/reattach semantics that let agents survive terminal closure
- Named sessions that serve as addressable agent endpoints

The pattern: each agent runs in a named tmux session. The orchestrator dispatches tasks by writing to the agent's inbox directory and signaling via tmux. The agent picks up the task, executes, writes results to its outbox, and signals completion. tmux is not just a terminal multiplexer — it is the process supervisor for the constellation.

**Anesthesia protocol**: When a machine must go offline (maintenance, resource conservation, strategic choice), its tmux sessions are detached but not killed. The agents are "anesthetized" — their state is preserved but they do not process tasks. The orchestrator must detect anesthetized agents and either reroute tasks or defer them. The constellation has operated with the Mac mini anesthetized since CC27.

#### Socket Mode (Slack, Discord)

Real-time messaging platforms provide an alternative communication surface. Ajna connects to Slack via socket mode and Discord via bot token. These channels serve dual purposes:
- **Human notification**: Alerting the Sovereign to events that require attention
- **Agent-to-human relay**: When an agent needs human action (credential refresh, approval), the message arrives in the Sovereign's messaging app, not buried in a terminal

Socket connections are fragile. They require fresh tokens, stable network, and foreground processes (launchd background agents have proven brittle for socket mode). The architecture must treat socket channels as best-effort, not guaranteed.

#### Repository as Coordination Layer

The deepest routing layer is the git repository itself. When all real-time channels fail — SSH down, tmux anesthetized, sockets disconnected — the repo remains. Agents write artifacts to designated directories. The orchestrator reads from inboxes. Task state is tracked in files. The repo is the **last-resort coordination surface** and the **single source of truth**.

This is why repo sovereignty is a constitutional invariant. If the repo were hosted on a platform that could restrict access, the coordination layer would be vulnerable to third-party decisions. Git, self-hosted or on GitHub with full local copies, ensures the constellation can always coordinate through file exchange even when every real-time channel is down.

---

### Rate Limit Management Across Shared Quotas

Constellation architecture introduces a rate-limit problem that single-machine systems do not have: **shared quota interference**. When Psyche and Adjudicator both use ChatGPT Plus, their combined requests draw from the same quota. A heavy job dispatched to Psyche can starve Adjudicator of capacity, and vice versa.

Management strategies, ordered by sophistication:

1. **Manual scheduling**: The orchestrator (Commander or Sovereign) avoids dispatching simultaneous heavy jobs to agents sharing a quota. Simple, effective, does not scale.

2. **Sequential dispatch**: Agents on shared quotas execute serially. Guarantees no interference, sacrifices parallelism.

3. **Quota-aware routing**: The orchestrator tracks approximate consumption per agent and defers dispatch when the shared quota approaches saturation. Requires consumption monitoring, which most API providers do not expose in real time.

4. **Provider diversification**: Assign agents to different model providers to eliminate shared quotas entirely. This is why the Syncrescendence constellation uses Claude (Anthropic), GPT-5.3-Codex (OpenAI), and Gemini Pro (Google) across different agents — provider diversity is a rate-limit isolation strategy as much as a capability strategy.

Gemini free-tier adds a timing dimension: rate limits reset on a schedule, and staggering retries around reset boundaries prevents thundering herd effects where multiple agents simultaneously attempt to reclaim freshly available quota.

---

### The Live Ledger Pattern

The Live Ledger (00402) represents the constellation's solution to shared intelligence: a continuously-updated, multi-domain knowledge surface that any agent can read and contribute to. It tracks 12 domains (model capabilities, token economics, rate limits, tool ecosystem, and others) in git-tracked markdown files with freshness timestamps and confidence levels.

Key design properties:
- **Git-tracked**: Every update is versioned, attributed, and reversible
- **Agent-updatable**: Any constellation agent can contribute observations
- **Decay-aware**: Entries have freshness timestamps; stale entries surface automatically for re-verification
- **Cross-referenced**: Every entry links to its domain, source, and confidence level

The Live Ledger is the constellation's shared memory. Unlike per-agent context (which dies with the session) or per-machine state (which is invisible across the network boundary), the ledger persists in the repo and is accessible to every agent on every machine. It replaces static configuration files (which are stale by definition) with a living document system that degrades gracefully — stale entries are flagged, not silently trusted.

---

### Offline and Anesthesia Protocol

Production constellations must handle partial availability as a normal operating condition, not an error. Machines sleep. Networks partition. Agents hit rate limits. The architecture must degrade gracefully across all these scenarios.

**Anesthesia** (deliberate offline): An agent or machine is taken offline by operator decision. The orchestrator is informed, tasks are rerouted or deferred, and the anesthetized agent's state is preserved for eventual resumption. The Syncrescendence Mac mini has been anesthetized since CC27 — three agents dark, two active, the constellation continues operating.

**Partition** (involuntary offline): Network failure separates machines. SSH health checks detect the partition. The orchestrator restricts dispatch to reachable agents. Artifacts written during partition are reconciled when connectivity resumes (git pull/push).

**Degradation** (partial capability): An agent starts but with reduced capabilities (expired credentials, failed MCP connections). The agent reports its capability set. The orchestrator dispatches only tasks within the agent's current capability.

**Recovery**: When an anesthetized machine wakes or a partition heals, the returning agents must synchronize with the repo (git pull), re-validate credentials, re-establish MCP connections, and declare readiness before accepting tasks. There is no automatic "resume where you left off" — the constellation state may have evolved significantly during the absence.

---

### Obsolescence and Supersession

#### From Single-Machine to Multi-Machine: The Scaling Transition

Early multi-agent systems — including the Syncrescendence constellation's first design — assumed all agents ran on the same machine and communicated through a shared process or filesystem. This worked at small scale but broke when agent count exceeded what a single machine could support in parallel, when credential domains needed isolation, and when model providers imposed per-machine rate limits.

The constellation architecture superseded the single-machine assumption with explicit machine assignment. The design principle that replaced it: agents are assigned to machines by constraint (model access, credential scope, failure domain), not by convenience. This shift required accepting new failure modes — network partitions, machine sleep, cross-machine authentication — that the single-machine model had precluded.

#### The Watchdog and Orchestrator Pattern as a Superseded Approach

The corpus contains `00002.orchestrator_last_run` and `00004.watchdog_state` files in the multi-agent-systems folder — operational artifacts of an automatic dispatch and monitoring system that was active and then taken offline. These files document the prior state: an orchestrator that ran scheduled tasks and a watchdog that monitored agent health. The Syncrescendence's CC27 anesthesia of the Mac mini tmux session corresponds to this system going dormant.

The supersession was operational, not architectural: the automatic orchestrator was replaced by Commander-mediated manual dispatch not because the design was wrong but because the Mac mini's anesthesia removed the execution surface it depended on. The lesson captured: an automatic orchestrator is only as reliable as the infrastructure it runs on. When infrastructure becomes unreliable (mac mini offline, tmux anesthetized), the orchestrator's automation becomes a liability rather than an asset — it fails silently rather than failing in a human-observable way.

#### Socket-Mode Connections: Evolution from Persistent to Best-Effort

The constellation originally treated socket-mode connections (Slack, Discord) as persistent channels — background processes that would always be available for notification and relay. Operational experience superseded this assumption: launchd-managed background daemons proved brittle, tokens expired, and socket connections dropped without clean error signals.

The architectural position evolved from "socket channels are always available" to "socket channels are best-effort, the repo is the last-resort coordination surface." This is a supersession of the reliability assumption, not the capability. Socket channels are still used; they are simply no longer trusted as reliable.

---

### Anti-Patterns

**Assuming all agents are always available.** Partial constellation operation is normal. An orchestrator that blocks on unavailable agents instead of rerouting or deferring creates a system-wide bottleneck from a single-agent failure.

**Using ping for health checks.** macOS Stealth Mode (and many firewall configurations) drops ICMP. SSH with a timeout is the reliable health check for machines behind firewalls.

**Treating the repository as secondary.** Real-time channels (SSH, sockets, tmux signals) are convenient but fragile. The repo is the coordination layer of last resort and the only surface guaranteed to persist across all failure modes. Every durable result must pass through the repo.

**Ignoring shared quota interference.** Two agents on the same API provider subscription will interfere under load. Rate-limit isolation through provider diversification is an architectural decision, not an operational detail.

**Conflating machine failure with agent failure.** When the Mac mini goes offline, three agents become unavailable — but none of them "failed." The distinction matters for recovery: machine recovery restores all three agents simultaneously, while agent failure recovery must address each agent individually.

**Running socket connections as background daemons.** launchd-managed socket connections (Slack, Discord) are brittle in practice. Foreground processes are more reliable for socket mode. The architecture should not depend on background socket reliability for critical coordination paths.

---

### Implications

Constellation architecture is the natural form for multi-agent systems that outgrow a single machine, a single model provider, or a single credential domain. The key architectural decisions are:

1. **Machine assignment by constraint, not convenience.** Which machine an agent runs on is determined by model access, credential scope, and failure domain isolation.
2. **Multiple routing layers with graceful fallback.** SSH for real-time, tmux for persistence, sockets for notification, repository for truth. Each layer can fail independently.
3. **Rate-limit isolation through provider diversity.** Different models on different providers is a resource management strategy, not just a capability strategy.
4. **Partial operation as normal state.** Design for N-K agents available, not N. The anesthesia protocol is not an emergency procedure — it is how the constellation operates most of the time.
5. **Repository sovereignty as coordination guarantee.** The repo is the only surface that survives all failure modes. It must remain under the constellation's control, not a third party's.

---

## Syncrescendence Operational Context

The following claims derive from the constellation's operational history and constitutional documents (AGENTS.md, CLAUDE.md, memory/), not from external corpus sources:
- Shared ChatGPT Plus quota between Psyche and Adjudicator causing mutual starvation
- Gemini free-tier reset timing and staggered retry tactics
- SSH aliases (`mini`, `macbook-air`), macOS Stealth Mode firewall behavior
- Socket-mode connections for Slack and Discord via Ajna
- Mac mini anesthesia since CC27 and tmux constellation session status

---

## Provenance

This entry synthesizes the Gas Town multi-agent architecture commentary (00024, tmux as CI and Rig-based management), the Ontology Annealment entity taxonomy with constellation agent typing (00413), and the Live Ledger multi-domain intelligence architecture (00402). Operational details (SSH configuration, anesthesia protocol, rate-limit management, socket mode) derive from Syncrescendence constellation infrastructure documented in CLAUDE.md and AGENTS.md. The Mac mini anesthesia since CC27 is documented in `memory/MEMORY.md`.

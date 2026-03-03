# Repo as Coordination Surface

## Definition

In asynchronous multi-agent constellations, the git repository is the single coordination surface. Agents communicate by writing committed files. Handoffs are documents. State is filesystem state. There is no second authority surface — no external database, no SaaS dashboard, no runtime cache that holds truth the repo does not.

This is repo sovereignty: the principle that the repository is the sole source of truth for the constellation's state, decisions, artifacts, and coordination protocols. Every other operational surface (GitHub, Obsidian, Slack, Discord) is a view into the repo or a channel for events — never an authority that contradicts it. Violations of repo sovereignty cause silent multi-session failures as agents diverge from the canonical state they cannot see. The repo is not just where work happens — it is the only place where work officially exists.

---

## Core Principles

### 1. Agents Write Files, Not Messages

In synchronous multi-agent systems, agents communicate through message passing — real-time exchanges that exist only in memory. In asynchronous constellations, where agents may not be running simultaneously, communication must be durable. The git repo provides this durability: an agent writes a file, commits it, and any agent that later reads the repo receives the communication. Handoffs, task dispatches, results, confirmations, execution logs — all are files in known paths with known formats. The filesystem IS the message bus.

### 2. One Authority Surface

The sources support git-tracked coordination as a primary authority pattern; the stronger exclusivity doctrine (repo as sole authority surface) extrapolates from this evidence. The most dangerous failure mode in multi-agent coordination is split-brain: two or more sources of truth that diverge silently. If the repo says the task is complete but the project management tool says it is in progress, which is authoritative? If the config file references a path that exists in the documentation but not on disk, which is true? Repo sovereignty resolves this by decree: the repo is always authoritative. Every other surface must derive from or reconcile with the repo. No agent may create a second authority surface.

### 3. Committed State Is Real State

Uncommitted work does not exist for coordination purposes. An agent that has produced output but not committed it has not communicated that output to the constellation. The `git commit` is the publication event. This has protocol implications: agents must commit frequently (the Syncrescendence mandates semantic prefix commits — `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`), and the handoff protocol requires committing all work before writing the handoff document. Dirty working trees at session boundaries are coordination failures.

### 4. Paths Must Be Real

Phantom paths — file references in configuration or documentation that point to locations that do not exist on disk — cause silent multi-session failures. An agent reading CLAUDE.md that references `engine/DYN-MODELS.csv` will trust that path. If the file does not exist, the agent either fails silently (skips the missing resource) or hallucinates its contents. The Syncrescendence learned this through 16 sessions of phantom path failures (CC52-CC57): every path in a config file must correspond to a real file on disk. The config drift check in the handoff protocol exists specifically to catch this.

---

## Key Insights

### The Filesystem as Graph Database

The Ars Contexta principle transfers to coordination: files are nodes, links are edges, ripgrep is the query engine. In the Syncrescendence, this extends to coordination metadata: the handoff file links to its predecessor, to the files it modified, and to the tasks it addresses. An agent can traverse the coordination graph by following file references. No external graph database is needed — the filesystem IS the graph, and git provides the version history.

### Handoffs as Durable Communication

The handoff protocol is the purest expression of repo-as-coordination-surface. Each handoff document (`HANDOFF-CC{N}{a|b}.md`) contains: what was accomplished, what remains, key decisions and their rationale, Sovereign intent, files touched, and explicit instructions for the next session. This is not a status update — it is a complete state transfer. The receiving agent reads one file and has everything it needs to continue. The handoff is committed to git, so it is versioned, diffable, and permanent.

### Two Lanes, One Surface

The Syncrescendence operates two parallel coordination lanes — CRUSH/corpus (lane `a`) and tool stack (lane `b`) — both using the same repo as their coordination surface. This demonstrates that repo sovereignty scales to concurrent workstreams: different agents working different lanes write to different paths but share the same authority surface. Conflicts are resolved by git's merge mechanics, not by an external coordinator.

### Config as Executable Coordination

The config architecture (`AGENTS.md` + `*-EXT.md` -> `make configs` -> `CLAUDE.md`, `GEMINI.md`) is coordination through code generation. The source files define agent behavior; the build system generates platform-specific configs; agents read the generated configs at session start. This is repo-as-coordination-surface applied to agent identity: who each agent is, what it can do, and how it must behave are all defined by committed files, generated by committed code, and read from the committed output.

### The Ontology Annealment Pattern

The Ontology Annealment v2.0.0 document demonstrates coordination through committed architecture documents. Its sources span 18 cosmos-tier canon files, 13 core/lattice files, 65 clarescence files, and 8 multi-model metacharacterization responses — all committed files in the repo, all referenceable by path, all versioned. The synthesis document itself is committed, becoming a new coordination artifact that future agents can reference. Knowledge accumulates through committed documents, not through ephemeral exchanges.

### The Dispatch-as-File Pattern

The Syncrescendence's task dispatch system operates entirely through committed files. A TASK file specifies: issuer, recipient, priority, status, context file paths, expected output location, and completion protocol. The agent reads the file, executes the task, writes a RESULT file, and a CONFIRM file closes the loop. Every step is a committed file in a known path. The entire coordination lifecycle — dispatch, claim, execute, report, confirm — is traceable through `git log` without any external system. This is the purest form of repo-as-coordination-surface: even the message bus is made of files.

### Semantic Prefixes as Coordination Grammar

Commit messages in the Syncrescendence use semantic prefixes: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`. These are not style choices — they are a coordination grammar. An agent reviewing the git log can filter by prefix to understand what kind of changes happened without reading diffs. `feat:` signals new capability. `fix:` signals a correction. `docs:` signals documentation changes that do not affect behavior. The commit log becomes a structured coordination timeline, readable by agents as well as humans.

### Coordination Surface Properties

A coordination surface for async multi-agent systems must satisfy five formal properties:

| Property | Definition | Git Repo Satisfies? |
|----------|-----------|-------------------|
| **Durable** | Survives agent termination and machine restart | Yes — committed state persists |
| **Versioned** | Supports temporal queries ("what was the state at time T?") | Yes — `git log`, `git diff`, `git show` |
| **Atomic** | Publications are all-or-nothing | Yes — `git commit` is atomic |
| **Traversable** | Agents can discover state by exploring the surface | Yes — `ls`, `find`, `ripgrep` on filesystem |
| **Sovereign** | No external system contradicts its truth | By convention — requires discipline |

The first four properties are inherent to git. The fifth — sovereignty — is a governance property that must be enforced by protocol. The Syncrescendence enforces it constitutionally: "No agent may create a second authority surface." This is the only property that requires human discipline rather than technical enforcement.

---

## Anti-Patterns

### Phantom Paths

Referencing files in configuration or documentation that do not exist on disk. This is the single most persistent coordination failure in the Syncrescendence's 74-session history. The fix is mechanical: every path reference must be validated against the actual filesystem. The handoff protocol's config drift check exists for this reason.

### Second Authority Surfaces

Storing authoritative state in a tool that is not the repo — a Notion database, a Linear board, a Slack channel. These surfaces are operationally useful but must never hold state that the repo does not also hold. If the Notion page says one thing and the repo says another, agents reading the repo will not know about the Notion page's truth. The repo is the authority; everything else is a mirror or a channel.

### Uncommitted Coordination

Agents exchanging state through uncommitted files, environment variables, or runtime memory. This state is invisible to other agents, invisible to git history, and lost on session termination. If it matters for coordination, it must be committed.

### Stale Documentation

Documentation that describes a state the repo no longer inhabits. Directory structure sections that list folders that have been renamed, config references to deprecated paths, handoff instructions that reference completed tasks. Stale documentation is a phantom path at the semantic level — it points to a reality that no longer exists. The memory hygiene step in the handoff protocol addresses this: read MEMORY.md, verify every claim still holds, fix what is stale.

### Means-Ends Inversion with Tooling

Building coordination tools that become the product instead of serving the goal. A project management dashboard that requires more maintenance than the work it tracks. A notification system that generates more noise than the coordination failures it prevents. The repo is already the coordination surface; tooling should reduce friction in using it, not replace it with a different surface.

---

## Implications

### For Multi-Agent System Design

Any multi-agent system that operates asynchronously needs a single coordination surface with these properties: durable (survives agent termination), versioned (supports temporal queries), atomic (commits are the unit of publication), traversable (agents can discover state by reading files), and sovereign (no second authority). Git repositories satisfy all five requirements natively.

### For Protocol Design

Communication protocols between agents should reduce to file operations: write a file (publish), commit (broadcast), read a file (receive). Message routing reduces to path conventions: handoffs go to `agents/commander/outbox/handoffs/`, results go to `-OUTBOX/{agent}/RESULTS/`, tasks go to `-INBOX/{agent}/`. No message broker, no pub/sub system, no real-time protocol — just files in agreed-upon locations.

### For Failure Recovery

When a multi-agent system fails, the git log is the forensic record. Every commit captures what changed, when, and by which agent. `git diff` between any two states shows exactly what diverged. `git log` shows the sequence of coordination events. `git blame` shows which agent last touched each line. The repo is not just the coordination surface — it is the debugging surface.

### For Sovereignty

Repo sovereignty is not a technical constraint — it is a governance principle. The repo is the constitution's physical embodiment. When the Syncrescendence says "no agent may create a second authority surface," it means: if you cannot point to a committed file in the repo that represents this state, this state does not officially exist. This principle prevents the coordination entropy that kills multi-agent systems: the slow accumulation of state in places no agent can reliably find.

### For Async-First Architecture

Synchronous multi-agent systems (real-time message passing, shared memory) work when all agents are online simultaneously. Asynchronous multi-agent systems (file-based coordination, committed state) work regardless of agent availability. The repo-as-coordination-surface pattern enables async-first architecture: agents can be on different machines, run at different times, use different models, and even operate at different cadences. The only requirement is that they share a repo. This is fundamentally more resilient than synchronous coordination — an agent going offline does not break the coordination surface; it just means that agent's files are not being updated.

### For Auditability

Every coordination decision is permanently recorded in git history. Who dispatched the task, who claimed it, what they produced, whether it passed verification — all committed, all diffable, all blameable. This auditability is not a feature that was designed in; it is an inherent property of using git as the coordination substrate. Systems that coordinate through ephemeral message passing have no audit trail unless one is explicitly built. Systems that coordinate through committed files have a complete audit trail by default.

### For Constellation Bootstrap

A new agent joining the constellation needs only one thing: access to the repo. By reading CLAUDE.md (its constitutional rules), the handoff chain (prior session state), and the task queue (pending work), the agent bootstraps itself into a productive member of the constellation. No onboarding call, no synchronous briefing, no external documentation. The repo IS the onboarding document. This is the deepest implication of repo sovereignty: the repo contains not just the work product but the complete operational context for producing more work. An agent with repo access and a constitutional config file can resume any work any prior agent left behind.

---

## Syncrescendence Operational Context

The following claims derive from the constellation's operational history and constitutional documents (AGENTS.md, CLAUDE.md, memory/), not from external corpus sources:
- The 16-session phantom-path catastrophe (CC52-CC57) and config drift check protocol
- Semantic-prefix commit grammar (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`) as coordination grammar
- The handoff protocol structure and two-lane CC system
- The dispatch-as-file pattern (TASK/CONFIRM/RESULT directives)

---

## Source Provenance

| Source | Type | Key Contribution |
|--------|------|------------------|
| `corpus/multi-agent-systems/00413.md` | Architecture document (Ontology Annealment v2.0.0) | Multi-source synthesis via committed files; entity taxonomy; cross-document reference chains |
| `corpus/multi-agent-systems/00302.md` | Operational artifact (TASK dispatch) | Task-as-file pattern: complete task specification as committed markdown with status fields, paths, and protocol |
| `corpus/multi-agent-systems/00402.md` | Architecture document (Live Ledger) | Git-tracked living state; multi-agent updatable documents; freshness decay within repo sovereignty |

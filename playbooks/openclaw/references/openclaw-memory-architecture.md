# OpenClaw Memory Architecture
## Definitive Nucleosynthesis Entry

---

### Provenance

| Field | Value |
|---|---|
| Fusion date | 2026-03-01 |
| Source 00051 | Deep technical blog: two-layer memory, hybrid search (sqlite-vec + FTS5 BM25), memory_search/memory_get, multi-agent isolation, context vs memory |
| Source 00057 | Three-layer upgrade: knowledge graph with atomic facts + living summaries, weekly synthesis cron, supersession model, compounding flywheel |
| Source 10904 | Social post: two-tier always-on (SOUL.md + MEMORY.md) + vector search on-demand, memoryFlush, S3 sync, QMD self-hosting mention |
| Source 10964 | Comprehensive guide: 3 failure modes, 4 basic config fixes, 4 advanced tools (QMD, Mem0, Cognee, Obsidian), multi-agent setup |
| Source 00179 | Setup template: 8 config files (AGENTS.md, SOUL.md, USER.md, MEMORY.md, HEARTBEAT.md, TOOLS.md, IDENTITY.md, BOOTSTRAP.md) |
| Fusion type | Nucleosynthesis — all distinct reasoning paths preserved, evolution narrative added |

---

## 1. The Core Architecture

### Context vs Memory: The Foundational Distinction

OpenClaw's memory system rests on a single foundational distinction that almost every failure mode traces back to: **context is not memory**.

- **Context** is what lives in the active conversation window. It is transient. When a session ends or the window gets compacted, context evaporates. Anything that exists only in context is gone.
- **Memory** is what gets written to persistent storage — files on disk, a vector database, a knowledge graph — and retrieved in future sessions. Memory survives compaction, reboots, and agent restarts.

The failure to keep this distinction sharp is the root cause of users believing an agent "forgot" something it was never actually asked to store. The agent's in-session recall is perfect. Its cross-session recall is only as good as what was explicitly committed to persistent storage.

### The Native Two-Layer System

Out of the box, OpenClaw operates a two-layer memory architecture:

**Layer 1: Daily logs**
- Append-only raw event log. Every tool call, user message, and agent response is written to a daily timestamped file.
- Granular. Not indexed for semantic retrieval by default. Serves as the audit trail and the raw material for synthesis.

**Layer 2: MEMORY.md**
- A structured markdown file that the agent updates at the end of sessions (or on trigger).
- The human-readable and agent-readable persistent state. Contains distilled facts, preferences, and project state.
- Not semantically indexed in its base configuration — it is loaded into context wholesale, which means it must stay compact enough to fit without crowding out working memory.

Together, these two layers give you: fine-grained history (logs) and a living summary (MEMORY.md). They are complementary and neither substitutes for the other.

### Surviving Reboots

For deployments where agent uptime matters, source 10904 describes an S3 sync pattern: the `memory/` directory is synced to S3 every 5 minutes. On restart, files restore and the vector index rebuilds automatically. This is the production resilience layer — without it, a host restart loses all memory state that hasn't been backed up externally.

### The Always-On Tier

SOUL.md and MEMORY.md operate as the always-on tier — loaded into every session's context without any retrieval step. This is their power and their constraint. They are immediately available but must be kept tight. As MEMORY.md grows, it consumes more context window on every session whether or not that information is relevant to the current task.

This creates the compaction pressure problem addressed in Section 3 and solved in Section 4.

### How Hybrid Search Works

When semantic search is enabled, OpenClaw indexes memory content into a hybrid retrieval system combining two engines:

**sqlite-vec**: Vector similarity search. Each memory chunk is embedded and stored in a sqlite-vec table. At retrieval time, the query is embedded and cosine similarity is computed against all stored embeddings. Returns semantically related results even when exact keywords don't match.

**FTS5 BM25**: SQLite's native full-text search using BM25 ranking. Keyword-based. Fast and exact. Returns results where the query terms appear in the stored text.

**Fusion weighting**: Results from both engines are merged with a 70/30 weighting — 70% weight on vector similarity, 30% on BM25 keyword score. This weighting reflects the empirical finding that semantic relevance is the primary retrieval signal, with keyword precision as a secondary tiebreaker. The combined score determines the final ranking.

### The Retrieval Tools

Two tools surface this system to the agent:

- **memory_search(query, k)**: Runs the hybrid retrieval pipeline. Takes a natural language query and a count `k`. Returns the top-k memory chunks ranked by the fused score. This is on-demand retrieval — it is not called automatically; the agent must decide to invoke it.

- **memory_get(id)**: Direct lookup by memory chunk ID. Used when the agent already knows which memory it wants, typically after a `memory_search` surfaced the ID in a previous call or when following a reference in MEMORY.md.

The on-demand nature of `memory_search` is critical: it means the agent must reason about what it doesn't know and explicitly retrieve it. Agents that don't have this habit — or aren't prompted to develop it — will miss available memories.

---

## 2. The Three Failure Modes

Source 10964 identifies three canonical failure modes. Every memory problem in practice collapses into one of these.

### Failure Mode 1: Never Saved

The information existed in context during a session. The session ended. The agent was never instructed to write the information to persistent storage. It is gone.

This is the most common failure. Users assume agents automatically persist what feels important. They do not unless configured to do so. The fix is explicit save triggers — either agent instructions that specify when to write to MEMORY.md, or automated hooks that run at session end.

Signs: "The agent knew this last session but forgot it today." The information was context-only.

### Failure Mode 2: Saved But Not Retrieved

The information was correctly written to MEMORY.md or the daily logs. But in the current session, the agent never consulted it. Either:

- MEMORY.md wasn't loaded into context (misconfiguration or context overflow pushed it out).
- The agent didn't call `memory_search` with a query that would have surfaced the relevant chunk.
- The chunk existed in the vector store but the query embedding wasn't similar enough to retrieve it (embedding mismatch, too-broad chunk boundaries, or the 70/30 weighting didn't favor the right result).

Signs: "I can see the information in the files but the agent doesn't know it." Storage succeeded; retrieval failed.

### Failure Mode 3: Compaction Destroys

Long-running sessions or projects accumulate context until the window approaches its limit. OpenClaw's compaction mechanism fires, summarizing the oldest context to free space. This summary is lossy by design — it preserves the gist but discards specific details, exact values, decisions and their rationale, and anything that wasn't salient to the summarizer.

If the agent hasn't written important information to persistent storage before compaction fires, that information is gone — replaced by a summary that may not contain it.

This is the most insidious failure mode because it feels like the agent is working fine until suddenly it isn't, and the user can't reconstruct what was lost.

Signs: Long sessions where the agent "drifts" or loses track of specifics established earlier in the same conversation.

---

## 3. Configuration Fixes

### Fix 1: memoryFlush

`memoryFlush` is a compaction-level directive that triggers a silent turn before compaction, prompting the agent to write durable memories to disk. This ensures that even if compaction subsequently destroys in-context detail, the important state has already been flushed.

```json
{
  "compaction": {
    "memoryFlush": {
      "enabled": true,
      "softThresholdTokens": 40000,
      "prompt": "Distill this session to memory/YYYY-MM-DD.md. Focus on decisions, state changes, lessons, blockers. If nothing: NO_FLUSH",
      "systemPrompt": "Extract only what is worth remembering. No fluff."
    }
  }
}
```

The key insight: customize the `prompt` to tell the agent exactly what to capture — decisions, state changes, lessons, blockers. The default prompt is generic. Raising `softThresholdTokens` to 40000 triggers flushes earlier, before the good stuff gets compacted.

This is the single highest-leverage configuration change for preventing Failure Mode 3. Deploy it first.

### Fix 2: Context Pruning TTL

Left unchecked, MEMORY.md grows monotonically. Every session adds entries; nothing is removed. Eventually the file is large enough that loading it whole consumes a significant fraction of the context window, crowding out working memory.

Context pruning controls how old messages are removed before full compaction. TTL mode is the simplest fix:

```json
{
  "contextPruning": {
    "mode": "cache-ttl",
    "ttl": "6h",
    "keepLastAssistants": 3
  }
}
```

This keeps messages from the last 6 hours and always preserves the 3 most recent assistant responses. This eliminates the situation where recent messages are lost following a context flush. The TTL and `keepLastAssistants` values can be tuned per use case — shorter TTLs for fast-moving sessions, longer for research work. Context pruning also reduces token costs by keeping the active window lean.

### Fix 3: Hybrid Search Configuration

Enabling the sqlite-vec + FTS5 hybrid search is done through the `memorySearch` config block:

```json
{
  "memorySearch": {
    "enabled": true,
    "sources": ["memory", "sessions"],
    "query": {
      "hybrid": {
        "enabled": true,
        "vectorWeight": 0.7,
        "textWeight": 0.3
      }
    }
  }
}
```

The 70/30 weighting favors vector similarity as the primary retrieval signal, with BM25 keyword matching as a secondary tiebreaker. BM25 catches exact matches (error codes, project names) that vector search misses. If you're not running hybrid search, you're leaving accuracy on the table.

### Fix 4: Session Indexing

By default, daily logs are written but not indexed into the vector store. Session indexing changes this: past conversations are chunked and embedded alongside memory files, making the full session history searchable via `memory_search`.

```json
{
  "memorySearch": {
    "sources": ["memory", "sessions"]
  },
  "experimental": {
    "sessionMemory": true
  }
}
```

With session indexing enabled, questions like "What did we decide about the content template last Tuesday?" become answerable. The `sessions` source in `memorySearch` tells the retrieval pipeline to include indexed session transcripts alongside the dedicated memory files.

---

## 4. Advanced Backends

### QMD (Query Memory Distillation)

QMD is a reranking layer that sits between `memory_search` retrieval and the agent's consumption of results. After the hybrid search returns k candidates, QMD runs a second pass: it uses a language model to score each candidate for relevance to the actual query, reranking the results beyond what vector similarity and BM25 can capture.

What QMD solves: the embedding space is imperfect. Two chunks can have similar vector representations but very different actual relevance to a specific question. QMD's LM-based reranking catches cases where the initial retrieval got the direction right but the ordering wrong.

When to use QMD: when retrieval quality matters more than retrieval latency, and when you have a library of memory content large enough that the top-k from raw hybrid search contains meaningful noise. Not worth the added latency and cost for small memory stores.

QMD also supports self-hosting — relevant for OpenClaw deployments where API calls to external reranking services are undesirable. The QMD reranker can run locally against open-weight models.

QMD shared paths: in multi-agent setups, QMD can be configured to index shared memory paths accessible to multiple agents, with per-agent filtering applied at retrieval time. This enables agents to benefit from a common retrieval layer without breaking memory isolation (covered in Section 6).

### Mem0

Mem0 is an external memory service that provides automatic capture — rather than requiring the agent to decide when to call memory tools, Mem0 intercepts all interactions and extracts and stores memories automatically based on content analysis.

What Mem0 solves: Failure Mode 1 (never saved) at scale. If the agent would have needed to recognize that something is worth remembering and call a write tool, Mem0 removes that dependency. Everything passes through Mem0's extraction layer and relevant facts are persisted without the agent needing to initiate the write.

When to use Mem0: when agents are operating in high-throughput scenarios where manual save triggers are impractical, or when you want zero-configuration memory persistence without tuning agent behavior. The tradeoff is that Mem0's automatic extraction is opinionated — it decides what's memorable, which may not match your priorities.

Mem0 is an external service (with a self-hosted option), adding a network dependency to the memory pipeline.

### Cognee

Cognee is a knowledge graph backend. It structures stored memories as a graph of entities and relationships rather than as a flat chunk store. Entities (people, projects, concepts, decisions) become nodes; relationships (owns, depends-on, succeeded-by, contradicts) become edges.

What Cognee solves: the flat chunk retrieval model loses relational structure. If MEMORY.md contains "Project X depends on Library Y" and "Library Y was deprecated in v3.2", a chunk-based retrieval for "Project X compatibility" may not surface the Library Y deprecation because the chunks are stored separately and the connection is implicit. In a knowledge graph, the traversal from "Project X" to "Library Y" to "deprecated in v3.2" is explicit and queryable.

Cognee overlaps in purpose with the native knowledge graph upgrade described in Section 5, but is an external managed service rather than a self-maintained file structure.

When to use Cognee: when memory content is relationship-dense and relational queries matter more than simple fact retrieval. Projects with complex dependency graphs, team structures, or evolving architectural decisions benefit most.

### Obsidian Integration

Obsidian is a local Markdown knowledge base with bidirectional links, graph view, and a plugin ecosystem. OpenClaw can be configured to write memories to an Obsidian vault, making the memory store human-browsable, editable, and linkable.

What Obsidian solves: the opacity of vector stores. A developer cannot open a sqlite-vec database and read it. An Obsidian vault is just files — you can read, edit, restructure, and link them manually. This gives humans a meaningful interface into the agent's memory, enabling review and correction that is impossible with opaque backends.

When to use Obsidian: when human oversight and editorial control of memory content is a priority. Research workflows, personal knowledge management, and any scenario where the human wants to contribute to the memory base directly. Not ideal for high-velocity automated workflows where manual editorial overhead defeats the purpose.

---

## 5. The Knowledge Graph Upgrade

Source 00057 describes a three-layer architecture that supersedes the native two-layer system.

### Layer 1: Event Logs (unchanged)

Daily timestamped logs remain the raw event record. No change in function.

### Layer 2: MEMORY.md (evolved role)

MEMORY.md continues as the always-on distilled summary, but its role narrows: it now holds only the highest-salience, most time-sensitive information — the working state for the current project phase. The knowledge graph absorbs the growing body of stable facts that previously accumulated in MEMORY.md until it became unwieldy.

### Layer 3: Knowledge Graph — /life/areas/

A directory structure (canonically at `/life/areas/` in the reference implementation) where each domain of knowledge has its own entity folder:

```
/life/areas/
├── people/
│   ├── sarah/
│   │   ├── summary.md
│   │   └── items.json
│   ├── maria/
│   └── emma/
├── companies/
│   ├── acme-corp/
│   └── newco/
```

Each entity folder contains two files:

- **items.json**: An array of atomic, timestamped facts. Each fact is a discrete unit with an ID, content, timestamp, category, and status (`active` or `superseded`). Facts are stored as JSON objects in a single array per entity — not one file per fact. Example: `{"id": "sarah-003", "fact": "Difficult manager, micromanages", "timestamp": "2025-06-15", "status": "active"}`.
- **summary.md**: A living summary rewritten weekly from the active facts in `items.json`. The human-readable snapshot of what the agent currently knows about this entity.

The tiered retrieval pattern: load `summary.md` first for quick context; drill into `items.json` only when atomic detail is needed. Rules from the source: "Save facts immediately to items.json. Weekly: rewrite summary.md from active facts."

### Supersession Model (Not Deletion)

When a fact changes, the old fact is not deleted. It is marked `superseded` in `items.json` with a pointer to the new fact:

```json
{
  "id": "sarah-003",
  "fact": "Difficult manager, micromanages",
  "timestamp": "2025-06-15",
  "status": "superseded",
  "supersededBy": "sarah-007"
}
```

The new fact is added to the same `items.json` array:

```json
{
  "id": "sarah-007",
  "fact": "Left company. New manager is supportive.",
  "timestamp": "2025-12-01",
  "status": "active"
}
```

This model preserves the history of how understanding evolved. Retrieval queries can filter by `status: active` to get present truth, or can traverse superseded facts via `supersededBy` pointers to understand the reasoning path. Nothing is destroyed; the record accumulates.

### Weekly Synthesis Cron

The living summary files don't update themselves. A cron job runs weekly, prompting the agent to:

1. Retrieve all atomic facts in a domain.
2. Identify which are current, which are historical.
3. Synthesize a new living summary that reflects current state.
4. Archive the previous living summary with a timestamp.

```cron
0 9 * * 1 /path/to/openclaw/scripts/synthesize-domain.sh --domain /life/areas/ --agent synthesis-agent
```

The weekly cadence is a deliberate design choice. Daily synthesis would be too expensive and surface noise. Monthly would let living summaries drift too far from current facts. Weekly tracks project evolution without excessive churn.

### The Compounding Flywheel

The knowledge graph architecture creates a self-reinforcing improvement loop:

1. New facts are atomically added as they emerge.
2. Weekly synthesis integrates new facts into living summaries.
3. Living summaries become richer reference material.
4. Richer reference material makes future sessions more productive.
5. More productive sessions surface more worth storing as atomic facts.

This is the compounding flywheel: the more faithfully the system captures atomic facts, the better the synthesis; the better the synthesis, the more useful the memory; the more useful the memory, the more the agent and human engage with it and maintain it. The system becomes self-sustaining.

Contrast with flat MEMORY.md, which has the opposite dynamic: the more you add, the harder it is to find what matters, the more the context window gets crowded, and the less useful the memory becomes over time.

---

## 6. Multi-Agent Memory

### Isolation by Default

Each OpenClaw agent has its own private memory space. Daily logs, MEMORY.md, and the vector index are agent-scoped. Agent A cannot read Agent B's private memory. This is the correct default — agents operating on different tasks, for different users, or with different trust levels must not bleed state into each other.

```
/agents/
  agent-a/
    memory/
      MEMORY.md
      daily_log/
      vector_index/
  agent-b/
    memory/
      MEMORY.md
      daily_log/
      vector_index/
```

### Shared Reference Files

Isolation is right for private memory. But agents in a constellation often need to share reference information: a shared knowledge base, project-wide decisions, organizational context.

The solution is shared reference files — read-only (or carefully write-controlled) files outside any agent's private memory directory that multiple agents can read. These are not searched via each agent's private `memory_search`; instead, they are loaded into context directly (like SOUL.md) or searched via a shared QMD path.

```
/shared/
  reference/
    project-decisions.md
    team-context.md
    architecture.md
```

Agents are configured to include shared reference paths in their context. The source describes this as adding shared directories to the agent's config so that reference files are loaded alongside private memory.

### QMD Shared Paths

When shared reference content is large enough that loading it wholesale into context is too expensive, QMD shared paths provide an alternative: a shared vector index covering the shared reference files, queried via `memory_search` with per-agent filtering. The QMD config includes the shared directory, and per-agent filtering ensures that private memories are retrievable only by the originating agent while shared reference content is retrievable by all.

### Coordination Patterns

Multi-agent memory introduces coordination challenges around writes. The sources do not prescribe specific named patterns, but the principle is clear: private memory spaces prevent write conflicts by default, and any cross-agent information sharing must be explicitly designed — either through shared read-only reference files, shared QMD index paths with per-agent filtering, or structured handoff mechanisms that gate what enters each agent's context.

---

## 7. The Setup Kit

Source 00179 provides a paste-and-go setup template built on 8 config files. These are the minimum viable configuration for a production OpenClaw deployment.

### AGENTS.md

The constitutional document. Defines the agent's role, authority, behavioral constraints, and operating principles — including subagent dispatch modes, memory system configuration, group chat behavior, security posture, heartbeat definitions, and tool references.

Contains: agent name and role, what the agent is authorized to do, what it is prohibited from doing, how it should handle uncertainty, its relationship to other agents.

### SOUL.md

The agent's persistent identity layer. Loaded into every session context. Contains the agent's stable self-model: its values, communication style, domain expertise, and relationship to the human it serves. SOUL.md should change rarely — it encodes who the agent is, not what it's currently working on.

Distinct from MEMORY.md: SOUL.md is identity, MEMORY.md is working state.

### USER.md

The human operator's profile as seen by the agent. Communication preferences, expertise level, working patterns, domain knowledge, and things the agent should know about the human to serve them well. Also loaded into every session context.

The split between SOUL.md (agent's self-model) and USER.md (model of the human) makes it easy to swap agents while preserving the human's profile, or to run the same agent for different humans.

### MEMORY.md

The always-on working state. Current projects, recent decisions, active context, open questions. See Sections 1 and 5 for the full treatment of how MEMORY.md fits into the memory architecture.

Key discipline: MEMORY.md must stay compact. It is loaded into every session. If it grows without bound, it eventually crowds out the context needed for actual work. Use context pruning TTL (Section 3) and the knowledge graph (Section 5) to manage its growth.

### HEARTBEAT.md

A session health and continuity file. Updated at the start and end of each session with: session timestamp, what was accomplished, what is pending, any anomalies or issues encountered. Provides a quick human-readable status check — open HEARTBEAT.md to understand where the agent is in its current work cycle without reading the full session log.

Optionally used as the trigger target for memoryFlush: the agent writes to HEARTBEAT.md as it flushes, providing a human-visible record of when and what was flushed.

### TOOLS.md

Enumerates the tools available to the agent and their usage constraints. Which tool to use for which purpose, rate limits, cost considerations, and any tools that are disabled in this deployment. Prevents the agent from attempting to invoke tools that aren't configured and provides a reference when the agent must choose between multiple capable tools.

### IDENTITY.md

A more detailed expansion of the agent's role definition. Where AGENTS.md defines the role at a constitutional level, IDENTITY.md provides the operational specifics: what outputs the agent produces, what decisions it owns, what it escalates, what it delegates. The agent reads IDENTITY.md to understand what "doing its job well" looks like.

### BOOTSTRAP.md

The initialization script for new sessions. A structured prompt that the agent runs through at the start of each session to orient itself: load MEMORY.md, read HEARTBEAT.md for current state, check inbox for pending work, verify tool availability. BOOTSTRAP.md encodes the session startup ritual so the agent consistently initializes in a known state.

Paste-and-go: copy BOOTSTRAP.md's contents into the first message of a new session to reliably orient the agent. This is the human's primary interface for controlling what the agent "wakes up knowing."

---

## 8. Evolution Narrative

The architecture described in this document did not arrive fully formed. It evolved through five recognizable phases, each one solving the failure mode that the previous phase exposed.

### Phase 1: Static Files (The Starting Point)

The simplest possible approach: one markdown file, MEMORY.md. The agent reads it at the start of a session, writes to it at the end. This works for small projects with a single agent and a small, well-organized knowledge base. It fails as soon as MEMORY.md grows large enough to crowd context, as soon as information from 45 days ago is irrelevant to today's work but still consuming tokens, or as soon as multiple agents need memory.

### Phase 2: Hybrid Search (Solving Retrieval)

The addition of sqlite-vec + FTS5 BM25 hybrid search transforms the memory store from a single large file into a searchable corpus. MEMORY.md shrinks to a compact always-on summary; the bulk of memory moves to the indexed store, retrieved on demand via `memory_search`. The 70/30 vector/BM25 weighting emerges from empirical tuning of retrieval quality.

This phase introduces the retrieval tools (`memory_search`, `memory_get`) and the chunking and embedding pipeline. It solves Failure Mode 2 (saved but not retrieved) at scale — now the memory store can grow without degrading context quality, because only relevant chunks are retrieved per session.

### Phase 3: Compaction-Aware Flush (Solving Loss)

Phase 2 solved retrieval but didn't address the write side. Long sessions still lost information to compaction. The addition of `memoryFlush` — triggered at a context window threshold rather than at session end — closes this gap. Combined with session indexing (end-of-session embedding of the session log), Phase 3 ensures that information written during a session survives compaction and becomes searchable in future sessions.

This phase also introduces context pruning TTL, which manages MEMORY.md's long-term growth by archiving aged entries to the searchable store.

### Phase 4: External Backends (Solving Scale and Specialization)

The native sqlite-vec + FTS5 system handles the common cases well. But specific use cases expose its limits: automatic capture (Mem0), reranking quality at large scale (QMD), relational retrieval (Cognee), and human editorial access (Obsidian). Phase 4 is modular — these backends aren't replacements for the native system, they're extensions that slot in where the native system is insufficient.

This phase also solidifies the multi-agent memory architecture: private isolation as the default, shared reference files and QMD shared paths for constellation-wide knowledge, coordination patterns for controlled cross-agent writes.

### Phase 5: Self-Maintaining Knowledge Graph (The Compounding State)

The final evolution resolves the fundamental limitation of all previous phases: they required the agent or the human to consciously maintain memory quality. MEMORY.md needed periodic manual pruning. Chunk boundaries needed tuning. The vector index needed monitoring.

The three-layer knowledge graph with atomic facts, the supersession model, and the weekly synthesis cron creates a system that maintains itself. New information enters as atomic facts — small, precise, easily managed. Weekly synthesis integrates them into living summaries. Historical facts are preserved but filtered from current views. No information is lost; no information is permanently in the way.

The compounding flywheel closes the loop: the system becomes more useful as it grows, rather than less useful. This is the qualitative shift that distinguishes Phase 5 from all previous phases — it is the first architecture where more usage makes the system better rather than more unwieldy.

---

*This entry is the definitive treatment of OpenClaw memory architecture as of 2026-03-01. All distinct reasoning paths from sources 00051, 00057, 10904, 10964, and 00179 are carried forward. Subsequent discoveries should be fused into this entry, not appended alongside it.*

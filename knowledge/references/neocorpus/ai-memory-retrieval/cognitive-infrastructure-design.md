# Cognitive Infrastructure Design

**Nucleosynthesis Date**: 2026-03-02
**Synthesized By**: Commander (Claude Opus 4.6)
**Protocol**: CRUSH — lossless compression of corpus source files

---

## Sources

| ID | File | Content |
|----|------|---------|
| 11092 | `corpus/ai-memory-retrieval/11092.md` | Oracle triangulation response — monorepo structure, PARA-style separation, agent tool configs, industry consensus |
| 00404 | `corpus/ai-memory-retrieval/00404.md` | Triangulated Memory Architecture Decision (STH) — three-layer memory, JSONL journals, file-first constitutional |
| 00730 | `corpus/ai-memory-retrieval/00730.md` | Deferred Commitments Register — per-agent memory layout execution, memsync daemon, Phase 1-2 implementation |
| 10197 | `corpus/ai-memory-retrieval/10197.md` | Ralph loop — context window degradation from self-modifying instruction files |
| 00082 | `corpus/ai-memory-retrieval/00082.md` | Supermemory — memory injection vs. tool-based recall, cross-platform persistence |

---

## Definitive Treatment

### What Cognitive Infrastructure Is

Cognitive infrastructure is the durable substrate — directories, files, schemas, version control practices, and retrieval systems — that enables one or more AI agents to accumulate, organize, and access knowledge across sessions. It is the engineering layer between raw information and usable intelligence.

The term distinguishes itself from "memory" (which implies a feature) and "knowledge base" (which implies a static collection). Cognitive infrastructure is living, versioned, multi-agent-aware, and designed to outlast any single session, model version, or tool platform. It is closer to an operating system for thought than a database for facts.

### Core Design Principles

#### Shallow Semantic Top-Level Directories

Industry consensus converges on 5-7 top-level directories maximum, organized by lifecycle stage rather than file type or agent identity. The Oracle triangulation (11092) documents this as the intersection of PARA (Projects/Areas/Resources/Archive), Johnny.Decimal numbering, and Zettelkasten atomic linking in git.

The rationale is cognitive overhead. Humans reviewing agent work — the "Sovereign bandwidth constraint" — can process approximately five atoms of new information per day. Deep nesting or ad-hoc subdirectories multiplies navigation friction. Every additional directory level is a tax on the human who must ultimately understand what the agents are doing.

The recommended structure separates:
- **Capture/Inbox**: Mutable, high-volume, disposable. Where raw information arrives before triage.
- **Operational scaffold**: Live, versioned scripts, prompts, configs. The machinery of coordination.
- **Append-only logs**: Handoffs, session records, pedigrees. Auditability and continuity.
- **Protected canon**: Immutable ground truth. What has been verified and ratified.

This four-way separation mirrors the lifecycle of knowledge: raw input is captured, processed through operational scaffolding, recorded in temporal logs, and crystallized into canonical output.

#### Single Source of Truth

The constitutional principle that recurs across every source: one authoritative file generates all downstream artifacts. In the Syncrescendence implementation, `AGENTS.md` plus a `Makefile` generates per-tool configuration files (`CLAUDE.md`, `GEMINI.md`, etc.). The generated files are never edited directly.

This is not merely a software engineering best practice applied to knowledge management. It solves a specific failure mode of multi-agent systems: divergent truth. When five agents can each write to shared state, and each reads from a different cached version, contradictions accumulate silently. A single source of truth with deterministic generation eliminates this class of error.

The principle extends to memory itself. The Sovereign Temporal Hybrid architecture (00404) declares git-tracked files as Layer 0 — constitutional truth with absolute authority. Graph databases and vector stores are explicitly designated as projections, not sources of truth. They are rebuildable from git. If they disagree with the filesystem, the filesystem wins.

#### Per-Agent Memory Layouts

The implementation record (00730) documents a specific per-agent directory structure:

```
agents/<name>/memory/
  MEMORY.md        — agent's persistent knowledge summary
  entities/        — known entities (people, projects, concepts)
  journal/         — append-only session records (JSONL)
  cache/           — ephemeral derived state
  sync/            — synchronization artifacts for graph/vector layers
```

Each agent gets its own memory workspace, not a shared pool. This is significant because different agents have different cognitive styles and different memory needs. The Oracle triangulation (00404) explicitly specifies per-agent tuning of memory retrieval: Claude gets wide lateral context with high `max_facts`, GPT gets narrow schema-matched precision, Gemini gets pre-computed relational subgraphs in plaintext.

The per-agent layout also enables independent evolution. One agent's memory can be restructured without affecting others. Memory layouts are versioned alongside the agent's operational config.

#### Git as the Substrate

Every source in the corpus converges on git as the foundational layer. Not as a version control afterthought, but as the constitutional substrate:

- **Append-only semantics**: Git history is immutable. Once committed, knowledge provenance is permanent.
- **Branching for experimentation**: Memory restructuring can be tested on branches before merging to main.
- **Diff-based change tracking**: Any mutation to agent memory is visible in `git diff`.
- **.gitignore for lifecycle management**: Ephemeral caches and perishable sources are excluded from the permanent record.
- **Protected zones**: `.gitattributes` or explicit policies prevent casual modification of canonical files.

Git hygiene for cognitive infrastructure requires specific discipline. The Oracle response (11092) warns: violation bloats history, pollutes search, and breaks continuity. Lost handoffs — session records that were never committed — are the most common failure mode.

### The Three-Layer Architecture

00404 describes a "three-layer architecture" while also treating git as a foundational Layer 0; this entry's Layer 0-3 taxonomy synthesizes that ambiguity into a cleaner structure than the source provides. The triangulated memory architecture (00404) defines three layers that are now the reference model:

**Layer 0 — Constitutional Truth (Git)**
Git-tracked markdown files. Absolute authority. If git works, Layer 0 works. All agents read and write. This is the filesystem-as-memory pattern at its most deliberate.

**Layer 1 — Working Memory (Context Window)**
The current context window contents — task state, active entities, tool outputs. Ephemeral by nature. Dies with the session. Must contain only what is needed to decide the next action safely. Per-agent tuning determines how much of Layers 0 and 2 are loaded into Layer 1.

**Layer 2 — Session Memory (File-Based, Git-Tracked)**
The per-agent memory directories. JSONL journals as machine-parseable event streams. Entity files as structured knowledge. This layer bridges the gap between the full context of Layer 0 and the constrained window of Layer 1.

**Layer 3 — Long-Term Memory (Graph)**
Graphiti on Neo4j, with group_id scoping for cross-agent memory partitions. Explicitly designated as a projection — rebuildable from git. The memsync daemon (00730) watches JSONL journals and posts to Graphiti, creating the bridge from file-first to graph-queryable.

The critical architectural decision: graph and vector are PROJECTIONS, not source of truth. This means the filesystem can always be reconstructed without the graph, but the graph cannot be reconstructed without the filesystem. The dependency arrow points one way.

### What Breaks

The corpus documents specific failure modes through lived experience:

**Phantom paths**: Referencing files or directories in config documents that do not exist on disk. This produces silent failure — agents receive instructions pointing to nonexistent resources and either hallucinate or silently skip. The Syncrescendence experienced 16 consecutive sessions of phantom path drift before detection.

**Growing instruction files**: The Ralph analysis (10197) documents what happens when agents modify their own instruction files each iteration. Models are verbose by default. Each loop adds tokens. Within ten iterations, the context window is consumed by instructions before the actual task begins. Self-modifying memory is a trap unless strictly bounded.

**Stale memory without decay**: Facts stored without timestamps accumulate contradictions. This example illustrates temporal contradiction patterns consistent with 10120-style analysis, though 10120 is not in this entry's declared provenance. A user changed jobs but the memory still contains both "loves their job" and "hates their job" with no temporal resolution. The STH architecture defers autopoietic decay (Hebbian learning on edge weights) as a long-term vision, using timestamp-based staleness detection as the current practical solution.

**Divergent caches**: When multiple agents or tools maintain their own state outside the canonical filesystem, truth diverges. The Syncrescendence rule — "repo sovereignty" — means no agent may create a second authority surface. GitHub, dashboards, and runtime tool state are operational surfaces, never constitutional truth.

---

## Anti-Patterns

**Deep nesting**: More than two directory levels for any cognitive infrastructure path. Each level taxes human reviewability and agent navigation.

**Shared mutable memory pools**: Multiple agents writing to the same memory file without coordination. Produces race conditions, interleaved garbage, and unreadable state.

**Generated files as sources**: Editing a downstream artifact instead of the source that generates it. The edit survives until the next regeneration, then vanishes — creating phantom state that worked once but fails permanently.

**Memory without provenance**: Facts stored without attribution to the session, source, or timestamp that produced them. Makes contradiction resolution impossible.

**Config without validation**: Agent configs that reference directories, tools, or paths without automated validation that those references resolve. Silent failure is the default outcome.

---

## Implications

Cognitive infrastructure design is an emerging discipline at the intersection of knowledge management, software architecture, and multi-agent systems engineering. The corpus teaches that the key decisions are not about which database to use or which embedding model to deploy. They are about:

1. **What is the source of truth?** The answer must be singular and unambiguous.
2. **What is a projection?** Everything that is not the source of truth must be explicitly labeled as derived and rebuildable.
3. **What is the human review surface?** The infrastructure must be legible to the human who ultimately governs it.
4. **What decays, and how?** Without explicit staleness management, memory becomes a liability rather than an asset.

The filesystem-first, git-tracked, single-source-of-truth pattern has emerged as the dominant architecture not because it is technically sophisticated, but because it is durable, inspectable, and sovereign. It survives model changes, tool migrations, and platform lock-in. It is the architecture that assumes everything else will change.

The deepest lesson from the corpus: cognitive infrastructure is not a technical project. It is an epistemic commitment. The choice of directory structure, memory schema, and truth hierarchy determines what the agents can know, how they can learn, and what they will forget. Every structural decision is a knowledge decision. Build accordingly.

---

## Obsolescence & Supersession

### Obsolescence: Deep Directory Hierarchies

Early agent systems (2022-2024) inherited software engineering conventions: deep nested directories, per-feature subdirectories, role-based file organization. Applied to cognitive infrastructure, this created navigation overhead that exceeded the human-review budget. The Oracle triangulation (11092) explicitly diagnosed this: five top-level directories maximum, organized by lifecycle stage. Deep nesting is now understood as a cognitive infrastructure anti-pattern — not a technical failure but a human-readability failure. The agent system is only as useful as its human oversight permits.

### Obsolescence: Generated Files as Sources

The catastrophic failure mode documented by the Syncrescendence CC31 incident: "sear everywhere" applied as find-replace across generated + source + historical files simultaneously. The assumption that all files with similar content should be updated together ignored the distinction between sources (AGENTS.md) and projections (CLAUDE.md, GEMINI.md). This is a cognitive infrastructure version of the graph-as-source-of-truth anti-pattern: when you edit a projection instead of a source, the edit survives until the next regeneration, then silently vanishes. 16 consecutive sessions of phantom path drift (CC52-CC57) resulted from this misunderstanding applied at the config level.

### Supersession: The Single-Source-of-Truth Pattern

**v1 (Ad-hoc configuration):** Agent configs were written independently per tool. CLAUDE.md and GEMINI.md were edited directly. Divergence was inevitable — the files said different things because they were maintained separately.

**v2 (Template consolidation):** A shared template or common document, manually maintained. Better, but still required manual synchronization.

**v3 (Current — AGENTS.md + Makefile):** A single source (AGENTS.md) generates all per-harness outputs via `make configs`. Validation (`make validate`) checks that all referenced paths exist. No generated file is ever edited directly. The Oracle session (pre-CC22, PROMPT-ORACLE-CONFIG-CONSENSUS-ARCHITECTURE.md) declared this "the most advanced implementation seen." The key lesson from the supersession chain: the cost of divergent truth in multi-agent systems scales non-linearly with agent count. What works for one agent fails for five.

---

## Syncrescendence Operational Context

The following claims derive from the constellation's operational history and constitutional documents (AGENTS.md, CLAUDE.md, memory/), not from external corpus sources:
- The 16-session phantom-path drift incident derives from the constellation's operational history (CC52-CC57 era), not from the cited corpus sources

## Source Provenance

- `corpus/ai-memory-retrieval/11092.md` — Oracle triangulation: monorepo structure + agent configs
- `corpus/ai-memory-retrieval/00404.md` — Triangulated Memory Architecture Decision (STH)
- `corpus/ai-memory-retrieval/00730.md` — Deferred Commitments Register (memory implementation)
- `corpus/ai-memory-retrieval/10197.md` — Ralph loop context degradation
- `corpus/ai-memory-retrieval/00082.md` — Supermemory memory injection pattern

This is excellent source material. I now have everything needed for a comprehensive, cited verification response.

***

## 1. Verdict

**Your remediation thesis is substantially correct and well-supported by current industry practice as of March 2026.** The specific architectural decomposition — constitution → executive intention → administrative program → harness playbooks → communications law → ontology registry — maps closely to patterns that the most serious AI engineering teams are independently converging on. The federal layering metaphor is sound. The main areas requiring clarification are artifact-class discipline (underspecified by most teams) and the "table of contents" principle for constitutional documents (your constitution layer risks becoming the monolithic AGENTS.md anti-pattern OpenAI already hit and documented).

***

## 2. What The Repo Thesis Gets Right

### The Harness Is the Product

OpenAI's February 2026 "Harness Engineering" post documents a real team shipping a million-line product with zero manually-written code, and their primary conclusion is precisely this: **"building software still demands discipline, but the discipline shows up more in the scaffolding rather than the code"**. The harness — its structure, its config system, its feedback loops — becomes the actual locus of engineering judgment. This directly validates your thesis that the harness is the product. [openai](https://openai.com/index/harness-engineering/)

### Repo-as-Coordination-Surface

OpenAI's harness engineering post is unusually explicit about this: *"From the agent's point of view, anything it can't access in-context while running effectively doesn't exist. Knowledge that lives in Google Docs, chat threads, or people's heads are not accessible to the system. Repository-local, versioned artifacts (e.g., code, markdown, schemas, executable plans) are all it can see."*. This is not a generic endorsement of version control — it is a precise architectural claim that the repo is the only durable coordination surface for agents, and the team made material investment decisions based on it. [openai](https://openai.com/index/harness-engineering/)

This is further reinforced by their practice of treating plans as first-class artifacts checked into the repository, with *"active plans, completed plans, and known technical debt all versioned and co-located, allowing agents to operate without relying on external context"*. [openai](https://openai.com/index/harness-engineering/)

### Constitutional Source + Per-Harness Playbooks

Both Claude Code and Codex have independently converged on a hierarchical, modular configuration model rather than a single universal prompt. Claude Code uses a three-level memory hierarchy: Enterprise (`~/.claude/CLAUDE.md`) → Project (`./CLAUDE.md`) → Personal local overrides, where higher-level rules override lower ones. Codex uses a parallel system with `AGENTS.md` as a **table of contents** that points into a structured `docs/` directory, with per-domain playbooks and skills. The OpenAI harness team explicitly tested the "one big AGENTS.md" approach and documented why it failed  — stale rot, non-guidance, context crowding, and inability to verify coverage. This is a direct empirical case for your thesis that one constitutional source + many harness-specific playbooks beats one flattened mega-prompt. [letanure](https://www.letanure.dev/blog/2025-07-31--claude-code-part-2-claude-md-configuration)

Codex skills provide the clearest example of per-harness doctrine: the team built 100+ internal skills including a security-best-practices skill, a PR automation skill, and a Datadog integration skill, and team members copy from each other. Claude Code has an analogous skills system in its extension layer. [introl](https://introl.com/blog/claude-code-cli-comprehensive-guide-2025)

### Federal Layering Is Structurally Supported

The federal metaphor — enforce boundaries centrally, allow autonomy locally — is explicitly described by OpenAI's harness team as their core governance principle: *"enforce boundaries centrally, allow autonomy locally. You care deeply about boundaries, correctness, and reproducibility. Within those boundaries, you allow teams—or agents—significant freedom in how solutions are expressed."*. Their actual implementation maps directly to your proposed layers: [openai](https://openai.com/index/harness-engineering/)

| Your Layer | OpenAI Harness Equivalent |
|---|---|
| Constitution | `AGENTS.md` (table of contents) + "golden principles" |
| Executive Intention | Active execution plans, checked into repo |
| Program / Backlog | Plans directory: active, completed, known technical debt |
| Harness Playbooks | Per-domain skills (100+ internally published) |
| Communications Law | Linter-enforced PR/review/handoff lifecycle |
| Ontology Registry | Architecture docs: domain map, package layering, quality grades |

 [openai](https://openai.com/index/harness-engineering/)

***

## 3. What Is Unsupported or Overclaimed

### The "Constitution as Single File" Risk

The biggest risk in your current thesis is that your constitutional layer becomes the monolithic-AGENTS.md anti-pattern. OpenAI documented this failure mode precisely: a giant instruction file crowds out task context, becomes non-guidance when everything is marked important, rots instantly because humans stop maintaining it, and cannot be mechanically verified. **The constitutional source should be a short, stable table of contents with explicit pointers to deeper truth — not a compendium.** If your neocorpus is being treated as the constitutional layer directly, this is an architecture smell. [openai](https://openai.com/index/harness-engineering/)

### Communications Law Has No Strong Established Precedent

The artifact-class separation you propose (prompts / responses / logs / handoffs / outputs as distinct classes) is directionally correct but **not yet formalized by any major practitioner ecosystem**. The closest existing pattern is ADR-as-code (Architectural Decision Records stored in `docs/adrs/`), incident runbooks, and the "plans as first-class artifacts" pattern from OpenAI. But prompt-vs-response-vs-handoff as separate legal classes does not have a documented, widely-adopted taxonomy. Your intuition is sound; the implementation is yours to define. [linkedin](https://www.linkedin.com/pulse/from-adrs-action-embedding-architectural-decisions-dev-riaz-a-khan-jqnec)

### Rosetta Stone / Intent Compass Path Resolution

This is a real gap. The harness engineering literature uniformly agrees that authority surfaces must be **mechanically discoverable** — not just conceptually important. OpenAI enforces this with dedicated linters and CI jobs that validate the knowledge base is cross-linked and structured correctly, and run a recurring "doc-gardening" agent. If Rosetta Stone and Intent Compass are live authority concepts without resolved, canonical, mechanically-enforced paths, they are in the same failure mode as every undiscoverable Google Doc. [openai](https://openai.com/index/harness-engineering/)

***

## 4. Current Industry Patterns

### Progressive Disclosure Architecture

The dominant pattern across Claude Code, Codex, and serious practitioner workflows is **progressive disclosure**: a short, stable entry point (AGENTS.md / CLAUDE.md at root) that points agents to deeper, domain-specific truth. The Codex harness team treats their `AGENTS.md` as roughly 100 lines serving as a map, not a manual. Claude Code's configuration system enforces this through its hierarchy: enterprise → project → personal, with more specific files overriding general ones. [eesel](https://www.eesel.ai/blog/claude-code-configuration)

### Plans as First-Class Versioned Artifacts

The practice of checking execution plans into the repo — with progress logs, decision logs, and known technical debt all versioned and co-located — is documented as a key enabler of agent reliability at OpenAI. This is the equivalent of your program/backlog layer being repo-resident, not external. [openai](https://openai.com/index/harness-engineering/)

### ADR Integration Into Agent Workflows

AI-enabled ADR enforcement is an emerging pattern where architectural decision records are stored in `docs/adrs/`, embedded into vector stores, and queried by agents during PR review. This is the closest current precedent to your ontology registry concept: a typed, queryable authority surface for architectural constraints. [linkedin](https://www.linkedin.com/pulse/from-adrs-action-embedding-architectural-decisions-dev-riaz-a-khan-jqnec)

### Prompt SDLC

The "Prompt SDLC" pattern — treating prompts as versioned, tested production artifacts rather than ad-hoc instructions — is documented as a core principle in serious agent harness design. This validates artifact-class separation as a direction, even if the full taxonomy isn't standardized. [linkedin](https://www.linkedin.com/posts/tommgomez_agent-harnesses-the-missing-layer-between-activity-7424459175507951616-1HpS)

***

## 5. Recent Product Changes That Matter

**OpenAI Codex (Feb 2026):** The desktop app launched in early February 2026, and GPT-5.3-Codex shipped the same week. Harness engineering was published February 11, 2026. The key change for your architecture: Codex now supports per-worktree isolated environments with ephemeral observability stacks, enabling agents to work on fully isolated app instances — this has direct implications for how you should think about harness isolation boundaries. [newsletter.pragmaticengineer](https://newsletter.pragmaticengineer.com/p/how-codex-is-built)

**OpenAI Codex CLI Skills:** The Codex team has built 100+ internal skills, and `AGENTS.md` has become a de facto cross-agent standard (the post notes Claude Code is "the only major agent not to use it"). If you're running multi-harness coordination across Claude Code and Codex, you now need to account for AGENTS.md as a parallel authority surface to CLAUDE.md. [newsletter.pragmaticengineer](https://newsletter.pragmaticengineer.com/p/how-codex-is-built)

**Claude Code MCP + Extension Layer (Dec 2025):** Claude Code now integrates 300+ external services via MCP protocol, with hooks for guaranteed shell command execution regardless of model behavior, and a skills system for domain expertise. This expands the harness surface you need to govern — MCP server configs are now part of your harness constitution. [introl](https://introl.com/blog/claude-code-cli-comprehensive-guide-2025)

**OpenAI Codex Context Compaction:** The `/compact` endpoint on the Responses API generates smaller representations of conversation history, replacing the old input to avoid quadratic inference costs. This is a product capability that changes how long-horizon handoffs should be structured — compacted context is now a first-class artifact type. [developers.openai](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide/)

**Gemini / Google AI Studio:** No major architectural-governance-relevant changes surfaced in the search results for this period.

***

## 6. Recommended Remediation Direction

Based on verified current evidence, the following adjustments strengthen your thesis:

1. **Constitution layer must be a table of contents, not a compendium.** The neocorpus is not the constitution — it is the deep-doctrine library the constitution points into. Your constitution file should be ~100 lines with explicit pointers, mechanically enforced cross-links, and a freshness linter. [openai](https://openai.com/index/harness-engineering/)

2. **Executive intention and program layers must be repo-resident, not mental.** Active intentions, priority compass (Rosetta Stone / Intent Compass), and backlog items should be checked-in markdown with canonical paths, not conceptually central but path-unresolved. This is the single most operationally important gap. [openai](https://openai.com/index/harness-engineering/)

3. **Per-harness playbooks should adopt the skills pattern.** Claude Code skills and Codex skills are the current standard for harness-specific doctrine. Each harness should have a `skills/` directory with named, invocable playbooks — not just narrative docs. [introl](https://introl.com/blog/claude-code-cli-comprehensive-guide-2025)

4. **Add AGENTS.md as a parallel authority surface to CLAUDE.md.** Since Codex uses AGENTS.md and it is now cross-agent standard, your multi-harness system needs to govern both surfaces explicitly — either through a shared pointer or explicit harness-specific versions. [newsletter.pragmaticengineer](https://newsletter.pragmaticengineer.com/p/how-codex-is-built)

5. **Artifact class law should cover at minimum: plans (active/completed), decisions (ADRs), prompts (versioned), outputs (generated reports), and runbooks (harness playbooks).** This is assembled from ADR-as-code practice, OpenAI's plans-as-artifacts pattern, and Prompt SDLC. [linkedin](https://www.linkedin.com/posts/tommgomez_agent-harnesses-the-missing-layer-between-activity-7424459175507951616-1HpS)

6. **Enforce everything mechanically.** Linters and CI jobs that validate knowledge-base cross-links and structure are not optional — they are what prevent the constitutional layer from rotting. [openai](https://openai.com/index/harness-engineering/)

***

## 7. Open Questions Still Requiring Experiment

- **How should compacted context (OpenAI `/compact` artifacts) be classified and stored?** These are a new artifact type that sits between a log and a handoff and has no established governance pattern yet. [developers.openai](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide/)

- **Can AGENTS.md and CLAUDE.md be unified under a single source-of-truth that renders to both formats?** This is the multi-harness constitution problem — no public solution exists yet.

- **What is the right granularity for harness-specific playbooks?** Codex uses 100+ skills internally, but the right decomposition for a sovereign personal system is unknown. Too fine = maintenance burden; too coarse = the monolithic-prompt failure mode. [newsletter.pragmaticengineer](https://newsletter.pragmaticengineer.com/p/how-codex-is-built)

- **How should ontology registry updates be triggered?** If the registry is a downstream projection from constitutional vocabulary, what event causes a registry update — a git commit? A CI job? An agent run? The event-driven multi-agent literature uses Kafka-style keyed partitioning for this, but the local-first equivalent is uncharted. [confluent](https://www.confluent.io/blog/event-driven-multi-agent-systems/)

- **What is the durable handoff format for stateless context across sessions?** Your CRUSH/nucleosynthesis effort created a neocorpus as a distilled doctrine layer — this is functionally equivalent to a compacted context artifact, but the session-boundary handoff format and its relationship to the live backlog is still architecturally unresolved.
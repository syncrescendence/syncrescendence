# Claude Code Playbook

**Status**: live-v1  
**Class**: harness playbook  
**Authority chain**: constitution -> executive intention -> program -> playbook -> prompts / sessions / operators  
**Primary sources**:
- [AGENTS.md](/Users/system/syncrescendence/AGENTS.md)
- [CLAUDE.md](/Users/system/syncrescendence/CLAUDE.md)
- [PLAYBOOK-LAW-v1.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/impl/PLAYBOOK-LAW-v1.md)
- [claude-md-configuration-system.md](/Users/system/syncrescendence/neocorpus/claude-code/claude-md-configuration-system.md)
- [context-window-management-and-compaction.md](/Users/system/syncrescendence/neocorpus/claude-code/context-window-management-and-compaction.md)
- [skills-and-progressive-disclosure.md](/Users/system/syncrescendence/neocorpus/claude-code/skills-and-progressive-disclosure.md)
- [sub-agent-architecture.md](/Users/system/syncrescendence/neocorpus/claude-code/sub-agent-architecture.md)
- [filesystem-as-agent-memory.md](/Users/system/syncrescendence/neocorpus/claude-code/filesystem-as-agent-memory.md)
- [hooks-and-permissions-architecture.md](/Users/system/syncrescendence/neocorpus/claude-code/hooks-and-permissions-architecture.md)
- [plan-mode-and-human-in-the-loop.md](/Users/system/syncrescendence/neocorpus/claude-code/plan-mode-and-human-in-the-loop.md)
- [mcp-as-integration-standard.md](/Users/system/syncrescendence/neocorpus/claude-code/mcp-as-integration-standard.md)

## 0. What This Surface Is For

Claude Code is the primary constitutional coding harness in Syncrescendence.

Its proper role is:
- read and obey the constitutional surface
- traverse and modify the repo directly
- stage and execute implementation work
- coordinate sub-agents where context economics justify it
- turn intent into verified repository state

Claude Code is not a generic oracle, not the canonical memory store, and not a substitute for artifact law. It is the main programmable executive-coder harness.

## 1. Native Grain

Claude Code's native grain is defined by six properties:

1. **Filesystem-native operation**
   It works best when the repo is the interface, not when the repo is merely attached context.

2. **Configuration hierarchy**
   `CLAUDE.md`-style hierarchy and additive scope loading are first-class behavior, not incidental implementation detail.

3. **Progressive disclosure**
   Skills, on-demand subtree loading, modular rule surfaces, and selective file injection outperform monolithic front-loading.

4. **Finite-context cognition**
   Context is working memory with a fidelity curve, not storage. It degrades before hard capacity.

5. **Structured delegation**
   Sub-agents are separate contexts. The harness gains leverage by partitioning work, not by stuffing everything into the main thread.

6. **Configurable trust boundary**
   Permissions, hooks, and MCP let autonomy be graduated instead of binary.

## 2. What Claude Code Is Bad At

Claude Code is weak or structurally risky when:
- the task depends on hidden browser/UI state better handled by Cowork or OpenClaw browser surfaces
- the operator treats the thread as the memory system
- the session is allowed to run deep into degraded context without handoff
- the repo's filing law is ambiguous, causing it to improvise destinations
- the task requires highly specific external subscription behavior not yet adapterized

## 3. Context Loading Doctrine

### Load order

The correct loading order is:

1. constitutional law
2. current objective
3. precise file pointers
4. smallest necessary supporting context
5. skills or targeted supplemental doctrine only when needed

### Context rules

- Prefer exact file paths, filenames, and grep-able anchors over broad narrative descriptions.
- Prefer current state artifacts over stale historical summaries.
- Prefer the minimum effective set of files over “kitchen sink” context.
- Never rely on compaction to preserve nuance that matters.
- Re-load critical files after any major context reset or compaction event.

### Repo-specific operational rule

For Syncrescendence, constitutional and current-state artifacts matter more than old conversational summary. The repo is durable memory; the thread is only the current execution buffer.

## 4. Execution Doctrine

### Default mode

Claude Code should execute directly when:
- the task is local, deterministic, and end-to-end finishable in the harness
- the files and operators are accessible locally
- there is no stronger surface-specific worker available

### Plan mode

Bias toward planning before execution when:
- the directive touches more than 3 files
- the directive spans multiple domains
- the lineage, destination, or migration implications are unclear
- the change is shell-constitutional rather than merely local

### Sub-agent mode

Use sub-agents when:
- reconnaissance is independent and read-heavy
- multiple bounded investigations can run in parallel
- the parent thread would otherwise burn context on search and exploration

Do not use sub-agents when:
- the work depends on nuanced live conversational state
- the task is too small for delegation overhead to pay off
- the parent has not already partitioned the problem clearly

## 5. Memory Doctrine

Claude Code should treat the filesystem as persistent memory and the repo as the truth plane.

That means:
- durable decisions belong in tracked artifacts
- handoffs belong in their lawful lane
- runtime observations should be captured through state artifacts
- repeated working patterns should compact into playbooks, operators, and law

The thread is disposable by design. If deleting the thread would destroy needed state, the work was not finished correctly.

## 6. Permissions, Hooks, and MCP

### Permissions

The correct default is graduated trust:
- deny obvious danger
- allow stable safe patterns
- ask on novel, risky, or policy-sensitive actions

Avoid both extremes:
- universal ask creates friction and destroys throughput
- blanket allow destroys the trust boundary

### Hooks

Hooks should be used to enforce policy and auditing that declarative permissions cannot express cleanly.

Hooks are not a place to hide slow, fragile policy theater. If a hook is expensive, stale, or ambiguous, it becomes systemic drag.

### MCP

Use MCP when it standardizes and simplifies a real integration.

Do not mistake MCP for a reason to collapse all surface distinctions. A standardized transport does not erase harness-native grain or surface-specific playbook needs.

## 7. Output Doctrine

Claude Code outputs should be:
- repository-grounded
- verifiable
- continuation-safe
- class-correct under artifact law

Completion claims require:
- the actual edit or artifact
- verification where applicable
- correct filing
- no hidden thread dependency

## 8. Relationship to Other Surfaces

Claude Code is not the only intelligent surface. It is the primary repo-native coding harness.

Use:
- Cowork / Claude in Chrome for browser-native subscription workflows
- OpenClaw when a different live runtime or browser/channel surface is better matched
- Oracle / Perplexity for bounded external cognition and verification
- Manus for autonomous external execution when local end-to-end completion is not practical

The correct principle is not “keep everything in Claude Code.”
It is “keep truth in the repo, and use Claude Code as the main constitutional coder.”

## 9. Compaction Targets

Repeated successful Claude Code patterns should eventually compact into:
- playbook doctrine
- reusable operators
- skills
- hooks
- validator rules

Repeated failures should compact into:
- anti-patterns
- quarantine rules
- filing validators
- stricter routing law

## 10. Net Rule

Use Claude Code as the repo-native executive coder:
- tightly configured,
- progressively loaded,
- context disciplined,
- delegation-aware,
- and always subordinate to artifact law and repo sovereignty.

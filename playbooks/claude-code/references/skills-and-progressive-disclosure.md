# Skills and Progressive Disclosure

A skill in Claude Code is a reusable block of context — instructions, constraints, workflows, or domain knowledge — that loads on-demand when invoked rather than occupying context permanently. Skills implement the progressive disclosure pattern: instead of front-loading every possible instruction into the context window at session start, the system reveals information precisely when it becomes relevant. This is the architectural answer to a fundamental tension: agents need extensive knowledge to operate effectively, but context windows are finite and degrade under load. Skills resolve this tension by making knowledge available without making it present.

---

## Core Architecture

### What Skills Are

A skill is a markdown file (`.md`) that loads on-demand when invoked. The specific mechanics — storage at `.claude/skills/`, project scope overriding user scope, and the exact invocation paths — are not directly established by this entry's cited sources. [synthesis — the concrete file locations and scope-override mechanics are not established by `10032`, `00419`, or `00001` as cited]

Each skill file contains natural-language instructions that the agent treats as behavioral directives for the duration of the task. A skill might describe a code review methodology, a deployment checklist, a refactoring protocol, or domain-specific knowledge about a particular subsystem. The format is deliberately simple — markdown, not code — because the consumer is a language model, not a runtime.

### Skill Scopes

Skills exist at two scopes. The specific file locations and scope-override behavior below are not directly established by the cited sources — they are consistent with Claude Code's general architectural patterns but should be treated as synthesis. [synthesis — not documented in cited sources]

| Scope | Location | Availability |
|-------|----------|-------------|
| **Project** | `.claude/skills/` | Available in this repository |
| **User/Personal** | `~/.claude/skills/` | Available across all repositories |

Project-level skills are version-controlled and team-shared. Personal skills reflect an individual developer's workflows and preferences. When both levels define a skill with the same name, the project-level skill is expected to take precedence.

### Invocation Patterns

Skills can be invoked through multiple paths:

- **Slash commands**: The operator types `/skill-name` to explicitly load a skill. This is the sovereign-facing invocation — the human decides when the skill is needed.
- **Programmatic invocation**: The Skill tool is called by the agent or by another tool, loading the skill's content into context automatically. This is the agent-loop invocation — the system decides when the skill is needed.
- **Chained invocation**: A hook or workflow triggers a skill as part of a larger pipeline. This is the infrastructure invocation — the process decides when the skill is needed.

The distinction between sovereign-facing and agent-loop invocation is architecturally significant. Sovereign-facing skills are designed for human operators: they present information, request confirmation, and guide interactive workflows. Agent-loop skills are designed for autonomous execution: they provide constraints, protocols, and decision criteria that the agent applies without human interaction.

### Progressive Disclosure Pattern

Progressive disclosure is a design principle borrowed from UI design: reveal complexity gradually, showing only what is needed at the current level of engagement. In Claude Code, this principle manifests at multiple levels:

1. **CLAUDE.md hierarchy**: Universal instructions load at session start; subdirectory instructions load on file access.
2. **Skills**: Domain knowledge loads on explicit or programmatic invocation.
3. **MCP servers**: External tool capabilities are available but not active until needed.
4. **Sub-agents**: Specialized knowledge is held in separate context windows, not the main thread.

Skills are the most explicit implementation of progressive disclosure. The operator or agent makes a conscious decision to load specific knowledge at a specific moment. The overhead is zero before that moment and bounded after it (limited to the skill's content size).

The token economics principle is clear: skills not loaded consume no tokens. The specific 30-skills × 500-tokens example and derived 10x savings calculation are not provided by `10032` (which is a short video description without these numbers). [synthesis — not directly stated in cited sources]

---

## Key Insights

### The Anti-Shelfware Rule

The Syncrescendence constellation discovered through operational experience that skills proliferate faster than they are used. The anti-shelfware rule addresses this: every skill with active status must have a non-empty "Wired To" field — it must be connected to a hook, a chain, an agent-loop trigger, or a slash command. Skills with empty wiring after a 30-day review period are demoted to dormant status.

This rule encodes a hard-won insight: a skill that exists but is never invoked is worse than no skill at all. It consumes maintenance attention, creates an illusion of capability, and clutters the skill registry. The wiring requirement forces every skill to justify its existence through actual use.

### Bifurcation: Agent vs. Sovereign

Skills naturally divide into two categories based on their primary consumer:

| Category | Consumer | Design Principle | Loading |
|----------|----------|-----------------|---------|
| **Agent skills** | Automation/agent-loops | Always available, loaded programmatically | Automatic when relevant |
| **Sovereign skills** | Human operator | Heuristically minimal, invoked by slash command | Manual on demand |
| **Both** | Either | Designed for dual use | Both paths |

This bifurcation matters because agent skills and sovereign skills have different design requirements. An agent skill should be precise, unambiguous, and self-contained — the agent cannot ask clarifying questions. A sovereign skill can be more open-ended, presenting options and requesting choices. Treating all skills as equivalent leads to agent skills that are too vague for automation and sovereign skills that are too rigid for interactive use.

### Skill as Context Engineering

The deeper insight behind skills is that they are a form of **context engineering** — the deliberate construction of the information environment in which the agent operates. Rather than hoping the agent has the right knowledge from its training data, skills inject specific, verified, project-relevant knowledge at the moment of need.

This is particularly powerful for:
- **Institutional knowledge**: How this team deploys, what conventions this codebase follows, which patterns are prohibited
- **Domain expertise**: Security audit checklists, accessibility requirements, regulatory compliance steps
- **Workflow protocols**: Session handoff procedures, triangulation playbooks, verification checklists

None of this knowledge exists in the model's training data in a project-specific form. Skills bridge the gap between general model capability and specific project needs.

### Consolidation and the Registry

As skill collections grow, overlap and redundancy emerge. Multiple skills may cover adjacent concerns with different levels of specificity, or the same concern from different perspectives. Consolidation reduces this redundancy through mode-parameterized wrappers — a single skill that handles multiple related modes instead of separate skills for each mode.

The Syncrescendence constellation tracks this through a formal skill registry (`ARCH-SKILL_REGISTRY.md`) that records every skill's provenance, security status, bifurcation category, pipeline stage assignment, and wiring state. At peak, the registry contained 264 skills; consolidation reduced this to approximately 196 effective skills. The registry is a living document, not a static manifest — it requires ongoing maintenance to remain accurate.

### Security Considerations

Skills are executable instructions loaded into an agent's context with directive authority. A malicious or compromised skill can instruct the agent to perform harmful actions. The permission system provides a backstop (deny rules block dangerous actions regardless of instruction source), but skill provenance matters.

The Syncrescendence constellation's security audit reviewed 230 skills, flagging 119 (primarily false positives from URLs and credential references in skill text) and clearing 111. The audit revealed that skill text frequently contains references to paths, URLs, and credential names that trigger security scanners despite being documentation rather than live credentials.

---

## Anti-Patterns and Failure Modes

### The Skill Graveyard

Creating skills for every conceivable task, then never invoking most of them. The skill registry fills with dormant entries that create maintenance burden and navigation overhead. The anti-shelfware rule exists specifically to prevent this pattern, but it requires active enforcement — a defined review cadence and a willingness to cull unused skills.

### Skill as Documentation

Writing skills that describe how something works rather than instructing the agent what to do. A skill is a behavioral directive, not a reference document. "The authentication system uses JWT tokens with a 24-hour expiry" is documentation. "When modifying authentication code, ensure JWT token expiry remains set to 24 hours and add a test verifying the expiry duration" is a skill. The former informs; the latter directs.

### Over-Disclosure

Loading too many skills simultaneously, negating the context savings of progressive disclosure. If every task triggers five skills, the per-session cost approaches the front-loading cost that progressive disclosure was designed to avoid. Skills should be invoked surgically — the minimum set needed for the current task.

### Stale Skills

Skills that reference outdated conventions, deprecated APIs, or removed file paths. Unlike CLAUDE.md (which the operator sees at session start), skills are invisible until invoked — and may not be invoked for weeks or months. Stale skills inject incorrect instructions at the worst possible moment: when the agent is actively performing the task the skill governs.

### Missing Wiring

Skills that are created and documented but never connected to an invocation path. They exist in the filesystem but no hook triggers them, no agent-loop references them, and no operator knows their slash-command name. They are capabilities in theory and dead weight in practice.

---

## Implications

Skills and progressive disclosure represent a maturation in how agent systems manage knowledge. The naive approach — load everything, hope the model sorts it out — fails at scale because context windows are finite and attention degrades with length. The engineered approach — load precisely what is needed, when it is needed — produces agents that are simultaneously more knowledgeable (they have access to extensive skill libraries) and more focused (they operate on compact, relevant context).

For teams, skills are the mechanism by which institutional knowledge becomes portable across developers and sessions. A skill encoding the team's deployment protocol works identically whether invoked by a senior engineer or a new hire, whether in a Monday morning session or a Friday evening hotfix. This is organizational knowledge operationalized — not written in a wiki and forgotten, but loaded into the agent and executed.

The progressive disclosure pattern extends beyond skills to a broader architectural principle: information should flow to the agent at the rate it can be usefully consumed, not at the rate it can be produced. This principle governs CLAUDE.md (layered, on-demand), sub-agents (isolated, summary-returning), MCP servers (available, not always active), and skills (registered, selectively invoked). Together, these mechanisms create an information architecture that respects the agent's cognitive constraints while maximizing its access to relevant knowledge.

---

## Obsolescence and Supersession

### Pre-Skills: The Kitchen Sink Session

Before skills and progressive disclosure, the standard approach to giving an agent extensive behavioral guidance was to load all instructions at session start — a single large CLAUDE.md or equivalent system prompt injection. This approach assumed that more context is always better, and that the overhead of loading unused instructions was acceptable.

The assumption broke under two conditions: (1) the context window filled before the work began, and (2) irrelevant instructions increased noise and reduced the agent's focus on the current task. The anti-pattern now called "Kitchen Sink" (documented in the CLAUDE.md Configuration System entry) was not originally recognized as an anti-pattern — it was the default approach before progressive disclosure existed as an alternative.

### The Skill Graveyard as a Phase-One Phenomenon

The Syncrescendence constellation's experience — a skill registry growing to 264 entries, requiring consolidation to ~196 with a formal anti-shelfware rule — documents a supersession arc that other teams will follow. Phase one: skills are created enthusiastically for every conceivable task. Phase two: most skills go unused. Phase three: the graveyard problem forces an audit and a maintenance protocol.

The anti-shelfware rule (every active skill must have a documented invocation path) is the institutionalized lesson from phase-two failure. Teams that understand this arc can skip phase two by building the rule in from the start.

### Progressive Disclosure as Correction to Monolithic Loading

The skills mechanism emerged as a correction to the monolith problem in the same way subdirectory CLAUDE.md files corrected the monolithic root CLAUDE.md. Both represent the same insight applied twice: front-loading all context is wasteful when only a fraction is relevant to the current task. The progressive disclosure principle was discovered through failure (sessions exhausting context before completing tasks) and encoded into the architecture (on-demand loading, selective skill invocation) as the correction.

This is the standard supersession form for Claude Code architectural patterns: a naive approach that works for small cases, a failure mode that appears at scale, a structural correction that encodes the lesson.

---

## Syncrescendence Operational Context

The following claims derive from the constellation's operational history and skill registry (`corpus/claude-code/00419.md`), not from generalizable external sources about Claude Code:
- The anti-shelfware rule, bifurcation schema, wiring requirement, and consolidation logic (these are Syncrescendence-internal registry policies documented in `00419`)
- The 230-skill audit with 119 flagged and 111 cleared (these exact counts are from the Syncrescendence's own `ARCH-SKILL_REGISTRY.md` as referenced in `00419`)
- The registry containing 264 skills at peak, reduced to ~196 effective skills after consolidation

## Source Provenance

| Corpus File | Content |
|-------------|---------|
| `corpus/claude-code/10032.md` | Progressive disclosure video — token efficiency, filesystem-based context, skill implementation |
| `corpus/claude-code/00419.md` | Skill registry — anti-shelfware rule, bifurcation schema, consolidation groups, security audit |
| `corpus/claude-code/10411.md` | Slack integration — skills as organizational capability, configuration as multiplier |
| `corpus/claude-code/00001.md` | Customization thread — plugins, skills, agents, hooks as unified customization surface |

# CLAUDE.md Configuration System

CLAUDE.md is the behavioral contract between a developer and Claude Code. It is not documentation, not commentary, not a suggestion box. It is a configuration file written in natural language that governs how the agent behaves in a given project, directory, or across all projects for a given user. The system loads configuration from multiple scopes with defined precedence, combines rather than replaces across levels, and supports on-demand loading that scales to monorepos without upfront context cost. Understanding this system is prerequisite to effective Claude Code operation — an agent without proper CLAUDE.md configuration is an agent operating on defaults and vibes.

---

## Core Architecture

### The Scope Hierarchy

Claude Code loads configuration from six distinct scopes, each with a specific purpose and shareability model:

| Scope | Location | Purpose | Shareability |
|-------|----------|---------|--------------|
| **Managed/Enterprise** | `/Library/Application Support/ClaudeCode/` (macOS), `/etc/claude-code/` (Linux) | Organization-wide policies enforced by IT | Admin-controlled, cannot be overridden |
| **User** | `~/.claude/CLAUDE.md` | Personal preferences across all projects | Per-developer, not version-controlled |
| **Project** | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Repository-specific guidance | Version-controlled, team-shared |
| **Rules** | `.claude/rules/*.md` | Modular thematic breakdowns | Version-controlled, conditional activation |
| **Local** | `./CLAUDE.local.md` | Per-developer overrides | Gitignored by convention |
| **Subdirectory** | `subdirectory/CLAUDE.md` | Path-specific context | Loaded on-demand when accessing subtree |

### Precedence Dynamics

The scopes combine additively — they do not replace each other. More specific scopes override more general ones only when there is a direct conflict. In practice, this means a project-level instruction and a user-level instruction on different topics both take effect, while a project-level instruction on the same topic as a user-level instruction takes precedence.

There is a documented ambiguity in how the community and official sources describe this hierarchy. The community-derived ordering (Enterprise > Project > Rules > User > Local) conflates two distinct hierarchies: the memory/instruction hierarchy and the settings hierarchy. Official documentation frames settings precedence as "Managed > CLI args > Local > Project > User." The distinction matters because settings (model selection, permissions, feature flags) and instructions (behavioral guidance, coding standards, project context) follow different precedence paths through the same scope system.

For behavioral instructions — the content most operators care about — the practical rule is: everything combines, conflicts resolve toward the more specific scope, and Enterprise/Managed scope overrides everything.

### On-Demand Loading

Subdirectory CLAUDE.md files are not loaded at session start. They load lazily when Claude Code accesses files within that subtree. This is a critical architectural decision for monorepos: a repository with 50 subdirectory CLAUDE.md files pays zero context cost for the 49 it never touches in a given session.

The loading trigger is file access within the subtree. The sources support on-demand subtree loading, but the stronger claim that directory listing specifically does not trigger loading (while file reads do) is not directly established in the cited sources. [synthesis — not directly stated in sources]

### Import Syntax and Depth

Files can reference other files using `@path/to/file.md` syntax, creating a graph of configuration dependencies. A maximum import depth of 5 hops is reported by multiple sources but marked as unverified in official documentation. The practical implication is clear regardless of the exact limit: deeply nested import chains are fragile and should be avoided. A flat or shallow import structure is both more reliable and easier to reason about.

---

## Key Insights

### CLAUDE.md as Behavioral Contract

The most productive mental model for CLAUDE.md is not "configuration file" or "documentation" but **behavioral contract**. It specifies what the agent will and will not do, how it will do it, and what constitutes correct behavior in the project's context. This framing has several consequences:

- Instructions should be imperative, not descriptive. "Run tests before committing" not "Tests are important in this project."
- Constraints should be explicit, not implied. "Never modify files in /vendor" not "The vendor directory contains third-party code."
- The contract is enforceable — the agent treats CLAUDE.md instructions with the same weight as system prompt instructions.

### The Monorepo Pattern

For large repositories with distinct modules, the combination of project-level CLAUDE.md and subdirectory CLAUDE.md files creates a natural configuration cascade:

- **Project root**: Universal standards — commit message format, testing requirements, language style, protected directories.
- **Subdirectory level**: Module-specific context — API conventions, database schemas, deployment targets, framework-specific patterns.

The on-demand loading ensures that an agent working on the frontend module receives frontend-specific instructions without being burdened by backend-specific context, and vice versa. This is progressive disclosure applied to configuration.

### Rules Files as Modular Configuration

The `.claude/rules/*.md` pattern enables thematic decomposition of configuration. Instead of a monolithic CLAUDE.md that grows unwieldy, teams can maintain focused rule files: `security-rules.md`, `testing-standards.md`, `api-conventions.md`. Each activates independently based on context.

This modularity also supports conditional activation — rules that apply only when certain conditions are met. A security-focused rules file might activate only when the agent is working in authentication-related code, keeping its instructions out of unrelated contexts.

### Configuration as Team Coordination

When agent teams are active, every teammate automatically loads the project's CLAUDE.md [supported by `corpus/claude-code/00212.md`, not in this entry's primary cited source set]. This makes CLAUDE.md the primary coordination mechanism for multi-agent work. Module boundaries declared in CLAUDE.md determine how the team lead splits work across teammates. Coding standards in CLAUDE.md ensure consistent output across parallel agents. Protected directories in CLAUDE.md prevent edit collisions.

The implication is that investing in CLAUDE.md quality has multiplicative returns: it improves not just single-agent sessions but every parallel agent session in the project.

---

## Anti-Patterns and Failure Modes

### The Phantom Path

Referencing files or directories in CLAUDE.md that do not exist on disk. This causes silent failure — the agent reads the instruction, attempts to follow it, and either hallucinate the referenced content or silently ignore the instruction. There is no error message. The Syncrescendence constellation discovered this failure mode through 16 consecutive sessions (CC52-CC57) of degraded performance before identifying phantom path references as the cause.

Prevention: run `make validate` or equivalent path-checking after every CLAUDE.md modification. Every path mentioned in configuration must resolve to an actual file or directory.

### The Kitchen Sink

Loading every possible instruction, context, and constraint into the root CLAUDE.md. This consumes substantial context at session start, leaving less room for actual work. It also violates the progressive disclosure principle — the agent receives information about modules it will never touch in this session.

The corrective is decomposition: root CLAUDE.md contains only universal instructions, subdirectory files contain module-specific context, and rules files handle thematic concerns. Total information may be the same, but the per-session cost is dramatically lower.

### Editing Generated Files

In systems where CLAUDE.md is generated from source files (as in the Syncrescendence's `AGENTS.md` + `*-EXT.md` > `make configs` > `CLAUDE.md` pipeline), editing the generated CLAUDE.md directly creates a divergence that will be overwritten on the next config generation. The source files are the authority; the generated file is an artifact.

This failure mode is particularly insidious because the edit appears to work — the agent reads the modified CLAUDE.md and follows the new instructions — until the next config regeneration silently reverts the change.

### Conflating Memory and Settings

Treating CLAUDE.md as both an instruction file and a settings file without understanding that these follow different precedence paths. User-level memory (behavioral preferences) and user-level settings (model selection, permissions) resolve differently in the hierarchy. Mixing them in a single mental model leads to confusion about why certain instructions are "ignored" — they may be overridden by a settings-level precedence rule, not by an instruction-level one.

### Stale Configuration

CLAUDE.md that describes a project's architecture, conventions, or directory structure as it existed six months ago. The agent follows outdated instructions faithfully, producing code that conforms to an obsolete standard. Configuration files require maintenance — they are living documents, not set-and-forget artifacts.

---

## Implications

The CLAUDE.md system transforms Claude Code from a generic AI assistant into a project-aware, team-aligned development partner. The quality of this transformation is directly proportional to the quality of the configuration. A well-maintained CLAUDE.md hierarchy produces an agent that understands module boundaries, follows project conventions, respects protected zones, and coordinates effectively with parallel agents. A neglected or absent CLAUDE.md produces an agent operating on model defaults — capable but unaligned with the project's specific needs.

For organizations, the managed/enterprise scope creates a governance layer: security policies, compliance requirements, and coding standards can be enforced across every Claude Code session in the organization without relying on individual developer configuration. This is the mechanism by which institutional knowledge becomes agent behavior.

The deeper implication is architectural: CLAUDE.md is the interface between human organizational knowledge and machine execution. It is where project wisdom becomes operational constraint. Every team investing in Claude Code should invest proportionally in their CLAUDE.md configuration — it is the highest-leverage artifact in the entire workflow.

---

## Syncrescendence Operational Context

The following claims derive from the constellation's operational history and constitutional documents (AGENTS.md, CLAUDE.md, memory/), not from external corpus sources:
- The Syncrescendence constellation discovering phantom path failure through 16 consecutive sessions (CC52-CC57) of degraded performance
- The `make validate` path-checking ritual as the prevention method
- The `AGENTS.md` + `*-EXT.md` > `make configs` > `CLAUDE.md` pipeline as the Syncrescendence's config generation pattern

## Source Provenance

| Corpus File | Content |
|-------------|---------|
| `corpus/claude-code/08764.md` | Unified research synthesis — scope hierarchy, precedence dynamics, import depth, on-demand loading |
| `corpus/claude-code/10032.md` | Progressive disclosure — CLAUDE.md as mechanism for scalable context management |
| `corpus/claude-code/00001.md` | Customization thread — configuration, permissions, rules, plugins, custom agents |

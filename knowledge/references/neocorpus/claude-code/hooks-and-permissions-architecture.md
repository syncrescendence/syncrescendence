# Hooks and Permissions Architecture

Claude Code's permission system is a layered security perimeter that governs every action the agent can take. At its core is a three-state evaluation order — deny, allow, ask — that determines whether a given tool invocation is blocked, permitted silently, or escalated to the operator for approval. Hooks provide an interception layer that fires before the declarative permission rules are evaluated, enabling custom validation, transformation, and auditing of agent actions. Together, permissions and hooks constitute the trust boundary between autonomous agent execution and human oversight. Understanding this architecture is essential for anyone operating Claude Code beyond default settings — it is the mechanism by which operators grant autonomy without surrendering control.

---

## Core Architecture

### The Permission Evaluation Order

Every tool invocation in Claude Code passes through a deterministic evaluation sequence:

1. **Deny rules** — evaluated first. If any deny rule matches, the action is blocked. No further evaluation occurs.
2. **Allow rules** — evaluated second. If an allow rule matches and no deny rule blocked, the action proceeds silently.
3. **Ask (default)** — if no deny or allow rule matches, the operator is prompted for approval.

This ordering is security-critical. Deny takes absolute precedence, ensuring that prohibited actions cannot be permitted by an overly broad allow rule. The default state is "ask" for anything not explicitly configured — however, Claude Code ships with a small set of pre-approved safe commands that do not require approval, so not literally every action requires approval absent configuration. Autonomy beyond the conservative safe-command defaults is opt-in.

### Permission Scopes

Permissions are declared at multiple scopes that mirror the CLAUDE.md configuration hierarchy:

| Scope | Location | Controlled By |
|-------|----------|---------------|
| **Managed/Enterprise** | System-level config | IT administrators |
| **Project** | `.claude/settings.json` | Version-controlled, team-shared |
| **User** | `~/.claude/settings.json` | Individual developer |

More restrictive scopes override less restrictive ones. An enterprise deny rule cannot be overridden by a project allow rule. This creates a governance hierarchy: organizations can enforce security baselines that individual developers cannot relax.

### Permission Granularity

Permissions target specific tool invocations with pattern matching. The format is `Tool(pattern)`:

- `Bash(git status:*)` — allow any git status command
- `Bash(rm -rf:*)` — could be denied to prevent destructive deletions
- `Bash(gh issue view:*)` — allow GitHub CLI issue viewing

The pattern matching supports wildcards, enabling both precise and broad permission grants. The `/permissions` command provides an interactive interface for reviewing and modifying the current permission set.

### Pre-Approved Defaults

Claude Code ships with a small set of pre-approved safe commands — read-only operations, standard git commands, and other actions deemed risk-free. Everything beyond this minimal set requires either explicit operator approval per invocation or a configured allow rule.

The conservative default is deliberate. The cost of an unnecessary approval prompt is a momentary interruption. The cost of an unauthorized destructive action is potentially catastrophic. The system optimizes for safety at the expense of convenience, placing the burden of granting autonomy on the operator.

### Hooks as Interception Layer

Hooks fire before the declarative permission rules are evaluated. They are custom code (typically shell scripts or executables) that intercept tool invocations and can:

- **Block** the invocation (return a non-zero exit code)
- **Allow** the invocation (return zero with an allow signal)
- **Transform** the invocation (modify the command before execution)
- **Audit** the invocation (log the action without modifying it)
- **Notify** on invocation (trigger external notifications)

Hooks receive the full invocation context: tool name, arguments, working directory, and session metadata. This enables arbitrarily complex validation logic that the declarative deny/allow/ask system cannot express.

Common hook applications include:
- Custom notification systems (desktop alerts when long operations complete)
- Command sanitization (stripping dangerous flags before execution)
- Audit logging (recording every action to a persistent log)
- Integration gates (checking external system state before permitting actions)
- Format enforcement (validating commit messages, branch names, or file formats)

### MCP Scope-Based Precedence

MCP (Model Context Protocol) server permissions follow their own scope-based precedence: **Local > Project > User**. This means a project-level MCP server configuration overrides a user-level one for the same server name. Enterprise `managed-mcp.json` provides an override layer above all three.

MCP permissions interact with the tool permission system: even if an MCP server is configured and available, individual tool invocations through that server still pass through the deny/allow/ask evaluation. MCP configuration determines which servers are available; tool permissions determine which actions through those servers are allowed.

---

## Key Insights

### The Trust Gradient

The permission system implements a trust gradient from zero-trust (deny everything, ask about everything) to high-trust (allow broad categories, deny only specific dangers). Operators move along this gradient by adding allow rules as they gain confidence in the agent's behavior within their specific project context.

The optimal position on the gradient depends on the risk profile:
- **Exploratory/research sessions**: High trust. Allow broad filesystem access and command execution. The cost of mistakes is low.
- **Production codebases**: Moderate trust. Allow standard development commands, deny destructive operations, ask about unfamiliar patterns.
- **Security-sensitive environments**: Low trust. Deny by default, allow only verified safe operations, require approval for anything novel.

The system supports this gradient without reconfiguration between modes — the same permission architecture serves all positions by adjusting the ratio of deny/allow/ask rules.

### Hooks as Organizational Policy

While declarative permissions express simple allow/deny logic, hooks express organizational policy. A hook can enforce that all commits include a ticket reference. A hook can verify that no secrets appear in staged files. A hook can check that deployments only proceed during approved maintenance windows. These policies are too complex for pattern-matching rules but straightforward in executable code.

For teams, hooks committed to version control become shared policy enforcement. Every developer running Claude Code on the project inherits the same hooks, ensuring consistent behavior regardless of individual permission configurations.

### The Prompt Injection Defense

The permission system serves a second, less obvious purpose: defense against prompt injection attacks. If a malicious file's content is read into context and attempts to instruct the agent to perform harmful actions, the permission system blocks those actions regardless of the instruction source. A deny rule on `Bash(rm -rf:*)` protects against both accidental operator commands and injected malicious instructions.

Claude Code combines the permission system with static analysis and sandboxing to create a multi-layer defense. Permissions are the human-configurable layer; static analysis detects suspicious patterns in commands; sandboxing restricts the execution environment. No single layer is sufficient; the combination provides defense in depth.

### Progressive Autonomy

A natural workflow for a new Claude Code deployment is to incrementally expand permissions as confidence grows. The day-1 / week-1 / month-1 rollout framing below is advisory synthesis rather than a documented source-backed Claude Code pattern; it is consistent with the general principle in the sources but not directly stated. [synthesis — not directly stated in cited sources]

1. **Day 1**: Default permissions. Approve unfamiliar actions manually. Observe what the agent does.
2. **Week 1**: Identify frequently approved safe actions. Add allow rules for these. Add deny rules for anything that should never occur.
3. **Month 1**: The permission set stabilizes. Most routine actions are allowed, dangerous actions are denied, and only novel or unusual actions trigger prompts.
4. **Ongoing**: Hooks codify organizational policy. The permission set evolves as the project's needs change.

This progression benefits from starting conservatively — the operator can observe what needs restricting before expanding autonomy.

---

## Anti-Patterns and Failure Modes

### Allow-All Syndrome

Setting overly broad allow rules to eliminate approval prompts. `Bash(*)` allows every shell command without scrutiny. This is convenient until the agent executes a destructive command that the operator would have caught with a moment's review. The correct response to excessive prompts is targeted allow rules for specific safe patterns, not a blanket override.

### Deny Rule Gaps

Relying solely on deny rules to define the security perimeter. Deny rules protect against known threats; they cannot protect against unknown ones. The three-state system (deny/allow/ask) ensures that anything not explicitly allowed or denied falls through to human review. Removing the ask layer by making everything either denied or allowed eliminates the safety net for unexpected actions.

### Stale Hooks

Hooks that reference external systems, file paths, or APIs that no longer exist. A hook that fails to execute (error, timeout, unreachable endpoint) may either block all actions (fail-closed) or permit all actions (fail-open), depending on implementation. Hooks require the same maintenance discipline as any other infrastructure code.

### Scope Confusion

Configuring permissions at the wrong scope. A user-level allow rule intended for one project applies to all projects. A project-level deny rule unintentionally blocks a teammate's legitimate workflow. Understanding which scope governs which context is essential for correct permission configuration.

### Hook Overhead

Complex hooks that introduce significant latency to every tool invocation. Hooks fire synchronously before each action; a hook that makes a network call or performs expensive computation adds that latency to every single tool use. Hooks should be fast by default, with expensive operations reserved for high-risk actions.

---

## Implications

The permissions and hooks architecture is the mechanism by which Claude Code transitions from a supervised tool to a semi-autonomous agent. Without it, operators face a binary choice: fully supervised (approve every action) or fully autonomous (trust everything). The layered system enables a nuanced middle ground where routine work proceeds autonomously while novel, risky, or policy-sensitive actions receive human oversight.

For organizations, the enterprise managed scope and version-controlled hooks create a governance framework for AI-assisted development. Security policies, compliance requirements, and operational standards can be encoded as permissions and hooks that apply uniformly across every Claude Code session in the organization. This transforms individual tool configuration into institutional capability.

The deeper implication is philosophical: the permission system embodies a theory of trust between humans and AI agents. Trust is not binary (on/off) but graduated (deny/allow/ask). Trust is not static but progressive (operators learn, permissions evolve). Trust is not universal but contextual (different projects, different risk profiles, different permission sets). This nuanced trust model is a prerequisite for deploying autonomous agents in environments where the consequences of mistakes are real.

---

## Obsolescence and Supersession

### Pre-Hooks: Purely Declarative Permissions

Before hooks, the permission system was purely declarative: deny/allow/ask rules evaluated against tool invocations. This system expressed what was permitted but had no mechanism to express how permissions should be enforced, under what conditions, or with what validation logic. The assumption: declarative rules are sufficient to govern agent behavior.

This assumption held for simple use cases. It broke under organizational requirements: "commits must include a ticket reference" cannot be expressed as a deny/allow/ask pattern. "No secrets in staged files" requires reading file content, not just matching a tool name. "Deployments only during maintenance windows" requires checking external system state. These policy-level requirements have irreducible conditional logic that pattern-matching rules cannot encode.

Hooks are the correction: an interception layer that fires before declarative rules, enabling executable policy alongside declarative policy. The combination covers the full space of organizational requirements that neither alone could address.

### The Sandbox Runtime Addition

The `corpus/claude-code/00001.md` source documents an opt-in sandbox runtime (`github.com/anthropic-experimental/sandbox-runtime`) introduced via the `/sandbox` command. This represents a further supersession within the permission system: from permission rules governing what the agent requests, to a sandbox layer governing what the underlying execution environment allows.

The sandbox approach embodies a different security assumption: rather than trusting that the permission evaluation correctly identifies all dangerous actions, the sandbox restricts the execution environment so that even unpermitted actions cannot cause damage. Defense-in-depth rather than defense-by-rules.

### The Audit Maturation Curve

The `00001.md` source describes a progression in how operators use the permission system: from manual approval of every novel action (early use, high friction), to targeted allow rules for safe patterns (reduced friction), to hooks encoding organizational policy (institutional maturity). This is not just a workflow pattern — it is a maturation arc that reflects changing assumptions about what the agent can be trusted to do.

Early Claude Code deployment assumed zero trust: approve everything. Mature deployment assumes calibrated trust: a permission configuration that reflects months of observed agent behavior. The system was designed to support both ends of this arc, but the path from one to the other requires deliberate configuration investment.

---

## Source Provenance

| Corpus File | Content |
|-------------|---------|
| `corpus/claude-code/08764.md` | Unified research synthesis — permission evaluation order, scope precedence, MCP scope interaction |
| `corpus/claude-code/00001.md` | Customization thread — permissions interface, pre-approved commands, hooks, plugins |
| `corpus/claude-code/10411.md` | Slack integration — configuration investment, permission system as organizational leverage |

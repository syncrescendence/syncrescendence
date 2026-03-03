# Plan Mode and Human-in-the-Loop

Plan Mode is Claude Code's mechanism for enforcing exploration before execution. When activated, the agent shifts from its default mode of reading, reasoning, and immediately writing files to a deliberate workflow: inventory the relevant code, map dependencies and implications, propose a structured plan, and wait for human approval before making any changes. It is the architectural expression of a principle that predates AI agents entirely — measure twice, cut once.

---

## Core Architecture

### What Plan Mode Actually Does

When Plan Mode is engaged, Claude Code shifts to an exploration-before-execution mode. The specific mechanics — whether write tools are literally suppressed at the permission level, and the exact output contract — are not directly documented in the cited sources. The operational description below is synthesis consistent with the sources. [synthesis — the mechanical detail of write-tool suppression and output contract is not established in `00025`, `10825`, `08764`, or CLAUDE.md as cited]

- **Read tools remain fully available.** The agent can read files, search the codebase, run grep, inspect git history, and gather any information it needs.
- **Write tools are not engaged during planning.** The agent focuses on understanding and planning rather than making changes.
- **The output is a plan.** Instead of producing code changes, the agent produces a structured proposal describing what it intends to do, which files it will modify, and why.

### Triggering Conditions

Plan Mode activates through several pathways:

1. **Explicit user command.** The `/plan` slash command or typing "plan" engages the mode directly.
2. **Automatic engagement.** Claude Code's initialization protocol specifies: "Enter Plan Mode for any directive touching >3 files or spanning multiple domains." This is configurable via CLAUDE.md.
3. **Sub-agent planning.** When using the orchestrator pattern, planning agents can be dispatched specifically to investigate and propose before coder agents execute.
4. **Team alignment.** In multi-person workflows, Plan Mode serves as a synchronization point — the plan document becomes a shared artifact that the team reviews before any agent writes code.

### The Plan Document

A well-formed plan produced in Plan Mode typically contains elements that help the human evaluate and approve the proposed changes. The specific required sections listed below (current state, ordered changes, risks, success criteria) are advisory synthesis rather than documented source-backed Claude Code mechanics. [synthesis — this structure is plausible but not established in the cited sources]

- **Current state assessment.** What exists now, what the relevant files contain, what the dependency graph looks like.
- **Proposed changes.** Specific files to create, modify, or delete, with rationale for each.
- **Ordering and dependencies.** Which changes must precede others, which can be parallelized.
- **Risk assessment.** What could go wrong, what is irreversible, what needs testing.
- **Success criteria.** How to verify the changes achieved their objective.

The plan is an execution plan that the agent itself will carry out once approved. The human reviews for correctness and alignment, then releases the agent to execute.

---

## Key Insights

### Plan Mode as Context Window Hygiene

One of the most practically significant benefits of Plan Mode is its effect on context window utilization. When an agent immediately begins editing files, every tool call, file read, edit attempt, error correction, and retry consumes context. In complex multi-file changes, the agent may exhaust 50-60% of its context window on the implementation itself, leaving insufficient room for verification and refinement.

Plan Mode front-loads the expensive exploration phase. The planning sub-agent (if delegated) operates in its own context window, consuming its own tokens. When the plan returns to the main thread, it arrives as a compact summary — perhaps 2-3% of the context that the exploration consumed. The main agent then executes from a clean, well-understood starting position with most of its context budget intact.

In practice, teams report that using planning sub-agents for investigation followed by coder sub-agents for implementation keeps the main thread at 25-30% context utilization even for complex features, compared to 60%+ when the main agent does everything sequentially.

### The Relationship to Extended Thinking

Plan Mode and extended thinking are orthogonal controls that compose multiplicatively:

| | Standard Thinking | Extended Thinking |
|---|---|---|
| **Normal Mode** | Quick edits, well-specified tasks | Complex single-file changes, debugging |
| **Plan Mode** | Simple multi-file changes, team alignment | Architectural decisions, large refactors |

The highest-quality outcomes come from Plan Mode with extended thinking enabled during the planning phase. The agent explores deeply, reasons extensively about what it finds, and produces a plan that reflects genuine understanding rather than surface-level pattern matching. Then execution can proceed with standard thinking, since the hard cognitive work is already done.

### Human-in-the-Loop as Quality Gate

The "human-in-the-loop" aspect of Plan Mode is not merely a safety mechanism. It serves three distinct functions:

1. **Alignment verification.** The human confirms the agent understood the intent correctly before resources are spent on implementation. Catching a misunderstanding at the plan stage costs minutes; catching it after implementation costs hours.

2. **Domain knowledge injection.** The plan often surfaces questions the agent cannot answer from the codebase alone — business constraints, performance requirements, upcoming changes that would conflict. The human provides this context as plan feedback.

3. **Scope control.** Agents tend toward completionism. A plan to "update the authentication system" may propose changes to 15 files when the human only needs 3 changed. The approval step is where scope creep gets caught.

### Plan Mode in Multi-Agent Orchestration

The most sophisticated use of Plan Mode appears in multi-agent architectures where the planning function is explicitly separated from execution:

1. **Multiple planning agents** investigate different aspects of the codebase in parallel, each in its own context window.
2. **The orchestrator** synthesizes their findings into a unified plan.
3. **The human** approves the plan (or requests modifications).
4. **Multiple coder agents** execute different tracks of the plan in parallel.
5. **Review agents** verify the implementation against the plan.

This pattern keeps any individual agent's context window clean while allowing the system as a whole to reason about arbitrarily complex changes. The plan document serves as the coordination artifact — it is the shared understanding that all agents work from.

---

## Anti-Patterns and Failure Modes

### Planning Without Reading

An agent that enters Plan Mode but does not thoroughly explore the codebase produces plans based on assumptions rather than evidence. The plan looks plausible but misses critical details — existing implementations that would conflict, naming conventions that should be followed, test patterns that need to be maintained. **Plan Mode without exploration is just speculation with extra steps.**

### Over-Planning Simple Changes

Not every change benefits from Plan Mode. A single-file bug fix with an obvious cause and clear solution gains nothing from a planning phase except latency. The automatic trigger ("any directive touching >3 files") is a reasonable heuristic, but it should be overridden for well-understood changes regardless of file count.

### Plan as Permanent Artifact

Plans describe a proposed action at a point in time against a specific codebase state. Storing plans as permanent documentation can create a maintenance burden when the codebase evolves past the plan's assumptions. The advice that plans are inherently ephemeral and should never be kept as durable artifacts is process guidance not cited in the sources. [synthesis — not directly stated in cited sources]

### Approval Without Review

The human approval step only adds value if the human actually reads the plan. Rubber-stamping plans because "the agent usually gets it right" defeats the purpose of the gate. When this pattern emerges, it indicates either that Plan Mode is being used for tasks too simple to need it, or that the human has lost engagement with the process.

### Infinite Planning Loops

When a plan is rejected with vague feedback ("this doesn't feel right"), the agent may re-plan indefinitely without converging. Feedback must be specific: which part of the plan is wrong, what constraint was violated, what alternative approach to consider. The human's job in the loop is not just to say yes or no but to provide the information that makes the next iteration converge.

---

## Implications

### For Engineering Workflows

Plan Mode formalizes what experienced engineers do naturally: think before coding. The difference is that it makes this thinking externally visible and reviewable. Junior engineers benefit from seeing how an expert-level agent approaches planning. Senior engineers benefit from having a structured format for reviewing proposed changes. The plan document becomes a communication artifact as much as a technical one.

### For Non-Technical Stakeholders

Plan Mode is the primary mechanism through which non-technical team members can meaningfully participate in technical decisions. A plan written in natural language with clear rationale is accessible in a way that code diffs are not. Product managers can review plans and catch misalignment before implementation, not after.

### For Agent Autonomy Gradients

Plan Mode exists on a spectrum. At one end, every change requires human approval. At the other, the agent operates fully autonomously. The appropriate position on this spectrum depends on task familiarity, error reversibility, and organizational trust. As teams build confidence in their agent's judgment, they can selectively disable Plan Mode for well-understood task categories while retaining it for novel or high-risk changes.

---

## Obsolescence and Supersession

### The Dive-First Default

Before Plan Mode, the default agent behavior was immediate execution: receive a task, begin reading and writing files, iterate toward completion. The assumption: starting implementation immediately is efficient because exploration and implementation naturally interleave.

This assumption held for small, well-specified tasks. It broke for large multi-file changes where the wrong implementation approach — chosen before understanding the full dependency graph — required backtracking that consumed more total context and time than upfront planning would have. The `corpus/claude-code/10825.md` source documents the cultural supersession of this assumption: "For twenty years, engineering culture has been about maximizing time spent writing code." The agent-first team described there explicitly inverted this: "no coding before 10am," with the morning dedicated to prompting, aligning, and planning before any agent writes code.

Plan Mode is the architectural expression of this cultural inversion.

### The Code Review Culture Supersession

The same source (`10825.md`) documents a related supersession: "Review the output, not the code. Don't read every line an agent writes. Test code against the objective. If it passes, ship it. If it doesn't, reset the objectives & constraints. Code review as we knew it is overhead the system no longer needs."

This is the inversion of the human code review model, where reviewers read every line. The human-in-the-loop gate in Plan Mode is not a code review gate — it is an objective alignment gate. The human reviews the plan (intent + approach) rather than the implementation (line-by-line code). This is a qualitatively different kind of review, appropriate for a workflow where agents write the code but humans set the objectives.

### Plan Mode as First-Class Feature vs. Prompt Convention

Plan Mode evolved from a prompt convention ("please think before acting") into a first-class mode with dedicated triggering mechanisms. The progression: early users discovered that including planning language in prompts improved outcomes, which led to community-standardized prompt templates, which led to formal Plan Mode as a feature. The current automatic engagement rule (activates for directives touching >3 files or spanning multiple domains) encodes the community-discovered threshold as a system-level default.

This is the standard trajectory for Claude Code capabilities: community discovers a valuable pattern through experimentation, documents it as a best practice, and the system eventually incorporates it as a built-in behavior.

---

## Syncrescendence Operational Context

The following claims derive from the constellation's constitutional documents (AGENTS.md, CLAUDE.md), not from external corpus sources:
- "Enter Plan Mode for any directive touching >3 files or spanning multiple domains" — this is the Syncrescendence's own CLAUDE.md protocol

## Source Provenance

| Source | Key Contribution |
|--------|-----------------|
| `corpus/claude-code/00025.md` | Sub-agent planning architecture — parallel planning agents, context window hygiene, orchestrator pattern |
| `corpus/claude-code/10825.md` | "No coding before 10am" — Plan Mode as organizational practice, team alignment before agent execution |
| `corpus/claude-code/08764.md` | Unified research synthesis on Plan Mode mechanics, triggering conditions, relationship to extended thinking |
| `CLAUDE.md` (project config) | Operational protocol: "Enter Plan Mode for any directive touching >3 files or spanning multiple domains" |

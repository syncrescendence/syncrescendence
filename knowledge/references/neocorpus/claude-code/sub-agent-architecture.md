# Sub-Agent Architecture

A sub-agent in Claude Code is a genuine agent instance with its own independent context window, agent loop, and tool access — not a function call, not a prompt template, but a separate execution thread that reads files, runs commands, and produces output without consuming tokens in the parent context. This architecture is the primary mechanism by which Claude Code transcends the single-context-window bottleneck. The parent agent delegates a scoped task, the sub-agent executes it in isolation, and only a compact summary returns to the parent thread. Understanding when and how to delegate is the difference between a session that exhausts its context halfway through and one that completes a full feature build with capacity to spare.

---

## Core Architecture

### What Sub-Agents Are

Each sub-agent is a full agent loop: it receives a task description, plans its approach, uses tools (file read/write, bash, grep, glob), iterates on its output, and returns a result. The critical architectural property is **context isolation** — tokens consumed by the sub-agent do not count against the parent's 200K context window. A sub-agent that reads 30 files and produces 50,000 tokens of intermediate reasoning returns perhaps 2,000 tokens of summary to the parent.

This isolation is not merely an optimization. It is an architectural boundary that changes the fundamental economics of agent work. Without sub-agents, every file read, every tool call, every intermediate thought consumes irreplaceable parent context. With sub-agents, these costs are externalized to disposable context windows.

### Built-In Agent Roster

Claude Code ships with several pre-configured sub-agents, each optimized for a specific class of work:

| Agent | Model | Capability | Use Case |
|-------|-------|------------|----------|
| **Bash** | Same as parent | Shell command execution | Git operations, terminal tasks, build commands |
| **General-purpose** | Same as parent | Full tool access (read, write, bash) | Multi-step tasks, complex implementations |
| **Explore** | Haiku (fast, cheap) | Read-only (search, read) | Codebase analysis, pattern finding, tech stack surveys |
| **Planning** | Same as parent | Read-only with structured output | Requirements investigation, architectural analysis |
| **Claude Code Guide** | Same as parent | Documentation access | Feature questions, capability queries |

The model selection is significant: the Explore agent runs on Haiku, making it dramatically cheaper and faster for read-only reconnaissance. Using a full Opus-class agent for codebase scanning is wasteful when Haiku can identify patterns and summarize findings at a fraction of the cost.

### Invocation Patterns

Sub-agents can be invoked through multiple paths:

- **Explicit invocation**: The `@agent-name` syntax directly summons a specific agent
- **Implicit delegation**: The parent agent decides autonomously to delegate based on task characteristics
- **Background execution**: `Ctrl+B` launches a sub-agent in the background, freeing the main thread for continued interaction
- **Parallel dispatch**: Multiple sub-agents launched simultaneously for independent tasks

Background execution deserves emphasis. A background sub-agent runs asynchronously — the operator can continue conversing with the main agent while the background agent works. Results appear when the background agent completes. This transforms the interaction model from sequential (do one thing, wait, do the next) to concurrent (do many things, review results as they arrive).

### The Nesting Constraint

Sub-agents cannot spawn additional sub-agents — the execution graph is two levels deep: parent and child. This constraint is documented in `corpus/claude-code/08764.md`, which is not cited in this entry's source provenance. The cited sources (`00025`, `08403`, `00212`) support sub-agent isolation and context economics but do not directly establish the two-level nesting limit. [citation gap — the nesting constraint is documented in `08764`, not in the sources cited by this entry]

This constraint shapes delegation strategy. A sub-agent must be self-sufficient for its assigned task. If a task requires hierarchical decomposition, the parent must perform the decomposition and dispatch multiple sub-agents, not delegate the decomposition itself.

---

## Key Insights

### The Decision Tree

Not every task should be delegated. The decision tree for delegation balances context conservation against coordination overhead:

```
Is the task independent of current conversation state?
+-- NO --> Execute inline (delegation would require re-establishing context)
+-- YES -->
    Does it require writing/editing files?
    +-- NO --> Use Explore agent (cheapest, fastest, read-only)
    +-- YES -->
        Is it > 5 minutes of estimated work?
        +-- NO --> Execute inline (coordination overhead exceeds savings)
        +-- YES -->
            Can multiple tasks run in parallel?
            +-- YES --> Fork multiple sub-agents simultaneously
            +-- NO --> Fork single general-purpose agent
```

The key branching criterion is **independence from current conversation state**. A task that requires understanding the nuanced discussion that led to the current approach is poorly suited for delegation — the sub-agent would need the full context transferred, defeating the purpose. A task that can be specified by its inputs and expected outputs alone is ideal for delegation.

### Context Economics

The economic case for sub-agents is that tokens consumed by sub-agents do not count against the parent context window, so delegation preserves main-thread context. The cited sources support this general principle. The specific numerical scenario (95,000 tokens without sub-agents vs. 15,000 with; sub-agents consuming 80,000 collectively) is synthesis — it illustrates the principle but is not directly stated in the cited sources. [synthesis — the general economics are supported; the specific numerical example is not directly stated in `00025`, `08403`, or `00212`]

### The Coordinator Pattern

The most powerful sub-agent usage pattern positions the parent as a pure coordinator. The parent:

1. Reads the implementation plan
2. Identifies tasks that can run in parallel
3. Dispatches Coder sub-agents for each parallel track
4. Reviews results via Code Reviewer sub-agents
5. Synthesizes findings and dispatches the next wave

The parent never reads source files directly, never writes code directly, never runs tests directly. Every concrete action is delegated. The parent's context contains only plans, summaries, and coordination decisions — the highest-value, lowest-token information.

This pattern enabled a documented build of a full-featured application (authentication, database integration, UI) while consuming only 58% of the main context window. Without the coordinator pattern, the same build would have exceeded context capacity partway through.

### Custom Agents

Beyond the built-in roster, operators can create custom sub-agents by placing `.md` files in `.claude/agents/`. Each custom agent has:
- A custom system prompt defining its persona and expertise
- A specified tool access set (which tools it can use)
- A model selection (Opus, Sonnet, or Haiku)

This enables domain-specific delegation: a "UI Expert" agent that enforces design system compliance, a "Security Reviewer" that audits for vulnerabilities, a "Database Specialist" that optimizes queries. The custom agent's system prompt acts as a behavioral contract scoped to its domain, analogous to CLAUDE.md but for a single agent persona.

---

## Anti-Patterns and Failure Modes

### Over-Delegation

Delegating tasks that are faster to execute inline than to describe, dispatch, and review. A simple file read or a single command execution has lower overhead when done directly. The coordination cost of sub-agent dispatch (task description, context establishment, summary parsing) creates a minimum viable task size below which delegation is counterproductive.

### Under-Specification

Dispatching a sub-agent with vague instructions ("fix the authentication") and expecting it to infer the parent's full context. Sub-agents start with empty context. Every relevant constraint, file path, convention, and expected outcome must be explicitly stated in the task description. The sub-agent has access to CLAUDE.md (loaded automatically) but not to the parent's conversation history.

### Ignoring the Nesting Constraint

Designing workflows that assume sub-agents can delegate further. This manifests as assigning tasks to sub-agents that are too large for a single agent to complete without decomposition. The parent must decompose such tasks into sub-agent-sized units before dispatching.

### Model Mismatching

Using an Opus-class sub-agent for tasks that Haiku handles well (codebase scanning, pattern matching, simple reviews), or using Haiku for tasks that require deep reasoning (architectural decisions, complex refactoring). The Explore agent exists specifically to provide fast, cheap read-only analysis; using the general-purpose agent for the same task wastes resources and time.

### Serial Where Parallel Is Possible

Dispatching sub-agents one at a time, waiting for each to complete before dispatching the next, when the tasks are independent. The primary throughput advantage of sub-agents is parallelism — three agents working simultaneously complete in the time of one. Sequential dispatch squanders this advantage.

---

## Implications

Sub-agents transform Claude Code from a single-threaded tool into a multi-threaded development environment. The architectural significance extends beyond token conservation: sub-agents enable specialization (different agents for different tasks), parallelism (concurrent execution of independent work), and quality preservation (keeping the main context clean and focused).

For the Syncrescendence constellation, sub-agents are the mechanism by which Commander maintains operational coherence across long sessions. By delegating exploration, implementation, and verification to sub-agents, Commander preserves its context for what only the coordinator can do: hold the strategic thread, maintain the Sovereign's intent, and make routing decisions that require the full conversational history.

The deeper pattern is that sub-agents implement a form of cognitive architecture — a division of mental labor between a supervisory executive (the parent) and specialized workers (the sub-agents). This mirrors the structure of effective human teams and, not coincidentally, the structure of the Syncrescendence constellation itself.

---

## Obsolescence and Supersession

### The Single-Agent Marathon

Before sub-agents, Claude Code sessions were single-threaded: one agent, one context window, tasks executed sequentially with all context accumulating in one place. The assumption underpinning this model: the context window is large enough (200K tokens) to handle complex multi-step projects without delegation. This assumption was correct for single-file tasks and quickly wrong for projects requiring broad codebase exploration before targeted implementation.

The corpus source (`corpus/claude-code/00025.md`) documents the key failure mode: "If I ask the main agent to summarize the tech stack without sub-agents, all tool responses and the final response contribute to the context usage." In a complex project, the agent exhausts significant context on exploration that could be externalized.

### The Haiku Optimization as Economic Supersession

The Explore agent's use of Haiku (fast, cheap, read-only) represents a targeted supersession of a prior assumption: that all sub-tasks require the same model capability as the main task. Before model-differentiated delegation, the choice was binary: use the primary (expensive) model for everything, or manually manage separate sessions with different models.

The built-in Explore agent makes asymmetric model allocation automatic: reconnaissance tasks (codebase scanning, pattern finding, tech stack surveys) run on Haiku; implementation tasks run on Sonnet or Opus. The source states this contrast explicitly: "even the Haiku model does a surprisingly good job at identifying glaring issues." The supersession is from "same model for everything" to "model matched to task complexity and cost."

### From Background Agents as Workaround to First-Class Feature

The `Ctrl+B` background execution pattern represents a supersession from a synchronous interaction model to an asynchronous one. The prior model required the operator to wait for every agent operation to complete before issuing the next instruction. Background agents were initially available but underused because the synchronous mental model dominated.

As practitioners discovered that background agents allowed continued interaction while compute ran asynchronously, background execution shifted from a workaround for impatient users to a recommended pattern for all substantial sub-tasks. The transformation of the interaction model — from sequential command-and-wait to concurrent command-and-continue — is the substantive architectural shift that background agents enable.

---

## Source Provenance

| Corpus File | Content |
|-------------|---------|
| `corpus/claude-code/00025.md` | Sub-agents and background agents — built-in roster, invocation patterns, context economics, coordinator pattern |
| `corpus/claude-code/08403.md` | Sub-agent delegation guide — decision tree, context annotation, fork/inline/parallel routing |
| `corpus/claude-code/00212.md` | Agent teams — sub-agent context isolation, CLAUDE.md automatic loading, teammate coordination |
| `corpus/claude-code/08764.md` | Unified research synthesis — two-level nesting constraint (not previously cited in this entry but documents the nesting limit) |

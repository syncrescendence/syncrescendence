# Agent Teams and Parallel Orchestration

Agent Teams is Claude Code's multi-agent coordination layer — an experimental system where a team lead spawns multiple teammate agents that work in parallel on partitioned tasks, communicating through a shared task list and message protocol rather than shared conversation history. Enabled by the `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` flag, this architecture transforms Claude Code from a tool that does one thing at a time into an orchestration platform that coordinates multiple simultaneous agents. The coordination challenge it solves is not merely parallelism but coherence: how do multiple agents with independent context windows produce a unified, non-conflicting result?

---

## Core Architecture

### The Team Structure

An agent team consists of:
- **Team lead**: The primary agent that receives the user's task, decomposes it, spawns teammates, assigns work, and synthesizes results
- **Teammates**: Independent agent instances, each with its own context window, tool access, and assigned scope of work
- **Shared task list**: A file-backed coordination structure that tracks task status, assignment, and dependencies
- **Message protocol**: Direct messages between agents for coordination, status updates, and handoffs

The team lead does not share conversation history with its teammates. Communication happens exclusively through the task list and message protocol. This constraint is architectural, not incidental — it forces coordination through structure rather than context, which scales better than shared state.

### Activation and Setup

Teams are activated by setting `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` to `"1"` in `settings.json`. No additional dependencies are required. The operator describes a task and requests a team; Claude Code reads the project's CLAUDE.md to determine how to partition work, then spawns teammates automatically.

The team configuration and task list storage paths (`~/.claude/teams/`, `~/.claude/tasks/`) and the `TeamCreate`/`TeamDelete` APIs are observed operational behavior; they are not documented in the cited sources. [observed behavior, not documented in cited sources]

### File Ownership Partitioning

The critical coordination mechanism is file ownership. The team lead divides the codebase into non-overlapping partitions and assigns each partition to a teammate. No two teammates should edit the same file. This eliminates the most destructive class of multi-agent failure: edit collisions where two agents modify the same file simultaneously, producing corrupted or conflicting output.

The quality of file partitioning depends directly on the clarity of module boundaries in CLAUDE.md. When CLAUDE.md declares explicit module boundaries (e.g., "The `data-core/` directory handles database operations, `ui-events/` handles frontend event handling, `features/` contains feature implementations"), the team lead can partition cleanly. When module boundaries are implicit or absent, the team lead must infer partitions from directory structure and file content, with lower reliability.

### Communication Protocol

Teammates communicate through two channels:

**Shared task list**: Each task has an ID, subject, description, status (pending/in_progress/completed), owner, and dependency list (blocks/blockedBy). Any teammate can read the full task list; task ownership is assigned by the team lead or claimed by idle teammates.

**Direct messages**: Teammates send messages to specific other teammates or broadcast to all. Messages include a content field and a summary field (for UI preview). The team lead receives automatic idle notifications when teammates complete their turns.

The message protocol supports lifecycle management including graceful termination and coordinated planning handoffs. Specific structured type names such as `shutdown_request`/`shutdown_response` and `plan_approval_request`/`plan_approval_response` are observed operational behavior; they are not documented in the cited sources. [observed behavior, not documented in cited sources]

---

## Key Insights

### Coordination Through Structure, Not Conversation

The most counterintuitive property of agent teams is that teammates have **no shared conversation history**. Each teammate's context window contains only: the CLAUDE.md configuration, their assigned task description, the files they've read, and messages they've received. They do not know what other teammates are doing except through the task list and direct messages.

This constraint is a feature, not a limitation. Shared conversation history would consume context in every teammate, scaling linearly with team size and conversation length. Structure-based coordination (task list + messages) scales to arbitrary team sizes with constant per-teammate overhead.

The practical consequence is that CLAUDE.md becomes the primary coordination mechanism. It is the only context that every teammate shares. Module boundaries, coding standards, naming conventions, and architectural constraints declared in CLAUDE.md are the shared vocabulary that enables teammates to produce coherent, compatible output without direct conversation.

### The Coordinator/Coder/Reviewer Pipeline

The most effective team pattern mirrors a human engineering team:

1. **Team lead as coordinator**: Decomposes the task, assigns tracks, monitors progress
2. **Coder teammates**: Execute implementation tasks within their assigned file partitions
3. **Reviewer teammates**: Audit completed work for correctness, security, and consistency

This pipeline can operate in waves: the team lead dispatches Coder agents for parallel implementation, then dispatches Reviewer agents to audit the results, then dispatches Coder agents to address review findings. Each wave is parallel within itself but sequential across waves.

The Reviewer role is particularly valuable because it operates at low cost — even the Haiku model produces useful code review feedback on issues like missing error handling, inconsistent naming, or security vulnerabilities. Running Reviewer agents on Haiku while Coder agents run on Opus creates an asymmetric team where quality assurance is cheap and pervasive.

### Task Dependencies and Blocking

The task list supports explicit dependency declarations: task B can be marked as blocked by task A, preventing B from being claimed until A completes. This enables the team lead to express sequencing requirements within a parallel execution model.

Dependencies must be managed carefully. Over-constraining dependencies (everything depends on everything) serializes execution and eliminates the parallelism advantage. Under-constraining (no dependencies when they exist) produces race conditions where a teammate builds on an interface that another teammate hasn't finished defining.

The correct granularity is: declare dependencies only for genuine data flow requirements. If teammate A must define an API interface before teammate B can consume it, that is a real dependency. If teammate A and teammate B work on independent modules, no dependency exists regardless of their conceptual relationship.

### Idle State Semantics

Teammates go idle after every turn. This is normal behavior, not an error condition. An idle teammate has simply finished its current turn and is waiting for input — a new message, a new task assignment, or a shutdown request. The system sends automatic idle notifications to the team lead, which are informational, not actionable.

The common mistake is interpreting idle as "done" or "stuck." A teammate that sends a completion message and then goes idle has completed its work successfully. A teammate that goes idle without sending a message may be waiting for a response. The task list status (completed vs. in_progress) is the authoritative indicator of work status, not idle state.

---

## Anti-Patterns and Failure Modes

### Overlapping File Ownership

Assigning the same files or directories to multiple teammates. This produces edit collisions — the last writer wins, silently overwriting the other teammate's changes. The team lead must ensure non-overlapping partitions, and CLAUDE.md should declare module boundaries clearly enough to enable clean partitioning.

### Excessive Broadcasting

Using broadcast messages (sent to all teammates) for routine communication. Each broadcast delivers a separate message to every teammate, consuming API resources linearly with team size. Broadcasts are appropriate only for critical team-wide announcements (e.g., "stop all work, blocking issue found"). Routine status updates and coordination should use targeted direct messages.

### Micro-Task Decomposition

Breaking work into tasks so small that coordination overhead exceeds execution time. Each task carries fixed costs: description writing, assignment, status tracking, completion reporting. A task that takes 30 seconds to execute but 2 minutes to describe and coordinate is a net negative. Tasks should be scoped to meaningful units of work — a complete module, a full feature, a coherent refactoring — not individual line changes.

### Missing CLAUDE.md Boundaries

Attempting to run agent teams on a project with minimal or absent CLAUDE.md configuration. The team lead cannot partition work effectively without declared module boundaries, coding standards, and architectural constraints. The result is overlapping assignments, inconsistent output, and frequent conflicts. Investing in CLAUDE.md configuration before activating teams is not optional preparation — it is a prerequisite.

### Premature Shutdown

Terminating teammates before verifying that all tasks are complete and all outputs are consistent. The team lead should check the full task list, verify all tasks show completed status, and run integration-level verification before issuing shutdown requests. Premature shutdown risks losing in-progress work that the teammate had not yet committed.

---

## Implications

Agent teams represent the frontier of Claude Code's capability — the point where it transitions from a developer tool to a development platform. A single Claude Code session coordinating five parallel agents is not five times faster than one agent; it is qualitatively different, capable of executing integration-level tasks that no single agent could complete within a single context window.

The coordination patterns that make teams effective — file ownership partitioning, structure-based communication, dependency-aware scheduling, CLAUDE.md as shared context — are the same patterns that make human engineering teams effective. This is not coincidental. The constraints are similar (limited working memory, communication overhead, conflict potential), and the solutions converge.

For the Syncrescendence constellation, agent teams offer a path to re-enabling the multi-agent coordination that was lost when the Mac mini constellation was anesthetized. A Commander session running agent teams can approximate the Cartographer + Adjudicator + Psyche pipeline within a single machine, using teammates as specialized sub-agents with persistent task state. The team task list provides the coordination layer that tmux sessions previously provided.

The experimental flag signals that this architecture is still evolving. Current limitations — no cross-session team persistence, no automatic conflict resolution, no resource-aware scheduling — will likely be addressed as the system matures. But the fundamental pattern is established: multi-agent coordination through structured partitioning and message-based communication, not shared context.

---

## Obsolescence and Supersession

### Pre-Teams Era: Sequential Single-Agent Bottleneck

Before agent teams, the standard Claude Code workflow was single-threaded: one agent, one context window, tasks executed sequentially. Parallelism required entirely separate Claude Code sessions that could not coordinate — there was no shared task list, no message protocol, no team lead abstraction. Multi-agent work meant the human acted as the coordination layer, manually shuttling context and results between isolated sessions.

The assumption underpinning the single-agent model was that the context window was the natural unit of coherent work. If a task was too large for one context, you broke it into independent sequential phases or you simply could not do it in one session. This assumption held until agent teams introduced structure-based coordination as an alternative to shared context.

### Supersession: From Human Coordinator to Agent Coordinator

The workflow superseded by teams was human-relayed multi-agent work: the Sovereign (human) dispatching separate sessions, relaying results manually, synthesizing outputs by hand. This is visible in the Syncrescendence constellation's own operational history — the Commander + Adjudicator + Cartographer + Psyche pipeline required the Sovereign to relay between agents because no programmatic coordination channel existed. Agent teams replace the human relay function with a machine-readable task list and message protocol.

The transition encodes a design decision: coordination overhead should be paid by the agent system, not by the human. The pre-teams pattern pushed coordination cost onto humans because it was the only option. Agent teams make coordination a first-class agent responsibility.

### What Remains Unresolved (as of early 2026)

The `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` flag marks this architecture as incomplete. Known limitations: no persistence of team state across sessions (teams dissolve when the session ends), no resource-aware scheduling (the system cannot throttle spawning based on API quota pressure), no automatic conflict detection when file ownership partitioning fails. These are the open problems whose solutions will define the next supersession.

---

## Source Provenance

| Corpus File | Content |
|-------------|---------|
| `corpus/claude-code/00212.md` | Agent teams in practice — setup, file ownership, 3 rules, communication patterns, CLAUDE.md as coordination layer |
| `corpus/claude-code/00025.md` | Sub-agents and background agents — context isolation, coordinator pattern, parallel dispatch |
| `corpus/claude-code/10411.md` | Slack integration — Claude Code as organizational platform, configuration investment multiplier |

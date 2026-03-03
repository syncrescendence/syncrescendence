# Task Decomposition and Dependency Graphs

Task decomposition is the translation of a complex goal into a directed acyclic graph of executable subtasks with explicit dependency edges. It is the first act of any multi-agent orchestration: before agents can be dispatched, the work must be broken into units that are independently executable, correctly ordered, and sufficiently specified that an agent can complete each unit without re-deriving the decomposition. The dependency graph is the scaffold on which parallelism, failure recovery, and progress tracking all depend. A malformed graph — cycles, missing edges, under-specified nodes — propagates errors through the entire pipeline. The quality of the decomposition determines the ceiling of the system's performance, regardless of how capable the individual agents are.

---

## Core Principles

### 1. The DAG as Execution Plan

A well-formed task dependency graph is a directed acyclic graph where:

- **Nodes** are subtasks with clear completion criteria, assigned agent types, and bounded scope.
- **Edges** represent "must complete before" relationships. If task B depends on an output of task A, the edge A -> B ensures B does not begin until A completes.
- **Parallelism** emerges from the absence of edges. Tasks with no dependency relationship can execute simultaneously.

The graph is not merely a planning artifact — it is the runtime execution plan. An orchestrator walks the graph, dispatching tasks whose dependencies are satisfied, collecting results, and unblocking downstream tasks. The Syncrescendence task dispatch system embodies this: each task carries `Status`, `Lease-ID`, `Timeout`, and `Escalation-Contact` fields that govern its lifecycle within the graph.

These architectural principles represent standard practice in distributed task systems; they are not directly stated in the cited sources. The formal property that matters most is the **critical path**: the longest chain of sequential dependencies in the graph. This chain determines the minimum wall-clock time for the entire pipeline, regardless of how many agents are available. Optimizing the decomposition means minimizing the critical path — moving tasks off the critical chain into parallel branches wherever the dependency structure permits.

### 2. The Topology Selection Problem

Research on task-adaptive orchestration identifies four canonical topologies for multi-agent task execution:

- **Parallel**: All subtasks are independent. Maximum throughput, minimum coordination overhead. Fails when tasks have hidden dependencies.
- **Sequential**: Each subtask depends on the previous one's output. Maximum control, minimum parallelism. Appropriate when each step transforms the previous step's output.
- **Hierarchical**: A coordinator decomposes the task, dispatches subtasks to workers, and synthesizes results. The coordinator is the single point of failure but also the single point of coherence.
- **Hybrid**: Different subgraphs use different topologies based on their internal dependency structure. A planning phase runs sequentially, then spawns parallel execution tasks, whose results are synthesized sequentially.

The key finding from AdaptOrch research is that topology selection itself yields 12-23% improvement over static single-topology baselines, even when using identical underlying models. The orchestration architecture matters more than the model when models have converged in capability. This is the regime the field entered in 2026: picking the best model yields diminishing returns; picking the best orchestration topology yields compounding returns.

### 3. The Specification Depth Principle

Each node in the dependency graph must be specified to the level where a single agent can execute it without further decomposition decisions. This is the Goldilocks constraint:

- **Under-specified**: "Implement the authentication system." This requires the executing agent to make architectural decisions that should have been made at decomposition time. Different agents may make incompatible decisions, producing outputs that do not compose.
- **Over-specified**: "Write line 47 of auth.py as `if token.is_valid():`." This eliminates the agent's ability to exercise judgment, making the orchestrator a slow typist rather than a coordinator.
- **Correctly specified**: "Implement JWT token validation that accepts tokens signed with RS256, returns a structured error on expiry, and writes results to the auth module's existing interface." This constrains the architectural decisions while leaving implementation latitude.

The test: could two different competent agents, given this specification independently, produce outputs that compose correctly? If yes, the specification depth is correct.

### 4. Failure Modes and Recovery

Dependency graphs introduce failure modes that do not exist in monolithic execution:

- **Node failure**: A subtask fails. The orchestrator must decide: retry (with a retry count and backoff), skip (if the subtask is optional), abort (if the subtask is on the critical path with no fallback), or escalate (route to a human or a different agent type).
- **Cascade failure**: A node fails, blocking all downstream nodes. The blast radius of a failure is proportional to the number of transitive dependents.
- **Timeout and lease expiry**: An agent claims a task but does not complete it within its lease window. The task must be reclaimed and re-dispatched, potentially to a different agent.
- **Stale dependency**: A task completes, but its output becomes invalid before the dependent task consumes it (e.g., a file is modified by a concurrent process). The dependency edge must carry not just "completed" but "completed and output still valid."

The Syncrescendence dispatch system handles several of these explicitly: `Retry-Count`, `Timeout`, `Lease-ID`, `Exit-Code`, and `Escalation-Delay` are first-class fields on every task. A task that fails with a retryable exit code is automatically re-dispatched. A task that exceeds its lease is reclaimed. A task that fails permanently routes to the escalation contact.

---

## Key Insights

### Premature Decomposition

The most common failure mode in task decomposition is decomposing too early — breaking a problem into subtasks before the problem is sufficiently understood. Premature decomposition locks in architectural decisions when information is least available, then forces all downstream work to conform to those decisions even when they prove wrong.

The corrective pattern is **progressive decomposition**: decompose only one level at a time. Execute the first level of subtasks, observe their outputs, then decompose the next level based on actual results rather than predicted results. This sacrifices some parallelism (you cannot dispatch level-2 tasks until level-1 completes) but dramatically reduces wasted work from incorrect decomposition.

### The Coordination Tax

Every edge in the dependency graph is a coordination cost. The orchestrator must track the edge, the producing task must output in a format the consuming task can parse, and the consuming task must validate its input. In systems with many fine-grained tasks, the coordination tax can exceed the cost of the tasks themselves.

The practical implication: prefer fewer, coarser tasks over many fine-grained ones, unless the parallelism gain from fine-grained decomposition exceeds the coordination cost. A system with 5 well-specified tasks that each take 10 minutes will often outperform a system with 50 micro-tasks that each take 1 minute but require 49 dependency edges.

### Orchestration as First-Class Optimization

When underlying models converge in capability — as they have in 2026 — the orchestration layer becomes the primary optimization target. The same models, arranged in different dependency topologies, produce measurably different outcomes. This inverts the traditional optimization priority: instead of "pick the best model and wrap it in scaffolding," the priority becomes "design the best orchestration and plug in whatever model meets the minimum capability bar."

The Topology Routing Algorithm from AdaptOrch maps tasks to optimal patterns in O(|V| + |E|) time — fast enough to be a runtime decision rather than a design-time decision. This enables dynamic topology selection: the same system can use parallel execution for independent subtasks and sequential execution for dependent chains, switching topology as the graph structure demands.

### The Lease as Timeout Mechanism

Dependency graphs without timeouts are dependency graphs that can block forever. The lease model — where an agent claims a task for a bounded duration — transforms the graph from a static plan into a self-healing system. When a lease expires, the task returns to the available pool and can be claimed by a different agent. This prevents a single slow or failed agent from blocking the entire downstream graph.

The Syncrescendence dispatch system demonstrates this concretely: every task carries a `Lease-ID` and `Timeout`. The Adjudicator claimed task DC-003 with `lease-adjudicator-1771575249-40825` and a `Timeout: 30` value (00302 specifies `Timeout: 30` without explicitly stating the unit). When the task failed (exit code 75, usage limit hit), the retry mechanism incremented the attempt counter and re-dispatched. Without the lease, the task would have remained "in progress" indefinitely, blocking any dependent work.

The lease duration must be calibrated to the task complexity: too short and agents are interrupted mid-work; too long and failed agents block the pipeline. A heuristic: set the lease to 2x the expected completion time, with escalation at 1x.

### The Consistency Problem

When multiple agents execute subtasks in parallel, they may produce outputs that are individually correct but mutually inconsistent. Agent A generates a database schema; Agent B generates an API layer; but A's schema and B's API assume different data models because they were decomposed from an under-specified parent task.

The solution is **interface-first decomposition**: define the interfaces between subtasks before defining the subtasks themselves. The dependency graph should include explicit "interface contract" nodes that are resolved before any implementation tasks begin. This front-loads the coordination cost but prevents the far more expensive cost of reconciling inconsistent parallel outputs.

---

## Obsolescence and Supersession

### Chain-of-Thought as Implicit Sequential Decomposition

Before multi-agent systems, the dominant task decomposition technique was chain-of-thought prompting: decompose within a single context window using explicit reasoning steps. "First, let me understand X. Then, I will address Y. Finally, I will synthesize Z." This internal sequential decomposition was appropriate when all work fit within a single context window and a single agent.

Chain-of-thought as a decomposition strategy is not obsolete — it is superseded as the appropriate choice for complex multi-step tasks that exceed a single agent's context or capability. The explicit DAG replaces implicit CoT sequential reasoning when: the task is long enough to exhaust a context window, subtasks can be parallelized for efficiency, different subtasks benefit from different agent specializations, or failure recovery requires re-dispatching specific nodes without rerunning the entire chain.

The supersession is task-dependent. Short tasks: CoT in a single agent. Tasks with parallelizable subtasks, context-window pressure, or heterogeneous cognitive requirements: explicit dependency graph with multi-agent dispatch.

### Design-Time Topology as Superseded Default

The default assumption in early orchestration frameworks was that topology was specified at design time and was fixed. You selected "sequential pipeline" or "hierarchical coordinator-workers" when building the system; the topology was baked into the code.

AdaptOrch supersedes this with runtime topology selection. The O(|V| + |E|) routing algorithm maps each incoming task's dependency graph to the optimal topology at dispatch time. The assumption being replaced: "topology is a property of the system." The replacement: "topology is a property of the task."

This supersession has a practical implication for how systems are built: rather than implementing a specific coordination pattern, systems should expose agents as composable components with standardized interfaces, and implement a topology router that selects the pattern based on the dependency structure of each incoming task. The design-time topology decision becomes a set of runtime routing rules.

---

## Anti-Patterns

### The Monolith Decomposition

Breaking a complex goal into exactly two tasks: "plan" and "execute." This is not decomposition; it is a restatement of the problem. The "execute" task still contains all the original complexity.

### The Granularity Trap

Decomposing into tasks that are too fine-grained for the executing agents. If each subtask takes 30 seconds but the coordination overhead (dispatch, context loading, result parsing) takes 2 minutes, the system spends 80% of its time on coordination. The minimum useful task granularity is bounded by the coordination overhead of the orchestration layer. In LLM-based systems, this overhead is substantial: each agent invocation requires loading context, establishing identity, and parsing output. Tasks should be large enough that execution time dominates coordination time.

### The Assembly Line Fallacy

Forcing all subtasks into a sequential chain when many could execute in parallel. This typically happens when the decomposer confuses temporal ordering in the mental model (I thought of A before B) with causal dependency (B requires A's output). Test every edge: does the downstream task actually consume an output of the upstream task? If not, the edge is artificial and should be removed.

### Decompose-and-Forget

Creating the task graph and then treating it as immutable. Real execution produces surprises: tasks that are easier than expected (and should be merged with their successors), tasks that are harder than expected (and should be further decomposed), and tasks that reveal previously unknown dependencies. The graph must be a living document that the orchestrator updates as execution proceeds.

### Ignoring the Critical Path

Optimizing tasks that are not on the critical path. If the critical path takes 60 minutes and a parallel branch takes 10 minutes, making the parallel branch 2x faster saves nothing. All optimization effort should target the critical path until it shifts to a different branch.

---

## Design Implications

### For Orchestrator Developers

Build the dependency graph as a first-class runtime data structure, not a planning artifact that is discarded after dispatch. Support dynamic modification: adding nodes, removing edges, splitting nodes, and re-dispatching failed nodes. Implement critical path analysis so that resource allocation prioritizes the bottleneck chain.

### For Agent Framework Designers

Standardize the interface between tasks: every task produces a structured output that downstream tasks can consume without parsing ambiguity. Define a small set of exit codes that distinguish between retryable failures (timeout, rate limit), permanent failures (invalid input, missing capability), and successes (with output location).

### For Task Specifiers

Write each subtask specification as if the executing agent has never seen the parent task. Include: the objective (what to produce), the constraints (what standards to meet), the inputs (what prior task outputs to consume and where to find them), and the output contract (what format, where to write it, what constitutes success). A specification that requires the agent to infer any of these from context is a specification that will be interpreted differently by different agents on different runs.

### For System Operators

Monitor the gap between the theoretical critical path (minimum time given infinite agents) and the actual execution time. The ratio reveals coordination overhead: a ratio near 1.0 means the system is efficiently parallel; a ratio of 3.0 or higher means coordination costs dominate and the decomposition should be coarsened.

Track task failure rates by position in the dependency graph. Tasks that fail frequently at the root of the graph waste more downstream work than tasks that fail at the leaves. Root tasks with high failure rates should be hardened first — better specification, more capable agents, or pre-validation steps that catch failures before committing to the full dependency chain.

The dependency graph is not just a planning tool — it is the primary diagnostic instrument for multi-agent system performance. Every bottleneck, every failure cascade, and every wasted parallel branch is visible in the graph if you instrument it correctly.

---

## Source Provenance

| Source | Corpus Path | Contribution |
|--------|-------------|--------------|
| AdaptOrch: Task-Adaptive Multi-Agent Orchestration | `corpus/multi-agent-systems/11041.md` | Four canonical topologies; 12-23% improvement from topology selection; orchestration as first-class optimization target |
| Google ADK / A2A architecture overview | `corpus/multi-agent-systems/09928.md` | Loop agents, sequential agents, judges; ADK as orchestration framework; agent communication over web standards |
| Deferred commitment task (DC-003) | `corpus/multi-agent-systems/00302.md` | Lease-ID, Timeout, Retry-Count, Escalation-Delay as task lifecycle fields; concrete dispatch system architecture |

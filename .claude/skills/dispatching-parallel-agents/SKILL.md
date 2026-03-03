---
name: dispatching-parallel-agents
description: BLITZKRIEG tactic parallel dispatch for Commander; fan-out independent tasks to concurrent subagents with structured result collection
wraps: dispatching-parallel-agents (vibeship)
provenance: vibeship (MIT)
vetted: 2026-02-12
pipeline_stages: [DISPATCH, EXECUTE]
---

# Dispatching Parallel Agents

## Syncrescendence Integration

**Agents:** Commander (COO)

This skill powers the BLITZKRIEG tactic -- Commander's high-throughput execution mode where independent tasks are fanned out to parallel subagents for concurrent execution.

### How it fits the pipeline

- **DISPATCH stage:** Commander analyzes the task dependency graph and identifies the maximum parallelizable frontier. Tasks with no inter-dependencies are dispatched simultaneously.
- **EXECUTE stage:** Each parallel subagent executes independently with its own context window. Results are collected and merged by Commander once all agents in the dispatch wave complete.
- **Wave sequencing:** When the plan has sequential dependencies, Commander dispatches in waves -- each wave waits for all prior-wave results before the next fan-out.
- **Composition with blitzkrieg_teams:** This skill is the low-level dispatch mechanism that the `blitzkrieg_teams` Syncrescendence skill orchestrates at a higher level.

### Config notes

- Maximum concurrent subagents should respect the host machine's resource constraints (memory, API rate limits).
- Each dispatched subagent inherits the `verification-before-completion` invariant independently.
- Result collection must handle partial failures gracefully: if one subagent fails, Commander retries that task without blocking completed results.

## Original Reference

@~/.agents/skills/dispatching-parallel-agents/SKILL.md

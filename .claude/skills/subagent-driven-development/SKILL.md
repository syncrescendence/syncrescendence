---
name: subagent-driven-development
description: Primary execution pattern for Commander plan implementation; dispatch fresh subagent per task with two-stage review (spec compliance then code quality)
wraps: subagent-driven-development (vibeship)
provenance: vibeship (MIT)
vetted: 2026-02-12
pipeline_stages: [EXECUTE, REVIEW]
---

# Subagent-Driven Development

## Syncrescendence Integration

**Agents:** Commander (COO)

This is Commander's primary execution pattern when implementing plans that decompose into independent tasks. Each task gets a fresh subagent with a clean context window, followed by a mandatory two-stage review.

### How it fits the pipeline

- **EXECUTE stage:** Commander decomposes a plan into atomic tasks, then dispatches one subagent per task. Each subagent receives only the task spec and relevant file context -- no cross-task bleed.
- **REVIEW stage:** After each subagent completes, Commander runs two review passes:
  1. **Spec compliance review** -- Does the output satisfy the directive requirements?
  2. **Code quality review** -- Does the output meet Syncrescendence coding standards?
- **Composition with BLITZKRIEG:** When tasks are also parallelizable, Commander combines this skill with `dispatching-parallel-agents` to run multiple subagents concurrently while preserving the two-stage review per task.

### Config notes

- Subagent context budgets should be scoped tight: include only the task spec, target files, and relevant type signatures.
- Failed reviews trigger a retry with the review feedback injected into a fresh subagent context (no patching in the same context).
- Each subagent must independently satisfy `verification-before-completion` before returning.

## Original Reference

@~/.agents/skills/subagent-driven-development/SKILL.md

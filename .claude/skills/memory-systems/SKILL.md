---
name: memory-systems
description: Architecture reference for agent memory design; informs update_agent_memory skill with short-term, long-term, and graph-based (Graphiti) memory patterns
wraps: memory-systems (community)
provenance: community - muratcankoylan/Agent-Skills-for-Context-Engineering (MIT)
vetted: 2026-02-12
pipeline_stages: [MEMORY]
---

# Memory Systems

## Syncrescendence Integration

**Agents:** All constellation agents (Ajna, Psyche, Commander, Adjudicator, Cartographer)

This skill provides the architectural reference for how Syncrescendence agents persist and retrieve knowledge across sessions. It directly informs the design of the `update_agent_memory` skill.

### How it fits the pipeline

- **MEMORY stage:** At session boundaries and after significant state changes, agents invoke memory persistence. This skill defines the layered architecture:
  1. **Short-term memory** -- Context window contents; ephemeral; lost at session end.
  2. **Long-term memory** -- Persisted to `.claude/memory/` files and agent state directories; survives across sessions.
  3. **Graph-based memory** -- Structured knowledge via Graphiti; enables relationship-aware retrieval for Cartographer's dependency mapping and Ajna's strategic pattern recognition.
- **update_agent_memory composition:** The `update_agent_memory` Syncrescendence skill is the operational implementation; this skill is the architectural blueprint it follows.
- **Pedigree chain:** Memory updates feed the pedigree hook chain, creating an audit trail of what each agent knew and when.

### Config notes

- Graph-based memory (Graphiti) requires the Neo4j service running on the Mac mini (Psyche's host).
- Memory file format follows the structured markdown convention defined in `orchestration/state/`.
- Each agent maintains its own memory namespace to prevent cross-agent contamination while allowing explicit sharing via the universal ledger.

## Original Reference

@~/.agents/skills/memory-systems/SKILL.md

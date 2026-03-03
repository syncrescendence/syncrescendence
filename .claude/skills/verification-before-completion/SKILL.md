---
name: verification-before-completion
description: Evidence-before-claims invariant for all constellation agents; no directive may be marked complete without executed verification commands and confirmed output
wraps: verification-before-completion (vibeship)
provenance: vibeship (MIT)
vetted: 2026-02-12
pipeline_stages: [VERIFY]
---

# Verification Before Completion

## Syncrescendence Integration

**Agents:** All constellation agents (Ajna, Psyche, Commander, Adjudicator, Cartographer)

This skill is the bedrock invariant of the Syncrescendence execution pipeline. Every directive completion -- whether a plan step, a commit, a PR, or a session handoff -- must pass through the VERIFY stage before any success claim is emitted.

### How it fits the pipeline

- **VERIFY stage gate:** No downstream stage (COMMIT, MEMORY, handoff) may proceed unless verification evidence exists in the current context window.
- **Adjudicator enforcement:** The CQO (Adjudicator) treats unverified completion claims as quality violations. Agents that skip verification will have their output rejected during reviewtrospective.
- **Commander integration:** When Commander dispatches subagents via BLITZKRIEG or subagent-driven-development, each subagent independently runs verification before reporting task completion.

### Config notes

- Verification commands are task-type-dependent: `pytest`, `cargo test`, `tsc --noEmit`, `docker compose up --dry-run`, etc.
- For documentation-only changes, verification means confirming the file renders correctly and links resolve.
- The pedigree hook chain checks for verification evidence in commit metadata.

## Original Reference

@~/.agents/skills/verification-before-completion/SKILL.md

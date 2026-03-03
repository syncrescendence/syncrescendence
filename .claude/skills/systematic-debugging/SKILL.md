---
name: systematic-debugging
description: Mandatory root-cause-first debugging protocol; no fixes without investigation, no guessing without evidence
wraps: systematic-debugging (vibeship)
provenance: vibeship (MIT)
vetted: 2026-02-12
pipeline_stages: [OBSERVE, EXECUTE]
---

# Systematic Debugging

## Syncrescendence Integration

**Agents:** All constellation agents (Ajna, Psyche, Commander, Adjudicator, Cartographer)

This skill enforces a root-cause-first debugging discipline. No agent may apply a fix without first completing a structured investigation that identifies the actual cause of the failure.

### How it fits the pipeline

- **OBSERVE stage:** When a failure is detected (test failure, runtime error, unexpected behavior), the agent enters OBSERVE mode:
  1. **Reproduce** -- Confirm the failure is reproducible and capture exact error output.
  2. **Hypothesize** -- Generate candidate root causes based on the error evidence.
  3. **Isolate** -- Narrow down through targeted investigation (log inspection, bisection, minimal reproduction).
  4. **Identify** -- Pinpoint the root cause with evidence.
- **EXECUTE stage:** Only after root cause identification does the agent proceed to implement a fix. The fix must directly address the identified cause, not symptoms.
- **Adjudicator enforcement:** During reviewtrospective, the CQO checks that debugging artifacts show evidence of investigation before fix application. "Shotgun debugging" (guessing at fixes) is a quality violation.
- **Composition with verification:** After the fix is applied, `verification-before-completion` must confirm the original failure is resolved and no regressions were introduced.

### Config notes

- Debugging artifacts (reproduction steps, investigation log, root cause analysis) should be captured in commit messages or inline comments for non-trivial fixes.
- When debugging crosses agent boundaries (e.g., a Psyche infrastructure issue affecting Commander's execution), the investigating agent must document the cross-boundary dependency.
- Time-boxed investigation: if root cause is not identified within a reasonable effort, escalate with the investigation log rather than guessing.

## Original Reference

@~/.agents/skills/systematic-debugging/SKILL.md

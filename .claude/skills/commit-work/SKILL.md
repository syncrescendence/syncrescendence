---
name: commit-work
description: Commit discipline invariant with semantic prefix enforcement; ensures atomic, well-described commits across all constellation agents
wraps: commit-work (vibeship)
provenance: vibeship (MIT)
vetted: 2026-02-12
pipeline_stages: [COMMIT]
---

# Commit Work

## Syncrescendence Integration

**Agents:** All constellation agents (Ajna, Psyche, Commander, Adjudicator, Cartographer)

This skill enforces commit discipline as a pipeline invariant. Every agent that modifies tracked files must produce atomic, semantically-prefixed commits with meaningful descriptions.

### How it fits the pipeline

- **COMMIT stage:** After VERIFY passes, the agent enters the COMMIT stage. This skill governs the mechanics: staging, message formatting, atomicity, and prefix selection.
- **Semantic prefix enforcement:** All commits must use a recognized prefix:
  - `feat:` -- New capability
  - `fix:` -- Bug repair
  - `refactor:` -- Structure change, no behavior change
  - `docs:` -- Documentation only
  - `chore:` -- Maintenance, config, dependencies
  - `test:` -- Test additions or modifications
  - `arch:` -- Architecture/orchestration changes
  - `state:` -- Agent state or memory updates
- **Pedigree hook chain:** Commits feed the `pedigree` skill, which records provenance metadata (which agent, which directive, which session).
- **Adjudicator audit:** The CQO spot-checks commit messages during reviewtrospective for prefix accuracy and description quality.

### Config notes

- Commits must be atomic: one logical change per commit. Do not bundle unrelated changes.
- The commit message body should reference the directive or plan step being satisfied.
- Never commit secrets, `.env` files, or credentials. The pre-commit hook chain should catch these, but agents must also self-enforce.

## Original Reference

@~/.agents/skills/commit-work/SKILL.md

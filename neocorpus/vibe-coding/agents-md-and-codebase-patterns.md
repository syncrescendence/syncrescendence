# AGENTS.md and Codebase Patterns for AI Coding
> The emerging infrastructure for effective AI coding consists of three document types (Spec, Blueprint, Todos), AGENTS.md files as "READMEs for agents," and tactical patterns like test-first bug verification and state machine diagrams.

## Sources
02677.jsonl, 02679.md, 04450.jsonl, 03112.jsonl, 03352.jsonl, 03354.md, 09996.md, 10260.md, 10525.md, 00132.md, 00180.md

## The Three Document System
Dylan Davis ("I've built 50 apps with AI") formalized the Three Document System for AI app development (02677.jsonl, 02679.md):

1. **Spec**: what the product should do. Requirements, user stories, acceptance criteria.
2. **Blueprint**: how it should be built. Architecture, tech stack, component structure.
3. **Todos**: the task list. Atomic, pass/fail items the agent works through sequentially.

Start every project by creating these three documents before writing a single line of code. This gives the AI agent persistent context and prevents the common failure mode of agents losing track of what they are building (02679.md).

## AGENTS.md: The README for Agents
AGENTS.md is an open format to guide coding agents — "a README for agents" concept (04450.jsonl). OpenAI's internal strategy mandates creating and maintaining AGENTS.md for every project, updating it whenever the agent does something wrong or struggles with a task (00180.md).

The pattern: AGENTS.md encodes project conventions, common pitfalls, testing instructions, and behavioral guardrails that agents read before starting work. Unlike comments in code, AGENTS.md is agent-facing documentation that teaches the model how to work in your specific codebase.

## Karpathy's Guidelines for Coding Agents
Andrej Karpathy published guidelines prioritizing caution over speed, explicit planning over implicit assumptions (03112.jsonl). The philosophy: agents should plan visibly, execute cautiously, and verify outcomes — the opposite of "move fast and break things."

## The Bug Fixes Prove It Pattern
nbaschez documented the pattern (03352.jsonl, 03354.md): before implementing a bug fix, write a reproducing test first. The test must fail, demonstrating the bug exists. Then implement the fix. The test must pass, demonstrating the fix works. This constrains the agent's solution space and provides automatic verification.

This is TDD applied specifically to AI agent workflows — the agent cannot claim a bug is fixed without proof. The test is the proof.

## Tactical Patterns
**State machine diagrams** (09996.md): ask Claude to make state machine diagrams of components before building them. Forces explicit modeling of states and transitions, preventing the common AI failure mode of building happy-path-only implementations.

**Six boring rules that outperform fancy setups** (10525.md): Dylan Davis argues that simple, consistent patterns beat elaborate AI coding configurations. The rules focus on clarity, atomic tasks, and explicit constraints.

**Common AI coding mistakes** (10260.md): Theo T3 documented errors including: over-prompting (asking for too much at once), not clearing sessions between tasks (context pollution), skipping code review, and forcing AI into every task when sometimes typing is faster.

**Skills for coding agents** (00132.md): Matt Pocock runs named skills — write-a-prd, make-refactor-request, tdd, design-an-interface, write-a-skill — as reusable prompt templates that standardize agent behavior across tasks.

## Antipatterns & Lessons
- **No AGENTS.md**: without persistent agent-facing documentation, every session starts from zero. The agent makes the same mistakes repeatedly (00180.md).
- **Vague task descriptions**: "make it good" gives the agent no completion criteria. Every task needs a clear pass/fail condition (02679.md, 10525.md).
- **Skipping test-first for bug fixes**: agents will claim fixes work without proof. The reproducing test is the only reliable verification (03354.md).
- **Context pollution between tasks**: previous debugging context leaks into new feature requests. Clear sessions between tasks (10260.md).
- **Elaborate orchestration over simple patterns**: fancy multi-agent setups often underperform a human with clear documents and atomic task lists (10525.md).

## Cross-References
- neocorpus/vibe-coding/overnight-autonomous-agents.md (Ralph depends on this document infrastructure)
- neocorpus/vibe-coding/shipping-at-inference-speed.md (power-user integration of these patterns)
- neocorpus/vibe-coding/vibe-coding-tools-landscape.md (which tools support AGENTS.md and skills)

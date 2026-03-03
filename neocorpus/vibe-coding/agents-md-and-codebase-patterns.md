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

## Obsolescence and Supersession

**"Leave comments in the code" as the primary agent-communication mechanism was superseded by dedicated agent-facing documentation.** The pre-AGENTS.md assumption was that code comments, READMEs, and docstrings were sufficient orientation for any reader — human or AI. The correction: AI agents read the entire codebase but cannot infer project conventions, testing philosophy, or behavioral guardrails from code alone. AGENTS.md emerged as a distinct document category specifically because agent working memory resets every session; the human-facing README assumes accumulated context that agents do not have (00180.md, 04450.jsonl). The supersession is two-tier documentation: READMEs for humans, AGENTS.md for agents — not because they contain different information but because they assume different prior knowledge.

**"Fix it and move on" as the bug-resolution workflow is superseded by test-first verification.** The pre-agentic assumption was that visual confirmation or manual testing was adequate to verify a bug fix. When AI agents claim a fix "works," they are reporting syntactic validity and local test passage — not that the original failure mode is gone. The nbaschez pattern (03352.jsonl, 03354.md) emerged precisely because agents were producing fixes that passed their own internal check but did not address the original failure. Test-first (write a failing test before implementing the fix) is not TDD-as-ideology; it is the only reliable constraint on what "fixed" means when the agent is both fixing and verifying.

**"Elaborate orchestration beats simple patterns" was falsified by practitioners.** The early multi-agent discourse treated orchestration complexity as a proxy for capability — more agents, more tools, more routing = more powerful system. Dylan Davis's "six boring rules that outperform fancy setups" (10525.md) is the documented correction: simple, consistent patterns with atomic task lists outperform elaborate AI coding configurations. The architectural supersession runs parallel to the overnight-agents entry: most developers who believe in complex orchestration are not thinking clearly about where the actual bottleneck is. Orchestration overhead consumes coordination budget that could be used for specification.

**"Context pollution" was not recognized as a distinct failure mode until practitioners named it.** Before Theo T3 documented the pattern (10260.md) — skipping code review, over-prompting, not clearing sessions between tasks — these were experienced as individual developer mistakes rather than a structural class of agent failure. Naming "context pollution" as a specific failure mode enabled targeted countermeasure (clear sessions between tasks) rather than vague guidance to "be more careful." This follows the same pattern as dark flow: naming a mechanism enables systemic response.

## Cross-References
- neocorpus/vibe-coding/overnight-autonomous-agents.md (Ralph depends on this document infrastructure)
- neocorpus/vibe-coding/shipping-at-inference-speed.md (power-user integration of these patterns)
- neocorpus/vibe-coding/vibe-coding-tools-landscape.md (which tools support AGENTS.md and skills)

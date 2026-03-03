# Shipping at Inference Speed: How Power Users Actually Build
> The most productive vibe coders work on 3-8 projects simultaneously, commit to main, never revert, treat codebases as AI-navigable structures rather than human-readable ones, and are bottlenecked by thinking speed — not coding speed.

## Sources
09820.md, 09607.md, 09881.md, 00099.md, 00173.md, 02191.jsonl, 02193.md, 04324.jsonl, 04326.md, 10006.md, 10029.md, 10562.md, 10742.md

## The Steipete Workflow (Most Detailed Account)
Peter Steinberger (steipete) published the most granular account of high-intensity vibe coding (09820.md):

**Model selection**: GPT 5.2 Codex on high reasoning. "There's very little benefit to xhigh other than it being far slower." One model, one mode. KISS principle applied to model selection.

**Multi-project parallelism**: 3-8 projects simultaneously. One big project in focus, satellite projects chugging along. Uses Codex's queueing feature — as new ideas arrive, they enter the pipeline. Works across two Macs, sometimes editing different parts of the same project on each, syncing via git.

**No branching, no reverting**: commits to main. Sometimes Codex automatically creates a worktree and merges back, but rarely. Finds the cognitive load of managing different states unnecessary. Prefers linear evolution. "Building software is like walking up a mountain. You don't go straight up, you circle around it and take turns."

**Short prompts, images over text**: prompts have gotten shorter. Often types rather than dictates. Drags in clipped images of UI with "fix padding" or "redesign." Shows the model what is wrong rather than describing it.

**Codebase-as-AI-infrastructure**: "I don't design codebases to be easy to navigate for me. I engineer them so agents can work in them efficiently." Maintains docs/ folders, uses scripts to force models to read docs on certain topics. The more obvious the structure for what the model is trained on, the easier the work.

**No issue trackers**: tried Linear, nothing stuck. Important ideas get tried immediately. Everything else either gets remembered or was not important. Bugs get prompted immediately — faster than writing them down.

**Context management**: with GPT 5.2, no longer needs to restart sessions for new tasks. Performance stays good even with full context because the model works faster when it already has loaded many files. Compaction works well enough for multi-compact runs.

**Cross-project referencing**: "Look at ../vibetunnel and do the same for Sparkle changelogs" — references solved problems in other projects rather than re-explaining.

## The Design-First Workflow
A complementary workflow optimized for design rather than engineering (00099.md):

1. **Brain dump**: dictate into the void. Dump transcripts, conversations, everything into Claude. Unstructured. "Here's a transcript, figure it out."
2. **Scope and plan**: back and forth with Claude Code as research assistant. Kick off subtasks for web searches, CSVs, markdown files.
3. **The bad build**: AI builds a terrible design — bad structure, bad affordances, bad microcopy. But it is functionally sound and gives a better starting point than a blank canvas.
4. **Creative director**: critique the terrible build with a super-critical eye. Find all edges, edge cases, missing screens, error states. Cut down to absolute bare minimum. "The cost to switch an application away from poorly made decisions is effectively zero."
5. **Refine**: use tools like Conductor to refine UI without touching Figma. Get it functional and correctly structured.
6. **Figma handoff**: when it feels real but still needs craft — iconography, uniform components, integration with a larger application — move to traditional design tools.

The insight: "AI is terrible at design. I don't mean UI, I mean application structure, affordances, microcopy, layout... But I don't care." The bad build is generative — it reveals what the product should be by showing what it should not be (00099.md).

## The Sharing Problem
AI coding created a sharing regression (00173.md). The multiplayer canvas is gone. Prototypes live in desktop folders, screen recordings, and PRs. The solution: /share commands that spin up shareable links with feedback guides — artifact + context + feedback in one link for Slack, Linear, or wherever the team works.

## Usage Intensity Data
Vibe coding 40+ minutes per day puts a user in the top 0.01% of users by usage (04324.jsonl, 04326.md). Theo T3 documented the rapid pace of change as personally disorienting — "You're falling behind. It's time to catch up" (10029.md). His 2025 year in review: "The year I stopped writing code" (09881.md).

## Antipatterns & Lessons
- **Over-orchestrating agents**: steipete explicitly rejects multi-agent orchestration systems — the human is usually the bottleneck, and iterative exploration beats upfront planning (09820.md).
- **Plan mode as magic**: "Plan mode feels like a hack that was necessary for older generations of models that were not great at adhering to prompts." With better models, conversational planning replaces artificial mode separation (09820.md).
- **Designing codebases for human readability instead of agent navigability**: a codebase optimized for AI navigation is different from one optimized for human reading. Convention, predictability, and docs/ folders matter more than clever organization (09820.md).
- **Starting with UI instead of CLI**: "Whatever you build, start with the model and a CLI first." Agents can call CLIs directly and verify output, closing the loop (09820.md).

## Obsolescence and Supersession

**"Plan Mode" as necessary architecture superseded by conversational planning with better models.** The early generation of AI coding tools introduced Plan Mode as a distinct step — a mode where the agent reasons about approach before executing. Steipete's workflow explicitly documents this trajectory: "Plan mode feels like a hack that was necessary for older generations of models that were not great at adhering to prompts. With better models, conversational planning replaces artificial mode separation" (09820.md). What was a required architectural scaffolding for early models is becoming an optional ceremony for later ones. The supersession is model-dependent: Plan Mode remains useful for weaker models and newer practitioners, but reflects a constraint that the model frontier is eliminating.

**"Codebase optimized for human readability" as the default organizing principle is being superseded by "codebase optimized for agent navigability."** The pre-AI assumption was that codebases should be organized for human comprehension — clear naming, logical grouping, minimal cleverness. Steipete's inversion is documented explicitly: "I don't design codebases to be easy to navigate for me. I engineer them so agents can work in them efficiently" (09820.md). This is not abandoning human readability but recognizing that the primary reader is now often an agent. Convention, predictability, and docs/ folders are the new organizing principles — not because humans cannot navigate clever structures but because agents perform better in conventional ones.

**"Issue trackers as the canonical task management layer" did not survive high-velocity vibe coding.** The pre-AI workflow assumed issue trackers (Linear, Jira, GitHub Issues) as the definitive task queue — everything worth doing gets a ticket. Steipete tried Linear and nothing stuck: "Important ideas get tried immediately. Everything else either gets remembered or was not important" (09820.md). The supersession is not "issue trackers are worthless" but that the throughput rate of AI-assisted building has exceeded the throughput rate of ticketing. When building is faster than writing tickets, the ticket becomes overhead. The overnight agents entry documents the correction: structured task queues (Ralph's model) do work, but they require atomic pass/fail criteria, not open-ended issue framing.

**"Single-project focus" as optimal developer state has given way to multi-project parallelism.** The deep-work productivity model treats undivided attention on one project as the ideal — context switching destroys focus. Steipete's documented workflow of 3-8 simultaneous projects (09820.md) represents a structural inversion: when agents execute while you specify, the developer's role becomes orchestration across multiple threads rather than deep execution in one. The model: one big project in focus, satellite projects queued. The supersession is not that deep work is wrong but that the deep work is now specification — and agents handle the implementation that previously required sustained single-project focus.

## Cross-References
- neocorpus/vibe-coding/overnight-autonomous-agents.md (the autonomous extension of this workflow)
- neocorpus/vibe-coding/vibe-coding-tools-landscape.md (the tools powering these workflows)
- neocorpus/vibe-coding/agents-md-and-codebase-patterns.md (codebase infrastructure patterns)

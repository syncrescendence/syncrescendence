# Dark Flow: The Perception Gap in AI-Assisted Coding
> Experienced developers using AI tools estimated they were 20% faster but actually worked 19% slower — a 39-percentage-point perception gap that researchers link to "dark flow," a gambling-adjacent absorption state that impairs self-assessment.

## Sources
10336.md, 03187.jsonl, 03189.md, 04339.jsonl, 02263.jsonl, 10982.md, 03484.jsonl

## The METR Study
The study from METR (Model Evaluation and Threat Research) produced the most cited finding in the vibe coding discourse: experienced open-source developers using AI tools took 19% longer on tasks while believing they were 24% faster (04339.jsonl, 10336.md, 03189.md). Economics experts had forecast ~40% speedup, ML experts ~35%. The observed result was negative.

This is not a study about novices. These were experienced developers working on their own open-source codebases — the demographic most expected to benefit. The common story that AI coding tools simply make developers faster is an oversimplification (02263.jsonl).

## The Dark Flow Mechanism
Rachel Thomas (fast.ai) connected the METR finding to gambling addiction research (10336.md, 03189.md). The argument:

**True flow** in coding involves full absorption, energized focus, adequate skills for challenges, and clear performance clues within a rule-bound system. Vibe coding appears to induce this state but violates several requirements:

- Lacks clear clues on how well you are performing (both vibe coding and gambling provide misleading "losses disguised as wins")
- Challenge-to-skill matching is murky
- Creates a false sense of control

**Dark flow** (coined by gambling addiction researchers Dixon et al., 2014) describes highly absorbed focus that is not true flow. It is associated with multiline slot machine play where "loss disguised as win" outcomes create a smoother, highly absorbing state. Csikszentmihalyi defined the related concept of "junk flow."

The parallel: in vibe coding, syntactically correct but architecturally poor output feels like progress (a win) while actually creating technical debt (a loss). The developer stays in an absorbed state, shipping code without noticing that each "fix" creates new problems. The absorption itself impairs the ability to accurately assess productivity and work quality (03189.md, 10336.md).

Armin Ronacher (@mitsuhiko) described his own "agent psychosis": two months of excessive prompting, not sleeping, building tools he never ended up using — a compulsive, addictive pattern (10336.md, 03189.md).

## The 90% Plateau
Nate B Jones extended the analysis: 90% of developers plateau at level 3 of a 5-level AI coding framework. The gap between "dark factories" (organizations like StrongDM shipping production code with no human-written or reviewed code) and everyone else is the most important divide in tech (10982.md). The study found that 90% of Claude Code was written by Claude Code — yet most developers using AI get measurably slower.

The bottleneck is not implementation speed but specification quality (10982.md). Organizational structures built for human development timelines cannot absorb agentic workflows without restructuring.

## The Overpromise Pattern
Tech industry leaders have a history of overoptimistic AI predictions: Dario Amodei said 90% of code would be AI-written by September 2025 (not close). Sundar Pichai and Jeff Dean predicted everyone would use neural architecture search by 2023. Geoffrey Hinton predicted AI would replace radiologists by 2021 (03189.md, 10336.md). The appeal of vibe coding is partly driven by extrapolation about future effectiveness, but the tech industry has a long history of overpromising (10336.md).

## What AI Does and Does Not Automate
AI coding agents produce syntactically correct code. They do not produce useful layers of abstraction, meaningful modularization, conciseness, or improved organization in large codebases. We have automated coding but not software engineering (03189.md, 10336.md). There are more incorrect ways to become effective with AI coding than correct ones — calibration itself is a scarce skill (03484.jsonl).

## Antipatterns & Lessons
- **Trusting self-assessment of speed**: the 39-point perception gap is the single strongest evidence that subjective productivity reports about AI tools should be discounted. Measure, don't feel.
- **Executive mandates for AI-generated code quotas**: managers pressuring employees to meet quotas of how much code must be AI-generated, while results fall short of promises, is the organizational instantiation of dark flow (10336.md).
- **Extrapolating from current trajectory**: past overpromises do not prove future tools will fail, but they do mean current claims deserve the same skepticism (10336.md).
- **Abandoning skill development**: "Don't completely abandon the development of your current skillset" even when using AI tools every day (10336.md).

## Cross-References
- neocorpus/vibe-coding/definition-and-eras.md (vibe coding vs. AI engineering distinction)
- neocorpus/vibe-coding/disposable-software-and-limits.md (where vibe coding breaks down at scale)
- neocorpus/vibe-coding/engineer-vs-vibe-coder.md (what skills still matter)

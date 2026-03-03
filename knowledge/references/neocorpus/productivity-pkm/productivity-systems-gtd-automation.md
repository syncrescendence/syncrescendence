# Personal Productivity Systems, GTD, and Agent-Driven Automation

## Sources
- `corpus/productivity-pkm/00948.md` — REF: Todoist GTD Integration
- `corpus/productivity-pkm/09940.md` — Agent Skills Format Specification
- `corpus/productivity-pkm/03723.md` — Extraction: Automatic Discipline with OpenClaw (29 atoms)
- `corpus/productivity-pkm/11013.md` — 21 OpenClaw Prompts for Agent Self-Improvement
- `corpus/productivity-pkm/03234.md` — Extraction: How to Make Your Agent Learn and Ship While You Sleep (17 atoms)
- `corpus/productivity-pkm/04590.md` — MECH: source_anneal_pipeline
- `corpus/productivity-pkm/00231.md` — Full AI life automation audit prompt: 9 domains, 3 phases, automation impact scoring

## Core Thesis
Traditional productivity systems (GTD, Todoist workflows) and the emerging agent-driven automation stack (OpenClaw, Agent Skills) are converging. The GTD methodology (capture, clarify, organize, reflect, engage) maps directly onto the agentic workflow: agents capture input, classify tasks, route to appropriate contexts, execute at scheduled intervals, and report results. The difference is that in the agent-driven model, the human shifts from executor to supervisor — the system runs while you sleep (03234) and the human's job is to set direction, review output, and adjust configuration.

## Key Frameworks

### 1. GTD in Todoist (00948)
A reference document mapping David Allen's Getting Things Done methodology to Todoist's task management interface. Projects map to Todoist projects, next actions to tasks, contexts to labels, weekly review to a recurring task. This is the baseline: human-executed productivity methodology in a human-operated tool.

### 2. OpenClaw Automatic Discipline (03723, 11013)
OpenClaw represents the agentic evolution: agents that execute discipline automatically rather than relying on human willpower. The 29 atoms from the extraction document the architecture: agents that learn from their own outputs, self-improve through prompted reflection, and ship work on automated schedules. The 21 prompts (11013) provide the concrete toolkit for agent self-improvement. The key claim: discipline is a system property, not a character trait. Automate the discipline and the human contributes judgment, not effort.

### 3. Agent Skills Format (09940)
The specification for how agents declare and expose capabilities. A skill is a directory with a SKILL.md file containing YAML frontmatter (name, description) and markdown instructions. This is the interface contract between the human productivity system and the agent execution layer. The SKILL.md format enables composability, discoverability, and version control — the modular principle from the Eurorack architecture (see `knowledge-management-methodology.md`) applied to task execution.

### 4. Source Anneal Pipeline (04590)
A mechanical specification (blueprint-stage; not yet implemented) for processing source material through stages of increasing refinement. This bridges the PKM and productivity domains: the pipeline is both a knowledge management process (extracting, compressing, synthesizing source material) and a productivity system (automated stages with defined inputs, outputs, and quality gates).

### 5. The AI Life Automation Audit (00231)
A structured three-phase methodology for mapping automation opportunities across an entire life. Phase 1 is a conversational audit covering nine domains systematically: primary work, side hustle, personal finance, health/fitness, personal productivity, communication/relationships, home/lifestyle, learning/personal development, and content consumption. Phase 2 produces an automation map scoring each opportunity on time saved, implementation difficulty, cost, and impact level — culminating in a "Top 10 Quick Wins" prioritized by high-impact-to-low-difficulty ratio. Phase 3 delivers implementation guides (what/why/tools/how/pro-tip/setup-time/maintenance) with a phased rollout plan. The methodology enforces discipline: maximum 3-5 questions per message, domain-by-domain progression, user confirmation before advancing. The key design choice is exhaustiveness before optimization — audit everything first, then prioritize. This extends the GTD paradigm: where GTD captures and organizes tasks, the automation audit captures and maps the entire task landscape for delegation to AI or automation tools.

### 6. Agent-Learns-While-You-Sleep (03234)
The extraction documents an architecture where agents ship work on automated schedules, learn from the outcomes, and improve their own processes. The human sets direction in the morning, reviews output in the evening, and the agent handles the execution cycle in between. This is GTD's "engage" phase fully delegated.

## Synthesis
The trajectory from GTD-in-Todoist (00948) to OpenClaw-automatic-discipline (03723) traces the evolution from human-executed to agent-executed productivity. The Agent Skills format (09940) provides the interface layer, and the source anneal pipeline (04590) describes a blueprint-stage pipeline (not yet implemented) that bridges knowledge management and task execution.

The critical shift is from "human does tasks with tool assistance" to "agent does tasks with human direction." This mirrors the bottleneck shift described in the AI workflow entry (see `ai-workflow-adoption-bottlenecks.md`): when execution is automated, the bottleneck moves to clarity of direction and quality of judgment. The GTD weekly review becomes the human's primary contribution — not reviewing what was done, but redirecting what will be done next.

## Obsolescence and Supersession

**GTD's "engage" phase as the human-executed terminal step has been superseded by agent execution.** David Allen's Getting Things Done methodology (00948.md) culminates in "engage" — you do the next action. The implicit assumption throughout the methodology is that the human is the executor. The agentic evolution documented in 03234.md supersedes this terminal assumption: the agent does the execution, the human sets direction and reviews output. GTD's capture/clarify/organize/reflect phases survive and remain valuable; the "engage" phase is the specific point where agentic systems achieve structural substitution. The weekly review — traditionally a reflection on what was done — becomes redirection toward what will be done next.

**"Discipline as character trait" was superseded by "discipline as system property."** The pre-automation productivity paradigm treated discipline as an individual virtue that had to be cultivated through habit formation, accountability systems, and willpower management. OpenClaw automatic discipline (03723.md, 11013.md) represents a structural claim: discipline is a system property, not a character trait. Automate the discipline and the human contributes judgment, not effort. The supersession is not that character discipline is worthless but that it was previously the only available implementation. When infrastructure can enforce consistent behavior regardless of the human's energy state or motivation, character discipline becomes a residual rather than the primary mechanism.

**"Issue-based task management" as the coordination primitive has been challenged by agent-native queuing.** Traditional task management assumed a human reading a ticket, deciding to act, and executing. Tools like Todoist and Linear were designed for this human-mediated flow. The Agent Skills format (09940.md) — a skill is a directory with a SKILL.md file containing YAML frontmatter and markdown instructions — represents a different coordination primitive: tasks declared as machine-readable specs that agents can discover, claim, and execute without human routing. The supersession is not that issue trackers disappear but that their primary consumer shifts from humans to agents. A ticket designed for human reading and a skill designed for agent execution have different structural requirements.

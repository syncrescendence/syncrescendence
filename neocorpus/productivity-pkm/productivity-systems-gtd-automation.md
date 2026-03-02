# Personal Productivity Systems, GTD, and Agent-Driven Automation

## Sources
- `corpus/productivity-pkm/00948.md` — REF: Todoist GTD Integration
- `corpus/productivity-pkm/09940.md` — Agent Skills Format Specification
- `corpus/productivity-pkm/03723.md` — Extraction: Automatic Discipline with OpenClaw (29 atoms)
- `corpus/productivity-pkm/11013.md` — 21 OpenClaw Prompts for Agent Self-Improvement
- `corpus/productivity-pkm/03234.md` — Extraction: How to Make Your Agent Learn and Ship While You Sleep (17 atoms)
- `corpus/productivity-pkm/04590.md` — MECH: source_anneal_pipeline

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

### 5. Agent-Learns-While-You-Sleep (03234)
The extraction documents an architecture where agents ship work on automated schedules, learn from the outcomes, and improve their own processes. The human sets direction in the morning, reviews output in the evening, and the agent handles the execution cycle in between. This is GTD's "engage" phase fully delegated.

## Synthesis
The trajectory from GTD-in-Todoist (00948) to OpenClaw-automatic-discipline (03723) traces the evolution from human-executed to agent-executed productivity. The Agent Skills format (09940) provides the interface layer, and the source anneal pipeline (04590) describes a blueprint-stage pipeline (not yet implemented) that bridges knowledge management and task execution.

The critical shift is from "human does tasks with tool assistance" to "agent does tasks with human direction." This mirrors the bottleneck shift described in the AI workflow entry (see `ai-workflow-adoption-bottlenecks.md`): when execution is automated, the bottleneck moves to clarity of direction and quality of judgment. The GTD weekly review becomes the human's primary contribution — not reviewing what was done, but redirecting what will be done next.

## Open Questions
- Does full delegation of execution create a "manager without domain expertise" failure mode — the human loses touch with the work and can no longer evaluate quality?
- How does the Agent Skills format handle skill dependencies and conflicts between concurrently active skills?
- Is there a ceiling to agent self-improvement through prompted reflection, or can iterative self-modification produce genuine capability growth?

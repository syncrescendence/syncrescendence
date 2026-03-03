# Extended Thinking and Effort Control

Extended thinking is Claude Code's mechanism for allocating variable reasoning depth to tasks of different complexity. Rather than applying uniform computational effort to every prompt, the system supports a graduated spectrum from quick responses to deep multi-step reasoning, controlled through both API-level configuration and natural language signals. Understanding when and how to engage extended thinking is the difference between an agent that reflexively acts and one that deliberates before committing.

---

## Core Architecture

### The Keyword-to-Budget Mapping

Claude Code recognizes a set of natural language keywords that signal desired reasoning depth. The documented tiers form a rough escalation ladder:

| Keyword | Intent Signal | Reported Budget (disputed) |
|---------|--------------|-------------------|
| *(none)* | Standard response | Default allocation |
| `think` | Moderate deliberation | ~4,000 tokens of internal reasoning |
| `think hard` | Substantial deliberation | ~10,000 tokens of internal reasoning |
| `ultrathink` | Maximum deliberation | ~32,000 tokens of internal reasoning |

The token budgets in the table above are disputed, not settled. Source-code-verified analysis reports specific numeric allocations (4,000 / 10,000 / 31,999), but `08764` presents this as genuinely unresolved and the project's own CLAUDE.md states that keywords are "cosmetic intent signals" that do not allocate specific token budgets. Independent verification confirms only `think` and `ultrathink` as hardcoded triggers, dismissing finer-grained escalations. The table values should be read as claimed, not confirmed.

The resolution of this tension is operationally important: **treat the keywords as behavioral signals, not API switches.** They reliably produce longer, more thorough reasoning chains, but the mechanism may be behavioral compliance rather than mechanical budget allocation. The practical effect is the same — more reasoning depth — but the mental model matters when debugging unexpected behavior.

### API-Level Extended Thinking

At the API level, extended thinking is a distinct feature that allocates a separate "thinking" token budget outside the normal output budget. When enabled, the model produces an internal reasoning trace before generating its visible response. Claude Code auto-enables this feature, meaning users benefit from it without explicit configuration.

The key architectural distinction: **extended thinking produces reasoning tokens that are not visible in the final output but consume billing tokens and influence the response.** The model "thinks out loud" internally, working through implications, considering alternatives, and structuring its approach before committing to a response.

### Effort-Level Configuration

Beyond per-prompt keywords, Claude Code may support session-level effort configuration. The `--thinking-budget` flag and the maximum-wins combination rule (where per-prompt keywords can override session-level floors) are not directly established in the cited sources for this entry. [synthesis — not documented in `08764` or CLAUDE.md as cited here]

---

## Key Insights

### When Extended Thinking Earns Its Cost

Extended thinking is not uniformly beneficial. It produces measurable improvements for:

- **Architectural decisions** where the agent must reason about trade-offs across multiple dimensions simultaneously. A quick response might fixate on the first viable solution; extended thinking explores the solution space.
- **Multi-step processing** where intermediate results feed subsequent steps. The reasoning chain catches errors that would propagate through the pipeline.
- **Forensic analysis** — debugging sessions where the agent must hold multiple hypotheses simultaneously and systematically eliminate them.
- **Complex refactoring** spanning many files, where understanding the dependency graph requires sustained attention across a large context.

For simple edits, file reads, or well-specified tasks with obvious implementations, extended thinking adds latency without improving outcomes.

### Extended Thinking vs. Plan Mode

This is the critical operational distinction that practitioners must internalize:

**Extended thinking** = deeper reasoning within a single response. The model thinks harder about one step.

**Plan Mode** = exploration before execution. The model investigates the codebase, maps dependencies, and proposes a plan for human approval before making any changes.

They serve complementary purposes. Extended thinking is a depth control. Plan Mode is a workflow gate. A complex multi-file refactoring benefits from Plan Mode (to map the terrain) with extended thinking enabled during the planning phase (to reason deeply about what it finds). Using extended thinking alone for such tasks risks the agent diving deep on the wrong approach without first surveying the landscape.

### The Compounding Effect with Sub-Agents

When extended thinking is combined with sub-agent delegation, the reasoning cost multiplies — each sub-agent may independently engage extended thinking. The orchestrating agent should reserve extended thinking for coordination decisions while allowing sub-agents to use standard reasoning for bounded subtasks. This mirrors human organizational intelligence: the coordinator thinks strategically while specialists execute tactically.

---

## Anti-Patterns and Failure Modes

### Ultrathink as Default

Setting maximum reasoning depth for every prompt is the most common misuse. It increases latency by 3-10x, consumes substantially more tokens, and does not improve outcomes for well-specified tasks. The result is an agent that deliberates endlessly over trivial decisions — the computational equivalent of analysis paralysis.

### Confusing Keywords with Guarantees

The keywords are signals, not contracts. Saying `think hard` does not guarantee the model will produce exactly 10,000 reasoning tokens. It may produce fewer if the problem resolves quickly, or more if the allocated budget proves insufficient and the model continues reasoning. Building workflows that depend on exact reasoning token counts will produce brittle systems.

### Extended Thinking Without Context

Deep reasoning over insufficient context produces confident but wrong conclusions. The model will reason extensively about whatever information it has, potentially reinforcing incorrect assumptions through elaborate justification chains. **Context quality must precede reasoning depth** — load the relevant files, check the current state, then think hard.

### Ignoring the Thinking Trace

When extended thinking is enabled, the reasoning trace (visible in some interfaces) may contain the model's deliberation. The practice of reading the thinking trace as a primary debugging tool is not directly discussed in the cited sources (`08764`, `10857`, `00041`). [synthesis — not directly stated in cited sources]

---

## Implications

### For Prompt Engineering

The existence of graduated effort control means prompts should encode not just what to do but how hard to think about it. A prompt that says "refactor this function" leaves effort allocation to defaults. A prompt that says "think hard about the edge cases in this refactoring, particularly around concurrent access" both escalates effort and directs it.

### For Agent Architecture

Multi-agent systems must make effort allocation a first-class architectural concern. An orchestrator that dispatches every sub-task with `ultrathink` will burn tokens without proportional benefit. Effort should be allocated based on task complexity, error cost, and reversibility — the same heuristics humans use when deciding how carefully to check their work.

### For the Research Frontier

The disagreement between API-level budget allocation and behavioral compliance models points to a deeper question about how language models allocate internal computation. As models evolve, the relationship between explicit reasoning tokens and implicit processing may shift. Systems built on the behavioral model (keywords as intent signals) will be more robust to architectural changes than those built on the mechanical model (keywords as exact budget switches).

---

## Obsolescence and Supersession

### Uniform Effort as the Original Default

Before extended thinking existed as an explicit control, AI coding agents applied uniform computational effort to all tasks — the same reasoning depth for "rename this variable" and "redesign this authentication system." The assumption: the model's default reasoning depth is appropriate for all tasks, and the user manages complexity by prompt design rather than effort allocation.

This assumption was economically wrong in both directions: expensive for simple tasks (unnecessary computation) and insufficient for complex ones (under-reasoning on high-stakes decisions). Effort control addresses both by making reasoning depth a first-class parameter rather than a model constant.

### The Keyword-as-API Assumption and Its Correction

The `corpus/claude-code/08764.md` synthesis documents a supersession in how practitioners understand the `think` / `think hard` / `ultrathink` keywords. Early documentation and community discussion treated these as direct API switches — each keyword mechanically allocated a specific token budget. Source-code analysis (referenced in `08764.md`) appeared to confirm specific values: 4,000 / 10,000 / 31,999 tokens.

This assumption was challenged by official documentation (ChatGPT's research iteration) and confirmed by Claude Code's own CLAUDE.md: "Keywords are cosmetic intent signals — useful as session markers but they do not allocate specific token budgets." The supersession is from "mechanical API switch" to "behavioral signal." The practical effect is the same (more deliberate reasoning), but systems built on exact token count expectations will behave unpredictably because the underlying model is behavioral compliance, not mechanical budget allocation.

### The Auto-Enable Assumption

Claude Code auto-enables extended thinking at the API level. This is a design decision that superseded an earlier expectation that extended thinking would be opt-in and explicitly configured per session. The implication: users receive the benefit without explicit configuration, but they may not know the feature is active unless they read the documentation or observe the reasoning trace.

This auto-enable pattern is consistent with Claude Code's broader philosophy: configure-by-default rather than require-configuration. The cost is reduced operator visibility into what is happening; the benefit is reduced configuration overhead for the majority who want the feature but would not explicitly enable it.

---

## Source Provenance

| Source | Key Contribution |
|--------|-----------------|
| `corpus/claude-code/08764.md` | Unified research synthesis documenting the productive contradiction between keyword-as-budget and keyword-as-signal interpretations |
| `corpus/claude-code/10857.md` | Practical demonstration of extended thinking in research workflows — GPU job monitoring, SSH management, sustained multi-day reasoning |
| `corpus/claude-code/00041.md` | Tools-for-thought perspective on agent reasoning depth — external systems to think in, meta-layer reflection |
| `CLAUDE.md` (project config) | Operational doctrine: "Keywords are cosmetic intent signals — useful as session markers but they do not allocate specific token budgets" |

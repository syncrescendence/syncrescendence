# Context Window Management and Compaction

The context window is the fundamental constraint shaping every Claude Code interaction. While the nominal limit stands at 200,000 tokens, the practical operating range is considerably smaller. Performance degrades well before capacity is reached, auto-compaction destroys detail in service of continuation, and the difference between a productive session and a confused one often comes down to how deliberately the operator manages this invisible resource. Context is not storage; it is working memory, and working memory has a fidelity curve that drops long before the buffer overflows.

---

## Core Mechanics

### The 200K Illusion

Claude Code advertises a 200,000-token context window. This is a theoretical maximum, not a practical operating range. The architecture exhibits measurable quality degradation before full capacity, due to the well-documented "Lost in the Middle" phenomenon. Information positioned in the middle third of the context receives less attention than information at the beginning or end. The sources present ranges and uncertainty rather than a settled threshold: the ~75% figure and a derived effective window of 120,000-150,000 tokens are consistent with the synthesis but should be treated as estimates, not confirmed thresholds. [the sources present this as uncertain; the specific figures are not definitively established in `08764`] Operators who treat the 200K limit as a runway rather than a cliff may discover too late that quality has already degraded.

### Auto-Compaction

When context usage crosses a trigger threshold, Claude Code performs automatic compaction — a lossy summarization of conversation history that preserves high-level decisions while discarding specific details, exact wording, intermediate reasoning, and tool output verbatim content.

**Trigger thresholds** are a point of genuine disagreement across sources:
- Some report 64-75% in newer versions
- Others cite a `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` environment variable with a ~95% default
- A 25% safe buffer (triggering at ~75%) appears in multiple independent sources
- The variance likely reflects version differences and configuration options

The critical insight is that compaction is **inherently lossy by definition**. It cannot be made lossless. A summarization that preserved every detail would not reduce token count. Every compaction event destroys information — the question is whether the destroyed information was still needed.

### What Compaction Loses

Compaction reliably preserves:
- High-level decisions and their stated rationale
- File paths that were recently active
- The current task trajectory
- Configuration instructions from CLAUDE.md (re-injected, not summarized)

Compaction reliably loses:
- Exact error messages and stack traces from earlier in the session
- Intermediate reasoning chains that led to abandoned approaches
- Verbatim content of files read early in the session
- Nuanced caveats and edge cases mentioned in passing
- The emotional/tonal register of earlier conversation

The result is a kind of artificial amnesia: the agent remembers what it decided but forgets why, remembers where it was working but forgets what it saw there.

---

## Key Insights

### The Vigilance Protocol

Effective context management requires proactive monitoring, not reactive recovery. The Syncrescendence constellation enforces a two-threshold protocol [this is a Syncrescendence operational protocol derived from the constellation's constitutional documents, not a documented practice in the cited external corpus sources]:

| Threshold | Action |
|-----------|--------|
| **<30% remaining** | Alert the operator. Continue working but flag every response. |
| **<15% remaining** | Emergency handoff. Stop current work. Commit state. Non-negotiable. |

The rationale: waiting for compaction to "solve" context pressure is equivalent to waiting for amnesia to solve information overload. By the time compaction fires, the session has already been operating in degraded mode for some time.

### Sub-Agents as Context Pressure Relief

The single most effective strategy for staying within the effective operating range is delegation to sub-agents. Each sub-agent operates in its own context window; the tokens it consumes do not count against the main thread. A sub-agent that uses 50,000 tokens for research returns a compact summary to the main thread, perhaps consuming 2,000 tokens there.

In practice, this means the difference between a session hitting 60% context at feature completion versus hitting 90% partway through. The architecture effectively multiplies the available context by the number of concurrent sub-agents, minus coordination overhead.

### The Compaction Cliff

Sessions that survive one compaction event are operating on summarized history. Sessions that survive two compactions are operating on summaries of summaries. Each successive compaction amplifies information loss non-linearly. A session that has compacted three times retains only the broadest strokes of its early work — and may actively contradict decisions made in the first third of the conversation, because the reasoning that supported those decisions has been compressed beyond recognition.

This creates a practical session-length ceiling that is well below the theoretical maximum. The cited sources support the general pattern that long sessions with multiple compaction events produce degraded, internally inconsistent output, but the specific ~100,000-token threshold is not established in the sources — it is a synthesis. [synthesis — not directly stated in sources]

### Pre-Compaction Handoff

The highest-fidelity strategy for long tasks is not to fight compaction but to preempt it entirely. The sources support fresh-session strategies and structured handoffs generally. The specific 70% threshold for triggering a handoff and the "two sessions of 70% quality" framing are consistent with the sources but are synthesis rather than directly documented thresholds. [synthesis — not directly stated in sources] When a session approaches significant context utilization, the operator commits all work to disk (git commit), writes a structured handoff document capturing the full mental model, and starts a fresh session that reads only the handoff.

The handoff document is the lossless equivalent of what compaction tries to do lossily. It preserves not just what was decided, but why; not just what remains, but what traps to avoid; not just the current file state, but the operator's intent.

---

## Anti-Patterns and Failure Modes

### Riding the Ceiling

Operating continuously above 80% context, trusting that compaction will keep the session viable. The session appears functional because the agent continues producing output, but the output quality has silently degraded. This is the most common failure mode because it is invisible — there is no error message for "your agent is now operating on a lossy summary of its earlier reasoning."

### Context Stuffing at Session Start

Loading the entire project context — every relevant file, every configuration document, every historical note — into the context at session start. This consumes 40-60% of context before any work begins, leaving minimal room for the actual task. The correct approach is progressive loading: start with the minimal context needed, load additional files on-demand as the task requires them.

### Ignoring the Middle

Placing critical instructions or context in the middle of a long conversation, where the "Lost in the Middle" effect is strongest. Critical constraints belong at the beginning (CLAUDE.md, loaded first) or at the end (the most recent user message). Information in the middle third of a long context should be assumed to have reduced influence on the agent's behavior.

### Post-Compaction Confidence

Continuing work after compaction without re-reading critical files or re-establishing key constraints. The agent will proceed with apparent confidence on a foundation of summarized memory, producing plausible but potentially inconsistent output. After any compaction event, the operator should re-state critical constraints and verify that the agent's understanding of the current task still matches reality.

### Single-Thread Marathons

Attempting to complete a large, multi-phase project in a single session without sub-agent delegation or session handoffs. This guarantees multiple compaction events and progressive degradation. The session ends with the agent unable to remember its early decisions, contradicting its own earlier work, and producing output that requires extensive manual correction.

---

## Implications

Context window management is not a technical detail — it is the central architectural constraint of agentic coding. Every other capability (sub-agents, skills, hooks, MCP integrations) exists within the envelope defined by context availability and fidelity. An agent with perfect tools but degraded context is less useful than an agent with limited tools but clean, high-fidelity context.

The trajectory of Claude Code development reflects this: features like sub-agent delegation, background agents, on-demand CLAUDE.md loading, and progressive disclosure all exist primarily to manage context pressure. They are not independent capabilities but facets of a single design imperative — keep the main thread's context clean, relevant, and within the effective operating range.

For multi-agent constellations like the Syncrescendence, context management becomes a coordination problem. Each agent session is a finite resource that must be spent wisely. The handoff protocol, the two-threshold vigilance system, and the systematic use of sub-agents are not bureaucratic overhead — they are the mechanism by which a constellation of finite-context agents approximates the behavior of an unbounded intelligence.

---

## Obsolescence and Supersession

### The "Just Let It Run" Assumption

Early agentic coding practice operated on the assumption that the context window was a generous buffer — 200K tokens felt limitless compared to earlier AI systems, and the natural impulse was to let sessions run until natural completion. The assumption: a larger context window means the agent can handle more work per session without degradation.

This assumption was wrong in a specific way: it conflated *capacity* with *fidelity*. The "Lost in the Middle" phenomenon (Liu et al., 2023) established that attention is not uniform across the context window. A session at 60% capacity does not perform 40% worse than a fresh session — it performs unpredictably, with middle-positioned information receiving systematically less attention. The degradation is not at the boundary; it is distributed and invisible.

### Supersession: From Reactive to Proactive Context Management

The initial response to context pressure was reactive: let compaction fire when the threshold was crossed, trust the summary, continue. This approach assumed compaction was approximately lossless — that the summarized session was functionally equivalent to the full session.

The supersession is the recognition that compaction is lossy by definition. A system that compresses cannot preserve everything. The practical correction: pre-empt compaction rather than react to it. Structure the session to avoid reaching the compaction threshold through sub-agent delegation, progressive loading, and structured handoffs. The handoff-and-fresh-session pattern is the lossless alternative to lossy compaction.

### The Threshold Uncertainty Problem

The corpus source (`08764.md`) documents a genuine disagreement across multiple research iterations about the compaction trigger threshold — some sources cite 64-75%, others cite a ~95% default with an override variable. This disagreement reflects a period of rapid Claude Code version evolution where compaction behavior changed between releases. The current entry preserves this uncertainty honestly rather than resolving it to a false consensus.

The practical lesson from this uncertainty: do not build workflows that depend on a specific compaction threshold. Build workflows that tolerate any threshold by proactively managing context below where any known threshold sits.

---

## Syncrescendence Operational Context

The following claims derive from the constellation's operational history and constitutional documents (AGENTS.md, CLAUDE.md, memory/), not from external corpus sources:
- The specific two-threshold vigilance protocol (<30% alert / <15% emergency handoff)
- The handoff protocol as a Syncrescendence constitutional practice

## Source Provenance

| Corpus File | Content |
|-------------|---------|
| `corpus/claude-code/08764.md` | Unified research synthesis — compaction thresholds, Lost in the Middle, CLAUDE.md hierarchy |
| `corpus/claude-code/10032.md` | Progressive disclosure — token efficiency through on-demand context loading |
| `corpus/claude-code/00025.md` | Sub-agent architecture — context isolation, parallel delegation, token conservation |

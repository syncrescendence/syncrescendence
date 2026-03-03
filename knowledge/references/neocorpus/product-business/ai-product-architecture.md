# AI Product Architecture: Prompt Caching, Context Graphs, and Building for Agents

> At Claude Code, we build our entire harness around prompt caching. A high prompt cache hit rate decreases costs and creates more generous rate limits, so we run alerts on cache hit rate and declare SEVs if it is too low.

## Sources

10849.md, 11001.md, 11006.md, 03517.jsonl, 03721.jsonl, 10712.md, 10879.md, 03999.md, 02449.jsonl, 09575.md, 10644.md, 09856.md

## Prompt Caching as Core Architecture

Prompt caching is not a performance optimization — it is a foundational architectural decision that determines product feasibility (11006.md). Long-running agentic products like Claude Code are made feasible by prompt caching, which reuses computation from previous roundtrips to decrease latency and cost.

**Key lessons from Claude Code at scale** (11006.md):

1. **Prompt caching is a prefix match**: Any change anywhere in the prefix invalidates everything after it. Design the entire system around this constraint. Order matters: static content first, dynamic content last.
2. **Layout for caching**: Static system prompt and tools (globally cached) → CLAUDE.md (cached per project) → session context (cached per session) → conversation messages.
3. **Use messages instead of system prompt changes**: Updating the system prompt breaks the cache. Pass updates via messages in the next turn using system-reminder tags.
4. **Never change models mid-session**: Prompt caches are model-specific. Switching from Opus to Haiku mid-conversation costs more than keeping Opus because you rebuild the entire cache. Use subagents instead.
5. **Never add or remove tools mid-session**: Changing the tool set invalidates the entire conversation cache. Use tools to model state transitions (Plan Mode as a tool, not a tool-set swap) and defer-loading for discovery.
6. **Cache-safe forking for compaction**: When summarizing to free context, use the exact same system prompt, tools, and history as the parent conversation to get cache hits on the parent's prefix.
7. **Monitor cache hit rate like uptime**: A few percentage points of cache miss rate dramatically affects cost and latency.

## Context Graphs as Defensible Moat

"Context graphs" represent the next defensible moat for AI companies — decision traces as institutional memory (03517.jsonl). As AI agents make decisions, the accumulated context of those decisions (what was tried, what worked, what failed, in what circumstances) becomes proprietary knowledge that competitors cannot replicate by copying the model or the code.

## Agent Product Architecture Patterns

**Multi-agent architectures** (10879.md): Building teams of specialized agents where each agent has a defined role, tools, and scope. The orchestration pattern — how agents hand off work, share context, and resolve conflicts — is the product architecture.

**Skills-based product design** (03721.jsonl, 03999.md): Platforms like OpenClaw enable AI agents to manage structured workflows — such as productivity systems built on shared databases — where the agent proactively handles tasks, reviews, and check-ins. This points toward a pattern of composable agent capabilities, though marketplace distribution remains nascent.

**Agentic product workflow** (02449.jsonl): "Ralph Wiggum" style — AI agents that build product features from PRDs directly, representing a new category of agentic development workflow.

## AI Audio and New Product Categories

NotebookLM as the "Spotify of AI" — creating an entirely new product category around AI-generated audio content (09575.md, 10644.md). This represents AI creating product categories that did not previously exist, not just improving existing ones.

## AI-Native Startup Architecture

Y Combinator's new startup playbook (10849.md): startups win not by hiring faster but by automating as many internal functions as possible. Tiny teams beating companies 20x their size by building automations into every workflow — engineering, ops, customer support.

The best AI-native startups spend thousands per month on token costs instead of adding headcount. Their biggest line item is compute, not salaries (11001.md).

## Antipatterns & Lessons

- **Fragile cache ordering**: Putting timestamps in static system prompts, shuffling tool order non-deterministically, or updating tool parameters all break caching silently (11006.md).
- **Swapping tools for state transitions**: Removing tools in plan mode seems intuitive but breaks the cache. Use tools-as-state-machines instead (11006.md).
- **Ignoring cache cost of model switching**: The math is unintuitive — switching to a cheaper model mid-conversation can cost more than staying on the expensive one (11006.md).
- **Building agent systems without context accumulation**: Agent systems that do not capture decision traces lose their competitive advantage with every session (03517.jsonl).

## Obsolescence & Supersession

**The "stateless API call" assumption (superseded by session architecture)**: Early LLM product architecture treated the model as a stateless function: input prompt → output response. This is how the first generation of LLM wrappers were built — each API call independent, no state accumulated, the "session" existing only in the application layer. This assumption made prompt caching impossible to reason about, because caching only makes sense when calls have shared prefixes that recur across invocations. The session-aware architecture (static system prompt → project context → session context → messages) represents a complete structural replacement, not an enhancement. The earlier stateless frame produced architectures that were expensive, slow, and architecturally incoherent for anything beyond simple chatbots (11006.md).

**Prompt-as-string versus prompt-as-structure**: The first generation of LLM applications treated prompts as strings to be concatenated at runtime — system prompt + conversation history + current message assembled fresh each call. This was natural given the API design and the one-shot use case. The caching-optimized architecture treats prompts as structured objects with immutable prefixes and mutable suffixes, where the ordering of elements is a primary architectural decision. These are not the same paradigm: one assembles strings, the other manages cache-aware state trees. Teams that built on the string-concatenation model encounter systematic cache misses, non-deterministic cost profiles, and unexplained latency spikes when scaling — all consequences of the prior paradigm leaking into the new one.

**Context windows as scarce resource (partially obsolete)**: Early agentic product design treated context window size as the primary architectural constraint — designing entire systems around the assumption that context was the binding limit. Extended context and prompt caching together shift the binding constraint: for many use cases, cost-per-token and cache miss rate now bind before raw context window size does. Architectures designed around context scarcity (aggressive summarization, early truncation, priority-based dropping) may be solving for the wrong limit if they do not account for what those decisions cost in cache coherence (11006.md).

## Cross-References

- [AI Product Design Failures](ai-product-design-failures.md) — why most products fail before architecture matters
- [Enterprise AI Adoption](enterprise-ai-adoption.md) — how enterprises deploy these patterns
- [Software Survival Framework](software-survival-framework.md) — what architectural properties survive

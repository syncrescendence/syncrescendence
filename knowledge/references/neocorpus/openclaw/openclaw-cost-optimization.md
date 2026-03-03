# OpenClaw Cost Optimization — Definitive Treatment

**Concept**: Why OpenClaw burns money by default, and every strategy to stop it — from model tiering and intelligent routing to prompt caching, local models, and script-first architecture.
**Fused from**: corpus/openclaw/00203, 00264, 10890, 10967, 00290
**Nucleosynthesis date**: 2026-03-01 (CC65)

---

## Provenance

| Source | Signal |
|--------|--------|
| `corpus/openclaw/00203.md` | Scripts for deterministic logic (zero tokens), three-tier model strategy, cron vs heartbeats, browser automation 5x cheaper via Haiku. Swarm dispatcher saved $10-20. |
| `corpus/openclaw/00264.md` | ClawRouter: intelligent routing layer classifying request complexity. Pricing tables (Opus $5/$25/MTok vs DeepSeek $0.28/MTok). 90%+ savings on routine tasks. |
| `corpus/openclaw/10890.md` | Comprehensive playbook: the 5 cost drivers, full model pricing tables, tiered routing framework, ClawRouter, OpenRouter, prompt caching, Ollama. |
| `corpus/openclaw/10967.md` | Post-mortem: $127 burned. Six specific mistakes, daily token spend from 40,000 to 1,500. |
| `corpus/openclaw/00290.md` | Minimax M2.5 case study: 80.2% SWE-Bench, 10B active params, ~$1/hour, 3-agent production setup. 95% cost reduction. |

---

## Why OpenClaw Burns Money

OpenClaw routes everything to your primary model by default. If that model is Opus 4.6, you are paying $5/$25 per million tokens for a heartbeat check that a $0.30 model could handle identically. That is the root problem. Five architectural mechanisms compound it:

**1. Context accumulation.** Session history grows with every message. A mature session can reach 200K+ tokens. A simple follow-up question carries the full accumulated weight. The model processes all of it every time.

**2. System prompt re-injection.** SOUL.md, AGENTS.md, MEMORY.md, and skill descriptions (3,000–14,000 tokens) are re-sent with every API call. Without caching, you pay full price for the same static content on every request.

**3. Tool output storage.** File listings, browser snapshots, and command outputs get logged into session history and re-transmitted indefinitely. Each tool call expands the context that every subsequent call must carry.

**4. Heartbeat overhead.** A heartbeat running every 30 minutes on Opus triggers 48 full-context API calls per day. Each one loads context, reads HEARTBEAT.md, runs checks, reasons, and responds — even when the answer is "nothing happening." At 96 triggers/day on a 15-minute interval, heartbeats alone cost $10-20/day on Opus.

**5. Frontier models for everything.** Every task — email triage, file reads, syntax checks, "does this file exist" queries — routed to the same $5/MTok model. A Formula 1 car delivering groceries. One user's daily token spend: 40,000 tokens before fixing this. After: 1,500.

---

## The Core Principle

> **Models are expensive thinkers. Scripts are free doers.**

If a task can be expressed as deterministic logic ("if X, then Y"), it belongs in a script. Models should only engage when there is actual ambiguity — formatting for humans, deciding whether something is worth reporting, handling edge cases too complex to code.

The pattern:

**Before (token-heavy)**:
Heartbeat → Model wakes → Reads HEARTBEAT.md → Figures out what to check → Runs commands → Interprets output → Decides action → Maybe reports.
Every step burns tokens. The model is thinking about things that require no thought.

**After (token-light)**:
Cron fires → Script runs (zero tokens) → Script handles all logic → Only calls model if there is something to report → Model formats and sends.

### Real examples of the shift

| Task | Old way | New way | Savings |
|------|---------|---------|---------|
| Swarm dispatcher | Opus every 2 min checking empty queue, $0.01-0.07/tick | Native code checks queue, model only invoked when work exists | 260+ empty invocations eliminated = $10-20 saved |
| Browser automation | Opus doing the clicking, $0.089/turn, $0.15+/task | Haiku sub-agent, $0.017/turn, $0.03/task | 5x cost reduction; 168K tokens isolated from main context |
| Auth watchdog | Model checks API token validity every heartbeat | Script returns exit code 0/1, model wakes on failure only | Every-heartbeat → 6-hour cron = 12x reduction in invocations |
| Print farm monitoring | Model checks printer status every 5 minutes | Bash script diffs status, outputs only if something changed | ~50 model invocations/day → ~3 |

### Implementation rules for script-first architecture

Write scripts that output nothing on success:
```bash
#!/bin/bash
result=$(check_something)
if [ "$result" != "ok" ]; then
  echo "$result"
fi
```
Then the cron job prompt becomes: "Run the script. If there is output, send it to me. If not, stay silent."

Pre-format output in scripts — do not make the model format tables:
```bash
echo "Banking Summary"
echo "• Checking: $(get_balance checking)"
echo "• Savings: $(get_balance savings)"
```
The model's job becomes "send this" — not "understand this data and present it nicely."

Run every cron job in `sessionTarget: "isolated"`. Scheduled work should not pollute main session context.

---

## Tiered Model Routing

The canonical framework: match model capability to task complexity.

| Tier | Task type | Recommended models | Cost profile (input/MTok) |
|------|-----------|-------------------|--------------------------|
| 1 — Heartbeat/Status | Background checks, keep-alive, "is there work to do?" | Gemini Flash-Lite, Haiku 4.5, DeepSeek V3.2 | $0.075–$1.00 |
| 2 — Simple queries | Calendar, weather, file lookups, existence checks | Haiku 4.5, Kimi K2.5 | $0.20–$1.00 |
| 3 — Standard work | Coding, analysis, writing, research | Sonnet 4.5, MiniMax M2.5, Kimi K2.5 | $0.30–$3.00 |
| 4 — Complex reasoning | Multi-step planning, critical decisions, architecture | Opus 4.6 or Opus 4.5 | $5.00 |

### Model pricing reference (as of Feb 2026)

**Anthropic Claude family:**

| Model | Input ($/MTok) | Output ($/MTok) |
|-------|---------------|-----------------|
| Claude Opus 4.6 / 4.5 | $5.00 | $25.00 |
| Claude Sonnet 4.6 | $3.00 | $15.00 |
| Claude Haiku 4.5 | ~$0.80 | ~$4.00 |

**OpenAI:**

| Model | Input ($/MTok) | Output ($/MTok) |
|-------|---------------|-----------------|
| GPT-5.2 | $1.75 | $14.00 |
| GPT-5.2 Pro | $20.00 | $188.00 |

**Open-weight models (hosted APIs):**

| Model | Input ($/MTok) | Output ($/MTok) |
|-------|---------------|-----------------|
| DeepSeek V3 / V3.2 | $0.14–$0.28 | $0.28–$0.42 |
| DeepSeek R1 (reasoning) | $0.55 | $2.19 |
| Qwen3 / Qwen3-Max / Qwen3-Coder | $0.40–$1.20 | $1.20–$6.00 |
| Kimi K2 / K2.5 | $0.10–$0.60 | $2.50–$3.00 |
| MiniMax M2.5 | ~$1.00/hour at 100 tok/sec | — |

**Browser automation measured cost differential:**

- Opus: $0.089 per turn, ~$0.15+ per task
- Haiku: $0.017 per turn, ~$0.03 per task
- Result: 5x cheaper for identical mechanical work

### Assigning models per function

In cron job payloads, explicitly set the model — do not rely on defaults:
```json
{
  "payload": {
    "kind": "agentTurn",
    "message": "...",
    "model": "anthropic/claude-haiku-4-5"
  }
}
```

Verify the model name is correct. OpenClaw initially used `claude-3-5-haiku` instead of `claude-haiku-4-5`, which caused silent fallback to Opus — the most expensive model, with no error signal.

---

## Routing Tools

### Custom routing skill

Build a private skill to route common tasks to the cheapest capable model. Sample `router.py`:

```python
import re
from openclaw import Skill, Context

class RouterSkill(Skill):
    def __init__(self):
        self.rules = {
            r'code|debug|script': 'openai/gpt-5.2-turbo',        # Coding
            r'email|schedule|remind': 'anthropic/claude-3-haiku-20240307',  # Routine
            r'plan|strategy|brainstorm': 'anthropic/claude-3-opus-20240229', # Complex
            'default': 'google/gemini-flash-1.5'
        }

    async def execute(self, context: Context):
        prompt = context.message.content.lower()
        for pattern, model in self.rules.items():
            if isinstance(pattern, str) and re.search(pattern, prompt):
                context.llm_model = model  # Override for this session
                break
        return await self.next(context)
```

Enable it:
```bash
openclaw skills enable router --path skills/router.py
```

Use keywords, regex, or intent classification to detect task type, then forward to the chosen LLM via OpenClaw's configurable endpoints. Start with 2-3 task types, monitor via `openclaw logs --tail`, then expand.

### OpenRouter (300+ models, 1 API)

OpenRouter's built-in router uses prompt analysis for hands-off routing decisions. Trade-off: slight added latency. Ideal if you do not want to manage multiple provider accounts.

Config:
```yaml
llm:
  provider: openrouter
  routing:
    enabled: true
    rules:
      - task: "routine"    # Auto-detected via OpenRouter's classifier
        model: "deepseek/deepseek-chat"
        max_cost: 0.50     # $/M tokens
      - task: "coding"
        model: "openai/gpt-5.2-turbo"
      - fallback: "anthropic/claude-3-haiku-20240307"
```

### ClawRouter (OpenClaw-native)

ClawRouter is an intelligence layer that sits between OpenClaw and the AI providers. It analyzes each incoming query locally using a fast, lightweight classifier (weighted scoring on query length, presence of code, reasoning markers, multi-step intent, tool usage signals). Classification completes in milliseconds — the layer is nearly invisible to users.

Complexity tiers:
- **Simple** → cheap/fast models (DeepSeek, Gemini Flash, ~$0.27–$0.60/MTok)
- **Medium** → mid-tier (GPT-4o-mini)
- **Complex** → strong models (Claude Sonnet)
- **Heavy reasoning/agentic/multi-step** → frontier models (Opus 4.6, Kimi K2.5)

Profiles: Auto (balanced), Eco (max savings, up to 95–100% on simple queries), Premium (best quality), Free (zero-cost models).

ClawRouter reports that 90%+ of requests are simple even within multi-task prompts. Most of what your agent does does not need a $5/MTok model.

Install:
```bash
curl -fsSL https://raw.githubusercontent.com/BlockRunAI/ClawRouter/main/scripts/reinstall.sh | bash
# Fund wallet with USDC on Base — $5 is enough for thousands of requests
openclaw gateway restart
```

---

## Prompt Caching and Local Models

### Prompt caching

When you send a request to Claude or GPT, the model processes every token from scratch each time by default. Prompt caching lets the provider remember the static parts — SOUL.md, AGENTS.md, MEMORY.md, skill descriptions — so you only pay full price once per cache TTL (standard: 5 minutes; extended: 60+ minutes with Anthropic's extended retention).

For 3,000–14,000 token system prompts sent with every API call, caching reduces subsequent hits by 90%.

Config:
```json
{
  "models": {
    "anthropic/claude-opus-4.6": {
      "cacheRetention": "long",
      "cacheSystemPrompts": true,
      "cacheThresholdTokens": 2048
    }
  }
}
```

Practical application: Anthropic's extended cache stays warm for 55+ minutes. Set your heartbeat interval to 55 minutes (instead of the default 30) so every heartbeat hits warm cache. Combined with routing heartbeats to Haiku ($0.30/MTok base + $0.03/MTok cached system context), heartbeats cost ~$0.50/month instead of $100+.

### Local models via Ollama

Once hardware is paid for, every inference is free. Economically compelling for high-volume, low-complexity automation running 24/7.

When local models make sense:
- Consistent, predictable load (not bursty)
- Sensitive data that should not hit external APIs
- High-volume, low-complexity tasks (classification, routine checks, data processing)
- Spare compute available (existing server, idle gaming PC)

When they do not:
- Frontier capabilities required (extended reasoning, complex creative work, advanced coding)
- Bursty workload (idle hardware is wasted spend)
- No appetite for infrastructure management

Current community recommendation (as of Feb 2026): **Qwen3 32B** — competitive with Sonnet 3.5 on many tasks, runs at 40+ tokens/sec on a single 4090. A decked-out Mac Studio (~$14K) is required to run anything in the Opus 4.5 capability category locally.

---

## The $127 Post-Mortem

Real lessons from a user who burned $127 before fixing the following six mistakes:

**Mistake 1: Expensive model for everything.** Opus set as default for every task — heartbeat checks, file scans, cron jobs. After switching to Haiku for routine work and Opus only for complex debugging: daily token spend dropped from 40,000 to 1,500.

**Mistake 2: No guardrail rules written in stone.** OpenClaw will loop forever, forget what it was doing, and rewrite database schemas from misread comments. Explicit `SKILL.md` files in `workspace/skills/` are required — not suggestions, but laws. One file: `anti-loop.md` — "If you see the same error twice, stop and ask me. Do not try a third variation."

**Mistake 3: Sessions dying on chat close.** Sessions are stateful only while the chat window is open. Closing the laptop kills the session and loses all context and stack. For background work: OpenClaw cron jobs with `sessionTarget: "isolated"`. Each cron trigger spins up a fresh agent instance, does one task, messages results, and dies. For one-off tasks: SQLite queue paired with an hourly cron.

**Mistake 4: Too many integrations at once.** Setting up email, calendar, Telegram, web scraping, and reporting simultaneously made it impossible to isolate failures. The discipline: start with one workflow that works end-to-end before adding anything. Each new integration is a new failure mode.

**Mistake 5: Compaction erasing memory.** When the context window fills, the system compacts older messages — and forgets them. A 20-minute database schema explanation, once compacted, becomes hallucinated schema. Resolution: persist everything important to state files (JSON/YAML), workspace docs (USER.md, AGENTS.md), and decision logs that the agent reads first each session.

**Mistake 6: Chat quality ≠ agent quality.** Some models produce articulate chat responses but generate malformed JSON and hallucinate function names when calling tools. Test any candidate model with three sequential tool calls before deploying it for autonomous work.

Models that work for agentic coding: Claude Sonnet/Opus, GPT-5.2, Kimi K2 via API.
Models to avoid: DeepSeek Reasoner (brilliant at reasoning, broken tool calls), GPT-5.1 Mini (skips steps, ignores tool results).

---

## Case Study: Minimax M2.5

**Claim**: 95% cost reduction with frontier-class agentic performance.

**Benchmark performance** (as of Feb 2026):
- 80.2% on SWE-Bench Verified (on par with Opus 4.6 for coding)
- 76.3% on BrowseComp (search tasks)
- 76.8% on BFCL multi-turn (agentic tool-calling)

**Architecture**: 10 billion active parameters — smallest among Tier-1 models. Designed from the ground up for long-horizon agentic tasks: the model does not lose context or collapse midway through a 15-step workflow.

**Economics**: ~$1/hour at 100 tokens per second via hosted API. Minimax Coding Plan: $8.80/month for production-grade agentic coding. Self-hosting advantage: 10B active params makes hardware requirements tractable compared to any other Tier-1 model.

**Production 3-agent setup running entirely on M2.5**:

| Agent | Role | Capability |
|-------|------|-----------|
| Neo | AI engineer | 24/7 coding, debugging, automation — works through complex assignments independently |
| Pulse | Deep researcher | Daily 8:30 AM briefing scanning Hugging Face, GitHub trending, AI lab blogs, relevant subreddits |
| Pixel | Graphic designer | Brand-consistent educational visuals from concept descriptions |

All three agents accessed via Telegram. All running M2.5. Cost: fraction of equivalent Opus 4.6 setup.

The progression for this user: started on MiniMax M2.1 → switched to Opus 4.6 for better results → switched to M2.5 and stayed.

**Self-hosting advantage**: For anyone willing to run local inference, M2.5's 10B active parameter count makes it the first Tier-1 model that is practically self-hostable on reasonable hardware.

---

## Evolution: The Four Stages

**Stage 1 — Naive single-model**: Everything routed to one frontier model. No tiering. Costs scale linearly with usage. Bills arrive as surprises.

**Stage 2 — Manual tiering**: User consciously assigns models per task type. Haiku for cron, Sonnet for coding, Opus for complex decisions. Explicit model override in every cron payload. Requires discipline to maintain.

**Stage 3 — Intelligent routing**: ClawRouter or custom routing skill intercepts every request, scores complexity in milliseconds, routes to the cheapest capable model automatically. 90%+ savings on routine tasks without degrading output quality where it matters. ClawRouter reaches 95–100% savings on the simplest queries.

**Stage 4 — Local models + hybrid**: Ollama handles the high-volume, low-complexity tier at zero marginal cost. API models handle what local cannot. Script-first architecture eliminates the bottom tier entirely — deterministic logic runs as cron bash with no model invocation at all. Prompt caching further reduces API spend on static context.

The endpoint: 80–90% total cost reduction while improving output quality on the tasks that actually matter, because frontier model capacity is no longer diluted by grocery delivery.

---

## Configuration Checklist

- [ ] Heartbeat model: Gemini Flash-Lite, Haiku, or DeepSeek — never Opus
- [ ] Heartbeat interval: 55 minutes (aligns with Anthropic extended cache TTL)
- [ ] Browser sub-agents: spawn Haiku, not Opus; verify model name resolves correctly
- [ ] Cron jobs: `sessionTarget: "isolated"` on every scheduled task
- [ ] Script-first: any check that can be a bash if-statement is not a model invocation
- [ ] Silent by default: cron job scripts output nothing on success
- [ ] Prompt caching: enabled for system prompts above 2,048 tokens
- [ ] Guardrail files: `anti-loop.md` and equivalent laws in `workspace/skills/`
- [ ] State persistence: long-running task state in JSON/YAML, not session memory
- [ ] Model verification: test any new model with three sequential tool calls before deployment

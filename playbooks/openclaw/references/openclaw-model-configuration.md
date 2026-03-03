# OpenClaw Model Configuration & Provider Strategy — Definitive Treatment

**Concept**: Model selection, provider setup, cost architecture, and the OAuth landscape for OpenClaw agents.
**Fused from**: corpus/openclaw/00162, 08829, 08831, 10599, 10993
**Nucleosynthesis date**: 2026-03-01 (CC64)

---

## The Model Decision

Model choice is the single biggest cost lever in OpenClaw. The wrong default burns $300/week. The right tiered config runs $15-20/month.

**Agent quality ≠ chat quality.** Models must handle tool calls reliably. The community consensus (as of Feb 2026):

| Model | Agent Quality | Cost | Best For |
|-------|--------------|------|----------|
| Claude Opus 4.6 | Excellent | $5/$25 per MTok (in/out) | Complex reasoning, architecture |
| Claude Sonnet 4.5 | Very good | Moderate | Heavy lifting, code gen |
| Claude Haiku 4.5 | Good for routine | Cheap | Default daily driver, cron |
| Kimi K2.5 | Excellent | Cheap (prepaid) | Primary agent model, #1 on OpenRouter |
| GPT-5.3 Codex | Very good | Subscription-based | ChatGPT OAuth users |
| GPT-5.1 Mini | Poor for agents | Very cheap | "Pretty useless" for agent work |
| DeepSeek Reasoner | Great reasoning, broken tools | Cheap | Avoid — malformed tool calls |
| Ollama local (llama3.2:3b) | Basic | Free | Heartbeats, cron checks |

---

## Provider Setup Paths

### Path 1: Kimi K2.5 (Moonshot AI) — Recommended Primary

Kimi K2.5 is the #1 most-used model on OpenRouter for OpenClaw. Native support means no adapters or workarounds.

**During onboarding**: Select Moonshot AI → choose billing option:

| Option | Billing | Best For |
|--------|---------|----------|
| Kimi Code Plan | Fixed monthly subscription with token cap | New users, predictable costs |
| Kimi API (.ai) | Pay-per-token, international USD billing | Unlimited usage, long-running agents |
| Kimi API (.cn) | Pay-per-token, mainland China platform | CN-based users |

```bash
# Code Plan key:
# https://www.kimi.com/code/console → Create API Key

# API key (.ai):
# https://platform.moonshot.ai/console/api-keys → Create API Key
```

**Moonshot is prepaid** — you physically can't overspend. Safer than Anthropic's post-paid billing for cost control. Start with $5-10.

### Path 2: Claude via API Key

```bash
openclaw models auth add  # choose Anthropic, paste key from console.anthropic.com
openclaw models set anthropic/claude-sonnet-4-5  # or claude-haiku-4-5 for cheap default
```

**Critical**: Anthropic OAuth (Free/Pro/Max subscription) is NOT permitted in OpenClaw. Using OAuth tokens from Claude subscriptions in third-party tools violates Anthropic's Consumer Terms of Service. Anthropic reserves the right to enforce without notice. Use API key authentication only.

### Path 3: OpenAI ChatGPT OAuth — Subscription-Based

OpenAI explicitly allows ChatGPT subscription use in OpenClaw (unlike Anthropic).

```bash
openclaw onboard --auth-choice openai-codex
# Browser opens for ChatGPT OAuth sign-in
# Uses your subscription's token budget instead of pay-per-token

openclaw models set openai-codex/gpt-5.3-codex
openclaw models status --plain  # verify it stuck
openclaw gateway restart
```

This uses your ChatGPT Plus/Pro subscription budget. More cost-effective if OpenClaw is chatty, since you're not paying per-token.

### Path 4: Free Tier via NVIDIA

NVIDIA hosts Kimi K2.5 at no cost via `build.nvidia.com/moonshotai/kim`.

```bash
# Generate API key at build.nvidia.com
# Point OpenClaw to the NVIDIA endpoint
# "Just tell OpenClaw to use it" — it auto-configures alternate endpoints
```

**Limitations**: Possibly capped at ~1,000 API calls (unconfirmed). Speed reported as slower. Suitable for experimentation, not production workloads.

---

## Tiered Configuration (The Cost Doctrine)

The optimal setup uses multiple models routed by task complexity:

```bash
# Primary (90% of tasks): cheap model
openclaw models set moonshotai/kimi-k2.5
# OR: openclaw models set claude-haiku-4-5

# Fallback (rate limits, downtime):
openclaw models fallbacks add anthropic/claude-sonnet-4-5

# Manual override for complex work:
# /model sonnet  ← switches mid-session
# /model kimi    ← switches back

# Heartbeats & cron (free):
# Point to ollama/llama3.2:3b in openclaw.json
```

**Register aliases** for easy switching:
```bash
openclaw config set agents.defaults.models '{
  "moonshotai/kimi-k2.5": { "alias": "kimi" },
  "anthropic/claude-sonnet-4-5": { "alias": "sonnet" }
}'
```

---

## Evolution Narrative (Supersession Chain)

The model configuration landscape evolved rapidly in Jan-Feb 2026:

1. **Pre-rebrand (Jan 26)**: Most users defaulted to Claude Opus, burning $50-150/week. MiniMax M2.1 was the budget alternative.
2. **Manual patching era (Feb 5)**: When Opus 4.6 dropped, OpenClaw hadn't updated its model catalog. Users manually patched `models.generated.js` and `normalizeAnthropicModelId` (00162). This worked but required re-patching after every `npm update`. **Now obsolete** — OpenClaw natively supports Opus 4.6.
3. **Kimi K2.5 native support (Feb 3-4)**: Moonshot AI's Kimi K2.5 became #1 on OpenRouter. NVIDIA offered free hosting. OpenClaw added native Kimi support, eliminating adapter complexity.
4. **Anthropic OAuth ban (mid-Feb)**: Anthropic formally prohibited Claude subscription OAuth in third-party tools. OpenAI immediately positioned ChatGPT subscriptions as allowed, winning goodwill. Users migrated away from Claude subscriptions for OpenClaw; API-key billing remained available.

The lesson: the model ecosystem moves weekly. Don't lock into one provider. The multi-provider fallback architecture is not optional — it's survival.

---

## Provenance

| Source | Date | Contribution |
|--------|------|-------------|
| 00162 | Feb 5, 2026 | Manual Opus 4.6 patching procedure (OBSOLETE — preserved as supersession artifact showing pre-native-support era) |
| 08829 | Feb 4, 2026 | Official Kimi K2.5 native setup guide, three billing options (Code Plan, API .ai, API .cn) |
| 08831 | Feb 3, 2026 | Free Kimi K2.5 via NVIDIA endpoint, community discussion on limits/speed |
| 10599 | Feb 5, 2026 | Alex Finn Opus 4.6 upgrade video — agent teams feature, reverse prompt technique (no transcript, structure only) |
| 10993 | Mid-Feb 2026 | Anthropic OAuth ban analysis, OpenAI ChatGPT OAuth walkthrough, 2-step setup commands, vendor comparison |

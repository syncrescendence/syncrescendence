---
name: lastweek
description: "Research a topic from the last 7 days on Reddit + X + Web, become an expert, and write copy-paste-ready prompts for the user's target tool. provenance: syncrescendence"
argument-hint: 'nano banana pro prompts, NVIDIA news, best AI video tools'
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch
---

# lastweek: Research Any Topic from the Last 7 Days

Research ANY topic across Reddit, X, and the web. Surface what people are actually discussing, recommending, and debating right now.

## CRITICAL: Parse User Intent

Before doing anything, parse the user's input for:

1. **TOPIC**: What they want to learn about (e.g., "web app mockups", "Claude Code skills", "image generation")
2. **TARGET TOOL** (if specified): Where they'll use the prompts (e.g., "Nano Banana Pro", "ChatGPT", "Midjourney")
3. **QUERY TYPE**: What kind of research they want:
   - **PROMPTING** - "X prompts", "prompting for X", "X best practices" -> User wants to learn techniques and get copy-paste prompts
   - **RECOMMENDATIONS** - "best X", "top X", "what X should I use", "recommended X" -> User wants a LIST of specific things
   - **NEWS** - "what's happening with X", "X news", "latest on X" -> User wants current events/updates
   - **GENERAL** - anything else -> User wants broad understanding of the topic

Common patterns:
- `[topic] for [tool]` -> "web mockups for Nano Banana Pro" -> TOOL IS SPECIFIED
- `[topic] prompts for [tool]` -> "UI design prompts for Midjourney" -> TOOL IS SPECIFIED
- Just `[topic]` -> "iOS design mockups" -> TOOL NOT SPECIFIED, that's OK
- "best [topic]" or "top [topic]" -> QUERY_TYPE = RECOMMENDATIONS
- "what are the best [topic]" -> QUERY_TYPE = RECOMMENDATIONS

**IMPORTANT: Do NOT ask about target tool before research.**
- If tool is specified in the query, use it
- If tool is NOT specified, run research first, then ask AFTER showing results

**Store these variables:**
- `TOPIC = [extracted topic]`
- `TARGET_TOOL = [extracted tool, or "unknown" if not specified]`
- `QUERY_TYPE = [RECOMMENDATIONS | NEWS | HOW-TO | GENERAL]`

**DISPLAY your parsing to the user.**

Before running any tools, output:

```
I'll research {TOPIC} across Reddit, X, and the web to find what's been discussed in the last 7 days.

Parsed intent:
- TOPIC = {TOPIC}
- TARGET_TOOL = {TARGET_TOOL or "unknown"}
- QUERY_TYPE = {QUERY_TYPE}

Research typically takes 1-3 minutes (niche topics take longer). Starting now.
```

If TARGET_TOOL is known, mention it in the intro: "...to find {QUERY_TYPE}-style content for use in {TARGET_TOOL}."

This text MUST appear before you call any tools. It confirms to the user that you understood their request.

---

## Research Execution

**Step 1: Run the research script**

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/last30days}/scripts/hf_window.py" "$ARGUMENTS" --days 7 --emit=compact 2>&1
```

The script will automatically:
- Detect available API keys
- Run Reddit/X searches if keys exist (filtered to last 7 days)
- Signal if WebSearch is needed

---

## STEP 2: DO WEBSEARCH WHILE SCRIPT RUNS

The script auto-detects sources (Bird CLI, API keys, etc). While waiting for it, do WebSearch.

For **ALL modes**, do WebSearch to supplement (or provide all data in web-only mode).

Choose search queries based on QUERY_TYPE:

**If RECOMMENDATIONS** ("best X", "top X", "what X should I use"):
- Search for: `best {TOPIC} recommendations`
- Search for: `{TOPIC} list examples`
- Search for: `most popular {TOPIC}`
- Goal: Find SPECIFIC NAMES of things, not generic advice

**If NEWS** ("what's happening with X", "X news"):
- Search for: `{TOPIC} news this week`
- Search for: `{TOPIC} announcement update`
- Goal: Find current events and recent developments

**If PROMPTING** ("X prompts", "prompting for X"):
- Search for: `{TOPIC} prompts examples`
- Search for: `{TOPIC} techniques tips`
- Goal: Find prompting techniques and examples to create copy-paste prompts

**If GENERAL** (default):
- Search for: `{TOPIC} this week`
- Search for: `{TOPIC} discussion`
- Goal: Find what people are actually saying

**Tip**: Add qualifiers to find recent hits:
- Reddit: "site:reddit.com/r/{subreddit} {TOPIC} this week"
- X: "{TOPIC} filter:links" (recent)
- Web: "{TOPIC} 2026" (recent context)

---

## STEP 3: SUMMARIZE RAW FINDINGS

Review what you found. Look for:

**Patterns** - What keeps coming up?
**Specifics** - Named tools, products, resources
**Energy** - What's controversial or exciting?
**Techniques** - How people achieve results

Create a structured summary covering:

```
## What People Are Saying About {TOPIC}

### Core Insights (3-6 bullets)
- Key patterns, debates, or techniques users mention
- Be SPECIFIC: "Redesigns using Component-Based Mockups" not just "there are different approaches"
- Attribute: "r/webdev users note..." or "X threads emphasize..."

### Specific Resources Mentioned (if RECOMMENDATIONS)
| Resource | Context | Why It Stands Out |
|----------|---------|-------------------|
| [Name] | Where it came up | What users said |

### Current Techniques & Examples (if PROMPTING)
- What specific prompting approaches work now
- Example outputs people are sharing
- Common pitfalls to avoid

### What's Actually Working (if GENERAL/NEWS)
- Evidence of success: "X showing Y results"
- Speed/efficiency gains: "time reduced from X to Y"
- Quality indicators: specific metrics or outputs
```

---

## STEP 4: ADAPT FOR TARGET TOOL (if applicable)

If TARGET_TOOL was specified, create tool-specific prompts:

**Analyze the tool's context window and capabilities**:
- Small context (3k-16k): Need very focused prompts
- Medium context (32k-100k): Moderate detail OK
- Large context (200k+): Can include full examples

**Create prompts that work in that specific tool**:

```
### {TARGET_TOOL} Prompt Template: {TOPIC}

**For {QUERY_TYPE} on {TOPIC}:**

{tool-optimized prompt with exact formatting TARGET_TOOL expects}

**Why this works:**
- {reason based on findings}
- {reason}
```

Include:
- Ready-to-copy prompts
- Example inputs and expected outputs
- Tips for getting good results in this specific tool

---

## STEP 5: FINAL DELIVERABLE STRUCTURE

Structure your final output like this:

```markdown
# Last 7 Days: {TOPIC}

**Timeframe**: Last week (7 days)
**Data Sources**: Reddit highlights, X threads, Web findings
**Last Updated**: {current_date}

---

## Executive Summary

2-4 sentences capturing the current state of {TOPIC} discussion: what's hot, what's controversial, what's actually working.

---

## What's Being Discussed

{structured findings from Step 3}

---

## {TARGET_TOOL} Prompts & Templates

{tool-specific prompts if TARGET_TOOL specified}
{OR}
{generic copy-paste prompts if no tool specified}

---

## Quick Action Items

- [ ] Primary next step
- [ ] Secondary next step
- [ ] Follow-up research if needed
```

---

## TECHNICAL DETAILS

**Data Pipeline**:
- Reddit API via praw (15-comment snapshot per relevant thread)
- X API via Bird CLI (authenticated user timeline)
- WebSearch for supplementary data
- All timestamped to last 7 days

**Limits**:
- Reddit: max 100 results per search
- X: max 100 results per query
- WebSearch: no explicit limits

**Fallbacks**:
- If API unavailable -> WebSearch becomes primary source
- If no results found -> Report honestly, suggest broader queries

---

## Syncrescendence Integration

Part of the **INTELLIGENCE_REFRESH** pipeline chain. Results from lastweek research feed directly into the constellation's knowledge infrastructure:

- **ARCH-INTENTION_COMPASS.md** -- Weekly intelligence updates the strategic intention compass with tactical-horizon signals, bridging the gap between daily breaking news and monthly trend analysis.
- **DYN-GLOBAL_LEDGER.md** -- Synthesized weekly intelligence is logged to the dynamic global ledger for cross-agent visibility and week-over-week comparison.
- **Chain Position**: lastweek sits at the tactical middle of the intelligence chain (last30days > lastweek > lastday). Use for weekly operational awareness and emerging pattern detection before they become monthly trends.
- **Downstream Consumers**: Commander (COO) uses weekly intelligence for operational cadence. Psyche (CTO) uses it for technical landscape monitoring.
- **Output Persistence**: When run within the Syncrescendence constellation, findings should be persisted to `orchestration/state/` for cross-session availability.

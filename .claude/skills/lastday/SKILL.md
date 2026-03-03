---
name: lastday
description: "Research a topic from the last 24 hours on Reddit + X + Web, become an expert, and write copy-paste-ready prompts for the user's target tool. provenance: syncrescendence"
argument-hint: 'breaking news, NVIDIA announcements, AI releases'
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch
---

# lastday: Research Any Topic from the Last 24 Hours

Research ANY topic across Reddit, X, and the web. Surface what people are actually discussing, recommending, and debating in the last day.

**Optimized for**: Breaking news, fresh announcements, viral topics, and time-sensitive research.

## CRITICAL: Parse User Intent

Before doing anything, parse the user's input for:

1. **TOPIC**: What they want to learn about (e.g., "breaking NVIDIA news", "latest Claude release", "AI announcements")
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
I'll research {TOPIC} across Reddit, X, and the web to find what's been discussed in the last 24 hours.

Parsed intent:
- TOPIC = {TOPIC}
- TARGET_TOOL = {TARGET_TOOL or "unknown"}
- QUERY_TYPE = {QUERY_TYPE}

Research typically takes 30 seconds to 2 minutes. Starting now.
```

If TARGET_TOOL is known, mention it in the intro: "...to find {QUERY_TYPE}-style content for use in {TARGET_TOOL}."

This text MUST appear before you call any tools. It confirms to the user that you understood their request.

---

## Research Execution

**Step 1: Run the research script**

```bash
python3 "${CLAUDE_PLUGIN_ROOT:-$HOME/.claude/skills/last30days}/scripts/hf_window.py" "$ARGUMENTS" --days 1 --emit=compact 2>&1
```

The script will automatically:
- Detect available API keys
- Run Reddit/X searches if keys exist (filtered to last 24 hours)
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
- Search for: `{TOPIC} news today`
- Search for: `{TOPIC} announcement update`
- Goal: Find current events and recent developments

**If PROMPTING** ("X prompts", "prompting for X"):
- Search for: `{TOPIC} prompts examples`
- Search for: `{TOPIC} techniques tips`
- Goal: Find prompting techniques and examples to create copy-paste prompts

**If GENERAL** (default):
- Search for: `{TOPIC} today`
- Search for: `{TOPIC} discussion`
- Goal: Find what people are actually saying

**Tip**: Add qualifiers to find recent hits:
- Reddit: "site:reddit.com/r/{subreddit} {TOPIC} past 24 hours"
- X: "{TOPIC} filter:links" (recent)
- Web: "{TOPIC} news today" (breaking coverage)

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
# Last 24 Hours: {TOPIC}

**Timeframe**: Last day (24 hours)
**Data Sources**: Reddit highlights, X threads, Web findings
**Last Updated**: {current_timestamp}

---

## Executive Summary

2-4 sentences capturing the current state of {TOPIC} discussion: what's hot, what's breaking, what's just happened.

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
- Reddit API via praw (15-comment snapshot per relevant thread, max 24h old)
- X API via Bird CLI (authenticated user timeline, last 24h)
- WebSearch for supplementary data
- All timestamped to last 24 hours (now-86400s)

**Limits**:
- Reddit: max 50 results per search (last 24h only)
- X: max 50 results per query (last 24h only)
- WebSearch: no explicit limits

**Fallbacks**:
- If API unavailable -> WebSearch becomes primary source
- If no results found -> Report honestly, suggest broader time window (lastweek)

---

## Syncrescendence Integration

Part of the **INTELLIGENCE_REFRESH** pipeline chain. Results from lastday research feed directly into the constellation's knowledge infrastructure:

- **ARCH-INTENTION_COMPASS.md** -- Breaking intelligence provides real-time signal updates to the strategic intention compass, enabling rapid response to fast-moving developments.
- **DYN-GLOBAL_LEDGER.md** -- 24-hour intelligence snapshots are logged to the dynamic global ledger for immediate cross-agent alerting and temporal anchoring.
- **Chain Position**: lastday is the sharpest temporal lens in the intelligence chain (last30days > lastweek > lastday). Use for breaking news, urgent signals, and time-critical awareness. When lastday returns thin results, automatically suggest broadening to lastweek.
- **Downstream Consumers**: All five constellation agents consume breaking intelligence. Adjudicator (CQO) uses it for real-time quality signal detection. Commander (COO) uses it for operational urgency triage.
- **Output Persistence**: When run within the Syncrescendence constellation, findings should be persisted to `orchestration/state/` for cross-session availability.

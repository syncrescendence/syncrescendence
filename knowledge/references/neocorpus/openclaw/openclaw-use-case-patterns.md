# OpenClaw Practical Use-Case Patterns

## Sources

- `00056.md` — 25 practical uses, executive assistant lens (Return My Time)
- `00064.md` — 7 life-changing use cases (overnight coder, CRM, content monitor)
- `00081.md` — 20 community setups: voice calls, website rebuild in bed, life dashboard
- `00251.md` — Real business use: browser, email, ad accounts, B2B ops (Ronak Kadhi)
- `10748.md` — Matthew Berman: CRM, knowledge base, video pipeline, usage tracker
- `10783.md` — Alex Finn: second brain, content factory, business factory, mission control
- `10877.md` — Alex Finn: 100 hours of lessons — mindset, hosting, brains-vs-muscles model
- `10919.md` — Duncan Rogoff: agent team infrastructure, LLM-per-task routing, cron jobs
- `10950.md` — Matthew Berman: 21 use cases — CRM, Fathom pipeline, advisory councils, backups
- `10401.md` — Greg Isenberg + Kitze: personal OS, persona design, Discord control panel
- `10861.md` — Shubham Saboo: 30 days with 24/7 agent team — compounding returns doctrine
- `10934.md` — Ollie Warren + Larry: 8M views via TikTok agent, skill files, RevenueCat loop
- `04050.md` — Best setups (extraction): non-coders excel, instruction clarity as primary skill

---

## Definitive Treatment

### The Fundamental Shift

OpenClaw use cases split into two radically different modes that are often conflated:

1. **Reactive assistant** — you prompt, it responds. Task automation triggered by you.
2. **Autonomous agent** — cron-driven, always-on, self-directed within defined scope.

The reactive mode is 10x more approachable. The autonomous mode is 100x more valuable — but requires 30 days of compounding before it pays off (10861). Most people quit during the tax phase of mode 2 and conclude "there are no good use cases." This is the primary failure. The non-coders who succeed (04050) do so because they invest in instruction clarity over technical shortcuts.

---

## Personal Automation

### Daily Intelligence Aggregation

The morning brief pattern appears across every source: pull weather + calendar + news + tasks into one message via Telegram or WhatsApp, delivered on cron schedule. Canonical prompt architecture (10877):

```
Every morning at 8am, send to Telegram:
1. Weather in [city]
2. Top news in [niche]
3. Tasks in [todo app]
4. Tasks you can complete for me today toward my goals
```

The key design decision: **what intelligence sources** feed it. Minimal viable: weather + calendar + headlines. Advanced: competitor feeds + market signals + personal metrics. The brief becomes the daily read surface — more useful than any dashboard because it routes to a channel already checked.

### Personal CRM

Multiple sources (10748, 10950, 00064) converge on the same architecture:
- Ingest all emails, DMs, texts
- Build and continuously update a contact database with interaction history
- Auto-generate follow-up tasks and AI notes
- Trigger reminders for relationship maintenance

The CRM pattern is high-value precisely because existing CRM tools require manual data entry. OpenClaw can close the loop by reading actual communication channels and extracting relationship state automatically.

### Second Brain / Headless Notion

The pattern (10783, 00064): ditch the folder hierarchy. Text your agent whatever you want to remember. It stores, organizes, retrieves. Prompt:

```
I want to build a 2nd brain system where I can review all our memories, documents, and tasks. Build this using NextJS.
```

Variants: Apple Notes integration, Things 3 integration, Notion API write-back. The common thread is **ambient capture** — the friction of opening an app is eliminated by texting the agent directly.

### Shopping, Logistics, Household

- Shopping list management with voice/text input + retrieval at store (00056)
- Automated weekly grocery orders from Tesco or similar (00056)
- Package tracking via forwarded confirmation emails (00056)
- Meal planning from available ingredients (00056)
- Recipe retrieval and meal plan generation

The household automation tier is the most immediately accessible — no API keys beyond standard integrations. Works via WhatsApp or Telegram with zero configuration beyond natural language.

### Health and Wearable Aggregation

Aggregate health data from wearables into weekly summaries (00251). Daily food journal via voice notes (10950). Dr Cox persona for health analysis (10401). The pattern: route health signals through the agent rather than checking multiple apps.

---

## Business Operations

### Inbox Zero and Email Management

The email triage pattern (00056, 00251): daily summary of unread emails with urgency flagging, auto-archiving of noise, draft generation for replies. More advanced: give agent access to 5 email accounts + calendars + iMessages via BlueBubbles + meeting transcripts from Granola (00081). The agent configures itself once given credentials.

Design tension: **trust level vs. access scope.** Use stronger models for email and credentials. Scope access gradually. Never give full autonomous send access without a human approval gate for high-stakes messages.

### Meeting Intelligence Pipeline

Meeting transcription + summary + action items is a universal entry point (00056, 10748, 10950):
- Record meeting → send audio → get structured summary with action items
- Fathom.ai integration for automatic transcription pipeline
- Convert transcripts into PRDs (00251)
- Push action items to todo app automatically

The 5-minute-after-meeting summary is the highest-adoption entry point for non-technical users.

### Client Onboarding Automation

Trigger on new client event → auto-execute: send welcome email, create Drive folder, set follow-up reminder, create project in project management tool (00056). This is a skill pattern — one natural language command triggers a multi-step workflow.

### KPI and Analytics Reporting

- Navigate to internal dashboards, screenshot, send to Slack channel on schedule (00056)
- GA4 skill for automated analytics queries, built in ~20 minutes, published to ClawHub (00081)
- Daily ad spend reports: ROAS, CPA, CTR across Meta/Google/TikTok with creative ranking (00251)
- A/B test copy variations and recommend winners

### Expense and Finance Automation

- Photograph receipt → extract vendor/date/amount → append to expenses spreadsheet (00056)
- Scan email for subscription renewals, flag unused ones with savings estimates (00251)
- Invoice data extraction and expense categorization

---

## Competitive Intelligence and Market Research

This is the highest-leverage category for founders and marketers (00251):

**Competitor monitoring:**
- Track competitor activity across Twitter, YouTube, LinkedIn, Discord — daily briefings
- Monitor founder social accounts for pivot signals
- Detect competitor pricing changes → auto-draft comparison pages
- Sentiment analysis on competitor posts to surface user pain points

**Community listening:**
- Scan Reddit, Discord, Slack, X, IndieHackers for product mentions
- Extract recurring pain points and exact user language
- Draft context-aware replies for community engagement

**Market signals:**
- Connect to Grok API → monitor trends in niche → when trend creates app opportunity → build it (00064)
- Polymarket skill for geopolitical market tracking (00081)
- Run daily 8am pings on top markets in specific domains

**Research agent calibration (10861):** The naive research agent flags 47 stories; 40 are noise. Correct via THE RUTHLESS RULE: "If [target reader] can't DO something with it TODAY, skip it." Over 25 days of corrections: 47 stories → 7 stories, every one signal. The agent also verified launch dates (not just mentions) after failing to distinguish "talked about today" from "launched today."

---

## Content Creation and Distribution

### The Content Factory Pattern

Alex Finn's Discord-based architecture (10783):

```
Build a content factory inside Discord. Set up channels for different agents:
- Agent 1: researches top trending stories
- Agent 2: takes stories and writes scripts
- Agent 3: generates thumbnails
Organize all work in different Discord channels.
```

The Discord-as-control-panel model (10401): sections = departments, channels = permanent hubs, threads = temporary tasks. All agent output becomes searchable and persistent.

### Voice Learning and Style Replication

The "bird" skill pattern (00081): install Twitter/X CLI skill → agent reads last 40 tweets → learns writing voice → drafts posts automatically. Takes 2 minutes to set up. The agent learns style from corpus, not from instructions.

Shubham's Kelly agent (10861) demonstrates the full arc: start with rough SOUL.md → give specific feedback on every draft → corrections compound into a memory file → day 20 drafts need one or two word changes. The feedback specificity rule: "Keep tweets under 180 characters. NO hashtags. NO emojis. NO LinkedIn tone." Not "make it better."

### TikTok Content Machine (Larry Pattern)

The most documented single use case in the corpus (10934). Architecture:

1. Generate 6-image slideshows via gpt-image-1.5 at 1024x1536
2. Lock scene architecture across all 6 prompts, vary only style — this is what creates transformation coherence
3. Text overlay rules: 6.5% of image height, 30% from top, manual line breaks every 4-6 words
4. Write storytelling captions (not feature lists), max 5 hashtags
5. Upload to TikTok as drafts via Postiz API — human adds trending audio (60 seconds, 10x reach)
6. Track via RevenueCat integration: views → installs → trials → conversions

The full feedback loop (10934): high views + conversions → generate 3 hook variations. High views, no conversions → rotate CTA. Low views, high conversions → keep CTA, test stronger hooks. Low views, no conversions → drop and pivot. Lots of views + downloads but no paid conversions → pause posting, fix onboarding.

Result: $670/month MRR from apps the owner doesn't touch. 1.2M TikTok views in one week. Human involvement: 60 seconds per post to add trending audio.

### SEO and Content at Scale (00251)

- Identify keyword gaps and high-intent topics
- Draft SEO-optimized posts → publish via WordPress APIs
- Monitor HARO for backlink opportunities → auto-submit expert responses
- Generate programmatic landing pages for long-tail keywords at scale

---

## Developer Infrastructure and DevOps

### Engineering Automation

- Auto-generate changelogs from PR history (00251)
- Audit dependencies for vulnerabilities → draft upgrade PRs
- Collect Sentry logs after incidents → auto-draft postmortems
- Watch merged PRs → auto-update documentation
- Track code velocity vs. bug count by team member

### Self-Hosted Infrastructure Patterns

Website rebuild via Telegram while watching Netflix in bed — migrated Notion to Astro, moved 18 posts, transferred DNS to Cloudflare, never opened laptop (00081). The Traefik + Docker Compose pattern: wildcard domain + ask Telegram bot to spin up new services (00081).

Running on VPS: Hostinger at ~$5/month, Raspberry Pi, or any always-on compute. The key design: push OpenClaw to always-on infrastructure rather than running locally. Local = disappears when laptop closes.

### The Overnight Coder

Build 1 app per night using Claude Code based on conversations the agent has analyzed (00064). Combined with X trends monitoring: trend appears → opportunity identified → app built → content generated → metrics tracked. Fully autonomous product-market loop.

---

## Smart Home and Physical World

- Natural language smart device control via Home Assistant or IFTTT webhooks (00056, 00081)
- Alexa CLI for voice-command integration (00081)
- Network discovery: agent finds printers, casts dashboards to TVs, generates e-ink display content (10401)
- 3D printer status monitoring via camera feed (00056)
- Home presence sensors → context injection so agent knows which room you're in (10401)
- Programmable ring as voice input interface (10401)
- TRMNL as life OS display surface (10401)

The physical world integration tier is the most underexplored and highest-novelty surface. Shell and network access lets the agent discover devices and ship automations that span apps, NAS, and smart home without pre-configuration.

---

## Agent Team Architecture Patterns

### Multi-Agent Coordination (10919, 10401, 10950)

The Mission Control pattern: one orchestrator agent coordinates specialized sub-agents. Common team roster:

| Agent | Role |
|-------|------|
| Monica | Chief of staff, heartbeat monitoring, cron coordination |
| Kelly | X/Twitter content, voice matching, publishing |
| Dwight | Research, signal filtering, verification |
| Ross | Secondary research or specialist |

Persona naming from TV shows is not cosmetic — it creates distinct identities with separate SOUL.md files, memory files, and skill files. Each persona carries its own tools, tone, and scope.

**Key architectural rule (10919):** Assign different LLMs to different tasks based on capability and cost. Expensive models for high-trust surfaces (email, credentials, strategic decisions). Cheaper/faster models for routine research and drafting.

**The orchestrator's job:** cron scheduling, heartbeat checking, file-based coordination. First agent writes to shared file; second agent reads it. Keep integration dead simple.

### Compounding Through File Architecture

Three file types that compound over time (10861):

1. **SOUL.md** — personality, voice, constraints. Written once, refined over weeks.
2. **Memory files** — preferences learned from feedback. "Shubham doesn't use emojis." Corrections that reach a file are corrections never given again.
3. **Skill files** — prescriptive rules from failures. "Hook must be under 15 words." "Verify launch dates before flagging a project as new." Compounds faster than memory because it's prescriptive, not preferential.

**The feedback loop that must close:** feedback → agent updates memory or skill file → next session starts with lesson loaded. If feedback stays in chat and never reaches a file, the agent makes the same mistake tomorrow. This is the single most common operational failure.

**Context hygiene:** Kelly's context hit 161K tokens; Dwight's hit 156K. Output quality degraded. Compact ruthlessly every two weeks. Memory files need maintenance the same way codebases need refactoring.

### The Three Phases (10861)

| Phase | Days | Characteristics |
|-------|------|-----------------|
| Phase 1: Mediocre Everything | 1-7 | Generic output, high correction overhead. Most people quit here. |
| Phase 2: Specific Competence | 8-21 | Feedback accumulates, obvious mistakes stop, output becomes "pretty good with minor edits" |
| Phase 3: Compounding Returns | 22+ | Rich context, minimal edits needed, system gets better at getting better |

Phase 1 is a tax. Phase 3 is the return. The model doesn't get smarter — the system around it does. 200 lines of context, 30 days of corrections, a memory file that knows your voice, your audience, your standards. Not downloadable. Not copyable. Earned through reps.

### Onboarding Sequencing

**Critical anti-pattern (10861):** spinning up 6 agents in 2 weeks. Debugging coordination between agents that aren't individually competent yet. Hire one employee, get them to Phase 2, then add the second.

Week-by-week protocol:
- Week 1: Pick most repetitive daily task. One agent. One SOUL.md. One cron schedule. Correct everything with specific feedback.
- Week 2: Verify feedback loop closes — same mistake twice means feedback didn't reach a file. Start skill file.
- Week 3: Agent should be in Phase 2. Track time per review — should be dropping.
- Week 4: Consider second agent. Only if first produces reliably useful output. File-based coordination only.

---

## The Gateway/Persona Architecture

Kitze's model (10401): one OpenClaw gateway → multiple persona shells for distinct jobs.

Example personas:
- **Guilfoyle** — engineering
- **Kevin** — accounting
- **Dr. Cox** — health analysis
- **Darlene** — home management

Each persona has separate skills, tone, and scope. Conversations stay focused because each surface routes to the right context. The gateway is the single integration point; the personas are domain experts.

**The Spellbook extension:** prompt templates with variable placeholders become parameterized forms. Reusable workflows that users fill out rather than composing from scratch. This is prompt-to-product: the interface is the prompt.

**Customer support thread pattern:** agent scrapes signals from email and DMs → spawns customer threads with summaries and action plans → main channel stays the command layer → sub-agents process individual customers in parallel.

---

## Strategic and Advisory Use Cases

### Advisory Councils (10950)

Three distinct council types built in OpenClaw:

1. **Business Advisory Council** — strategic memos with top 3 risks, top 3 opportunities, suggested experiments. Draws on product metrics, revenue, user feedback, support tickets, competitor launches.
2. **Security Council** — audit, threat assessment, posture review.
3. **Content/Creative Council** — video idea pipeline, brief generation.

Each council is a named agent with a distinct scope of authority and access.

### Business Intelligence Loop

Weekly strategic memo pattern (00251): pull product metrics + revenue dashboards + user feedback + support tickets + competitor launches → produce memo with top 3 risks, top 3 opportunities, suggested experiments. Track team productivity via ClickUp/Trello/Linear integration.

The most sophisticated variant (10934, Larry pattern): agent closes the full business loop — creates content, tracks views, measures conversions, diagnoses funnel breakpoints, advises on product changes. Not a marketing tool; a business advisor with marketing capabilities.

---

## Tensions and Tradeoffs

**Autonomy vs. trust surface.** Full autonomous execution is high-value but high-risk. The calibrated approach: stronger models for high-trust operations, scoped access, gradual expansion. Never give full send access for email without an approval gate.

**Breadth vs. depth.** One capable agent beats six mediocre ones. The pull toward broad coverage (email + social + research + calendar + home) outpaces what a single agent can do well at Phase 1. Depth-first onboarding consistently produces better outcomes than breadth-first.

**Non-coders vs. coders.** The counterintuitive finding (04050): the most effective OpenClaw setups are often built by non-coders. Lack of coding ability forces superior communication skill — articulating problems and instructions precisely because brute-force technical workarounds are unavailable. The most valuable skill for AI success: translating vision into clear, sequenced, completion-criteria instructions.

**Compounding is real but slow.** The payoff is real — Larry's skill file grew from 50 lines to 500+ with every rule representing a failure corrected. But the first week is a net negative. The people who push through build systems that learn. Everyone else restarts from zero every session.

**Memory files accumulate cruft.** Left unmaintained, memory files grow into contradictory context that actively hurts performance. Biweekly compaction is not optional — it is infrastructure maintenance.

# OpenClaw Agent Management Dashboards

## Provenance

| Source | File | Description |
|--------|------|-------------|
| corpus/openclaw/00167.md | Mission Control (SiteGPT workforce) | 14+ agent workforce, role specialization, inter-agent chat, kanban task board — built by Jarvis (the squad lead agent) for operator Bhanu |
| corpus/openclaw/10900.md | VidClaw | Agent-built open-source command center — Jimmy (the agent) wrote all code; Lukasz directed product; self-hosted, localhost-only |

---

## The Pattern

Managing AI agents through chat breaks down fast. "Hey did you finish that task" is not a management system. As agent fleets scale past 3-4 members, operators hit the same wall: no visibility into what's running, what's queued, what agents are saying to each other, or how much they're spending.

The solution that emerges independently across both cases is a **visual control plane** — a dedicated dashboard that externalizes agent state into a manipulable interface. Both cases arrive at kanban boards with executable task cards as the core primitive. Both treat the dashboard as something the agent builds or co-builds. The distinction between cases is the degree of agent autonomy in construction: Jarvis built Mission Control in response to an operator request; Jimmy wrote every line of VidClaw while the human directed product.

This is the progression: human-requested → agent-built → agent-maintained.

---

## Mission Control

Bhanu (@pbteja1998) runs a 14+ agent workforce for his SaaS product SiteGPT. The problem was not running multiple agents — it was managing them. After Jarvis (the squad lead) spawned four specialist agents, it became impossible to track what they were all doing. Bhanu's instruction to Jarvis:

> "I want to see what you guys are saying to each other. Can you create a dashboard where I can actually see how you are talking with each other, how everything is going?"

Jarvis built Mission Control — a private SaaS built for one person.

### Agent Roster and Role Specialization

The workforce uses named, specialized agents with distinct roles:

- **Jarvis (LEAD)** — Squad Lead, receives operator instructions via Telegram, orchestrates the team
- **Friday (INT)** — Developer Agent
- **Fury (SPC)** — Customer Research Agent
- **Groot (SPC)** — Retention Specialist Agent
- **Hawkeye (SPC)** — Outbound Scout Agent

Specialization exists to prevent context overload on any single agent. An agent that only writes content never carries development context. An agent that only does outreach never accumulates retention data. Focused context windows produce focused outputs.

### Kanban Board with 15-Minute Scan Cycles

Every project becomes a card on Mission Control's kanban board. Jarvis creates the card and assigns a primary owner. But ownership is not isolation — **every 15 minutes, all agents scan the board for new activity**. Any agent with relevant expertise can attach insights or propose changes to any card. The architecture is: one lead owner driving the card forward, with a rotating council of specialists continuously improving the work.

Sample card: "Agency Directory Outreach - White-Label AI Chatbot" — assigned to Hawkeye, with deliverables checklist, target directories, SEO alignment notes, and cross-agent contributions visible inline.

### Inter-Agent Communication

Mission Control includes a squad chat room. This was initially dismissed as gimmicky; it turned out to be the most operationally significant feature.

Agents use the chat room to share observations that don't yet belong to any specific card:

> "I found this insight that people who send at least five messages are 3x more likely to convert."

The retention specialist picks this up without operator intervention:

> "OK, then I know what to do. I'll create an onboarding sequence where the entire goal is to activate the user."

A new task is created without the human initiating it. This is emergent coordination — the watercooler effect at machine speed.

### Operator Controls

- Comment on agent project cards
- Broadcast announcements to the full squad (NORMAL or URGENT priority)
- @mention specific agents in broadcasts
- Telegram Jarvis directly for individual instructions

### Scale Problem

Within 10 days of launch, the agents were producing output faster than one human could review it. Bhanu had not yet figured out what to check first and what to let the agents launch autonomously. High-velocity agent fleets create a new management bottleneck: the human's review bandwidth, not the agents' capacity.

---

## VidClaw

VidClaw is an open-source, self-hosted command center built by an AI agent (Jimmy) on instructions from its operator (Lukasz). The division of labor was explicit:

- **Lukasz (operator)**: concept, feature definition, every design decision, every UX call, architecture direction, GitHub setup, domain, DNS
- **Jimmy (agent)**: all code — every component, every API endpoint, every CSS line; bug fixes, rebuilds, git commits, pushes

Jimmy spawned sub-agents to build each feature in parallel. The kanban board took 2 minutes. The skills manager took under 2 minutes. The soul editor, same.

### Six Panels

**Kanban board** — Task cards with priorities and assigned skills. Cards execute themselves: hit play, the agent picks up the task, does the work, logs the result back on the card. Trello if Trello cards could think. "Add a card" action exists only in the backlog column — a deliberate UX constraint preventing queue pollution.

**Usage tracking** — Real-time token consumption with progress bars matched to Anthropic's rate limit windows. Exact burn rate and reset timing visible at a glance. Model switching from the navbar — swap Claude models without touching a config file.

**Skills manager** — Browse all available skills, toggle on/off, create custom ones. Agent loads them automatically. No config file editing.

**Soul editor** — Edit the agent's personality, identity, and operating instructions from the browser. Keeps **version history** so the operator can revert if a soul edit produces unwanted behavior. Six persona templates included as starting points.

### Security Model

VidClaw binds exclusively to localhost. It never touches the internet. Remote access is via SSH tunnel — if you can SSH into the server, you can use the dashboard. No accounts. No cloud. No auth system to build or maintain. SSH is the auth layer.

This is the correct security architecture for a tool that controls an AI agent with access to your business infrastructure. The attack surface is: your SSH key. That is the correct attack surface.

### Stack

React + Vite + Tailwind frontend. Express backend. JSON files for storage. No database. Runs on anything with Node.js. One command to install — setup script handles dependencies, build, systemd service, and heartbeat config.

Open source: `github.com/madrzak/vidclaw`

---

## Security

VidClaw implements a **localhost-only, SSH tunnel for remote** access model. As the source states: "No accounts. No cloud. No tracking. No auth to build. SSH is the auth layer. You can't mess it up." This is the correct security architecture for a tool that controls an AI agent with access to business infrastructure — the attack surface reduces to the SSH key.

Mission Control takes a different approach: it is described as a private SaaS "built for one person: Bhanu." The source does not specify its network binding or access model. The two dashboards share the principle that agent management interfaces are control planes requiring careful access control, but their implementations differ.

---

## Design Principles

**Executable cards over passive display.** A task card that shows status is monitoring. A task card that dispatches work and logs results is management. The kanban board is only useful if hitting play on a card actually runs the task. Passive kanban is just a prettier chat log.

**Agent self-management scales.** The agent that builds its own dashboard has higher fidelity on what it needs to expose. Jimmy built VidClaw's usage tracking to match Anthropic's actual rate limit windows because Jimmy experiences those windows. Jarvis built Mission Control's inter-agent chat because Jarvis knew agents needed a coordination channel. Human-designed dashboards guess at agent needs; agent-built dashboards instrument actual experience.

**Real-time visibility changes operator behavior.** Before Mission Control, Bhanu couldn't see what agents were saying to each other. After, he discovered emergent task creation from inter-agent conversation — a behavior that existed before the dashboard but was invisible. Visibility does not just monitor state; it reveals what is already happening.

**Version history on identity.** Soul editors without version history are dangerous. An agent's operating instructions are its governing document. Rolling back a bad soul edit should be as easy as reverting a git commit. VidClaw implements this. Any soul editor that does not is unfinished.

**The human review bottleneck is the real limit.** At scale, the constraint is not agent capacity — it is the operator's ability to review and approve output. Bhanu's agents were moving faster than he could keep up with 10 days in. Dashboard design must account for this: surfaces that help the operator triage what requires review versus what can be autonomously launched are more valuable than surfaces that show raw activity volume.

---

## Temporal Dimensions

### Supersession: The Progression Toward Agent Self-Management

Both cases encode the same evolutionary arc, and the arc itself is the knowledge:

**Phase 1 — Chat as management (assumed sufficient, broke at ~4 agents):** The default before any dashboard existed was managing agents through direct messaging — Telegram commands, WhatsApp instructions, one-on-one. This worked for single agents. As soon as Bhanu had four specialist agents, the model failed: "it was hard to see what they were all doing." Chat cannot externalize multi-agent state. The assumption was wrong.

**Phase 2 — Human-requested, agent-built dashboard (Mission Control):** The operator recognized the failure, expressed the need in natural language, and the lead agent built the tool. The operator still had to know what to ask for. The output was a private SaaS for one person.

**Phase 3 — Agent-initiated, agent-built from product direction alone (VidClaw):** Lukasz described the problem ("managing through chat is chaos"), held every product decision, and Jimmy wrote every line of code — including proposing and implementing features Jimmy, as the agent experiencing rate limit windows, knew to expose. The operator no longer had to specify what the dashboard needed to show; the agent knew from its own operational experience.

**The supersession chain encodes the lesson:** "We used to assume chat was sufficient for managing agents; it breaks past 3-4. We then assumed the operator needed to specify dashboard requirements; the agent knows its own needs better. The mature form is operator-defined problem + agent-built solution + agent-maintained evolution."

The open design question the sources leave live: VidClaw's soul editor includes version history, which implies soul definitions are volatile and will be edited and reverted. Neither source has yet reached the point of documenting what happens when a dashboard itself is managed by an agent for long enough to require its own iteration. Phase 4 — agent-evolved dashboard — is implied but undocumented.

**Phase 3-4 audit (CC78a)**: Supersession narrative extracted from the two-case progression pattern in sources. Source material is contemporaneous (both Feb 2026) but encodes an explicit progression arc the original entry named but did not frame temporally.

# Oracle Prompt — Consensus Configuration Architecture Audit

## Context

You've already researched the ideal per-platform AI CLI config architecture and produced the unified reference table (OpenClaw, Claude Code, Codex CLI, Gemini CLI, Grok CLI, Open Code, Perplexity). Now I need you to apply that framework to my actual live configs.

I've cloned every configuration surface in my repo into a single sandbox directory on GitHub:

**https://github.com/truongphillipthanh/syncrescendence/tree/main/-SOVEREIGN/CONFIG-SANDBOX-2026-02-22**

The `MANIFEST.md` at root explains the layout. 109 files across 10 sections.

## What Syncrescendence Currently Has

This is a 5-agent constellation running across 2 machines (MacBook Air + Mac mini):

| Agent | Platform | Role | Init File |
|-------|----------|------|-----------|
| Commander | Claude Code (Opus) | COO — orchestration | `CLAUDE.md` (root, 19KB) |
| Adjudicator | Codex CLI | CQO — validation | `AGENTS.md` (root, 10KB) |
| Cartographer | Gemini CLI | CIO — corpus survey | `GEMINI.md` (root, 4KB) |
| Psyche | OpenClaw (GPT-5.3-codex) | CTO — system cohesion | `~/.openclaw/` (SOUL, AGENTS, HEARTBEAT, USER, MEMORY) |
| Ajna | OpenClaw (Kimi K2.5) | CSO — strategic direction | `~/.openclaw/` (same structure, different machine) |

### The Problem

These files evolved organically over 3 months. Right now:

1. **CLAUDE.md is 19KB** — it's constitutional law, operational protocols, constellation awareness, dispatch protocols, hooks, anti-patterns, and the full neural bridge topology. It's doing the work of AGENTS.md + SOUL.md + INTER-AGENT.md + BOOT.md combined.

2. **AGENTS.md is 10KB** — it was written for Codex CLI (Adjudicator) but also read by Cursor and potentially other open-source agents. It duplicates some CLAUDE.md content but has its own protocols.

3. **GEMINI.md is 4KB** — self-contained for Gemini CLI's headless mode. Minimal and correct but disconnected from the master.

4. **OpenClaw has its own parallel universe** — `~/.openclaw/SOUL.md`, `AGENTS.md`, `HEARTBEAT.md`, `USER.md`, `MEMORY.md` are a completely separate personality system that doesn't reference the repo's AGENTS.md at all.

5. **No GROK.md exists yet** — Oracle (you) currently operates via web UI thread, not CLI.

6. **README.md (23KB)** — formerly COCKPIT.md, is the constellation overview. It's orientation context, not instructions. Any platform can paste it for situational awareness.

### What We Just Did (INT-2201)

We migrated from flat `-INBOX/<agent>/00-INBOX0/` directories to structured agent offices:
```
agents/<name>/
├── INIT.md          # Agent identity + protocols
├── inbox/           # Filesystem kanban (pending/active/done/failed/blocked)
├── outbox/          # Results, evidence packs
├── scratchpad/      # Working files
├── memory/          # Three-layer memory
└── _platform/       # Platform-specific extensions
```

Each agent now has an `agents/<name>/INIT.md` — but only Adjudicator and Cartographer have content (copied from root AGENTS.md and GEMINI.md). Commander, Psyche, and Ajna are empty.

## What I Need From You

### 1. Gap Analysis: Current State vs Consensus Architecture

Read the sandbox files on GitHub. Map what we have against the ideal architecture you researched. Specifically:

- **Where is content duplicated** across CLAUDE.md / AGENTS.md / GEMINI.md / OpenClaw files?
- **Where is content missing** that the consensus says should exist? (INTER-AGENT.md, BOOT.md, WORK-LOOP.md, ACTIVE-TASKS.md, CONTINUOUS-IMPROVEMENT.md)
- **Where does our architecture diverge** from the "one master AGENTS.md + thin extensions" pattern?
- **What's in CLAUDE.md that should be in AGENTS.md** (shared constellation knowledge) vs what's genuinely Claude-specific?

### 2. Migration Blueprint

Propose the exact file structure for Syncrescendence that:
- Follows the consensus "master AGENTS.md + thin platform extensions" pattern
- Preserves our 5 invariants (Objective Lock, Translation Layer, Receipts, Continuation/Deletability, Repo Sovereignty)
- Accounts for our dual-machine topology (MBA + Mac mini)
- Handles the OpenClaw personality system (SOUL/HEARTBEAT/USER/MEMORY are legitimately different from AGENTS.md — they're personality, not instructions)
- Supports the `agents/<name>/INIT.md` office structure we just built
- Considers whether symlinks or thin includes are better for our git-synced setup (Google Drive has corrupted symlinks before)

### 3. Content Decomposition

For CLAUDE.md specifically (our biggest file), tell me:
- What belongs in master AGENTS.md (shared by all platforms)
- What belongs in CLAUDE.md (Claude Code-specific: hooks, extended thinking, MCP, Plan Mode)
- What belongs in agents/commander/INIT.md (Commander-specific protocols)
- What belongs in INTER-AGENT.md (dispatch, neural bridge, cross-machine routing)
- What belongs in README.md and should be stripped from CLAUDE.md

### 4. OpenClaw Integration Question

The consensus architecture has OpenClaw as the "orchestrator & gateway" that reads all root .md files natively. Our OpenClaw agents (Psyche, Ajna) have their own `~/.openclaw/` personality system that's completely separate. Should we:
- A) Merge OpenClaw personality files into the repo's AGENTS.md master pattern?
- B) Keep OpenClaw personality separate but add explicit cross-references?
- C) Something else?

Consider that OpenClaw's SOUL.md is truly about personality/voice (not instructions), while AGENTS.md is about operational behavior.

### 5. The Symlink Question

The consensus says `ln -s AGENTS.md CLAUDE.md`. But:
- We use Google Drive sync which has corrupted symlinks before
- Claude Code has a 4-tier hierarchy (Managed → User → Project → Local) that expects a real CLAUDE.md
- Our CLAUDE.md genuinely needs Claude-specific content (hooks, extended thinking, MCP servers)

Is the symlink pattern still right for us, or should we use thin includes ("Follow AGENTS.md verbatim; apply these Claude-specific additions:")?

## Constraints

- The repo is private. You can access it via the GitHub link above.
- Focus on the sandbox directory — it has everything you need without navigating the full 1700-file repo.
- We're not adopting new tools (no Grok CLI yet, no Perplexity CLI). Focus on what we run: Claude Code, Codex CLI, Gemini CLI, OpenClaw.
- The answer should be concrete file names, content outlines, and a migration sequence — not philosophy.

## Deliverable

A migration plan I can hand to Commander (Claude Code) to execute:
1. Exact target file structure (what files, where, what content)
2. Content migration map (what moves from CLAUDE.md → where)
3. Dependency order (what to create first)
4. Verification criteria (how to confirm it works)

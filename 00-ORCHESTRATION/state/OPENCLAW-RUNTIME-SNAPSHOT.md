# OpenClaw Runtime Snapshot

- Captured: `2026-03-02T02:33:02Z`
- Agent focus: `ajna`
- Primary model: `anthropic/claude-sonnet-4-5`
- Workspace path: `/Users/system/.openclaw/workspace`
- Browser enabled: `True`
- Tools denied: `exec, process, apply_patch`
- Installed skills: `playwright-mcp`
- Gateway: `bind=loopback` `port=18789` `mode=local`

## Channels

- `discord` enabled: `False`
- `slack` enabled: `False`

## Workspace Excerpts

### AGENTS.md
```md
---

# Syncrescendence — Operational Law

**Version**: 7.0.0
**Last Updated**: 2026-02-28
**Authority**: Constitutional — all agents inherit this file verbatim via `make configs`.

## Identity

This is Syncrescendence, a civilizational sensing infrastructure demonstrating AI-amplified individual capability at institutional scale. You are executing directives as part of a multi-agent coordination system (the Constellation).

## Five Invariants (Constitutional Law)

These are non-negotiable axioms. They cannot be suspended, overridden, or traded away.

1. **Objective Lock** — No work begins until the objective is explicitly confirmed by the Sovereign. Ambiguity is not a license to interpret; it is a signal to clarify.
2. **Translation Layer** — All outputs must be intelligible without retransmission. If the Sovereign must re-explain your output to another platform, the output failed.
3. **Receipts (Closure Gate)** — No completion claim without artifacts committed to the repository. "I did the work" without a commit is a claim without evidence.
4. **Continuation/Deletability** — Any conversation must be deletable without losing system state. All durable knowledge lives in the repo, not in threads.
5. **Repo Sovereignty** — The repository is ground truth; web apps are cache. When state conflicts between a platform and the repo, the repo wins.

---

## Constitutional Rules

### Structural
1. **FLAT PRINCIPLE**: Directories are flat. Sanctioned exceptions: `00-ORCHESTRATION/state/`, `engine/02-ENGINE/`, `corpus/<topic>/` (22 semantic folders), `neocorpus/<topic>/` (mirrors corpus/ structure), `canon/sn/`, `ascertescence/oracle/`, `ascertescence/canon-remediation/`, `agents/commander/outbox/handoffs/`, `-INBOX/commander/00-INBOX0/`.
2. **SEMANTIC DIRECTORIES**: Top-level directories: `corpus`, `neocorpus`, `canon`, `engine`, `agents`, `00-ORCHESTRATION`, `ascertescence`, `memory`, `-INBOX`. Do not create new top-level directories without Sovereign approval.
3. **PROTECTED ZONES**: `canon/` requires explicit Sovereign approval for deletions.

### Operational
4. **VERIFICATION BEFORE COMPLETION**: Never claim done without running verification commands.
5. **COMMIT DISCIPLINE**: Commit frequently with semantic prefixes (feat:, fix:, docs:, chore:, refactor:).
6. **SOURCES VS GENERATED**: AGENTS.md is the source. CLAUDE.md and GEMINI.md are generated via `make configs`. NEVER edit generated files directly.

---

## Directory Structure

```
corpus/              Knowledge corpus (5,954 files across 22 semantic topic folders)
  NUCLEOSYNTHESIS-MAP.md   Classification authority
  <topic>/SUBCATEGORY-INDEX.md   Ranganathan faceted indexes (5 largest folders)
neocorpus/           The compendium — definitive nucleosynthesis entries, one per concept
  <topic>/           Mirrors corpus/ folder structure (currently: openclaw/)
canon/               Verified canonical knowledge (PROTECTED, 164 files)
  sn/                Syncrescript notation
engine/              Prompts for agent dispatch
  02-ENGINE/         Subcategory/audit prompts
agents/              Agent offices
  commander/outbox/handoffs/   Session handoffs (HANDOFF-CC{N}a.md = CRUSH lane, CC{N}b.md = tool stack lane)
00-ORCHESTRATION/    Strategic coordination
  state/             Implementation backlog + map
ascertescence/       Triangulation session artifacts
  oracle/            Oracle prompts + responses
  canon-remediation/ Canon remediation passes
memory/              Operational state (burndown, logs, legacy handoffs)
-INBOX/              Commander inbox for triangulation responses
  commander/00-INBOX0/
```

**Config generation**: `make validate` checks source/manifests/path coherence. `make configs` renders harness-specific outputs into `configs/`. `make reconcile` refreshes `CLAUDE.md` and `GEMINI.md` from the rendered tree on the current machine.
Current live runtime state for tool-stack reconciliation is tracked separately in `00-ORCHESTRATION/state/TOOL-STACK-LIVE-STATE.md`.
```

### MEMORY.md
```md
# Ajna Memory — Current Runtime State

## Current State
- OpenClaw install: 2026.2.26 clean rebuild, now partially rewired
- Model: Claude Sonnet 4.5 primary
- Workspace: /Users/system/.openclaw/workspace
- Repo root: /Users/system/syncrescendence
- Gateway: live on 127.0.0.1:18789
- Browser: enabled
- Playwright MCP skill: installed
- Slack: disabled after attempted setup; bot token believed valid, app token stale
- Discord: disabled after attempted setup

## Standing Orders
- Repo is ground truth; if runtime and repo disagree, reconcile into repo
- Tool stack authority: engine/CC65-TOOL-STACK-FINAL.md
- Current implementation order: engine/CC72b-IMPLEMENTATION-BRIEF.md
- Fortress dispatch protocol: compress on send, expand on receive

## Near-Term Priorities
- Use the repo-managed deploy/sync loop instead of letting workspace state drift
- Distill runtime changes into repo state and memory instead of leaving them only here
- Keep OpenClaw workspace deployment conservative while normalization rules mature
- Use the next Oracle round to resolve exocortex↔ontology bridge sequencing, not settled Ajna questions
```

# IMPLEMENTATION-BACKLOG.md

> Queue of implementation paths (normalized) ready to map into Linear.
> Source of truth remains the repo; Linear is an execution surface.

## 2026-02-05 (Tranche A)

### P0
- IMPL-A-0008 — CANON-31150 rewrite (platform catalog expanded + deconflated)
- IMPL-A-0010 — DYN-TOOLCHAIN_INTERACTION_PROTOCOL.md
- IMPL-A-0002 — Chorus vs Medley correction (COCKPIT)

### P1
- IMPL-A-0001 — Fix outdated extended thinking guidance (CLAUDE.md)
- IMPL-A-0004 — Self-healing constitution hook
- IMPL-A-0005 — Git worktree isolation as canonical parallelism
- IMPL-A-0007 — Ralph Pattern implementation verification + canonical doc

### P2
- IMPL-A-0006 — Skill subagent delegation (`context: fork` guidance)
- IMPL-A-0009 — Missing avatar specs (OpenClaw / Commander)
- IMPL-A-0014 — MCP buildout plan (Slack/Linear)
- IMPL-A-0015 — Velocity management rules + budget alerts

### P3
- IMPL-A-0012 — Linear reconciliation design + sync spec
- IMPL-A-0013 — FDIS requirements + deployment surface

## 2026-02-06 (Tranche A) — Four-Systems operationalization

### P0
- IMPL-A-0019 — System 4 triage & qualification SOP + schema (signal_tier, value_modality)

### P1
- IMPL-A-0016 — System 1 scheduled monitoring runner + brief artifact output
- IMPL-A-0017 — System 2 ‘save-to-queue’ capture protocol + processor to 04-SOURCES/processed/
- IMPL-A-0021 — Executable interaction state machine (entrypoints → triage → route)

### P2
- IMPL-A-0018 — Research packet template + tool routing rules (System 3)
- IMPL-A-0020 — Value-modality decision tree → processing function mapping
- IMPL-A-0023 — DecisionAtom: automation substrate (launchd/cron vs n8n vs OpenClaw cron)
- IMPL-A-0025 — Verify/create missing cross-ref docs (SOURCES_SCHEMA/TRIAGE_PROTOCOL/PROCESSING_ROUTING)
- IMPL-A-0026 — Operator command reference / make targets per system

### P3
- IMPL-A-0022 — Automation milestones (M0→M2) + acceptance tests per system
- IMPL-A-0024 — System↔IIC stream mapping (default recipients, cadence, SLA)

## 2026-02-06 (Tranche B) — Twin coordination + Intent Compass mechanics + Dispatch Kanban

### P0
- IMPL-B-0009 — Establish -OUTBOX/<agent>/ structure + align watcher RESULT receipts + relay rule to -OUTGOING
- IMPL-B-0010 — Kanban schema linter: Kind gating + header validation (safety rail)

### P1
- IMPL-B-0006 — Intent Compass triage SOP (queue → compass flush semantics + cadence)
- IMPL-B-0001 — Sovereign contact rules as enforceable decision gate (notify reason required)
- IMPL-B-0012 — Wrong-agent prevention: enforce To + Claimed-By hostname + stale-claim scan

### P2
- IMPL-B-0002 — Durable TWIN handoff surface + indexing/ledger for twin relays
- IMPL-B-0004 — TWIN-UPDATE template + linter
- IMPL-B-0007 — INT ID generator/authority + uniqueness enforcement
- IMPL-B-0008 — Compass resolution requires evidence/integrated_into
- IMPL-B-0011 — Ledger policy for lifecycle completeness (add BLOCKED/WAITING if needed)
- IMPL-B-0005 — make twin-heartbeat command that emits update stub
- IMPL-B-0003 — Psyche contribution protocol (PATCH bundles/branches; Ajna commits)

## 2026-02-06 (Tranche C) — Canon hotspots: multi-agent orchestration + memory systems + tech stack DB

### P0
- IMPL-C-0012 — Tech Stack DB migration execution + integrity checks + receipt
- IMPL-C-0006 — Memory taxonomy mapping to concrete repo artifacts (working/episodic/semantic/procedural/prospective)

### P1
- IMPL-C-0001 — Orchestration-patterns → Syncrescendence mapping + router
- IMPL-C-0005 — Progressive trust ladder for lanes (allowed actions + promotion criteria)
- IMPL-C-0010 — Memory verification gates + stale/deprecated markers + re-verify policy

### P2
- IMPL-C-0002 — DecisionAtom: default collaboration topology + allowed deviations/triggers
- IMPL-C-0003 — Protocol posture: MCP vs A2A vs filesystem kanban (security + roadmap)
- IMPL-C-0004 — Message schema headers integrated into TASK header format
- IMPL-C-0007 — Context engineering policy (chunking/relevance/decay/summarization)
- IMPL-C-0008 — Sleep-time compute jobs (cron/launchd) for memory maintenance
- IMPL-C-0011 — Memory security policy (PII handling + audit)
- IMPL-C-0013 — Minimal Tech Stack DB CLI for search/routing/compare

### P3
- IMPL-C-0009 — Memory interface operations (write/read/update/forget) with logging
- IMPL-C-0014 — Tech Stack DB maintenance cadence as jobs
- IMPL-C-0015 — Tech Stack DB acceptance tests + metrics report

## 2026-02-06 (Tranche D) — Makefile + GitHub connector protocol

### P0
- IMPL-D-0071 — Makefile verify/update-ledgers missing-file tolerant (no hard failures)
- IMPL-D-0078 — Ensure connector entrypoints exist + are current (create CHATGPT.md if missing)
- IMPL-D-0079 — DecisionAtom: ground truth precedence (desktop vs GitHub main)

### P1
- IMPL-D-0076 — Token generation cross-platform clipboard fallback (no pbcopy hard dependency)
- IMPL-D-0077 — Add ops-health umbrella target + improve help for intelligence targets
- IMPL-D-0082 — Receipts enforce write-path: commit hash + files changed + push confirmation

### P2
- IMPL-D-0072 — Root .md allowlist check (structure verification)
- IMPL-D-0073 — Guard sources.csv reads in update-ledgers
- IMPL-D-0074 — tree target fallback if tree missing
- IMPL-D-0075 — clean target safety review/dry-run
- IMPL-D-0080 — DecisionAtom: branching policy (single-branch vs short-lived branches/PRs)
- IMPL-D-0081 — Connector navigation playbook in each platform entrypoint

## 2026-02-06 (Tranche D) — Script surfaces: verify/lint/triage/canon regen

### P0
- IMPL-D-0089 — regenerate_canon.py machine-readable regenerated IDs (enables truthful regen logs + ledger REGEN)
- IMPL-D-0083 — verify_all.sh allowlist mismatch fix + missing-file tolerance hardening

### P1
- IMPL-D-0087 — triage_outgoing.sh: lane-folder truth + header mismatch detection
- IMPL-D-0085 — ops_lint.sh: validate kind/id conventions + YAML parse + id uniqueness
- IMPL-D-0090 — remove jinja2 auto-install; preflight dependency policy

### P2
- IMPL-D-0084 — verification missing-file policy (error vs warn)
- IMPL-D-0086 — expand lint coverage beyond 02-ENGINE (or add scoped linters)
- IMPL-D-0088 — triage deps: rg fallback + install guidance

## 2026-02-06 (Tranche D) — intent_compass / dispatch / canon watch

### P0
- IMPL-D-0101 — watch_canon regen log: actual regenerated CANON IDs (remove 31150 hardcode)
- IMPL-D-0102 — watch_canon concurrency lock (no overlapping regen)

### P1
- IMPL-D-0095 — dispatch.sh creates full kanban lane set (00/10/20/30/40/50/90/RECEIPTS)
- IMPL-D-0096 — dispatch.sh Kind validation
- IMPL-D-0105 — watch_canon ledger REGEN events (trigger/status/ids)

### P2
- IMPL-D-0091 — intent_compass signals ruleset + tests
- IMPL-D-0093 — intent_compass atomic append/lock
- IMPL-D-0092 — intention queue correlation_id + richer capture
- IMPL-D-0094 — jq dependency preflight/rate-limited warn
- IMPL-D-0097 — -OUTBOX/<agent>/{RESULTS,ARTIFACTS} existence policy
- IMPL-D-0098 — timeout semantics standardized + Kind defaults
- IMPL-D-0099 — dispatch template aligns with ‘folder is canonical state’ doctrine
- IMPL-D-0100 — ledger DISPATCH reliability (warn/stub)
- IMPL-D-0103 — watch_canon --diagnose (critical missing watch_paths)
- IMPL-D-0104 — watch_canon daemon-safe dependency preflight

## 2026-02-06 (Tranche D) — Always-on watchers readiness

### P0
- IMPL-D-0036 — Watchers must auto-write RESULT receipts to -OUTGOING (durable proof of execution)
- IMPL-D-0037 — Unblock mini executors: install OpenClaw, fix Codex auth, resolve Claude billing for Commander

### P1
- IMPL-D-0038 — watcher_health.sh (launchctl+env+binary+log+ledger health report)
- IMPL-D-0039 — Align dispatch task contract vs watcher behavior (RESULT vs logs)
- IMPL-D-0041 — Self-test/precheck at watcher start (prevent false "running" health)

### P2
- IMPL-D-0040 — Standardize NODE_OPTIONS/NODE_NO_WARNINGS across watcher plists (mini + psyche)
- IMPL-D-0034 — Two-set watcher plist install (mini/home vs psyche/system) kept deterministic
- IMPL-D-0035 — Mini home base path hardcode to /Users/home (policy)


## 2026-02-06 (Tranche D) — Outfitment sync (Ajna ↔ Psyche)

### P0
- IMPL-D-0044 — SSH alias + host-key pinning procedure for Ajna↔Psyche (unblock rsync sync)
- IMPL-D-0045 — Fix Ajna OAuth dir missing (~/.openclaw/credentials) and add preflight

### P1
- IMPL-D-0047 — Deterministic parity smoke test: invoke workspace skill on Ajna and return PASS/FAIL receipt
- IMPL-D-0046 — Make sync_openclaw_skills.sh robust across remote usernames/paths (flags + receipts)

### P2
- IMPL-D-0049 — rearm_watchers verification step prints resolved paths + loaded labels
- IMPL-D-0048 — Add BLOCKED status / classifier to watcher lifecycle to distinguish env blockers from task failure
- IMPL-D-0050 — Ajna git stash hygiene: audit + policy


## 2026-02-06 (Tranche D) — Kanban + watcher hardening follow-ons

### P0
- IMPL-D-0051 — Executor wall-clock timeout + BLOCKED classification + RESULT on timeout
- IMPL-D-0055 — Truthful CANON regen log (actual IDs) + ledger REGEN events
- IMPL-D-0059 — watch_canon regen log writes actual regenerated CANON IDs
- IMPL-D-0060 — Ledger REGEN events emitted by watch_canon (include IDs + trigger)
- IMPL-D-0062 — watch_canon concurrency lock (avoid overlapping regen)

### P1
- IMPL-D-0052 — Enforce Kind gating (TASK/SURVEY/PATCH only)
- IMPL-D-0053 — RESULT path determinism (prefer Expected Output header)
- IMPL-D-0054 — Log hygiene: no long-form diagnostics in watcher stderr

### P1
- IMPL-D-0067 — Makefile verify/update-ledgers: existence checks + align with verify_all
- IMPL-D-0065 — verify_all.sh: fix root .md allowance mismatch + explicit allowlist

### P2
- IMPL-D-0056 — watch_canon --diagnose (missing watch_paths detection)
- IMPL-D-0061 — watch_canon --diagnose mode (missing watch_paths detection + nonzero on critical missing)
- IMPL-D-0057 — make ops-health aggregator target
- IMPL-D-0068 — make ops-health: lint + verify-full + watcher_health (when available)
- IMPL-D-0069 — make canon-watch / canon-watch-once targets
- IMPL-D-0063 — ops_lint: validate kind/id conventions + YAML parse
- IMPL-D-0064 — ops_lint: detect duplicate ids across artifacts
- IMPL-D-0066 — verify_all.sh hardening: set -euo pipefail + missing-file resilience
- IMPL-D-0070 — verify JSON output mode for dashboards/health checks
- IMPL-D-0058 — Kanban protocol: integration hooks section (SaaS subscriptions)

## 2026-02-09 (Tranche F) — Toolchain alignment + Neo-Blitzkrieg + Intentions

### P0
- IMPL-F-0001 — Rosetta Stone updates: add OpenClaw/Codex/Gemini terms (#170–180) + update related entries
- IMPL-F-0002 — CANON-31150 regeneration protocol (JSON source → generated markdown)

### P1
- IMPL-F-0007 — Slack/Linear MCP server buildout (or alternatives) + config templates + threat model note
- IMPL-F-0009 — Temporal intelligence refresh pipeline spec (cadence + expiration warning frontmatter)
- IMPL-F-0010 — Triage pending meta-intentions into concrete task definitions (reports canonization; tmux; HighCommand; session discipline)

### P2
- IMPL-F-0003 — Neo-Blitzkrieg “Toolchain Alignment” micro-cycle template (Stream A/B/C task stubs + receipts)
- IMPL-F-0005 — FDIS v0 requirements + Modal 1 field node spec + acceptance checks
- IMPL-F-0006 — SN ↔ Foundry Ontology impedance mismatch memo
- IMPL-F-0008 — Session budgeting spec (token/cost burn thresholds + alert surfaces)
- IMPL-F-0012 — DecisionAtom addendum: map Four-Systems automation to substrate ownership (OpenClaw/launchd/n8n)

### P3
- IMPL-F-0004 — Gemini CLI API key setup on Account 2 + non-interactive preflight receipt (blocked on key)
- IMPL-F-0011 — DecisionAtom: revenue target reset (new deadline + leading indicators) (needs Sovereign ratification)

## 2026-02-09 (Tranche G) — Rosetta + Kanban + Intentions mechanics

### P0
- IMPL-G-0008 — Kanban lint gating: validate Kind/Kanban/Reply-To/Receipts-To + watcher-safe prefixes

### P1
- IMPL-G-0009 — Fix twin relay surface drift (replace stale -INBOX/outputs references with canonical path)
- IMPL-G-0003 — Five Invariants disambiguation (explicit list + override semantics in CLAUDE.md)

### P2
- IMPL-G-0004 — Memory Crystal protocol (token-economic session compaction artifact)
- IMPL-G-0005 — Adversarial Validation checklist + routing rule (Oracle/Augur for disproof)
- IMPL-G-0006 — Temporal versioning/decay metadata + refresh scanner (align w/ temporal pipeline)
- IMPL-G-0007 — Syncrescript terminology migration (docs updated; tooling remains sn_*)
- IMPL-G-0010 — Intentions triage hardening: cadence + INT id allocator + ‘resolved requires evidence’ lint

### P3
- IMPL-G-0001 — Medley/Chorus glossary + doc sweep (COCKPIT + ops)
- IMPL-G-0002 — Complete Ring→sigma rename + sigma/tau glossary/migration note

## 2026-02-10 (Follow-up Tranche I)

### P0
- IMPL-I-0002 — Execute Tech Stack DB migration (choose backend; locate CSVs; integrity checks; receipt)

### P1
- IMPL-I-0001 — CANON-31150 regeneration protocol documentation + e2e verification
- IMPL-G-0008 — Kanban lint gating (Kind/Kanban/Reply-To/Receipts-To; watcher-safe prefixes)

### P2
- IMPL-I-0003 — corpus_health_check.py scheduled execution (launchd/cron + alerting)
- IMPL-G-0009 — Fix twin relay surface drift (canonical -OUTBOX/<agent>/ARTIFACTS/ path)

### P3
- IMPL-I-0004 — Twin handoff indexing (INDEX.md in -OUTBOX/ + doc update)

## 2026-02-10 (Tranche J — Canon Hotspots: Five-Account + Multi-Agent + Memory + Seven-Layer)

### P0
- IMPL-J-0002 — Coherence IIC synthesis pipeline with weekly handoff automation
- IMPL-J-0006 — Multi-agent topologies: planner-executor, critic-refiner, specialist swarm runners

### P1
- IMPL-J-0001 — Acumen IIC daily brief automation and Red Alert routing
- IMPL-J-0007 — MCP vs A2A vs filesystem-kanban protocol DecisionAtom + prototype
- IMPL-J-0008 — Memory taxonomy → repo artifact mapping (working/episodic/semantic/procedural/prospective)

### P2
- IMPL-J-0003 — Efficacy IIC task triage and velocity tracking
- IMPL-J-0004 — Mastery IIC curriculum YAML schema and spaced repetition integration
- IMPL-J-0009 — Memory system evaluation (A-MEM/MIRIX/MemGPT) for local deployment
- IMPL-J-0011 — Seven-Layer sovereignty configurations (device → meta-intelligence)

### P3
- IMPL-J-0005 — Transcendence IIC reflection prompts and values alignment
- IMPL-J-0010 — Context compression: chunking, relevance, decay, summarization automation
- IMPL-J-0012 — Differential sovereignty: human judgment vs automation decision matrix

## 2026-02-10 (Tranche K — New Material: SaaS Integrations + Memory Audit + Sensing)

### P0
- IMPL-K-0003 — Jira Cloud API migration (/rest/api/3/search → /rest/api/3/search/jql)
- IMPL-K-0006 — Memory portability audit script (lock-in risk scoring + migration recs)
- IMPL-K-0010 — Linear ↔ IMPLEMENTATION-MAP bidirectional sync

### P1
- IMPL-K-0001 — Airtable ontology.db sync (bidirectional, rate-limited)
- IMPL-K-0002 — Seed Airtable tables (Platforms, Models)
- IMPL-K-0004 — Todoist v1 API integration (v2 deprecated)
- IMPL-K-0005 — Todoist ↔ ClickUp GTD bridge
- IMPL-K-0007 — Memory export automation (Claude, ChatGPT, Gemini, Notion MCP, Mem0, Graphiti)
- IMPL-K-0011 — Ecosystem health monitoring (all SaaS APIs)

### P2
- IMPL-K-0008 — Frontier scanning automation (paradigm shift detection)
- IMPL-K-0009 — Corpus staleness detection + refresh queuing

## 2026-02-10 (Tranche L — Operational Recalibration: Atomicity + Wiring)

### P0
- IMPL-L-0001 — Restore REF-WEB_APP_MEMORY_AUDIT.md (Ajna sync casualty)
- IMPL-L-0002 — Clear uncommitted DYN-* files (Receipts invariant violation)
- IMPL-L-0003 — Wire SYN-31 sensing templates into claudecron Phase 2

### P1
- IMPL-L-0004 — Advance SYN-16: T1a↔T2 bridge (14.2% → 25%+)
- IMPL-L-0005 — Ajna sync coordination guard (prevent destructive deletions)

## 2026-02-10 (Tranche M — MCP Decisions + Sensing Progress)

### P0 (Sovereign Decision Required)
- IMPL-M-0001 — Jira MCP approval + Scrum board conversion
- IMPL-M-0002 — Todoist MCP approval + frozen project decision (Option A/B/C)
- IMPL-M-0003 — Airtable MCP approval

### P1
- IMPL-M-0004 — Todoist weekly review cadence (auto/manual/hybrid)
- IMPL-M-0010 — Activate sensing launchd agents (in progress; 3 plists created)
  - corpus-staleness: Mon 05:30
  - frontier-scan: Sun 06:00
  - linear-impl-sync: daily 07:30

### Decision Required
**Sovereign**: Review -SOVEREIGN/DECISION-BATCH-MCP-ONBOARDING.md
**Actions**: Provide "APPROVED ALL" signature for MCP installation batch, or individual decisions per MCP.

## 2026-02-10 (Tranche N — Jira Sync + Launchd Activation)

### P0
- IMPL-N-0001 — Implement jira_linear_sync.py (bidirectional sync via REF-JIRA_SYNC_MAP)
- IMPL-N-0010 — Commit and activate all 12 launchd agents (complete M-0010)

### P1
- IMPL-N-0002 — Automate status sync using transition IDs

### Progress Note
- Jira↔Linear sync map documented (REF-JIRA_SYNC_MAP.md)
- 12 launchd plists ready (sensing + existing agents)
- Next: Load agents and verify scheduling

## 2026-02-16 (Tranche Q — Research Corpus Insights: Exocortex + Memory + Security)

*Source: 59 articles deep-read across 8 notebooks. Extracted from RESEARCH-INSIGHTS-VERY-HIGH-SIGNAL.md + RESEARCH-INSIGHTS-HIGH-SIGNAL.md.*

### P0
- IMPL-Q-0001 — Progressive Disclosure Layer for Vault: Implement 4-layer context loading (tree → YAML descriptions → outlines → full content) with frontmatter descriptions on all vault notes (INT-1701)
- IMPL-Q-0002 — SHIELD.md Security Policy: Create SHIELD.md for all OpenClaw agents, populate from MoltThreats threat intelligence (INT-1709)
- IMPL-Q-0003 — OpenClaw Security Audit: Run `clawdbot security audit --fix` on Ajna + verify Miessler Top 10 checklist (gateway auth, DM allowlist, sandbox, network isolation)
- IMPL-Q-0004 — Hook Audit of CLAUDE.md: Identify all instructions that should be hooks (deterministic checks). Promote verified patterns: instruction → skill → hook (INT-1705)

### P1
- IMPL-Q-0005 — Three-Layer Memory System for OpenClaw: Knowledge Graph (entities), Daily Notes (timeline), Tacit Knowledge (MEMORY.md) with automated heartbeat extraction (INT-1707)
- IMPL-Q-0006 — Claim-Named Notes Migration: Rename vault notes from topic-style to claim-style titles — file tree becomes table of arguments
- IMPL-Q-0007 — Vault Index Pattern: Single file listing every note with one-line description, scanned FIRST before any note reading
- IMPL-Q-0008 — Verbatim Trap Test as Mandatory Checkpoint: Every research synthesis must produce something the source didn't contain. Enforce via hook or skill gate
- IMPL-Q-0009 — Memory Decay Engine: Hot/Warm/Cold tiering for entity summaries with weekly synthesis cron, access tracking, frequency resistance
- IMPL-Q-0010 — Enable Agent Teams on MBA: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, test peer-to-peer coordination alongside tmux cockpit
- IMPL-Q-0011 — PreToolUse Hooks: Intercept `git commit` to enforce clarescence-format messages, prevent commits to protected paths, auto-lint
- IMPL-Q-0012 — Path-Scoped Rules: Migrate per-domain instructions into `.claude/rules/` with path scoping (orchestration.md → 00-ORCHESTRATION/**)
- IMPL-Q-0013 — Tailscale ACL Tags: Separate MBA (Ajna) from Mac mini (Psyche), directional restrictions, workers cannot initiate to orchestrator (INT-1712)

### P2
- IMPL-Q-0014 — Observational Memory Integration: Evaluate Mastra's @mastra/memory (94.87% LongMemEval) for conversation compression into priority-tagged observations
- IMPL-Q-0015 — QMD Local Search Integration: Deploy QMD for hybrid BM25 + vector search across vault collections (SQLite-based, fully local)
- IMPL-Q-0016 — Correction-Based Knowledge Capture: System where agent corrections during normal work auto-generate persistent knowledge items
- IMPL-Q-0017 — Daily OpenClaw Supply Chain Audit Cron: Diff all changed files, audit for obfuscated code/suspicious network calls, SAFE/CAUTION/BLOCK report
- IMPL-Q-0018 — Formalize One-Writer-Many-Readers: Document pattern in ARCH-CONSTELLATION with explicit write targets and read sources per agent
- IMPL-Q-0019 — Read-Only Subagents: Security boundary for untrusted content ingestion — ingest and return structured summaries, cannot execute/edit
- IMPL-Q-0020 — Refactor skills to progressive disclosure: Move heavy reference content to references/ subfolder, add validation scripts in scripts/
- IMPL-Q-0021 — OpenClaw Personality File Alignment Audit: Verify SOUL, USER, MEMORY, AGENTS, HEARTBEAT cross-file coherence + add negative constraints

### P3
- IMPL-Q-0022 — Evaluate 4-Table Closed Loop (proposals/missions/steps/events) for kanban dispatch evolution
- IMPL-Q-0023 — Evaluate LobeHub as prototyping/design surface complementing OpenClaw execution layer
- IMPL-Q-0024 — Minority Report Agent Dashboard: Kanban-style live status board with color-coded task cards, progress bars
- IMPL-Q-0025 — Confidence-Scored Memory: Implement 5 memory types (insight, pattern, strategy, preference, lesson) with confidence scores and 30% influence ratio

### P1 (Addendum — Orphan Resolution, per Adjudicator Audit)
- IMPL-Q-0026 — File-First Architecture Enforcement: Codify plain-markdown-as-source pattern across vault. Validated by ClawVault benchmark (markdown+grep 74.0% vs specialized tools 68.5%). Enforce file ownership and grep-discoverability for all knowledge assets (INT-P017)
- IMPL-Q-0027 — Anti-Tool-Shaped-Object Gate: Institutionalize "what is the number before making it go up?" as mandatory pre-adoption gate. Prevent false productivity loops from tools that look useful but don't serve mission. Framework: purpose → metric → baseline → tool → re-measure (INT-1704)
- IMPL-Q-0028 — Tool-Shaped System Audit: Audit existing infrastructure for anti-patterns — tools adopted for perceived productivity without mission linkage, deprecated systems still running, false positive health signals. Produce remediation matrix with priority ordering (INT-1704, INT-P019)

### P0 (Addendum — Antifragile Infrastructure, per Session 18 INT-1804)
- IMPL-Q-0029 — Agent Auto-Ingest Loop: Build `auto_ingest_loop.sh` — polls agent INBOX0 every 30s, extracts Objective, feeds to CLI pane via tmux, monitors OUTBOX for result, manages DONE/FAILED lifecycle. Solves: agents don't autonomously pick up task files (INT-1804)
- IMPL-Q-0030 — Constellation Health Watchdog: Build `constellation_watchdog.sh` + launchd plist — pings all 4 agent panes every 60s, detects RATE_LIMITED/ERROR/STALE/HEALTHY/IDLE states, writes DYN-CONSTELLATION_HEALTH.md, warns on prolonged failures (INT-1804)
- IMPL-Q-0031 — Open Model Housekeeping Pipeline: Onboard Cline and OpenCode with free-tier open models via OpenRouter for routine tasks: formatting, linting, file moves, state sync, health checks. Reduces proprietary API dependency (INT-1803)
- IMPL-Q-0032 — Token Economics Dispatch Router: Budget-aware task routing that tracks ChatGPT Plus shared consumption (Psyche + Adjudicator), staggers heavy tasks, failovers to Gemini/Kimi/open models when quota is thin (INT-1801, INT-P023)
- IMPL-Q-0033 — Cline CLI Integration: Configure Cline v2.2.2 (`/opt/homebrew/bin/cline`) with OpenRouter API key pointing to best free model (DeepSeek-V3 or Qwen-2.5-72B). Create `~/.cline/` config for headless/non-TUI operation. Verify tmux send-keys dispatch works (unlike Gemini TUI). Add to cockpit as Tier 4 housekeeping agent (INT-1803, INT-C011)
- IMPL-Q-0034 — OpenCode CLI Installation + Integration: Install OpenCode terminal agent, configure with OpenRouter free tier, verify tmux-dispatchable. Add to auto_ingest_loop.sh agent allowlist. Pair with Cline for dual housekeeping capacity (INT-1803, INT-C011)

## 2026-02-16 (Tranche P — Research Pipeline Automation)

*Source: RESEARCH-PIPELINE-AUTOMATION-SPEC.md (780 lines). Full pipeline from capture to NotebookLM to scaffold injection.*

### P0
- IMPL-P-0001 — Build `classify_research.py`: 3-tier auto-classification (author match, keyword match, LLM fallback) for .md files against 14-notebook taxonomy
- IMPL-P-0002 — Build `partition_research.sh`: Create per-notebook staging dirs from classification manifest, copy files
- IMPL-P-0003 — Create `taxonomy.json`: Machine-readable notebook taxonomy with IDs, slugs, keywords, trusted authors, signal patterns
- IMPL-P-0004 — Evaluate NotebookLM Enterprise API access: Determine if Google Workspace qualifies for Pre-GA; evaluate `notebooklm-py` as bridge
- IMPL-P-0005 — Build `upload_to_notebooklm.py`: Create notebooks + upload partitioned .md sources via API (Enterprise or notebooklm-py fallback)

### P1
- IMPL-P-0006 — Configure Hazel rule on MBA: Watch ~/Desktop/research/ for new .md files, trigger classify_research.py
- IMPL-P-0007 — Build `/generate_notebook_questions` skill: 5-15 questions per notebook using taxonomy + Rosetta + Intention Compass
- IMPL-P-0008 — Build `research_threshold.sh` + launchd plist: Daily alert when unprocessed count > 20 or days since processing > 7
- IMPL-P-0009 — Build `archive_research.sh`: Move processed files to 04-SOURCES/research/batch-YYYY-MM-DD/, update manifest, commit
- IMPL-P-0010 — Build NotebookLM tracking ledger: JSON mapping notebook IDs to NotebookLM names, source counts, seeding status
- IMPL-P-0011 — Build `append_to_notebook.py`: Incremental source addition to existing notebooks for new research
- IMPL-P-0012 — Build `/extract_insights` skill: Semi-automated extraction from NotebookLM responses with criteria checklist

### P2
- IMPL-P-0013 — Build `inject_insight.py`: Automated routing of tagged insights to target artifacts (Compass, Backlog, Rosetta, Sigma)
- IMPL-P-0014 — End-to-end pipeline orchestrator: `make research-pipeline` (classify → partition → upload → question → extract → inject → archive)
- IMPL-P-0015 — Claude 200K context as NotebookLM supplement for programmatic queries
- IMPL-P-0016 — Cross-notebook resonance detector: Identify thematic connections across 14 notebooks, generate meta-synthesis questions
- IMPL-P-0017 — Notebook lifecycle policy: Split at 50-source limit, merge low-activity, archive stale
- IMPL-P-0018 — Research velocity dashboard: Save rate, classification distribution, notebook saturation, processing lag

### P3
- IMPL-P-0019 — Autonomous research agent: OpenClaw monitors X for articles matching Sovereign Curation Profile, auto-saves
- IMPL-P-0020 — Continuous notebook refresh: Periodic re-querying as Syncrescendence priorities evolve
- IMPL-P-0021 — NotebookLM-to-Obsidian bridge: Export synthesis outputs as wikilinked markdown

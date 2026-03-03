# INTENTION ARCHAEOLOGY COMPASS
## Oracle Pedigree Extraction Instrument
**Last Updated**: 2026-02-09
**Oracle Lineage**: 0 → 15+
**Status**: Rolling snapshot
**Authority**: Oracle 13+ / Commander

---

## PURPOSE

The Intention Archaeology Compass is a unified instrument that extracts, categorizes, and tracks Sovereign intentions across Oracle sessions. It serves as both:
- **Cache**: Quick reference for active intentions
- **Rolling Snapshot**: Historical record of intention evolution

From Oracle 12 (Sovereign's words):
> "The intention archaeology compass should be unified. All intentions are compounding vectors that are interdependent... In essence, it's a cache, but it's also a rolling snapshot."

---

## SCHEMA

Each intention entry contains:

```yaml
- id: INT-XXXX
  oracle: [origin Oracle number]
  timestamp: [ISO datetime or Oracle reference]
  category: [urgent|sprint|backlog|pattern|capture]
  priority: [P0|P1|P2|P3]
  status: [active|resolved|superseded|deferred]
  text: "[Sovereign's actual words]"
  interpretation: "[Oracle's understanding]"
  blocked_by: [null|dependency]
  integrated_into: [null|CANON/task/decision]
  notes: "[additional context]"
```

### Category Definitions

| Category | Description | Action Horizon |
|----------|-------------|----------------|
| **urgent** | Address NOW | Same session |
| **sprint** | Integrate at checkpoint | Current Oracle |
| **backlog** | Future work | Future Oracles |
| **pattern** | Meta-observations | Ongoing |
| **capture** | Undifferentiated inbox | Pending triage |

---

## ACTIVE INTENTIONS

### URGENT (Address NOW)

| ID | Oracle | Text | Status | Notes |
|----|--------|------|--------|-------|
| INT-1201 | 12 | "accounts become self-sustaining by month end" | failed | Jan 31 deadline missed. Reset target pending sovereign input. |
| INT-1202 | 12 | "capitalize on these heavy machinery to construct as much of Syncrescendence" | active | Maximum velocity during capability window |
| INT-1209 | 12 | "Temporal intelligence refresh pipeline" | active | Automation candidate for model/platform features that expire; cadenced update system for ARCH- archived research |
| INT-1612 | 16 | "Begin ALL automations" | active | Master plan: activate Hazel, launchd, Make/Zapier, webhook bridges, n8n, cron. The machine is built — RUN IT. P0. |

### SPRINT (Current Cycle)

| ID | Oracle | Text | Status | Integrated Into |
|----|--------|------|--------|-----------------|
| INT-1203 | 12 | "design/architect for 3 Claude + 1 Gemini + 1 ChatGPT paid" | active | [[CANON-25200-CONSTELLATION_ARCH-lattice]] |
| INT-1204 | 12 | "update [[CANON-25100-CONTEXT_TRANS-lattice]] with Oracle Pedigree section" | resolved | [[CANON-25100-CONTEXT_TRANS-lattice]] v2.1.0 |
| INT-1205 | 12 | "intention archaeology compass should be unified" | resolved | This document |
| INT-1206 | 11 | "Complete Efficacy, Mastery, Transcendence IIC configs" | active | PROJ-002 |
| INT-1101 | 11 | "Multi-CLI integration validation" | resolved | DIRECTIVE-042B |
| INT-1210 | 12 | "Canonize Model Manual/Prompting conceptual space" | resolved | DIRECTIVE-044B audit: 10 CANON files + translate.xml provide sufficient coverage |
| INT-1211 | 12 | "Canonize Platform Features/Ecosystem Leverage" | resolved | DIRECTIVE-044B audit: 77 CANON files provide excellent coverage |
| INT-1212 | 12 | "Canonize Model Qualities/Capabilities/Benchmarks" | resolved | DIRECTIVE-044B audit: 73 CANON files with correct temporal/evergreen split |
| INT-1213 | 12 | "Blitzkrieg model specification protocol" | resolved | CLAUDE.md v2.1.0 + coordination.yaml v2.1.0 per DIRECTIVE-044B |

### SESSION 15+ (2026-02-09): Autonomy Expansion + Narrative DNA

| ID | Oracle | Text | Status | Integrated Into |
|----|--------|------|--------|-----------------|
| INT-1501 | 15 | "Maximize Claude Code autonomy, close that final 30%" | active | SOVEREIGN-012, SYN-34 |
| INT-1502 | 15 | "Inscribe narrative DNA — StarCraft/Dune/Halo/anime as design vocabulary" | resolved | memory/narrative-dna.md |
| INT-1503 | 15 | "Close 30% gap to fiduciary level — Commander must self-improve, embrace or die" | active | SOVEREIGN-TRAJECTORY.md §7 |
| INT-1504 | 15 | "Cascade deployment from Mac mini HQ to MBA field ops" | active | DEPLOYMENT-PLAYBOOK.md Cascade Differential |
| INT-1505 | 15 | "Deep syncretization of sci-fi/gaming/literature narratives" | active | TASK-NARRATIVE-EXEGESIS.md (Cartographer) |
| INT-1506 | 15 | "We are a Neo-organization — individual + AI constellation as institutional equivalent" | active | SOVEREIGN-012 §3 |
| INT-1507 | 15 | "Appropriate martial, legal, financial, political, scientific terminology" | resolved | REF-ROSETTA_STONE.md v2.3.0 (32 new terms) |
| INT-1508 | 15 | "Track Yegge Gas Town + Anthropic Hivemind — validate architecture against his patterns" | resolved | memory/narrative-dna.md, SOVEREIGN-012 §2 |
| INT-1509 | 15 | "launchd over cron — cron killed by power management on laptops" | resolved | DEC-SOV-006, 3 new plists deployed |

### SESSION 16 (2026-02-09): Sovereign Expansion Directive

| ID | Oracle | Text | Status | Integrated Into |
|----|--------|------|--------|-----------------|
| INT-1601 | 16 | "Syncrescript synchronized to corpus, adopt Rails sensibilities" | active | SYN-37 |
| INT-1602 | 16 | "IIC ingestion pipeline on Google ecosystem + feedcraft sources" | active | SYN-49 |
| INT-1603 | 16 | "JIT-software — HighCommand as variable tmux dashboard, Mac mini stable/dashboard, MBA kinetic cockpit" | active | SYN-40 |
| INT-1604 | 16 | "Web app memory architecture audit + Project custom instructions + RAG strategy" | active | SYN-38 |
| INT-1605 | 16 | "NotebookLM research architecture + operational thesis" | active | SYN-39 |
| INT-1606 | 16 | "Discord + Slack — give OpenClaw all tools to self-service" | active | SYN-50 |
| INT-1607 | 16 | "Setapp app audit — clone to terminal-first, reconceptualize interaction dynamic, evaluate Hammerspoon" | active | SYN-47 |
| INT-1608 | 16 | "Extract Apple Notes — ingest/digest/excrete" | active | SYN-46 |
| INT-1609 | 16 | "YouTube Watch Later + X favorites — meta-digests via OpenClaw" | active | SYN-46 |
| INT-1610 | 16 | "Terminal cascade sync — AI CLI tools across iTerm/Ghostty continuum, synchronized between machines" | active | SYN-43 |
| INT-1611 | 16 | "Mac mini + MacBook Air handbooks once settled" | active | SYN-44 |
| INT-1613 | 16 | "Cockpit border white instead of blue" | active | SYN-42 |
| INT-1617 | 16 | "Add Marvel/ComicbookUniverses/Star Wars/Star Trek/Accelerando to narrative imaginal layers" | active | SYN-41, narrative-dna.md |

### SESSION 17 (2026-02-16): Research Corpus Intelligence Extraction

*Source: 267-file research corpus analysis (59 articles deep-read, 4 parallel agents). Insights extracted from RESEARCH-INSIGHTS-VERY-HIGH-SIGNAL.md and RESEARCH-INSIGHTS-HIGH-SIGNAL.md.*

| ID | Oracle | Text | Status | Integrated Into |
|----|--------|------|--------|-----------------|
| INT-1701 | 17 | "Progressive Disclosure is the correct context loading pattern — 4-layer graduated system for vault traversal" | active | RESEARCH-INSIGHTS-VERY-HIGH-SIGNAL.md §1.1 |
| INT-1702 | 17 | "Judgment Engineering as Service — exocortex encodes accumulated judgment that agents execute against" | active | → IMPL-Q-0005 (Three-Layer Memory); RESEARCH-INSIGHTS-VERY-HIGH-SIGNAL.md §3.1 |
| INT-1703 | 17 | "Attention as the Post-Labor Currency — cognitive sovereignty becomes a governance question" | active | → CONVERGENCE-INTENT-TAXONOMY.md domain 7; strategic framing, no direct IMPL (academic); RESEARCH-INSIGHTS-VERY-HIGH-SIGNAL.md §3.5 |
| INT-1704 | 17 | "Anti-Tool-Shaped-Object Discipline — institutionalize 'what is the number before making it go up?'" | active | → IMPL-Q-0027 (Anti-Tool-Shaped-Object Gate), IMPL-Q-0028 (Tool-Shaped System Audit); RESEARCH-INSIGHTS-VERY-HIGH-SIGNAL.md §3.6 |
| INT-1705 | 17 | "Instruction → Skill → Hook maturity ladder — new patterns start as instructions, graduate to hooks" | active | RESEARCH-INSIGHTS-VERY-HIGH-SIGNAL.md §Cross-Cutting #3 |
| INT-1706 | 17 | "Data Layer Sovereignty — ontology, convergence taxonomy, Rosetta Stone ARE proprietary data assets" | active | → REF-ROSETTA_STONE.md v2.7.0 + ontology.db (1484 rows); RESEARCH-INSIGHTS-VERY-HIGH-SIGNAL.md §INT-004 |
| INT-1707 | 17 | "Three-Layer Memory Architecture — Knowledge Graph + Daily Notes + Tacit Knowledge (consensus converging)" | active | RESEARCH-INSIGHTS-VERY-HIGH-SIGNAL.md §2.1 |
| INT-1708 | 17 | "Research → NotebookLM pipeline automation — classify, partition, upload, question, extract, inject" | active | → IMPL-P-0001 through IMPL-P-0014 (full pipeline); MVP: P-0003→P-0001→P-0002→P-0004→P-0005→P-0007→P-0012→P-0013→P-0009; RESEARCH-PIPELINE-AUTOMATION-SPEC.md |
| INT-1709 | 17 | "Security is existential — 200+ exposed instances, supply chain attacks via skill marketplaces" | active | RESEARCH-INSIGHTS-HIGH-SIGNAL.md §18 |
| INT-1710 | 17 | "The Constellation pattern is validated — independent practitioners converged on our exact architecture" | active | → IMPL-Q-0021 (Personality File Alignment Audit); RESEARCH-INSIGHTS-HIGH-SIGNAL.md §Theme 1 |
| INT-1711 | 17 | "Agent Vault = Human-Agent Shared Knowledge Graph — Obsidian vault IS the agent's memory" | active | → IMPL-Q-0005 (Three-Layer Memory) + IMPL-Q-0007 (Vault Index Pattern); RESEARCH-INSIGHTS-VERY-HIGH-SIGNAL.md §INT-007 |
| INT-1712 | 17 | "The perimeter is capability, not network — redefine security around what agents CAN DO" | active | RESEARCH-INSIGHTS-HIGH-SIGNAL.md §17 |

### BACKLOG (Future Work)

| ID | Oracle | Text | Status | Priority | Notes |
|----|--------|------|--------|----------|-------|
| INT-1207 | 12 | "Manus before Perplexity" | deferred | P3 | Platform prioritization |
| INT-1208 | 12 | "promos for Perplexity and additional Gemini account" | deferred | P3 | Cost optimization future |
| INT-0801 | 8+ | "Tech Lunar 306K specs to CANON-30xxx" | deferred | P2 | PROJ-008 |
| INT-0802 | 8+ | "Modal 2 visual capabilities" | deferred | P3 | PROJ-009 |
| INT-1102 | 11 | "Skills conversion for top 5 functions" | deferred | P3 | PROJ-016 |
| INT-0701 | 7 | "Browser automation for account cloning" | deferred | P3 | PROJ-015 |
| INT-1214 | 12 | "Deep Research: Claude Code + Anthropic Ecosystem" | deferred | P2 | Prompt prepared |
| INT-1215 | 12 | "Deep Research: OpenAI Codex + ecosystem" | deferred | P3 | Requires community sampling |
| INT-1216 | 12 | "Deep Research: Google Jules + Gemini CLI" | deferred | P3 | Requires community sampling |
| INT-1217 | 12 | "Plan Mode as Oracle replacement" | deferred | P3 | Evaluate CLI Plan vs web app strategic synthesis |
| INT-1218 | 12 | "Permission fatigue mitigation" | deferred | P3 | --dangerously-skip-permissions vs allowlisting |
| INT-1614 | 16 | "Student (Chaffey college) + apprentice (IEETC) — FDE modules into Syncrescendence" | active | P1 | Education/professional integration; health+fitness, homeowner property mgmt |
| INT-1615 | 16 | "Health+fitness and homeowner property management modules" | active | P2 | Personal domain integration into Syncrescendence |
| INT-1616 | 16 | "LifeOS/Zettelkasten/PKM/PARA/GTD architectural convergence" | active | P1 | Serious discussion needed: note-taking, linking your thinking, personal context lakehouse, pillars, pipelines, vaults |
| INT-1618 | 16 | "Celestial alignment synchronization — cosmic coherence" | deferred | P3 | Poetic, cathartic moment for the Syncrescendence metaphor. When capacity allows. |

### PATTERNS (Meta-Observations)

| ID | Oracle | Pattern | Status | Notes |
|----|--------|---------|--------|-------|
| INT-P001 | 3 | "Orchestration is OPERATIONAL, not CANON" | resolved | Constitutional rule |
| INT-P002 | 4 | "Metabolism applies to CONTENT, not infrastructure" | resolved | Constitutional rule |
| INT-P003 | 6 | "Verify before declare" | resolved | Constitutional rule |
| INT-P004 | 7 | "Globe before trees" | active | Holistic framing first |
| INT-P005 | 10 | "automation infrastructure must precede content work" | resolved | PROJ-011 complete |
| INT-P006 | 12 | "Multi-agent 90.2% outperforms single-agent" | active | Constellation justification |
| INT-P007 | 12 | "Pedigree supersedes handoff for repository-centric work" | active | New paradigm |
| INT-P008 | 12 | "Temporal vs evergreen distinction" | resolved | Archive temporal intelligence with expiration warning; CANON = evergreen only |
| INT-P014 | 16 | "Tokens are the new minerals and vespene gas" | active | Token economics as strategic resource management. StarCraft resource model applied to API credits, context windows, compute. |
| INT-P015 | 16 | "Mac mini = stable dashboard (macro), MBA = kinetic cockpit (micro)" | active | Dual-machine interaction paradigm. Mac mini: always-on, terminal-based, less frequent interaction, StarCraft macro. MBA: synaptic, kinetic, consistent but audible-ready. |
| INT-P016 | 16 | "Web app system prompts general, leverage platform strengths — confirmed superior" | active | Thesis validated: general prompts + platform-native strengths beats over-specialization. Memory architecture needs audit post-pivot. |
| INT-P017 | 17 | "File-First, Always — plain markdown outperforms specialized memory infrastructure" | active | ClawVault benchmark: markdown+grep 74.0% vs specialized tools 68.5%. LLMs trained on text files. Own data as files. |
| INT-P018 | 17 | "Supersede, Never Delete — all state changes preserve history via supersession chains" | active | Temporal record of knowledge evolution more valuable than current state alone. |
| INT-P019 | 17 | "Security as Binding Constraint — limiting factor is safety, not capability" | active | 200+ exposed instances, supply chain attacks, prompt injection. Defense-in-depth is not optional. |
| INT-P020 | 17 | "The Verbatim Trap Test — every synthesis must produce what the source didn't contain" | active | Connections, tensions, implications, questions. If not, reject and redo. Anti-pattern for all Constellation work. |
| INT-P021 | 17 | "Knowledge-Code Isomorphism — knowledge bases and codebases share identical structure" | active | Same tools (git, grep, hooks, CI/CD) manage both. Vault index = skill discovery. Notes = skills. |
| INT-P022 | 17 | "The Constellation pattern is emergent consensus — independent practitioners converged on our architecture" | active | Differentiation from quality of personality files, memory curation, coordination patterns, security hardening. |

### SESSION 18 (2026-02-16): Token Economics + Antifragile Constellation

**Sovereign Directive**: "Opus 4.6 is second-to-none in interpretability. 5.3-Codex is very meticulous but sub-optimal in rapport. Gemini CLI has large token limits but worst at tool use. Kimi K2.5 has generous but fickle limits. Most intelligent models strategize and plan. Open models conduct housekeeping. Onboard Cline and OpenCode."

| ID | Oracle | Intention Text | Status | Notes |
|----|--------|---------------|--------|-------|
| INT-1801 | 18 | "Token Economics Dispatch — budget-aware routing across shared API plans" | active | ChatGPT Plus fuels BOTH Psyche (5.3-codex) AND Adjudicator (5.2-codex). Shared rate limit pool. Dispatch must account for cumulative consumption. |
| INT-1802 | 18 | "Model Role Specialization — assign by cognitive strength, not availability" | active | Opus 4.6 = interpreter/orchestrator (rapport, interpretability). GPT-5.3-codex = meticulous executor (systematic, thorough). Gemini 2.5 Pro = capacity/fidelity passes (1M context, multi-pass). Kimi K2.5 = strategic auxiliary (generous limits, philosophical depth). |
| INT-1803 | 18 | "Open Model Onboarding — Cline + OpenCode for housekeeping at scale" | active | **Ground truth (2026-02-16)**: Cline v2.2.2 installed (`/opt/homebrew/bin/cline`), TUI-based, supports OpenRouter (free tier = DeepSeek, Qwen, Llama). Needs auth setup via "Use your own API key" → OpenRouter. OpenCode not yet installed (empty `~/.config/opencode/`, no binary in PATH). Both need tmux-dispatchable configuration for Commander orchestration. → IMPL-Q-0031, IMPL-Q-0033, IMPL-Q-0034 |
| INT-1804 | 18 | "Antifragile Agent Infrastructure — self-healing constellation" | active | Five capabilities: (1) auto-ingest loop polls INBOX0, (2) health watchdog monitors panes every 60s, (3) rate limit circuit breaker with failover dispatch, (4) worktree isolation via git worktree or read-only mode, (5) local-first sync via SCP when git push blocked. |

| INT-P023 | 18 | "Shared Rate Limit Awareness — competing agents on same API plan must be dispatch-coordinated" | active | Never dispatch simultaneous heavy tasks to Psyche + Adjudicator. Stagger or route overflow to Gemini/Kimi/open models. |
| INT-P024 | 18 | "Intelligence Tiering — most capable models strategize, open models execute housekeeping" | active | Tier 1 (strategy/planning): Opus 4.6, Kimi K2.5. Tier 2 (meticulous execution): GPT-5.3-codex. Tier 3 (capacity passes): Gemini 2.5 Pro. Tier 4 (housekeeping): open models via Cline/OpenCode. |
| INT-P025 | 18 | "Agent Auto-Recovery — agents must self-heal without Commander intervention" | active | Rate limits → exponential backoff + task queue. Dirty worktree → read-only analytical mode. Stale state → git pull + verify. Dead agent → watchdog restart. |

### CAPTURE (Pending Triage)

| ID | Oracle | Raw Capture | Status |
|----|--------|-------------|--------|
| INT-C001 | 12 | "audit and anneal the corpus again for alignment/congruence" | resolved |
| INT-C002 | 12 | "attached reports ought to be canonized" | pending |
| INT-C003 | 13 | "Revenue target reset — new deadline TBD by Sovereign" | pending |
| INT-C004 | 13 | "Corpus hygiene sprint: triage -INBOX, refresh stale state, compress" | resolved |
| INT-C005 | 14 | "Learn tmux for multi-session terminal management — maximum parallel efficacy" | pending |
| INT-C006 | 14 | "HighCommand (Agendizer) = GUI substrate for INT-MI19 Ontology — document the connection, track as PROJ dependency" | pending |
| INT-C007 | 14 | "Session discipline: chunk work into parallel sessions, stop sequential single-terminal habits" | pending |
| INT-C008 | 16 | "Whatever we were trying to do with Notion/Airtable — serious LifeOS/PKM/ontology discussion needed" | pending |
| INT-C009 | 16 | "Celestial alignment synchronization — poetic, cathartic cosmic coherence moment for the Syncrescendence" | pending |
| INT-C010 | 16 | "Notion/Airtable/LifeOS/Zettelkasten — note-taking, PKMs, linking your thinking, PARA, BASE, GTD, productivity, personal context lakehouse" | pending |
| INT-C011 | 18 | "Cline + OpenCode installed — integrate for Commander manipulation via tmux, use most intelligent free models (OpenRouter free tier). Backlog now, operationalize as constellation stabilizes." | pending |

### PRE-ORACLE INTENTIONS (Extracted from `my inputs.md`, 2026-02-01)

*Source: Sovereign raw inputs to ChatGPT Vizier sessions, pre-dating formal Oracle numbering. 50 entries compressed into 20 intention vectors.*

**Resolved by Restructuring (Oracle 13 work):**

| ID | Text (compressed) | Status | Resolved By |
|----|-------------------|--------|-------------|
| INT-MI01 | "Don't nerf ChatGPT/Grok/Gemini—general intelligence has value beyond narrow roles" | resolved | Avatar Pantheon v3 (COCKPIT.md) — roles expanded, not lobotomized |
| INT-MI02 | "Capitalize on ALL memory features across ALL platforms" | resolved | CANON-25000 (Memory Architecture + Teleology) — comprehensive coverage |
| INT-MI03 | "Algebraize/symbolize the corpus—reduce tokens, maximize semantics" | resolved | PROJ-SN-VARS — SN system (79% compression) + DEF variables |
| INT-MI04 | "Code-ify the corpus so things update everywhere—variables, not literals" | resolved | sn_expand.py + 9 DEF blocks in DEF-CONSTELLATION_VARIABLES.md |
| INT-MI05 | "Obsidian-friendly wikilinks and graph backlinks" | resolved | Cross-references maintained throughout restructuring ([[CANON-XXXXX]] format) |
| INT-MI06 | "Rename directories—developer happiness, not legacy numbering" | resolved | PROJ-RESTRUCTURE — 00/01/02/04/05 + -INBOX/-OUTGOING/-SOVEREIGN |
| INT-MI07 | "GEMINI.MD and AGENTS.MD in root for CLI agents" | resolved | AGENTS.md created, gemini-settings.json in 02-ENGINE |
| INT-MI08 | "02-OPERATIONAL is a shitshow—why does it look like that?" | resolved | PROJ-RESTRUCTURE — 00-ORCHESTRATION/state/scripts/archive/ |
| INT-MI09 | "Consolidate directives and execution logs holistically" | resolved | archive/ with compendiums, compact_wisdom.sh automation |
| INT-MI10 | "Forensic audit of Canon—conceptual coherence, not metadata" | resolved | CANON lean-out (82→79), cross-reference sweep, CANON-00007+00008 merge |
| INT-MI11 | "Live capability and features matrix—not ossified in stone" | resolved | MODEL-INDEX.md + ARCH-LIVE_CANON_TICKER.md design |
| INT-MI12 | "05 is short-term memory; 06 is cautionary tales/aphorisms" | resolved | 05-SIGMA merger — MEMORY-*, EXEMPLA-*, synthesis/mechanics/practice/ |
| INT-MI13 | "03→06 are interim containers" | resolved | 03 absorbed into 02-ENGINE, 05+06+07 merged into 05-SIGMA |
| INT-MI14 | "Semantic annealment—collapse bloated logs, condense with acumen" | resolved | PROJ-RESTRUCTURE (1267→636 files), compact_wisdom.sh |

**Active (Not Yet Resolved):**

| ID | Text (compressed) | Status | Priority | Blocked By |
|----|-------------------|--------|----------|------------|
| INT-MI15 | "Offload transcripts to Google ecosystem—04-SOURCES externalized into Drive" | active | P2 | Google AI Pro setup (Account 2) |
| INT-MI16 | "Build pipeline in Google ecosystem—Drive sync, Personal Intelligence, Gmail integration" | active | P2 | PROJ-014 (Multi-Account Sync) |
| INT-MI17 | "On-device automation—Hazel, Keyboard Maestro, BTT, AppleScript, Shortcuts" | active | P3 | — |
| INT-MI18 | "Web↔CLI bridge via Hazel + macros—automate between web and CLI" | active | P3 | INT-MI17 |
| INT-MI19 | "Palantir-like ontology—the FINAL BOSS" | active | P1 | PROJ-006, PROJ-003. **UPDATE 2026-02-07**: HighCommand (Agendizer) now implements OntologyClass enum, force-directed graph, convergence detection, echo patterns, bidirectional edges. Reflect primitives (daily notes, backlinks, entity types) are the GUI interaction grammar for this ontology. HighCommand = the native substrate. |
| INT-MI20 | "Category/type theory applied to corpus taxonomization down to token level" | active | P2 | SN system provides foundation; deeper application pending |

**Patterns (Meta-Observations from `my inputs.md`):**

| ID | Pattern | Status | Notes |
|----|---------|--------|-------|
| INT-P009 | "ChatGPT proposes creative postulations Claude wouldn't—bounded windows of superior intelligence" | active | Platform-specific cognitive strengths; don't homogenize |
| INT-P010 | "Claude is so amenable it lacks mind-expansion; ChatGPT has more creative divergence" | active | Informs role specialization—ideation ≠ execution |
| INT-P011 | "Everything is just trade-offs—don't disqualify features for spottiness" | active | Memory reliability is spectrum, not binary |
| INT-P012 | "ChatGPT SD → Codex DD → Claude CD pipeline" (architecture metaphor) | active | Schematic Design → Design Development → Construction Documents |
| INT-P013 | "Chorus/collaboration, not unidirectional compilation—interdisciplinary synergy" | active | Multi-agent should be dialogic, not just dispatch |

---

## HISTORICAL EXTRACTIONS

### Oracle 0: Vision

| ID | Text | Status | Outcome |
|----|------|--------|---------|
| INT-0001 | "civilizational sensing infrastructure" | resolved | Core framing established |
| INT-0002 | "skate to where the puck is going" | active | Ongoing design principle |
| INT-0003 | "leverage The Bitter Lesson" | active | Lens 2 institutionalized |

### Oracle 1: Research

| ID | Text | Status | Outcome |
|----|------|--------|---------|
| INT-0101 | "consumer/prosumer focus" | resolved | Ecosystem cartography scope |
| INT-0102 | "multi-platform strategy" | active | 5-platform constellation |

### Oracle 2: Infrastructure

| ID | Text | Status | Outcome |
|----|------|--------|---------|
| INT-0201 | "flat + symlink architecture" | resolved | Decision 2.1 |
| INT-0202 | "designing the librarian, not compressing the library" | active | Context engineering thesis |
| INT-0203 | "human navigation: comprehensible in 5 minutes" | active | Design constraint |

### Oracle 3: Orchestration Peak

| ID | Text | Status | Outcome |
|----|------|--------|---------|
| INT-0301 | "orchestration infrastructure pattern" | resolved | THE MODEL established |
| INT-0302 | "Reception Calibration vs Archetype Engineering" | resolved | Three-layer architecture |
| INT-0303 | "visibility bridge via execution logs" | active | Visibility flow |

### Oracle 4: Metabolic Defrag

| ID | Text | Status | Outcome |
|----|------|--------|---------|
| INT-0401 | "canonize or delete, no middle ground" | superseded | Too aggressive |
| INT-0402 | "79% file reduction" | resolved | Defrag completed |
| INT-0403 | "nine evaluative lenses" | resolved | Extended to 18 in Oracle 6 |

### Oracle 5: Recovery + Genesis

| ID | Text | Status | Outcome |
|----|------|--------|---------|
| INT-0501 | "orchestration is protected infrastructure" | resolved | Constitutional rule |
| INT-0502 | "Genesis layer creation" | resolved | CANON-0000x series |
| INT-0503 | "most extreme dynamic progressive route" | active | Decision principle |

### Oracle 6: Semantic Annealment

| ID | Text | Status | Outcome |
|----|------|--------|---------|
| INT-0601 | "extended nine lenses to 18" | resolved | STANDARDS.md |
| INT-0602 | "bifurcation: filesystem vs Obsidian" | resolved | Decision 6.2 |
| INT-0603 | "aliases for Finder, not Obsidian" | active | Design principle |

### Oracle 7: Ground Truth

| ID | Text | Status | Outcome |
|----|------|--------|---------|
| INT-0701 | "REVIEW EVERY CONVERSATION" | resolved | Forensic audit completed |
| INT-0702 | "maximum resolution documentation" | active | ORACLE_DECISIONS.md created |
| INT-0703 | "repository is Foyer" | active | All context accessible |

### Oracle 8-9: [Recovery Phase]

| ID | Text | Status | Outcome |
|----|------|--------|---------|
| INT-0801 | "complete PROJ-001 transcript ingestion" | resolved | 43 sources processed |
| INT-0901 | "directory restructuring to 00-06" | resolved | Numbered scheme deployed |

### Oracle 10: Infrastructure Completion

| ID | Text | Status | Outcome |
|----|------|--------|---------|
| INT-1001 | "PROJ-011 automation infrastructure" | resolved | CLAUDE.md + Makefile + commands |
| INT-1002 | "multi-Claude coordination" | resolved | coordination.yaml |
| INT-1003 | "worktree-based isolation" | active | Zone ownership pattern |

### Oracle 11: Blitzkrieg

| ID | Text | Status | Outcome |
|----|------|--------|---------|
| INT-1101 | "parallel stream execution" | resolved | 4 streams completed |
| INT-1102 | "IIC configuration reconnaissance" | resolved | 14500+ lines reviewed |
| INT-1103 | "Gemini CLI validation" | resolved | APPROVED |

### Oracle 12: Constellation Architecture

| ID | Text | Status | Outcome |
|----|------|--------|---------|
| INT-1201 | "self-sustaining by month end" | active | Revenue target |
| INT-1202 | "5-platform constellation" | active | [[CANON-25200-CONSTELLATION_ARCH-lattice]] |
| INT-1203 | "ChatGPT Plus integration" | active | coordination.yaml update |
| INT-1204 | "Oracle Pedigree protocol" | resolved | [[CANON-25100-CONTEXT_TRANS-lattice]] update |
| INT-1205 | "unified intention compass" | resolved | This document |

---

## INTEGRATION PROTOCOL

### 1. Extraction (During Oracle Session)

When Sovereign speaks:
1. Capture exact words in quotes
2. Assign temporary INT-XXXX ID
3. Note Oracle number
4. Add to CAPTURE category if unclear

### 2. Categorization (Session Checkpoint)

Move from CAPTURE to appropriate category:
- **urgent**: Requires immediate action
- **sprint**: Part of current cycle
- **backlog**: Future work
- **pattern**: Meta-observation

### 3. Resolution Tracking

When intention is addressed:
1. Update status to `resolved`
2. Add `integrated_into` reference
3. Document outcome

### 4. Supersession

When intention is replaced:
1. Update status to `superseded`
2. Reference replacing intention
3. Document rationale

---

## DEPENDENCY MAP

```
INT-1201 (sustainability) ──────────────────► Revenue generation
     │
     ├── INT-1202 (heavy machinery) ──────► Maximum velocity
     │        │
     │        └── INT-1203 (5 platforms) ─► [[CANON-25200-CONSTELLATION_ARCH-lattice]]
     │
     └── INT-1206 (IIC configs) ──────────► PROJ-002 completion
              │
              └── INT-1101 (multi-CLI) ───► Gemini validated

INT-P006 (multi-agent 90.2%) ─────────────► Constellation justification
     │
     └── INT-P007 (pedigree) ─────────────► New paradigm

INT-1612 (begin automations) ────────────► Everything below
     │
     ├── INT-1603 (JIT HighCommand) ─────► Mac mini dashboard + MBA cockpit
     │        │
     │        └── INT-1610 (terminal sync) ► Machine synchronization
     │                 │
     │                 └── INT-1611 (handbooks) ► Documentation
     │
     ├── INT-1608 (Apple Notes) ──────────► Information extraction
     │        └── INT-1609 (YouTube/X) ───► Meta-digest pipeline
     │
     ├── INT-1602 (IIC Google) ───────────► Ingestion pipeline
     │        └── INT-1605 (NotebookLM) ──► Research architecture
     │
     └── INT-1604 (web app memory) ───────► Platform leverage audit

INT-P014 (tokens = minerals) ────────────► Resource economics lens
INT-P015 (dual-machine paradigm) ─────────► INT-1603, INT-1611
```

---

## PATTERN ANALYSIS

### Recurring Themes

1. **Velocity**: "capitalize", "heavy machinery", "accelerating pace", "begin all automations"
2. **Architecture**: "constellation", "5-platform", "specialization", "JIT-software"
3. **Sustainability**: "self-sustaining", "month end"
4. **Holism**: "unified", "integrated", "globe before trees", "LifeOS convergence"
5. **Trade-off Pragmatism**: "everything is trade-offs", "don't disqualify for spottiness"
6. **Compression**: "algebraize", "symbolize", "reduce tokens maximize semantics", "Rails conventions"
7. **Automation**: "Hazel", "macros", "bridge web and CLI", "sensing", "begin ALL automations"
8. **Resource Economics**: "tokens are the new minerals and vespene gas", API credits as strategic resource
9. **Dual-Machine Paradigm**: Mac mini = stable dashboard (macro), MBA = kinetic cockpit (micro)
10. **Information Stream Extraction**: Apple Notes, YouTube, X favorites — ingest/digest/excrete cycle
11. **Narrative Depth**: Marvel, Star Wars, Star Trek, Accelerando join StarCraft/Dune/Halo/anime/gaming

### Anti-Patterns Identified

1. **Oracle 4 Category Error**: Applied metabolism to infrastructure
2. **Oracle 6 Verification Failure**: Evaluated reports, not reality
3. **Fragmented Intention Tracking**: Pre-compass scattered approach

### Success Patterns

1. **Oracle 3 Model**: Orchestration infrastructure pattern
2. **Oracle 10-11 Blitzkrieg**: Parallel stream execution
3. **Oracle 12 Constellation**: Purpose-specialized platforms

---

## MAINTENANCE SCHEDULE

| Action | Frequency | Responsible |
|--------|-----------|-------------|
| Extract intentions | Every Oracle session | Active Oracle |
| Categorize captures | Session checkpoint | Active Oracle |
| Resolve completed | Immediately on completion | Executing instance |
| Pattern analysis | Monthly | Any Oracle |
| Archive old resolved | Quarterly | Any Oracle |

---

## VERSION HISTORY

**v3.0.0** (2026-02-09): Sovereign Expansion Directive (Session 16)
- 18 new intentions (INT-1601 through INT-1618) from massive Sovereign brain dump
- 3 new patterns (INT-P014 through INT-P016): token economics, dual-machine paradigm, web app thesis confirmation
- 3 new captures (INT-C008 through INT-C010): Notion/Airtable/LifeOS discussion, celestial alignment
- 14 Linear issues created (SYN-37 through SYN-50)
- 8 ClickUp tasks created across Professional/Personal/Financial spaces
- Narrative DNA expanded: Marvel, Star Wars, Star Trek, Accelerando
- Dependency map expanded with new intention chains
- Authority: Commander / Sovereign Session 16

**v2.0.0** (2026-02-01): Pre-Oracle Extraction + Resolution Sweep
- Metabolized `my inputs.md` (16K, 50 entries) → 20 INT-MI entries
- 14 resolved (by PROJ-RESTRUCTURE, PROJ-SN-VARS, PROJ-CANON-LEAN, PROJ-AVATARS)
- 6 active (Google pipeline, on-device automation, Palantir ontology)
- 5 new patterns (P009-P013: platform cognitive strengths, trade-off philosophy)
- Resolved INT-C001 (corpus audit) and INT-C004 (corpus hygiene sprint)
- Authority: Oracle 13+ / Commander session

**v1.0.0** (2026-01-11): Genesis establishment
- Complete extraction from Oracle 0-12
- Schema defined with 5 categories
- Integration protocol documented
- Pattern analysis included
- Authority: Oracle 12 / DIRECTIVE-043A

---

**END ARCH-INTENTION_COMPASS.md**

# UPDATE AGENT MEMORY SKILL
## Agent Memory Architecture Update — Per-Agent Context Persistence

**Version**: 1.0.0
**Last Updated**: 2026-02-08
**Authority**: Oracle 13

---

## PURPOSE

Update per-agent memory files with session insights, decision patterns, and calibration adjustments. Each constellation agent has its own memory architecture suited to its CLI tool. This skill ensures learned context persists across sessions for every agent.

---

## WHEN TO USE

Trigger this skill when:
- A session produces insights that should persist (decision patterns, calibration data)
- Method kaizen crystallizes a pattern affecting agent behavior
- Agent configuration changes (new tools, new access, new workflows)
- Session end — capture session-specific learnings
- Sovereign issues calibration adjustments for specific agents
- Cross-agent coordination reveals communication patterns to encode

---

## AGENT MEMORY ARCHITECTURES

### Commander (Claude Code Opus)

**Memory location**: `~/.claude/projects/*/memory/` files

**Files to update**:
- `MEMORY.md` — Strategic context, project states, dependency chains, anti-patterns
- `syncrescendence-paths.md` — Key file path reference (if paths change)

**Update procedure**:
1. Read current `MEMORY.md`
2. Identify sections needing update (project states, current intentions, etc.)
3. Apply changes preserving existing structure
4. Verify no sensitive data (API keys already present are fine; do not add new ones outside the established pattern)

**What to capture**:
- Updated project completion percentages
- New dependency chain information
- Resolved or new active intentions
- Changed anti-patterns based on kaizen
- Session protocol refinements

### Ajna (OpenClaw Opus 4.5, Mac Mini)

**Memory location**: OpenClaw persistent memory via HEARTBEAT.md and context files

**Files to update**:
- `HEARTBEAT.md` — Current operational state, last sync timestamp
- `agents/ajna/inbox/` context files — Standing orders, calibration
- `orchestration/state/DYN-PEDIGREE_LOG.md` — Session lineage (automated via hook)

**Update procedure**:
1. Read current HEARTBEAT.md state
2. Update operational parameters (active tasks, sync state)
3. Write calibration adjustments if behavior needs tuning
4. Verify launchd service is running: `launchctl list | grep openclaw`

**What to capture**:
- Integration patterns that worked/failed
- Sub-agent orchestration insights
- Commit workflow optimizations
- Sync timing calibrations

### Adjudicator (Codex CLI)

**Memory location**: Codex CLI memory files

**Files to update**:
- `agents/adjudicator/INIT.md` — Agent capability definitions, routing rules
- Codex-specific configuration files
- `agents/adjudicator/inbox/` standing orders

**Update procedure**:
1. Read current Codex CLI configuration
2. Update agent definitions if capabilities changed
3. Adjust validation thresholds based on kaizen
4. Update routing rules if agent assignments shifted

**What to capture**:
- Validation patterns (what checks catch real issues)
- False positive patterns (what checks waste time)
- Test execution optimizations
- Debugging workflow improvements

### Cartographer (Gemini CLI)

**Memory location**: Gemini CLI memory files

**Files to update**:
- `agents/cartographer/INIT.md` — Survey patterns, corpus knowledge, research context
- Gemini-specific configuration
- `agents/cartographer/inbox/` standing orders

**Update procedure**:
1. Read current Gemini CLI configuration
2. Update corpus survey patterns based on recent findings
3. Adjust research scope parameters
4. Record successful query patterns for reuse

**What to capture**:
- Effective survey strategies (what found useful information)
- Corpus coverage gaps identified
- Cross-reference patterns discovered
- Source quality assessments

### Psyche (OpenClaw GPT-5.2, MacBook Air)

**Memory location**: OpenClaw persistent memory

**Files to update**:
- Psyche-specific context files
- `agents/psyche/inbox/` standing orders
- QA pattern files

**Update procedure**:
1. Read current Psyche configuration
2. Update extraction patterns based on recent work
3. Adjust QA thresholds
4. Record specification writing patterns

**What to capture**:
- Extraction techniques that worked
- QA criteria refinements
- Specification templates improvements
- Cross-platform perspective insights

---

## PROCESS

### 1. Identify Update Scope

Determine which agents' memories need updating:

| Trigger | Agents Affected |
|---------|----------------|
| Session end | Current agent only |
| Kaizen crystallization | All agents using the pattern |
| Configuration change | Target agent only |
| Sovereign calibration | Specified agent(s) |
| Cross-agent insight | Both communicating agents |

### 2. Gather Update Content

From the current session, extract:
- **Decisions made**: What was decided and why
- **Patterns observed**: Recurring behaviors or issues
- **Calibrations needed**: Thresholds, timing, scope adjustments
- **New knowledge**: Information not previously in memory

### 3. Apply Updates

For each affected agent:

1. Read the current memory file
2. Identify the correct section for the update
3. Apply the change:
   - For additive information: Append to the relevant section
   - For corrections: Replace the outdated information
   - For new sections: Add following existing formatting conventions
4. Verify the file is well-formed after editing
5. Commit with prefix: `memory: update <agent> memory — <brief description>`

### 4. Cross-Agent Consistency

After updating individual agents, verify:
- No contradictions between agent memories
- Shared knowledge (e.g., project states) is consistent across agents
- Routing rules in Adjudicator's INIT.md match actual agent capabilities

---

## ANTI-PATTERNS

1. **Overwriting without reading**: Always read current memory before updating. Updates are surgical, not wholesale replacements.

2. **Stale memory**: If a project completed 3 sessions ago and memory still says "40% complete," the memory is stale. Update it.

3. **Duplicating repo state**: Memory files should contain agent-specific context, not copies of ledger data. Point to ledgers, do not duplicate them.

4. **Cross-agent memory editing**: Each agent's memory should be updated by that agent or by Commander. Agents should not edit each other's memory files.

5. **Sensitive data in memory**: API keys belong in environment variables or the established MEMORY.md pattern, not scattered across agent memory files.

---

## CROSS-REFERENCES

- `~/.claude/projects/*/memory/MEMORY.md` — Commander memory
- `~/.claude/projects/*/memory/syncrescendence-paths.md` — Path reference
- `agents/*/inbox/` — Per-agent inbox and standing orders
- `orchestration/state/DYN-PEDIGREE_LOG.md` — Ajna session lineage
- `.claude/skills/method_kaizen.md` — Kaizen patterns (upstream trigger)
- `.claude/skills/reviewtrospective.md` — Review insights (upstream data)
- `BRIDGE.md` — Agent/avatar assignments and capabilities

---

*Update Agent Memory Skill v1.0.0 | Syncrescendence*

---
name: blitzkrieg_teams
description: Deploy parallel agent teams for multi-lane execution using Claude Code native teams
---

# /blitzkrieg_teams — Blitzkrieg Agent Teams Skill

You are invoking **Blitzkrieg Teams**: parallel multi-agent dispatch using Claude Code's native team infrastructure (TeamCreate, Task, SendMessage, TaskUpdate, TaskList).

**Version**: 1.0.0
**Last Updated**: 2026-02-09
**Authority**: Oracle 13

---

## When to Use

Trigger this skill when:
- A directive decomposes into **2+ independent workstreams** that can run in parallel
- Research must happen across multiple domains simultaneously (corpus, web, config)
- Implementation spans multiple files/subsystems with no cross-dependencies
- Sovereign requests "blitzkrieg", "parallel", "all hands", or "swarm"
- The Plan skill produced a BLITZKRIEG-mode plan ready for execution

**Do NOT use when**:
- Work is sequential (one step depends on the previous) -- use Execute skill instead
- A single agent can finish the task in under 10 minutes -- overhead not justified
- The task requires heavy git operations across lanes -- merge conflicts will stall you
- Context budget is already above 50% -- spawning agents will compound pressure

---

## Team Composition Patterns

### Scout Team — `blitz-research`
**Purpose**: Parallel information gathering before a decision or implementation.
**Composition**: 2-3 agents, all `Explore` subagent type.
**Use when**: Multiple questions need answers from different sources simultaneously.

| Slot | Subagent Type | Typical Assignment |
|------|---------------|--------------------|
| Scout-1 | Explore | Corpus search (CANON, ENGINE, SIGMA docs) |
| Scout-2 | Explore | Configuration audit (dotfiles, launchd, scripts) |
| Scout-3 | Explore | External research (web, API docs, changelogs) |

**Example**: "Survey the state of all launchd agents, all MCP server configs, and all skill files simultaneously."

### Strike Team — `blitz-implement`
**Purpose**: Parallel implementation across independent file scopes.
**Composition**: 2-4 agents, all `general-purpose` subagent type.
**Use when**: Multiple files/subsystems need changes that do not depend on each other.

| Slot | Subagent Type | Typical Assignment |
|------|---------------|--------------------|
| Strike-1 | general-purpose | Subsystem A implementation |
| Strike-2 | general-purpose | Subsystem B implementation |
| Strike-3 | general-purpose | Subsystem C implementation |
| Strike-4 | general-purpose | Test/validation harness |

**Example**: "Update cockpit.sh pane config, write new launchd plist, and create the dispatch script simultaneously."

### Mixed Team — `blitz-mixed`
**Purpose**: Research phase followed by implementation phase, or research running alongside implementation.
**Composition**: 1-2 `Explore` + 1-2 `general-purpose` agents.
**Use when**: Some lanes need discovery while others can begin immediately.

| Slot | Subagent Type | Typical Assignment |
|------|---------------|--------------------|
| Researcher-1 | Explore | Investigate unknowns, gather requirements |
| Researcher-2 | Explore | Audit current state, find conflicts |
| Implementer-1 | general-purpose | Begin work on known-good lanes |
| Implementer-2 | general-purpose | Pick up implementation after research completes |

**Example**: "Research the Qdrant MCP configuration while simultaneously implementing the Linear MCP setup."

---

## Procedure

### 1. Decompose into Lanes

Before spawning any agents, decompose the work:

1. **List all subtasks** from the directive or plan
2. **Identify dependencies**: Draw the dependency graph (even mentally)
3. **Group into independent lanes**: Each lane must be executable without waiting on another lane's output
4. **Assign file scopes**: Each lane gets an explicit list of files/directories it may modify -- NO OVERLAP
5. **Define success criteria** per lane: What artifact or state change marks the lane as complete?

**Output format** (write this to your working memory before proceeding):
```
BLITZKRIEG DECOMPOSITION
Lane A: <description> | Files: <scope> | Success: <criteria>
Lane B: <description> | Files: <scope> | Success: <criteria>
Lane C: <description> | Files: <scope> | Success: <criteria>
Sync point: <where lanes must converge, if any>
```

### 2. Select Team Pattern

Choose the composition pattern:
- All research? -> Scout Team (`blitz-research`)
- All implementation? -> Strike Team (`blitz-implement`)
- Mix of both? -> Mixed Team (`blitz-mixed`)

### 3. Create Team and Spawn Agents

```
Step 1: Create the team
  TeamCreate with team_name (e.g., "blitz-implement")

Step 2: Create tasks for each lane
  TaskCreate for Lane A with description and success criteria
  TaskCreate for Lane B with description and success criteria
  (repeat for each lane)

Step 3: Spawn teammates
  For each lane, use the Task tool:
    - team_name: the team created in Step 1
    - subagent_type: "Explore" or "general-purpose" per the composition pattern
    - description: the lane's full context including:
      a. What to do (the task)
      b. Which files are in scope (explicit paths)
      c. Which files are OUT of scope (explicit exclusion)
      d. Success criteria
      e. "Report results via SendMessage to team lead when complete"

Step 4: Assign tasks
  TaskUpdate to assign each task to the spawned teammate
```

### 4. Monitor Progress

While teammates execute:

1. **Check TaskList** periodically to see lane status
2. **Watch for SendMessage** from teammates reporting completion or blockers
3. **Respond to questions** -- teammates may need clarification via SendMessage
4. **Do NOT start integration** until all lanes report complete or blocked

If a lane is blocked:
- Assess whether the blocker can be resolved without the lane's output
- If yes, resolve and notify the teammate via SendMessage
- If no, note the partial result and proceed with available lanes

### 5. Collect and Integrate Results

When all lanes complete:

1. **Verify each lane's success criteria** -- read the artifacts, confirm state changes
2. **Integrate outputs** if lanes produce artifacts that must be combined
3. **Run verification**: `git status`, relevant tests, grep checks
4. **Commit the integrated result** with semantic prefix:
   ```
   feat(blitzkrieg): <what was accomplished across lanes>
   ```
5. **All git operations are performed by the team lead only** -- teammates report; lead commits

### 6. Shutdown and Cleanup

After integration:

1. **Send shutdown_request** to each teammate via SendMessage
2. **Log execution** to `DYN-EXECUTION_STAGING.md` (per Execute skill protocol)
3. **Update ledger** via `append_ledger.sh` if the directive warrants it
4. **Report to Sovereign** if this was a dispatched directive

---

## Standard Team Names

| Name | Pattern | Typical Size |
|------|---------|-------------|
| `blitz-research` | Scout Team | 2-3 Explore agents |
| `blitz-implement` | Strike Team | 2-4 code agents |
| `blitz-mixed` | Mixed Team | 1-2 Explore + 1-2 general-purpose |

Use these names consistently. They appear in TaskList output and execution logs.

---

## Safety Rails

### Agent Limits
- **Maximum 4 agents per team**. Context economics: each agent consumes API resources. Diminishing returns above 4.
- **Maximum 1 team active at a time**. Running multiple teams simultaneously creates coordination overhead that exceeds the parallelism benefit.

### File Scope Isolation
- **Every agent gets an explicit file scope** in its task description. This is mandatory, not optional.
- **No two agents may modify the same file**. If two lanes need to touch the same file, they are not independent -- restructure the decomposition.
- **Read access is unrestricted** -- any agent can read any file for context. Only writes are scoped.

### Git Discipline
- **Only the team lead (Commander) performs git operations**: add, commit, push, branch, merge.
- **Teammates report their changes** via SendMessage. The lead reviews and commits.
- **Rationale**: Concurrent git operations from multiple agents cause index.lock conflicts, lost staging, and corrupted state. This is not theoretical -- it has happened.

### Verification Gate
- **No lane is marked complete without verification** by the team lead.
- **No blitzkrieg is marked complete** until all lane outputs are verified and integrated.
- **Partial success is a valid outcome**: If 3 of 4 lanes succeed, commit those 3 and re-plan the failed lane.

### Context Economics
- **Check context usage before spawning**: If the lead is already at 50%+ context, spawning agents will degrade quality. Compact first or defer.
- **Prefer fewer, well-scoped agents** over many vaguely-scoped ones. Two agents with clear mandates outperform four with fuzzy boundaries.

---

## Integration with Constellation Dispatch

Blitzkrieg Teams uses Claude Code's native team infrastructure for **Claude-to-Claude** parallelism. For dispatching to **non-Claude constellation agents** (Psyche, Ajna, Adjudicator via Codex, Cartographer via Gemini), use the repo's dispatch system:

```bash
# Dispatch to non-Claude agents via agent inbox folders
bash orchestration/scripts/dispatch.sh <agent> "<TOPIC>" "<DESC>" "" "<KIND>" "commander"
```

**Hybrid pattern** -- Claude team + constellation dispatch:
1. Spawn a `blitz-implement` team for Claude Code lanes
2. Simultaneously dispatch to Psyche/Adjudicator/Cartographer via `dispatch.sh`
3. Monitor Claude team via TaskList, constellation via `agents/commander/inbox/pending/` for RESULT files
4. Converge both streams before declaring complete

| Target | Mechanism | Monitor Via |
|--------|-----------|-------------|
| Claude Code agents | TeamCreate + Task + SendMessage | TaskList |
| Psyche (GPT-5.3-codex) | dispatch.sh -> `agents/psyche/inbox/` | RESULT files in commander inbox |
| Ajna (Kimi K2.5) | dispatch.sh -> `agents/ajna/inbox/` | RESULT files in commander inbox |
| Adjudicator (Codex CLI) | dispatch.sh -> `agents/adjudicator/inbox/` | RESULT files in commander inbox |
| Cartographer (Gemini CLI) | dispatch.sh -> `agents/cartographer/inbox/` | RESULT files in commander inbox |

---

## Anti-Patterns

1. **Blitzkrieg for sequential work**: If Lane B needs Lane A's output, they are not parallel. Use the Execute skill with ordered steps instead.

2. **Overlapping file scopes**: Two agents writing to the same file guarantees conflicts. Restructure the decomposition until scopes are disjoint.

3. **Fire-and-forget spawning**: Spawning agents without monitoring is resource waste. Always track via TaskList and collect via SendMessage.

4. **Git operations by teammates**: Only the team lead commits. Teammates that run git commands will corrupt the index. This rail is absolute.

5. **Spawning without decomposition**: Jumping to TeamCreate before writing the lane decomposition produces vague scopes and redundant work.

6. **Over-parallelism**: 4 agents doing 15-minute tasks each is not faster than 1 agent doing 4 tasks sequentially if the coordination overhead exceeds the time saved. Minimum useful parallelism: each lane takes 5+ minutes independently.

7. **Ignoring partial failure**: If one lane fails, do not discard the others. Commit successful lanes, re-plan the failed one.

---

## Quick Reference: Tool Sequence

```
1. TeamCreate(team_name="blitz-implement")
2. TaskCreate(description="Lane A: ...", team_name="blitz-implement")
3. TaskCreate(description="Lane B: ...", team_name="blitz-implement")
4. Task(team_name="blitz-implement", subagent_type="general-purpose", description="Lane A context...")
5. Task(team_name="blitz-implement", subagent_type="general-purpose", description="Lane B context...")
6. TaskUpdate(task_id=<lane_a_id>, assignee=<agent_a_name>)
7. TaskUpdate(task_id=<lane_b_id>, assignee=<agent_b_name>)
8. [Monitor] TaskList(team_name="blitz-implement")
9. [Collect] Read SendMessage results from teammates
10. [Verify] Check artifacts, run tests
11. [Commit] git add + git commit (team lead only)
12. [Shutdown] SendMessage(type="shutdown_request") to each teammate
```

---

## Cross-References

- `.claude/skills/plan.md` -- Plan generation (upstream; BLITZKRIEG mode feeds into this skill)
- `.claude/skills/execute.md` -- Execution tracking (downstream; logs and completion protocol)
- `.claude/skills/triage.md` -- Inbox triage (monitoring RESULT files from constellation dispatch)
- `orchestration/scripts/dispatch.sh` -- Constellation dispatch to non-Claude agents
- `orchestration/state/REF-NEO_BLITZKRIEG_BUILDOUT.md` -- Blitzkrieg architectural reference
- `orchestration/state/DYN-EXECUTION_STAGING.md` -- Execution tracking ledger
- `CLAUDE.md` -- Constitutional rules and Directive Completion Protocol

---

*Blitzkrieg Teams Skill v1.0.0 | Syncrescendence*

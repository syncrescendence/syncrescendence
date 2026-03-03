# EXECUTE SKILL
## Execution + Dispatch — Take a Plan and Make It Real

**Version**: 1.0.0
**Last Updated**: 2026-02-08
**Authority**: Oracle 13

---

## PURPOSE

Take a generated plan (from the Plan skill) and execute it: dispatch DIRECTIVE/FINGERPRINT files to agent inboxes, deploy Swarm(AgentTeams) when in Commander context, track execution via `DYN-EXECUTION_STAGING.md`, and trigger completion protocol hooks when done.

---

## WHEN TO USE

Trigger this skill when:
- A plan has been generated and approved (Plan skill output)
- Commander is orchestrating multi-agent execution
- A single-agent task needs formal execution tracking
- Sovereign issues a direct execution order
- Resuming execution after a session break

---

## PROCESS

### 1. Pre-Execution Verification

Before executing anything:

1. **Read the plan**: Load from `orchestration/state/impl/plans/` or inline
2. **Verify fingerprint**: `git rev-parse --short HEAD` must match plan's fingerprint (or document drift)
3. **Check agent availability**: Scan all target agent inboxes for capacity
4. **Confirm dependencies**: Verify prerequisite tasks/artifacts exist
5. **Ground truth**: Run `git status` to confirm clean working tree

### 2. Dispatch Phase

For each lane or task in the plan:

**Single-agent dispatch**:
```bash
bash orchestration/scripts/dispatch.sh <agent> "<TOPIC>" "<DESCRIPTION>" "" "<KIND>" "commander"
```

**Multi-agent Swarm deployment** (Commander only):
```bash
# Lane A — Commander executes directly
# Lane B — Dispatch to Adjudicator
bash orchestration/scripts/dispatch.sh adjudicator "LANE_B" "description" "" "DIRECTIVE" "commander"
# Lane C — Dispatch to Cartographer
bash orchestration/scripts/dispatch.sh cartographer "LANE_C" "description" "" "SURVEY" "commander"
# Lane D — Dispatch to Psyche
bash orchestration/scripts/dispatch.sh psyche "LANE_D" "description" "" "TASK" "commander"
```

Each dispatch creates a `TASK-*.md` in the target agent's `inbox/pending/`. The `dispatch.sh` script auto-injects:
- `Reply-To: commander` (bidirectional feedback)
- `CC: commander` (visibility)
- Ledger entry via `append_ledger.sh`

### 3. Direct Execution Phase

For work Commander executes directly (Lane A or single-agent plans):

1. **Execute the work**: Code changes, file operations, integrations
2. **Commit incrementally**: Semantic prefixes (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`)
3. **Verify after each step**: Run relevant verification before proceeding
4. **Log to execution staging**: Append progress to `DYN-EXECUTION_STAGING.md`

### 4. Execution Tracking

Maintain real-time state in `DYN-EXECUTION_STAGING.md`:

```markdown
### DIRECTIVE-<id> | YYYY-MM-DD HH:MM
- **Plan**: PLAN-<mode>-YYYY-MM-DD-<slug>.md
- **Branch**: <branch>
- **Fingerprint**: <git-short-hash>
- **Outcome**: IN_PROGRESS | SUCCESS | PARTIAL | FAILED
- **Lanes**:
  | Lane | Agent | Status | Commits | Notes |
  |------|-------|--------|---------|-------|
  | A | commander | COMPLETE | 3 | direct execution |
  | B | adjudicator | IN_PROGRESS | — | awaiting RESULT |
  | C | cartographer | PENDING | — | dispatched |
```

### 5. Convergence Phase

When lanes complete:

1. **Collect RESULTs**: Check `agents/commander/inbox/pending/` for `RESULT-*.md` files
2. **Verify lane outputs**: Confirm each lane's success criteria met
3. **Integrate if needed**: Merge outputs from parallel lanes
4. **Handle failures**: Re-dispatch failed lanes or escalate to Sovereign

### 6. Completion Protocol

After all lanes converge (or plan is declared complete/failed):

1. **Produce execution log** in `DYN-EXECUTION_STAGING.md`:
   - Header: `### DIRECTIVE-<id> | YYYY-MM-DD HH:MM`
   - Metadata: Branch, Fingerprint, Outcome, Commits count, Changes summary
   - Body: Directives executed, Decisions made, Commit log
2. **Update ledgers**:
   ```bash
   bash orchestration/scripts/append_ledger.sh COMPLETE commander sovereign "<task-id>" "" "<intention-link>"
   ```
3. **Trigger reviewtrospective**: If the task was non-trivial, invoke the reviewtrospective skill
4. **Final git status**: Verify no uncommitted work remains
5. **Notify Sovereign**: If dispatched by Sovereign, write RESULT to `sovereign/`

---

## SWARM DEPLOYMENT (Commander Only)

When Commander needs maximum parallelism:

1. **Assess the work**: How many independent streams exist?
2. **Map to agents**: Each stream to the best-fit constellation member
3. **Dispatch simultaneously**: All `dispatch.sh` calls in rapid sequence
4. **Monitor via triage**: Periodically invoke triage skill to check for RESULTs
5. **Converge**: Collect all RESULTs, integrate, and close

**Swarm constraints**:
- Maximum 4 parallel lanes (commander + 3 dispatched agents)
- Each lane gets a unique DIRECTIVE with explicit scope
- Cross-lane dependencies must be explicit in the plan
- Commander holds the integration responsibility

---

## ANTI-PATTERNS

1. **Executing without a plan**: Even simple tasks benefit from explicit success criteria. At minimum, state the objective before executing.

2. **Fire-and-forget dispatch**: Dispatching without monitoring for RESULTs creates orphaned tasks. Always track.

3. **Skipping the execution log**: Every non-trivial execution must be logged to `DYN-EXECUTION_STAGING.md`.

4. **Claiming completion without verification**: Run `git status`, check artifacts, verify success criteria before declaring COMPLETE.

5. **Monolithic commits**: Commit incrementally with semantic prefixes. One giant commit at the end loses granularity.

6. **Dispatching without Reply-To**: Always use `dispatch.sh` which auto-injects Reply-To and CC. Never write TASK files manually without these headers.

---

## CROSS-REFERENCES

- `orchestration/scripts/dispatch.sh` — Task dispatch mechanism
- `orchestration/scripts/append_ledger.sh` — Ledger event logging
- `orchestration/state/DYN-EXECUTION_STAGING.md` — Execution tracking
- `engine/TEMPLATE-EXECUTION_LOG.md` — Execution log template
- `.claude/skills/plan.md` — Plan generation (upstream)
- `.claude/skills/triage.md` — Inbox triage (monitoring)
- `.claude/skills/reviewtrospective.md` — Post-execution review (downstream)
- `CLAUDE.md` — Directive Completion Protocol

---

*Execute Skill v1.0.0 | Syncrescendence*

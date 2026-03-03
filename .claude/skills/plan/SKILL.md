# PLAN SKILL
## Strategic Planning — Mode-Driven Plan Generation and Dispatch

**Version**: 1.0.0
**Last Updated**: 2026-02-08
**Authority**: Oracle 13

---

## PURPOSE

Generate structured execution plans in one of four modes: BLITZKRIEG, SURGICAL, SURVEY, or FORTIFY. Each mode produces a plan with objective, constraints, success criteria, lane assignments, and risk assessment. Plans are dispatched to agent inboxes via `dispatch.sh`.

---

## WHEN TO USE

Trigger this skill when:
- Commander is orchestrating multi-agent work (BLITZKRIEG)
- A specific issue needs targeted resolution (SURGICAL)
- Information must be gathered before action (SURVEY)
- Quality or resilience hardening is required (FORTIFY)
- Sovereign requests a plan for any non-trivial directive

---

## MODES

### BLITZKRIEG — Parallel Multi-Agent Execution

**Owner**: Commander (specialty)
**Use when**: Multiple independent work streams can execute concurrently.

1. Decompose objective into parallel lanes (max 4: one per available agent)
2. Assign each lane to the best-fit agent:
   - Commander: orchestration, integration, complex implementation
   - Adjudicator: validation, testing, linting, formatting, debugging
   - Cartographer: corpus survey, research, 1M+ context analysis
   - Psyche: extraction, specification writing, QA review
3. Define synchronization points (where lanes must converge)
4. Set timeouts per lane (default: 30 min)
5. Dispatch DIRECTIVE/FINGERPRINT to each agent via `dispatch.sh`

**Template**:
```markdown
# BLITZKRIEG PLAN — <title>
## Issued: <timestamp> | Fingerprint: <git-short-hash>

### Objective
<single clear statement>

### Constraints
- Time: <budget>
- Context: <capacity considerations>
- Dependencies: <what must exist first>

### Success Criteria
- [ ] <measurable outcome 1>
- [ ] <measurable outcome 2>

### Lanes
| Lane | Agent | Task | Timeout | Sync Point |
|------|-------|------|---------|------------|
| A | commander | ... | 30m | convergence-1 |
| B | adjudicator | ... | 30m | convergence-1 |
| C | cartographer | ... | 30m | — |

### Risk Assessment
- **High**: <what could fail catastrophically>
- **Medium**: <what could slow progress>
- **Low**: <minor concerns>
- **Mitigation**: <fallback plan>

### Dispatch Commands
bash dispatch.sh adjudicator "LANE_B_TOPIC" "description" "" "DIRECTIVE" "commander"
bash dispatch.sh cartographer "LANE_C_TOPIC" "description" "" "SURVEY" "commander"
```

### SURGICAL — Targeted Single-Issue Resolution

**Owner**: Any agent
**Use when**: One specific issue needs focused resolution.

1. Identify the exact issue (file, function, error, state)
2. Determine root cause hypothesis
3. Define the minimal change set
4. Assign to single best-fit agent
5. Set tight success criteria

**Template**:
```markdown
# SURGICAL PLAN — <issue>
## Issued: <timestamp>

### Issue
<precise description with file paths and line numbers>

### Root Cause Hypothesis
<best guess, with evidence>

### Minimal Change Set
- [ ] File: <path> — Change: <description>

### Assigned To
<agent> — Rationale: <why this agent>

### Success Criteria
- [ ] <specific verification command passes>

### Risk
- Blast radius: <what else could break>
- Rollback: <how to undo>
```

### SURVEY — Information Gathering Before Action

**Owner**: Cartographer (specialty)
**Use when**: Decisions require data not yet available.

1. Define the question(s) to answer
2. Identify sources to consult (corpus, APIs, external)
3. Set scope boundaries (prevent unbounded exploration)
4. Define output format for findings
5. Dispatch SURVEY tasks to Cartographer or appropriate agent

**Template**:
```markdown
# SURVEY PLAN — <topic>
## Issued: <timestamp>

### Questions
1. <specific question>
2. <specific question>

### Sources
- Internal: <repo paths, ledgers, CANON docs>
- External: <APIs, web resources>

### Scope Boundaries
- DO scan: <included areas>
- DO NOT scan: <excluded areas>
- Time limit: <max duration>

### Expected Output Format
<markdown report structure>

### Assigned To
cartographer — Corpus survey specialist
```

### FORTIFY — Quality and Resilience Hardening

**Owner**: Adjudicator (specialty)
**Use when**: Existing systems need hardening, validation, or stress testing.

1. Identify the target system/component
2. Define quality dimensions to assess (correctness, consistency, completeness, resilience)
3. Design test/validation strategy
4. Set acceptance thresholds
5. Dispatch to Adjudicator with validation criteria

**Template**:
```markdown
# FORTIFY PLAN — <target>
## Issued: <timestamp>

### Target
<system, component, or process to harden>

### Quality Dimensions
- Correctness: <what should be true>
- Consistency: <cross-references that must align>
- Completeness: <gaps to identify>
- Resilience: <failure modes to test>

### Validation Strategy
1. <test or check>
2. <test or check>

### Acceptance Thresholds
- Pass: <criteria>
- Fail: <criteria>

### Assigned To
adjudicator — Validation specialist
```

---

## PROCESS

### 1. Mode Selection

Determine mode from context:
- Sovereign says "blitzkrieg" or "parallel" or "all hands" -> BLITZKRIEG
- Sovereign says "fix" or "resolve" or targets a specific issue -> SURGICAL
- Sovereign says "investigate" or "survey" or "find out" -> SURVEY
- Sovereign says "harden" or "validate" or "fortify" -> FORTIFY
- If unclear, default to SURGICAL (smallest blast radius)

### 2. Plan Generation

1. Read current state: `git status`, `ARCH-INTENTION_COMPASS.md`, relevant ledgers
2. Identify constraints: time, context capacity, agent availability
3. Generate plan using appropriate template
4. Write plan to `orchestration/state/impl/plans/PLAN-<mode>-YYYY-MM-DD-<slug>.md`

### 3. Plan Dispatch

For each lane/assignment in the plan:
```bash
bash orchestration/scripts/dispatch.sh <agent> "<TOPIC>" "<DESCRIPTION>" "" "<KIND>" "commander"
```

### 4. Plan Tracking

- Log plan creation to `DYN-GLOBAL_LEDGER.md` via `append_ledger.sh`
- Track lane completion via inbox RESULT files
- Report plan completion when all lanes converge

---

## ANTI-PATTERNS

1. **BLITZKRIEG for single tasks**: Do not spin up multi-agent coordination for work one agent can handle. Use SURGICAL.

2. **Unbounded SURVEY**: Always set scope boundaries and time limits. Cartographer can explore forever.

3. **Planning without dispatching**: A plan without dispatch is a document, not an operation.

4. **Overloading agents**: Check agent inbox depth before dispatching. Do not pile 5 tasks on one agent.

5. **Missing sync points**: BLITZKRIEG lanes that depend on each other need explicit sync points.

---

## CROSS-REFERENCES

- `orchestration/scripts/dispatch.sh` — Task dispatch mechanism
- `orchestration/state/impl/plans/` — Plan archive
- `engine/REF-NEO_BLITZKRIEG_BUILDOUT.md` — Blitzkrieg reference
- `engine/REF-FLEET_COMMANDERS_HANDBOOK.md` — Fleet operations
- `README.md` — Agent/avatar assignments
- `.claude/skills/triage.md` — Inbox triage (pre-plan)
- `.claude/skills/execute.md` — Plan execution (post-plan)

---

*Plan Skill v1.0.0 | Syncrescendence*

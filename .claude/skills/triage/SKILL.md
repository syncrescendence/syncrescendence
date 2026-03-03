# TRIAGE SKILL
## Inbox Triage — Scan, Categorize, and Process Agent Inbox Items

**Version**: 1.0.0
**Last Updated**: 2026-02-08
**Authority**: Oracle 13

---

## PURPOSE

Scan an agent's `agents/AGENT/inbox/pending/` for pending dispatch items, categorize by priority and kind, acknowledge completions, claim actionable tasks, flag blocked items, and report stale items to Sovereign. Extends to external sources: Discord, Linear, ClickUp, GitHub, Backlog.

---

## WHEN TO USE

Trigger this skill when:
- Starting any session (Directive Initialization Protocol step 1)
- Resuming after compaction or context switch
- An agent has been idle and needs to pick up work
- Periodic sweep requested by Sovereign or Commander
- External platform notifications need routing into the inbox system

**Note**: The `triage_inbox.sh` script handles the mechanical scan. This skill provides the semantic triage layer — deciding what to do with each item.

---

## PROCESS

### 1. Inbox Scan Phase

Scan `agents/<agent>/inbox/pending/` for these file types:
- `TASK-*.md` — Actionable work items
- `CONFIRM-*.md` — Completion confirmations from other agents
- `RESULT-*.md` — Execution results returned from dispatched tasks
- `DIRECTIVE-*.md` — Strategic directives from Commander or Sovereign
- `SURVEY-*.md` — Information gathering requests
- `EVIDENCE-*.md` — Supporting data from other agents
- `RECEIPT-*.md` — Acknowledgment receipts

### 2. Categorization Phase

For each item, extract and assess:

| Field | Source | Action |
|-------|--------|--------|
| **Priority** | `Priority:` header (P0-P3) | P0 = immediate, P1 = session, P2 = sprint, P3 = backlog |
| **Kind** | `Kind:` header | Determines processing path |
| **Status** | `Status:` header | PENDING = claimable, IN_PROGRESS = check staleness |
| **Staleness** | File modification time | >60 min IN_PROGRESS = stale, report to Sovereign |
| **Reply-To** | `Reply-To:` header | Route responses back to originator |
| **CC** | `CC:` header | Additional agents to notify |

### 3. Action Phase

For each categorized item:

**TASK (PENDING)**: Claim it.
1. Update `Status: PENDING` to `Status: IN_PROGRESS`
2. Set `Claimed-By: <this-agent>`
3. Set `Claimed-At: <timestamp>`
4. Move file to `10-IN_PROGRESS/` if kanban dirs exist
5. Begin execution or queue for this session

**CONFIRM / RESULT**: Acknowledge it.
1. Read the content, verify it addresses the original dispatch
2. Update originating task status if applicable
3. Move to `40-DONE/` or `RECEIPTS/`
4. Log to `DYN-GLOBAL_LEDGER.md` via `append_ledger.sh`

**DIRECTIVE**: Elevate it.
1. If P0, interrupt current work and execute
2. If P1-P3, queue according to priority
3. Acknowledge receipt to Reply-To agent

**Blocked items**: Flag them.
1. Note the blocker in triage report
2. Do not claim — leave in INBOX0
3. Report to Sovereign via `sovereign/` if P0/P1

**Stale items**: Escalate.
1. IN_PROGRESS items older than 60 min with no progress
2. Write escalation note to `sovereign/STALE-<task-id>.md`
3. Optionally reassign via `dispatch.sh`

### 4. External Source Triage

When triaging external platforms:

**Linear**: Query via API for issues assigned to this agent's domain
```bash
# Check for new/updated Linear issues
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"{ issues(filter:{state:{name:{in:[\"Todo\",\"In Progress\"]}}}) { nodes { id title priority state { name } } } }"}'
```

**ClickUp**: Query for tasks in active lists
**GitHub**: Check for assigned issues, PR review requests
**Backlog**: Scan `DYN-BACKLOG.md` for items matching agent's domain

### 5. Triage Report

Produce a summary:

```markdown
## TRIAGE REPORT — <agent> — <timestamp>

### Claimed (this session)
- TASK-20260208-foo.md (P1, TASK) — claimed

### Acknowledged
- RESULT-adjudicator-20260208-bar.md — verified, archived
- CONFIRM-cartographer-20260208-baz.md — acknowledged

### Blocked
- TASK-20260207-quux.md — blocked by PROJ-006b (substrate)

### Stale (escalated)
- TASK-20260206-old.md — IN_PROGRESS 3h, escalated to Sovereign

### External
- Linear SYN-25: Todo, P1 — no inbox match, creating TASK
- ClickUp #abc: overdue — flagged
```

---

## ANTI-PATTERNS

1. **Claiming without capacity**: Do not claim P1 tasks if current session is already saturated. Queue them.

2. **Ignoring CONFIRM/RESULT files**: These are completion signals. Processing them closes feedback loops.

3. **Stale hoarding**: Do not leave stale items in INBOX0 hoping they resolve. Escalate.

4. **Cross-agent triage**: Each agent triages their OWN inbox only. Commander may triage all inboxes for oversight but should not claim other agents' tasks.

5. **Skipping the ledger**: Every claim and completion must be logged via `append_ledger.sh`.

---

## CROSS-REFERENCES

- `orchestration/scripts/triage_inbox.sh` — Mechanical scan script
- `orchestration/scripts/dispatch.sh` — Task dispatch (for reassignment)
- `orchestration/scripts/append_ledger.sh` — Ledger logging
- `orchestration/state/DYN-GLOBAL_LEDGER.md` — Event log
- `agents/` — Agent inbox root
- `sovereign/` — Sovereign decision queue
- `CLAUDE.md` — Directive Initialization Protocol (step 1)

---

*Triage Skill v1.0.0 | Syncrescendence*

# UPDATE UNIVERSAL LEDGER SKILL
## Universal Ledger Update — Atomic Multi-Ledger Synchronization

**Version**: 1.0.0
**Last Updated**: 2026-02-08
**Authority**: Oracle 13

---

## PURPOSE

Single skill to update all ledgers atomically using the safe backup-validate-rename pattern. Covers internal CSV ledgers (tasks.csv, projects.csv, sprints.csv, burndown.csv), external platforms (Linear, ClickUp), and backlog state files.

---

## WHEN TO USE

Trigger this skill when:
- A task completes and ledgers need updating
- Project status changes (started, blocked, completed)
- Sprint boundaries (new sprint, sprint close)
- Burndown data needs recording
- External platforms (Linear, ClickUp) need syncing with repo state
- Backlog items change status

**Rule**: Ledger updates are NEVER deferred. Update immediately upon state change.

---

## PROCESS

### 1. Determine Update Scope

Identify which ledgers need updating:

| Event | Ledgers Affected |
|-------|-----------------|
| Task complete | tasks.csv, burndown.csv, Linear, ClickUp (if applicable) |
| Task created | tasks.csv, Linear (if tracked there) |
| Project status change | projects.csv, Linear project, ClickUp |
| Sprint boundary | sprints.csv, burndown.csv |
| Backlog change | DYN-BACKLOG.md, tasks.csv |

### 2. Atomic Write Protocol (CSV Ledgers)

For each CSV ledger that needs updating:

```
Step 1: BACKUP    cp {ledger}.csv {ledger}.csv.bak.$(date +%Y%m%d%H%M%S)
Step 2: READ      Load current CSV content
Step 3: MODIFY    Apply requested changes in memory
Step 4: VALIDATE  Check: required columns present, no malformed rows,
                  row count delta is expected, no duplicate IDs
Step 5: WRITE     Write to temp file: {ledger}.csv.tmp
Step 6: VERIFY    Confirm temp file is valid CSV with correct headers
Step 7: RENAME    mv {ledger}.csv.tmp {ledger}.csv
Step 8: CONFIRM   Report changes made, row counts before/after
```

**If validation fails at any step**: Stop. Do NOT proceed with rename. Report the specific validation error. Keep backup intact.

### 3. CSV Ledger Specifications

**tasks.csv** — `orchestration/state/tasks.csv`
```
Required columns: id, project_id, name, type, status, priority, owner
Valid statuses: TODO, IN_PROGRESS, DONE, BLOCKED, CANCELLED
Valid priorities: P0, P1, P2, P3
```

**projects.csv** — `orchestration/state/projects.csv`
```
Required columns: id, name, type, status, priority, owner
Valid statuses: ACTIVE, BLOCKED, COMPLETE, ARCHIVED
```

**sprints.csv** — `orchestration/state/sprints.csv`
```
Required columns: id, name, start_date, end_date, status, goal
Valid statuses: PLANNED, ACTIVE, COMPLETE
```

**burndown.csv** — `orchestration/state/burndown.csv`
```
Required columns: date, sprint_id, total_points, completed_points, remaining_points
```

### 4. Linear API Sync

When Linear issues need updating:

```bash
# Update issue status
TMPFILE=$(mktemp)
cat > "$TMPFILE" << 'GRAPHQL'
mutation {
  issueUpdate(id: "<issue-id>", input: { stateId: "<state-id>" }) {
    success
    issue { id title state { name } }
  }
}
GRAPHQL

curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"query\": $(jq -Rs . < "$TMPFILE")}"
rm -f "$TMPFILE"
```

**Linear state IDs**:
- Done: `4f15cb0a-a5a2-45e2-b441-05b468fedea1`
- In Progress: `17db8a8b-46fd-4681-9703-ced64059738c`
- Todo: `910fb97d-1954-4e7c-a6ed-8e43842eb372`
- Backlog: `e4201e12-3448-459f-bdbc-e41a037c0bdb`

### 5. ClickUp API Sync

When ClickUp tasks need updating:

```bash
# Update task status
curl -s -X PUT "https://api.clickup.com/api/v2/task/<task-id>" \
  -H "Authorization: $CLICKUP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "<new-status>"}'
```

### 6. Backlog State Update

Update `DYN-BACKLOG.md` for project-level status changes:

1. Read current backlog state
2. Find the project entry
3. Update status, percentage, notes
4. Write back using atomic pattern (backup first)

### 7. Global Ledger Event

After all updates complete, log the event:
```bash
bash orchestration/scripts/append_ledger.sh <EVENT> <FROM> <TO> <TASK_ID>
```

### 8. Verification

After all ledger updates:
1. Confirm CSV row counts are as expected
2. Verify no duplicate IDs introduced
3. Check that external API calls returned success
4. Run `git diff` on changed ledger files to verify the delta

---

## ANTI-PATTERNS

1. **Partial updates**: If tasks.csv and projects.csv both need updating, update BOTH. Do not leave ledgers inconsistent.

2. **Skipping backup**: Always backup before modifying. The `.bak` file is your rollback path.

3. **Direct file writes**: Never write directly to the ledger file. Always use the temp-validate-rename pattern.

4. **Deferring to later**: Ledger updates happen NOW, not "after the next task." Stale ledgers erode trust in ground truth.

5. **Ignoring API failures**: If Linear or ClickUp API calls fail, log the failure and flag for manual resolution. Do not silently skip.

6. **Editing .bak files**: Backup files are read-only artifacts. Never modify them.

---

## CROSS-REFERENCES

- `orchestration/state/tasks.csv` — Task ledger
- `orchestration/state/projects.csv` — Project ledger
- `orchestration/state/sprints.csv` — Sprint ledger
- `orchestration/state/burndown.csv` — Burndown tracking
- `orchestration/state/DYN-BACKLOG.md` — Backlog state
- `orchestration/state/DYN-GLOBAL_LEDGER.md` — Event log
- `orchestration/scripts/append_ledger.sh` — Ledger event logging
- `orchestration/scripts/sync_ledgers.py` — Ledger sync utility
- `.claude/commands/project/update-ledgers.md` — Slash command wrapper

---

*Update Universal Ledger Skill v1.0.0 | Syncrescendence*

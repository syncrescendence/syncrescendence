# REF -- Jira <-> Linear Sync Map

## Bidirectional Issue Mapping

This file maps Jira issues to their Linear counterparts for manual or automated sync.

**Last synced**: 2026-02-10T21:00Z (Commander, Session)

---

## Instance Details

| System | URL | Project | Board/Team |
|--------|-----|---------|------------|
| Jira Cloud | `https://syncrescendence.atlassian.net` | SCRUM (ID: 10000) | Board 1 (simple) |
| Linear | `https://linear.app` | SYN Team (`7b039eee`) | -- |

---

## Epic <-> Linear Project Map

| Jira Epic | Jira Key | Jira ID | Linear Project | PROJ Code | Status |
|-----------|----------|---------|---------------|-----------|--------|
| Tool Onboarding | SCRUM-5 | 10036 | Tool Onboarding | PROJ-TOOLS | Active |
| Ontology Substrate | SCRUM-6 | 10037 | Ontology Substrate | PROJ-006b | Active |
| Live Intelligence Substrate | SCRUM-7 | 10038 | Live Intelligence | Epic 1 | Active |
| Constellation Agents | SCRUM-8 | 10039 | Constellation Agents | PROJ-AGENTS | Active |
| Automation & Integration | SCRUM-9 | 10040 | Automation Master | PROJ-AUTO | Active |

---

## Story <-> Linear Issue Map

| Jira Story | Jira Key | Jira ID | Linear Issue | Points | Sprint | Status |
|------------|----------|---------|-------------|--------|--------|--------|
| Jira Onboarding | SCRUM-10 | 10041 | SYN-51 | 8 | Sprint 0 | In Progress |
| Live Ledger Pipeline | SCRUM-11 | 10042 | SYN-31 | 5 | Sprint 0 | In Progress |
| Todoist Integration | SCRUM-12 | 10043 | SYN-53 | 5 | Sprint 0 | To Do |
| MBA Ajna Setup | SCRUM-13 | 10044 | SYN-35 | 8 | Sprint 0 | To Do |
| Webhook Bridge | SCRUM-14 | 10045 | -- | 13 | Backlog | To Do |

---

## Sprint Map

| Jira Sprint | Sprint ID | State | Dates | Linear Cycle |
|-------------|-----------|-------|-------|-------------|
| SCRUM Sprint 0 | 2 | active | 2026-02-10 to 2026-02-24 | -- (manual) |
| SCRUM Sprint 1 | 1 | future | TBD | -- |

---

## Archived Seed Issues

| Key | Original Summary | Disposition |
|-----|-----------------|-------------|
| SCRUM-1 | Task 1 | Marked Done (seed data) |
| SCRUM-2 | Task 2 | Marked Done (seed data) |
| SCRUM-3 | Task 3 | Marked Done (seed data) |
| SCRUM-4 | Subtask 2.1 | Marked Done (seed data) |

---

## Status Mapping (Workflow)

| Jira Status | Jira ID | Transition ID | Linear State | Linear ID |
|-------------|---------|---------------|-------------|-----------|
| To Do | 10000 | 11 | Todo | `910fb97d` |
| In Progress | 10001 | 21 | In Progress | `17db8a8b` |
| In Review | 10002 | 31 | In Progress | `17db8a8b` |
| Done | 10003 | 41 | Done | `4f15cb0a` |

---

## Key API IDs

| Entity | ID | Notes |
|--------|-----|-------|
| Project ID | 10000 | SCRUM project |
| Board ID | 1 | SCRUM board (type: simple) |
| Active Sprint ID | 2 | Sprint 0 (2026-02-10 to 2026-02-24) |
| Future Sprint ID | 1 | Sprint 1 (not started) |
| Account ID | `712020:6de8ce37-716e-4c5d-a6ac-729e324bc46c` | Phillip Truong |
| Epic type ID | 10001 | -- |
| Story type ID | 10004 | -- |
| Task type ID | 10003 | -- |
| Bug type ID | 10007 | -- |
| Feature type ID | 10005 | -- |
| Subtask type ID | 10002 | -- |
| Story Points field | customfield_10016 | Estimation |
| Sprint field | customfield_10020 | Sprint assignment |
| Rank field | customfield_10019 | Backlog ordering |

---

## Sprint 0 Velocity Budget

| Story | Points | Status |
|-------|--------|--------|
| SCRUM-10 (Jira Onboarding) | 8 | In Progress |
| SCRUM-11 (Live Ledger) | 5 | In Progress |
| SCRUM-12 (Todoist) | 5 | To Do |
| SCRUM-13 (MBA Ajna) | 8 | To Do |
| **Total** | **26** | -- |

---

## Sovereign Actions Required

- [ ] **Convert SCRUM board from "simple" to "Scrum"** -- enables velocity charts, burndown, sprint planning view. Path: Board Settings > Board Type.
- [ ] **Approve MCP server addition** -- `@rokealvo/jira-mcp` in `~/.claude.json` (config in design doc).
- [ ] **Review Sprint 0 stories** -- 26 points committed. Adjust if needed.

---

*Updated by Commander (COO) during SYN-51 implementation. This is the source-of-truth for Jira <-> Linear cross-references.*

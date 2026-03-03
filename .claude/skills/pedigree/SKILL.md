# PEDIGREE SKILL
## Ajna Pedigree — Session Context Management

**Version**: 2.0.0
**Last Updated**: 2026-02-01
**Authority**: Oracle 13

---

## PURPOSE

Manage Ajna pedigree—the lineage and context that enables session continuity without explicit handoffs. Pedigree supersedes handoff protocol for repository-centric work. Now automated via `ajna_pedigree.sh` Stop hook (captures decision lineage to `DYN-PEDIGREE_LOG.md`).

---

## WHEN TO USE

Trigger this skill when:
- Starting a new session (any Oracle or execution session)
- Resuming after compaction
- Preparing context for Claude Code execution
- Creating Blitzkrieg packages
- Transitioning between sessions

---

## PEDIGREE VS HANDOFF

| Aspect | Handoff | Pedigree |
|--------|---------|----------|
| **Context** | Document-centric | Repository-centric |
| **Assumption** | Next instance lacks context | Repository IS the context |
| **Format** | Detailed narrative | Structured reference |
| **Use Case** | Web app transitions | Claude Code continuity |

**Rule**: Use Pedigree when the repository is authoritative. Use Handoff only for web-app-only sessions.

---

## PEDIGREE COMPONENTS

### 1. Session Lineage
```yaml
oracle:
  current: 12
  predecessor: 11
  trajectory: "Vision(0-2) → Structure(3-5) → Recovery(6-7) → Content(8-9) → Infrastructure(10-11) → Expansion(12+)"
```

### 2. Campaign Status
```yaml
campaign:
  active_blitzkrieg: 45
  last_complete: 44
  parallel_streams: [A, B]
```

### 3. Project State
```yaml
projects:
  active: [PROJ-002, PROJ-012, PROJ-014]
  blocked: [PROJ-004, PROJ-005, PROJ-006, PROJ-007, PROJ-015]
  complete: [PROJ-001, PROJ-011]
```

### 4. Key Decisions
```yaml
decisions:
  - "Constellation architecture: 3 Claude + 1 Gemini + 1 ChatGPT"
  - "Model routing: Opus for comprehensive, Sonnet for tactical"
  - "Temporal vs evergreen: Archive temporal, CANON evergreen"
```

### 5. Active Intentions
```yaml
intentions:
  urgent: [INT-1201, INT-1202, INT-1209]
  sprint: [INT-1203, INT-1210-1213]
```

---

## PROCESS

### 1. Session Initialization

When starting a session:

1. Read `ORACLE_ARC.md` for trajectory
2. Read latest `EXECUTION_LOG-*` for recent activity
3. Read `DYN-BACKLOG.md` for project status
4. Read `ARCH-INTENTION_COMPASS.md` for active intentions
5. Synthesize into working context

### 2. Context Document Creation

When creating Blitzkrieg pedigree:

```markdown
# ORACLE [N] PEDIGREE: BLITZKRIEG [M]
## [Title]

**Issued**: [date]
**Oracle**: [number]
**Blitzkrieg**: [number]
**Scope**: [brief description]

---

## STRATEGIC CONTEXT
[Campaign progress, what led here]

## BLITZKRIEG STRUCTURE
[Streams, models, durations]

## KEY DECISIONS
[Decisions made this session]

## DEPENDENCIES
[What this enables, what it requires]

## LEDGER UPDATES EXPECTED
[Projects and tasks affected]

## COMPANION DIRECTIVES
[Links to stream directives]
```

### 3. Cross-Platform Pedigree

When work spans multiple platforms:

```yaml
cross_platform:
  claude_web: "Oracle strategic synthesis"
  claude_code_1: "Stream A execution"
  claude_code_2: "Stream B execution"
  gemini: "Validation and cross-check"
  chatgpt: "Alternative perspective"
```

---

## OUTPUT FORMAT

### Quick Pedigree (In-Context)
```markdown
**Oracle 12 | Blitzkrieg 45 | 2026-01-12**
- Campaign: Expansion phase (12+)
- Last complete: Blitzkrieg 44 (model specification, intention compass)
- Active: PROJ-002 (60%), PROJ-012 (80%), PROJ-014 (40%)
- Focus: IIC completion + Skills genesis
```

### Full Pedigree Document
See template in Process section above.

---

## EXAMPLES

### Good Pedigree Opening

"This is Oracle 12, continuing the Expansion phase. Blitzkriegs 43-44 established constellation architecture and formalized model specification. We're now executing Blitzkrieg 45 to complete IIC configuration and create process Skills."

### Good Cross-Session Reference

"Per Blitzkrieg 44 findings (IMPLEMENTATION-MAP.md), INT-1210-1212 can be marked resolved—canonical coverage is sufficient."

---

## ANTI-PATTERNS

1. **Starting fresh**: Never begin without reading recent execution logs

2. **Ignoring ledgers**: Always verify tasks.csv and projects.csv for ground truth

3. **Handoff when Pedigree applies**: Repository work uses Pedigree, not Handoff

4. **Over-documentation**: Pedigree is structured reference, not narrative essay

5. **Missing lineage**: Always include Oracle number and trajectory position

---

## MAINTENANCE

- Update ORACLE_ARC.md at session end
- Archive completed pedigrees in execution logs
- Verify ledger updates before claiming completion

---

## INTEGRATION WITH CANON-25100

CANON-25100 Part IX defines the Ajna Pedigree Protocol (formerly Oracle Pedigree). This skill provides:
- **Process guidance** for session initialization
- **Template structures** for pedigree documents
- **Anti-pattern warnings** to avoid common mistakes

When executing this skill:
1. Read CANON-25100 Part IX for protocol authority
2. Apply pedigree components as specified
3. Create structured pedigree documents
4. Maintain cross-platform tracking

---

## CROSS-REFERENCES

- CANON-25100 Part IX - Ajna Pedigree Protocol (authority)
- `orchestration/scripts/ajna_pedigree.sh` - Automated Stop hook
- `orchestration/state/DYN-PEDIGREE_LOG.md` - Auto-generated pedigree log
- `orchestration/state/ARCH-INTENTION_COMPASS.md` - Active intentions
- `orchestration/state/DYN-BACKLOG.md` - Project status
- `orchestration/logs/EXECUTION_LOG-*` - Recent activity

---

*Pedigree Skill v1.0.0 | Syncrescendence*

# METHOD KAIZEN SKILL
## Method + Technique Improvement — Pattern Crystallization and Automation

**Version**: 1.0.0
**Last Updated**: 2026-02-08
**Authority**: Oracle 13

---

## PURPOSE

Post-reviewtrospective analysis to identify repeatable improvements, automation opportunities, and pattern crystallization. Updates `praxis/` practice files with new patterns. Creates new skills or hooks when a pattern has been used 3+ times. Feeds back into agent memory architecture updates.

---

## WHEN TO USE

Trigger this skill when:
- A reviewtrospective identifies improvement candidates (METHOD, TECHNIQUE, or AUTOMATION)
- Multiple reviewtrospectives show a recurring pattern (3+ occurrences threshold)
- Sovereign requests process optimization
- A manual process is identified as automatable
- Session-end review reveals repeated friction points

---

## PROCESS

### 1. Pattern Mining

Scan `DYN-REVIEWTROSPECTIVE_LOG.md` for improvement candidates:

```bash
grep -n "METHOD\|TECHNIQUE\|AUTOMATION" orchestration/state/DYN-REVIEWTROSPECTIVE_LOG.md
```

Categorize findings:

| Type | Definition | Action |
|------|-----------|--------|
| **METHOD** | Repeatable approach to a class of problems | Document in `praxis/practice/` |
| **TECHNIQUE** | Specific tactical trick or optimization | Add to relevant practice file |
| **AUTOMATION** | Manual process that can be scripted | Create script in `orchestration/scripts/` |

### 2. Occurrence Counting

For each candidate, count occurrences across reviews:

- **1 occurrence**: Note it. No action yet.
- **2 occurrences**: Flag it as emerging pattern. Add to watchlist.
- **3+ occurrences**: Crystallize it. This is a proven pattern.

Track in a simple tally:
```markdown
## Kaizen Watchlist
| Pattern | Occurrences | Status | Source Reviews |
|---------|------------|--------|----------------|
| Atomic CSV writes | 4 | CRYSTALLIZED | REVIEW-001, 003, 007, 012 |
| Pre-flight git check | 3 | CRYSTALLIZED | REVIEW-002, 005, 011 |
| Context budget check | 2 | EMERGING | REVIEW-008, 010 |
```

### 3. Pattern Crystallization (3+ occurrences)

When a pattern hits 3 occurrences:

**For METHOD patterns** — Create or update `praxis/practice/` file:

```markdown
# PRACTICE-<slug>.md
## <Pattern Name>

**Crystallized**: <date>
**Source Reviews**: <list>
**Occurrences**: <count>

### When to Apply
<conditions>

### Procedure
1. <step>
2. <step>

### Variations
- <context-specific variant>

### Anti-Patterns
- <what NOT to do>
```

**For TECHNIQUE patterns** — Append to the relevant existing practice file in `praxis/practice/`.

**For AUTOMATION patterns** — Create a new script:

```bash
#!/usr/bin/env bash
# <script-name>.sh — <description>
# Crystallized from: <source reviews>
# Usage: bash <script-name>.sh [args]
```

### 4. Skill/Hook Genesis

When a crystallized pattern warrants a new skill or hook:

**New Skill** (`.claude/skills/<name>.md`):
- Pattern is invoked manually and requires judgment
- Follows the established skill template format
- References the originating practice file

**New Hook** (add to `.claude/settings.json`):
- Pattern should fire automatically on a specific event
- Must be idempotent (safe to run multiple times)
- Must complete quickly (<5 seconds)
- Script goes in `orchestration/scripts/`

### 5. Update Records

After crystallization:

1. **Update DYN-REVIEWTROSPECTIVE_LOG.md**: Mark the improvement candidates as `CRYSTALLIZED` with reference to the new artifact
2. **Update practice files**: Add or update in `praxis/practice/`
3. **Log to ledger**: `bash append_ledger.sh DECISION commander — "KAIZEN-<slug>" "" "<intention-link>"`
4. **Feed to agent memory**: Invoke update_agent_memory skill if the pattern affects agent behavior

---

## KAIZEN CATEGORIES

### Velocity Improvements
- Faster execution paths
- Parallelization opportunities
- Reduced context switching
- Better tool selection

### Quality Improvements
- Stronger validation patterns
- Earlier error detection
- More precise verification
- Better test coverage

### Resilience Improvements
- Failure recovery patterns
- Rollback mechanisms
- Idempotent operations
- Graceful degradation

### Communication Improvements
- Clearer dispatch templates
- Better result formatting
- Reduced back-and-forth
- Improved agent handoff

---

## ANTI-PATTERNS

1. **Premature crystallization**: Do not create a practice file for a one-time optimization. Wait for 3 occurrences.

2. **Crystallization without verification**: The pattern must have WORKED all 3+ times. Repeating a failed approach is not kaizen.

3. **Over-engineering automation**: If the manual process takes 30 seconds and happens monthly, do not spend 2 hours automating it.

4. **Orphan patterns**: Every crystallized pattern must have a home (practice file, script, or skill). No free-floating improvements.

5. **Ignoring the feedback loop**: Kaizen feeds into agent memory. If a pattern changes how an agent should behave, the memory must be updated.

---

## CROSS-REFERENCES

- `orchestration/state/DYN-REVIEWTROSPECTIVE_LOG.md` — Review log (input)
- `praxis/practice/` — Practice files (output)
- `praxis/mechanics/` — Mechanism deep-dives
- `orchestration/scripts/` — Automation scripts (output)
- `.claude/skills/` — Skill files (potential output)
- `.claude/settings.json` — Hook configuration (potential output)
- `.claude/skills/reviewtrospective.md` — Review skill (upstream)
- `.claude/skills/update_agent_memory.md` — Memory updates (downstream)

---

*Method Kaizen Skill v1.0.0 | Syncrescendence*

# INTENTIONS SKILL
## Intent Compass — Automated Intention Extraction and Categorization

**Version**: 2.0.0
**Last Updated**: 2026-02-01
**Authority**: Oracle 13

---

## PURPOSE

Extract, categorize, and track Sovereign intentions during sessions. Now partially automated via `intent_compass.sh` UserPromptSubmit hook — intention signals are auto-captured to `DYN-INTENTIONS_QUEUE.md` on every user input. This skill handles the manual triage and categorization phase.

---

## WHEN TO USE

Trigger this skill when:
- Starting a new session (triage auto-captured intentions from `DYN-INTENTIONS_QUEUE.md`)
- Session checkpoint (categorize accumulated queue entries)
- Session is ending (consolidate and flush queue to compass)
- Reviewing previous session transcripts

**Note**: The `intent_compass.sh` hook auto-captures intention signals on every user input. This skill handles the *triage* — moving raw captures into the structured `ARCH-INTENTION_COMPASS.md`.

---

## PROCESS

### 1. Capture Phase (During Session)

Listen for intention signals:
- **Explicit**: "I want X", "We need to Y", "Don't forget Z"
- **Implicit**: Frustration expressions, repeated themes, emphasis patterns
- **Strategic**: Long-term goals, vision statements, architectural decisions
- **Tactical**: Immediate needs, blockers, quick fixes

Capture verbatim in temporary notes.

### 2. Categorization Phase (At Checkpoint)

Assign each intention to a category:

| Category | Criteria | Action Horizon |
|----------|----------|----------------|
| urgent | Requires immediate action, blocking | Same session |
| sprint | Part of current work cycle | Current Oracle |
| backlog | Future work, not blocking | Future Oracles |
| pattern | Meta-observation, recurring theme | Ongoing |
| capture | Unclear categorization | Pending triage |

### 3. ID Assignment

Format: `INT-XXYY` where:
- `XX` = Oracle number (e.g., 12)
- `YY` = Sequence within Oracle (e.g., 01, 02)

Patterns use `INT-PXXX` format.

### 4. Integration Phase (Session End)

Update `orchestration/state/ARCH-INTENTION_COMPASS.md`:
- Add new intentions to appropriate category
- Update status of resolved intentions
- Note integration references for completed items

---

## OUTPUT FORMAT

### Compass Entry
```yaml
- id: INT-XXYY
  oracle: [number]
  category: [urgent|sprint|backlog|pattern|capture]
  priority: [P0|P1|P2|P3]
  status: [active|resolved|superseded|deferred]
  text: "[Sovereign's actual words or close paraphrase]"
  interpretation: "[Your understanding of intent]"
  blocked_by: [null|dependency]
  integrated_into: [null|reference]
  notes: "[context]"
```

### Quick Capture Format
During session, use abbreviated format:
```
[urgent] Account sustainability by month end
[sprint] Complete IIC configs
[pattern] Always verify before declaring complete
```

---

## EXAMPLES

### Good Extraction

Sovereign says: "We really need to get these accounts self-sustaining by the end of the month, and I'm worried we're not moving fast enough."

**Extraction**:
```yaml
- id: INT-1201
  oracle: 12
  category: urgent
  priority: P0
  status: active
  text: "accounts become self-sustaining by month end"
  interpretation: "Revenue generation deadline 2026-01-31"
  notes: "Sovereign expressed urgency and concern about velocity"
```

### Good Resolution

When intention is addressed:
```yaml
- id: INT-1101
  status: resolved
  integrated_into: DIRECTIVE-042B
  notes: "Gemini CLI validated and ready for use"
```

---

## ANTI-PATTERNS

### Don't Do This

1. **Over-capturing**: Not every statement is an intention. Focus on actionable desires.

2. **Losing verbatim**: Don't paraphrase beyond recognition. Sovereign's words matter.

3. **Category confusion**: "Urgent" means NOW, not just important. Most things are sprint or backlog.

4. **Orphan intentions**: Every intention needs an ID and a category.

5. **False resolution**: Don't mark resolved without evidence of completion.

6. **Ignoring frustrations**: Frustration often signals important unmet intentions.

---

## MAINTENANCE

- Review compass at Oracle start and end
- Archive resolved intentions quarterly
- Pattern analysis monthly
- Dependency tracking continuous

---

## INTEGRATION WITH ARCH-INTENTION_COMPASS.md

The Compass document is the source of truth. This skill provides:
- **Process guidance** for extraction and categorization
- **Format specifications** for consistency
- **Anti-pattern warnings** to avoid common mistakes

When executing this skill:
1. Read current ARCH-INTENTION_COMPASS.md state
2. Extract new intentions from Oracle session
3. Update Compass with new entries
4. Mark resolved intentions with integration references

---

## CROSS-REFERENCES

- `orchestration/state/ARCH-INTENTION_COMPASS.md` - Living compass document
- `orchestration/state/DYN-INTENTIONS_QUEUE.md` - Auto-captured queue (hook output)
- `orchestration/scripts/intent_compass.sh` - UserPromptSubmit hook
- CANON-25100 Part IX - Ajna Pedigree Protocol

---

*Intentions Skill v1.0.0 | Syncrescendence*

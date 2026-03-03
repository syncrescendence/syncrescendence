---
name: compact-wisdom
description: Meta-auto-compact running logs into durable operational wisdom in praxis, refresh sovereign self-audit, then clear logs
provenance: syncrescendence
pipeline_stages: [VERIFY, COMMIT, MEMORY]
---

# Compact Wisdom

## Purpose

Transform accumulated running logs into standing-on-shoulders operational knowledge. This is the metabolic cycle for agent interaction data — raw logs become wisdom, wisdom persists, logs clear.

**Invoke when**: Running logs in `/Users/system/Desktop/-surface/running_logs/` have accumulated enough weight to justify synthesis (typically after 1-3 major sessions or when files exceed ~100K total).

## Protocol

Execute these phases sequentially. Do NOT skip phases or auto-approve your own work.

### Phase 0: Measure

```bash
wc -l /Users/system/Desktop/-surface/running_logs/*.md 2>/dev/null
du -sh /Users/system/Desktop/-surface/running_logs/
```

If total is <5K lines or <20KB, STOP — not enough signal to justify synthesis. Tell the Sovereign "logs are too thin, check back after the next major session."

Report the inventory: which agents have logs, how large each is.

### Phase 1: Ingest (Delegate to Sonnet agents)

Dispatch parallel subagents (model: sonnet) to read the logs — one per major log file or agent cluster. Each agent produces a structured digest:

**Digest schema** (per agent):
```
## [Agent Name] — Session Digest
### Infrastructure Lessons (things that broke and why)
### Verification Failures (what passed that shouldn't have, or vice versa)
### Process Improvements (what worked better than before)
### Anti-Patterns Observed (mistakes to never repeat)
### Sovereign Interaction Notes (prompting patterns, corrections, terminology)
### New Aphorisms (if any wisdom crystallized into a single sentence)
```

Do NOT read the raw logs into Opus context. Read ONLY the digests returned by subagents.

### Phase 2: Synthesize

Read all digests. Cross-reference against the existing compendium:

```
praxis/practice/PRAC-operational_wisdom_compendium.md
praxis/EXEMPLA-APHORISMS.md
```

Produce three outputs:

1. **Compendium Delta** — NEW lessons only. Do not duplicate existing wisdom. Append to the appropriate section of `PRAC-operational_wisdom_compendium.md`, or create a new section if the topic is genuinely novel.

2. **Aphorism Candidates** — Any single-sentence wisdom that crystallized. Append to `EXEMPLA-APHORISMS.md` under the appropriate category (or create a new category).

3. **Sovereign Self-Audit Refresh** — Update `/Users/system/Desktop/SOVEREIGN-README.md`:
   - Refresh improvement vectors based on new evidence
   - Note any patterns that improved (move from "improvement needed" to "strength")
   - Note any new patterns that emerged
   - Keep the structure: strengths, improvement vectors, directive template, meta-lesson

### Phase 3: Present for Approval

Show the Sovereign:
- Summary of what was extracted (bullet points, not full text)
- Count of new lessons added to compendium
- Count of new aphorisms
- Any sovereign self-audit changes
- Confirmation prompt: "Approve and clear logs?"

Do NOT clear logs until the Sovereign explicitly approves.

### Phase 4: Commit and Clear

Upon approval:

1. Commit the updated praxis files:
```bash
git add -- praxis/practice/PRAC-operational_wisdom_compendium.md praxis/EXEMPLA-APHORISMS.md praxis/README.md
git commit -m "wisdom(sigma): compact running logs into operational knowledge"
```

2. Clear the logs:
```bash
rm /Users/system/Desktop/-surface/running_logs/*.md
```

3. Clear the capture markers so next session starts fresh:
```bash
rm /Users/system/Desktop/-surface/running_logs/.last_capture_* 2>/dev/null
```

4. Report: "Logs cleared. Wisdom persists in praxis. Sovereign README refreshed."

## Anti-Patterns

- **DO NOT** read raw logs into Opus context — delegate to Sonnet subagents
- **DO NOT** rewrite the entire compendium — append deltas only
- **DO NOT** clear logs before Sovereign approves
- **DO NOT** duplicate wisdom that already exists in the compendium
- **DO NOT** fire this skill automatically — it requires Sovereign judgment on timing

## Architecture Notes

- Running logs are captured automatically by `running_log_capture.sh` (Stop + PreCompact hooks)
- This skill is the metabolic counterpart — capture is automatic, synthesis is sovereign-invoked
- The cycle: **auto-capture → accumulate → `/compact-wisdom` → persist → clear → repeat**
- Sovereign README lives on Desktop (not in repo) — it's personal, not canonical

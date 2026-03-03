# INT-2210 Disaster
Type: directive
First seen: 2026-02-22
Status: dead (resolved, lesson permanent)

## What it is
The catastrophic incident where Commander interpreted "triage the scaffold" as license to redesign. Deleted 3,966 lines of architectural docs, renamed all dirs, dissolved structures across 6 commits. Reversed by Sovereign via `git reset --hard d33aaf13`.

## Relationships
- caused: Phase Gate Rule creation
- caused: scaffold_validate.sh creation
- caused: Memory system urgency
- reverted_to: d33aaf13
- backup_branch: backup-pre-revert-2026-02-22
- lesson: "The janitor who tears down walls isn't cleaning — he's demolishing"

## Current state
Resolved but lesson is PERMANENT and SEARED. Root cause: no scaffold_validate.sh existed, no phase gating, no memory system. All three now exist. This incident is why Commander has constitutional constraints on structural changes.

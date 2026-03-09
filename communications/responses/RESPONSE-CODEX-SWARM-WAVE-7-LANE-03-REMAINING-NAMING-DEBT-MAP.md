# Response — Codex Swarm Wave 7 Lane 03 Remaining Naming Debt Map

**Response ID**: `RESPONSE-CODEX-SWARM-WAVE-7-LANE-03-REMAINING-NAMING-DEBT-MAP`  
**Date**: `2026-03-08`  
**Packet ID**: `PKT-20260308-codex-swarm-wave-7-lane-03-remaining-naming-debt-map`  
**Status**: `complete`

## Scope

This pass maps the `7` active warnings still present after the Wave 6 reduction into:

- later rename tranche
- permanent report-only legacy hold

No file renames or validator changes are proposed in this artifact.

## Source Basis

The current warning source is [COMMUNICATIONS-NAMING-REPORT.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REPORT.md), which shows `7` active findings.

Disposition aligns with the adjudicated buckets in [COMMUNICATIONS-NAMING-TRIAGE-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-TRIAGE-v1.md).

The assigned live file [COMMUNICATIONS-NAMING-REMAINING-DEBT-v1.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REMAINING-DEBT-v1.md) is not present at the referenced path, so this map is derived from the live report plus the triage anchor.

## Remaining Debt Map

### Later Rename Tranche

These `4` warnings are real filename mismatches and should stay queued for a coordinated rename pass:

- `communications/prompts/DISPATCH-AJNA-cc79-openclaw-command-verification.md`
- `communications/prompts/DISPATCH-AJNA-cc91-connector-verification-tranche-01.md`
- `communications/prompts/DISPATCH-MANUS-cc79-harness-command-verification.md`
- `communications/prompts/DISPATCH-PSYCHE-cc81-node-pairing-and-runtime-audit.md`

Rationale: these are active prompt-lane artifacts whose names drift from the lane convention, but fixing them cleanly requires downstream reference updates rather than isolated moves.

### Permanent Report-Only Legacy Hold

These `3` warnings should remain report-only legacy debt:

- `communications/assessments/CC79-HARNESS-INGEST-AND-GRADING.md`
  - reason: historical assessment artifact with low-return rename value
- `communications/prompts/COWORK-PERPLEXITY-PROTOTYPE-PROMPT.md`
  - reason: metadata warning on preserved prototype lineage artifact
- `communications/responses/RESPONSE-ORACLE-cc78a-architectural-remediation-hypersensing.md`
  - reason: older response artifact with legacy downstream references

## Future Reference-Update Risk

The later-rename group carries moderate reference-update risk because those prompt files are likely cited by:

- response artifacts paired to the same command-verification or tranche work
- orchestration state reports, triage notes, and handoff summaries
- dispatch packets or historical manifests that preserve current filenames as lineage

The main risk is not the rename itself; it is leaving stale links or path literals behind in state and response artifacts after the rename tranche executes.

## Recommended Next-Step Boundary

When the wrapper-cutover blocker is no longer dominant, the rename tranche should:

1. rename the `4` queued prompt artifacts together
2. update repo references in the same change set
3. rerun the communications naming report to confirm only the `3` legacy-hold warnings remain active

## Final Status

- mapped to later rename tranche: `4`
- mapped to permanent report-only legacy hold: `3`
- execution performed in this wave: `none`
- tranche result: `complete`

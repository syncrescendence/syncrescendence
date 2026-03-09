# Communications Naming Remaining Debt v1

**Date**: `2026-03-08`  
**Status**: `post-wave-6 remainder map`  
**Source report**: [COMMUNICATIONS-NAMING-REPORT.md](/Users/system/syncrescendence/orchestration/state/COMMUNICATIONS-NAMING-REPORT.md)

## 1. Summary

After Wave 6, the active communications naming surface is `7` warnings.

They divide into:

- later coordinated rename tranche: `4`
- permanent report-only legacy hold: `3`

## 2. Later Rename Tranche

These files remain real filename mismatches and should be handled together in a later coordinated rename pass:

- [DISPATCH-AJNA-cc79-openclaw-command-verification.md](/Users/system/syncrescendence/communications/prompts/DISPATCH-AJNA-cc79-openclaw-command-verification.md)
- [DISPATCH-AJNA-cc91-connector-verification-tranche-01.md](/Users/system/syncrescendence/communications/prompts/DISPATCH-AJNA-cc91-connector-verification-tranche-01.md)
- [DISPATCH-MANUS-cc79-harness-command-verification.md](/Users/system/syncrescendence/communications/prompts/DISPATCH-MANUS-cc79-harness-command-verification.md)
- [DISPATCH-PSYCHE-cc81-node-pairing-and-runtime-audit.md](/Users/system/syncrescendence/communications/prompts/DISPATCH-PSYCHE-cc81-node-pairing-and-runtime-audit.md)

Reason:

- these are active prompt-lane artifacts
- the problem is real
- fixing them cleanly requires coordinated reference updates rather than isolated renames

## 3. Permanent Report-Only Legacy Hold

These warnings should remain visible but should not drive active remediation:

- [CC79-HARNESS-INGEST-AND-GRADING.md](/Users/system/syncrescendence/communications/assessments/CC79-HARNESS-INGEST-AND-GRADING.md)
- [COWORK-PERPLEXITY-PROTOTYPE-PROMPT.md](/Users/system/syncrescendence/communications/prompts/COWORK-PERPLEXITY-PROTOTYPE-PROMPT.md)
- [RESPONSE-ORACLE-cc78a-architectural-remediation-hypersensing.md](/Users/system/syncrescendence/communications/responses/RESPONSE-ORACLE-cc78a-architectural-remediation-hypersensing.md)

Reason:

- these are retained historical lineage artifacts
- rename or metadata cleanup would have low operational return
- keeping them visible in report-first mode is enough

## 4. Recommendation

Do not widen naming strictness while wrapper retirement is still open.

When wrapper retirement is complete, a later naming tranche should:

1. batch-rename the `4` coordinated rename items
2. update references in the same change set
3. leave the `3` legacy-hold items as permanent report-only residue

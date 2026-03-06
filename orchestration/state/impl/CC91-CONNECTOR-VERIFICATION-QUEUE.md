# CC91 Connector Verification Queue

**Date**: 2026-03-06  
**Status**: active  
**Class**: verification queue

## Purpose

Move connector states from `user_claimed_configured_unverified` to evidence-backed verified states without resetting topology or violating boundary policy.

## Tranche 01 (high fanout hubs)

Priority sources:

1. `notion_surface`
2. `clickup_surface`
3. `perplexity_surface`

Dispatch packets:

1. [DISPATCH-AJNA-cc91-connector-verification-tranche-01.md](/Users/system/syncrescendence/communications/prompts/DISPATCH-AJNA-cc91-connector-verification-tranche-01.md)
2. [PACKET-MANUS-cc91-connector-verification-tranche-01.md](/Users/system/syncrescendence/communications/prompts/PACKET-MANUS-cc91-connector-verification-tranche-01.md)

Live dispatch state:

1. Ajna office task queued:
   - `/Users/system/syncrescendence/offices/ajna/inbox/pending/TASK-cc91-connector-verification-tranche-01-20260306T064820Z.md`
2. Manus task created:
   - `HN3BVTzV6zhshniaPqjJ5C`
   - `https://manus.im/app/HN3BVTzV6zhshniaPqjJ5C`
   - state: `completed_all_blocked_no_auth`
   - response: `/Users/system/syncrescendence/communications/responses/RESPONSE-MANUS-cc91-connector-verification-tranche-01.md`
   - normalized receipt applied: `/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONNECTOR-RECEIPTS-cc91-tranche-01.json`

Expected receipt path:

- `/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONNECTOR-RECEIPTS-cc91-tranche-01.json`

## Receipt Application

```bash
make -C /Users/system/syncrescendence exocortex-connector-verification-run \
  RECEIPTS=/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONNECTOR-RECEIPTS-cc91-tranche-01.json \
  BATCH_ID=cc91-tranche-01 \
  STRICT=1
```

## Artifacts

1. [EXOCORTEX-CONNECTOR-MANIFEST-CC91.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONNECTOR-MANIFEST-CC91.json)
2. [EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json)
3. [EXOCORTEX-CONNECTOR-VERIFICATION-TRACKER-CC91.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONNECTOR-VERIFICATION-TRACKER-CC91.json)
4. [EXOCORTEX-CONNECTOR-VERIFICATION-TRACKER-CC91.md](/Users/system/syncrescendence/orchestration/state/impl/EXOCORTEX-CONNECTOR-VERIFICATION-TRACKER-CC91.md)

## Guardrails

1. No secret-bearing payloads in receipts.
2. No destructive connector mutations during verification tranches.
3. All connector state transitions must be receipt-backed and replayable.

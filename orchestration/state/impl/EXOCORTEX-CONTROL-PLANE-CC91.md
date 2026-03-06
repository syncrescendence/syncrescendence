# Exocortex Control Plane — CC91

**Date**: 2026-03-05  
**Status**: active  
**Class**: implementation runbook

## Objective

Convert connector sprawl into a tractable, auditable control plane that can be projected into ontology without credential leakage.

## Artifacts

1. [guide.md](/Users/system/Desktop/guide.md)
2. [EXOCORTEX-CONNECTOR-MANIFEST-CC91.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONNECTOR-MANIFEST-CC91.json)
3. [EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json)
4. [EXOCORTEX-CONTROL-PLANE-STATUS-CC91.md](/Users/system/syncrescendence/orchestration/state/impl/EXOCORTEX-CONTROL-PLANE-STATUS-CC91.md)
5. [EXOCORTEX-CAPTURE-POLICY.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CAPTURE-POLICY.json)

## Execution

```bash
make -C /Users/system/syncrescendence exocortex-control-plane-run GUIDE=/Users/system/Desktop/guide.md
```

## Control Plane Semantics

1. `user_claimed_configured_unverified` means a connector claim exists but evidence is still pending.
2. `bounded_unverified` means topology is mapped and policy-compliant, but verification receipts are not complete.
3. Unknown source/target lists are explicit gaps and must trend to zero or be explicitly accepted as external.

## Verification Tranches

1. P1 hubs first: Slack, Notion, Linear, ClickUp, Jira/Confluence lanes.
2. For each connector, capture a sanitized receipt artifact and re-run control-plane audit.
3. Promote each tranche by re-running ontology projection and checking `ExocortexControlPlaneStatus` state transition.

## Boundary Rules

1. No tokens, cookies, secrets, raw prompts, or full transcripts in control-plane payloads.
2. Repo artifacts remain constitutional; GUI surfaces remain execution projections.
3. Every direction-changing connector change must land as typed registry/status artifacts.

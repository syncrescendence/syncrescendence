# TASK

**Kind**: TASK
**Line-ID**: ajna-cc91-connector-verification-tranche-01-20260306T064820Z
**From**: commander
**To**: ajna
**Reply-To**: offices/commander/inbox/pending
**CC**: 
**Issued-At**: 2026-03-06T06:48:20Z
**Priority**: normal
**Decision-Envelope**: office-dispatch
**Objective-Lock**: complete exactly the payload
**Expected-Output**: receipt and result artifact
**Receipts-Required**: Yes
**Completion-Condition**: task marked complete with evidence
**Escalation-Path**: offices/commander/inbox/blocked

## Payload

# DISPATCH-AJNA-cc91-connector-verification-tranche-01

**Surface**: `ajna_openclaw_browser_runtime`  
**Packet type**: `verification_dispatch`  
**Purpose**: verify high-fanout exocortex connector states on browser-native surfaces without performing destructive mutations.

## Scope

Verify these connector IDs in source UI integration panels:

1. `notion_surface--slack_surface--1`
2. `notion_surface--jira_surface--3`
3. `notion_surface--github_surface--5`
4. `clickup_surface--slack_surface--1`
5. `clickup_surface--github_surface--2`
6. `clickup_surface--jira_surface--8`
7. `perplexity_surface--notion_surface--4`
8. `perplexity_surface--github_surface--7`
9. `perplexity_surface--slack_surface--9`

## Required Outcomes

Per connector, return exactly one outcome:

- `connected`
- `not_connected`
- `partial`
- `blocked`

## Constraints

1. No credential export and no token disclosure.
2. No ownership transfer or destructive configuration changes.
3. If a connector requires privileged mutation, mark `blocked` and capture evidence.

## Return Artifacts

1. Human-readable report:
   - `/Users/system/syncrescendence/communications/responses/RESPONSE-AJNA-cc91-connector-verification-tranche-01.md`
2. Machine receipt JSON matching template:
   - `/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONNECTOR-RECEIPTS-cc91-tranche-01.json`
   - Template: `/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONNECTOR-VERIFICATION-RECEIPT-TEMPLATE-CC91.json`

## Completion Command (run locally after receipt lands)

```bash
make -C /Users/system/syncrescendence exocortex-connector-verification-run \
  RECEIPTS=/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONNECTOR-RECEIPTS-cc91-tranche-01.json \
  BATCH_ID=cc91-tranche-01 \
  STRICT=1
```

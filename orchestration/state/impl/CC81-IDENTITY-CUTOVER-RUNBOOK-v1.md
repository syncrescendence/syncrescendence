# CC81 Identity Cutover Runbook v1

**Date**: 2026-03-04  
**Status**: active  
**Class**: execution runbook

## Scope

Centralize service ownership toward `syncrescendence@gmail.com` while preserving `truongphillipthanh@icloud.com` as temporary break-glass until verification gates pass.

## Inputs

- [CC81-IDENTITY-CENTRALIZATION-PROGRAM.md](/Users/system/syncrescendence/orchestration/state/impl/CC81-IDENTITY-CENTRALIZATION-PROGRAM.md)
- [RESPONSE-MANUS-cc81-identity-cutover-capability-development.md](/Users/system/syncrescendence/communications/responses/RESPONSE-MANUS-cc81-identity-cutover-capability-development.md)
- [RESPONSE-MANUS-cc81-identity-cutover-capability-development-raw.md](/Users/system/syncrescendence/communications/responses/RESPONSE-MANUS-cc81-identity-cutover-capability-development-raw.md)
- [IDENTITY-CUTOVER-TRACKER-CC81.json](/Users/system/syncrescendence/orchestration/state/IDENTITY-CUTOVER-TRACKER-CC81.json)

## Execution Law

1. No legacy-owner removal before post-cutover verification passes.
2. One platform mutation window at a time.
3. Pre-cutover snapshots are mandatory and immutable.
4. Secrets stay local; repo artifacts remain pointer-only.
5. Reversible platforms first; irreversible flows last.

## Automation Envelope (normalized)

| Platform | Mutation automation | Required human owner action |
|---|---|---|
| GitHub | partial | billing/contact + final owner choreography |
| GCP | high | final confirmation/approval |
| Google Workspace | partial | final super-admin demotion/removal |
| Slack | conditional (Enterprise Grid) | required on non-Enterprise Grid |
| Cloudflare | low | super-admin + zone/account transfer |
| Discord | low | server/team ownership transfer |
| Notion/Coda/Linear/ClickUp/Basecamp | low | workspace/account ownership transfer |
| Airtable | partial | ownership/admin transfer via UI/admin panel |
| Atlassian (Jira/Confluence org transfer) | high-risk manual | irreversible transfer flow |

## Phase Plan

### Phase 0 — Security and Readiness

Owner: human  
Support: Commander, Manus

1. Confirm MFA and recovery controls on `syncrescendence@gmail.com`.
2. Confirm break-glass access from legacy account still works.
3. Confirm token/key inventory exists for all integrated automations.
4. Freeze non-essential credential rotations during migration windows.

Gate to proceed:
- `phase0_ready = true` in tracker.

### Phase 1 — Snapshot Capture

Owner: Commander  
Support: Manus

1. Capture platform membership/role snapshots.
2. Capture billing owner/contact pointers.
3. Capture app/integration/token pointer inventory.
4. Store snapshot receipts in repo-safe artifacts.

Gate to proceed:
- per-platform `snapshot_done` state.

### Phase 2 — Low-Blast-Radius Ownership Moves

Owner: human  
Support: Manus checklists

Surfaces:
- Basecamp
- ClickUp
- Airtable
- Coda
- Notion

Pattern:
1. Add target account as admin/owner equivalent.
2. Validate owner-only action with target account.
3. Keep legacy owner in elevated state.

Gate to proceed:
- each surface `transferred` + `verified`.

### Phase 3 — Work-Scaffold and Comms

Owner: human  
Support: Commander/Manus

Surfaces:
- Linear
- Slack
- Discord
- Jira/Confluence admin-role alignment (not full irreversible org transfer)

Pattern:
1. Promote target account.
2. Run deterministic post-checks.
3. Rotate platform tokens tied to legacy owner where applicable.

Gate to proceed:
- communication surfaces verified with live access checks.

### Phase 4 — Control Plane

Owner: human  
Support: Commander scripting

Surfaces:
- GitHub
- Google Workspace
- GCP
- Cloudflare

Pattern:
1. Promote target identity to owner/super-admin.
2. Verify policy/billing/control panel access.
3. Delay legacy-owner demotion by stabilization window.

Gate to proceed:
- each control-plane surface `rollback_ready = true`.

### Phase 5 — Irreversible/Terminal Actions

Owner: human  
Support: Commander checklists

Surfaces:
- Atlassian full org transfer (if still required)
- legacy-owner primary removal

Pattern:
1. Reconfirm all prior platforms stable.
2. Execute terminal action in isolated window.
3. Publish cutover receipt.

## Verification Harness

### Core checks per platform

1. Target account can perform owner-only action.
2. Legacy account still has rollback-capable access until explicitly removed.
3. Integrations continue functioning or are intentionally reauthorized.
4. Billing ownership/contact alignment completed.

### Tooled checks

- Manus task API for checklist generation and verification templates.
- Repo trackers and runbooks for deterministic state transitions.
- OpenClaw/Psyche runtime audit after node pairing.

## Psyche Capability Development

Current blocker:
- `openclaw nodes list --json` reports no paired nodes.

Required before Psyche can help directly:
1. Pair Commander machine with Psyche node.
2. Validate `openclaw nodes run` works for non-destructive audit commands.
3. Add Psyche runtime cutover audit receipts to communications responses.

Dispatch artifact:
- [DISPATCH-PSYCHE-cc81-node-pairing-and-runtime-audit.md](/Users/system/syncrescendence/communications/prompts/DISPATCH-PSYCHE-cc81-node-pairing-and-runtime-audit.md)

## Website Position

Build only identity-cutover-supportive website scope during migration:

1. OAuth redirect support
2. operational health/status page
3. docs surface for migration receipts/runbooks

Defer broad website/product build until cutover stabilizes.

## Completion Criteria

1. `syncrescendence@gmail.com` is primary owner/admin on all required surfaces.
2. Legacy account downgraded to break-glass or removed per policy.
3. All platform trackers show `verified` and `rollback_ready` then `closed`.
4. CC81 cutover receipt published with timestamped evidence links.

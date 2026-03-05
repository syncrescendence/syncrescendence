# CC81 Identity Centralization Program

**Date**: 2026-03-04  
**Status**: active  
**Class**: cutover program

## Objective

Centralize control-plane ownership toward `syncrescendence@gmail.com` without breaking live operations, while preserving a temporary break-glass path from legacy account surfaces currently bound to `truongphillipthanh@icloud.com`.

## Current Runtime Facts (verified this session)

1. Local OpenClaw node pairing for remote `nodes` execution is currently unavailable (`Paired: 0`).
2. Manus API is reachable from CLI with Keychain-backed auth and can create tasks via `POST /v1/tasks`.
3. Local auth surfaces still show legacy account bindings (Claude/gcloud/wrangler all still on the legacy account in current local status snapshot).

## Current Program State

1. Capability analysis from Manus is completed and landed:
   - [RESPONSE-MANUS-cc81-identity-cutover-capability-development.md](/Users/system/syncrescendence/communications/responses/RESPONSE-MANUS-cc81-identity-cutover-capability-development.md)
   - [RESPONSE-MANUS-cc81-identity-cutover-capability-development-raw.md](/Users/system/syncrescendence/communications/responses/RESPONSE-MANUS-cc81-identity-cutover-capability-development-raw.md)
2. Execution runbook is now active:
   - [CC81-IDENTITY-CUTOVER-RUNBOOK-v1.md](/Users/system/syncrescendence/orchestration/state/impl/CC81-IDENTITY-CUTOVER-RUNBOOK-v1.md)
3. Tracker state machine is active:
   - [IDENTITY-CUTOVER-TRACKER-CC81.json](/Users/system/syncrescendence/orchestration/state/IDENTITY-CUTOVER-TRACKER-CC81.json)
4. Psyche remote execution remains blocked pending OpenClaw node pairing.

## Program Law

1. No direct owner/billing mutation without pre-cutover snapshot.
2. No secret values in repo artifacts; pointer-only evidence.
3. One platform at a time; never concurrent owner transfers across critical platforms.
4. Each platform cutover must define rollback owner and rollback time window.
5. Production delivery remains active; cutover windows must be reversible.

## Platform Teleology for Identity Cutover

| Platform | Canonical Role | Target Account Position | Automation Mode |
|---|---|---|---|
| Google account / workspace / cloud | root identity and upstream auth substrate | `syncrescendence@gmail.com` becomes primary owner/admin | hybrid |
| GitHub | code sovereignty and CI control plane | org/repo ownership centralized to target account | hybrid |
| Cloudflare + domain | edge ingress and domain authority | target account is super-admin and billing owner | hybrid |
| Slack | operator bus and office routing | target account is primary owner/admin | agentified |
| Discord | runtime channel surface | target account owns app/bot/server admin | agentified |
| Manus | bounded autonomous backend worker | service account key remains local; tenant ownership mapped to target account | headless |

## Cutover Waves

### Wave 0 — Security Baseline (blocking)

1. Enforce MFA/hardware key policy on `syncrescendence@gmail.com`.
2. Register break-glass recovery path and test recovery before migrations.
3. Capture immutable pre-cutover evidence snapshots for each platform.

### Wave 1 — Authority Transfer (highest risk)

1. GitHub org/repo owner and billing transfer.
2. Cloudflare account and domain ownership/billing transfer.
3. Google cloud/project ownership and IAM rebinding.

### Wave 2 — Runtime Collaboration Surfaces

1. Slack workspace + app owner transfer, token rotation.
2. Discord app/bot/server ownership transfer, token rotation.

### Wave 3 — Exocortex Control Plane

1. Notion/Coda/Confluence/Linear/Jira/ClickUp/Basecamp/Airtable owner/admin rebinding.
2. Token and service principal rotation into target account-controlled vaults.

### Wave 4 — Decommission Legacy Primacy

1. Convert `truongphillipthanh@icloud.com` from owner to backup admin where required.
2. Revoke stale tokens and API keys bound to legacy identity.
3. Publish cutover receipt package.

## Delegation Matrix (Human vs Manus vs Psyche)

| Work Type | Human | Manus | Psyche |
|---|---|---|---|
| Owner/billing changes | required | no | no |
| Browser-heavy preflight checklists | supervise | yes | yes (after node pairing) |
| API discovery and platform-specific migration runbooks | review | yes | partial |
| Token inventory and rotation planning | approve | yes (plan only) | yes (local runtime checks) |
| Local runtime identity audits (OpenClaw/tmux substrate) | supervise | no | yes |
| Bulk evidence packaging and receipts | review | yes | yes |

## Capability Development Dispatches

### Manus (can dispatch now)

1. Generate platform-by-platform migration matrix (automatable vs human-only steps).
2. Produce rollback checklists and pre-cutover snapshot schema.
3. Produce idempotent verification tests for post-cutover ownership assertions.

### Psyche (blocked until node pairing)

1. Establish OpenClaw node pairing from this machine to Mac mini.
2. Add repeatable local runtime audit commands (account bindings, daemon status, token pointers).
3. Build local “pre-cutover runtime readiness” report and return artifact.

## Website Decision (build now or later)

Build only the minimal website layer now if it directly helps cutover:

1. OAuth redirect endpoints
2. health/status page for control-plane visibility
3. canonical docs landing for operational runbooks

Do **not** start full product-site implementation during cutover. It does not reduce identity migration risk.

## Immediate Execution Next Steps

1. Dispatch Manus capability probe for migration automation envelope and rollback recipe.
2. Stage Psyche dispatch packet for node pairing + runtime audit development.
3. Open `IDENTITY-CUTOVER-TRACKER` with per-platform status (`not_started`, `snapshot_done`, `transferred`, `verified`, `rollback_ready`).
4. Perform Wave 0 and require explicit receipt before Wave 1.

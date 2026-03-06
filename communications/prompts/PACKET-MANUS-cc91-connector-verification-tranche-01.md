# PACKET-MANUS-cc91-connector-verification-tranche-01

**Surface**: `manus_api_runtime`  
**Packet type**: `verification_dispatch`  
**Purpose**: verify exocortex connector states for high-fanout hubs and return evidence-structured receipts.

## Context

Canonical connector manifest:

- `/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONNECTOR-MANIFEST-CC91.json`

Receipt template:

- `/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONNECTOR-VERIFICATION-RECEIPT-TEMPLATE-CC91.json`

## Verification Set

Verify these connector IDs:

1. `notion_surface--slack_surface--1`
2. `notion_surface--jira_surface--3`
3. `notion_surface--github_surface--5`
4. `clickup_surface--slack_surface--1`
5. `clickup_surface--github_surface--2`
6. `clickup_surface--jira_surface--8`
7. `perplexity_surface--notion_surface--4`
8. `perplexity_surface--github_surface--7`
9. `perplexity_surface--slack_surface--9`

## Output Requirements

For each connector ID:

1. Determine current state in source integration UI.
2. Return one outcome:
   - `connected`
   - `not_connected`
   - `partial`
   - `blocked`
3. Provide short evidence note and at least one evidence pointer (screenshot or UI path description).

## Constraints

1. Do not reveal secrets, tokens, session cookies, or raw auth material.
2. Do not perform destructive or ownership mutations.
3. If blocked by auth or role, mark `blocked` and explain the exact gate.

## Return Format

Return two artifacts in your response body:

1. Markdown summary titled:
   - `RESPONSE-MANUS-cc91-connector-verification-tranche-01`
2. JSON object with shape:
   - `verification_batch_id`
   - `captured_at`
   - `captured_by`
   - `receipt_scope`
   - `receipts[]`

Use:

- `verification_batch_id`: `cc91-tranche-01`
- `captured_by`: `manus`
- `receipt_scope`: `high_fanout_hubs`

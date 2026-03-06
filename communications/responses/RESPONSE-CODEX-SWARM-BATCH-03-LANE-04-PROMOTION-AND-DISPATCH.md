# Response

**Response ID**: `RSP-20260306-promotion-and-dispatch`
**Surface**: `codex_parallel_session`
**Date received**: `2026-03-06`
**Dispatch packet**: `communications/prompts/PACKET-CODEX-SWARM-BATCH-03-LANE-04-PROMOTION-AND-DISPATCH.md`
**Result state**: `complete`
**Receipt artifacts**:
  - `communications/responses/RESPONSE-CODEX-SWARM-BATCH-03-LANE-04-PROMOTION-AND-DISPATCH.md`

## Returned Content

Derived from:

- [RESPONSE-CODEX-SWARM-BATCH-02-LANE-04-PROMOTION-THRESHOLDS.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-04-PROMOTION-THRESHOLDS.md)
- [COMMUNICATIONS-LAW-v1.md](/Users/system/syncrescendence/orchestration/state/impl/COMMUNICATIONS-LAW-v1.md)
- [communications/README.md](/Users/system/syncrescendence/communications/README.md)

The narrow, implementable recommendation is:

- add one compact constitutional artifact that states the promotion thresholds without repeating the full law stack
- make `communications/dispatches/` a first-class lane for dispatch-event records and routed task receipts
- keep `offices/` as the live root lane
- reject direct `offices/` -> `executive/` filing except through derived executive classes already allowed by law

## 1. Patch-Ready Draft: Compact Promotion-Threshold Artifact

**Recommended target path**: `orchestration/state/impl/PROMOTION-THRESHOLDS-v1.md`

```md
# Promotion Thresholds v1

**Date**: 2026-03-06
**Status**: compact constitutional addendum
**Purpose**: define the minimum lawful thresholds for promoting artifacts from `offices/` into `communications/` and from `communications/` into `executive/`

---

## 1. Core Rule

Artifact movement has two thresholds:

- **lineage threshold**: `offices/` -> `communications/`
- **steering threshold**: `communications/` -> `executive/`

No artifact should skip directly from `offices/` to `executive/`.

---

## 2. Offices -> Communications

Promote an office artifact into `communications/` when any of the following becomes true:

- another office, session, runtime surface, or external actor must read or act on it
- it is the authoritative packet, response, receipt, confirm, handoff, assessment, or dispatch record for a named exchange
- it must survive beyond local queue cleanup as durable lineage or audit evidence
- it is cited outside the originating office as proof of state, completion, failure, or transfer

Keep the artifact in `offices/` when it is still:

- scratch work
- queue residue
- local bookkeeping
- machine/runtime noise
- uncited local notes

---

## 3. Communications -> Executive

Promote a communications artifact into `executive/` only when sovereign steering is required.

Allowed executive classes:

- `briefing`
- `escalation`
- `summit`

Promotion is lawful only when the artifact:

- requests sovereign decision, ratification, reprioritization, or exception handling
- synthesizes cross-lane state for sovereign read-in
- requires synchronized comparative review across multiple lanes or ministries

Do not promote when the artifact is merely:

- informative
- evidentiary
- operationally resolvable under existing authority
- an ordinary prompt, response, receipt, confirm, dispatch record, or log

---

## 4. Dispatch Classification

`communications/dispatches/` exists for communication-event records, not for every outbound prompt.

A dispatch artifact belongs in `communications/dispatches/` when it records one or more of:

- the routed task or packet identifier
- sender and intended receiver
- route or surface used
- dispatch status
- authoritative send, receipt, or retry history

Prompts remain in `communications/prompts/`.
Responses remain in `communications/responses/`.
Chronological operational traces remain in `communications/logs/`.

---

## 5. Forbidden Direct Promotions

The following are unlawful by default:

- `offices/**` filed directly into `executive/**`
- raw office `TASK`, `RESULT`, `RECEIPT`, `CONFIRM`, `ALERT`, or `EXECLOG` artifacts filed directly into `executive/`
- use of `executive/` as a prestige archive for artifacts that do not carry steering burden

If executive attention is required, derive a lawful `briefing`, `escalation`, or `summit` artifact inside `communications/` first, then promote that derivative artifact.

---

## 6. Default Filing Table

| Artifact burden | Default home | Promote when |
|---|---|---|
| office-local work | `offices/` | it crosses a lineage threshold |
| prompt / packet | `communications/prompts/` | it is a live routed communication |
| response | `communications/responses/` | it answers a prompt or packet |
| dispatch record | `communications/dispatches/` | it records routing, receipt, status, or retries |
| log | `communications/logs/` | it is primarily chronological observability |
| sovereign steering derivative | `executive/briefings/`, `executive/escalations/`, or `executive/summits/` | it crosses a steering threshold |

---

## 7. Enforcement Minimum

Validators should enforce at least:

- no direct `offices/` -> `executive/` filing
- no artifact under `executive/` unless classed as `briefing`, `escalation`, or `summit`
- no dispatch record filed as a response or log merely because a dispatch lane is missing
```

## 2. Patch-Ready Draft: `communications/dispatches/README.md`

**Recommended target path**: `communications/dispatches/README.md`

```md
# Dispatches

This lane is the authoritative home for dispatch-event artifacts inside `communications/`.

Use it for:

- dispatch records for routed packets, tasks, and handoffs
- authoritative send / receipt / retry / failure state for a named communication
- routing metadata that must survive beyond local office queues
- compact dispatch ledgers that other offices or validators may cite

Do not use it for:

- prompt bodies; those stay in `communications/prompts/`
- response bodies; those stay in `communications/responses/`
- generic chronology; that stays in `communications/logs/`
- office-local queue residue that has not crossed a lineage threshold

## Filing Rule

Create a dispatch artifact here when the communication event itself needs durable lineage.

Examples:

- a packet was sent to an external surface and needs an auditable send record
- a routed task crossed office boundaries and needs authoritative receipt state
- retries, failures, or route changes must be preserved outside office-local inbox/outbox state

Do not create a dispatch artifact merely because a prompt exists.
Only create one when dispatch metadata is itself part of the durable record.

## Minimum Metadata

Each dispatch artifact should carry at least:

- `artifact_class: dispatch`
- `dispatch_id`
- `related_packet` or `related_artifact`
- `sender_office`
- `target_surface` or `target_office`
- `dispatch_status`
- `dispatched_at`

Recommended additional fields:

- `route`
- `account_surface`
- `attempt`
- `receipt_state`
- `promotion_scope`

## Naming

Recommended filename pattern:

- `DISPATCH-<sender>-<slug>.md`

If the dispatch is tied to an existing packet ID, reuse that ID or slug in the filename and metadata.

## Relationship To Other Lanes

- `prompts/` contains the request content
- `responses/` contains the answer content
- `dispatches/` contains the routing and receipt record
- `logs/` contains broad chronology

One communication may legitimately have artifacts in all four lanes.
The lanes are complementary, not interchangeable.
```

## 3. Recommended Template Metadata Fields

Keep the set minimal enough to adopt quickly.

### 3.1 Office artifacts

Recommended fields:

- `artifact_class`
- `artifact_id`
- `office_id`
- `office_path`
- `date`
- `status`
- `promotion_scope`
- `current_harness`
- `related_dispatch`
- `related_outputs`

Why this set:

- `office_id` and `office_path` preserve stable office identity even if harness binding changes
- `promotion_scope` makes local vs cross-office vs sovereign burden machine-checkable
- `current_harness` keeps mutable runtime assignment in metadata rather than path naming

### 3.2 Communications artifacts

Recommended fields:

- `artifact_class`
- `artifact_id`
- `surface`
- `date`
- `status`
- `lineage_root`
- `dispatch_role`
- `promotion_scope`
- `steering_class`
- `derived_from`
- `related_outputs`

Dispatch-specific additions:

- `dispatch_id`
- `sender_office`
- `target_surface`
- `dispatch_status`
- `dispatched_at`

Recommended enum direction:

- `promotion_scope`: `local`, `cross_office`, `federal`, `sovereign_candidate`
- `steering_class`: `none`, `briefing`, `escalation`, `summit`
- `dispatch_role`: `sender`, `receiver`, `relay`, `observer`

## 4. Minimal Validator Checks

The validator should stay narrow and reject only constitutional violations that matter immediately.

### 4.1 Forbidden direct office -> executive filing

Reject any artifact when both are true:

- path begins with `offices/`
- destination path begins with `executive/`

Error text:

- `office artifacts may not file directly into executive; derive a briefing, escalation, or summit artifact in communications first`

### 4.2 Executive class gate

Reject any artifact under `executive/` unless:

- `artifact_class` is one of `briefing`, `escalation`, `summit`, or
- `steering_class` is one of `briefing`, `escalation`, `summit`

Error text:

- `executive artifacts must declare briefing, escalation, or summit steering class`

### 4.3 Dispatch lane anti-drift check

Reject or warn when a communications artifact appears to be a dispatch record but is filed elsewhere.

Minimal heuristics:

- filename starts with `DISPATCH-` and path is not `communications/dispatches/`
- `artifact_class: dispatch` and path is not `communications/dispatches/`

Error text:

- `dispatch artifacts belong in communications/dispatches unless explicitly historical`

### 4.4 Historical exception

Allow non-canonical placement only when metadata explicitly marks:

- `status: historical`
- or `pedigree_exception: true`

This keeps retrofit and preserved evidence lawful without weakening live filing rules.

## 5. Top Failure Modes If Dispatch Physicalization Is Sloppy

1. `dispatches/` turns into a duplicate prompt lane, so operators file full prompt bodies there and split the same communication across two authoritative homes.
2. `dispatches/` turns into a duplicate log lane, so broad chronology swamps the small set of dispatch records that validators actually need.
3. offices keep storing cross-office receipt state locally because the dispatch lane exists physically but has no clear trigger rule.
4. `responses/` absorbs send, retry, and receipt metadata because teams use "response" to mean "anything that happened after sending."
5. executive artifacts get created directly from office matter because dispatch records are mistaken for escalation artifacts.
6. metadata is too thin to pair dispatches with prompts and responses, producing orphan records that cannot prove what was sent, to whom, or why.
7. the lane gets introduced with too many mandatory subtypes or templates, which raises filing friction and causes continued use of old ad hoc locations.

## Immediate Notes

- The recommended change set is intentionally narrow: one compact law artifact, one dispatch-lane README, and a validator floor.
- The dispatch lane should be about routing lineage, not message-body duplication.
- Stable office identity should remain path-based; mutable harness identity should remain metadata-based.

## Open Ambiguities

- None for the requested first write set. A later batch can decide whether dispatches need a dedicated template file beyond the README.

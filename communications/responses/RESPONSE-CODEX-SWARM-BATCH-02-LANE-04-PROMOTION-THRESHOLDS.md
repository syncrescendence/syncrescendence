# Response

**Response ID**: `RSP-20260306-promotion-thresholds`
**Surface**: `codex_parallel_session`
**Date received**: `2026-03-06`
**Dispatch packet**: `communications/prompts/PACKET-CODEX-SWARM-BATCH-02-LANE-04-PROMOTION-THRESHOLDS.md`
**Result state**: `complete`
**Receipt artifacts**:
  - `communications/responses/RESPONSE-CODEX-SWARM-BATCH-02-LANE-04-PROMOTION-THRESHOLDS.md`

## Returned Content

Derived from:

- [OFFICE-LAW-v1.md](/Users/system/syncrescendence/orchestration/state/impl/OFFICE-LAW-v1.md)
- [OFFICE-ARTIFACT-LAW-v1.md](/Users/system/syncrescendence/orchestration/state/impl/OFFICE-ARTIFACT-LAW-v1.md)
- [COMMUNICATIONS-LAW-v1.md](/Users/system/syncrescendence/orchestration/state/impl/COMMUNICATIONS-LAW-v1.md)
- [EXECUTIVE-LANE-LAW-v1.md](/Users/system/syncrescendence/orchestration/state/impl/EXECUTIVE-LANE-LAW-v1.md)
- [RESPONSE-CODEX-SWARM-LANE-05-SOVEREIGN-AND-OFFICES.md](/Users/system/syncrescendence/communications/responses/RESPONSE-CODEX-SWARM-LANE-05-SOVEREIGN-AND-OFFICES.md)

The minimum lawful contract is:

- office-local artifacts stay in `offices/` unless they cross a lineage threshold
- communications artifacts stay in `communications/` unless they cross a steering threshold
- executive receives only classified steering artifacts: `briefing`, `escalation`, or `summit`
- no raw office artifact should promote directly into `executive/`
- the root lane should remain `offices/`, not revert to `agents/`
- canonical office directories should stay stable by office identity, not mutable harness binding

## 1. Promotion Thresholds

### 1.1 Agent-local -> communications

| Test | If yes | If no |
|---|---|---|
| Another office, session, or external surface must act from this artifact | promote to `communications/` as a prompt, response, handoff, assessment, log, or dispatch record | keep in the originating office |
| The artifact is the authoritative receipt, result, or confirm for a named dispatch/packet and must survive beyond local queue cleanup | promote to `communications/` | keep local queue residue only |
| The artifact is cited outside the office as proof of completion, failure, state, or handoff continuity | promote to `communications/` | keep in `offices/` |
| The artifact is only scratch work, cache, journal, internal queue bookkeeping, or raw mechanical trace | do not promote | keep in `scratchpad/`, `memory/`, `inbox/`, `outbox/`, or `platform/logs/` |
| The artifact now carries sovereign-steering burden | first shape it as a classified communication artifact, then evaluate `communications -> executive`; do not file directly into `executive/` from an office | keep below executive |

### 1.2 Communications -> executive

| Test | If yes | If no |
|---|---|---|
| The artifact requests or records sovereign decision, reprioritization, ratification, legitimacy change, or exception handling across lanes/offices | promote to `executive/escalations/` | keep in `communications/` |
| The artifact is a cross-lane state synthesis for sovereign read-in or durable state-of-the-union | promote to `executive/briefings/` | keep in `communications/` |
| The artifact requires synchronized comparative review across multiple lanes or ministries | promote to `executive/summits/` | keep in `communications/` |
| The artifact is informative, evidentiary, or operational but fully resolvable under existing law, program, and office authority | do not promote | keep in `communications/` |
| The artifact is an unclassified prompt, response, receipt, result, confirm, or raw log | do not promote | executive may cite it, but should not absorb it as an executive artifact |

## 2. Explicit Non-Promotion Rules

### Must remain local

- unfinished `TASK` envelopes that have not crossed an office boundary
- office-internal `RECEIPT` and `CONFIRM` artifacts used only to manage one office's queue
- draft or low-signal `RESULT` artifacts that are not yet cited outside the office
- `memory/journal`, `memory/cache`, `memory/sync`, and `scratchpad/` matter
- `platform/contracts/`, `platform/templates/`, and `platform/logs/` by default
- `EXECLOG` unless another lane needs it as evidence
- low-signal `ALERT` artifacts about local machine, provider, or harness noise

### Must remain communications-only

- prompts, responses, handoffs, assessments, and logs that preserve lineage but do not seek sovereign steering
- cross-office receipts, confirms, and results that close loops under existing authority
- incident reports that require coordination or audit but not executive reprioritization or ratification
- supporting evidence for an executive decision; only the derived `briefing`, `escalation`, or `summit` belongs in `executive/`

## 3. Naming Recommendation

### Root lane

Recommendation:

- keep the physical root lane as `offices/`
- do not revert the live shell root to `agents/`

Reason:

- `offices/` names the burden class: local working domains under federal law
- `agents/` names the predecessor pattern and remains valuable as pedigree, but it is overloaded by software-agent taxonomy and would blur role, harness, and ontology again

### Office directory names

Recommendation:

- do not make canonical office directories harness-named
- keep canonical directories stable by office identity
- record harness, account, provider, and machine binding in metadata or office-local runtime docs instead

Reason:

- harness binding is mutable
- lineage needs a stable path anchor
- one office may move between harnesses without becoming a different office
- one harness may host more than one office over time

Net contract:

- physical path = stable office identity
- harness binding = metadata
- avatarization = conceptual and contractual, not the primary reason to rename physical directories

If a later rename is ever desired, the safer target is stable office-role IDs, not harness names.

## 4. Example Classification

| Class | Default home | Promote to communications when | Promote to executive when |
|---|---|---|---|
| `TASK` | office `outbox/dispatches/` or `inbox/pending/` | it is actually dispatched across an office or external-surface boundary and requires a durable reply path | never directly |
| `RECEIPT` | office `outbox/receipts/` | it is the authoritative acknowledgment of a routed dispatch or claim another actor must audit | never directly |
| `RESULT` | office `outbox/results/` or receiving office queue | it is the substantive answer to a named packet/dispatch or is cited outside the office | only indirectly, through a derived briefing or escalation that changes steering |
| `CONFIRM` | receiving office `inbox/done/` or `inbox/active/` | it is the durable closure record for a cross-office handoff or dispatch | never directly |
| `ALERT` | office `inbox/active/` or `platform/` context | another office, program, runtime, or federal operator must respond | the alert is unresolved locally and requires sovereign decision, reprioritization, or legitimacy judgment |
| `BRIEFING` | office `inbox/pending/` or local orientation context | it is routed orientation or synthesis for another office but does not ask for sovereign steering | it is sovereign-facing, cross-lane, or state-of-the-union in burden |
| `EXECLOG` | office `platform/logs/` | only as evidence attachment or extracted log record when lineage or audit requires it | never directly; executive may cite derived findings, not raw logs |

## 5. Top Hidden-Authority Failure Modes If This Stays Vague

1. Office outboxes become shadow communications lanes because receipts, results, and confirms never get promoted.
2. `executive/` becomes a prestige inbox for anything "important," collapsing steering law into generic significance.
3. The same office acquires parallel identities across avatar names, harness names, and historical `agents/*` lineage, which forks memory and legitimacy by path.
4. Raw `EXECLOG` or terse `ALERT` artifacts begin substituting for receipts, results, and executive briefs simply because they landed in a high-status folder.
5. Communications-only incident matter is silently treated as sovereign decision material because no one can tell when escalation is actually required.
6. Reverting to `agents/` without a stricter naming contract reopens the older confusion between inhabited office, runtime harness, and software-agent taxonomy.

## 6. Recommended Repo Deltas

1. Add a first-class `communications/dispatches/` lane so promoted `TASK` and routed `RECEIPT` artifacts have a lawful federal home instead of drifting into `responses/` or `logs/`.
2. Add minimal metadata to office and communications templates: `office_id`, `current_harness`, `artifact_class`, `promotion_scope`, and `steering_class`.
3. Add a validator/operator that rejects direct office -> executive filing unless the artifact is explicitly classed as `briefing`, `escalation`, or `summit`.
4. Add an office metadata contract that keeps harness/account binding observable without forcing path renames when runtime assignment changes.

## Status

Complete. The threshold contract is intentionally narrow: lineage moves artifacts from `offices/` to `communications/`; steering moves a classified subset from `communications/` to `executive/`; path names should remain stable by office identity rather than by mutable harness.

# Communications Law v1

**Date**: 2026-03-02  
**Status**: constitutional redesign package  
**Purpose**: define the legal classes, lineage requirements, storage law, and enforcement model for prompts, responses, handoffs, logs, retros, and derived outputs

---

## 0. Why This Exists

The repo's most persistent structural pain point is not execution anymore.
It is communications law.

Too many things currently blur together:

- prompt vs packet
- response vs report
- handoff vs summary
- assessment vs output
- log vs runtime state
- inbox vs lineage lane

This document formalizes that layer.

---

## 1. Core Doctrine

Communications artifacts are **not** a miscellaneous residue of work.

They are the explicit lineage layer between:

- law
- intentions
- execution
- outputs
- memory
- ontology

If this layer is ambiguous, the whole shell becomes harder to audit and compact.

---

## 2. Primary Communications Classes

## 2.1 Prompt / Packet

**Definition**
- outbound artifact requesting work, sensing, verification, execution, or synthesis

**Examples**
- Oracle packet
- Perplexity verification packet
- adjudicator prompt
- Cowork relay job packet

**Rules**
- must have a stable identifier
- must name the intended surface
- should have an expected response or failure state

## 2.2 Response

**Definition**
- inbound artifact produced by the target surface in direct answer to a prompt or packet

**Rules**
- should remain linked to its originating prompt
- should not be stored as a generic orphan
- if imported historically without a prompt, it must be marked as such

## 2.3 Dispatch Record

**Definition**
- metadata around a communication event

**Examples**
- who sent it
- when
- by which route
- using which account/surface

This may live as frontmatter, metadata sidecar, or event record.

## 2.4 Handoff

**Definition**
- explicit state transfer artifact between sessions or agents

**Rules**
- must be lossless enough to continue work
- must contain current state, remaining work, traps, and open questions
- is not the same as a generic recap

## 2.5 Log

**Definition**
- chronological record of events, attempts, statuses, or progress

**Rules**
- logs are primarily for chronology and observability
- they do not replace playbooks or lineage

## 2.6 Retrospective / Kaizen

**Definition**
- reflective artifact that extracts improvements from repeated work

**Rules**
- may cite logs, prompts, responses, and failures
- should eventually compact into playbooks, regulation, or automation

## 2.7 Assessment

**Definition**
- focused evaluative artifact about a particular run, response, design, or experiment

**Rules**
- should point back to concrete lineage
- should not replace underlying prompt/response artifacts

## 2.8 Output / Deliverable

**Definition**
- the product generated from communications and execution

**Examples**
- schematic design
- implementation brief
- sitrep
- architectural package

---

## 3. Why the Current Shell Drifts

Because communications artifacts currently live across:

- `engine/`
- `-INBOX/`
- `agents/.../handoffs/`
- `ascertescence/`
- `00-ORCHESTRATION/state/impl/`

the shell has weak filing law for:

- what is a prompt,
- what is a response,
- what is a report,
- what is a handoff,
- and which lanes are live vs transitional.

The result is not lack of intelligence.
It is lack of constitutional filing.

---

## 4. Storage Law

The next shell should eventually separate these physically:

- `communications/prompts/`
- `communications/responses/`
- `communications/dispatches/`
- `communications/handoffs/`
- `communications/logs/`
- `communications/retros/`
- `communications/assessments/`

Derived outputs may remain in output/program/implementation lanes, but should point back into communications lineage.

---

## 5. Pairing and Lineage Rules

## 5.1 Prompt-response pairing

Default rule:

- one prompt -> one primary response

Allowed variants:

- one prompt -> multiple responses when deliberately triangulated
- one prompt -> no response, but only if marked:
  - abandoned
  - superseded
  - failed-to-dispatch

## 5.2 Response-only imports

Historical imports without prompts are allowed only if marked:

- `historical-orphan`
- `imported-without-prompt`

and queued for future linkage if possible.

## 5.3 Handoff lineage

Handoffs must link to:

- prior handoff when applicable
- active branch or workstream
- major relevant outputs or current state docs

## 5.4 Assessment lineage

Assessments should cite:

- the prompt(s)
- the response(s)
- the output(s)
- the conclusion(s)

---

## 6. Naming and Metadata

The system should converge toward stable communication IDs, not filename intuition alone.

At minimum, communications artifacts should eventually carry:

- `artifact_class`
- `surface`
- `slug`
- `date`
- `lineage_root`
- `related_outputs`

Additional recommended fields:

- `dispatch_role`
- `account_surface`
- `status`
- `derived_from`

---

## 7. Inbox Law

An inbox is allowed as a transient intake lane.

An inbox is **not** a permanent filing system.

So:

- `-INBOX` can exist as transitional intake
- it cannot remain the long-term authoritative home of responses once communications law is live

Deprecation should therefore mean:

1. intake may still happen there temporarily
2. the authoritative lineage lane exists elsewhere
3. validators eventually block new permanent filing there

This resolves the current contradiction of "`-INBOX` is sunsetted" while it is still actively used.

---

## 8. Logs Are Not Everything

This has to be explicit.

Logs are one class only.

Do not treat:

- prompts,
- responses,
- handoffs,
- assessments,
- implementation briefs,
- state snapshots

as if they are all "logs."

That flattening is one of the main causes of shell cruft.

---

## 9. Compaction Rules

Communications artifacts compact in several lawful directions:

- repeated successful prompts -> playbook patterns
- repeated failures -> anti-patterns / QA rules
- repeated handoff structure -> handoff protocol
- repeated logs -> automation / observability regulation
- repeated assessments -> design doctrine

Original lineage remains in provenance or historical lanes.

---

## 10. Edge Cases

## 10.1 One report synthesizes many prompts and responses

The report is still an output or assessment.
The prompts and responses remain separate lineage artifacts.

## 10.2 A prompt contains embedded metadata and dispatch notes

That does not make it a handoff.
Its primary class still governs.

## 10.3 Real-time chat that is not yet saved

Until it lands as an artifact, it is not durable system state.

## 10.4 Imported historical folders with mixed artifact classes

Allowed in provenance lanes, but should be marked mixed and not treated as properly filed live communications.

---

## 11. Enforcement Model

The next validator layer should eventually enforce:

- no new `PROMPT-*` files outside approved communications lanes
- no new `RESPONSE-*` files outside approved communications lanes
- no handoffs outside approved handoff lanes
- no reports masquerading as responses
- no permanent filing in legacy inboxes once migration reaches enforcement stage

Quarantine is preferable to silent acceptance.

---

## 12. Net Rule

If a file exists because one surface asked another surface for work, returned work, transferred state, recorded chronology, extracted learning, or produced an evaluative synthesis, the shell must make that function explicit.

If the operator cannot tell which of those it is, communications law is still missing.

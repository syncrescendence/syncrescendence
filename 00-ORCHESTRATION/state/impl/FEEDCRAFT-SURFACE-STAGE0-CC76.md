# Feedcraft Surface Stage 0 — CC76

**Date**: 2026-03-02  
**Purpose**: define the first tooling-facing boundary for Feedcraft so it can emerge on top of the exocortex taxonomy rather than bypass it

---

## What Feedcraft Is

Feedcraft is not a single tool.

It is the higher-order subsystem responsible for:

- signal intake
- feed conditioning
- recommendation-environment understanding
- platform-specific routing and publication logic

At the tooling level, Feedcraft should be treated as a **composite exocortex subsystem** built over already-separated surfaces, especially:

- [youtube_feed_surface](/Users/system/syncrescendence/00-ORCHESTRATION/state/impl/EXOCORTEX-SURFACE-TAXONOMY-CC75.md)
- `oracle_web_surface`
- `perplexity_web_surface`
- `notebooklm_surface`
- `google_model_surface`
- `xai_model_surface`

Feedcraft is therefore not a new authority surface.
It is a layer that conditions and routes signals between already-governed surfaces.

---

## Constitutional Constraints

Feedcraft must not:

- become a second canon
- dump raw transcripts into the repo by default
- bypass the event ledger
- store opaque platform state without provenance
- collapse multiple platforms into a single undifferentiated “content” blob

Feedcraft should:

- stay pointer-first on intake
- emit structured events when it qualifies or routes signals
- preserve platform specificity
- remain auditable through repo artifacts and ontology projection

---

## Stage 0 Surface Model

At Stage 0, Feedcraft should be understood as four bounded functions:

## 1. Intake

What entered the system?

Examples:

- YouTube channel or video metadata
- Substack post pointer
- X/Twitter list item or account pointer
- manually flagged source candidate

Correct durable record:

- pointer
- summary
- typed routing metadata

## 2. Qualification

Why does this signal matter?

Examples:

- priority band
- abstraction level
- modality
- temporal urgency
- signal fidelity

Correct durable record:

- typed record
- summary markdown when useful

## 3. Routing

Where should the signal go next?

Examples:

- Acumen reconnaissance queue
- NotebookLM synthesis set
- corpus extraction queue
- publication or output backlog

Correct durable record:

- typed routing decision
- pointer to downstream artifact or queue

## 4. Publication Conditioning

How should an already-qualified idea be shaped for a platform?

Examples:

- YouTube long-form exposition
- Substack essay
- X/Twitter thread
- internal intelligence brief

Correct durable record:

- summary + typed publication descriptor
- not the full drafted output by default

---

## Immediate Dependencies

Feedcraft Stage 0 depends on surfaces that now exist:

- `youtube_feed_surface` for media/feed intake
- `google_model_surface` and `xai_model_surface` for bounded model execution
- `notebooklm_surface` for source-bounded synthesis
- web packetized surfaces for strategic or verification passes

It also depends on the account/auth matrix:

- [EXOCORTEX-ACCOUNT-IDENTITY-MATRIX-CC76.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/impl/EXOCORTEX-ACCOUNT-IDENTITY-MATRIX-CC76.md)

Without those layers, Feedcraft would collapse into vague “content ops.”

---

## Proposed Stage 0 Event Classes

These are the first event classes Feedcraft will likely need once code lands:

- `feedcraft_intake_record`
- `feedcraft_signal_qualification`
- `feedcraft_route_decision`
- `feedcraft_publication_conditioning`

These should remain distinct from:

- raw platform events
- corpus extraction events
- final publication artifacts

---

## First Tooling Moves After Stage 0

The first concrete engineering moves should be:

1. a feed qualification schema
2. a YouTube-first intake bridge extension
3. a routing target vocabulary tied to current queues
4. a platform grammar descriptor for YouTube, X/Twitter, and Substack

That sequence respects the current repo architecture:

`surface event -> qualification -> routing -> downstream execution`

Not:

`platform dump -> implicit judgment -> hidden routing`

---

## Why This Is Enough For Now

The goal of Stage 0 is not to build Feedcraft in full.

The goal is to ensure that when Feedcraft begins to materialize, it does so:

- on top of the existing exocortex grammar
- with platform-specific rigor
- without creating another authority surface
- with event and ontology compatibility from the start

# Tool Stack Addendum — Post-CC75

**Date**: 2026-03-02  
**Purpose**: capture the questions, clarifications, and strategic additions raised after `TOOL-STACK-CONSOLIDATED-SITREP-CC75.md`

---

## Why This Exists

After the consolidated SITREP, the Sovereign raised three important follow-on lines:

1. what else may still be missing from the tooling plan
2. how Google AI / GCP / YouTube API / xAI API fit into the architecture
3. how the exocortex line should expand to include later surfaces like NotebookLM, Claude Cowork, Feedcraft, and the IIC stack

This addendum records those answers explicitly so they do not remain only in thread memory.

---

## Questions Answered After CC75

## 1. Comprehensive Documentation

The tooling lane was documented in:

- [TOOL-STACK-CONSOLIDATED-SITREP-CC75.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/impl/TOOL-STACK-CONSOLIDATED-SITREP-CC75.md)

That document captured:

- config architecture implementation
- Ajna rewiring
- event reconciliation
- boundary contract
- ontology/domain cutover
- Manus integration
- GitHub verification surface
- exocortex bridges
- Mac mini tmux stage 1 revival

## 2. Web/CLI Gap

The correct answer is:

**do not force web-native surfaces to masquerade as local agents.**

Instead, treat Oracle, Perplexity, NotebookLM, Claude Cowork, and similar surfaces as governed **web exocortex surfaces**.

Their participation model should be:

`repo dispatch packet -> web response artifact -> exocortex event -> reconciliation -> ontology`

That is the right form of two-way communication.

It preserves:

- repo authority
- durable provenance
- typed downstream projection
- agent-to-agent communication through artifacts rather than hidden threads

## 3. Agents To Each Other

The correct model is not unconstrained direct chat.

It is:

- dispatch packets
- returned artifacts
- event ledger
- ontology projection

So “agent communication” should remain:

- artifact-mediated
- provenance-preserving
- replayable
- repo-grounded

Not:

- hidden continuous conversation across many surfaces
- local state known only to one runtime

---

## Additional Surfaces Explicitly Added To The Plan

The Sovereign clarified that the tool map must explicitly include the broader Google stack, YouTube API, and xAI API.

Those belong in the plan.

## 1. Google Surface Family

This should not be modeled as one monolithic “Google” tool.

It is a family of surfaces:

- `google_model_surface`
  - Gemini API
  - Google AI Studio
  - Vertex AI model access
- `notebooklm_surface`
  - notebook-bounded source synthesis
  - research digestion
- `gcloud_resource`
  - projects
  - credentials
  - service configuration
- `youtube_feed_surface`
  - subscriptions
  - channel graph
  - video metadata
  - publication/analytics later

These have different contracts and should not be collapsed into one exocortex class.

## 2. YouTube API

The Sovereign noted that YouTube API will likely be central to Feedcraft.

That is directionally correct.

Why:

- it exposes feed-level signal structure
- it enables channel/subscription topology
- it provides metadata useful for qualification and routing
- it can become the intake backbone for a Feedcraft subsystem

The correct default posture is still pointer-first:

- fetch metadata
- emit structured pointer/summary events
- selectively persist downstream artifacts when justified

Not:

- indiscriminate transcript dumps
- raw bulk ingestion by default

## 3. xAI API

The Sovereign also noted xAI API belongs in the plan.

That is correct, but it must be separated from Grok web Oracle.

These are two distinct surfaces:

- `oracle_web_surface`
  - Grok web / Oracle prompt line
  - strategic hypersensing
  - thesis + industry synthesis
- `xai_model_surface`
  - direct API access
  - programmatic model execution
  - possibly later integrated into local or external execution flows

They should not be conflated.

## 4. NotebookLM

NotebookLM should be treated as:

- an exocortex synthesis surface
- not a canonical authority

Proper role:

- source-bounded synthesis
- notebook-mediated retrieval
- domain digestion

Proper return path:

- repo-authored notebook packet or source set
- saved return artifact
- exocortex event
- ontology pointer or summary record

## 5. Claude Cowork

Claude Cowork should be treated as:

- a collaborative external execution/synthesis surface
- not a constitutional law source

Proper pattern:

- repo dispatch packet
- returned artifact
- event reconciliation

## 6. Feedcraft

Feedcraft belongs in the same realm because it is about exocortex shaping and feed physics.

It should be understood as a specialized exocortex subsystem concerned with:

- signal intake
- feed conditioning
- recommendation environments
- platform-specific routing and publication logic

## 7. IIC

IIC is upstream governance over these surfaces.

It should eventually specify:

- which surfaces belong to which IIC
- what each IIC is allowed to ingest
- what each IIC is allowed to output
- how cross-IIC synthesis occurs

This means:

**Feedcraft and IIC are not separate from the exocortex line.**  
They are higher-order organization of the exocortex.

---

## What Was Identified As Still Missing / Easy To Overlook

The likely omissions in the tooling plan are no longer “forgotten tools.”

They are mostly missing **governance and control layers** around the growing exocortex.

## 1. Web-Surface Packetization

Oracle, Perplexity, NotebookLM, Claude Cowork, and future web-native surfaces still need formal packet standards:

- outbound dispatch packet
- inbound response artifact contract
- event emission contract
- ontology projection rule

Without that, they remain semi-manual rituals.

## 2. Account / Identity Matrix

Still under-specified:

- which account owns which surface
- which IIC it belongs to
- which auth substrate it uses
- which harness is allowed to operate it

This becomes more important as Google, xAI, Feedcraft, and IIC surfaces multiply.

## 3. Secrets Lifecycle

Improved, but still not fully formalized:

- issuance
- storage
- hydration
- rotation
- revocation
- audit trail

## 4. Observability / Incident Layer

There are status snapshots and event projection, but not yet a mature:

- what broke
- where
- when
- how to recover

layer for all surfaces.

## 5. Idempotency / Replay / Schema Evolution

This already surfaced once through the reconciler race.

As more surfaces join, the system needs continuing discipline around:

- dedupe
- replay
- schema migration
- safe re-projection

## 6. Rate / Cost Governance

This is easy to miss while adding capabilities.

Needed eventually:

- throughput awareness
- cost class per surface
- rate-limit risk map
- budget view across Claude, Gemini/Google, xAI, Manus, Perplexity, Grok

## 7. Evaluation Harness

Not just “is it integrated,” but:

- does Oracle ground correctly
- does Perplexity verify correctly
- does NotebookLM synthesize usefully
- do external bridges preserve provenance

Infrastructure truth exists more strongly than quality truth.

## 8. Data Rights / Copyright / Privacy Boundaries

Especially important for:

- YouTube
- NotebookLM
- Feedcraft
- publication-facing exocortex surfaces

The capture policy must continue to distinguish:

- pointer-only
- summary
- typed record
- full persistence

## 9. Stage 2 tmux Policy

Stage 1 is now complete enough.

The next decision is structural:

- prepared shells only
- controlled startup wrappers
- or real agent autostart

This should be a deliberate policy choice.

## 10. Shared Capacity / Account Collision Testing

The earlier “Account 3” style empirical question remains in principle:

- how do shared substrates behave under real concurrent load?

That still deserves eventual measurement rather than assumption.

---

## Recommended Surface Taxonomy Expansion

The following surface classes should now be explicitly recognized in the exocortex map:

1. `oracle_web_surface`
2. `perplexity_web_surface`
3. `notebooklm_surface`
4. `claude_cowork_surface`
5. `google_model_surface`
6. `gcloud_resource`
7. `youtube_feed_surface`
8. `xai_model_surface`

For each of these, the system should eventually define:

- dispatch packet shape
- response artifact shape
- allowed durable capture mode
- ontology projection behavior
- owning account / IIC / harness

---

## Recommended Next Moves

If the plan is to keep expanding cleanly, the next engineering sequence should be:

1. formalize Oracle dispatch packet template
2. formalize Perplexity verification packet template
3. add landing/bridge wrappers for Oracle and Perplexity responses
4. define the account / identity / IIC ownership matrix
5. define the expanded exocortex surface taxonomy above
6. only then onboard NotebookLM and Claude Cowork into the same governed loop
7. after that, begin Feedcraft and IIC operationalization on top of the now-stable exocortex grammar

---

## Preserved Principle

The mistake to avoid is building every new external surface as a special-case ritual.

The governing pattern should remain:

- one constitutional repo
- one boundary contract
- one event/reconciliation line
- one ontology projection layer
- many bounded execution and sensing surfaces

That is how the constellation grows without fragmenting.

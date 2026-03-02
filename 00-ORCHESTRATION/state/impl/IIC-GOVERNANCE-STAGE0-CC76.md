# IIC Governance Stage 0 — CC76

**Date**: 2026-03-02  
**Purpose**: define the first tooling-facing role of the IIC layer so future surface ownership can become explicit without prematurely operationalizing the full IIC constellation

---

## What The IIC Layer Is

The IIC layer is not a raw tool surface.

It is the governance overlay that eventually decides:

- which surfaces belong to which intelligence modality
- what each modality is allowed to ingest
- what each modality is allowed to output
- how cross-IIC handoffs occur

At the tooling level, the IIC layer should therefore be modeled as:

- an ownership and routing framework
- not as a browser, API, or CLI surface in itself

---

## Stage 0 Goal

Stage 0 does not attempt to operationalize full five-IIC deployment.

It only establishes the minimum discipline needed now:

1. surface ownership must be legible
2. surface purpose must be bounded
3. future IIC affinity must have a place to land

This is enough to prevent surface sprawl before the constellation is fully activated.

---

## Current Practical Position

Right now, the repo has:

- a surface taxonomy
- an account/auth matrix
- a live agent runtime split
- packetized and bridged exocortex surfaces

What it does not yet have is a formal per-surface IIC mapping.

That is correct for the current phase.

The IIC layer should come **after**:

- surface separation
- capture policy
- account/auth clarity
- event/reconciliation discipline

Those prerequisites now largely exist.

---

## Stage 0 Mapping Rule

Every exocortex surface should eventually declare:

- current operating harness
- current auth substrate
- likely IIC affinity
- whether that affinity is authoritative or provisional

For now, only the first two are mandatory.
The IIC affinity can remain provisional until the actual IIC rollout begins.

---

## Provisional IIC Affinities

These are directional, not yet binding:

| Surface | Likely Primary IIC Affinity | Why |
|---|---|---|
| `oracle_web_surface` | Transcendence / Coherence | strategic synthesis and meta-pattern sensing |
| `perplexity_web_surface` | Acumen | verification and factual disambiguation |
| `notebooklm_surface` | Coherence / Mastery | bounded synthesis and corpus digestion |
| `claude_cowork_surface` | Efficacy / Coherence | collaborative execution and parallel implementation |
| `youtube_feed_surface` | Acumen | reconnaissance and signal intake |
| `google_model_surface` | Efficacy / Technology | direct model execution and tooling leverage |
| `xai_model_surface` | Acumen / Technology | programmatic sensing and model-side execution |
| `github_issue_pr_surface` | Efficacy | coordination, validation, operational closure |
| `manus_workflow_surface` | Efficacy | backend execution |
| `cloudflare_dns_domain_surface` | Efficacy / Technology | infrastructure and deployment control |

These affinities should not be treated as constitutional law yet.
They are scaffolding for future explicit IIC governance.

---

## First Real Deliverables For The IIC Layer

When the IIC line begins real implementation, the first deliverables should be:

1. per-surface `iic_affinity` field in the taxonomy
2. per-IIC allowed-surface lists
3. per-IIC ingestion/output rules
4. cross-IIC handoff descriptors

Only after those exist should account provisioning and operational choreography expand aggressively.

---

## Why This Matters

Without this stage, the exocortex will grow faster than the intentional structure meant to guide it.

With this stage, future IIC work can attach cleanly to:

- the surface taxonomy
- the account/auth matrix
- the event ledger
- the ontology projection layer

That is the correct order of operations.

# CC73 Oracle Convergence Brief

**Date**: 2026-03-02
**Lane**: Tooling Stack / Oracle Line
**Purpose**: Freeze the current convergence state so the next Oracle round targets only unresolved boundary questions.

## What Is Now Implemented

1. **Ajna is operational in OpenClaw**
   - Claude Sonnet 4.5 primary
   - browser relay attached and authenticated
   - generated OpenClaw workspace surface is under the injection limit

2. **Repo truth and runtime truth have a first reconciliation loop**
   - Ajna emits structured event files
   - Commander-side reconciliation ingests those events into repo memory/state
   - OpenClaw runtime snapshot and memory synthesis land back into the repo

3. **Config architecture is real**
   - rendered harness outputs
   - machine-aware manifest
   - validation and reconciliation targets in `Makefile`

4. **Ontology v1 now exists as a conservative projection layer**
   - SQLite schema at `ontology_v1_schema.sql`
   - projector/API at `ontology_v1.py`
   - current endpoints: `/health`, `/entities`, `/entities/{id}`, `/events`, `/ingest/event`, `/project/repo`
   - projection source is repo-normalized state, not raw runtime or direct SaaS

5. **OpenClaw LaunchAgent is healthy again**
   - gateway now runs under launchd with `gateway run --port 18789`
   - `openclaw gateway status` returns `RPC probe: ok`

## What Oracle Already Settled Enough

These points are strong enough to treat as operating law:

- **Projection must be unidirectional**
  Ajna/runtime/exocortex emit raw state; Commander normalizes; ontology is downstream projection only.

- **Repo remains constitutional authority**
  Runtime is ephemeral execution surface.
  Ontology is typed query surface.
  Exocortex is external action surface.

- **Memory must stay layered and selective**
  No unbounded mirroring.
  No second repo inside ontology.
  No direct SaaS-to-ontology bypass.

## What Is Still Unresolved

These are the remaining Oracle-grade questions:

1. **Root vs dotfile vs runtime boundary policy**
   - What must live at repo root?
   - What belongs in tool-local dotfiles only?
   - What should remain runtime-only and never be committed?

2. **Obsidian role**
   - interface over repo truth
   - mirror/cache
   - or selective authoring layer

3. **GitHub role**
   - remote transport
   - public mirror
   - automation trigger surface
   - what, if anything, is authoritative there

4. **Exocortex capture policy**
   - which SaaS state becomes markdown summaries
   - which becomes typed ontology records
   - which remains pointers only
   - which should never be copied at all

5. **Domain role after ontology v1**
   - API only
   - operator dashboard
   - docs/status surface
   - staged sequence among them

## Recommended Next Oracle Question

Do **not** ask Oracle to redesign Ajna, OpenClaw, or the config scaffold again.

Ask instead:

**Given that Ajna is operational, reconciliation exists, and ontology v1 is now live as a projection layer, what is the correct boundary contract among repo root, tool-local dotfiles, Obsidian, GitHub, exocortex SaaS surfaces, and the domain-facing ontology API so Syncrescendence avoids parallel realities while remaining usable day to day?**

## Operational Implication

Commander can continue the rest of tooling stack execution:
- Slack/Discord triage
- Manus
- `gcloud` / `wrangler`
- ontology hookup behind the domain

The Oracle line should now stay on **boundary policy and capture policy**, not on re-litigating already-implemented plumbing.

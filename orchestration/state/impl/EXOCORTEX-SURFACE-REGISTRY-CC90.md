# Exocortex Surface Registry — CC90

**Date**: 2026-03-05  
**Status**: active  
**Class**: canonical ownership and ontology binding snapshot

## Purpose

This is the first complete exocortex registry aligned to the canonical identity:

- `syncrescendence@gmail.com`

and canonical workspace namespace:

- `syncrescendence`

It expands prior CC75/CC76 surface notes into a full inventory with auth-dependency edges so ontology projection can treat exocortex as a graph instead of a flat list.

## Source Snapshot

- [EXOCORTEX-SURFACE-REGISTRY-CC90.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-SURFACE-REGISTRY-CC90.json)

## Included Scope

1. 37 exocortex surfaces
2. 2 auth dependencies:
   - `github_surface -> supabase_surface` (Sign in with GitHub)
   - `slack_surface -> incident_surface` (Sign in with Slack)
3. canonical repo path:
   - `https://github.com/syncrescendence/syncrescendence`

## Ontology Binding Contract

Each surface row declares:

1. `slug`
2. `service`
3. `class`
4. `access_model`
5. `owner_identity`
6. `workspace_namespace`
7. `status`
8. `ontology_entity_id`

This enables deterministic projection to ontology entities/relations without embedding secrets or mutable session artifacts.

## Relationship to Prior Artifacts

1. CC75 taxonomy remains useful as the early policy seed:
   - [EXOCORTEX-SURFACE-TAXONOMY-CC75.md](/Users/system/syncrescendence/orchestration/state/impl/EXOCORTEX-SURFACE-TAXONOMY-CC75.md)
2. CC76 identity matrix remains useful as the original framing:
   - [EXOCORTEX-ACCOUNT-IDENTITY-MATRIX-CC76.md](/Users/system/syncrescendence/orchestration/state/impl/EXOCORTEX-ACCOUNT-IDENTITY-MATRIX-CC76.md)
3. CC90 registry is the live canonical expansion for full exocortex inventory.

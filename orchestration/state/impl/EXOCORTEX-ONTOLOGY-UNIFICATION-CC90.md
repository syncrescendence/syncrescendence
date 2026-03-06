# Exocortex Ontology Unification — CC90

**Date**: 2026-03-05  
**Status**: active  
**Class**: implementation runbook

## Objective

Bind the complete exocortex inventory to ontology projection as typed, queryable state.

## Inputs

1. [EXOCORTEX-SURFACE-REGISTRY-CC90.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-SURFACE-REGISTRY-CC90.json)
2. [EXOCORTEX-CAPTURE-POLICY.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CAPTURE-POLICY.json)
3. [exocortex_surface_registry_bridge.py](/Users/system/syncrescendence/operators/exocortex/exocortex_surface_registry_bridge.py)
4. [ontology_v1.py](/Users/system/syncrescendence/operators/ontology/ontology_v1.py)

## Execution

1. emit exocortex registry event and reconcile:

```bash
make -C /Users/system/syncrescendence exocortex-sync-surface-registry
```

2. project repo state into ontology store:

```bash
make -C /Users/system/syncrescendence ontology-project-repo
```

## Expected Result

1. registry snapshot appears as `ExocortexRegistry` entity in ontology DB
2. event ledger includes `exocortex_surface_registry_snapshot`
3. auth dependency edges are preserved in payload for downstream graph use

## Boundary Rules

1. no credentials/tokens in registry payload
2. only typed metadata lands in ontology
3. ownership claims should be updated through registry snapshots, not ad hoc notes

# Exocortex Ontology Unification — CC90

**Date**: 2026-03-05  
**Status**: active  
**Class**: implementation runbook

## Objective

Bind the complete exocortex inventory to ontology projection as typed, queryable state.

## Inputs

1. [EXOCORTEX-SURFACE-REGISTRY-CC90.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-SURFACE-REGISTRY-CC90.json)
2. [EXOCORTEX-TELEOLOGY-REGISTRY-CC90.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-TELEOLOGY-REGISTRY-CC90.json)
3. [EXOCORTEX-CONNECTOR-MANIFEST-CC91.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONNECTOR-MANIFEST-CC91.json)
4. [EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CONTROL-PLANE-STATUS-CC91.json)
5. [EXOCORTEX-CAPTURE-POLICY.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CAPTURE-POLICY.json)
6. [exocortex_surface_registry_bridge.py](/Users/system/syncrescendence/operators/exocortex/exocortex_surface_registry_bridge.py)
7. [exocortex_connector_manifest_bridge.py](/Users/system/syncrescendence/operators/exocortex/exocortex_connector_manifest_bridge.py)
8. [ontology_v1.py](/Users/system/syncrescendence/operators/ontology/ontology_v1.py)

## Execution

1. emit exocortex registry event and reconcile:

```bash
make -C /Users/system/syncrescendence exocortex-sync-surface-registry
```

2. project repo state into ontology store:

```bash
make -C /Users/system/syncrescendence ontology-project-repo
```

3. import/audit/sync connector graph and re-project ontology:

```bash
make -C /Users/system/syncrescendence exocortex-control-plane-run GUIDE=/Users/system/Desktop/guide.md
```

## Expected Result

1. registry snapshot appears as `ExocortexRegistry` entity in ontology DB
2. teleology snapshot appears as `ExocortexTeleology` entity in ontology DB
3. connector manifest snapshot appears as `ExocortexConnectorManifest` entity in ontology DB
4. control-plane status snapshot appears as `ExocortexControlPlaneStatus` entity in ontology DB
5. event ledger includes `exocortex_surface_registry_snapshot`, `exocortex_connector_manifest_snapshot`, and `exocortex_control_plane_status_snapshot`
6. auth dependency edges and connector topology are preserved in payload for downstream graph use

## Boundary Rules

1. no credentials/tokens in registry payload
2. only typed metadata lands in ontology
3. ownership claims should be updated through registry snapshots, not ad hoc notes

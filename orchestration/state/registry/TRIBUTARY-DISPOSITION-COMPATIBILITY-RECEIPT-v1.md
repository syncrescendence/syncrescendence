# TRIBUTARY-DISPOSITION-COMPATIBILITY-RECEIPT-v1

```json
{
  "receipt_id": "TRIBUTARY-DISPOSITION-COMPATIBILITY-RECEIPT-v1",
  "receipt_type": "ratification-compatibility",
  "label": "Bind the live tributary v1 proof rows to ratification-pointer authority during the compatibility window",
  "timestamp_utc": "2026-03-09T22:39:53Z",
  "actor": "codex_parallel_session",
  "effective_date": "2026-03-09",
  "governing_artifact": {
    "ratification_pointer": "ratification-pointer-rollout/v1",
    "ratified_by_artifact_path": "/Users/system/syncrescendence/orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md",
    "ratified_by_artifact_id": "RATIFICATION-POINTER-ROLLOUT-v1",
    "ratified_at": "2026-03-09"
  },
  "governed_family": {
    "schema_path": "orchestration/state/registry/tributary-disposition-schema-v1.md",
    "registry_path": "orchestration/state/registry/tributary-disposition-registry.csv",
    "ledger_path": "orchestration/state/registry/tributary-disposition-ledger.jsonl",
    "baseline_report_path": "orchestration/state/TRIBUTARY-DISPOSITION-VALIDATION-REPORT.md"
  },
  "proof_baseline": {
    "status": "PASS",
    "rows": 10,
    "ledger_events": 50
  },
  "unbound_rows_status": "informative_only",
  "scope_statement": "Any legacy v1 candidate absent from row_bindings remains informative_only during the compatibility window.",
  "row_bindings": [
    {
      "candidate_id": "tdc-artifact-protocol-old-0001",
      "authority_status": "authority_bound",
      "ratification_pointer": "ratification-pointer-rollout/v1",
      "ratified_by_artifact_path": "/Users/system/syncrescendence/orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md",
      "ratified_by_artifact_id": "RATIFICATION-POINTER-ROLLOUT-v1",
      "ratified_at": "2026-03-09",
      "record_state": "verified",
      "source_tributary": "syncrescendence_old",
      "source_path": "01-CANON/CANON-00011-ARTIFACT_PROTOCOL-cosmos.md"
    },
    {
      "candidate_id": "tdc-artifact-protocol-neo-0002",
      "authority_status": "authority_bound",
      "ratification_pointer": "ratification-pointer-rollout/v1",
      "ratified_by_artifact_path": "/Users/system/syncrescendence/orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md",
      "ratified_by_artifact_id": "RATIFICATION-POINTER-ROLLOUT-v1",
      "ratified_at": "2026-03-09",
      "record_state": "verified",
      "source_tributary": "syncrescendence_pre_schematic_design",
      "source_path": "neocanon/CANON-1003-ARTIFACT_PROTOCOL.md"
    },
    {
      "candidate_id": "tdc-memory-architecture-old-0003",
      "authority_status": "authority_bound",
      "ratification_pointer": "ratification-pointer-rollout/v1",
      "ratified_by_artifact_path": "/Users/system/syncrescendence/orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md",
      "ratified_by_artifact_id": "RATIFICATION-POINTER-ROLLOUT-v1",
      "ratified_at": "2026-03-09",
      "record_state": "verified",
      "source_tributary": "syncrescendence_old",
      "source_path": "01-CANON/CANON-25000-MEMORY_ARCH-lattice.md"
    },
    {
      "candidate_id": "tdc-memory-architecture-neo-0004",
      "authority_status": "authority_bound",
      "ratification_pointer": "ratification-pointer-rollout/v1",
      "ratified_by_artifact_path": "/Users/system/syncrescendence/orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md",
      "ratified_by_artifact_id": "RATIFICATION-POINTER-ROLLOUT-v1",
      "ratified_at": "2026-03-09",
      "record_state": "verified",
      "source_tributary": "syncrescendence_pre_schematic_design",
      "source_path": "neocanon/CANON-3004-MEMORY_ARCHITECTURE.md"
    },
    {
      "candidate_id": "tdc-context-transition-old-0005",
      "authority_status": "authority_bound",
      "ratification_pointer": "ratification-pointer-rollout/v1",
      "ratified_by_artifact_path": "/Users/system/syncrescendence/orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md",
      "ratified_by_artifact_id": "RATIFICATION-POINTER-ROLLOUT-v1",
      "ratified_at": "2026-03-09",
      "record_state": "verified",
      "source_tributary": "syncrescendence_old",
      "source_path": "01-CANON/CANON-25100-CONTEXT_TRANS-lattice.md"
    },
    {
      "candidate_id": "tdc-context-transition-neo-0006",
      "authority_status": "authority_bound",
      "ratification_pointer": "ratification-pointer-rollout/v1",
      "ratified_by_artifact_path": "/Users/system/syncrescendence/orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md",
      "ratified_by_artifact_id": "RATIFICATION-POINTER-ROLLOUT-v1",
      "ratified_at": "2026-03-09",
      "record_state": "verified",
      "source_tributary": "syncrescendence_pre_schematic_design",
      "source_path": "neocanon/CANON-3005-CONTEXT_TRANSITION.md"
    },
    {
      "candidate_id": "tdc-research-protocols-old-0007",
      "authority_status": "authority_bound",
      "ratification_pointer": "ratification-pointer-rollout/v1",
      "ratified_by_artifact_path": "/Users/system/syncrescendence/orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md",
      "ratified_by_artifact_id": "RATIFICATION-POINTER-ROLLOUT-v1",
      "ratified_at": "2026-03-09",
      "record_state": "verified",
      "source_tributary": "syncrescendence_old",
      "source_path": "01-CANON/CANON-30330-RESEARCH_PROTOCOLS-asteroid-TECH_STACK-comet-INTELLIGENCE.md"
    },
    {
      "candidate_id": "tdc-research-protocols-neo-0008",
      "authority_status": "authority_bound",
      "ratification_pointer": "ratification-pointer-rollout/v1",
      "ratified_by_artifact_path": "/Users/system/syncrescendence/orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md",
      "ratified_by_artifact_id": "RATIFICATION-POINTER-ROLLOUT-v1",
      "ratified_at": "2026-03-09",
      "record_state": "verified",
      "source_tributary": "syncrescendence_pre_schematic_design",
      "source_path": "neocanon/CANON-3006-RESEARCH_PROTOCOLS.md"
    },
    {
      "candidate_id": "tdc-lineage-old-0009",
      "authority_status": "authority_bound",
      "ratification_pointer": "ratification-pointer-rollout/v1",
      "ratified_by_artifact_path": "/Users/system/syncrescendence/orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md",
      "ratified_by_artifact_id": "RATIFICATION-POINTER-ROLLOUT-v1",
      "ratified_at": "2026-03-09",
      "record_state": "verified",
      "source_tributary": "syncrescendence_old",
      "source_path": "01-CANON/CANON-00002-LINEAGE-cosmos.md"
    },
    {
      "candidate_id": "tdc-lineage-neo-0010",
      "authority_status": "authority_bound",
      "ratification_pointer": "ratification-pointer-rollout/v1",
      "ratified_by_artifact_path": "/Users/system/syncrescendence/orchestration/state/impl/RATIFICATION-POINTER-ROLLOUT-v1.md",
      "ratified_by_artifact_id": "RATIFICATION-POINTER-ROLLOUT-v1",
      "ratified_at": "2026-03-09",
      "record_state": "verified",
      "source_tributary": "syncrescendence_pre_schematic_design",
      "source_path": "neocanon/CANON-2009-INTELLECTUAL_LINEAGE.md"
    }
  ]
}
```

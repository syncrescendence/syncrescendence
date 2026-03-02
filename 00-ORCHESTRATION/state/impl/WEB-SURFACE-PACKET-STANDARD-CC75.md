# Web Surface Packet Standard — CC75

**Date**: 2026-03-02  
**Purpose**: define the first formal packet and landing conventions for web-native exocortex surfaces that do not operate as local CLI agents

---

## Principle

Web surfaces do not become constitutional authority and do not become pseudo-local agents.

They participate through a governed loop:

`repo dispatch packet -> web response artifact -> exocortex event -> reconciliation -> ontology`

This preserves:

- repo authority
- durable provenance
- agent-to-agent communication through artifacts
- typed downstream projection

---

## Packet Classes Introduced Here

## 1. Oracle Dispatch Packet

**Surface**: `oracle_web_surface`  
**Role**: hypersensing, thesis formation, strategic synthesis  
**Repo home**: `engine/PACKET-ORACLE-*.md`

Required sections:

- objective
- state summary
- anchor links
- required output contract
- return path
- bridge command

Default return path:

- `-INBOX/commander/00-INBOX0/RESPONSE-ORACLE-<slug>.md`

## 2. Perplexity Verification Packet

**Surface**: `perplexity_web_surface`  
**Role**: external verification, citation-backed validation, disproof/counterexample search  
**Repo home**: `engine/PACKET-PERPLEXITY-*.md`

Required sections:

- claim or question to verify
- why the verification matters
- acceptable source classes
- required citation contract
- return path
- bridge command

Default return path:

- `-INBOX/commander/00-INBOX0/RESPONSE-PERPLEXITY-<slug>.md`

---

## Landing Convention

When a response returns from Oracle or Perplexity:

1. save the response artifact into the repo
2. bridge the response through the matching wrapper
3. reconcile into the event ledger
4. optionally project into ontology

Wrapper scripts:

- [oracle_response_bridge.py](/Users/system/syncrescendence/oracle_response_bridge.py)
- [perplexity_response_bridge.py](/Users/system/syncrescendence/perplexity_response_bridge.py)

These wrappers emit:

- `surface = exocortex`
- `artifact_class = repo_markdown_change`
- `durable_capture = summary_and_typed_record`

The response markdown remains the durable human-readable artifact.
The emitted event provides the machine-readable bridge into memory and ontology.

---

## Packet Generation Helpers

Generation helpers exist for the two initial packet classes:

- [stage_oracle_packet.py](/Users/system/syncrescendence/stage_oracle_packet.py)
- [stage_perplexity_packet.py](/Users/system/syncrescendence/stage_perplexity_packet.py)

These create repo-native dispatch packets with:

- deterministic file naming
- standard headers
- declared return path
- declared response-bridge command

---

## Invariants

- packet is outbound authority
- returned markdown is inbound evidence
- bridge event is machine-readable normalization
- ontology remains projection, not direct source
- other agents consume the returned artifact through repo or ontology, not hidden web session state

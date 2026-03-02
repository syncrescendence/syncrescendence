# Cowork Relay v1

This directory is the designated relay folder for the first CLI↔web bridge prototype.

It is intentionally simple:

- one file per job
- Cowork grounded to this folder
- Claude in Chrome performs the web interaction
- Cowork writes the returned artifact back here
- local scripts reconcile the result into repo truth

See:

- [COWORK-FOLDER-INSTRUCTIONS.md](/Users/system/syncrescendence/00-ORCHESTRATION/relay/cowork-v1/COWORK-FOLDER-INSTRUCTIONS.md)
- [JOB-SCHEMA.md](/Users/system/syncrescendence/00-ORCHESTRATION/relay/cowork-v1/JOB-SCHEMA.md)
- [HAZEL-RULES.md](/Users/system/syncrescendence/00-ORCHESTRATION/relay/cowork-v1/HAZEL-RULES.md)
- [CC76-CLI-WEB-GAP-FOLLOWUP-ASSESSMENT.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/impl/CC76-CLI-WEB-GAP-FOLLOWUP-ASSESSMENT.md)

Runtime queue folders live under:

- `jobs/inbox/`
- `jobs/running/`
- `jobs/completed/`
- `jobs/failed/`
- `artifacts/outgoing/`

These runtime files are intentionally gitignored by a local ignore file in this directory.

Hazel is the recommended edge-trigger layer for v1:

- Cowork writes the response artifact and status file
- Hazel notices the status file
- Hazel runs the finalization script
- repo/event/ontology are updated automatically

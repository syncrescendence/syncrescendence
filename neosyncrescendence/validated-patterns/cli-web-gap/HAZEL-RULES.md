# Hazel Rules — Cowork Relay v1

Hazel should be used here as an edge-trigger layer, not as the intelligence layer.

Its job is simple:

- notice when Cowork has produced a result
- run the correct finalization script
- optionally move desktop-side drops into the relay inbox

---

## Recommended Rule 1

**Folder watched**

- `00-ORCHESTRATION/relay/cowork-v1/artifacts/outgoing/`

**Match**

- file extension is `.json`
- filename ends with `.status.json`

**Run shell script**

```bash
/usr/bin/env python3 /Users/system/syncrescendence/CLI-WEB-GAP/scripts/finalize_cowork_relay_job.py --status-file "$1" --project-ontology
```

**What this does**

- reads the Cowork-written status file
- infers job id, result, note, and optional citation count
- copies the staged response artifact into the repo target path
- runs the correct bridge script
- reconciles into the event ledger and ontology

This is the main Hazel integration point.

---

## Recommended Rule 2

**Folder watched**

- `~/Desktop/main/`

**Match**

- filename starts with `PACKET-`
- file extension is `.md`

**Suggested action**

- do nothing automatically unless you want a desktop-to-relay intake path later

Rationale:

- packets are usually deliberate relay artifacts
- moving them automatically can make active browser relay awkward

So this rule is optional and low priority.

---

## Recommended Rule 3

**Folder watched**

- `00-ORCHESTRATION/relay/cowork-v1/jobs/inbox/`

**Match**

- any `.json` file

**Suggested action**

- optional notification only

Rationale:

- Cowork still needs to actually process the job
- Hazel should not move active jobs around

---

## Cowork Status File Contract

For Hazel automation to work cleanly, Cowork should write a status file shaped like:

```json
{
  "job_id": "perplexity-20260302-193000-example",
  "result": "success",
  "note": "Perplexity response captured and saved.",
  "citation_count": 8
}
```

Required fields:

- `job_id`
- `result`
- `note`

Optional fields:

- `citation_count`

The matching response markdown must already exist at the job's `response_staging_path`.

---

## Why Hazel Helps Here

Hazel reduces the amount of manual shell work after Cowork finishes.

It does **not** replace:

- the job file
- the browser execution
- the bridge scripts
- the repo/event/ontology contract

It simply turns:

`artifact appears -> finalize it`

into an automatic edge behavior.

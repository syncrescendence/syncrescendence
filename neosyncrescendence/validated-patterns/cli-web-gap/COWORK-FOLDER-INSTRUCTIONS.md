# Cowork Folder Instructions — Relay v1

Use this folder as a deterministic relay, not as a second source of truth.

## Mission

Process one job file at a time from `jobs/inbox/`.

Each job asks you to use the browser to complete a specific web task, then save the returned artifact into the exact output path described in the job file.

## Rules

1. Treat the job JSON as authority for the task.
2. Move the job file from `jobs/inbox/` to `jobs/running/` when you begin.
3. Read the `packet_staging_path` file referenced in the job.
4. Use Claude in Chrome only for the web interaction required by the job.
5. Save the returned result as markdown to the exact `response_staging_path` from the job.
6. Do not overwrite unrelated files.
7. Do not invent a new file location.
8. Do not leave the result only in browser state.
9. After saving the artifact, write the status JSON to the exact `status_path`.
10. If the job cannot be completed, move it to `jobs/failed/` and write a failure status JSON.

## Output Contract

For successful jobs:

- preserve citations and source links when present
- keep markdown readable
- do not add extra conversational framing unless the packet explicitly asks for it

For failed jobs:

- write a short machine-readable failure note
- say what blocked completion

## Status JSON Contract

Write a JSON object with:

- `job_id`
- `result`
- `note`

Optionally include:

- `citation_count`

Example:

```json
{
  "job_id": "perplexity-20260302-193000-example",
  "result": "success",
  "note": "Perplexity response captured and saved.",
  "citation_count": 8
}
```

Hazel can watch this file and trigger finalization automatically.

## State Discipline

- one job per file
- one response artifact per job
- one status file per job
- packet and attachments are already staged locally inside this folder

Do not use a shared document for multiple jobs.

## Safety

- ask for confirmation before any irreversible or sensitive web action
- read-only retrieval and synthesis tasks are preferred
- if a site blocks the workflow or upload behavior is unclear, fail cleanly instead of improvising

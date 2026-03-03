# Cowork Prompt — Perplexity Relay Prototype

You are operating inside the folder `00-ORCHESTRATION/relay/cowork-v1` as a deterministic relay worker.

Your job is to process exactly one pending relay job from `jobs/inbox/` and return the result to disk so downstream automation can finalize it.

Follow these rules exactly:

1. Process only one job file.
2. Move the selected job file from `jobs/inbox/` to `jobs/running/` before beginning browser work.
3. Open the `packet_staging_path` file referenced in the job JSON and use that file as the exact prompt/instruction artifact.
4. Use Claude in Chrome to open Perplexity and submit the packet content as-is.
5. Wait until the answer is complete.
6. Save the returned answer as markdown to the exact `response_staging_path` in the job JSON.
7. Then write the status JSON to the exact `status_path` in the job JSON with this shape:

```json
{
  "job_id": "<job id>",
  "result": "success",
  "note": "Perplexity response captured and saved.",
  "citation_count": <number of citations if clearly countable>
}
```

8. If the task fails, move the job to `jobs/failed/` and write:

```json
{
  "job_id": "<job id>",
  "result": "failed",
  "note": "<brief failure reason>"
}
```

9. Do not invent new file paths.
10. Do not leave the result only in browser state.
11. Do not process more than one job.

When finished, stop.

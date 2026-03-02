# Cowork Relay v1 Job Schema

Each job is a single JSON file in `jobs/inbox/`.

Required fields:

- `id`
- `created_at`
- `surface`
- `job_type`
- `title`
- `packet`
- `response_artifact`
- `response_staging_path`
- `status_path`
- `summary_for_bridge`

Optional fields:

- `attachments`
- `instructions`
- `metadata`

## Surface Values

- `perplexity`
- `oracle`
- `notebooklm`
- `claude_cowork`

## Suggested Job Types

- `query_response`
- `verification_query`
- `upload_then_query`
- `notebook_synthesis`
- `followup_query`

## Example

```json
{
  "id": "perplexity-20260302-193000-example",
  "created_at": "2026-03-02T19:30:00Z",
  "surface": "perplexity",
  "job_type": "verification_query",
  "title": "Perplexity relay smoke test",
  "packet": "engine/PACKET-PERPLEXITY-cc76-cli-web-gap-followup.md",
  "response_artifact": "-INBOX/commander/00-INBOX0/RESPONSE-PERPLEXITY-cc76-cli-web-gap-followup.md",
  "response_staging_path": "00-ORCHESTRATION/relay/cowork-v1/artifacts/outgoing/RESPONSE-PERPLEXITY-cc76-cli-web-gap-followup.md",
  "status_path": "00-ORCHESTRATION/relay/cowork-v1/artifacts/outgoing/perplexity-20260302-193000-example.status.json",
  "summary_for_bridge": "Perplexity follow-up landed for current official Cowork and Claude in Chrome capabilities.",
  "attachments": [],
  "instructions": [
    "Open Perplexity in the browser and submit the packet content as-is.",
    "When the answer completes, save the response markdown into response_staging_path."
  ],
  "metadata": {
    "priority": "prototype"
  }
}
```

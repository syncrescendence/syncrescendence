# Ajna Event Schema

Ajna emits structured events into the OpenClaw workspace landing zone:

`/Users/system/.openclaw/workspace/events/inbox/`

Commander ingests those events into repo state with:

`make reconcile-ajna-events`

## Required Fields

```json
{
  "id": "ajna-20260302-021500-browser-auth-check",
  "emitted_at": "2026-03-02T02:15:00Z",
  "source": "ajna",
  "type": "browser_auth_state",
  "summary": "Checked browser auth state for Cloudflare and GitHub.",
  "capture_level": "summary",
  "payload": {}
}
```

## Optional Fields

- `repo_paths`: affected repo files
- `ontology_entities`: identifiers to project later
- `payload`: compact structured details, never secrets

## Capture Levels

- `pointer`: external pointer only, minimal durable trace
- `summary`: durable operational summary worth committing to repo memory
- `full`: reserved for exceptional cases; still no secrets or raw message dumps

## Forbidden Content

- tokens
- passwords
- cookies
- full Slack/Discord message bodies
- raw browser session dumps
- unbounded SaaS payloads

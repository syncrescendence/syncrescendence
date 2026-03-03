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
  "surface": "browser",
  "artifact_class": "browser_action",
  "type": "browser_auth_state",
  "summary": "Checked browser auth state for Cloudflare and GitHub.",
  "capture_level": "summary",
  "durable_capture": "summary_markdown",
  "payload": {}
}
```

## Optional Fields

- `repo_paths`: affected repo files
- `ontology_entities`: identifiers to project later
- `payload`: compact structured details, never secrets

## Surface Values

- `repo`
- `runtime`
- `obsidian`
- `github`
- `exocortex`
- `browser`

## Artifact Classes

- `repo_markdown_change`
- `runtime_state`
- `obsidian_repo_markdown`
- `obsidian_workspace_state`
- `slack_discord_comms`
- `github_issue_pr`
- `linear_issue_project`
- `cloudflare_dns_domain`
- `gcloud_resource`
- `wrangler_worker`
- `manus_workflow`
- `browser_action`

## Common Event Types

- `obsidian_note_create`
- `obsidian_note_append`
- `browser_auth_state`
- `browser_state_check`

## Capture Levels

- `pointer`: external pointer only, minimal durable trace
- `summary`: durable operational summary worth committing to repo memory
- `full`: reserved for exceptional cases; still no secrets or raw message dumps

## Durable Capture Modes

- `none`: do not persist beyond runtime
- `pointer`: persist only an external reference / minimal trace
- `summary_markdown`: distill into repo markdown only
- `typed_record`: project into ontology/API only
- `summary_and_typed_record`: both repo summary and ontology projection

## Boundary Rules

- `surface` identifies where the event originated; it is not the final authority.
- `artifact_class` identifies which exocortex or repo policy applies.
- `durable_capture` must match the policy in `00-ORCHESTRATION/state/EXOCORTEX-CAPTURE-POLICY.json`.
- Obsidian-authored durable markdown belongs in tracked repo directories, never `.obsidian/`.
- Communication events must never include full third-party bodies even if they are important.

## Forbidden Content

- tokens
- passwords
- cookies
- full Slack/Discord message bodies
- raw browser session dumps
- unbounded SaaS payloads

# PACKET-MANUS-cc81-phase0-phase1-implementation

You are implementing capability development for Syncrescendence identity cutover.

## Mission

Produce executable Phase 0 and Phase 1 artifacts only:

- Phase 0: security/readiness gates
- Phase 1: pre-cutover snapshot capture design

## Scope constraints

1. No destructive actions.
2. No tenant logins.
3. No secrets.
4. Evidence-backed output only.
5. Return markdown that can be dropped directly into runbooks.

## Required output

1. `PHASE0-GATE-CHECKLIST`
   - exact checks, pass/fail criteria, and who executes (`human`, `commander`, `psyche`, `manus`).
2. `PHASE1-SNAPSHOT-SCHEMA`
   - normalized schema for pre-cutover evidence artifacts across platforms.
3. `PLATFORM-SNAPSHOT-COMMAND-RECIPES`
   - where API exists, include non-destructive command examples to collect baseline state.
4. `EVIDENCE-RECEIPT-TEMPLATE`
   - machine-readable JSON template for storing snapshot receipts.
5. `RISKS-IN-PHASE0-1`
   - top failure modes and mitigations.

## Platforms

- GitHub
- Cloudflare
- Google Workspace
- GCP
- Slack
- Discord
- Notion
- Coda
- Jira
- Confluence
- Linear
- ClickUp
- Basecamp
- Airtable

## Success

Deliver a practical, implementation-ready output for CC81 Phase 0 and 1, with no hidden assumptions.

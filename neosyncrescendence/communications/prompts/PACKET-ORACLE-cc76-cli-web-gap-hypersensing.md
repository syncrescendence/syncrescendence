# Oracle Dispatch Packet — CLI/Web Gap Hypersensing

- Surface: `oracle_web_surface`
- Packet type: `oracle_dispatch`
- Created: `2026-03-02T18:45:00Z`
- Slug: `cc76-cli-web-gap-hypersensing`
- Return artifact: `-INBOX/commander/00-INBOX0/RESPONSE-ORACLE-cc76-cli-web-gap-hypersensing.md`

## Objective

Hypersense the real architecture for closing the CLI↔web gap across paid subscription surfaces without defaulting to separate metered API costs, while preserving Syncrescendence's current boundary contract:

`repo dispatch -> surface execution -> returned artifact -> event reconciliation -> ontology projection`

The core question is:

How do we turn flat-rate or subscription web tools into callable workers from a single dispatch point without creating second authorities, while still leaving room for APIs, MCP, and browser automation where they are genuinely better?

## Current State Summary

The repo now has:

- explicit exocortex surface taxonomy
- packetized web surfaces
- checkpoint bridges for API/backend surfaces
- live event ledger and ontology projection
- local/domain ontology serving
- account/auth matrix for current surfaces
- stage-0 Feedcraft and IIC governance docs

What is still unresolved is the true bridge between CLI and web surfaces.

We are specifically trying to reason about:

- whether the cleanest bridge is browser adapters
- whether those adapters should be wrapped in MCP
- whether Cowork should become the main dispatch cockpit
- whether the website/domain should be the control plane
- whether filesystem job queues are the right relay primitive
- when APIs are worth paying for versus when they should be avoided
- how to leverage already-paid subscription tools from a singular dispatch point

The working intuition is:

- repo/event/ontology should remain truth plane
- some other plane should become dispatch/control
- browser-driven subscription workers may be the lowest-cost execution plane for Grok, Perplexity, NotebookLM, Claude Cowork, and similar surfaces

## Anchor Links

### Repo / GitHub Anchors

- [Surface taxonomy](https://github.com/truongphillipthanh/syncrescendence/blob/main/00-ORCHESTRATION/state/impl/EXOCORTEX-SURFACE-TAXONOMY-CC75.md)
- [Packet standard](https://github.com/truongphillipthanh/syncrescendence/blob/main/00-ORCHESTRATION/state/impl/WEB-SURFACE-PACKET-STANDARD-CC75.md)
- [Account and identity matrix](https://github.com/truongphillipthanh/syncrescendence/blob/main/00-ORCHESTRATION/state/impl/EXOCORTEX-ACCOUNT-IDENTITY-MATRIX-CC76.md)
- [Feedcraft stage 0](https://github.com/truongphillipthanh/syncrescendence/blob/main/00-ORCHESTRATION/state/impl/FEEDCRAFT-SURFACE-STAGE0-CC76.md)
- [IIC governance stage 0](https://github.com/truongphillipthanh/syncrescendence/blob/main/00-ORCHESTRATION/state/impl/IIC-GOVERNANCE-STAGE0-CC76.md)
- [Live local surface status](https://github.com/truongphillipthanh/syncrescendence/blob/main/00-ORCHESTRATION/state/LOCAL-SURFACE-STATUS.md)

### Official Current-World Anchors

- [Anthropic Claude Code MCP docs](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [Anthropic MCP overview](https://docs.anthropic.com/en/docs/mcp)
- [Anthropic computer use tool docs](https://docs.anthropic.com/en/docs/build-with-claude/computer-use)
- [Perplexity MCP server docs](https://docs.perplexity.ai/docs/getting-started/integrations/mcp-server)
- [Perplexity Agent API quickstart](https://docs.perplexity.ai/docs/agentic-research/quickstart)
- [Perplexity Search API quickstart](https://docs.perplexity.ai/docs/search/quickstart)
- [Perplexity pricing](https://docs.perplexity.ai/docs/getting-started/pricing)
- [xAI release notes](https://docs.x.ai/docs/release-notes)
- [xAI overview](https://docs.x.ai/docs/overview)
- [xAI Google Drive integration for Grok](https://docs.x.ai/docs/grok-business/apps/google-drive)
- [NotebookLM help center](https://support.google.com/notebooklm/answer/16070070)
- [NotebookLM mobile app help](https://support.google.com/notebooklm/answer/16296687)
- [Google Workspace privacy note for NotebookLM](https://support.google.com/a/answer/15706919)

## Questions To Answer

### 1. Architecture

Given the repo state and current official product landscape, what is the best actual architecture for closing the CLI↔web gap?

Compare these candidate forms directly:

- human relay with repo packets only
- local file-queue plus browser worker
- browser adapter wrapped in MCP
- website/domain as control plane
- Cowork as dispatch cockpit over repo truth
- API-first for selected surfaces only

State clearly:

- which should be primary
- which should be fallback
- which should be avoided

### 2. Subscription Worker Fabric

We want to leverage already-paid subscription surfaces from a single dispatch point without defaulting to separate API charges.

What is the best architecture for turning web subscription tools into callable workers?

Examples:

- Grok / Oracle web
- Perplexity web
- NotebookLM
- Claude Cowork

Tell us whether the right primitive is:

- browser profile + adapter + queue file
- browser profile + adapter + MCP wrapper
- browser profile + website-issued jobs
- something else used by strong operators in practice

### 3. Industry Patterns

Who is actually solving this well?

Not generic “agentic browsers,” but concrete patterns from practitioners, startups, open-source builders, or infrastructure teams who are:

- orchestrating paid web subscriptions from one control point
- bridging browser-only SaaS into CLI/agent systems
- using filesystem queues, MCP, browser workers, or hybrid control planes
- minimizing metered API exposure

We want the real design patterns, not just the names of products.

### 4. Cowork / Website / MCP Roles

Clarify the right role of each:

- Cowork as dispatch interface
- website/domain as control plane
- MCP as tool abstraction layer
- browser adapter as execution layer
- repo/event/ontology as truth layer

What stack shape is most coherent?

### 5. Recent Product Changes We May Be Missing

Are there any recent feature releases, product updates, or shifts in official capabilities that materially change the answer here?

Especially:

- Perplexity MCP server / Agent API / Search API
- Claude Code remote MCP and Claude-as-MCP-server
- Anthropic computer use
- xAI tools, collections, connectors, Grok web/API overlap
- NotebookLM current input/output and enterprise capabilities

### 6. File Attachments And Richer Jobs

We also need an answer for richer jobs:

- plain query/response
- query with attachments
- upload sources then query
- create notebook/workspace then synthesize

What is the right abstraction:

- one adapter per site with multiple job types?
- one job queue with per-job action schemas?
- something better?

## Required Output Contract

- Lead with your own thesis, not consensus recap.
- Ground the answer in both the repo anchors and the official current-world anchors above.
- Distinguish clearly between verified current facts and your architectural inference.
- If there are strong industry precedents, name the pattern and why it matters.
- Return a recommended stack diagram in words: dispatch plane, execution plane, return plane, truth plane.
- Return a phased recommendation: what to do now, next, and later.
- Explicitly answer whether browser adapters plus subscription workers are the right primary path.
- Explicitly answer whether Cowork should be the main dispatch cockpit.

## Return Instructions

- Save or relay the response back into `-INBOX/commander/00-INBOX0/RESPONSE-ORACLE-cc76-cli-web-gap-hypersensing.md`
- Do not let the response remain only in web-session state.
- Keep concrete links, dates, and source attributions where relevant.

## Bridge Command

```bash
python3 CLI-WEB-GAP/scripts/oracle_response_bridge.py --dispatch engine/PACKET-ORACLE-cc76-cli-web-gap-hypersensing.md --response -INBOX/commander/00-INBOX0/RESPONSE-ORACLE-cc76-cli-web-gap-hypersensing.md --summary "Oracle hypersensing landed for the CLI-web gap and subscription-worker architecture." --project-ontology
```

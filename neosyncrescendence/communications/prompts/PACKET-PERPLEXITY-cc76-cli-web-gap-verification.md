# Augur Verification Packet — CLI/Web Gap Capability Check

- Surface: `perplexity_web_surface`
- Packet type: `perplexity_verification`
- Created: `2026-03-02T18:45:00Z`
- Slug: `cc76-cli-web-gap-verification`
- Return artifact: `-INBOX/commander/00-INBOX0/RESPONSE-PERPLEXITY-cc76-cli-web-gap-verification.md`

## Claim Or Question To Verify

We need an official-fact verification pass on the current product landscape for closing the CLI↔web gap.

The architectural direction being considered is:

- repo remains source of truth
- web-native subscription surfaces are driven through browser adapters or MCP-connected relays
- APIs are used selectively where they are structurally superior
- goal is to maximize already-paid subscription surfaces and minimize unnecessary metered API usage

We need to know which current official capabilities materially support or weaken that direction.

## Why This Verification Matters

Tooling choices for the next phase depend on current official access models, not assumptions.

We specifically need to avoid stale beliefs about:

- whether MCP now closes some of the gap directly
- whether Perplexity, Claude, xAI, or NotebookLM have released capabilities that change the relay design
- whether some surfaces that looked browser-only are now API- or MCP-addressable
- whether some surfaces still require browser automation because no stable official path exists

## Verification Questions

### 1. Perplexity

Using official Perplexity sources:

- Does Perplexity now have an official MCP server?
- What tools does it expose?
- Does that materially reduce the need for browser automation for research/query use cases?
- Are Perplexity API paths separately metered from subscription use?

### 2. Anthropic / Claude

Using official Anthropic sources:

- Does Claude Code now support remote MCP over HTTP/SSE and OAuth-authenticated remote servers?
- Can Claude Code itself be used as an MCP server?
- Is Anthropic’s computer-use capability still API/beta oriented rather than a subscription-surface substitute?
- Do these capabilities materially support a dispatch architecture where Cowork or Claude-side tools act as a cockpit over repo truth?

### 3. xAI / Grok

Using official xAI sources:

- What current xAI API capabilities are relevant to the CLI↔web gap?
- Do release notes indicate tools, collections, connectors, or integrations that reduce reliance on brittle browser automation?
- Is there any current official mechanism that makes Grok web and xAI API meaningfully converge?

### 4. NotebookLM

Using official Google sources:

- Is NotebookLM still effectively browser/mobile-first for ordinary users?
- Is there any current official public API or equivalent developer access path?
- What are the current source input methods and constraints?
- Does Google Workspace positioning of NotebookLM change how it should be modeled inside the exocortex stack?

### 5. Cost / Metering

Verify, from official sources where possible:

- which surfaces are subscription/web-first versus separately metered API products
- whether MCP changes pricing or merely changes the interface layer
- whether using APIs for Perplexity, xAI, or model execution clearly implies separate usage billing beyond web subscriptions

### 6. Best-Available Official Bridge

Based only on currently official capabilities, which of these now has the strongest factual support:

- browser adapters for web subscription surfaces
- MCP for surfaces with official MCP support
- direct API for selected infrastructure/model surfaces
- hybrid architecture using all three

## Acceptable Source Classes

- Official vendor docs first.
- Official release notes or changelogs first.
- Official pricing pages first.
- Official help-center or admin docs first.
- If you must use secondary reporting, label it clearly as secondary and lower confidence.

## Citation Contract

- Cite the strongest official sources directly.
- Distinguish verified fact from inference.
- Prefer precise dates, product names, and official pages.
- If a feature appears to exist only in enterprise or beta contexts, say so explicitly.

## Return Instructions

- Save or relay the response back into `-INBOX/commander/00-INBOX0/RESPONSE-PERPLEXITY-cc76-cli-web-gap-verification.md`
- Keep citations intact in the returned artifact.
- Return disproofs, caveats, and confidence limits explicitly.

## Bridge Command

```bash
python3 CLI-WEB-GAP/scripts/perplexity_response_bridge.py --dispatch engine/PACKET-PERPLEXITY-cc76-cli-web-gap-verification.md --response -INBOX/commander/00-INBOX0/RESPONSE-PERPLEXITY-cc76-cli-web-gap-verification.md --summary "Perplexity verification landed for current official capabilities around the CLI-web gap." --project-ontology
```

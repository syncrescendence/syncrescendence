# Augur Verification Packet — CLI/Web Gap Follow-Up

- Surface: `perplexity_web_surface`
- Packet type: `perplexity_verification`
- Created: `2026-03-02T19:05:00Z`
- Slug: `cc76-cli-web-gap-followup`
- Return artifact: `-INBOX/commander/00-INBOX0/RESPONSE-PERPLEXITY-cc76-cli-web-gap-followup.md`

## Claim Or Question To Verify

We need a narrow factual verification pass on the remaining open questions around using **Cowork + Claude in Chrome** as the practical bridge for browser-native subscription surfaces.

The decision we are trying to make is not the whole architecture.
It is whether current official capabilities are strong enough that Cowork + Claude in Chrome should be the first real execution layer before building custom browser adapters.

## Why This Verification Matters

If current official capabilities already support:

- browser back-and-forth
- local-folder working area
- repeated workflows
- file uploads
- multi-step follow-up loops

then the next move is a concrete prototype, not more architecture work.

If they do not, then the next move is custom browser-worker infrastructure.

## Verification Questions

### 1. Cowork + folder grounding

From official Anthropic sources:

- Can Cowork operate against a designated local folder as its working context?
- Can it read and write files there as part of a task?
- Are there any official constraints that would make folder-based job relay unrealistic?

### 2. Claude in Chrome browser execution

From official Anthropic sources:

- Can Claude in Chrome reliably perform multi-step browser interactions?
- Does it explicitly support repeated workflows, shortcuts, or task continuation?
- Can a Cowork task invoke Claude in Chrome as part of its execution path?

### 3. File uploads

From official sources only if possible:

- What kinds of uploads are explicitly supported by Claude in Chrome?
- Is support limited to image upload, or is there evidence of broader file-upload capability?
- Is there any official statement that would support using it for third-party site uploads in tools like NotebookLM or Perplexity?

### 4. Follow-ups and continuation

- Can Claude in Chrome keep state across a multi-step interaction on the same site during one task?
- Can it continue a prior browser workflow or act on existing tabs?
- Are there official limitations around long-running or complex chained browsing actions?

### 5. Extension / programmability / hooks

- Does Anthropic expose any official programmable interface, developer hook, or automation surface for Claude in Chrome beyond the user-facing workflow?
- If not, is the current official model purely interactive and task-driven?

### 6. Best factual interpretation

Based only on current official capabilities:

- Is Cowork + Claude in Chrome strong enough for a Perplexity browser relay prototype now?
- Is it strong enough for NotebookLM upload + synthesis prototype now?
- Which part remains unverified enough that we should treat it as experimental rather than architectural fact?

## Acceptable Source Classes

- Official Anthropic support docs first.
- Official Anthropic release notes first.
- Official Anthropic docs first.
- Use secondary sources only if the official docs are silent, and label them clearly as lower confidence.

## Citation Contract

- Cite official Anthropic sources directly where possible.
- Distinguish verified fact from inference.
- If a behavior is plausible but not explicitly documented, say so directly.

## Return Instructions

- Save or relay the response back into `-INBOX/commander/00-INBOX0/RESPONSE-PERPLEXITY-cc76-cli-web-gap-followup.md`
- Keep citations intact in the returned artifact.
- Return confidence limits explicitly.

## Bridge Command

```bash
python3 CLI-WEB-GAP/scripts/perplexity_response_bridge.py --dispatch engine/PACKET-PERPLEXITY-cc76-cli-web-gap-followup.md --response ./-INBOX/commander/00-INBOX0/RESPONSE-PERPLEXITY-cc76-cli-web-gap-followup.md --summary "Perplexity follow-up landed for current official Cowork and Claude in Chrome capabilities." --project-ontology
```

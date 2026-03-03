# Oracle Dispatch Packet — CLI/Web Gap Follow-Up

- Surface: `oracle_web_surface`
- Packet type: `oracle_dispatch`
- Created: `2026-03-02T19:05:00Z`
- Slug: `cc76-cli-web-gap-followup`
- Return artifact: `-INBOX/commander/00-INBOX0/RESPONSE-ORACLE-cc76-cli-web-gap-followup.md`

## Objective

Narrow the remaining uncertainty in the CLI↔web bridge question.

We no longer need another broad architecture answer.
We need a decisive recommendation about whether **Cowork + Claude in Chrome** should become the primary execution layer for web subscription surfaces before building a custom local queue + browser-worker fabric.

## Current State Summary

The repo now has:

- packetized web surfaces for Oracle, Perplexity, NotebookLM, and Claude Cowork
- checkpoint bridges for YouTube, xAI, Google model surfaces, Manus, GitHub, Cloudflare
- account/auth matrix
- Feedcraft stage 0
- IIC governance stage 0
- assessment of the first CLI/web gap research round

The current best working thesis is:

- repo/event/ontology remain truth plane
- some deterministic dispatcher remains control plane
- browser-capable subscription surfaces are the missing execution layer

The open decision is whether the best first execution layer is:

1. **Cowork + Claude in Chrome**
2. **custom local queue + Playwright browser workers**
3. **Cowork first, then custom workers later**

## Anchor Links

- [CLI/web gap assessment](https://github.com/truongphillipthanh/syncrescendence/blob/main/00-ORCHESTRATION/state/impl/CC76-CLI-WEB-GAP-RESPONSE-ASSESSMENT.md)
- [Packet standard](https://github.com/truongphillipthanh/syncrescendence/blob/main/00-ORCHESTRATION/state/impl/WEB-SURFACE-PACKET-STANDARD-CC75.md)
- [Surface taxonomy](https://github.com/truongphillipthanh/syncrescendence/blob/main/00-ORCHESTRATION/state/impl/EXOCORTEX-SURFACE-TAXONOMY-CC75.md)
- [Account/auth matrix](https://github.com/truongphillipthanh/syncrescendence/blob/main/00-ORCHESTRATION/state/impl/EXOCORTEX-ACCOUNT-IDENTITY-MATRIX-CC76.md)
- [Feedcraft stage 0](https://github.com/truongphillipthanh/syncrescendence/blob/main/00-ORCHESTRATION/state/impl/FEEDCRAFT-SURFACE-STAGE0-CC76.md)
- [IIC governance stage 0](https://github.com/truongphillipthanh/syncrescendence/blob/main/00-ORCHESTRATION/state/impl/IIC-GOVERNANCE-STAGE0-CC76.md)
- [Cowork getting started](https://support.claude.com/en/articles/13345190-get-started-with-cowork)
- [Claude in Chrome getting started](https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome)
- [Claude in Chrome release notes](https://support.claude.com/en/articles/12306336-claude-in-chrome-release-notes)
- [Cowork safety guide](https://support.claude.com/en/articles/13364135-utilizzo-di-cowork-in-sicurezza)

## Questions To Answer

### 1. Strategic recommendation

Given the current official Claude/Cowork/Chrome capabilities, what is the strongest recommendation:

- make Cowork + Claude in Chrome the primary web execution layer now
- use it only as a transitional prototype layer
- skip it and build custom browser workers immediately

State your answer clearly.

### 2. What would make the setup truly "fused"?

Define the minimum scaffold required so the setup is no longer just assisted browsing but a real bridge.

We need a concrete answer in terms of:

- dispatch primitive
- execution primitive
- return primitive
- truth primitive

### 3. Folder-based workflow

Cowork can operate on a local folder.

Is a designated folder plus browser execution enough to create a working relay, or is a real queue daemon still necessary even for v1?

Be specific about:

- one file per job vs single shared document
- attachments as sibling files
- output artifacts
- success/failure state

### 4. Uploads and follow-ups

Can Cowork + Claude in Chrome plausibly serve as the first bridge for:

- query/response
- file upload + query
- follow-up loop after an answer
- multi-step task on the same website

If yes, what constraints should we assume?
If no, what exact missing capability forces a custom browser worker?

### 5. Cowork’s right role

Should Cowork be:

- dispatch cockpit
- execution surface
- planning surface
- all three
- or something narrower

Distinguish control UX from truth plane.

## Required Output Contract

- Lead with your own thesis.
- Do not re-answer the broad architecture question from scratch.
- Focus only on the unresolved choice between Cowork/Chrome and custom browser workers.
- Return a recommended v1 stack and a v2 stack.
- Explicitly state what should be tested first this week.

## Return Instructions

- Save or relay the response back into `-INBOX/commander/00-INBOX0/RESPONSE-ORACLE-cc76-cli-web-gap-followup.md`
- Do not let the response remain only in web-session state.

## Bridge Command

```bash
python3 CLI-WEB-GAP/scripts/oracle_response_bridge.py --dispatch engine/PACKET-ORACLE-cc76-cli-web-gap-followup.md --response ./-INBOX/commander/00-INBOX0/RESPONSE-ORACLE-cc76-cli-web-gap-followup.md --summary "Oracle follow-up landed for Cowork/Chrome versus custom browser-worker strategy." --project-ontology
```

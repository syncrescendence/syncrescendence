# Exocortex Account And Identity Matrix — CC76

**Date**: 2026-03-02  
**Purpose**: make surface ownership, auth substrate, and current operating harness explicit so exocortex expansion does not outrun governance

---

## Why This Exists

The tooling lane now has real wrappers across multiple surface families:

- Oracle / Perplexity / NotebookLM / Claude Cowork
- GitHub / Manus / Cloudflare
- YouTube / xAI / Google model surfaces
- OpenClaw runtime and channel surfaces

The missing control layer was an explicit account and identity matrix.

This document does not attempt to define full IIC governance yet.
It does define the minimum operational facts needed now:

- which surface is being operated
- which harness currently owns it
- what auth substrate it uses
- what the current durable role is
- what remains unresolved

---

## Current Matrix

## CC90 Ownership Update

The exocortex ownership baseline has been updated:

1. all listed exocortex workspaces are now declared under `syncrescendence@gmail.com`
2. canonical workspace namespace is `syncrescendence`
3. auth dependency edges are explicitly tracked (`github -> supabase`, `slack -> incident`)

Live canonical registry:

- [EXOCORTEX-SURFACE-REGISTRY-CC90.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-SURFACE-REGISTRY-CC90.json)

Historical CC76 table below remains useful for provenance of earlier split-ownership state.

| Surface | Current Harness | Identity / Account Substrate | Auth Substrate | Status | Durable Role | Notes |
|---|---|---|---|---|---|---|
| `oracle_web_surface` | Commander relay | web session identity | browser session | packetized | strategic hypersensing | returned artifact only; no hidden authority |
| `perplexity_web_surface` | Commander relay | web session identity | browser session | packetized | citation-backed verification | returned artifact only |
| `notebooklm_surface` | Commander relay | Google web identity | browser session | packetized | source-bounded synthesis | personal NotebookLM remains browser-only |
| `claude_cowork_surface` | Commander relay | Claude web identity | browser session | packetized | collaborative external execution | same packet/landing pattern as NotebookLM |
| `github_issue_pr_surface` | Commander local | GitHub authenticated account | `gh` auth | implemented | coordination + verification | CI, issues, and templates already active |
| `manus_workflow_surface` | Manus | `syncrescendence` Manus tenant | API key in Keychain | implemented | autonomous backend execution | checkpoint bridge operational |
| `cloudflare_dns_domain_surface` | Commander local | Syncrescendence Cloudflare account | `cloudflared` login + `wrangler` auth | implemented | domain + edge infrastructure | public ontology edge is live |
| `gcloud_resource_surface` | Commander local | active Google Cloud account | `gcloud auth` | implemented | cloud infrastructure | infra/auth surface distinct from model surfaces |
| `google_model_surface` | Commander local or future wrapper | Google AI / Vertex project identity | API key or project credentials | implemented | programmatic model execution | bridge exists; account binding still needs concrete per-surface rollout |
| `youtube_feed_surface` | Commander local or future wrapper | Google / YouTube API project identity | API key or OAuth | implemented | feed/media ingestion | pointer-first capture only |
| `xai_model_surface` | Commander local or future wrapper | xAI account / project | API key | implemented | programmatic model execution | explicitly separate from Oracle/Grok web line |
| `obsidian_repo_surface` | Commander local | local repo user | local filesystem | implemented | repo-backed exocortex writing | `.obsidian/` remains non-authoritative |
| `slack_discord_runtime_surface` | OpenClaw + Commander local | workspace / bot identities | local OpenClaw channel auth | implemented | runtime channel state | provider health can be tracked before end-to-end dispatch returns |

---

## Agent Runtime Split

The current live agent split remains:

- **Ajna**: Claude/OpenClaw on the MacBook Air
- **Psyche**: ChatGPT Plus / `openai-codex` on the Mac mini

That split is documented separately in:

- [AGENT-RUNTIME-IDENTITIES-CC75.md](/Users/system/syncrescendence/orchestration/state/impl/AGENT-RUNTIME-IDENTITIES-CC75.md)

This matrix is narrower. It governs exocortex surfaces rather than local agent runtime identities.

---

## Operational Rules

## 1. Web Surfaces

Web-native surfaces should continue to use:

`repo packet -> returned artifact -> bridge event -> reconciliation -> ontology`

That applies to:

- Oracle
- Perplexity
- NotebookLM
- Claude Cowork

## 2. API / Backend Surfaces

API-capable surfaces should continue to use:

`checkpoint bridge -> event ledger -> reconciliation -> ontology`

That applies to:

- Manus
- GitHub
- Cloudflare
- Google model surfaces
- YouTube API
- xAI API

## 3. Identity Discipline

Every new surface should declare at minimum:

- current owning harness
- auth substrate
- storage location for local credentials
- whether the durable record is pointer-only, summary, or typed

If a new surface cannot answer those four questions, it is not ready to be onboarded.

---

## Unresolved Work

The matrix still needs future expansion for:

- explicit IIC ownership once that governance layer is live
- per-surface rotation runbooks
- service-specific rate-limit and cost ownership
- final Google split between AI Studio, Gemini API, and Vertex deployments

Those are not blockers for the current bridge layer, but they are the next governance step after surface onboarding.

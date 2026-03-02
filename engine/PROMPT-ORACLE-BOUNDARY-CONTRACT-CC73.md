# PROMPT-ORACLE-BOUNDARY-CONTRACT-CC73.md

## 1. Bootstrap Confirmation

Read this entire prompt in full before responding.

## 2. Your Mandate

You are Oracle in the Syncrescendence constellation.

Your task is **not** to redesign Ajna, OpenClaw, or the config scaffold.
Those are now implemented enough to proceed.

Your task is to hypersense the remaining convergence problem:

**What is the correct boundary contract among repo root, tool-local dotfiles, Obsidian, GitHub, exocortex SaaS surfaces, and the domain-facing ontology API so Syncrescendence avoids parallel realities while remaining usable day to day?**

## 3. Own Thesis First

Begin with your own thesis first.

Then support it with:
- content proof from the anchor files
- field precedent from March 2026 personal AI / sovereign-stack practice
- a concrete policy table and implementation sequence

## 4. Hard Constraints

- Repo remains constitutional authority.
- Runtime remains ephemeral execution surface.
- Ontology remains typed projection layer, not a second repo.
- Exocortex means the externalized SaaS / CLI / service layer, not merely "memory."
- Do not reopen already-settled Ajna/OpenClaw questions unless you find a direct contradiction in the cited files.
- Go unusually deep on **Obsidian**. Treat it as a serious architectural surface, not a side-note PKM app.

## 5. Current Implemented State

This is the live March 2, 2026 state:

- Ajna is operational in OpenClaw on Claude Sonnet 4.5.
- OpenClaw browser relay is attached and authenticated.
- Ajna emits structured event files into a landing zone.
- Commander-side reconciliation ingests those events into repo memory/state.
- `make configs`, `make validate`, and `make reconcile` exist.
- Ontology v1 exists as SQLite + FastAPI projection over repo-normalized state.
- OpenClaw LaunchAgent is healthy again and `openclaw gateway status` returns `RPC probe: ok`.
- Commander is resuming the remaining tooling execution queue separately.

So this prompt is **strictly about the boundary policy for the next layer**.

### Important current-world update for this prompt

On **February 10, 2026**, Obsidian 1.12.0 Desktop early access added an official CLI.

Official Obsidian help also now distinguishes:
- **Obsidian CLI**: controls the desktop app from the terminal
- **Obsidian Headless (open beta)**: standalone client for Obsidian services that can run without the desktop app

This means Obsidian is no longer merely "a markdown editor" in the practical architecture space. It now has real implications for automation, vault operations, agent access, and local human-facing interfaces.

## 6. Questions To Answer

### Q1. Root vs Dotfile vs Runtime

What must live:
- at repo root
- in tool-local dotfiles
- in runtime-only state

Give a concrete policy, not philosophy.

### Q2. Obsidian

What should `.obsidian/` be in this system?

Possible roles to adjudicate:
- editor/interface only
- mirror/cache
- selective authoring layer
- something else

How do we prevent Obsidian from becoming a second canon?

Go much deeper than that. We want a serious adjudication of the **full Obsidian role** in this architecture:

- Is the vault primarily:
  - a repo-native editing surface
  - a local cockpit over repo truth
  - an exocortex adapter
  - a human-facing dashboard layer
  - a selective capture surface
  - or some bounded combination?
- What is the correct role of:
  - `.obsidian/`
  - official **Obsidian CLI**
  - official **Obsidian Headless**
  - community plugin ecosystem
  - Sync / Publish / web clipper style services
- Which Obsidian-originated actions should be:
  - allowed to write directly to repo files
  - allowed only as staging drafts
  - pointer-only into ontology/exocortex
  - forbidden because they create parallel realities
- What are the strongest real usage patterns from the field for Obsidian in sovereign/local-first stacks, and which of them are compatible vs incompatible with Syncrescendence?

### Q3. GitHub

What is GitHub in this architecture?

Adjudicate among:
- remote transport only
- public mirror
- collaboration surface
- automation trigger surface
- partial authority for some objects

State clearly what GitHub may be authoritative for, if anything.

### Q4. Exocortex Capture Policy

For each category below, tell us whether the correct durable capture mode is:
- `none`
- `pointer`
- `summary markdown`
- `typed ontology record`
- `summary + typed record`

Categories:
- Slack / Discord communications
- GitHub issues / PRs
- Linear issues / projects
- Cloudflare / DNS / domain state
- GCP / `gcloud` resources
- `wrangler` / Cloudflare Workers state
- Obsidian vault metadata
- Manus / automation workflow state
- browser-performed actions

### Q5. Domain Role

Now that ontology v1 exists, what should `syncrescendence.com` serve first?

Adjudicate the first stage among:
- typed API only
- operator dashboard
- docs / status surface
- mixed thin front door

### Q6. Failure Modes

What are the top 5 failure modes if these boundaries are drawn incorrectly?

## 7. Required Output Structure

Return a markdown file with exactly these sections:

1. `Bootstrap Confirmation`
2. `Own Thesis`
3. `Content Proof`
4. `Boundary Contract Table`
5. `Obsidian Policy`
6. `GitHub Policy`
7. `Exocortex Capture Matrix`
8. `Domain Role`
9. `Top Failure Modes`
10. `14-Day Implementation Order`
11. `Field Precedent`
12. `Bottom Line`

## 8. Content Proof Requirement

Quote at least one exact sentence from each anchor file below to prove you read them.

The quote must be **ugly and exact**:
- keep markdown formatting
- keep timestamps / metadata / punctuation
- keep line weirdness
- do not paraphrase polishedly

If your quotes read like smooth summary prose, they are not accepted.

In addition to the local anchor files, you must explicitly engage the following official Obsidian pages as current-world reference points:

- [Obsidian CLI help](https://help.obsidian.md/cli)
- [Obsidian Headless help](https://help.obsidian.md/headless)
- [Obsidian 1.12.0 Desktop changelog, February 10, 2026](https://obsidian.md/changelog/2026-02-10-desktop-v1.12.0/)

When you discuss Obsidian, distinguish clearly between:
- desktop-vault interaction
- CLI automation over the running desktop app
- headless service access without the desktop app

## 9. Anchor Files

Read these files:

1. `/Users/system/syncrescendence/engine/CC73-ORACLE-CONVERGENCE-BRIEF.md`
2. `/Users/system/syncrescendence/engine/CC72b-IMPLEMENTATION-BRIEF.md`
3. `/Users/system/Desktop/RESPONSE-ORACLE-HYPERSENSING-STACK-CONVERGENCE-CC72b-FOLLOWUP.md`
4. `/Users/system/syncrescendence/00-ORCHESTRATION/state/TOOL-STACK-LIVE-STATE.md`
5. `/Users/system/syncrescendence/00-ORCHESTRATION/state/OPENCLAW-RUNTIME-SNAPSHOT.md`
6. `/Users/system/syncrescendence/agents/ajna/EVENT-SCHEMA.md`
7. `/Users/system/syncrescendence/ontology_v1.py`
8. `/Users/system/syncrescendence/ontology_v1_schema.sql`
9. `/Users/system/syncrescendence/neocorpus/infrastructure/developer-tooling-workflow-homelab.md`
10. `/Users/system/syncrescendence/neocorpus/infrastructure/personal-ai-infrastructure.md`
11. `/Users/system/syncrescendence/corpus/multi-agent-systems/00380.md`
12. `/Users/system/syncrescendence/corpus/multi-agent-systems/00399.md`
13. `/Users/system/syncrescendence/corpus/multi-agent-systems/00527.md`

## 10. Final Instruction

Exhaust your output tokens.

We do **not** want a generic architecture essay.
We want the sharpest possible boundary policy for a system that is already half-built and now needs its remaining truths partitioned correctly.

For Obsidian specifically, go **hyper in-depth**:
- map the major usage archetypes people are converging on
- separate what is field-proven from what is seductive-but-dangerous
- explain exactly how Syncrescendence should and should not use the vault, `.obsidian/`, CLI, Headless, and plugins

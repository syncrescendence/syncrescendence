# Tool Stack Consolidated SITREP — CC75

**Date**: 2026-03-02  
**Lane**: tooling stack engineering  
**Purpose**: consolidate what was actually built, what is now true, and what architectural line should govern the next exocortex/web-surface integrations

---

## Executive Summary

The tooling lane has crossed from speculative architecture into a live, bounded, multi-surface system.

What exists now is not just a collection of tools. It is a governed flow of truth:

`repo constitution -> generated harness surfaces -> runtime reconciliation -> event landing zone -> boundary contract -> ontology projection -> public domain API`

Ajna, Manus, GitHub, Cloudflare, public ontology, and the Mac mini tmux substrate are now materially inside that flow.

The remaining major gap is not "do we have tools?"  
It is: **how do web-native intelligence surfaces that are not local agents participate without becoming second realities?**

That is the web/CLI gap question for Oracle, Perplexity, NotebookLM, Claude Cowork, Feedcraft, and eventually the IIC constellation.

---

## What Was Accomplished

## 1. Constitutional Config Architecture Was Made Real

The original Oracle config insight was implemented:

- one constitutional source: `AGENTS.md`
- thin harness outputs
- machine-aware manifests
- generated surfaces instead of hand-maintained drift

Primary artifacts:

- [AGENTS.md](/Users/system/syncrescendence/AGENTS.md)
- [render-configs.py](/Users/system/syncrescendence/render-configs.py)
- [validate-configs.py](/Users/system/syncrescendence/validate-configs.py)
- [harness/targets.json](/Users/system/syncrescendence/harness/targets.json)
- [machine/lisas-macbook-air.json](/Users/system/syncrescendence/machine/lisas-macbook-air.json)
- [machine/mac-mini.json](/Users/system/syncrescendence/machine/mac-mini.json)
- [configs/manifest.json](/Users/system/syncrescendence/configs/manifest.json)

Operational result:

- repo truth now generates Commander, Ajna, Psyche, Adjudicator, and Cartographer surfaces
- Ajna and Psyche receive compact OpenClaw surfaces under bootstrap limits
- execution-surface routing doctrine is now constitutional rather than conversational

## 2. Ajna Was Rewired Into Repo Truth

Ajna is no longer hypothetical and no longer Kimi-primary.

Primary facts:

- live runtime moved to Claude Sonnet 4.5 via OpenClaw
- browser relay was fixed and verified
- runtime memory and repo truth were reconciled
- Ajna can emit structured events instead of leaving state trapped in runtime

Primary artifacts:

- [agents/ajna/OPENCLAW-ROLE.md](/Users/system/syncrescendence/agents/ajna/OPENCLAW-ROLE.md)
- [agents/ajna/EVENT-SCHEMA.md](/Users/system/syncrescendence/agents/ajna/EVENT-SCHEMA.md)
- [sync-openclaw.py](/Users/system/syncrescendence/sync-openclaw.py)
- [TOOL-STACK-LIVE-STATE.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/TOOL-STACK-LIVE-STATE.md)

Operational result:

- Ajna became a real strategist/runtime surface, not a future placeholder
- OpenClaw runtime can now be snapped back into repo state

## 3. The First Durable Reconciliation Loop Exists

A real landing zone now exists for agent/exocortex/runtime outputs.

Primary artifacts:

- [reconcile-ajna-events.py](/Users/system/syncrescendence/reconcile-ajna-events.py)
- [memory/AJNA-EVENT-LEDGER.jsonl](/Users/system/syncrescendence/memory/AJNA-EVENT-LEDGER.jsonl)
- [memory/AJNA-EVENT-SUMMARY.md](/Users/system/syncrescendence/memory/AJNA-EVENT-SUMMARY.md)
- [00-ORCHESTRATION/state/AJNA-EVENT-RECONCILIATION.json](/Users/system/syncrescendence/00-ORCHESTRATION/state/AJNA-EVENT-RECONCILIATION.json)

Operational result:

- runtime changes can enter the repo in structured form
- the repo now has a durable event ledger
- ontology projection can occur after reconciliation instead of from raw runtime exhaust

## 4. Boundary Contract Was Ratified And Enforced

The Oracle boundary round was distilled into machine-checked policy.

Primary artifacts:

- [BOUNDARY-CONTRACT-POLICY-CC73.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/BOUNDARY-CONTRACT-POLICY-CC73.md)
- [EXOCORTEX-CAPTURE-POLICY.json](/Users/system/syncrescendence/00-ORCHESTRATION/state/EXOCORTEX-CAPTURE-POLICY.json)

Operational result:

- repo root = authority
- dotfiles = local interface/runtime state
- GitHub = verification + coordination surface
- Obsidian = cockpit, not canon
- ontology = projection only
- exocortex = pointer-first externalized cognitive surface

## 5. Ontology v1 Exists And Is Public

The ontology is no longer just a concept.

Primary artifacts:

- [ontology_v1.py](/Users/system/syncrescendence/ontology_v1.py)
- [ontology_v1_schema.sql](/Users/system/syncrescendence/ontology_v1_schema.sql)
- [00-ORCHESTRATION/state/impl/ONTOLOGY-DOMAIN-STAGE1.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/impl/ONTOLOGY-DOMAIN-STAGE1.md)
- [00-ORCHESTRATION/state/impl/CLOUDFLARED-ONTOLOGY-STAGE1.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/impl/CLOUDFLARED-ONTOLOGY-STAGE1.md)

Operational result:

- local ontology API works
- local Caddy proxy works
- public domain path works through Cloudflare Tunnel
- `syncrescendence.com` is now a typed API surface, not a speculative domain

## 6. Manus Became A Real Execution Surface

Manus is not theoretical anymore.

Primary facts:

- API key exists
- Manus API auth shape was verified
- Manus bridge/checkpoint path exists and projects into ontology

Primary artifacts:

- [manus_checkpoint_bridge.py](/Users/system/syncrescendence/manus_checkpoint_bridge.py)
- [00-ORCHESTRATION/state/impl/MANUS-FIRST-DISPATCH-CC73.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/impl/MANUS-FIRST-DISPATCH-CC73.md)

Operational result:

- tasks that cannot be cleanly completed locally can be routed to Manus
- Manus outputs no longer need to remain external narrative; they can return through the event/ontology pipeline

## 7. GitHub Became Verification + Coordination Surface

GitHub is now structurally in the system without becoming a second control plane.

Operational result:

- constitutional integrity CI exists
- issue templates and labels exist
- the tooling convergence queue was issueified
- GitHub issue state is bridgeable into ontology

Primary artifacts:

- [github_issue_bridge.py](/Users/system/syncrescendence/github_issue_bridge.py)
- [.github/workflows/constitutional-integrity.yml](/Users/system/syncrescendence/.github/workflows/constitutional-integrity.yml)

## 8. Exocortex Bridges Now Exist

There is now a general pattern for external surfaces.

Primary artifacts:

- [exocortex_event_bridge.py](/Users/system/syncrescendence/exocortex_event_bridge.py)
- [obsidian_repo_bridge.py](/Users/system/syncrescendence/obsidian_repo_bridge.py)
- [cloudflare_domain_bridge.py](/Users/system/syncrescendence/cloudflare_domain_bridge.py)
- [github_issue_bridge.py](/Users/system/syncrescendence/github_issue_bridge.py)
- [manus_checkpoint_bridge.py](/Users/system/syncrescendence/manus_checkpoint_bridge.py)
- [channel_surface_bridge.py](/Users/system/syncrescendence/channel_surface_bridge.py)

Operational result:

- external surfaces can emit structured, boundary-compliant events
- ontology receives normalized checkpoints rather than raw dashboard state

## 9. Mac mini tmux Substrate Was Revived To Stage 1

The mini is no longer “anesthetized” in the old absolute sense.

Primary artifacts:

- [TMUX-CONSTELLATION-REVIVAL-STAGE1.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/impl/TMUX-CONSTELLATION-REVIVAL-STAGE1.md)
- [MINI-CONSTELLATION-STATUS.md](/Users/system/syncrescendence/00-ORCHESTRATION/state/MINI-CONSTELLATION-STATUS.md)
- [bootstrap-mac-mini.sh](/Users/system/syncrescendence/bootstrap-mac-mini.sh)
- [constellation-mini-stage1.sh](/Users/system/syncrescendence/constellation-mini-stage1.sh)
- [install-mini-constellation-launchagent.sh](/Users/system/syncrescendence/install-mini-constellation-launchagent.sh)
- [com.syncrescendence.constellation-stage1.plist](/Users/system/syncrescendence/00-ORCHESTRATION/state/impl/com.syncrescendence.constellation-stage1.plist)

Operational result:

- mini reachable over SSH
- canonical repo checkout exists at `/Users/home/syncrescendence`
- detached `tmux` session `constellation` exists with `psyche`, `adjudicator`, `cartographer`, `ops`
- LaunchAgent exists to reassert the stage-1 session
- this is substrate revival, not full automation revival

---

## What Is True Right Now

## Stable / Live

- constitutional config pipeline
- Ajna runtime reconciliation
- event ledger + reconciliation
- boundary contract
- ontology API and public domain path
- Manus as external execution surface
- GitHub as verification/coordination surface
- Mac mini stage-1 tmux substrate

## Intentionally Not Yet Fully Revived

- Psyche end-to-end autonomous work
- Slack/Discord end-to-end operational dispatch
- full tmux agent autostart fabric
- browser-native Oracle/Perplexity ingress/egress automation
- NotebookLM and Claude Cowork integration
- Feedcraft and IIC operationalization through the same exocortex boundary

---

## The Web/CLI Gap

## The Problem

Oracle and Perplexity are not currently first-class local agents.

That means they do not naturally participate in:

- repo-driven config generation
- local CLI orchestration
- structured event emission
- ontology projection

Without care, they become high-value but non-integrated web oracles:

- valuable answers
- poor continuity
- no machine-checked return path
- high risk of second-reality drift

## The Correct Architectural Resolution

Do **not** try to force Oracle or Perplexity to become fake local CLIs before their participation model is mature.

Instead, make them **web exocortex surfaces with a strict bidirectional relay contract**.

That means:

### 1. Outbound to web surfaces

Agents or Commander generate a **dispatch packet** in the repo.

That packet should contain:

- objective
- exact anchor links
- output contract
- return location
- event metadata

This packet is the authoritative outbound artifact.

### 2. Inbound from web surfaces

The returned Oracle/Perplexity/NotebookLM/Cowork result lands as:

- a markdown artifact in the repo or Desktop relay
- then a structured exocortex event is emitted
- then reconciliation/ontology projection happens

This makes the web response part of governed system state rather than “something a tab said.”

### 3. Human or automation is only the courier

The Sovereign, Manus, future browser automation, or a revived agent can relay the packet.

But the courier is **not** the authority.

Authority remains:

- outbound packet in repo
- inbound response artifact in repo
- reconciliation event

This is the same pattern already used successfully for Oracle prompt engineering, GitHub, Manus, and Cloudflare.

## Minimal Two-Way Contract

To close the web/CLI gap, Oracle and Perplexity should be treated as:

- `surface = exocortex` when the durable return is a typed pointer/summary into repo truth
- `surface = browser` only when the task is specifically UI/browser mediated

The durable flow should be:

`repo dispatch packet -> web surface reply -> repo response artifact -> exocortex event -> reconciliation -> ontology`

That is two-way communication without pretending the web app is the constitution.

## What “Two-Way” Actually Means

Not “agents directly chat to each other.”

It means:

1. Commander or another agent creates a precise outbound request artifact.
2. The web intelligence surface receives it.
3. Its response returns as a governed artifact.
4. Other agents can consume the returned artifact through repo and ontology.

That is the correct kind of inter-agent communication here: **artifact-mediated, not thread-mediated**.

---

## How To Close Oracle + Perplexity Specifically

## Oracle

Oracle is already close to this pattern culturally, but still too human-relay dependent.

What is needed next:

1. Create a formal Oracle dispatch packet template in the repo.
2. Create a formal Oracle response landing-zone convention.
3. Emit an exocortex event whenever an Oracle response lands.
4. Project key response metadata into ontology.

This turns Oracle from “web sage” into a governed external sensing node.

## Perplexity

Perplexity should be treated differently from Oracle:

- Oracle = strategic hypersensing + thesis
- Perplexity = external verification + citation

So Perplexity needs its own narrower packet shape:

- claim to verify
- acceptable sources
- citation requirements
- response format

Perplexity should not become a freeform synthesis node.
It should be a verifier surface whose outputs re-enter as citation-bearing exocortex artifacts.

---

## Agents To Each Other

The correct answer is:

**not direct unconstrained conversation.**

Direct conversational coupling between many agents creates hidden state and drift.

The better pattern is:

- agents emit bounded artifacts/events
- repo stores durable truth
- ontology provides typed projection/query layer
- other agents consume those artifacts

So “agents to each other” should mean:

- shared repo artifacts
- shared event ledger
- shared ontology projections
- selective dispatch packets

Not:

- freeform background chatter
- hidden long-running conversational state between surfaces

tmux stage 2 may add more local inter-agent execution, but the data plane should still remain artifact-first.

---

## Next Surfaces To Onboard

The next surfaces named by the Sovereign are coherent with the same architecture.

## 1. NotebookLM

NotebookLM should enter as an exocortex synthesis surface, not as authority.

Correct role:

- corpus digestion
- source-bounded synthesis
- notebook-level retrieval/summarization

Correct return path:

- notebook prompt/spec in repo
- notebook output saved back as markdown artifact
- exocortex event emitted
- ontology pointer or summary record

NotebookLM should not become a shadow canon.

## 2. Claude Cowork

Claude Cowork should be treated as a collaborative external execution/synthesis surface.

Correct role:

- bounded parallel execution or collaboration
- not constitutional authority

Correct pattern:

- repo dispatch packet
- returned artifact
- event reconciliation

## 3. Feedcraft

Feedcraft belongs to the same realm because it is about platform-conditioned exocortex configuration.

Correct role:

- exocortex shaping
- signal intake/output conditioning
- platform physics and curation

That means it should eventually integrate through:

- typed surface descriptors
- capture policy
- platform-specific event classes

## 4. IIC

IIC is the higher-order identity/cognitive compartmentalization framework above these tools.

The right sequence is:

- do not operationalize the full IIC layer before the exocortex/tool boundary is clean
- once the boundary contract is stable, IIC can specify which surfaces belong to which identity-intelligence complex

In other words:

Feedcraft and IIC are not separate from the exocortex line.
They are **higher-order organization of the exocortex**.

---

## Recommended Next Engineering Moves

## Immediate

1. Formalize web-avatar dispatch packets for Oracle and Perplexity.
2. Add first exocortex bridge wrappers for Oracle-response and Perplexity-response landings.
3. Keep NotebookLM and Claude Cowork onboarding inside the same packet -> response -> event -> ontology loop.

## After That

4. Decide whether tmux stage 2 should auto-launch real agent entry commands or remain prepared shells longer.
5. Define exocortex surface classes for:
   - Oracle
   - Perplexity
   - NotebookLM
   - Claude Cowork
6. Only then begin Feedcraft/IIC operationalization on top of that clean surface taxonomy.

---

## Principle To Preserve

The mistake to avoid is building every new web surface as its own special-case ritual.

The correct pattern is:

- one repo constitution
- one boundary contract
- one event return path
- one ontology projection layer
- many execution/sensing surfaces

That is how the constellation expands without fragmenting.

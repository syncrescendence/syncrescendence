# CLI-Web Gap Intent And Operating Model

**Date**: 2026-03-02  
**Purpose**: capture the actual intent behind the Cowork line and the broader CLI<->web gap closure effort so the work does not degrade into ad hoc browser rituals or uncontrolled tool sprawl

---

## Core Problem

The project increasingly depends on high-value web-native subscription surfaces:

- Claude / Cowork / Claude in Chrome
- Perplexity
- Grok / Oracle
- NotebookLM
- later Claude Cowork extensions, Feedcraft surfaces, and other exocortex tools

The repo and CLI environment are the constitutional and durable side of the system.
The web tools are often the most capable and most economically attractive side of the system.

The gap is this:

- the CLI cannot natively inhabit browser state
- the web tools cannot be allowed to become hidden sources of truth
- API-first integration often defeats the point by introducing separate metered costs or losing access to subscription-only capability

So the real question is not "how do we call everything from code."
It is:

**How do we leverage paid web/subscription tools from a single dispatch point, without creating a second brain and without defaulting to extra API spend?**

---

## Governing Intent

The intent of this line is:

1. preserve `repo + event ledger + ontology` as the truth plane
2. turn browser-native subscription surfaces into callable workers
3. keep the return path artifact-based and durable
4. use APIs and MCP selectively where they are truly superior
5. avoid turning Cowork, the website, or any external surface into hidden authority

The system should become:

`dispatch -> execution surface -> returned artifact -> reconciliation -> ontology projection`

not:

`chat thread / browser tab -> informal memory -> invisible state`

---

## Why Cowork Exists In This Architecture

Cowork is not the final orchestrator.
Cowork is the best officially supported **v1 execution surface** currently available for closing part of the gap.

Why Cowork was chosen for v1:

- official local folder grounding exists
- official local file read/write exists
- official Claude in Chrome integration exists
- it can execute multi-step browser tasks through a subscription surface you already pay for
- it can write outputs back to disk without manual copy-paste

Why Cowork is not the final answer:

- it is slower and more gesture-heavy than a dedicated adapter
- it shares browser context with a human-facing environment
- it is not truly headless
- it should not become the hidden decision-maker or canonical store
- it is still closer to an agentic operator surface than a deterministic runtime

So the intended role of Cowork is:

- **prototype execution plane**
- **human-supervised transition layer**
- **proof that subscription-surface relays can be closed**

not:

- permanent sovereign orchestrator
- source of truth
- final automation substrate

---

## V1 Bridge Model

The first closure model is intentionally simple.

Use:

- repo packet as outbound dispatch artifact
- a designated local folder as relay boundary
- Cowork grounded to that folder
- Claude in Chrome for browser-native execution
- status and artifact files as return contract
- Hazel as edge-trigger finalizer
- repo/event/ontology as the durable landing path

This is what the first live Perplexity relay already proved.

The important insight is:

**v1 does not need teleportation.**
It needs a disciplined postal system.

That means:

- one job per file
- one response per file
- one status file per run
- no shared mutable document
- no hidden browser-only result

---

## Bifurcation: Gestures vs Scripting

One of the main lessons from the first live run is that the bridge must sharply separate:

## Gesture work

Use gestures only where the website requires them:

- click
- type
- paste
- select
- upload
- navigate
- interact with site-native controls such as follow-up fields or copy buttons

## Scripted work

Use scripts for everything deterministic:

- staging packets
- copying packets into relay-local scope
- selecting exact output paths
- validating filenames
- finalizing returned artifacts
- bridging into repo events
- ontology projection
- replay, cleanup, and audit

The rule is:

**gesture only for irreducibly visual web actions; script everything before and after.**

This is the key cleanup principle for the next iteration.

---

## What "Fused" Actually Means

The goal is not merely "the CLI can open a browser."

The gap is truly closed only when:

1. a job is issued from a single dispatch surface
2. the web action is performed without manual copy-paste in the middle
3. the result lands back automatically as an artifact
4. that artifact becomes repo truth through reconciliation

So fusion is:

`single dispatch point -> browser-capable worker -> automatic return artifact -> repo truth`

Anything less is assisted operation, not true closure.

The first Cowork relay succeeded on this definition for a real Perplexity task.

---

## Economic Intent

This line is explicitly about **not** defaulting to metered API spend when subscription surfaces already provide the needed capability.

The intended economic hierarchy is:

1. use already-paid subscription surfaces where feasible
2. use browser execution to leverage those subscriptions
3. use APIs only where they are structurally worth paying for
4. use MCP where it improves interface shape, not because it magically removes billing

MCP is valuable, but it is not a billing bypass.

The true cost-saving logic is:

- subscriptions for cognition and web-native capability
- local scripts for deterministic plumbing
- artifact relay for durability
- APIs only where browser execution is inferior

---

## What The Website / Domain Is For

The domain or website is not meant to be the authority.

It may become:

- a control plane
- a review plane
- a monitoring plane
- a human dispatch surface

But it must not replace:

- the repo
- the event ledger
- the ontology projection layer

So the website is allowed to become a cockpit.
It is not allowed to become the canon.

---

## What The Durable v2 Direction Is

The intended v2 direction is not "more Cowork."

It is:

- local queue/orchestrator
- dedicated browser profiles or workers
- more deterministic browser adapters
- optional MCP wrappers over those adapters
- clearer separation of execution workers from human-facing control surfaces

That means:

- Cowork proves the path
- dedicated browser workers harden the path

The likely split is:

- **v1**: Cowork + Claude in Chrome + file relay + Hazel
- **v2**: queue daemon + browser adapters + dedicated execution box (likely the mini, later possibly cloud/VPS)

---

## Intended Execution Surfaces

The system now distinguishes these classes:

## Truth plane

- repo
- event ledger
- ontology

## Dispatch / control plane

- repo-authored packets
- local queue
- possibly website/Cowork as UI later

## Execution surfaces

- Cowork + Claude in Chrome for v1 browser execution
- Manus for bounded autonomous backend work
- local scripts for deterministic transforms
- future browser adapters / Playwright workers for v2

## Exocortex surfaces

- Perplexity
- Oracle / Grok web
- NotebookLM
- Claude Cowork
- later other surfaces like Feedcraft-related tools

---

## Current Proven Facts

As of this memo:

- the packet-and-landing architecture exists
- the event/ontology normalization path exists
- the Cowork relay folder exists
- Hazel can finalize returned relay jobs
- the first live Perplexity round-trip succeeded end to end

That means the bridge is no longer hypothetical.

What remains is:

- performance cleanup
- clearer gesture-vs-script rails
- dedicated browser execution context
- extension to additional surfaces, especially NotebookLM

---

## Practical Rules Going Forward

1. Do not build new web relays as one-off rituals.
2. Every new surface should declare its dispatch artifact, execution path, return artifact, and finalization path.
3. Prefer `Copy` or other site-native affordances over reconstructing responses manually when reliable.
4. Keep browser gestures minimal and deterministic.
5. Keep returned artifacts durable and local.
6. Keep Cowork as execution assistance, not authority.
7. Keep the repo as the constitutional center.

---

## Net Intent

This project is not trying to "make the browser magically become the CLI."

It is trying to build a disciplined relay fabric where:

- web-native subscription tools become callable workers
- the repo remains the authority
- returned work becomes durable system truth
- cost stays aligned with already-paid subscriptions where possible

Cowork is the first real bridge because it closes the loop with the least new infrastructure.

The long-term destination is a cleaner worker fabric.
But the strategic intent is already fixed:

**one dispatch world, many execution surfaces, one truth plane.**

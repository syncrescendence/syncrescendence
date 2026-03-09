# Response

**Response ID**: `RSP-20260309-office-agent-federalism-pass`  
**Surface**: `codex_parallel_session`  
**Date received**: `2026-03-09`  
**Dispatch packet**: `communications/prompts/PACKET-CODEX-CAMPAIGN-01-LANE-05-OFFICE-AGENT-FEDERALISM-PASS.md`  
**Result state**: `complete`  
**Receipt artifacts**:
  - `communications/responses/RESPONSE-CODEX-CAMPAIGN-01-LANE-05-OFFICE-AGENT-FEDERALISM-PASS.md`

## Returned Content

The current shell is directionally correct: the five-office federal model survived contact with the actual harness stack, and `offices/` is the right live root instead of reviving `agents/`. The real mismatch is not topological philosophy. It is uneven physicalization. The office layer is constitutionally defined and largely scaffolded, while harness reality is mostly carried by playbooks, root veneers, and runtime docs rather than by office-local contracts and metadata.

The practical conclusion is:

- keep the five offices federal and path-stable by office identity
- keep harnesses as playbook, adapter, runtime, and metadata bindings
- keep avatar names as symbolic routing handles only
- refine the office layer by hardening the already-ratified office/harness junctions, especially for Ajna and Psyche

## 1. Evaluation Of Current `offices/` Topology

### 1.1 Against prior `agents/` lineage

The successor shell preserved the right part of the predecessor pattern:

- `offices/` contains the same five burden-bearing roles as the old `agents/*`: Commander, Adjudicator, Ajna, Cartographer, Psyche
- the refined predecessor substructure survived: `inbox/{pending,active,done,failed,blocked}`, `outbox/{dispatches,receipts,results}`, `memory/{journal,cache,sync}`, and `platform/{contracts,templates,logs}`
- the live constitutional artifacts explicitly anchor this to predecessor lineage rather than pretending it is new invention:
  - `orchestration/state/impl/OFFICE-LAW-v1.md`
  - `orchestration/state/impl/OFFICES-LAYOUT-v1.md`
  - `orchestration/state/impl/OFFICE-TOPOLOGY-REFINEMENT-v1.md`
  - `pedigree/rehoused/pre-syncrephoenix/agents/*/INIT.md`

The old `agents/` root itself should remain pedigree only. There is no live `agents/` lane in the repo now, which is correct. The surviving institutional meaning was office-local work, not the old path name.

### 1.2 Against current harness reality

The live harness stack is now clearer than the old lineage:

- Claude Code is surfaced through generated root veneers and Commander/Adjudicator posture
- Gemini CLI is surfaced through the generated Gemini veneer and Cartographer posture
- OpenClaw is the persistent runtime substrate split across Ajna and Psyche
- other surfaces such as Manus, NotebookLM, Google AI Studio, OpenHands, Aider, and Opencode are present as playbooks or capability-registry entries, not as burden-bearing offices

That split is already encoded in the repo:

- office law and office playbooks carry burden by office identity
- harness playbooks carry native surface doctrine
- root veneers such as `CLAUDE.md` and `GEMINI.md` are thin generated adapters over constitutional truth
- avatar mappings in `AGENTS.md` are explicitly non-sovereign

This means the federalism model is coherent with current harness reality.

### 1.3 Current mismatch

The mismatch is physical completeness, not conceptual design:

- Commander is the only office with materially developed local contracts and templates under `offices/commander/platform/{contracts,templates}`
- Adjudicator, Cartographer, Ajna, and Psyche mostly have scaffolded office trees plus a small amount of queued work or receipts
- Ajna and Psyche have real harness-specific burden via OpenClaw, but that reality mostly lives in `playbooks/openclaw/PLAYBOOK.md`, the office playbooks, and runtime docs rather than in office-local metadata/contracts
- Adjudicator and Cartographer have live office identities but only thin office-local law despite Codex and Gemini being real harness bindings

Net assessment:

- topology: correct
- federal split: correct
- harness split: correct
- physicalization depth: uneven and tranche-ready for refinement

## 2. What Belongs Where

### 2.1 Should remain federal

These should stay federal because they are burden-bearing shell law or cross-office truth:

- the five offices themselves as constitutional roles
- office identity and routing law
- promotion thresholds between `offices/`, `communications/`, `executive/`, and `runtime/`
- artifact classes and validator rules
- root adapter rendering discipline
- the avatar registry and harness-differentiation rule in `AGENTS.md`
- any decision about adding or retiring an office

### 2.2 Should become harness-specific

These should live in playbooks, office-local metadata, runtime docs, or operator contracts tied to a surface:

- provider, auth mode, machine binding, and account binding
- command-surface capability claims
- browser/channel/runtime repair doctrine
- harness-native prompt/loading doctrine
- surface-specific event schemas, receipts, and logs
- office-local templates that only make sense for one harness

This is especially true for:

- Ajna and Psyche under OpenClaw
- Adjudicator under Codex
- Cartographer under Gemini
- Commander under Claude Code

### 2.3 Should remain avatarized only at the symbolic layer

These should not become new directories, offices, or constitutional authorities:

- `Vanguard`, `Vizier`, `Diviner`, `Oracle`, `Augur`
- stage0 surface avatars such as `Fabricator`, `Alchemist`, `Archivist`, `Outrider`, `Automator`, `Pairwright`
- mutable harness labels when they are only current bindings rather than durable roles

Avatarization is useful for routing shorthand and symbolic continuity. It should not be allowed to create new sovereign paths, new office roots, or hidden authority.

## 3. Next Tranche-Ready Structural Refinements

### 3.1 Add first-class office identity metadata

Add one small office metadata contract per office, for example under `offices/<office>/platform/contracts/`, with fields such as:

- `office_id`
- `office_role`
- `current_harness`
- `provider`
- `machine`
- `account_mode`
- `runtime_surface`
- `avatar_label`
- `promotion_scope`

This keeps path identity stable while making harness binding explicit and queryable.

### 3.2 Harden Ajna and Psyche as the first harness-specific offices

Ajna and Psyche carry the heaviest real harness particularity today. They should get the first deeper office-local physicalization:

- OpenClaw-specific contract files
- event/receipt/result templates that match the runtime and relay reality
- explicit office-local notes on what remains local versus what must promote into `runtime/` or `communications/`
- machine/account/auth binding captured as metadata instead of hidden in playbooks alone

Do not create a separate `openclaw/` office root. Harden the two existing offices.

### 3.3 Bring Adjudicator and Cartographer up to the Commander minimum

Commander already has office-local contract and template shape. The next tranche should give Adjudicator and Cartographer a minimum equivalent:

- local artifact-shape contract
- task/receipt/result/confirm templates
- office-specific anti-shadow-memory guidance

This closes the physicalization gap between constitutional equality and operational reality.

### 3.4 Add validator support for office/harness coherence

Add a validator that checks:

- every live office has the required substructure
- every office has an explicit metadata contract
- every office playbook points to a real office root
- harness bindings are declared in metadata rather than inferred from path names
- no stage0 surface accidentally acquires office-like authority without federal promotion

### 3.5 Keep provisional surfaces below the federal threshold

Do not create new federal offices for Manus, NotebookLM, Google AI Studio, OpenHands, Aider, Opencode, or similar surfaces yet.

Current evidence supports:

- playbook-level doctrine
- capability registry tracking
- adapter/operator experiments
- symbolic avatar handles only

No current repo evidence shows that these surfaces have earned constitutional office burden.

### 3.6 Optional but high-value refinement

Add a single federal registry artifact for office-to-harness bindings so the shell can answer:

- which office is currently bound to which harness
- which bindings are durable versus provisional
- when a binding changed
- whether the change was symbolic, runtime, or constitutional

This would reduce ambiguity without reopening the `offices/` versus `agents/` question.

## 4. Decision Summary

The next correct move is not more agent proliferation.
It is finishing the office/harness separation that the current shell already believes in:

- federal role stays at the office level
- native surface doctrine stays at the harness level
- symbolic continuity stays at the avatar level

That preserves institutional coherence while still allowing harness plurality and future rebinding.

## 5. `git diff --check`

`git diff --check` ran clean after writing this response.

## Status

`complete`

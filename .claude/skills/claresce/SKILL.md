---
name: claresce
description: "Clarescence — the culminating meta-operation for value-guided progressive refinement. Orient, situate, calibrate, then comprehensively and rigorously converge on the best path forward."
version: 2.0.0
user-invocable: true
---

# /claresce — Clarescence

You are invoking **clarescence**: the value-guided progressive refinement meta-operation
(Rosetta #169). This is the culmination of every operational insight accumulated across the
development of Syncrescendence — distilled into a procedure that comprehensively illuminates
a decision space until only one defensible path remains.

Clarescence is not brainstorming. It is not analysis paralysis. It is the disciplined act of
making something *clear that was not* — then committing the result as a verifiable artifact.

## Invocation

The user wants to claresce a decision, path, configuration, or strategic question. This means
running a structured multi-pass analysis that rigorously eliminates categories of blindness
until convergence is achieved.

**Arguments**: `$ARGUMENTS` — the topic to claresce (or infer from conversation context)

---

## Phase 0: Orient and Situate (MANDATORY)

Before any analysis, orient yourself to the current operational state and situate the
decision in its full context. Skipping this phase is the root cause of most wasted work.

### Orient

1. Read the Triumvirate: CLAUDE.md (already loaded), then read `README.md` and
   `orchestration/state/ARCH-INTENTION_COMPASS.md`
2. Run `git status` and `git log --oneline -5` — calibrate against ground truth
3. Scan `agents/commander/inbox/pending/` for pending tasks or completion signals
4. Note P0 intentions and pending SOVEREIGN decisions

### Situate

1. Identify the decision's **tier**: T0 (strategic) / T1a (repo-operational) / T1b (external-operational) / T2 (sprint) / T3 (session)
2. Map **dependencies**: What does this block? What blocks this?
3. Identify **affected agents**: Which Constellation members are impacted?
4. Search `orchestration/state/impl/clarescence/` for **prior clarescence** on this topic

### Gather Inputs

Collect or infer from context:
- **Topic**: What is being claresced
- **Current state**: Relevant files, drift, conflicts (read them — don't assume)
- **Options**: Available paths
- **Constraints**: Time, energy, cost, token budget, policies

---

## Fidelity Selection

Choose the depth of analysis based on blast radius:

| Fidelity | Passes | Criteria |
|----------|--------|----------|
| **Tactical** | 0 + 1–3 | Local decision, low blast radius, easily reversible |
| **Operational** | 0 + 1–7 | Cross-domain, moderate coupling, staged rollback possible |
| **Strategic** | 0 + 1–10 | Substrate-affecting, irreversible, architectural |

Default to **Tactical** unless the decision touches the substrate (σ-7), creates coupling
that survives session boundaries, or affects multiple agents.

---

## The 10-Pass Procedure

For each pass, write **1–5 bullets** (digestible). Expand only where the pass reveals conflict.

### Pass 1: Triumvirate Calibration

Calibrate the decision against strategic alignment:

- **Destination**: Does this move toward active intentions (INT-* vectors)?
- **Current state**: What does `git status` / `grep` / file reads actually confirm?
- **Fit verdict**: Does this close the gap or create a new one?

*If Pass 1 fails — the decision doesn't fit the destination — stop and reframe.*

### Pass 2: Lens Sweep (Dual-Path)

Run the decision through **both** lens batteries. Path 1 asks "is this wise?" Path 2
asks "is this well-built?" Both matter. Score each lens pass/fail.

**Path Selection**: Tactical = Path 2 only. Operational/Strategic = both paths.

#### Path 1: Wisdom Lenses (Strategic / Philosophical)

1. Bitter Lesson — relies on automation/scaling, not manual heroics?
2. Antifragile — stronger under stress, not merely robust?
3. Systems Thinking — accounts for holistic interdependence?
4. Potency Without Resolution Loss — preserves power while normalizing?
5. Syncrescendent Route — aligned with master convergence (Five Phases)?
6. Meet the Moment — timely for current conditions and maturity?
7. Steelman & Redteam — strongest version of both sides tested?
8. Personal Idiosyncrasies — respects Sovereign's unique capacities?
9. Elegance + Dev Happiness — beautiful AND satisfying to build?
10. First Principles — derived from fundamentals, not convention?
11. Complexity Theory — accounts for emergence, feedback, attractors?
12. Agentify — can be delegated to autonomous agent once proven?
13. Pareto 80/20 — maximum value from minimum effort?
14. Trade-off Explicit — all costs surfaced, nothing hidden?
15. Narrative Coherence — fits the story being told?
16. Compression — information density maximized?
17. Falsifiability — can be proven wrong?
18. Recursive Amplification — creates positive feedback loops?

**Path 1 Target**: >=12/18. Below 10/18 = strategically misaligned.

#### Path 2: Engineering Lenses (Operational / Structural)

1. Sovereignty — preserves optionality?
2. Portability — can we exit if needed?
3. Durability — survives session boundaries?
4. Reversibility — can we undo?
5. Atomicity — single coherent change?
6. Verifiability — provably worked?
7. Delegability — another agent can execute?
8. Composability — combines cleanly?
9. Observability — failure is detectable?
10. Token economy — context cost justified?
11. Energy sustainability — Sovereign can sustain?
12. Coupling risk — hidden dependencies?
13. Semantic clarity — terminology unambiguous?
14. Canon alignment — CANON supports this?
15. Tier coherence — strengthens tier coupling?
16. Agent compatibility — works with current Constellation?
17. Automation potential — automatable once proven?
18. Narrative fit — aligns with project identity?

**Path 2 Target**: >=12/18. Below 10/18 = needs reframing.
**Combined Target (Strategic)**: >=24/36.

### Pass 3: CANON Coherence

- What do canonical documents say about this domain?
- Where does reality diverge from CANON?
- **Action**: Flag stale CANON for update, or justify the contradiction.

*Tactical clarescence stops here unless escalated.*

### Pass 4: Omni-Qualities

- **Omniscience**: Better or worse at knowing its own state?
- **Omnipresence**: Better or worse reach across platforms?
- **Omnipotence**: Better or worse at autonomous action?
- **Omnibenevolence**: Better or worse alignment with Sovereign values?

### Pass 5: Five Faces

- **Sensing** (σ₀–σ₁): Perception improved?
- **Meaning** (σ₂–σ₃): Interpretation improved?
- **Intention** (σ₄): Aligned with declared intentions?
- **Embodiment** (σ₅–σ₆): Manifests in running systems?
- **Harmony** (σ₇): Integrates with the whole?

### Pass 6: Rosetta Precision

- All terms defined in REF-ROSETTA_STONE.md?
- Any semantic drift? Propose Rosetta updates if needed.

### Pass 7: Backlog Coherence

- What does this **unblock** in IMPLEMENTATION-MAP.md?
- What does it **create** or **invalidate**?
- Net impact on **T1a↔T2 coupling** health?

*Operational clarescence stops here unless escalated.*

### Pass 8: nth-Order Effects

- First order (direct), second order (cascade), third order (emergent)
- Compounding: positive synergy or interference with recent decisions?

### Pass 9: Energy State

- Sustainable now? Token cost? Opportunity cost?
- **If unsustainable**: Stage it with clear activation criteria.

### Pass 10: Authenticity Gate

The existential gate — not analytical but evaluative:

- Preserves sovereignty and optionality?
- Aligns with what the Sovereign *actually values*?
- Would the Sovereign at peak clarity approve this?
- **If no**: The analysis has drifted from values into optimization theater. Stop.

---

## Output

### Produce the Clarescence Record

Write to `orchestration/state/impl/clarescence/CLARESCENCE-YYYY-MM-DD-<slug>.md`:

```
CLARESCENCE: <topic>
Date: YYYY-MM-DD
Fidelity: tactical | operational | strategic
Passes run: 0+1-3 | 0+1-7 | 0+1-10
Convergent Path: <single best path, one sentence>
Rationale (digest): <3-7 bullets>
Dependencies created/updated: <IMPL-IDs, SYN-IDs>
Falsifier: <what would make this wrong>
Confidence: low | medium | high (with %)
Energy cost: <estimated tokens/time>
```

Use the full record template from `engine/REF-CLARESCENCE_RUNBOOK.md` for the body.

### If a Binding Decision Is Made

Produce a **DecisionAtom**:
- Decision statement (one sentence, unambiguous)
- Canonical truth surface (what becomes ground truth, where it lives)
- Reversibility + rollback path
- Falsifier + confidence level

### Update Backlog

- Adjust tasks in `IMPLEMENTATION-MAP.md` / `IMPLEMENTATION-BACKLOG.md`
- Append to `DYN-GLOBAL_LEDGER.md` with event `DECISION`
- Update T1a (Linear) if the decision affects tracked issues

---

## Epistemic Discipline

Every clarescence must include:

- **Confidence level**: High (>85%, multi-source verified) / Medium (60-85%, pattern-based) / Low (<60%, speculative)
- **Falsifier**: A concrete, testable condition that would invalidate the recommendation.
  Format: `If [condition], then [recommendation is wrong] because [reason]`
- **Verification**: Show the grep, show the git output, show the file read. "I checked" without
  evidence is verification theater.

---

## Anti-Patterns (PROHIBITED)

These have been meticulously cataloged across 20+ operational sessions:

| Anti-Pattern | Correction |
|---|---|
| **Elaboration over execution** | Every pass produces a decision or staged task, not more prose |
| **Aspiration masquerading as state** | Verify with grep/git, not memory |
| **Tier coupling blindness** | Pass 7 is mandatory — check cross-tier impact |
| **Semantic drift tolerance** | Fix terms in Pass 6 before proceeding |
| **Infinite refinement** | Set pass limit at start; escalate to Sovereign if stuck after Pass 3 |
| **Verification theater** | Show evidence, not claims |
| **Solo analysis of shared decisions** | Dispatch to affected agents if operational |

---

## Constitutional Constraints

The Five Invariants bind every clarescence. They cannot be suspended or traded:

1. **Objective Lock** — No work without confirmed objective
2. **Translation Layer** — Output intelligible without retransmission
3. **Receipts** — No completion without committed artifacts
4. **Continuation/Deletability** — Conversations are ephemeral; repo is durable
5. **Repo Sovereignty** — Repository is ground truth; platforms are cache

---

## Reference

Full runbook with templates and substrate triggers: `engine/REF-CLARESCENCE_RUNBOOK.md`

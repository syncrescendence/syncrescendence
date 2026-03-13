# Response

**Response ID**: `RSP-20260313-codex-campaign-11-lane-06-channel-portfolio-and-signal-policy-widening`  
**Surface**: `codex_parallel_session`  
**Date received**: `2026-03-13`  
**Dispatch packet**: `communications/prompts/PACKET-CODEX-CAMPAIGN-11-LANE-06-CHANNEL-PORTFOLIO-AND-SIGNAL-POLICY-WIDENING.md`  
**Result state**: `complete`  
**Receipt artifact**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-11-LANE-06-CHANNEL-PORTFOLIO-AND-SIGNAL-POLICY-WIDENING.md`

## Returned Content

The next widening should be policy-first, not count-first.

Acumen should not respond to the first full intelligence cycle by admitting a large new pile of channels. It should widen only when a source can be placed inside an explicit portfolio role, a bounded triage path, and a downstream consumption path that already exists in the cycle:

`registry -> poll -> triage -> product / verification -> repo-side assessment -> primary escalation when needed`

Anything that does not fit that chain cleanly should remain outside the active portfolio until the cycle can absorb it.

## 1. The Direct-Write Set

The next direct-write set should be small:

1. Create `orchestration/state/impl/ACUMEN-CHANNEL-PORTFOLIO-WIDENING-POLICY-v1.md`
   - define admission law for widening
   - define portfolio roles for channels
   - define what signal classes are allowed to stop at triage, move to verification, or require primary escalation
2. Create `orchestration/state/ACUMEN-CHANNEL-PORTFOLIO-REPORT.md`
   - derive a current portfolio view from `runtime/acumen/registry.json`
   - group channels by active role, not just by `priority_band`
   - show current `signal_density`, `visual_dependency`, `triage_hit_rate`, and recommended operating mode
3. Patch `operators/acumen/validate_registry.py`
   - tighten strict-mode warnings around widening-risk combinations
   - examples: low-density sources treated as full-priority core feeds, visually dependent sources routed as normal compression feeds, or low-yield sources left on aggressive cadence
4. Patch the Acumen poll / triage path only where needed to enforce policy
   - widening should be enforced through cadence ceilings, triage budgets, and routing limits
   - not through a second intake surface or an external scheduler becoming de facto authority

Important restraint:

- do not widen the registry schema first if the current fields already support the decision
- the current contract already exposes enough signal for first policy widening: `priority_band`, `signal_density`, `visual_dependency`, `cadence`, `default_compression`, `default_polish`, and `triage_hit_rate`

## 2. The Widened Portfolio Logic

The right move is to widen by portfolio role, not by raw channel count.

### A. Core monitored channels

These are the small set of feeds that deserve routine polling and normal triage participation.

Default profile:

- `priority_band`: `Tier 1` or strong `Tier 2`
- `signal_density`: `medium` or `high`
- `visual_dependency`: `none` or `low`
- `triage_hit_rate`: stable enough to justify recurring cost

Operating rule:

- full participation in the normal Acumen cycle
- eligible for `Headline`, `Compress`, `Promote`, and `Flag-for-Primary`
- routine contributors to `Dawn Brief` and downstream verification queue

### B. Selective monitored channels

These channels are worth watching, but not at the same operating cost as the core set.

Default profile:

- domain-relevant but lower-density feeds
- irregular or bursty channels
- sources with meaningful upside but inconsistent yield

Operating rule:

- poll on wider cadence or under narrower candidate windows
- prefer heuristic prefiltering before Gemini spend
- allow `Promote` and `Flag-for-Primary`, but do not assume routine brief inclusion

### C. Event-driven surge channels

These are dormant most of the time and become active around specific moments:

- major model or product releases
- hearings, policy actions, regulatory events
- notable guest appearances
- infrastructure incidents, benchmark controversies, or platform shifts

Operating rule:

- not part of steady-state baseline cost
- temporarily activated because the intelligence cycle has a reason to absorb them
- demoted back out when the event window closes

### D. Primary-only witness channels

Some channels should be in the portfolio without being treated as ordinary compression feeds.

Default profile:

- high visual dependency
- live debate or adversarial dynamics
- demos or teardowns where performance and interaction carry the signal
- material likely to matter only when a later assessment points back to the original

Operating rule:

- remain registry-known
- do not consume routine summarization budget as if they were ordinary talking-head feeds
- escalate mainly through `Flag-for-Primary` or assessment-linked source recovery

## 3. Signal Policy

The widening policy should separate three questions that are easy to collapse if left implicit.

### What deserves triage

An item deserves Acumen triage when at least one of the following is true:

- it comes from a core or selective monitored channel already inside the registry
- it contains novelty markers that could change interpretation: release, roadmap, architecture, capability claim, benchmark shift, policy action, or material guest crossover
- it touches one of the currently active intelligence domains the product family can actually consume

This preserves the intake boundary.
Acumen still decides what enters the machine. Augur, Perplexity, and later products do not nominate their own intake.

### What deserves verification

An item deserves downstream verification when:

- Acumen returns `Promote`
- multiple lesser items converge on the same claim or directional thesis
- the claim would change product positioning, competitive reading, or institutional judgment if true
- the claim is external-reality-sensitive enough that current-state checking matters

Verification remains downstream.
It is not a second intake pass over random widened feeds.

### What deserves primary escalation

Primary escalation should stay narrow and expensive.
It is justified when:

- Acumen returns `Flag-for-Primary`
- compression would destroy the signal
- repo-side assessment cannot safely resolve the item from secondary or near-primary witnesses
- the claim is visually dependent, interaction-dependent, or judgment-heavy
- the item could influence doctrine, major planning, or operator action if misunderstood

The key discipline is:

- not every interesting item deserves verification
- not every verified item deserves primary review
- widening fails when those boundaries blur

## 4. Compatibility With Sovereignty And Cost Guardrails

This widening is compatible with the current guardrails only if four rules remain explicit:

1. One intake plane
   - every widened source still enters through the Acumen registry and triage contract
   - no Augur packet, external search pass, or manual sidecar becomes a parallel intake authority
2. Cost follows role
   - core channels get routine spend
   - selective channels get bounded spend
   - event-driven channels get temporary spend
   - primary-only witnesses get near-zero routine spend until explicitly escalated
3. Verification stays downstream
   - `Promote` and tightly defined convergent-signal cases widen into verification
   - `Flag-for-Primary` remains a narrow exception, not a prestige label
4. Widening stays subordinate to the cycle
   - add only what existing products, assessment surfaces, and escalation paths can absorb
   - do not widen the portfolio faster than `Dawn Brief`, verification packets, repo-side assessment, and primary queue logic can metabolize it

## 5. Highest-Risk Widening Failure Modes

- channel-count widening without portfolio roles
  - this turns the registry into an undifferentiated heap and guarantees rising triage volume without sharper output quality
- priority drift becoming automatic spend
  - a channel marked important once can silently keep poll and model budget long after its observed yield collapses
- visual or adversarial sources being treated like ordinary compression feeds
  - this creates false confidence because the system appears to have processed the item while actually discarding the load-bearing signal
- downstream verification becoming shadow intake
  - once Augur or search-based passes start sourcing their own candidates, Acumen stops being the sovereign intake plane
- schema widening ahead of operating evidence
  - too many new registry fields create policy theater instead of operational discipline and make the cycle harder to audit
- widening beyond product absorption
  - if more channels enter than the current intelligence products and assessment path can metabolize, the result is source sediment rather than intelligence

## 6. Bottom Line

The next widening should not ask, "What else can Acumen watch?"

It should ask:

- which additional sources fit a defined portfolio role
- which of those roles justify recurring triage cost
- which signals can lawfully stop at Acumen
- which rare cases truly deserve verification or primary escalation

That keeps widening subordinate to the new intelligence cycle instead of letting source collection outrun intelligence production.

## 7. Status

`complete`

# Response

**Response ID**: `RSP-20260313-codex-campaign-12-lane-05-portfolio-policy-and-registry-enforcement`  
**Surface**: `codex_parallel_session`  
**Date received**: `2026-03-13`  
**Dispatch packet**: `communications/prompts/PACKET-CODEX-CAMPAIGN-12-LANE-05-PORTFOLIO-POLICY-AND-REGISTRY-ENFORCEMENT.md`  
**Result state**: `complete`  
**Receipt artifact**: `communications/responses/RESPONSE-CODEX-CAMPAIGN-12-LANE-05-PORTFOLIO-POLICY-AND-REGISTRY-ENFORCEMENT.md`

## Returned Content

The next widening should be governed by portfolio fit, source-of-truth feed capture, and chain role.
It should not be governed by "more channels means better coverage."

Every newly admitted source should satisfy all four tests before it increases steady-state load:

1. it comes from a curated inbound feed manifest captured for one of the five chain accounts
2. it has an explicit Acumen portfolio role
3. it has at least one lawful downstream consumer role in the chain ecology
4. it fits inside the present intelligence cycle's poll, triage, verification, and product budget

If a source fails any of those tests, it can remain manifest-known without entering the active registry.

## 1. The Direct-Write Set

1. Create `orchestration/state/impl/ACUMEN-PORTFOLIO-POLICY-AND-REGISTRY-ENFORCEMENT-v1.md`
   - define admission law from curated inbound manifests into `runtime/acumen/registry.json`
   - define allowed portfolio roles: `core_monitored`, `selective_monitored`, `event_surge`, `primary_only_witness`
   - bind those roles to chain consumers: Acumen intake, Coherence synthesis, Efficacy operations, Mastery curriculum, Transcendence meta-review
   - state explicitly that downstream chains do not create their own raw intake surfaces
2. Create `orchestration/state/ACUMEN-PORTFOLIO-REPORT.md`
   - derive from `runtime/acumen/registry.json`, poll status, and triage evidence
   - group channels by portfolio role, source account, and downstream chain relevance
   - report `priority_band`, `signal_density`, `visual_dependency`, `triage_hit_rate`, current cadence, and recommended enforcement action
   - include a widening budget line: how many additional feeds the current cycle can absorb without degrading Dawn Brief and verification quality
3. Patch `operators/acumen/validate_registry.py`
   - keep structural validation as-is, then add strict policy warnings for widening-risk combinations
   - fail strict mode when a low-yield channel is treated as routine core intake, when high-visual channels are routed as normal compression feeds, or when an unproven feed is placed on aggressive cadence
   - add a check that each admitted channel names a lawful source account and at least one downstream chain role
4. Patch `operators/acumen/poll_registry.py`
   - enforce cadence ceilings by portfolio role instead of trusting each row in isolation
   - cap routine polling for `selective_monitored` and `event_surge` feeds unless they are explicitly due
   - preserve one intake plane by refusing feeds that are not already present in the curated registry path

## 2. The Portfolio Logic

The registry should widen by role and by chain usefulness, not by raw count.

### Admission law

A feed enters the active registry only when it can be described as:

`captured source account -> Acumen portfolio role -> downstream chain consumer -> bounded cadence/budget`

That means the registry row is not just a channel description.
It is a commitment that the current cycle knows why the source exists and where its output can lawfully stop.

### Portfolio roles

#### A. `core_monitored`

Use for a small number of feeds that deserve routine Acumen polling because they regularly produce compressible or promotable signal.

Typical profile:

- `priority_band`: `Tier 1` or strong `Tier 2`
- `signal_density`: `medium` or `high`
- `visual_dependency`: `none` or `low`
- `triage_hit_rate`: already proven

Operating rule:

- Acumen may poll them on normal cadence
- they are eligible for `Headline`, `Compress`, `Promote`, or narrow `Flag-for-Primary`
- downstream consumers should already be known before admission

#### B. `selective_monitored`

Use for feeds that matter to one chain role but do not justify full steady-state cost.

Typical profile:

- domain-relevant but inconsistent yield
- narrower utility for Coherence, Efficacy, or Mastery
- plausible upside without routine Acumen prominence

Operating rule:

- default to wider cadence than core feeds
- require evidence of recurring yield before promotion
- should mostly stop at Acumen unless a real item is promoted

#### C. `event_surge`

Use for feeds that matter around launches, hearings, incidents, or temporary competitive windows.

Operating rule:

- remain registry-known but mostly dormant
- widen only for a declared event window
- return to low cadence or inactive status once the window closes

#### D. `primary_only_witness`

Use for sources where compression is often misleading.

Typical profile:

- high `visual_dependency`
- demos, debates, hearings, teardowns, adversarial exchanges
- items whose signal lives in interaction, tone, timing, or performance

Operating rule:

- do not spend routine summarization budget as if they were ordinary channels
- route mainly through `Flag-for-Primary`
- remain witness inventory, not steady-state compression inventory

### Chain-role binding

The five accounts should shape admission:

- `Acumen`: sovereign intake and triage plane for all admitted raw feeds
- `Coherence`: admit feeds whose output can become synthesis, frameworks, or cross-source integration
- `Efficacy`: admit feeds whose promoted items can affect operating decisions, tactics, execution, or portfolio moves
- `Mastery`: admit feeds whose yield is pedagogical, tutorial, or curriculum-bearing
- `Transcendence`: admit feeds whose value is meta, governance, identity, or long-horizon strategic reflection

A feed should not enter routine Acumen load just because one chain account follows it.
It should enter only if the chain role explains downstream use.

### Widening rule

Widening should start conservative:

- new feeds default to `selective_monitored` or `event_surge`, not `core_monitored`
- new feeds default to slower cadence until observed yield justifies more
- promotion into core status requires evidence from the current cycle, not narrative optimism

### Budget and cadence guardrails

The current cycle should stay metabolizable.
That implies:

- no widening that materially outruns current triage bandwidth
- no widening that turns verification into backlog sediment
- no widening that degrades Dawn Brief quality by flooding it with low-yield source activity

Practical enforcement:

- cap routine polling for unproven channels
- demote channels whose hit rate decays
- keep high-cost witness channels outside routine compression spend
- treat downstream verification as a narrow consequence of Acumen decisions, not a second discovery engine

## 3. Highest-Risk Widening Failure Modes

- `count-first widening`
  - the registry grows because more feeds feel like more coverage, but no role or downstream consumer is defined, so triage cost rises faster than intelligence yield
- `shadow intake surface`
  - Coherence, Efficacy, Mastery, Transcendence, or downstream verification start sourcing their own raw candidates, and Acumen stops being the sovereign intake plane
- `role laundering`
  - a feed is justified as useful for one later chain but is silently granted routine Acumen core polling without proving current-cycle yield
- `cadence inflation`
  - newly imported feeds inherit aggressive poll schedules before they earn them, causing load spikes that the cycle cannot metabolize
- `witness compression failure`
  - demos, live debates, or hearings are treated like ordinary commentary feeds, producing false confidence from lossy summaries
- `account ambiguity and duplicate authority`
  - the same source is captured under multiple chain accounts without a source-of-truth rule, causing duplicate intake or conflicting role assignments
- `verification becoming intake`
  - downstream research starts introducing novel raw sources rather than checking promoted claims, which breaks intake sovereignty and hides widening debt

## 4. Bottom Line

The portfolio should widen only when a curated inbound feed can be placed inside a lawful chain:

`source account -> Acumen role -> downstream chain consumer -> bounded cadence and budget`

That keeps policy first, keeps widening metabolizable, and prevents a shadow intake surface from forming behind the registry.

## Status

`complete`

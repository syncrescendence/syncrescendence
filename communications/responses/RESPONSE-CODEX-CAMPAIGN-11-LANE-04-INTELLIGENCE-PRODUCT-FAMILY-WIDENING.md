# Response

**Response ID**: `RSP-20260313-codex-campaign-11-lane-04-intelligence-product-family-widening`  
**Surface**: `codex_desktop`  
**Date**: `2026-03-13`  
**Dispatch packet**: [PACKET-CODEX-CAMPAIGN-11-LANE-04-INTELLIGENCE-PRODUCT-FAMILY-WIDENING.md](/Users/system/syncrescendence/communications/prompts/PACKET-CODEX-CAMPAIGN-11-LANE-04-INTELLIGENCE-PRODUCT-FAMILY-WIDENING.md)  
**Result state**: `complete`

## Direct-Write Set

The smallest lawful direct-write set is:

1. [ACUMEN-INTELLIGENCE-PRODUCT-FAMILY-CONTRACT-v1.md](/Users/system/syncrescendence/orchestration/state/impl/ACUMEN-INTELLIGENCE-PRODUCT-FAMILY-CONTRACT-v1.md)
   - defines the product family as a downstream rendering family, not a new authority family
   - states that ledgers, dossiers, Augur returns, and repo-side assessments remain upstream witness surfaces
2. `runtime/acumen/out/DAWN-BRIEF-YYYYMMDD.md`
   - existing triage-era awareness brief
   - remains compiled from [triage-decisions.jsonl](/Users/system/syncrescendence/runtime/acumen/triage-decisions.jsonl), which is itself rematerialized from the append-only Acumen ledgers
3. `runtime/acumen/out/VERIFIED-SIGNAL-BRIEF-YYYYMMDD.md`
   - new post-assessment brief
   - must compile from repo-side assessment artifacts after the existing chain `verification dossier -> Augur packet -> Augur return -> repo-side assessment`
4. `orchestration/state/ACUMEN-PRIMARY-SOURCE-QUEUE.json`
   - authoritative queue state for unresolved items that require direct source acquisition or original-form review
5. `runtime/acumen/out/PRIMARY-SOURCE-QUEUE-READOUT-YYYYMMDD.md`
   - human-readable readout of the queue above
   - operational readout only; it does not decide what enters or leaves the queue

That is enough widening for the first full cycle. It adds two new downstream products and one explicit queue state, without inventing a parallel intelligence stack.

## New Product Family

The truthful family should be three products, not more:

| Product | State placement | Intended consumers | Lawful role |
| --- | --- | --- | --- |
| `Dawn Brief` | `runtime/acumen/out/DAWN-BRIEF-*.md` downstream of [triage-decisions.jsonl](/Users/system/syncrescendence/runtime/acumen/triage-decisions.jsonl) and the Acumen evidence ledgers | operator, daily scan, tactical awareness consumer | pre-verification awareness after intake and triage |
| `Verified Signal Brief` | `runtime/acumen/out/VERIFIED-SIGNAL-BRIEF-*.md` downstream of verification dossier, Augur return, and repo-side assessment | decision-maker, research planner, higher-order synthesis surface | post-verification summary with explicit `verified fact`, `inference`, and `remaining gaps` sections |
| `Primary-Source Queue Readout` | `runtime/acumen/out/PRIMARY-SOURCE-QUEUE-READOUT-*.md` downstream of `orchestration/state/ACUMEN-PRIMARY-SOURCE-QUEUE.json` | primary-source researcher, analyst, operator doing next witness pulls | action-oriented queue visibility after assessment identifies unresolved or high-value follow-up |

## Naming And State Placement

The naming rule should follow the intelligence state, not the rendering mechanism:

1. `Dawn Brief` = triage state
2. `Verified Signal Brief` = assessment state
3. `Primary-Source Queue Readout` = escalation state

That placement keeps authority explicit:

1. evidence and decision authority stay in [acumen-triage-decision-ledger.jsonl](/Users/system/syncrescendence/orchestration/state/registry/acumen-triage-decision-ledger.jsonl), [acumen-training-corpus-ledger.jsonl](/Users/system/syncrescendence/orchestration/state/registry/acumen-training-corpus-ledger.jsonl), and the rematerialized current-state views
2. verification bridge authority stays in [verification-dossiers](/Users/system/syncrescendence/runtime/acumen/out/verification-dossiers), the Augur packet surface, and the Augur return surface
3. assessment authority should stay in repo-side assessment artifacts, not be silently absorbed into a brief
4. briefs remain derivative renderings only

This is the key guardrail: no product in the family may read directly as if it were the source of truth. Each one renders a prior lawful state.

## What Still Remains Future-Facing

Three things should stay future-facing for now:

1. A separate `Verification-Ready Brief` should not be added yet. The verification dossier plus Augur packet family already covers that state, and adding a second human-facing pre-verification brief would duplicate authority without adding a new cycle stage.
2. Executive, weekly, or channel-specific rollups should wait. The first widening should prove the daily cycle first, not explode into a portfolio of stylistic variants.
3. Final doctrine or ratified strategic synthesis should remain outside this family. The `Verified Signal Brief` is still an assessed signal product, not constitutional truth and not the terminal research artifact.

## Bottom Line

Acumen should widen from one product to three:

1. `Dawn Brief` for triage-era awareness
2. `Verified Signal Brief` for post-verification assessed signal
3. `Primary-Source Queue Readout` for unresolved direct-source follow-up

That is the smallest product family that actually reflects the first full intelligence cycle:

`intake -> triage -> verification bridge -> Augur return -> repo-side assessment -> primary-source escalation`

Anything broader right now is speculative breadth. Anything narrower leaves the cycle invisible after triage.

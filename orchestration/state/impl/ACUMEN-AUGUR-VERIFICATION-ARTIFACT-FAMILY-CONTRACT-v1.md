# Acumen Augur Verification Artifact Family Contract v1

**Status**: staged
**Class**: implementation law
**Purpose**: define the first lawful post-triage artifact family that routes promoted or flagged Acumen items into Augur / Perplexity verification without violating repo sovereignty

## Why This Family Exists

Acumen now has a real intake and triage path.
That creates a narrow follow-on need:

- some items deserve external reconnaissance after triage
- those items need a reusable verification input
- Augur must remain downstream of triage rather than entering the intake path

This family satisfies that need with one bounded rule:

`Acumen intake -> Acumen triage -> promoted or flagged item -> verification dossier -> Augur packet -> cited response -> repo-side assessment -> primary-source queue`

## Placement Law

Perplexity / Augur is not part of Acumen intake.
It is not part of the triage classifier.
It is a downstream verification and reconnaissance surface that activates only after Acumen has already decided an item is worth more attention.

That means the lawful eligible states are:

- `Promote`
- `Flag-for-Primary`

The following states do not emit Augur artifacts by default:

- `Skip`
- `Headline`
- `Compress`

## Surfaces

Runtime dossier surface:

1. `runtime/acumen/out/verification-dossiers/*.json`

Dispatch surface:

1. `communications/prompts/PACKET-PERPLEXITY-acumen-*.md`

Return surface:

1. `communications/responses/RESPONSE-PERPLEXITY-acumen-*.md`

Bridge state surface:

1. `orchestration/state/ACUMEN-AUGUR-VERIFICATION-BRIDGE.json`

Generation helper:

1. `operators/acumen/build_verification_bridge.py`

Validation helper:

1. `operators/validators/validate_acumen_verification_bridge.py`

Downstream continuation:

1. `orchestration/state/impl/ACUMEN-AUGUR-RETURN-INGESTION-CONTRACT-v1.md`

## Dossier Law

The dossier is a repo-local input artifact.
It preserves:

- the Acumen decision record
- source-video identity and bounded metadata
- triage packet provenance when available
- the exact verification mission handed to Augur

It does not preserve:

- secrets
- hidden provider state
- raw private prompts beyond the already lawful triage provenance
- claims that Augur is authoritative on repo-local state

## Packet Law

The Augur packet must ask for:

- reconnaissance
- source discovery
- current-reality verification
- disconfirming or complicating evidence
- primary or near-primary witness finding

The Augur packet must not ask for:

- final drafting
- constitutional ratification
- repo-state adjudication
- polished doctrine authorship

The return is a verification input.
It is not a final brief.

## Repo Sovereignty Rule

Repo-local Acumen artifacts remain authoritative for:

- the existence of the item
- the triage decision that elevated it
- the packet provenance emitted by the runtime

Augur may verify only external reality:

- whether the implied topic or claim is current
- which official or primary sources matter
- what corroborating or disconfirming evidence exists
- what stronger reasoning surfaces should inspect next

Augur may not overrule repo state, rewrite Acumen history, or become the hidden source of truth.

## Output Contract

The returned response should remain reconnaissance-first.
It should emphasize:

1. source terrain
2. current-reality checks
3. disconfirming or complicating evidence
4. highest-value follow-up witnesses
5. confidence and unresolved gaps

That structure keeps Augur in its lawful role as cited witness-set generator rather than final drafter.

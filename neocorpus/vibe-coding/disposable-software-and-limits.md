# Disposable Software and the Limits of Vibe Coding
> Software cost collapsed but attention cost did not — the disposable software discourse gets it wrong by conflating developer-facing tools (Cursor philosophy: ship fast, tolerate variance) with enterprise reliability markets where customers pay to not have to think.

## Sources
10166.md, 02836.jsonl, 09857.md, 03487.jsonl, 03412.jsonl, 01645.jsonl, 03103.jsonl, 04171.jsonl, 03763.jsonl, 03765.md, 10672.md

## Two Phenomena Sharing One Name
Nate B Jones identified the core confusion: "disposable software" conflates two completely different phenomena (10166.md).

**Developer-facing disposable software** (Cursor philosophy): code is reality, ship multiple times a day, tolerance for variance. This works because the customers are developers who understand and accept breakage.

**Enterprise reliability software** (Salesforce model): customers buy reliability — something they do not have to think about. This is not a temporary gap. It is a fundamental difference in what customers pay for (10166.md).

The claim that vibe coding will replace enterprise SaaS is wrong (02836.jsonl). Complex apps still require real engineering (03487.jsonl). The "Software is Dead" narrative fails when applied beyond prototypes and internal tools.

## Attention as the True Constraint
When software becomes cheap to build, the bottleneck shifts to attention, not production. Code cost collapsed; attention cost did not (10166.md). 95% of the market needs a completely different strategy than "ship like Cursor." Enterprise builders should earn the right to deploy proactive AI that creates value customers did not know they were missing, rather than trying to imitate developer-tool shipping cadence (10166.md).

## Frontend Engineering Collapse
The front-end engineering paradigm is shifting (09857.md). Hand-implementing pages is collapsing into cheap, repeatable work. The job moves from ticket-taker to system designer. Composability replaces implementation. AI agents become 99% of a tool's consumers in some contexts. The "$500K mistake": 8 engineers doing implementation, 0 doing governance.

Mental model shifts required: from data schemas to screens, from pixels to brand promises, from design patterns to workflows, from static access controls to dynamic role-based UIs for AI consumers (09857.md).

## Where Vibe Coding Fails Structurally
Multiple sources converge on failure modes:

- **Frontend intent translation**: coding agents are inefficient at frontend work because translating user intent to visual UI is hard — the gap between "what I want it to look like" and "what the code produces" is where most tokens burn (03412.jsonl).
- **Production codebases**: AI coding tools struggle with real production codebases at scale (01645.jsonl).
- **Rewriting economics**: when AI makes rewriting cheap, the incentive to rely on opaque dependencies collapses — you can rewrite rather than maintain, but this creates its own problems with testing and reliability (04171.jsonl).
- **Code scaffolding obsolescence**: LLMs make existing scaffolding obsolete, requiring frequent deletion rather than maintenance (03103.jsonl).

## The Nuance Nobody Wants
Vibe coding is not simply a hustle opportunity or a developer threat (03763.jsonl, 03765.md, 10672.md). The two failure modes that trip up most new vibe coders: (1) treating it as a get-rich-quick scheme without domain understanding, and (2) treating it as an existential threat without understanding where it actually adds value.

The valuable skill is not coding anymore — it is specification (10672.md). "Software vision" — seeing software-shaped problems in the world — is what separates successful vibe coders from the 90% who fail. That gap closes faster than learning to program from scratch, but it still requires genuine domain expertise (10672.md).

## Antipatterns & Lessons
- **Applying developer-tool philosophy to enterprise markets**: Cursor's shipping speed works for developers. CIOs buying Salesforce need reliability guarantees, not faster deploys (10166.md).
- **"Disposable software" as universal strategy**: works for personal projects and internal tools; breaks when attention cost, security, and user trust matter (10166.md).
- **Ignoring the governance gap**: spending engineering resources on implementation while neglecting governance, auditability, and row-level security for dynamic UIs (09857.md).

## Cross-References
- neocorpus/vibe-coding/definition-and-eras.md (the graduation path from vibe to engineering)
- neocorpus/vibe-coding/dark-flow-and-metr-study.md (why builders overestimate vibe-coded quality)
- neocorpus/vibe-coding/engineer-vs-vibe-coder.md (the skills that survive)

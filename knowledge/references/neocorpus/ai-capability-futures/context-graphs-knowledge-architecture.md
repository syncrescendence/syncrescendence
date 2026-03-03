# Context Graphs & Knowledge Architecture

> A context graph is the institutional memory of "the why" behind decisions — captured through decision traces, the sequence of steps and human reasoning that AI models typically miss. If knowledge graphs store what is known, context graphs store why it was decided.

## Sources
- `corpus/ai-capability-futures/03519.md` — 3 atoms: Context graphs (Latent Space podcast, Jaya Gupta & Ashu Garg). Definition of context graph as decision trace architecture, prediction of context graphs as defensible moat for applied AI, prediction of "Context Graph Stack" emerging at production scale in 2026.

## Core Concept

A "context graph" is a framework defined as the institutional memory of "the why" behind business decisions, captured through "decision traces" — the sequence of steps and human reasoning that AI models often miss. Where a knowledge graph represents entities and their relationships (static facts), a context graph represents the reasoning processes that produced decisions (dynamic rationale).

The decision trace is the key primitive: not just "we chose Vendor X" but "we evaluated Vendors X, Y, Z against criteria A, B, C; X scored highest on A which we weighted 3x because of incident Q last quarter; the decision was approved by P with the caveat that we re-evaluate in 6 months." The trace preserves the context that makes the decision interpretable, auditable, and revisable.

## Strategic Claims

**Defensible moat**: Context graphs will become the defensible moat for the next generation of applied AI companies and systems of agents. The argument: AI models can be replicated, data can be commoditized, but the accumulated decision rationale of an organization — the institutional "why" — is proprietary, path-dependent, and extremely difficult to reconstruct. Companies that capture decision traces build compounding advantage.

**Production scale in 2026**: The "Context Graph Stack" will emerge and scale to production in 2026. This is a timing prediction with high speculation risk.

## Architectural Significance

Context graphs address a specific failure mode of current AI systems: they can retrieve relevant information (RAG) and reason about it (chain-of-thought), but they cannot access the organizational reasoning that produced the information's current form. An AI assistant can find the procurement policy but cannot explain why it was written that way, what it replaced, or what failure it was designed to prevent.

This connects directly to the Palantir Ontology's concept of "institutional epistemology" — the organization's formal model of what it knows and why. The context graph is the temporal/causal dimension that static ontologies lack: not just "what exists" but "why it came to exist this way."

## Limitations

The source material is thin — 3 atoms from a podcast description. The concept is named and predicted but not architecturally specified. Key open questions not addressed by the source:
- How are decision traces captured? (Manual logging? Automated instrumentation? AI observation?)
- What is the data model? (Graph with decision nodes and rationale edges? Temporal knowledge graph? Something novel?)
- How does retrieval work? (When an agent needs the "why" behind a decision, how does it query the context graph?)
- What distinguishes this from existing provenance/lineage tracking?

The concept is promising but the corpus currently contains only the naming and the prediction, not the substance.

## Cross-References
- neocorpus/infrastructure/palantir-ontology-enterprise-semantic-layer (static ontology that context graphs extend temporally)
- neocorpus/productivity-pkm/agent-native-tools-for-thought (decision traces as agent memory architecture)

# Direct Design: Code as the Primary Creative Medium

## Sources

| ID | Title | Origin |
|----|-------|---------|
| 00169 | The Design Vibeshift | Pablo Stanley, Substack / X (Feb 2026) |
| 00267 | The Future of Design is Direct Design | Alex Kehr, X (Feb 11, 2026) |
| 03562 | Atoms from Design Vibeshift | SOURCE-20260205-014 |
| 03564 | Extraction: Design Vibeshift | SOURCE-20260205-014 |
| 03838 | Atoms from Direct Design | SOURCE-20260211-001 |
| 03840 | Extraction: Direct Design | SOURCE-20260211-001 |
| 04246 | Figma Claude Code import | SOURCE-20260217-022 |
| 10939 | OpenEditor Thread — Dami Dina | X, Feb 17, 2026 |

---

## Core Thesis

A paradigm shift is underway in product design: code is displacing the design canvas as the primary medium of creative work. This is not a tooling preference — it is a structural change in who builds what, when, and with what fidelity. The key mechanism is elimination of the handoff, the thirty-year bottleneck at the center of every design-to-engineering workflow. When the person who holds the product vision is also the person executing it in a living, running system, a translation layer that consumed weeks of iteration and delivered 80% of the intended vision simply ceases to exist.

This paradigm is best named **Direct Design** (00267): the process that occurs when the translation layer between designer intent and product reality is removed. It is distinguished sharply from *vibe coding* — undisciplined prompt-throwing that produces shaky output — by its rigor: the Direct Designer holds the entire product context simultaneously (user problem, interaction model, edge cases, business logic, feel) and makes real-time decisions with a working version in front of them (00267, 03838).

The aphorism that crystallizes the paradigm: **Taste now has a compiler** (00267).

---

## Key Frameworks

### The Handoff as the Structural Root Cause

The prior paradigm had a well-documented anatomy: designer thinks about a problem, makes a picture of the solution in a design tool, writes a spec explaining what they meant, hands it to an engineer who interprets that spec, builds something close but not quite right, and everyone iterates for weeks until it ships at ~80% of the original vision (00267, 03838).

The entire field of design systems exists as a response to this gap — elaborate component libraries and documentation built to solve a communication problem between two people sitting ten feet apart (00267, 03840). The diagnosis is precise: **the handoff was always the problem. It was never the design.** (00267)

Atlassian's institutional response — renaming the relationship "Handoffs into Handshakes" — frames this correctly: the goal is not to replace tools but to collapse the gap between designing and building (00169, 03562). The framing signals that the problem is structural, not technological.

### Direct Design vs. Vibe Coding: A Critical Distinction

The conflation of Direct Design with vibe coding is the most important distinction in the entire discourse, and 00267 makes it explicitly.

**Vibe coding**: Throw a prompt at an AI, hope for the best. Build without thinking. The Cursor CEO himself called this "shaky foundations" (00267, 03838). It is the abdication of craft in favor of generation.

**Direct Design**: The opposite. Rigorous. The practitioner describes not just what a product should look like, but what it should *do*, how it should *feel*, who it's *for* — then shapes a living product in real time as it comes to life (00267). It requires holding the entire product in mind: user problem, interaction model, edge cases, business logic, the feel. That is not less disciplined than the old process — it is more (00267, 03840).

The operative contrast: in Figma, you are *guessing* how it will feel when an engineer builds it. In Direct Design, you are *experiencing* it (00267). The feedback loop collapses from weeks to hours or minutes. Things you would never catch in a mockup surface immediately because you are encountering the actual artifact (00267, 03838).

### The Source-of-Truth Migration

The displacement of Figma is not about Figma being a bad tool. It is about Figma being the wrong kind of artifact at the center of a workflow that has moved.

Three practitioners articulate the same insight from different angles:

**Adam Whitcroft** (00169, 03562): Figma's role as the source of truth for design is numbered. Its surviving use case is initial direction-setting and mood exploration — not maintaining monolithic product files.

**Darrin Henein** (00169, 03562): Design systems will migrate from Figma into GitHub — becoming codified, version-controlled, branchable, and machine-consumable. The canonical definition of a product moves from the design tool into the product itself.

**Hardik Pandya, Head of Design, Atlassian** (00169, 03562): After six months in Cursor, it is hard to go back to designing on canvas. Advantages: real-time behavior, responsiveness, live data, micro-interactions, no manual duplication for states. His stronger claim: Figma is rapidly becoming a significant bottleneck in product development.

The convergence of these three: **code is the source of truth** (00169). The Figma file is a snapshot, not an authority.

### The Workflow Loop: Idea → Code → Shipped

The emergent pattern across practitioner reports is a hybrid loop: **Idea → Code → Shipped** (00169, 03562). Code enables quicker iteration for complex screens and interactions — animations, live data, micro-states, edge cases that a static design tool forces you to either painstakingly mock up or simply skip. What you are "too lazy to design" in Figma you encounter automatically in code (00169).

One practitioner's concrete workflow: Figma wireframe (using actual system components) becomes the initial prompt — it communicates structure without requiring descriptive prose. From there, all finalized UI/UX work happens in code (00169). The Figma artifact is a launching pad, not the destination.

Mobile-specific note: vibe-coding from scratch performs better than forcing Figma fidelity into frameworks like React Native, where the design tool's assumptions don't map (00169).

### Taste as a Directly Executable Property

The deeper philosophical claim: the value of a great designer was never in drawing rectangles. It was always in knowing *what to build and why* — product taste, user instinct, the ability to hold complexity and make it simple (00267, 03840).

That skill is now directly executable. Taste has a compiler.

The implication is that the prior workflow forced a roundtrip through an interpreter — the engineer — who re-expressed the designer's intent with their own signal loss. Direct Design eliminates the interpreter. The person with taste is now the person with the commit.

This reframes the role trajectory: eliminating the translation layer pushes design toward strategy. Which is what the best designers have always wanted — a seat at the table where the real decisions happen (00169, 03562). The tool change is a surface effect of a deeper power-structure shift.

### The Figma Countermove: Bidirectional Integration

Figma's response is not to ignore the shift. Figma Make converts designs into working prototypes with AI. More telling is the Claude Code → Figma import feature (04246): UI work created in Claude Code can be imported directly into Figma as editable design frames, enabling exploration of new design ideas, visualization of multi-page flows on the canvas, or reimagination of user experiences.

This bidirectionality is significant: it acknowledges that code is now primary, and that design tools should serve the code workflow rather than anchor it. The direction of import has inverted.

### OpenEditor: The Figma-Like Canvas for Code

OpenEditor (10939) represents a third path — not "do Figma" and not "do code-only" but bring the bird's-eye canvas view to code-first workflows. A performant desktop app that enables viewing an application across breakpoints, states, and environments in real time. A config file maps routes and states to previews.

The design instinct driving OpenEditor is legible: what designers valued in Figma was spatial overview and instant feedback on variations. OpenEditor delivers that for code-native work, without requiring the detour through a design file. It is tooling built in the image of the new paradigm rather than the old one.

### The Counterargument: Systemic Coherence Risk

The honest treatment requires the counterargument. If everyone is shipping directly to code, who is maintaining the bigger picture? Consistency across screens? The design system as a whole? (00169, 03562)

This is not a trivial objection. The risk is a fragmentation where individual screens are well-crafted but the system loses coherence — the problem design systems were invented to solve, now potentially replicated at a higher level of abstraction.

The pragmatist position (00169): Figma for core screens, code for the rest. Some designers maintain Figma for exploration, alignment, detail work like components and consistency. Rogie (Figma product designer): "Do both — vibe coding is incredible for communicating designs faster, but nothing is replacing iterating by duplicating and riffing and exploring the solution space." (00169, 03562)

Greg Huntoon's workflow formalizes the roundtrip: Figma Design → code → copy designs back to Figma, with GPT-cleaned prompts and Cursor/VSCode CoPilot throughout (00169, 03562). The question becomes what cadence of synchronization between the two worlds is sustainable at scale.

### Why Immediate Feedback Wins Attention

The attention gravity of Direct Design tools is not about perfection. It is about the feedback loop:

> "When I describe something to v0 or Claude Code and see it running in my browser thirty seconds later, that's different from pushing pixels and then waiting for a developer to interpret my intent. The design IS the code. There's no translation layer." (00169)

Tools that enable idea to shipped product in the same conversation win attention not because they produce better code than engineers, but because the latency between intention and experience collapses (00169, 00267). This is the decisive experiential difference. The iteration cycle that previously required scheduling, handoff documentation, and developer availability now requires only typing.

---

## Synthesis: What Is Actually Shifting

Three things are shifting simultaneously, and they reinforce each other:

1. **The locus of authority**: from the design file (Figma) to the running product (the codebase). Version control, branchability, and machine-consumability accrue to whoever holds the source of truth.

2. **The role of the designer**: from specification-writer and visual-mockup-producer to direct product executor. The skill is unchanged — taste, instinct, complexity-reduction — but the medium through which that skill operates is now code rather than canvas.

3. **The meaning of "done"**: from "approved in Figma" to "shipped." The intermediate artifact (the design file) loses its status as a deliverable and becomes at most a communication tool or exploration space.

We spent decades trying to teach engineers to think like product people. It turned out it was easier to give product people the ability to ship (00267). The paradigm shift is that asymmetric.

---

## Current State (Early 2026)

The discourse is not at "Figma is dead." It is at "Figma is no longer central." The transition is active and uneven — practitioners with different workflows, team structures, and product types are at different points on the adoption curve. The hybrid modes (Figma for ideation/alignment, code for execution; Figma for core screens, code for the rest; Figma as wireframe input to LLM prompt) reflect genuine contextual adaptation rather than confusion or resistance.

The signal that distinguishes this from an ordinary tool transition: the artifacts being shared have changed. The designer's feed no longer shows "here's a design I made" — it shows "here's something I shipped this afternoon" (00169). The output has changed identity. That is a paradigm shift, not a preference update.

# Direct Design: Code as the Primary Creative Medium

---

## Core Thesis

A paradigm shift is underway in product design: code is displacing the design canvas as the primary medium of creative work. This is not a tooling preference -- it is a structural change in who builds what, when, and with what fidelity. The key mechanism is elimination of the handoff, the thirty-year bottleneck at the center of every design-to-engineering workflow. When the person who holds the product vision is also the person executing it in a living, running system, a translation layer that consumed weeks of iteration and delivered 80% of the intended vision simply ceases to exist.

This paradigm is best named **Direct Design**: the process that occurs when the translation layer between designer intent and product reality is removed. It is distinguished sharply from *vibe coding* -- undisciplined prompt-throwing that produces shaky output -- by its rigor: the Direct Designer holds the entire product context simultaneously (user problem, interaction model, edge cases, business logic, feel) and makes real-time decisions with a working version in front of them.

The aphorism that crystallizes the paradigm: **Taste now has a compiler.**

---

## Key Frameworks

### The Handoff as the Structural Root Cause

The prior paradigm had a well-documented anatomy: designer thinks about a problem, makes a picture of the solution in a design tool, writes a spec explaining what they meant, hands it to an engineer who interprets that spec, builds something close but not quite right, and everyone iterates for weeks until it ships at approximately 80% of the original vision.

The entire field of design systems exists as a response to this gap -- elaborate component libraries and documentation built to solve a communication problem between two people sitting ten feet apart. The diagnosis is precise: the handoff was always the problem. It was never the design.

Atlassian's institutional response -- renaming the relationship "Handoffs into Handshakes" -- frames this correctly: the goal is not to replace tools but to collapse the gap between designing and building.

### Direct Design vs. Vibe Coding: A Critical Distinction

The conflation of Direct Design with vibe coding is the most important distinction in the entire discourse.

**Vibe coding**: Throw a prompt at an AI, hope for the best. Build without thinking. The Cursor CEO himself called this "shaky foundations." It is the abdication of craft in favor of generation.

**Direct Design**: The opposite. Rigorous. The practitioner describes not just what a product should look like, but what it should do, how it should feel, who it is for -- then shapes a living product in real time as it comes to life. It requires holding the entire product in mind: user problem, interaction model, edge cases, business logic, the feel. That is not less disciplined than the old process -- it is more.

The operative contrast: in Figma, you are guessing how it will feel when an engineer builds it. In Direct Design, you are experiencing it. The feedback loop collapses from weeks to hours or minutes. Things you would never catch in a mockup surface immediately because you are encountering the actual artifact.

### The Source-of-Truth Migration

The displacement of Figma is not about Figma being a bad tool. It is about Figma being the wrong kind of artifact at the center of a workflow that has moved.

Figma's role as the source of truth for design is numbered. Its surviving use case is initial direction-setting and mood exploration -- not maintaining monolithic product files. Design systems will migrate from Figma into GitHub -- becoming codified, version-controlled, branchable, and machine-consumable. The canonical definition of a product moves from the design tool into the product itself.

After six months in Cursor, the Head of Design at Atlassian finds it hard to go back to designing on canvas. Advantages: real-time behavior, responsiveness, live data, micro-interactions, no manual duplication for states. The stronger claim: Figma is rapidly becoming a significant bottleneck in product development.

The convergence: code is the source of truth. The Figma file is a snapshot, not an authority.

### The Workflow Loop: Idea -> Code -> Shipped

The emergent pattern across practitioner reports is a hybrid loop: Idea -> Code -> Shipped. Code enables quicker iteration for complex screens and interactions -- animations, live data, micro-states, edge cases that a static design tool forces you to either painstakingly mock up or simply skip. What you are "too lazy to design" in Figma you encounter automatically in code.

One practitioner's concrete workflow: Figma wireframe (using actual system components) becomes the initial prompt -- it communicates structure without requiring descriptive prose. From there, all finalized UI/UX work happens in code. The Figma artifact is a launching pad, not the destination.

Mobile-specific note: vibe-coding from scratch performs better than forcing Figma fidelity into frameworks like React Native, where the design tool's assumptions do not map.

### Taste as a Directly Executable Property

The deeper philosophical claim: the value of a great designer was never in drawing rectangles. It was always in knowing what to build and why -- product taste, user instinct, the ability to hold complexity and make it simple.

That skill is now directly executable. Taste has a compiler.

The implication is that the prior workflow forced a roundtrip through an interpreter -- the engineer -- who re-expressed the designer's intent with their own signal loss. Direct Design eliminates the interpreter. The person with taste is now the person with the commit.

This reframes the role trajectory: eliminating the translation layer pushes design toward strategy. Which is what the best designers have always wanted -- a seat at the table where the real decisions happen. The tool change is a surface effect of a deeper power-structure shift.

We spent decades trying to teach engineers to think like product people. It turned out it was easier to give product people the ability to ship. The paradigm shift is that asymmetric.

### The Figma Countermove: Bidirectional Integration

Figma's response is not to ignore the shift. Figma Make converts designs into working prototypes with AI. More telling is the Claude Code to Figma import feature: UI work created in Claude Code can be imported directly into Figma as editable design frames, enabling exploration of new design ideas, visualization of multi-page flows on the canvas, or reimagination of user experiences.

This bidirectionality is significant: it acknowledges that code is now primary, and that design tools should serve the code workflow rather than anchor it. The direction of import has inverted.

### OpenEditor: The Figma-Like Canvas for Code

OpenEditor represents a third path -- not "do Figma" and not "do code-only" but bring the bird's-eye canvas view to code-first workflows. A performant desktop app that enables viewing an application across breakpoints, states, and environments in real time. A config file maps routes and states to previews.

The design instinct driving OpenEditor is legible: what designers valued in Figma was spatial overview and instant feedback on variations. OpenEditor delivers that for code-native work, without requiring the detour through a design file. It is tooling built in the image of the new paradigm rather than the old one.

### The Counterargument: Systemic Coherence Risk

The honest treatment requires the counterargument. If everyone is shipping directly to code, who is maintaining the bigger picture? Consistency across screens? The design system as a whole?

This is not a trivial objection. The risk is fragmentation where individual screens are well-crafted but the system loses coherence -- the problem design systems were invented to solve, now potentially replicated at a higher level of abstraction.

The pragmatist position: Figma for core screens, code for the rest. Some designers maintain Figma for exploration, alignment, detail work like components and consistency.

> "Do both -- vibe coding is incredible for communicating designs faster, but nothing is replacing iterating by duplicating and riffing and exploring the solution space."

The question becomes what cadence of synchronization between the two worlds is sustainable at scale. Greg Huntoon's workflow formalizes the roundtrip: Figma Design -> code -> copy designs back to Figma, with GPT-cleaned prompts and Cursor/VSCode CoPilot throughout.

### Why Immediate Feedback Wins Attention

The attention gravity of Direct Design tools is not about perfection. It is about the feedback loop:

> "When I describe something to v0 or Claude Code and see it running in my browser thirty seconds later, that's different from pushing pixels and then waiting for a developer to interpret my intent. The design IS the code. There's no translation layer."

Tools that enable idea to shipped product in the same conversation win attention not because they produce better code than engineers, but because the latency between intention and experience collapses. This is the decisive experiential difference. The iteration cycle that previously required scheduling, handoff documentation, and developer availability now requires only typing.

---

## Synthesis: What Is Actually Shifting

Three things are shifting simultaneously, and they reinforce each other:

1. **The locus of authority**: from the design file (Figma) to the running product (the codebase). Version control, branchability, and machine-consumability accrue to whoever holds the source of truth.

2. **The role of the designer**: from specification-writer and visual-mockup-producer to direct product executor. The skill is unchanged -- taste, instinct, complexity-reduction -- but the medium through which that skill operates is now code rather than canvas.

3. **The meaning of "done"**: from "approved in Figma" to "shipped." The intermediate artifact (the design file) loses its status as a deliverable and becomes at most a communication tool or exploration space.

---

## Current State (Early 2026)

The discourse is not at "Figma is dead." It is at "Figma is no longer central." The transition is active and uneven -- practitioners with different workflows, team structures, and product types are at different points on the adoption curve. The hybrid modes (Figma for ideation/alignment, code for execution; Figma for core screens, code for the rest; Figma as wireframe input to LLM prompt) reflect genuine contextual adaptation rather than confusion or resistance.

The signal that distinguishes this from an ordinary tool transition: the artifacts being shared have changed. The designer's feed no longer shows "here's a design I made" -- it shows "here's something I shipped this afternoon." The output has changed identity. That is a paradigm shift, not a preference update.

---

## Provenance

| Source File | Contribution |
|-------------|-------------|
| `corpus/design-taste/00267.md` | Alex Kehr, "The Future of Design is Direct Design" -- the naming and definition of Direct Design, the vibe coding distinction, "taste now has a compiler," the handoff as root cause, the observation that we spent decades teaching engineers to think like product people when it was easier to give product people the ability to ship. |
| `corpus/design-taste/00169.md` | Pablo Stanley, "The Design Vibeshift" -- practitioner survey of the shift, Hardik Pandya (Atlassian) testimony, Adam Whitcroft on Figma's diminishing centrality, Darrin Henein on design systems migrating to GitHub, the "do both" pragmatist position, the hybrid loop pattern, the designer's feed changing from designs to shipped products. |
| `corpus/design-taste/03562.jsonl` | Atoms extracted from Design Vibeshift -- 19 atoms covering designer sentiment shift, Figma as supplementary, Atlassian "Handoffs into Handshakes," code as source of truth, systemic coherence risk. |
| `corpus/design-taste/03564.md` | Extraction of Design Vibeshift -- structured breakdown of all claims, concepts, frameworks, praxis hooks, and predictions. |
| `corpus/design-taste/03838.jsonl` | Atoms from Direct Design article -- Direct Design definition, vibe coding contrast, feedback loop collapse, product taste as directly executable. |
| `corpus/design-taste/03840.md` | Extraction of Direct Design -- 13 atoms covering handoff problem, middleman elimination, rigorous product-context holding, team workflow with direct code tweaks. |
| `corpus/design-taste/04246.jsonl` | Figma Claude Code import feature -- bidirectional integration, code-to-Figma import as acknowledgment that code is now primary. |
| `corpus/design-taste/10939.md` | OpenEditor thread (Dami Dina) -- Figma-like canvas for code projects, bird's-eye view across breakpoints/states/environments, config-driven route-to-preview mapping. |

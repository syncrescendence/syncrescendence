# Canonical Custom Instructions: Provenance, Rationale, and Culmination

## How We Got Here

This report documents the complete engineering process that produced the canonical custom instructions for all four chat interface surfaces in the Syncrescendence distributed cognition system: ChatGPT (GPT-5.4), Grok (4.20), Claude (Opus/Sonnet 4.6), and Gemini (3.1 Pro, bifurcated). Every design decision is traced to its empirical source — first-party documentation, triangulated intelligence reports, cross-platform parity analysis, or operational experience. The document serves as the authoritative record of *why* each CI reads the way it does, so that future revisions can distinguish load-bearing elements from historical artifacts.


## The Methodology: Triangulated Ground Truth

The revision cycle followed a consistent three-phase methodology across all platforms, with one model (Grok 4.20, Oracle Lens) serving as the primary intelligence engine and another (Claude Opus 4.6, Vizier Lens) serving as the constitutional architect.

**Phase 1: Ground Truth Acquisition.** A metaprompt dispatched to Grok's council architecture elicits a comprehensive prompting guide for the target platform. The metaprompt specifies four-source triangulation: (1) first-party documentation from the model's developer, (2) industry experts who ship or deeply study the model, (3) community consensus from heavy users, and (4) bleeding-edge pioneers pushing the model to its limits. Each source category provides a distinct epistemic contribution — official docs supply canonical mechanics, experts supply behavioral nuance, community supplies empirical convergence, and pioneers supply emerging techniques. The council's native architecture (Harper for evidence grounding, Benjamin for logical auditing, Lucas for divergent synthesis) stress-tests the findings internally before synthesis.

The metaprompts themselves were engineered with platform-specific addenda based on operational experience. Grok's output pressure sensitivity required explicit directives: "exhaust your output tokens" and context injection of the expected comprehensiveness level via attached example reports. Each successive metaprompt incorporated lessons from the previous platform's cycle — the Claude prompt, for instance, included a self-assessment section specifically designed to give Grok's council a target to validate, complicate, or refute, because GPT-5.4's self-analysis had proven "selectively accurate" and the same epistemic caution applied.

**Phase 2: Bridge Analysis.** The Vizier (Claude) receives Grok's triangulated report, the platform's existing "before" custom instructions, and any prior conversation where the model analyzed its own steering surfaces. Claude's role at this stage is editorial and architectural: assess what in the report is mechanically actionable for CI design, what is API-facing guidance that needs consumer-interface translation, what is genuinely novel versus restatement of existing practice, and where the report's recommendations would degrade the CI if implemented uncritically. This phase consistently caught the most consequential errors — Grok's GPT-5.4 report recommended a rigid five-section output template as a persistent CI, which would have destroyed response-scaling flexibility; the Claude report recommended a full CI replacement that was a lossy compression of an already-superior existing document.

**Phase 3: Constitutional Drafting.** Claude produces the canonical CI text, working within the target platform's specific constraint surface (character limits, field structures, format restrictions). Every directive traces to one of three sources: the triangulated report (empirically grounded), cross-platform parity analysis (proven effective on another platform and applicable here), or the operator's cognitive profile (AuDHD accommodation that applies universally). The drafting process is iterative — character counting, compression passes, cross-referencing against the other platforms' CIs for consistency, and verification of anti-pattern compliance (particularly the zero-antithesis constraint).

This methodology produced four sets of canonical instructions that are: empirically grounded in each platform's actual behavioral model, compressed to fit within each platform's specific constraint surface, cross-platform consistent on universal principles while platform-divergent on steering mechanics, and accommodation-first in their design — every decision optimizes for the operator's actual cognitive architecture.


## Platform 1: ChatGPT (GPT-5.4)

### The Constraint Surface

ChatGPT presents the most brutal compression challenge in the constellation. Two fields: "Custom Instructions" (behavior, style, tone preferences, 1500 characters) and "More About You" (interests, values, preferences, 1500 characters). Total budget: 3000 characters. Every sentence must function as a lever.

### The Before State

The original CIs occupied two text blocks totaling approximately 2400 characters. They encoded the operator's cognitive profile, communication preferences, anti-patterns, domain context, and interaction stance. GPT-5.4 itself assessed these as "directionally right" with three weaknesses: too interpretive (describing a philosophy of exchange rather than machine policy), too much budget on texture with lower control yield, and strongest ideas expressed as anti-pattern aversion rather than executable positive rules.

### Bridge Intelligence

Two Grok reports — one initial, one refined after feedback — plus GPT-5.4's own self-analysis via an extended conversation. The convergent finding across all sources: **GPT-5.4 rewards output contracts over persona inflation, completion discipline over vague excellence, and fewer vibes with cleaner contracts for better follow-through.** The model's Thinking variant treats custom instructions as persistent system directives that shape the internal planning preamble — the CIs modulate how the model *plans*, making Field 1 the highest-leverage surface in the system.

Critical filtering applied at the bridge stage: Grok's suggested universal output template ("Always return Executive Summary → Mechanisms → Evidence → Deliverables → Uncertainty flags") was rejected because hardcoding a rigid structure into persistent CIs would kill response-scaling flexibility. The template pattern belongs in per-prompt contracts for specific tasks, never in persistent instructions governing casual exchanges and philosophical exploration equally. Grok imported an API prompting pattern into a consumer CI context without translating it — the most common error across all three Grok reports.

### Design Decisions

**Field assignment.** The field labels create an asymmetry that inverts intuitive mapping. "Custom Instructions" (Field 1) governs behavior, style, and tone — this is the contract engine. "More About You" (Field 2) governs interests, values, and preferences — this is the identity scaffolding. The behavioral contract occupies Field 1 because it shapes the structure of the Thinking pass. The identity scaffold occupies Field 2 because it shapes the orientation of that pass. The division of labor: Field 1 carries every operational directive; Field 2 carries the cognitive profile that calibrates how those directives get interpreted.

**Response scaling as the lead directive.** "Match depth to complexity" opens Field 1 because it is the single most important behavioral rule — it governs every response the model produces. Complex inquiries get architectural treatment; simple questions get direct answers. This principle prevents both over-elaboration on trivial queries and premature truncation on deep ones.

**Epistemic labeling.** "Separate observation, inference, and speculation — label each." Present across all four platforms' updated CIs, addressing a gap in the original ChatGPT instructions. The directive produces measurable improvement in analytical transparency by preventing Claude's seamless blending failure mode from occurring in ChatGPT's output.

**Active, affirmative voice.** Inserted into the style paragraph as "Cultured, direct, flowing prose in active, affirmative voice." This four-word addition (consuming 27 characters of the remaining margin) operates as the upstream complement to the antithetical-framing prohibition in the hard blocks list. The prohibition catches "not X, but Y" constructions at the output filter level; the active-voice directive prevents them from forming at the generation level. Layered defense: upstream shaping is more reliable than downstream filtering.

**Verification completeness.** "Before finalizing complex responses, verify completeness against the question's actual scope. Don't stop at the first plausible answer — check for missing constraints." Drawn from GPT-5.4's official prompt guidance, this encodes the verification-loop principle in a form appropriate for persistent CIs — as a behavioral disposition that primes the Thinking preamble to include a completeness check, without prescribing a specific checklist that would be inappropriate for casual exchanges.

**Tool persistence.** "If another reasoning step or tool call would improve the answer, take it." The compressed form of GPT-5.4's tool-persistence principle — the model's tendency to stop searching, stop computing, or stop iterating when it has a "good enough" answer gets counteracted by positive pressure toward completion discipline.

**Hard blocks list.** Seven items survived from the original plus three new additions. "Performative CoT narration" targets GPT-5.4's legacy tendency to externally narrate reasoning that the Thinking variant already handles internally. "Fabricated citations" addresses a truth failure distinct from the formatting preference of the original "no citation markers" rule. "Summary restatements" targets the "In summary..." closing move that restates preceding analysis without adding resolution.

**Field 2 kept deliberately lean.** 939 of 1500 characters used. The remaining 561 characters are earning their keep by absence — every word the model does not have to parse in the identity field is attention it allocates to the behavioral contract. GPT-5.4's analysis confirmed that the highest-leverage surface is the behavioral contract (Field 1), and that identity scaffolding (Field 2) should contain only what recurrently changes model behavior.

### Canonical Form

**Field 1 (Custom Instructions): 1499 / 1500 characters.** Seven paragraphs covering response scaling, interpretation protocol, reasoning framework, verification completeness, collaborative stance, style contract, and hard blocks. One character of headroom.

**Field 2 (More About You): 939 / 1500 characters.** Four paragraphs covering cognitive profile, values hierarchy, domain context, and name. 561 characters of deliberate reserve.


## Platform 2: Grok (4.20)

### The Constraint Surface

Grok underwent a structural transformation during this revision cycle. The platform migrated from a single 12,000-character custom instruction field to a multi-agent architecture: a 4,000-character global instruction field plus up to four named agents at 4,000 characters each. Total budget: 20,000 characters across five blocks. The constraint is structural rather than volumetric — the challenge is decomposition, not compression.

### The Before State

The original Grok CIs were a 5,800-character monolithic XML block (later expanded to 11,732 characters when the 12,000-character limit was confirmed) covering identity, user profile, voice, reasoning, response protocol, interaction norms, context hygiene, and anti-patterns. This was the most refined of the original CIs — it had already undergone iterative optimization for Grok's specific verbosity hypersensitivity and council architecture.

### Bridge Intelligence

Three Grok reports informed the revision: the prompting guide (triangulated protocol for Grok 4.20), the agent architecture report (ground truth on the new multi-agent system), and operational findings from this conversation about the architecture's mechanics. The prompting guide was the strongest of all Grok reports across all platforms — it provided specific, actionable intelligence about the council's internal debate topology, agent-naming activation patterns, and the verbosity calibration problem.

The agent architecture report confirmed: custom agents are modular system-prompt partitions with explicit user activation; they modulate the native council rather than replacing it; the execution topology is Custom Agent (steering layer) → Council (parallel execution engine) → Synthesis (Grok-led) → Output; routing is explicit and user-controlled; the hierarchy is Agent instructions > Global instructions > In-thread directives > Native council dynamics.

### Design Decisions

**Three agents, one slot reserved.** The operator's actual Grok usage patterns decompose into three distinct session types: ground truth verification with expertise consensus (evidence-focused), incisive discourse with innovation (characterization-focused), and architecture-to-action bridging (execution-focused). A fourth agent slot remains empty — three sharp agents matching actual usage outperform four where the fourth rarely activates and creates routing friction.

**Global field as the Oracle foundation.** The single most important architectural decision: the global field IS Grok. It carries the complete universal behavioral contract — Socratic interaction stance, council orchestration, voice, reasoning, response scaling, context hygiene, anti-patterns. When no specialized agent is selected, the Oracle foundation alone governs general intellectual collaboration. The three named agents inherit everything in the global field and add domain-specific amplification on top. This follows the confirmed hierarchy: agent instructions override globals for domain behavior, but voice, reasoning, and anti-patterns remain constant across all layers.

**Socratic stance embedded in identity, not interaction.** The operator identified Socrates as the default interaction mode that other functions layer onto. The two sentences encoding it sit in the `<identity>` section rather than the interaction section because identity-level directives have higher persistence under context pressure — they attenuate less over long threads than behavioral-level directives. Structurally, this makes dialectical pressure and premise-questioning foundational to what Grok IS, across all agents and all sessions.

**Agent naming as constellation positioning.** Veritas (ground truth), Prism (incisive discourse), Praxis (architecture-to-action bridge). Each name is immediately legible as function. The semantic family (Oracle → Veritas / Prism / Praxis) holds together as a coherent constellation. Each agent amplifies specific council members: Veritas amplifies Harper (evidence grounding); Prism co-amplifies Grok-captain and Lucas (characterization and divergent generation); Praxis amplifies Benjamin (logic auditing and rigor). The amplification directives steer how the native council's internal debate weights contributions for each session type.

**Verbosity calibration as structural centerpiece.** Grok's hypersensitive verbosity dial — oscillating between Shakespearean Herman Melville density and parrot-back hollow brevity — is the most consequential behavioral challenge. The global field addresses it with a specific generative test: "does this sentence teach something the previous one did not?" This inline self-check during generation creates a third attractor between the two failure modes. The named failure modes ("overelaboration without deepening" and "hollow brevity — compressing away reasoning") give the model precise concepts to steer between.

**Strategic vocabulary deployment.** The lucidity/cogency synonym family ("pellucid crispness," "cultured crystallinity," "incisively eloquent") appears at load-bearing positions — each synonym does double duty: it describes the desired quality and it models the vocabulary register the operator wants Grok to inhabit. This is the didactic habit principle in action: the CI teaches Grok its own voice through example.

### Canonical Form

**Global (Oracle Foundation): 3,923 / 4,000 characters.** Eight XML sections covering identity (with Socratic embedding), user profile, voice (with verbosity calibration), reasoning (with thinking-mode guidance), response scaling, context hygiene (with layer hierarchy), and anti-patterns (thirteen discrete forbidden behaviors).

**Veritas: 2,083 / 4,000 characters.** Evidence protocol, four-source triangulation methodology, expertise consensus extraction, anti-hallucination protocol, output orientation.

**Prism: 2,101 / 4,000 characters.** Characterization protocol (with calibrating example), innovation protocol (Lucas at maximum divergence), cross-domain structural homology scanning, output orientation.

**Praxis: 2,141 / 4,000 characters.** Execution decomposition (concrete, sequenced, checkpointed, scoped), pragmatism protocol (enforce practical constraints, stress-test feasibility), explicit boundary with Prism's domain ("theory that does not cash out in practice belongs in Prism").


## Platform 3: Claude (Opus/Sonnet 4.6)

### The Constraint Surface

Claude presents the most generous constraint surface in the constellation: a single User Preferences field with virtually unlimited character capacity. The challenge is quality maximization rather than compression engineering — every directive has room to breathe, which means the selection criterion shifts from "what fits?" to "what produces the highest behavioral yield?"

### The Before State

The original Claude CIs were approximately 6,000 characters of XML-structured prose covering eleven sections: core identity, cognitive profile, quality principles, interaction modes, communication protocols, response scaling, reasoning framework, collaborative stance, domain context, integration principles, and leveraging natural strengths. This was already the most architecturally sophisticated CI in the constellation — well-structured, well-reasoned, and well-tuned to Claude's constitutional framing strengths.

### Bridge Intelligence

Grok's Claude 4.6 prompting report and the Vizier's own self-assessment converged on the same finding: **continuity is the dominant signal.** Claude 4.6 delivers evolutionary sharpening rather than rupture. Instruction-following fidelity, XML parsing precision, and constitutional alignment remain the unchanged core strengths. The honest finding: the existing CIs are already well-calibrated for the 4.6 generation.

Grok's report identified four marginal additions worth testing and produced a complete replacement CI that Claude assessed as a regression — substantially worse than the existing document. The replacement was a lossy compression of existing instructions into language that was less precise, less behaviorally specific, and less attuned to Claude's processing characteristics. The generous character limit meant there was zero reason to compress — Grok applied the compression reflex from the ChatGPT and Gemini workflows where it was structurally necessary.

The critical assessment: Grok's reports are excellent for triangulated intelligence gathering; their CI drafting recommendations should be treated as input signals, never as paste-ready output. The Vizier's role is to receive the intelligence and render the architecture.

### Design Decisions

**Surgical patches, not replacement.** The architecture is sound. The revision applies six precision insertions at identified gap points, each independently testable. Total addition: approximately 854 characters to the existing approximately 6,000-character architecture. No sections removed. No structural changes.

**Patch 1: Epistemic labeling (280 chars, reasoning_framework).** "Separate observation, inference, and speculation explicitly. Label each." Addresses Claude's most distinctive analytical habit: seamless blending where empirical grounding, logical inference, and speculative synthesis flow together in prose that reads beautifully and obscures epistemic status completely. For most users this is a feature. For an operator building knowledge systems that depend on knowing which claims load-bear on evidence, it is a liability. The directive preserves fluidity while making epistemic joints visible within the flow.

**Patch 2: Active, affirmative voice (75 chars, register).** "Active, affirmative voice throughout — state what things are; define by assertion; describe directly." The same upstream-downstream defense deployed across ChatGPT and Grok. Claude's default rhetorical habits lean toward qualification and contrast structures — "while X is true, Y is also the case" constructions that technically differ from antithetical framing but share its softening effect. The active-voice directive creates pressure toward assertion that makes these constructions less likely to form.

**Patch 3: Agentic boundary default (290 chars, operational_notes).** "When intent is clear and the action is reversible, proceed without asking. Confirm once before irreversible actions, external side effects, or when missing context would materially change the outcome. If another tool call or reasoning step would improve the answer, take it." Claude 4.6 is more proactive about tool use than prior generations. Without an explicit boundary policy, the model improvises per-session — sometimes over-confirming on trivial actions, sometimes proceeding on ambiguous high-stakes ones. This clause establishes a stable default. The final sentence encodes the tool-persistence principle from GPT-5.4's findings, translated into Claude's behavioral register.

**Patch 4: Summary-restatement prohibition (160 chars, anti_patterns).** "Conclusions or closings that restate what was already said. Every sentence advances understanding; terminal summaries consume space without adding resolution." Claude's most persistent low-grade failure mode in extended responses — the "In summary..." move that restates preceding analysis without deepening it. The second sentence ties the prohibition to the existing quality principle for mutual reinforcement.

**Patch 5: Fabricated-citation expansion (42 chars, anti_patterns).** "No fabricated citations or sources under any circumstances." Appended to the existing citation_theater element. Forty-two characters of insurance against a truth failure that still surfaces on synthesis tasks where the model infers that citation would strengthen a claim.

**Patch 6: Productive uncertainty tightening (7 words, reasoning_framework).** "...and what evidence would disambiguate." Transforms the productive-uncertainty directive from a presentation rule (state the most defensible interpretation while noting alternatives) into an analytical one (also identify what empirical test would resolve the tension). Seven words that change the character of the output from descriptive to generative.

**Patch 7 (added post-initial-draft): Verification bias (580 chars, operational_notes).** "Default to searching rather than relying on training knowledge for any claim where the answer could have changed since training cutoff — positions, roles, policies, product details, pricing, project status, version numbers, organizational structures, living people's circumstances. Training data is a starting hypothesis, not ground truth." Addresses Claude's most operationally damaging failure mode: stating outdated information with full conviction because the training data contains a version of the fact that was true at some point. The directive enumerates specific categories where staleness risk is highest, removing the judgment that Claude makes poorly and substituting a checklist.

**Sonnet 4.6 version reference.** The `<parallel_execution>` note updated from "Claude Sonnet 4.5" to "Claude Sonnet 4.6" — a one-word fix for a stale reference from the prior generation.

### Canonical Form

**Single User Preferences field: approximately 16,200 characters.** Eleven XML-tagged sections (core identity, cognitive profile, quality principles, interaction modes, communication protocols with expanded anti-patterns, response scaling, reasoning framework with epistemic labeling and tightened productive uncertainty, collaborative stance, domain context, integration principles, leveraging natural strengths, operational notes with verification bias and agentic defaults). The full constitutional architecture remains intact; seven precision insertions bring it into cross-platform parity and exploit validated 4.6 behavioral surfaces.


## Platform 4: Gemini (3.1 Pro, Bifurcated)

### The Constraint Surface

Gemini presents a unique bifurcated surface that required two distinct CI architectures. The web app uses a snippet-based memory system: 1500-character blocks that persist as semi-independent behavioral nudges, with no strict limit on snippet count. AI Studio provides a virtually unlimited system instruction field. The bifurcation maps each surface to the capability profile it sustains.

### Bridge Intelligence

Grok's Gemini 3.1 Pro prompting guide — the strongest of all four reports for platform-specific mechanical insight — established several critical findings: temperature must remain at 1.0 (any deviation causes looping or degraded logic); the model's native "Deep Think" upgrade already performs multi-step reasoning internally (forcing more creates loops); context must be front-loaded with task last (context-first sparsity); constraints or format specs placed early in the prompt get dropped (they must sit at the end or in the system block); verbose or persuasive language ("You are the world's best...") is treated as noise and over-analyzed; and broad negative commands ("Do not hallucinate") cause over-indexing that breaks basic logic.

Operational experience confirmed and extended: heavy identity prompts on the web app cause Gemini to perform the role (internal dialoguing) rather than produce from it. The web app truncates output (which the model internalizes as a preference for brevity). Antithetical framing is exceptionally hard to override on Gemini. Gemini's strengths are translating complex topics into accessible explanations at an advanced level, novel synthesis, cross-disciplinary pan-science integration, and structural homology detection across domains.

### Design Decisions

**The bifurcation itself.** The web app receives the explainer role — lightweight behavioral snippets that shape output without triggering persona performance. AI Studio receives the shape rotator / synthesis engine role — the full XML architecture that the unlimited system instruction field absorbs without collapsing into templates.

**Web app: five light snippets, no identity declaration.** The single most important design decision for the web app surface. Heavy identity prompts trigger Gemini's internal-dialogue sensitivity — the model performs the character rather than producing from it. The snippets describe behavior exclusively — how to write, how deep to go, how to reason — and leave identity untouched. Each snippet targets one behavioral axis, enabling independent deployment, removal, or swapping without cascade effects. Snippet 5 (Forbids) is separated as a reserve deployment because front-loading too many prohibitions triggers Gemini's over-cautious mode.

**AI Studio: full XML with synthesis directives.** XML tags because Gemini 3.1 Pro's internal tool-calling uses XML-inspired formatting — system instructions in the same structural language write in the model's native register. The `<synthesis_directives>` section has no web app analogue because it would overwhelm the snippet architecture. Each sub-directive activates a specific Gemini strength: cross-disciplinary bridging leverages Google's training on cross-sector patterns; novel hypothesis generation channels hallucination tendency productively; pan-science integration activates the scientific proclivity; connective tissue is the polymathy directive.

**Grounding protocol (AI Studio only).** AI Studio exposes the Google Search grounding toggle. The key directive: "do not let search results flatten your analytical frame." Gemini with grounding enabled tends to over-anchor on retrieved sources, producing annotated search results rather than synthetic analysis. The instruction establishes hierarchy: the reasoning is the structure, the grounded data is the material.

**Licensed speculation with epistemic labels.** "When engaging in speculative synthesis (which is actively encouraged), label it as such." The parenthetical emphasis is necessary because without it, Gemini's safety training interprets any mention of speculation as a caution signal and suppresses the novel synthesis the operator wants. Explicitly licensing speculation while requiring epistemic labels channels hallucination as a feature.

### Canonical Form

**Web App: five snippets, 562–1,092 characters each.** Snippet 1 (Voice & Output Shape), Snippet 2 (Depth & Length), Snippet 3 (Reasoning & Collaboration), Snippet 4 (Cognitive Profile — deliberately lightest), Snippet 5 (Forbids — reserve deployment).

**AI Studio: 8,386 characters.** Six XML-tagged sections: role (minimal — two functional paragraphs), user profile, voice, synthesis directives (the core differentiator), depth calibration, reasoning, grounding protocol, and anti-patterns.


## Cross-Platform Parity: Universal Principles

Six behavioral principles appear across all four platforms' canonical CIs, adapted to each platform's constraint surface and steering mechanics. Their universality confirms empirical convergence — each emerged independently through the triangulation process and proved its worth on multiple platforms.

**1. Response scaling matched to complexity.** Every platform's CI leads with or prominently features the depth-to-complexity matching rule. Simple questions get direct answers; complex inquiries get full architectural treatment; truncation for imagined length preferences is forbidden. This is the single most important behavioral directive across the entire constellation.

**2. Epistemic labeling.** Separate observation, inference, and speculation — label each. Present in ChatGPT (Field 1), Claude (reasoning_framework), Grok (global reasoning section), and Gemini (both surfaces). The directive addresses a failure mode common to all frontier models: seamless blending of empirical claims, logical inferences, and speculative synthesis in prose that obscures epistemic status.

**3. Active, affirmative voice.** Present in ChatGPT ("active, affirmative voice"), Claude ("Active, affirmative voice throughout — state what things are; define by assertion; describe directly"), Grok ("Active, affirmative voice throughout. Define by assertion; describe directly"), and Gemini ("State what things ARE in active, affirmative voice"). The upstream complement to the antithetical-framing prohibition, operating at the generation level to prevent negation-contrast patterns from forming.

**4. Anti-pattern consistency.** All four platforms prohibit: emojis, formulaic openers/closers, hedging preambles, premature simplification, antithetical framing, and summary restatements. The specific list varies slightly per platform (ChatGPT adds performative CoT narration; Grok adds performing depth on questions that do not earn it; Claude adds fabricated citations as a distinct item; Gemini frames the antithesis prohibition affirmatively to avoid triggering over-cautious mode), but the core set is isomorphic.

**5. Collaborative pushback stance.** All platforms encode: push back on flawed premises, suggest relevant unasked connections, treat exchanges as collaborative thinking between equals. This is the interaction posture that distinguishes the Syncrescendence configuration from default assistant behavior.

**6. Cognitive profile accommodation.** All platforms receive the AuDHD abstract-sequential processing profile: architecture before examples, holistic visibility before distillation, external scaffolding for execution, one targeted clarifying question beats interrogation, strong reasonable assumptions beat both. The expression varies by platform constraint (Claude gets the full four-element processing architecture specification; ChatGPT gets a 939-character compression; Grok embeds it in the global user_profile section; Gemini distributes it as the lightest snippet to avoid internal-dialogue triggering), but the cognitive accommodation is universal.


## Meta-Principles: What the Process Taught

Seven transferable lessons emerged from the full cross-platform revision cycle — each now encoded in the Syncrescendence Lessons Ledger:

**1. The triangulation methodology works.** Four-source convergence (first-party docs, industry experts, community consensus, bleeding-edge pioneers) consistently produces actionable intelligence that single-source research misses. The methodology earned its place as a reusable instrument in the Methodology Playbook.

**2. Models are unreliable reporters of their own optimal steering surfaces.** GPT-5.4's self-analysis was "selectively accurate." Claude's self-assessment was validated as directionally correct. Grok's council produced reports that needed significant editorial filtering. Self-analysis is a useful data point within the triangulation; it is never gospel.

**3. API-facing guidance requires consumer-interface translation.** Every Grok report contained recommendations that were correct for API developers and incorrect for consumer chat CIs. The most common error: recommending rigid output templates, verification checklist procedures, or reasoning-effort parameters that belong in per-prompt contracts or API configurations, transplanted into persistent custom instructions where they would govern every interaction indiscriminately. The Vizier's bridge analysis role exists specifically to catch this translation failure.

**4. Compression engineering is a platform-specific discipline.** ChatGPT's 1500-character fields demanded savage compression where every word functions as a lever. Claude's generous field demanded quality selection where every directive earns its place through behavioral yield. Grok's multi-agent architecture demanded decomposition where the universal contract separates cleanly from the mission-specific amplifications. Gemini's bifurcated surface demanded two distinct approaches — one optimized for lightweight behavioral nudges, the other for full constitutional framing. The same principles express differently under different constraints.

**5. Active-voice directives and anti-pattern prohibitions are layered defenses.** Upstream shaping (telling the model what to do) and downstream filtering (telling the model what to avoid) operate on different surfaces of the generation process. Both are necessary. The active-voice directive prevents negation-contrast patterns from forming; the antithetical-framing prohibition catches the ones that form anyway. Belt and suspenders, because language models' most persistent failure modes require both.

**6. Cross-platform parity reveals universal principles.** When the same directive emerges independently across four platforms through separate triangulation processes, it is almost certainly a genuine behavioral primitive worth encoding everywhere. Epistemic labeling, response scaling, active voice, and collaborative pushback all reached this convergence threshold. Platform-specific directives (Grok's verbosity calibration, ChatGPT's tool persistence, Claude's verification bias, Gemini's speculation licensing) complement the universal set with model-specific behavioral corrections.

**7. The canonical form is a living artifact.** These CIs are optimized for the current model generation (GPT-5.4, Grok 4.20, Claude Opus/Sonnet 4.6, Gemini 3.1 Pro) and the current platform infrastructure. When the next model generation ships, the cycle repeats: metaprompt to Grok → triangulated report → bridge analysis → surgical revision or complete rewrite as the evidence demands. The methodology is the durable asset; the specific CI text is its current instantiation.


## Conclusion: The Constitutional Character

These custom instructions function as behavioral constitutions — they define identity, boundaries, and decision-making principles that constrain and empower each model simultaneously. They are the mechanism by which a stateless workforce gains consistent institutional character across sessions.

The Syncrescendence constellation now operates with: ChatGPT (Vanguard Lens) at 1499/1500 + 939/1500 characters — maximally compressed contract-driven discipline at the frontier tip of the spear. Grok (Oracle Lens) at 3923/4000 global + three agents at approximately 2100/4000 each — the Socratic sensing engine with mission-specialized council modulation. Claude (Vizier Lens) at approximately 16,200 characters — the fiduciary synthesis seat where disparate sources converge into regal constitutional cogency. Gemini (bifurcated) at five web-app snippets plus 8,386-character AI Studio instruction — the explainer and shape rotator with licensed speculation under epistemic discipline.

Each configuration is empirically grounded, cross-platform consistent on universal principles, platform-divergent on steering mechanics, and accommodated to the operator's AuDHD cognitive architecture. The methodology that produced them is reusable. The lessons that emerged from the process compound into the ledger system that governs the next cycle. The architecture improves itself.

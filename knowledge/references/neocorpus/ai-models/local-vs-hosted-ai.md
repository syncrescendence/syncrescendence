# Local vs. Hosted AI

> **Epistemic Status — THIN SOURCING**: This entry's declared sources are three YouTube artifacts with no transcripts and one minimal extraction. They establish that the local-vs-hosted comparison is a live practitioner topic and that GPT-5.1 has specific hosted-model improvements, but they do not supply the substantive reasoning this entry originally claimed. Claims below are marked by what actually supports them. Assertions that require richer sourcing are flagged explicitly. This entry should be treated as a placeholder framework pending deeper corpus material.

---

## What the Sources Establish

### From 10361 — Clawdbot + LM Studio + GPT-OSS Setup Guide

Source 10361 is a YouTube video by Bijan Bowen (published 2026-01-27, 32m) covering a hands-on local AI setup. The video description confirms the following topics were demonstrated:

- **Clawdbot paired with a locally hosted model** (LM Studio + GPT-OSS 20B) rather than a hosted API — framed as a test of how well Clawdbot performs in local deployment
- **Browser automation** and **log analysis** as demonstrated test tasks
- **Security disclaimers** appear as a named section (timestamp 06:37) — indicating security considerations are part of the practitioner discourse, though the specific content of those disclaimers is not available
- **Context length** is called out as a notable consideration ("Context Length FYI" at timestamp 24:51)
- **GPT-OSS 20B** is the local model used for the browser tool test (timestamp 30:25 — "GPT-OSS 20B Browser Tool Result")
- **Autonomous browser control** is demonstrated as a Clawdbot capability (timestamp 14:51)
- **WhatsApp setup** and **refusal testing** are also covered — indicating local model behavior boundaries were probed

What the source does NOT establish: any quantified claims about capability gaps, cost comparisons, context length numbers, percentage coverage of use cases, or recommendations for hybrid vs. pure-local vs. pure-hosted architectures. The video demonstrates local AI setup; it does not argue for or against it relative to hosted APIs.

### From 10270 — "AI in 2026 is going to be wild"

Source 10270 is a Wes Roth YouTube video (published 2026-01-25, 12m43s) covering general AI news. The description references OpenAI, Google, Anthropic, NVIDIA, and open-source AI as topics. No transcript is available. No specific claims about local vs. hosted AI are extractable from this source as filed. The source establishes only that the AI landscape in early 2026 is active and that frontier model development across multiple labs is ongoing.

### From 01332 — GPT-5.1 Capability Extraction

Source 01332 is an extraction from a panel discussion about GPT-5.1. Four atoms are established:

1. GPT-5.1 has two modes: "Instant" (rapid chat) and "Thinking" (in-depth problem-solving)
2. GPT-5.1 shows improvements in conversational warmth, instruction following, and adaptive thinking that allocates more processing time to complex tasks
3. GPT-5.1 gains span simple task accuracy, strategic decision-making, planning, and long-form writing
4. GPT-5.1 offers personalization presets for tone and role-based behavior

What this establishes for local-vs-hosted: Hosted frontier models are iterating on capability dimensions (reasoning depth, instruction following, planning, personalization) that local models typically lack direct equivalents to. The "Thinking" mode and adaptive compute allocation describe hosted-model infrastructure that consumer hardware cannot replicate at equivalent scale.

---

## Framework (Sourcing Gaps Marked)

The following framework reflects the practitioner framing implied by the sources. Where claims go beyond what the sources establish, they are marked **[UNSOURCED — requires additional corpus material]**.

### The Local Deployment Surface

From 10361: Clawdbot running GPT-OSS 20B locally via LM Studio demonstrates that local AI can perform browser automation, log analysis, and autonomous browser control. Context length is a noted consideration in local setup. Security disclaimers are part of practitioner guidance for this configuration.

The setup demonstrates that local models with tool access can interact with browsers and execute tasks autonomously. The security dimension — that a locally running model with shell and browser access operates with the user's system permissions — is a practitioner-recognized concern (the video includes a dedicated security disclaimer section).

### Hosted Model Capability Trajectory

From 01332: As of late 2025, hosted frontier models like GPT-5.1 are developing capability dimensions including adaptive compute allocation, planning improvements, and instruction following that represent architectural choices requiring large-scale infrastructure. These are not features of the local models demonstrated in 10361.

### What Remains Unestablished by These Sources

The following claims appeared in the prior version of this entry and are **not supported** by 10361, 10270, or 01332:

- That local-vs-hosted is a tradeoff "across economics, security, capability, latency, privacy, and operational complexity" as a systematic framework — the sources do not articulate this taxonomy
- Specific cost comparisons or crossover-point economics
- That hosted APIs cover "80-90% of local use cases better" — fabricated figure
- That local context is "typically 4K-8K" while hosted offers "128K-1M" — specific numbers not found in sources (10361 mentions context length as a consideration but provides no numbers)
- That hybrid local+hosted is the recommended default architecture
- Any recommendation about which deployment approach most users should adopt
- Capability gap characterizations beyond what the GPT-5.1 extraction establishes for that specific model

---

## Anti-Patterns (Retained — Practitioner-Level Reasoning)

These anti-patterns reflect practitioner common sense consistent with the demonstrated setup in 10361, though not argued explicitly in the sources:

- **Granting full shell access to a local model without reviewing the security implications** — 10361 includes a dedicated security disclaimer section, indicating practitioners treat this as a non-trivial risk surface
- **Assuming local deployment equals private deployment** — not argued by the sources but a standard practitioner caveat when discussing local AI tooling

---

## Syncrescendence Operational Context

*This section contains internal operational facts that are true for the Syncrescendence constellation but are not sourced from the corpus files declared above. They are recorded here for operational transparency, not as compendium claims.*

- The Syncrescendence constellation depends on hosted frontier models (Claude Opus 4.6, GPT-5.3-Codex, Gemini Pro 3.1) as its cognitive core. Local models are not currently deployed in the agent stack.
- The constellation's API budget is approximately $55/month as of CC62.
- These operational facts belong in `memory/` and `AGENTS.md` — not in this compendium entry's core claims.

---

## Temporal Framing

### What the Sources Support

The sources establish one temporal signal with Phase 3-4 value: GPT-OSS 20B running locally via LM Studio (demonstrated in 10361, published January 2026) represents a data point in the long-running displacement of the assumption that local AI was inherently limited to toy use cases. A practitioner in 2026 is demonstrating autonomous browser control and log analysis with a 20B parameter local model — tasks that would have required hosted frontier APIs two years earlier.

The sourced GPT-5.1 material (01332) documents hosted-model capability dimensions (adaptive compute allocation, Thinking mode, planning improvements) that represent infrastructure choices local models cannot replicate at equivalent scale on consumer hardware. This establishes the persistent capability gap for compute-intensive tasks even as local capability has expanded.

### Obsolescence: "Local AI is a Research Toy"

The assumption that local models were inherently unsuitable for production-adjacent tasks has been progressively invalidated by the open-weight model ecosystem (Llama, Mistral, GPT-OSS). The Clawdbot + GPT-OSS 20B demonstration in 10361 is evidence from the practitioner layer: the tooling exists, the setup is demonstrated, and the tasks (browser automation, log analysis) are substantive. The question has shifted from "can local models do useful work?" to "what are the remaining capability and security tradeoffs?"

### Phase 3-4 Audit Note

Source material for this entry is insufficient for a full temporal framing treatment. The three sources (10361, 10270, 01332) provide: one hands-on demo with no quantitative capability claims, one general AI news video with no extractable content, and one 4-atom extraction covering GPT-5.1 features. No source establishes the historical trajectory of local vs. hosted capability gaps, the economics of crossover points, or the design decisions that made one preferable to the other at different points in time. The supersession chain (from "local is a toy" to "local handles substantive tasks with tradeoffs") is directionally supportable from the sources but cannot be quantified or detailed without additional corpus material. This entry's enrichment path (listed below) remains the honest characterization of its state.

---

## Enrichment Path

This entry requires additional corpus material to become a full compendium treatment. Needed:

1. Source material with transcript-level detail on local vs. hosted capability comparisons
2. Source material establishing context length norms for consumer-grade local deployments
3. Source material on cost economics of local vs. hosted inference
4. Source material on privacy and data sovereignty tradeoffs

Until richer sources are incorporated, this entry serves as a source-accurate stub documenting what the filed corpus actually establishes.

---

## Sources

| Source | File | What It Actually Contains |
|--------|------|--------------------------|
| Clawdbot + LM Studio + GPT-OSS setup guide | `corpus/ai-models/10361.md` | YouTube video description + timestamps. Demonstrates local AI setup with Clawdbot, GPT-OSS 20B, browser automation, log analysis, security disclaimers, context length note. No transcript. |
| AI in 2026 outlook | `corpus/ai-models/10270.md` | YouTube video description only. General AI news coverage. No substantive local-vs-hosted claims extractable. |
| GPT-5.1 feature extraction | `corpus/ai-models/01332.md` | 4 atoms: GPT-5.1 Instant/Thinking modes, instruction following improvements, planning gains, personalization presets. No local-vs-hosted comparison. |

---

*Compendium entry 10 of 21 -- ai-models*
*Crystallized: 2026-03-02*
*Remediated: 2026-03-02 — stripped unsupported claims per Adjudicator audit (8/8 issues)*
*Phase 3-4 enrichment: 2026-03-02 — "local is a toy" obsolescence noted; full supersession flagged as requiring richer sources*

# Neural Memory Architectures

## What the Sources Actually Say

Google published research on "Titans" and "MIRAS" (referenced as "Mira" in some coverage) under the framing of helping AI have long-term memory. A December 2025 Wes Roth video (09623.md) describes these as papers on long-term memory and "surprise" metrics in AI, linking to a Google research blog post titled "Titans + MIRAS: Helping AI have long-term memory." The video timeline notes a segment at 04:40 titled "Google Research: Titans, Mira & Long-Term Memory" and another at 06:00 titled "The 'Surprise' Metric: How AI Learns Like Humans." No transcript is available; the corpus file contains only the video description and metadata.

The source does not explain what Titans or MIRAS actually do architecturally, what the surprise metric measures, how it modulates attention, or what the claimed memory mechanism is. The entry in 09623.md is a brief description-level mention within a video covering multiple unrelated topics (Grok 4.20, OpenAI "Code Red," Google TPU sales, SpaceX data centers).

## Platform Memory Convergence (Verified)

The mid-January 2026 platform survey (08814.md) documents convergence across major AI platforms toward persistent and personalized memory features:

- **Gemini Personal Intelligence** (beta, January 14 2026): Opt-in feature connecting Gmail, Photos, YouTube, and Search for proactive, hyper-personalized responses. Described as bridging "memory gaps for Google users."
- **ChatGPT improved memory** (January 15 2026): Better detail recall from past chats for Plus/Pro users.
- **Claude project memory**: Described as project-scoped, with API enhancements bridging GUI-API gaps. "Memory remains project-scoped" per the survey.

The survey frames this as "convergence in memory architectures" across platforms, though the implementations described are external/session-level memory systems (connected apps, chat history recall), not architectural changes to model weights.

## What Is Not Supported by Sources

The following claims have no basis in the corpus files:

- Detailed mechanics of how Titans or MIRAS implement memory as learnable parameters
- The surprise metric as a specific mechanism for attention allocation
- Any claim about retrieval latency elimination
- Neural memory enabling long-term memory without long context windows
- RAG having a hard ceiling or being complementary to neural memory
- Convergence of Titans with Complementary Learning Systems neuroscience
- The context window arms race being misdirected
- Write-read asymmetry as a property of neural memory systems

---

## Syncrescendence Operational Notes

*Claims specific to Syncrescendence operations, not derivable from corpus sources.*

Agent memory in the constellation currently lives in external systems: project files, handoff documents, MEMORY.md. Whether future model architectures could internalize this state is an open architectural question that the current sources do not address.

---

## Source Provenance

| Source | File | Actual Content |
|--------|------|----------------|
| Wes Roth — Dec 2025 AI news roundup | `corpus/ai-models/09623.md` | Brief mention of Titans + MIRAS papers on long-term memory and surprise metrics; no transcript, no technical detail |
| Frontier AI platform survey (mid-Jan 2026) | `corpus/ai-models/08814.md` | Platform-level memory feature rollouts: Gemini Personal Intelligence, ChatGPT memory improvements, Claude project memory |
| Wes Roth — AI in 2026 outlook | `corpus/ai-models/10270.md` | Generic AI news video; no transcript, no technical content relevant to neural memory |

---

## Temporal Framing

### What the Sources Support (Platform Convergence Only)

The mid-January 2026 platform survey (08814.md) establishes a verifiable temporal signal: all three major frontier platforms — Gemini, ChatGPT, Claude — rolled out or upgraded persistent memory features within a two-day window in January 2026 (Gemini Personal Intelligence: January 14; ChatGPT memory: January 15; Claude project memory: ongoing). Simultaneous rollout by competitors indicates a convergence point — memory has crossed the threshold from differentiator to table stakes.

The direction of travel is clear from the source: platforms are moving from stateless (each conversation begins fresh) toward persistent (context accumulates across sessions). The mechanism differs by platform — Claude isolates per project, Gemini connects across apps, ChatGPT maintains a single memory store — but the direction is uniform.

### Obsolescence: The Stateless Session Assumption

Before persistent memory became standard, AI deployment assumed stateless sessions. Each conversation was independent. Users who wanted continuity had to manually re-inject context at the start of each session. Workflow designs built around this assumption include: preamble templates, "remind me what we were working on" prompts, and external note-keeping systems to bridge session gaps.

These workarounds are not yet obsolete — Claude's project memory is project-scoped and does not persist arbitrary cross-session context — but they are being progressively displaced. The obsolescence is in progress, not complete.

### Phase 3-4 Audit Note

Source material for this entry is severely limited. The Titans and MIRAS architectural papers are mentioned only in a brief video description (09623.md) with no transcript. No corpus file provides the technical depth needed to write a supersession chain for neural memory architectures at the model-weights level. The temporal framing above is drawn exclusively from the platform-level convergence documented in 08814.md — which concerns external/session memory features, not architectural changes to how models store information in weights.

A complete Phase 3-4 treatment of neural memory architectures (LSTM→attention→neural memory as weight update) requires corpus sources with transcript-level content on Titans, MIRAS, or comparable architectures. This entry cannot provide that without fabrication.

---

*Compendium entry 8 of 21 -- ai-models*
*Remediated: 2026-03-02 — stripped fabricated claims; entry reflects only source-supported content*
*Phase 3-4 enrichment: 2026-03-02 — platform convergence temporal framing added; architectural supersession flagged as requiring richer sources*

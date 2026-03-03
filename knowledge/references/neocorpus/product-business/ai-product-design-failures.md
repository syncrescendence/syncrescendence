# AI Product Design Failures: Local Maxima, Tool-Shaped Objects, and the Correctness Problem

> Most current AI products are Segways — technically impressive, enthusiastically funded, solving a problem nobody will frame the same way in five years.

## Sources

00255.md, 00269.md, 03856.jsonl, 03858.md, 01939.jsonl, 02577.md, 02592.md, 01395.md, 01393.jsonl

## The Local Maxima Problem

A local maximum is the highest point in your immediate vicinity — but only because you have not zoomed out enough to see the mountain behind you. The pressure to ship pushes every builder toward the nearest peak, not the tallest one. This is the entire AI industry right now (00255.md).

**Specific examples of local maxima** (00255.md):

- **Sora**: Generates stunning video, optimizing for a version of "content creation" defined before AI existed. Assumes the artifact is still a video. Nobody asks what replaces video entirely.
- **Perplexity**: Rebuilt search with citations and clean answers. Still requires you to ask a question and read a response. Made the horse faster; someone else will invent the car.
- **Open-weight models** (Mistral, LLaMA): Optimizing the transformer architecture, which is twelve years old. Everyone optimizes the engine of a vehicle whose chassis has not been questioned.

The historical pattern repeats: MapQuest digitized paper maps, then GPS-enabled phones changed the question entirely. Blackberry perfected mobile email, then the iPhone redefined what a phone was for. Every one was genuinely good. Every one optimized the right variable at the wrong altitude (00255.md).

**The uncomfortable truth**: When the environment shifts beneath your feet, the most legible improvements — the ones that feel like obvious progress — are almost always lateral moves along the current landscape, not the leap to a new one. The leap never feels like optimization. It feels like a weird left turn that only makes sense in retrospect (00255.md).

Genuine breakthroughs do not announce themselves in the language of the thing they replace. The smartphone was not marketed as a "better PDA." Google was not sold as a "better directory" (00255.md).

## Tool-Shaped Objects

A tool-shaped object fits in the hand the way a tool should. It produces the feeling of work — friction, labor, the sense of forward motion — but it does not produce work. Its function is to feel like a tool (00269.md).

**The market for feeling productive is orders of magnitude larger than the market for being productive.** Most people, most of the time, want to click and watch the number go up. They do not want to be told the number is fake (00269.md).

The current generation of LLM-driven agent systems is the most sophisticated tool-shaped object ever created. You can build an agent that reads email, summarizes contents, drafts a response, checks against a style guide, routes through approval, logs the interaction, and reports to a dashboard. The entire apparatus hums with the unmistakable energy of work being done. What is being done is the operation of the apparatus (00269.md).

**The critical nuance**: LLMs are also genuinely tools. They do real work. The line between the tool and the tool-shaped object is not a line but a gradient, and it shifts with every use case, every user, every prompt. You can only fail to notice when you have crossed from one side to the other (00269.md).

**The FarmVille analogy**: FarmVille is a command-and-control interface where no matter where you click, your farm expands and the number goes up. The direction of input is irrelevant. Productivity apps you configure for three weeks and never use, Notion workspaces with fourteen linked databases tracking a life that does not require tracking — these are all tool-shaped objects. The current AI boom is FarmVille at institutional scale. The quality that makes LLMs so effective as tool-shaped objects is their verbal fluency — an LLM can produce the sensation of anything (00269.md).

**The test**: Ask what the number is before making it go up (00269.md).

## The Correctness Problem

AI projects fail because "correctness" is undefined — this is a foundational architectural principle (01939.jsonl). Without a clear definition of what correct output looks like for a given domain, AI products cannot be evaluated, improved, or trusted. This is not a technical problem but a product architecture problem.

## Why Most Enterprise AI Products Fail

From 50+ enterprise AI deployments at OpenAI, Google, Amazon, and Databricks (02577.md):

- AI products fundamentally differ from traditional software in two key ways requiring different approaches
- Obsessing about customer trust and reliability is an underrated success driver
- Evaluations (evals) are not a universal solution; common misconceptions exist about their utility
- Start small, then scale up
- The Continuous Calibration, Continuous Development (CC/CD) framework enables iterative improvement
- Human control remains important in AI systems
- The Codex team's approach to evals and customer feedback provides a model

## AI-Native Business Models

Certain business models are entirely dependent on the existence and capabilities of AI — they could not exist without it (02592.md). These represent new categories, not improvements to existing ones.

## Antipatterns & Lessons

- **Optimizing the nearest peak**: Ship pressure drives builders to the local maximum. Zoom out. The gold rush is loud but the landscape is still forming (00255.md).
- **Confusing activity for output**: Token consumption does not scale linearly to value produced. The relationship is, in most cases, a cloud, not a line (00269.md).
- **Building agents that observe agents that analyze agents**: The primary output of many agent systems is the existence of the system itself (00269.md).
- **Skipping correctness definition**: Without defining what "correct" means for the domain, AI products cannot improve and will fail (01939.jsonl).
- **Trusting polished output as evidence of work**: An LLM can produce the sensation of anything. Verbal fluency is not evidence of value creation (00269.md).

## Cross-References

- [Software Survival Framework](software-survival-framework.md) — what software architecture survives
- [AI Product Architecture](ai-product-architecture.md) — technical patterns for building AI products that work
- [Enterprise AI Adoption](enterprise-ai-adoption.md) — why enterprises struggle to capture value

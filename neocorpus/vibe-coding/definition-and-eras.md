# Vibe Coding: Definition and the Three Eras of Software
> Vibe coding is the practice of describing desired outcomes to AI and accepting generated code without fully understanding it — a practice born in the Software 3.0 era where prompts are programming, and one that is already being superseded by structured AI engineering.

## Sources
00078.md, 03097.jsonl, 03094.jsonl, 03277.jsonl, 03279.md, 03673.jsonl, 10282.md, 09685.md, 01336.jsonl, 09423.md

## The Term and Its Origin
Andrej Karpathy captured the essence: "There's a new kind of coding where you fully give in to the vibes, embrace exponentials, and forget that the code even exists" (10282.md). The term gained rapid adoption as an industry descriptor for a development approach where the builder describes what they want, the AI generates it, and the builder evaluates by running it — not by reading code (03097.jsonl, 10282.md).

By early 2026, vibe coding had gained acceptance even from prominent skeptics. Linus Torvalds and DHH both acknowledged its legitimacy (02638.jsonl, 02640.md, 10063.md). The term entered mainstream developer vocabulary as an emerging industry standard (03094.jsonl).

## The Three Eras Framework
Software development has passed through three distinct eras (00078.md, 03279.md):

- **Software 1.0** (1940s-2012): Traditional code. Humans write explicit instructions computers execute.
- **Software 2.0** (~2012): Neural networks. Weights and parameters program behavior instead of explicit code.
- **Software 3.0** (~2019, GPT-2 onward): Prompts. Natural language programs LLM behavior.

This framing positions vibe coding not as a fad but as the first native practice of Software 3.0. The analogy to the 1990s internet is explicit: businesses that ignored the internet are gone; people ignoring AI coding face the same outcome (00078.md).

## Vibe Coding vs. AI Engineering
A critical distinction emerged: vibe coding and AI engineering are not the same thing (00078.md, 10282.md).

**Vibe coding** = self-driving car. Enter destination, sit back. No planning, no review, no deep understanding. Best for prototypes, internal tools, personal projects, demos. The 30-second test: just you using it? Exists for months not years? Standard patterns? Vibe code it (10282.md).

**AI engineering** = driving with a co-pilot. Human strategy, AI implementation, rigorous review. Best for production systems, team codebases, anything with security, scale, or longevity. Addy Osmani's golden rule: "Never commit code you can't explain to someone else" (10282.md).

The decision matrix turns on five questions: Who's using this? How long will it exist? What if it breaks? Do I need to understand the code? How complex is the business logic? (10282.md). Answering "AI engineering" to even one question means engineering the whole thing.

## The Graduation Path
Vibe-coded projects follow a predictable lifecycle. Someone builds an app in a weekend, gets likes, then real users arrive — race conditions, bad schemas, duct-tape auth. Technical debt compounds. Every fix creates two new problems. This is the "vibe coding cycle" and it is a trap (00078.md).

The graduation path: export to GitHub, set up local dev, read the code, add tests, refactor incrementally, establish CI/CD. The mature approach is hybrid: vibe to explore, engineer to build (10282.md).

## The Levels Framework
Multiple sources converge on a leveled model of AI-assisted development:

- Olly Rosewell's 6 levels: hiring a team, manual coding, boilerplate strategy, auto-completions, vibe coding ("cooking with GAS"), God Mode with autonomous agents (01336.jsonl, 09423.md).
- Nate B Jones's 5 levels of AI coding: 90% of developers plateau at level 3. The gap between "dark factories" (StrongDM shipping production with no human-written code) and everyone else is the most important divide in tech (10982.md).

## The Bottleneck Shift
Historically, execution was scarce — having the idea was easy, building it was hard (03433.jsonl). Vibe coding inverted this. Code became cheap. The bottleneck moved upstream to vision, specification, taste, and judgment (00078.md, 10282.md, 10982.md). The people winning are not the ones prompting the most but the ones thinking the clearest (00078.md).

## Antipatterns & Lessons
- **Delegating decisions to AI** produces mediocre, undifferentiated software and causes the builder to lose understanding of their own codebase (00078.md).
- **Conflating vibe coding with AI coding** leads to production-quality expectations from prototype-quality process (00078.md, 10282.md).
- **Ignoring the graduation moment** — continuing to vibe code after a project gets serious, has paying users, or hits tool complexity limits (10282.md).
- **Chasing perfection in vibe mode** instead of accepting 80% and graduating to engineering for the remaining 20% (10282.md).

## Cross-References
- neocorpus/vibe-coding/dark-flow-and-metr-study.md (the perception gap)
- neocorpus/vibe-coding/overnight-autonomous-agents.md (the next evolution)
- neocorpus/vibe-coding/engineer-vs-vibe-coder.md (identity implications)

# AI Workflow, Adoption Barriers, and the Bottleneck Shift

## Sources
- `corpus/productivity-pkm/09805.md` — Claude in Chrome: How To Teach AI To Do ALL Your Work
- `corpus/productivity-pkm/09926.md` — The Transcript Method That Changed My 2026 Workflow (ChatGPT for meetings)
- `corpus/productivity-pkm/09557.md` — The $700 Billion AI Productivity Problem (a16z: measuring AI ROI)
- `corpus/productivity-pkm/10724.md` — Same AI, Same Task: Why Did Half the Users Get Dumber?
- `corpus/productivity-pkm/09874.md` — AI New Year's: The 10 Week AI Resolution
- `corpus/productivity-pkm/00075.md` — Stop Trying to Keep Up With Every AI Launch
- `corpus/productivity-pkm/02700.md` — Extraction: Bottleneck Model (15 atoms: shifted bottleneck thesis)
- `corpus/productivity-pkm/02968.jsonl` — Atom: AI productivity bottleneck shifted from capability to cognitive architecture
- `corpus/productivity-pkm/03042.md` — Extraction: Why employees quit AI after 3 weeks (6 atoms: adoption failure)
- `corpus/productivity-pkm/03540.md` — Extraction: How to Win When Everyone Has AI (16 atoms: amplification thesis)
- `corpus/productivity-pkm/03051.md` — Extraction: AI interpretability and thinking (9 atoms)
- `corpus/productivity-pkm/00951.md` — Essential AI Tools for Academic Research
- `corpus/productivity-pkm/02970.md` — Bottleneck shifted to cognitive architecture: engineering manager mindset, kill the contribution badge, systems thinking over tool optimization

## Core Thesis
AI tools are widely available but inconsistently effective. The bottleneck has shifted from AI capability to human cognitive architecture (02968, 02700). The $700 billion productivity problem (09557) is not that AI does not work but that organizations cannot measure whether it works, cannot train employees to use it effectively, and cannot distinguish between genuine productivity gains and the illusion of productivity. 80% of workers abandon AI tools within three weeks (03042). The differentiator is not the tool but the user's capacity for judgment, delegation, and quality assessment — management skills, not prompting skills.

## Key Frameworks

### 1. The Bottleneck Shift Model (02700, 02968, 02970)
Execution capacity is no longer the scarce resource. When AI can build features faster than meetings can discuss them ("Anthropic shipped Cowork in 10 days with four people"), the bottleneck moves downstream to clarity, ambition, and distribution (02700). "The meeting to discuss a feature now takes longer than building it." When a bottleneck is eliminated, it moves downstream — eliminating execution bottlenecks exposes decision and distribution bottlenecks. "Distribution is the moat when everyone can build." Source 02970 extends this with three concrete prescriptions: adopt an engineering manager mindset (supervise AI work rather than doing it yourself), kill the contribution badge (stop measuring personal code output and start measuring system output), and develop strategic deep diving across both technical and non-technical work. The key claim: "experience cannot be compressed at the speed one can build" — building is now cheap, but the judgment to know what to build still requires lived operational experience. What separates high-performers is systems thinking and fluid movement between altitudes of abstraction, not access to better tools.

### 2. Amplifier vs Diminisher Effect (10724, 03540)
Same AI, same task, divergent outcomes. 10724 documents the phenomenon: half the users got measurably worse. The BCG/Harvard research (cited in 03042) found that AI users performed worse on tasks outside the AI's capability frontier. The 03540 extraction provides the macro frame: AI amplifies differences — "good people become better and great people become unusually effective" — but it also amplifies weaknesses. AI is not a leveler; it is an amplifier.

### 3. The 80% Abandonment Pattern (03042)
80% of workers quit AI tools after three weeks. The skills that predict AI success are management skills, not prompting skills. Two integration patterns exist: "Centaur" (clear human/AI task division) and "Cyborg" (fluid human-AI collaboration). Organizations need a "judgment layer" — the ability to evaluate AI output — not more tool training. The "201 training gap" between basic awareness and effective integration is where most adoption fails.

### 4. The Measurement Gap (09557)
a16z's thesis: companies buying AI tools have no idea whether anyone is actually using them. The measurement infrastructure that unlocked internet advertising's trillion-dollar boom (attribution, analytics, ROI tracking) does not exist for AI productivity. Most productive employees hide their AI usage from management. Without measurement, companies cannot optimize adoption, cannot justify investment, and cannot distinguish between real and performative AI use.

### 5. Practical AI Workflow Patterns (09805, 09926, 09874)
Claude in Chrome (09805) demonstrates teaching AI to replicate complete workflows. The transcript method (09926) turns meeting recordings into structured assets. The 10-week resolution (09874) provides a structured AI adoption cadence. These are the ground-level implementations that succeed — specific, constrained, measurable use cases rather than general "use AI for everything" mandates.

### 6. Stop Keeping Up (00075)
The counter-pattern: trying to track every AI launch creates its own productivity drain. The recommendation is to pick tools, go deep, and ignore the rest. This directly addresses the "shiny tool syndrome" that drives the abandonment cycle.

## Synthesis
The sources construct a coherent diagnosis: AI capability has outrun human capacity to integrate it. The bottleneck shift (02700) explains why raw AI power does not translate to productivity. The amplifier effect (10724, 03540) explains why outcomes diverge. The abandonment pattern (03042) explains where adoption fails. The measurement gap (09557) explains why organizations cannot diagnose the problem.

The prescription across sources is consistent: stop training prompting, start training judgment. Build specific workflows (09805, 09926) not general AI fluency. Measure actual usage and outcomes (09557). Accept that AI amplifies existing capability rather than creating it (03540). The connection to the focus engineering entry (see `focus-engineering-deep-work.md`) is direct: if cognitive architecture is the bottleneck, then focus engineering and system design determine AI effectiveness more than tool selection does.

## Obsolescence and Supersession

**"Prompting training" as the primary AI upskilling intervention was falsified by the abandonment data.** The dominant organizational response to AI tool adoption was to train employees in prompting — workshops, prompt libraries, prompt engineering guides. The 80% abandonment-within-three-weeks finding (03042.md) is a direct refutation: organizations were solving for the wrong bottleneck. The skills that predict AI success are management skills (delegation, judgment, quality assessment), not prompting skills. Prompting is a tactic; the bottleneck is cognitive architecture. The supersession is training intervention design: stop training "how to prompt," start training "how to delegate and evaluate AI output."

**"AI is a leveler" was superseded by the amplifier finding.** The early democratization discourse treated AI as equalizing — giving less capable people access to capabilities previously reserved for the highly skilled. The BCG/Harvard research cited in 03042.md and the 10724.md documentation of "same AI, same task, half the users got dumber" falsified the leveling claim. AI amplifies existing differences: capable people become more capable, weak reasoners produce worse outputs at higher velocity. The supersession is the amplifier model — which changes the prescription entirely. Instead of rolling out AI uniformly and expecting convergence, organizations must invest in the underlying judgment capability that AI will amplify.

**"Self-reported AI usage" as a reliable metric was exposed by the measurement gap.** Organizations attempting to track AI adoption relied initially on self-report (survey questions: "do you use AI tools?"). The a16z finding (09557.md) — most productive employees hide their AI usage from management — invalidates self-report as a measurement methodology. The thing being measured (self-reported adoption) is inversely correlated with the thing being optimized for (genuine productivity gain from AI). The supersession is behavioral measurement: before/after task timing, output quality assessment, and usage telemetry rather than survey data.

**"The bottleneck was capability" — now falsified by the bottleneck shift.** The pre-2024 productivity bottleneck was AI capability itself — the tools were not good enough to be reliably useful. The 02700.md/02968.jsonl extraction documents the shift: execution capacity is no longer the scarce resource. Anthropic shipping Cowork in 10 days with four people means "the meeting to discuss a feature now takes longer than building it." The bottleneck has moved downstream to clarity, ambition, and distribution. Organizations still behaving as if capability is the constraint — buying more tools, adopting more models — are optimizing a bottleneck that moved.

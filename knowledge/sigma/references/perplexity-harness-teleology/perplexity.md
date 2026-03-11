# Perplexity Pro Harness Teleological Manual

*A research-grounded, adversarially honest framework for deploying Perplexity's seven operational modes with precision, based on independent practitioner testimony, comparative platform studies, and documented failure rates. Every capability claim is stress-tested against what practitioners actually report — not what Perplexity says about itself.*

---

## Foundational Constraint

Before the teleologies, a boundary condition must be stated plainly, because every prior framework collapsed by ignoring it: **Perplexity's harness is a research accelerant, not a reasoning engine, and certainly not a creation engine.** The tasks eliminated from this manual — polished professional drafting, creative expansion, nuanced arbitration, multimodal synthesis, code generation, and artifact production — are better executed in first-party apps. Routing them to Perplexity produces structurally inferior results. The harness earns its keep exclusively in the discovery, reconnaissance, and source-mapping phases of research workflows. Everything downstream belongs elsewhere.

This constraint also reframes the question of wrapper advantage. The correct question is not "what can Perplexity do?" but "what can Perplexity do that a researcher holding ChatGPT Pro, Claude Pro, Google One AI Premium, and Kimi paid cannot replicate even in combination?" That answer is narrower than vendors admit, more durable than skeptics acknowledge, and entirely research-specific.

---

## Part I — The Genuine Harness Advantages

Three structural capabilities survive every replication test. A fourth — Model Council — survives with significant caveats.

### 1. Proprietary index with domain-corpus routing (Focus modes)

This is the harness's primary non-replicable advantage and the one most consistently underestimated.

Perplexity operates a hybrid proprietary index of 200+ billion URLs built on Vespa.ai's vector-lexical infrastructure, backed by over 400 petabytes of hot storage, with an ML model predicting re-indexing cadence per URL at tens of thousands of updates per second (ByteByteGo architectural teardown, November 2025). This is architecturally independent from Bing (which powers ChatGPT's search), Brave Search (which powers Claude's web tool), and Google (which powers Gemini). Independent analysis by Whitehat SEO (February 2026, meta-synthesis of 50+ source studies) found that only 11% of cited domains overlap between platforms for identical queries. SE Ranking's 2,000-keyword empirical study confirmed the differentiation: Perplexity locks at exactly five displayed links per response 99.05% of the time, while ChatGPT swings from two to twenty-four — Perplexity's citation behavior is deterministic and auditable in a way no first-party app replicates.

But the index is not the primary advantage. The advantage is **user-selectable domain-corpus routing through Focus modes** — a feature with no equivalent in any first-party app.

**Finance mode** routes queries to SEC EDGAR (confirmed via the API parameter `search_mode: "sec"`), Morningstar premium research, FinChat.io earnings data, Quartr live transcripts refreshed within 15 minutes of earnings calls ending, and Unusual Whales options data. For an analyst or investor, the ability to query "What did the CFO say about margin guidance in the latest earnings call?" and receive an inline-cited answer drawn from the verified transcript — not secondary reporting — is genuinely impossible to replicate in ChatGPT or Claude. They would surface general web content. JD Semrau's "Ultimate Guide: Perplexity For Finance" (Substack) documented this distinction across dozens of financial queries; GlobalGPT's independent review confirmed the Finance mode's integration depth as genuinely unique at the $20/month tier. The limitation is equally clear: it does not replace Bloomberg for institutional workflows, offers no proprietary datasets, no real-time streaming, and no compliance infrastructure.

**Academic mode** routes to PubMed, Semantic Scholar, arXiv, IEEE Xplore, and ACM Digital Library. Academic librarian Aaron Tay (Medium) tested Perplexity restricted to academic domains against Elicit and Scite.ai, calling it "unreasonably effective" for synthesis-style literature questions. The University of Tennessee Knoxville library guide correctly limits the claim: the mode is effective for *answering natural-language questions across literature*, not for conducting systematic reviews requiring PRISMA compliance, exhaustive coverage guarantees, or reproducible search strategies. That distinction matters. Academic mode outperforms Google Scholar for "What does the literature say about X?" It does not outperform it for "Give me all papers on X published between 2019 and 2023."

**Patents mode** (launched October 2025) routes to USPTO, EPO, and WIPO with semantic matching across vocabulary boundaries. Charles Eldering, a patent professional, published the only rigorous independent benchmark (Substack, November 2025): on infringement detection, Perplexity missed two of three potentially infringing leads that Patlytics, Limestone, and PioneerIP caught; on prior art search, only 3 of 25 returned references overlapped with competing tools; and "the results looked more like a search of the specification than of the claims — a fatal distinction in invalidity analysis." Repeatability was poor across identical re-prompts. Eldering's verdict: reliable for invention disclosure drafting assistance and landscape orientation, unreliable for client-facing professional patent work.

### 2. Inline citation at claim level

Every sentence in a Perplexity response carries a numbered citation linked to a specific source document — not a cluster of references appended at the end. ChatGPT aggregates citations by paragraph or section. Gemini links inline but at coarser granularity. For research verification, this distinction is structural: Perplexity answers the question "which specific source supports this specific claim?" rather than "which sources informed this paragraph?" Qwairy's analysis of 118,101 answers confirmed 21.87 sources cited per Perplexity response versus 7.92 for ChatGPT. Hikemytraffic.com's cross-platform assessment: "On citation clarity and traceability, Perplexity is widely regarded as the current leader."

The critical caveat, documented across multiple independent studies: citation does not equal accuracy. The Tow Center for Digital Journalism's March 2025 study of 1,600 queries found Perplexity's error rate at 37% — the lowest among tested platforms, but still meaning more than one in three responses contain citation errors. The Stanford study found reference fabrication at approximately 26.6% of the time. Futurism (June 2024) documented Perplexity citing AI-generated spam content as factual sources. G2 reviewers (multiple, 2026) articulated the practitioner heuristic that has emerged: "Citation ≠ truth. The presence of sources creates a false sense of certainty if you don't click through." The advantage of inline citation is that it makes verification possible and efficient — not that it makes verification unnecessary.

### 3. Deep Research for cold-start domain reconnaissance

Perplexity's Deep Research executes autonomous multi-hop search loops — Stephen Smith (Substack, "Intelligence by Intent," November 2025) documented a single query triggering 145 web searches across 32 sources in under five minutes, producing a 6–9 page synthesis. ChatGPT Deep Research ran 11 searches across 23 sources in 21 minutes and produced a 20–31 page report. The economic profile: 500 Deep Research queries per day for Pro subscribers at $20/month, versus ChatGPT's 30 per month at the same price point.

Where Deep Research has genuine, practitioner-confirmed advantage is the **cold-start reconnaissance problem** — entering a domain unfamiliar enough that you don't yet know what to look for. Soundarya Jayaraman (G2, 2026) documented replacing an afternoon of manually analyzing 30+ marketing competitive intelligence blogs with a few Deep Research queries. A Hacker News commenter (item 46229488) built a travel research tool specifically on Perplexity's Deep Research API because "it actually cites real sources and pulls fresh data." SecondTalent's nine-test review found it excelled on localized market research, correctly identifying UAE payroll software companies with current 2024–2025 pricing.

The practitioner ceiling is equally well-documented. HN user "jaggs" (February 2025): "It's producing superficially good results, but there are actually no decent 'insights' integrated with the words. In other words, it's just a super search on steroids." HN user "tkgally" (April 2025), after months of parallel testing: ranked Gemini's Deep Research as deepest, OpenAI's as most incisive, Perplexity's as fastest-but-shallowest. Professor Craig Van Slyke ("AI Goes to College" Substack, February 2025) caught Perplexity fabricating a specific analytical "matrix" attributed to a named researcher — the researcher confirmed no such work existed. The consensus that has solidified: **Deep Research is where you start, not where you finish.** Amdad H (Medium) captured the workflow that practitioners have converged on: "I now use Perplexity for initial reconnaissance and ChatGPT for deep dives — a combo that's cut my research time by 60%."

### 4. Model Council — epistemic triangulation with correlated failure risk

Launched February 5, 2026, Model Council runs a query through three user-selected models simultaneously; a synthesizer model produces a structured comparison surfacing agreements, divergences, and unique contributions. Available only to Max subscribers ($200/month), web-only.

The conceptual advantage is real. R. Thompson (PhD, Medium/Bootcamp, February 2026): "The issue is not that models can't write or reason. The issue is that they can be wrong with the same rhetorical confidence they use when they're right." Structured divergence surfacing before a researcher commits to a conclusion is genuinely valuable, and the format — side-by-side with explicit disagreement markers — is unavailable in any first-party app. Generation Digital's assessment: it helps move from "a confident answer" to "a clearer level of confidence."

The correlated failure mode is serious and must constrain its use: all three Council models draw from Perplexity's same proprietary search index. Their agreement may reflect shared retrieval failure rather than independent epistemic convergence. A researcher manually querying Claude (Brave Search) and ChatGPT (Bing) would achieve genuinely *independent* source diversity — the 11% cross-platform domain overlap means multi-platform querying searches fundamentally different corpora, while Council searches the same corpus three times with different interpreters. Council is therefore not equivalent to multi-platform querying; it provides reasoning diversity, not source diversity. Use it to stress-test interpretations of a source set, not to verify source coverage. At $200/month, it belongs in high-stakes verification workflows only.

### What does not survive replication testing

**Spaces** provide persistent file storage, custom standing instructions, and collaborative access organized around research projects — with live web search integration that neither Claude Projects nor Custom GPTs match natively. David Haberlah (Medium, October 2024), after a direct hackathon comparison: "I used Perplexity Spaces for the research phase, leveraging web search for statistical information. Then moved to Claude Projects for content generation." The 32K token context window is the crippling constraint — versus Claude Projects' 200K–500K and NotebookLM's two million. DataStudios.org documents the degradation: as running total nears the window, Perplexity trims older turns, causing responses to ignore previously established constraints and restate definitions. Spaces work as lightweight organizational scaffolding for active research sessions, not as accumulative knowledge bases. The advantage exists but is narrower than prior frameworks claimed.

**Tasks** (scheduled recurring searches, max 10 for Pro) produce AI-synthesized monitoring summaries superior to Google Alerts (synthesized output versus raw links). Dibeesh KS (Medium, 2025) documented a genuine workflow win catching a niche compliance update. The gaps are structural: no adaptive deduplication, no "what's new since last time" intelligence, no failure reporting, no integration with external tools. Useful for lightweight signal monitoring; outperformed by purpose-built competitive intelligence platforms for professional workflows.

---

## Part II — Differential Harness Value

Harness amplification is mechanically simple once the harness is understood correctly: models gain amplification in direct proportion to how much their first-party interfaces lack search integration. The harness contributes search and domain routing. A model that already has sophisticated, deep search integration at home gains very little from Perplexity's wrapper. A model that is retrieval-weak or retrieval-absent at home gains the most.

**Claude Sonnet 4.6 — greatest amplification.** Claude natively searches through Brave Search, which is demonstrably shallow: Whitehat SEO found 86.7% citation overlap with Brave's top results, meaning Claude's web access is effectively a thin Brave wrapper. The model's native strengths — careful analysis, nuanced reading, textual precision — have been systematically retrieval-bottlenecked. Perplexity's harness removes that bottleneck by supplying a proprietary index, domain corpus routing, and Deep Research's multi-hop loops. Academic mode plus Claude Sonnet 4.6 pairs the best available corpus filter for scholarly sources with the model most capable of reading what that corpus surfaces. This claim is analytically derived rather than directly corroborated by practitioner testimony attributing Claude-as-harness-core to empirical workflow testing — but the mechanism is robust, and no practitioner evidence contradicts it.

**Kimi K2.5 — high amplification.** Kimi's native search is documented as shallow and inconsistent. Its always-on thinking is its defining characteristic, and that thinking engine benefits directly from having reliable web grounding supplied by the harness that it lacks natively. Kimi's training corpus also diverges most sharply from GPT and Claude's Western-dominated distributions, making it the highest-diversity addition to any multi-model research configuration. The always-on thinking constraint means Kimi should be reserved for invocations where that compute overhead is warranted — maximum-depth queries where cheaper alternatives would insufficiently explore the search results.

**GPT-5.4 — moderate amplification.** ChatGPT Pro already integrates Bing search natively, and GPT-5.4's search capability in its first-party app is among the strongest available. The marginal gain from Perplexity's wrapper is real but narrow: different index, different source pool (that 11% domain overlap), and the Focus mode routing unavailable in ChatGPT. Thinking mode gains more amplification than standard mode because it can apply visible multi-step reasoning to the search results Deep Research surfaces — but the first-party alternative is competitive enough that GPT-5.4's gain inside Perplexity is moderate, not transformative.

**Gemini 3.1 Pro — weakest amplification.** Gemini Advanced natively integrates Google Search — the deepest search integration of any first-party app, backed by the Google Knowledge Graph's 500 billion facts. The harness adds Focus mode routing and a different index, but Gemini's native search capability is already the closest approximation to what Perplexity provides. The residual edge is narrow: Perplexity's Finance mode data integrations (Quartr, FinChat, Morningstar) are not available in Gemini natively. When the research task specifically requires those financial corpora, Gemini inside Perplexity is justified. Otherwise, Gemini Advanced is the superior choice.

**Sonar — minimal amplification.** Sonar is Perplexity's native model, fine-tuned for search summarization and citation within this exact RAG pipeline. The harness is not additive to Sonar — it is Sonar's native environment. The Focus modes represent the primary amplification vector: Sonar operating in Academic or Finance mode is a different instrument than Sonar on open web. But "amplification from the harness" is the wrong frame for the model the harness was built for.

---

## Part III — The Seven Teleological Modes

Each teleology begins from the harness feature that justifies the invocation, then specifies the model as the optimal interpreter of what that feature produces. The principle is strict: if the task can be done as well or better in the model's first-party app, it should be done there. Every teleology here answers the question: why invoke *this model* inside Perplexity specifically, rather than in its native environment?

### Mode 1 — Sonar (no thinking mode)

**Primary domain:** Rapid cited reconnaissance across specific corpora.

**Harness mechanism:** Focus mode corpus routing paired with Sonar's native search optimization. Sonar + Academic routes to PubMed, Semantic Scholar, arXiv, IEEE Xplore, and ACM Digital Library, answering natural-language literature questions with inline-cited scholarly sources — no equivalent in any first-party app. Sonar + Finance routes to SEC EDGAR, earnings transcripts, and financial data integrations, answering market and corporate questions from primary financial sources. Sonar + Open Web is Sonar in its default habitat: fastest path from question to sourced answer within Perplexity's index.

Focus mode selection is the primary mechanism here, not model characteristics. Sonar is the correct model for Focus-routed queries because it was trained for exactly this retrieval-and-summarize function; premium models in Focus modes add reasoning overhead without adding retrieval quality.

**Canonical prompt pattern:** State the query precisely and briefly. If using Academic: "Focus: Academic — [precise research question]." If using Finance: the interface handles corpus selection; query as if speaking to a financial analyst with access to all SEC filings and earnings calls. No preamble, no role-setting — Sonar needs direction, not context.

**Decision rule:** Invoke Sonar when the output needed is a sourced answer, not an analysis. The test is: if the response can be evaluated primarily by checking whether the sources are real and relevant, this is Sonar's domain. If evaluating the response requires assessing reasoning quality, switch to a thinking-enabled model.

**Patents:** Sonar + Patents is the correct starting configuration for landscape orientation and invention disclosure assistance. For professional patent work — infringement analysis, prior art searches for validity proceedings — Eldering's benchmark indicates the tool is unreliable. Use Sonar to understand the terrain; use a professional tool for the work product.

---

### Mode 2 — GPT-5.4 (thinking off)

**Primary domain:** Real-time structured query synthesis where first-party search suffices but the research workflow is already inside Perplexity's index.

**Harness justification — stated honestly:** This is the narrowest teleology in the framework. GPT-5.4 natively integrates Bing search in ChatGPT Pro, and for most structured queries, that combination matches what Perplexity provides. The genuine justification for invoking GPT-5.4 standard inside Perplexity rather than its first-party app is **workflow continuity within a Perplexity research session** — when you have already built context in a Space, uploaded documents to the session, or generated a Deep Research output that needs synthesis by a capable general-purpose model without thinking overhead, switching to the first-party app incurs context-loss entropy that exceeds the marginal quality gain.

There is a secondary structural edge: GPT-5.4 inside Perplexity accesses Perplexity's index rather than Bing. For queries where the 11% domain divergence between indices matters — and it does matter when sources are niche, recent, or from domains Bing underweights — this is a genuine advantage.

**Canonical prompt pattern:** Reference the existing session context explicitly. "Based on the Deep Research output above, [specific structured question]." The model should be bridging from harness-generated source material to synthesized answer, not initiating fresh research from a blank context.

**Decision rule:** Use GPT-5.4 standard when the thinking overhead of GPT-5.4 Thinking is unnecessary for the query, but session continuity inside Perplexity makes switching to the first-party app more disruptive than the native quality edge is worth. This is the honest answer: a maintenance and continuity mode, not a capability-differentiated one.

---

### Mode 3 — GPT-5.4 Thinking (thinking on)

**Primary domain:** Multi-hop source evaluation and complex domain scoping via Deep Research.

**Harness mechanism:** Deep Research's autonomous search loop (up to 145 searches per invocation) paired with GPT-5.4 Thinking's visible chain-of-thought. The thinking mode adds query refinement intelligence to the search loop — it can reason explicitly about what the first round of results reveals, identify gaps, and formulate better second-round queries. This is most valuable when entering a research domain where you don't yet know enough to pre-specify the right questions, and where the gap-identification between search passes requires structured reasoning.

The visible chain-of-thought serves a secondary function for research: it makes the model's inference steps auditable, which means a researcher can identify where the reasoning departed from what the sources actually support — a failure mode that standard mode conceals.

**Canonical prompt pattern:** "Run Deep Research on [domain]. After retrieving initial results, identify the three most significant gaps or contradictions in the source landscape and formulate follow-up queries to resolve them. Show your reasoning between search passes." The instruction to surface gaps is critical; without it, Deep Research produces a synthesis, not an analytical map.

**Decision rule against Claude Sonnet 4.6 Thinking:** Both thinking modes can handle complex multi-step research tasks inside Perplexity. The differentiator is task character. GPT-5.4 Thinking is the right choice when the research involves mapping a landscape — understanding what exists, who claims what, where disagreements are. Claude Sonnet 4.6 Thinking is the right choice when the research involves evaluating a specific body of retrieved sources — reading them carefully for what they actually support versus what they claim to support. Architecture first, then textual analysis.

---

### Mode 4 — Gemini 3.1 Pro (thinking always active)

**Primary domain:** Financial data cross-referencing via Finance mode.

**Harness mechanism:** The narrow residual edge where Perplexity's Gemini wrapper outperforms Gemini Advanced natively is the Finance mode corpus: Quartr's live earnings transcripts (refreshed within 15 minutes of calls ending), FinChat.io data, Morningstar premium research, and SEC EDGAR integration. Gemini's native search pulls from Google, which does not provide this level of structured financial data aggregation. Gemini's always-on thinking mode, applied to financial synthesis tasks, can cross-reference contradictions between what a CFO said in a transcript versus what was filed in a 10-K versus what analysts wrote in Morningstar research — all within a single inference.

This is the honest statement of the teleology: narrow, Finance-mode-specific, and not compelling for most research tasks. For the majority of queries where the financial corpus routing is not required, Gemini Advanced at home is the superior tool. The always-on thinking means Gemini inside Perplexity is never fast; it is the deliberate, high-cost option within an already narrow use case.

**Canonical prompt pattern:** "Using Finance data sources: [specific cross-referencing question spanning earnings transcripts, SEC filings, and analyst research]." Specify which data types should be cross-referenced; Gemini's thinking mode will attempt to identify contradictions and inconsistencies across sources if the task is clearly framed as a reconciliation problem.

**Decision rule:** Invoke Gemini inside Perplexity only when the Finance mode corpus is essential to the query. If the financial research question can be answered from general web sources or from Gemini's existing knowledge, use Gemini Advanced natively. The Finance mode data integration is the only thing the harness provides Gemini that Gemini cannot better provide itself.

---

### Mode 5 — Claude Sonnet 4.6 (thinking off)

**Primary domain:** Scholarly literature question-answering via Academic mode.

**Harness mechanism:** Academic mode filters Perplexity's search to peer-reviewed sources across PubMed, Semantic Scholar, arXiv, IEEE Xplore, and ACM Digital Library. Claude Sonnet 4.6 standard brings careful reading and nuanced synthesis to what that corpus surfaces. The pairing works because Claude's native web access via Brave Search provides substantially weaker scholarly source coverage than Perplexity's Academic mode — Claude at home will surface preprints, blog posts summarizing studies, and secondary coverage alongside peer-reviewed sources, with no ability to filter to primary literature. Perplexity + Academic mode delivers the primary literature; Claude reads it well.

The thinking toggle is off here because the task is comprehension and synthesis of retrieved sources, not reasoning through uncertainty or multi-step inference. Standard mode produces cleaner, more directly synthesized outputs for literature questions where the primary challenge is reading and distilling, not deliberating.

**Canonical prompt pattern:** "Academic sources only: [specific literature question framed as a research question, not a broad topic]." The framing as a research question — "What mechanisms have been proposed for X?" rather than "Tell me about X" — directs Claude to structure its synthesis around the literature's claims rather than its own priors.

**Decision rule against Sonar + Academic:** Both modes use Academic corpus routing. The differentiator is complexity. Sonar answers literature questions quickly with inline citations; Claude Standard answers them more carefully, with more nuanced representation of what the literature actually supports versus what it merely suggests. Use Sonar when you need a fast literature-informed answer. Use Claude Standard when the answer requires representing scholarly consensus accurately — when precision about the state of the literature matters.

---

### Mode 6 — Claude Sonnet 4.6 Thinking (thinking on)

**Primary domain:** Source-critical analysis and epistemic verification of retrieved research material.

**Harness mechanism:** This is where the harness most materially amplifies Claude's native capability. Claude's thinking mode, supplied with a set of Perplexity-retrieved sources, can reason explicitly about what those sources actually support, where their claims are overstated relative to their evidence, where there are conflicts between sources that the synthesis has elided, and what would constitute a genuine gap in the evidentiary base. This is the research verification function — the pass that a careful researcher performs before trusting synthesized output. Model Council (Max tier) extends this function: Kimi K2.5's distinctive training corpus, combined with Claude Thinking's source evaluation, provides maximum reasoning diversity for high-stakes verification.

The thinking toggle must be on here because the task is explicitly deliberative — the researcher is not asking for a synthesis but for a critique of an existing synthesis. Standard mode would produce a cleaner-sounding answer; thinking mode produces a more honest one, including visible uncertainty.

**Canonical prompt pattern:** "Here is the Deep Research synthesis on [topic]. Evaluate it source by source: for each key claim, identify whether the cited source actually supports it, whether the synthesis overstates confidence, and what significant perspectives or sources are absent from this synthesis." The source-by-source instruction prevents Claude from producing a high-level summary of the synthesis rather than a critical reading of it.

**Decision rule against GPT-5.4 Thinking:** GPT-5.4 Thinking maps landscapes (what exists and where disagreements are). Claude Sonnet 4.6 Thinking reads sources (whether what exists actually supports what's being claimed). After GPT-5.4 Thinking has scoped a domain, Claude Sonnet 4.6 Thinking evaluates the specific sources that domain mapping surfaced. Sequentially, not interchangeably.

---

### Mode 7 — Kimi K2.5 (thinking always active)

**Primary domain:** Maximum-depth exhaustive research on well-scoped topics requiring sustained multi-hop inference.

**Harness mechanism:** Kimi K2.5's always-on thinking distinguishes it from GPT-5.4 and Claude Sonnet 4.6 in one critical, structural way: **it cannot be turned off.** This means Kimi should never be the model of first resort for straightforward research queries — the thinking overhead is wasted compute on questions that don't require it. The always-on constraint is simultaneously the reason to use Kimi and the reason to use it rarely: it performs maximum-depth exploration by default, making it cost-optimal for the specific class of queries where that depth is required rather than a premium option.

The harness amplifies Kimi precisely because Kimi's native first-party interface has shallow search. Perplexity supplies the web retrieval; Kimi's always-on thinking applies sustained multi-step inference to what is retrieved — identifying non-obvious connections between sources, pursuing implications across multiple retrieval passes, and maintaining reasoning coherence across a long sequence of search-inform-refine cycles. Its training corpus divergence (strongest among the five models on non-Western sources) makes it the optimal candidate for Model Council configurations where genuine epistemic diversity is the goal — Kimi's disagreements with GPT-5.4 and Claude are more likely to reflect genuine interpretive difference than theirs with each other.

The resource-inefficiency flag is real and must inform usage: if the research question can be answered by Sonar, Claude Standard, or GPT-5.4 standard without thinking, those modes are strictly preferable to Kimi on cost and latency grounds. Kimi's teleological niche is the question where you expect the answer to be non-obvious, where shallow search would miss the relevant material, and where sustained reasoning across multiple retrieved sources is required to reach a defensible conclusion.

**Canonical prompt pattern:** "Exhaustively research [well-scoped, specific topic]. Do not optimize for coverage speed — pursue depth over breadth. Identify connections between sources that are not explicit in the sources themselves, note where different sources' reasoning frameworks produce different conclusions on the same evidence, and flag where the retrieved literature appears incomplete." The anti-speed instruction is critical; it signals that thinking depth should not be compressed to produce faster output.

**Decision rule:** Invoke Kimi when the research question meets three conditions simultaneously: (1) the topic is specific enough that exhaustive coverage is achievable, (2) the expected answer is non-obvious enough that multi-step inference will be required to reach it, and (3) the time budget allows for the always-on thinking overhead. If any condition fails, use a faster mode.

---

## Part IV — Anti-Patterns

The following failure modes are the most consequential and most consistently documented across practitioner reports. They are presented in order of how often they undermine research quality.

**Anti-pattern 1: Using Deep Research when Sonar + Focus mode dominates.** Deep Research is the highest-cost harness operation. Practitioners consistently invoke it reflexively for domain-specific questions that a Sonar + Finance or Sonar + Academic query would answer in seconds with better source precision. HN user "jaggs" (February 2025) captured the failure: "Super search on steroids" is what Deep Research provides when Sonar would suffice. The heuristic: if the query has a well-defined domain and a specific, answerable form, try Sonar + the appropriate Focus mode first. Deep Research is for when you don't yet know what you don't know.

**Anti-pattern 2: Treating Model Council as a default rather than a high-stakes instrument.** Model Council costs are Max-tier ($200/month) and the feature was five weeks old as of this writing with no peer-reviewed evaluation. Practitioners who use it as a default for routine queries pay in latency and cost for a feature whose primary value is stress-testing high-stakes conclusions. The correlated failure mode — all three Council models drawing from the same index — means Council on routine queries often produces three similar answers, not independent epistemic triangulation. The heuristic: invoke Council only when the stakes of a wrong conclusion are high enough to justify the cost, and when the query involves interpretation rather than fact retrieval (where shared index failure would affect all three models equally).

**Anti-pattern 3: Routing synthesis, drafting, and creation into Perplexity.** The harness is a research discovery tool. Multiple practitioners across G2, Reddit, and independent blogs have noted that Perplexity's prose is structurally inferior to Claude and GPT-5.4 in their native environments, its document production adds no harness-specific value, and its interface is not optimized for iterative creative or analytical refinement. David Haberlah's workflow: research in Perplexity Spaces, then export to Claude Projects for generation. XDA Developers documented the failure pattern: "Perplexity was my favorite AI tool. Then it started lying to me" — specifically in the context of trusting it for tasks requiring synthesis depth the harness does not provide. The heuristic: when the output is what you'll send, don't produce it in Perplexity.

**Anti-pattern 4: Trusting citations without clicking through.** The 37% error rate (Tow Center, March 2025) and 26.6% reference fabrication rate (Stanford study) are not edge cases. Perplexity's confidence calibration is inverted at the premium tier: Pro demonstrates a higher error rate than free Perplexity because the premium model is more willing to produce a definitive-but-wrong answer rather than declining. The practitioner heuristic, stated consistently across G2, Reddit, and independent reviews: inline citations establish what to verify, not verification itself. Every citation supporting a claim you will rely on must be clicked and read. This applies especially to academic and patent queries, where fabricated references have been documented by named researchers.

**Anti-pattern 5: Using thinking-enabled models for speed-sensitive queries.** GPT-5.4 Thinking and Claude Sonnet 4.6 Thinking add substantial latency. Practitioners report the most common waste pattern is toggling thinking on for queries that standard mode or Sonar would answer as accurately in a fraction of the time. The heuristic: thinking mode is warranted when the question requires visible deliberation — multi-step inference, gap identification, source critique — not when it requires a well-sourced answer to a specific question. Recency bias compounds this: Perplexity cites 82% of sources from content updated within 30 days (Whitehat SEO, 2026). A thinking model applying sustained inference to a recency-biased source set can produce a deeply-reasoned but systematically distorted output, because the reasoning quality cannot compensate for the source selection failure.

---

## Part V — Characterizations

These labels are cognitive handles — compact enough to navigate model selection in the moment, accurate enough to survive contact with the teleological reasoning above. They are grounded in the harness-specific functions established across Parts I–IV, not in the models' general market reputations.

**Sonar — The Domain Scanner.** Operates the harness in its native mode. Its value is not speed alone but corpus routing: in Academic or Finance mode it becomes an instrument unavailable elsewhere. When you need a sourced answer from a specific corpus, Sonar is what you reach for first.

**GPT-5.4 — The Session Continuator.** Honest about its narrow harness-specific justification: most valuable when session context inside Perplexity makes switching to ChatGPT Pro more disruptive than it's worth. Within an active research workflow, it bridges from what the harness surfaced to a structured synthesis.

**GPT-5.4 Thinking — The Landscape Cartographer.** Maps the terrain of a research domain through Deep Research. Finds what exists, where the disagreements are, what the gaps are. The output is a map for subsequent, more targeted investigation — not the investigation itself.

**Gemini 3.1 Pro — The Financial Cross-Referencer.** Justified narrowly by Finance mode's corpus integrations. Applies always-on thinking to reconciling contradictions across earnings transcripts, SEC filings, and analyst research. Outside Finance mode, Gemini Advanced natively is the better choice.

**Claude Sonnet 4.6 — The Literature Interpreter.** Reads what Academic mode surfaces with more care than Sonar and more speed than thinking mode warrants. The precision instrument for answering scholarly questions accurately from primary literature.

**Claude Sonnet 4.6 Thinking — The Source Auditor.** Performs the verification pass that converts research into reliable knowledge. Takes a synthesis produced by any other mode and evaluates it source by source for evidentiary adequacy. The final stage of any high-stakes research workflow before conclusions are trusted.

**Kimi K2.5 — The Deep Terrain Miner.** Reserved for well-scoped questions where the answer is non-obvious and shallow search would miss it. Always-on thinking makes it expensive by default — its use is a commitment to maximum-depth exploration. The epistemic diversity it brings to Model Council configurations is its secondary value: its disagreements with Western-corpus models reflect genuine training difference.

---

## Operational Summary

The Perplexity harness is a two-stage research instrument. Stage one is source discovery: Sonar with Focus modes for domain-specific retrieval, GPT-5.4 Thinking with Deep Research for complex landscape mapping, Kimi for maximum-depth terrain mining. Stage two is source evaluation: Claude Sonnet 4.6 standard for literature synthesis, Claude Sonnet 4.6 Thinking for adversarial source critique, Gemini specifically when Finance mode cross-referencing is required. Model Council extends the evaluation stage for high-stakes conclusions where reasoning diversity — not source diversity — is the marginal need.

Everything downstream of stage two: synthesis, drafting, creation, artifact production. That work belongs in first-party apps. The harness has done its job when the source map is reliable and the evaluation is complete. Hand it off.
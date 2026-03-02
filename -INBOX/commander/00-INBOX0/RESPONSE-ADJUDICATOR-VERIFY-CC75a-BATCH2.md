# Adjudicator Verification Pass (CC75a Batch 2)

**Repo**: https://github.com/truongphillipthanh/syncrescendence  
**Git HEAD**: `cc3dea17`  
**Verification date**: 2026-03-02  
**Scope**: 24 neocorpus entries in `neocorpus/ai-capability-futures/` and `neocorpus/philosophy-esoterica/`

Notes:
- Read each target entry in full.
- Read every source listed in each entry's `## Sources` block.
- Resolved one misrouted source: `01594.jsonl` exists under `corpus/ai-capability-futures/`, not `corpus/philosophy-esoterica/`.
- Also checked for body/source mismatches where the entry cited IDs not present in its own `## Sources` block.

### Entry 1: agi-timelines-predictions.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 1

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Functional AGI = "ability to figure things out"; long-horizon agents complete the third ingredient | 00023, 02625 | VERIFIED | Matches the Sequoia essay and extraction. |
| 2 | Main timeline cluster places AGI in the late 2020s and ASI later | 08441, 08479, 09656, 10160 | VERIFIED | Fair synthesis of the cited forecasts. |
| 3 | METR-style autonomous task duration is doubling roughly every 7 months, with day/year projections | 00023, 00257 | VERIFIED | Present directly in `00023`, with `00257` reinforcing the trend frame. |
| 4 | February 5, 2026 is framed as an inflection: GPT-5.3 Codex and Opus 4.6 arrived together; Codex was described as helping build itself | 00257 | VERIFIED | Supported by explicit language in `00257`. |
| 5 | "21 actions" lifestyle/finance thread is attributed to `00270, 03900` | 00270, 03900 | CITATION ERROR | `03900` supports the claim, but it is cited in-body and omitted from the entry's `## Sources` block. |

Orphan claims: no major orphaned section-level claims detected.  
Missing wisdom: `09506` contributes a more explicit "software-only singularity seems unlikely" constraint than the entry foregrounds.

### Entry 2: intelligence-explosion-recursive-improvement.md

**Overall verdict**: CLEAN  
**Claims checked**: 5  
**Issues found**: 0

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Intelligence explosion is a feedback loop captured by the R&D progress multiplier | 08441 | VERIFIED | Core content of the Kokotajlo/Alexander note. |
| 2 | GPT-5.3 Codex crossed an operational self-improvement threshold; AI is now writing substantial AI-lab code | 00257 | VERIFIED | Supported by the quoted Codex passage and surrounding argument. |
| 3 | Physical constraints and real-world bottlenecks prevent a pure vertical software-only singularity | 03534, 09506 | VERIFIED | Both sources argue for material/world constraints. |
| 4 | Current AI is stronger at optimization than true paradigm-breaking discovery | 00147, 03501 | VERIFIED | This is Buehler's central thesis. |
| 5 | A more "boring," compounding singularity remains a live scenario | 10134, 09925, 09877 | VERIFIED | Fairly represented. |

Orphan claims: none detected.  
Missing wisdom: `03534` gives a much richer "compressed century" upside account than this entry preserves.

### Entry 3: post-agi-futures-civilizational-vision.md

**Overall verdict**: CLEAN  
**Claims checked**: 5  
**Issues found**: 0

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Amodei's optimistic frame is a "compressed century" in biology, neuroscience, growth, and some governance domains | 03534, 10537 | VERIFIED | Strongly supported by both the extraction and the essay. |
| 2 | Mid-2027 is a civilizational branch point with good / deteriorating / takeover paths | 08441 | VERIFIED | Directly present in `08441`. |
| 3 | Post-AGI business structure collapses toward a few durable company types; agent-to-agent coordination changes product design | 10906, 10891 | VERIFIED | Fair synthesis of the cited threads. |
| 4 | The singularity may feel gradual and normalizing rather than cinematic | 10134, 02226 | VERIFIED | Well supported. |
| 5 | Material abundance does not solve the meaning problem | 03534 | VERIFIED | Amodei explicitly treats work/meaning as a hard residual problem. |

Orphan claims: none detected.  
Missing wisdom: `10342` adds a more explicit longtermist governance-preparation frame than the entry surfaces.

### Entry 4: agi-governance-geopolitical-race.md

**Overall verdict**: CLEAN  
**Claims checked**: 5  
**Issues found**: 0

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | The core governance dilemma is nationalization vs private anarchy | 08441 | VERIFIED | Directly supported. |
| 2 | US-China race dynamics structurally pressure speed over safety; Amodei proposes a supply-chain-focused democratic entente | 08441, 03534 | VERIFIED | Accurate synthesis. |
| 3 | US institutional responses include Pentagon preparation, federal-preemption fights, and insurer concern about correlated AI risk | 09640, 09700, 09524 | VERIFIED | Supported by the cited descriptions/extractions. |
| 4 | Cronin and Kyle Hill represent important skeptical / prohibitionist counterpositions | 09905, 03129, 10349 | VERIFIED | Correctly attributed. |
| 5 | Regulatory timelines are misaligned with model timelines measured in months | 08441, 09640, 09700 | VERIFIED | Fair synthesis from the cited materials. |

Orphan claims: none detected.  
Missing wisdom: `09582` and `09670` carry more explicit democratic-fragility framing than the entry preserves.

### Entry 5: agi-skepticism-counternarratives.md

**Overall verdict**: CLEAN  
**Claims checked**: 5  
**Issues found**: 0

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Manidis's "tool-shaped object" critique targets AI systems that produce the feeling of work more than real work | 03867 | VERIFIED | Central source claim. |
| 2 | Buehler's critique is that closed-system learning suppresses genuine discovery | 00147 | VERIFIED | Directly supported. |
| 3 | Israetel and Cronin anchor opposing poles in the embodiment debate | 08479, 09905 | VERIFIED | Accurately summarized. |
| 4 | The "boring singularity" / normalization critique is a serious counternarrative, not dismissal of progress | 10134, 02226 | VERIFIED | Supported. |
| 5 | Spending/usage metrics can be detached from output/value creation | 03867 | VERIFIED | Directly present in the source. |

Orphan claims: none detected.  
Missing wisdom: `09614` contributes a more explicit critique of overconfident AGI discourse than the entry captures.

### Entry 6: scaling-laws-trajectories.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 1

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Capability is better modeled on two axes: task complexity and sustained time horizon | 08442, 02091 | VERIFIED | Strong support. |
| 2 | Clean reward signals explain why code/math progress faster than open-ended work | 08442, 02205, 02091 | VERIFIED | Central thesis of `08442`. |
| 3 | The field is moving from an age of scaling to an age of research | 01539, 09526 | VERIFIED | Explicitly supported. |
| 4 | Neuralese / THAT-vs-WHY / inference bottleneck together define a major interpretability and deployment constraint | 08442 | VERIFIED | Accurate. |
| 5 | Frontier-model milestone paragraph cites `09700` for GPT-5.2 benchmark standing | 01863, 09700 | CITATION ERROR | `09700` is cited in-body but omitted from the entry's `## Sources` block. |

Orphan claims: none detected.  
Missing wisdom: `10902` adds a clearer "rewrite all software" thesis than the entry fully integrates.

### Entry 7: ai-market-investment-dynamics.md

**Overall verdict**: CLEAN  
**Claims checked**: 5  
**Issues found**: 0

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Compute has become a board-level strategic weapon with tiered access dynamics | 00199 | VERIFIED | Matches the source closely. |
| 2 | The current wave is framed as real infrastructure buildout, not a pure valuation bubble | 09353, 09374, 10037, 10306 | VERIFIED | Fair synthesis. |
| 3 | Claude Cowork plugin news triggered a large SaaS/legal/IT selloff ("SaaSpocalypse") | 03606 | VERIFIED | Direct support. |
| 4 | The durable battle is over the distribution/platform layer, not isolated features | 04308 | VERIFIED | Supported by the source's platform-lock-in framing. |
| 5 | US-China compute/talent dynamics and insurer exclusions are meaningful market signals | 09353, 09695, 09524 | VERIFIED | Accurate. |

Orphan claims: none detected.  
Missing wisdom: `10449` and `09487` add more concrete chip-supply and ASIC-competition nuance than the entry keeps.

### Entry 8: ai-labor-displacement-historical-pattern.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 1

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Bastiat's seen/unseen framework is the right starting point for AI labor panic | 00262 | VERIFIED | Directly supported. |
| 2 | The entry's historical examples (Luddites, ATMs, barcodes, e-discovery, spreadsheets) broadly support "task shifts before job collapse" | 00262, 01449 | VERIFIED | Fair synthesis of the cited historical material. |
| 3 | Current quantitative picture: 57% automatable work hours, 80% median task-time savings, productivity acceleration, AI skill premium | 01593, 09540, 04107, 10839 | VERIFIED | Supported by the cited source set. |
| 4 | The K-shaped structure and tokenizable-cognition framing are real emerging patterns | 10012, 10839, 09847, 10438 | VERIFIED | Accurately grounded. |
| 5 | The quality-crisis paragraph relies on `00233`/`00142` cross-references not listed in `## Sources` | 00140, 00233, 00142 | CITATION ERROR | The claims may be true, but the entry cites body-only sources outside its declared source list. |

Orphan claims: no major additional orphan sections detected.  
Missing wisdom: `09608` emphasizes skill-overlap limits and deep-skill atrophy more strongly than the entry does.

### Entry 9: post-labor-economics.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 1

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Post-labor is economic refactoring, not automatic collapse | 08472 | VERIFIED | Core source thesis. |
| 2 | Post-labor does not eliminate scarcity because scarcity collapses to physical constraints | 08472 | VERIFIED | Direct support. |
| 3 | Firms persist because capital-risk management and economies of scale remain scarce | 08472 | VERIFIED | Well supported. |
| 4 | Robot deployment lags cloud-agent capability, so human physical labor remains needed in the near term | 00151 | VERIFIED | Directly argued in the source. |
| 5 | "AI-created businesses already hiring humans" cites `10726`, which is not in the source list | 10726 | CITATION ERROR | The claim may be source-grounded elsewhere, but `10726` is cited in-body and omitted from `## Sources`. |

Orphan claims: none beyond the citation mismatch above.  
Missing wisdom: `09601` contributes a richer distribution/deflation tension than the entry retains.

### Entry 10: human-ai-productivity-augmentation.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 1

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | The winning pattern is orchestration under human architectural ownership, not blind vibe coding | 00233 | VERIFIED | Strongly supported. |
| 2 | The 2026 tool stack, MCP wiring, persistent `claude.md`, and repository-context patterns are real productivity levers | 00233 | VERIFIED | Direct support in the source. |
| 3 | Executive/high-context augmentation yields much smaller gains than operational/coding augmentation | 10870, 10186 | VERIFIED | Accurate synthesis of the contrast. |
| 4 | Token-use data, professional sentiment, and "riot if removed" coding-tool dependence all support a real adoption shift | 01791, 09620, 01812 | VERIFIED | Supported. |
| 5 | Final antipattern bullet cites `03855`, which is not in the entry's `## Sources` block | 03855 | CITATION ERROR | Body/source mismatch. |

Orphan claims: none beyond the citation mismatch above.  
Missing wisdom: `03777` contains a sharper human-computer-interface argument than the entry's brief UI section.

### Entry 11: human-competitive-advantage-ai-era.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 1

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Rarity comes from overlapping top-quartile skills plus commercialization ability | 00142 | VERIFIED | Central thesis of the source. |
| 2 | Specialization-only career advice is obsolete; polymathic integration matters more | 02850, 03855 | VERIFIED | Fair synthesis. |
| 3 | Jobs are bundles of tasks; AI acts as amplifier more than equalizer | 00142 | VERIFIED | Well supported. |
| 4 | Wisdom/deep knowledge and value creation cannot be delegated to credentials or shallow tooling | 04038, 01104 | VERIFIED | Supported. |
| 5 | The five-level AI-native maturity model uses `03879`, which is cited in-body but omitted from `## Sources` | 03879 | CITATION ERROR | Clear body/source mismatch. |

Orphan claims: none beyond the citation mismatch above.  
Missing wisdom: `02442` contains a stronger agency/learned-helplessness frame than the entry ultimately preserves.

### Entry 12: physical-ai-robotics.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 1

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Physical AI is the fourth wave after perception/generative/agentic AI | 00912 | VERIFIED | Directly supported. |
| 2 | Physical-AI progress is bottlenecked by real-world data and world-model/simulation pipelines | 00912, 01146 | VERIFIED | Accurate. |
| 3 | Simulation, digital twins, and synthetic data are central accelerants | 00912 | VERIFIED | Strong support. |
| 4 | Zipline, autonomous vehicles, and human-robot comfort zones illustrate real deployment constraints | 02916, 02914, 03939, 01374 | VERIFIED | Fair synthesis. |
| 5 | SIMA 2 / ARC-v3 evaluation claims cite `01284` and `09332`, which are not in the entry's `## Sources` block | 01284, 09332 | CITATION ERROR | Body/source mismatch for a substantive capability-eval paragraph. |

Orphan claims: none beyond the citation mismatch above.  
Missing wisdom: `01227_from_infrastructure` adds a more explicit compute-substrate argument than the entry's brief alternative-hardware section.

### Entry 13: agent-evals-capability-benchmarks.md

**Overall verdict**: CLEAN  
**Claims checked**: 5  
**Issues found**: 0

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Agent evals differ in kind from model evals; graders/transcripts/trials matter | 00020 | VERIFIED | Exact Anthropic framing. |
| 2 | Chollet's metric is skill-acquisition efficiency, and ARC v3 operationalizes that more interactively | 09332, 09598 | VERIFIED | Supported. |
| 3 | Benchmark saturation and grader bugs routinely masquerade as capability ceilings | 00020 | VERIFIED | Directly supported. |
| 4 | `pass@k` and `pass^k` measure different product realities under non-determinism | 00020 | VERIFIED | Accurate. |
| 5 | There is a genuine tooling/agent-innovation stagnation critique, despite some architectural divergence | 10863, 10918 | VERIFIED | Fair synthesis. |

Orphan claims: none detected.  
Missing wisdom: `09545`/`09519` provide a stronger benchmark-to-science-impact arc than the entry's short AlphaFold comparison.

### Entry 14: democratization-open-models.md

**Overall verdict**: CLEAN  
**Claims checked**: 4  
**Issues found**: 0

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Open models closing to parity in ~3 months underwrite a moatlessness thesis | 08474 | VERIFIED | Directly stated. |
| 2 | Printing press -> internet -> AI is presented as an accelerating democratization cascade | 08474 | VERIFIED | Supported by the source. |
| 3 | AI is framed as a transparency technology that destroys intellectual gatekeeping | 08474 | VERIFIED | Direct support. |
| 4 | The source supports the Year Zero / Agents / Robots / Superintelligence staging and "adapt or die" frame | 08474 | VERIFIED | Present in `08474`. |

Orphan claims: none detected.  
Missing wisdom: `02464` contributes almost no conceptual depth beyond lightweight modality/open-model examples.

### Entry 15: consciousness-hard-problem.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 1

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Nagel's formulation treats consciousness as irreducibly subjective and not capturable by objective physical description | 09277, 01099, 01101 | VERIFIED | Strong support. |
| 2 | The Damasio/Chalmers/Gleiser panel is accurately described as an interdisciplinary confrontation over the hard problem | 10210, 02913 | VERIFIED | Fairly represented. |
| 3 | Hoffman's interface theory says evolution tracks fitness, not truth; spacetime is interface-like | 09319, 01168, 01180 | VERIFIED | Supported. |
| 4 | Penrose/Fuentes material is accurately described as probing gravity/quantum-collapse ideas with BECs | 09808, 02149, 02151 | VERIFIED | Supported. |
| 5 | The plant-intelligence / Levin / avian-consciousness / OMNI-gradualism block cites many IDs not listed in `## Sources` | 01123, 01125, 01906, 01908, 02289, 02851, 02853, 03382, 03384, 09291, 09555, 10471 | CITATION ERROR | Large body/source mismatch: the section relies on uncatalogued sources outside the declared source set. |

Orphan claims: no major additional orphan sections detected beyond the mismatched citation block above.  
Missing wisdom: `09976`/`02505` give a stronger "mystical experience as evidence?" tension than the entry's brief treatment.

### Entry 16: panpsychism-idealism.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 1

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Kastrup's analytic idealism is presented as consciousness-first metaphysics, with Levin/Koch used as adjacent empirical support | 09279, 01107 | VERIFIED | Fair synthesis. |
| 2 | Faggin's quantum-consciousness and self-knowing-universe claims are accurately summarized | 10225, 09725 | VERIFIED | Supported. |
| 3 | Francis Lucille is correctly used as an Advaita/non-duality source | 09663, 01867, 01869 | VERIFIED | Supported. |
| 4 | Swami Sarvapriyananda is correctly used to frame Atman/Brahman identity and non-dualism | 10911, 04177, 04179 | VERIFIED | Supported. |
| 5 | `01828.jsonl` appears unrelated to the entry's actual claims and functions as a miscited source in the source list | 01828 | CITATION ERROR | The file content is about AI/metabolic-rift language, not panpsychism/idealism. |

Orphan claims: none detected.  
Missing wisdom: `10264` adds a broader embedded-cognition/faith bridge than the entry fully develops.

### Entry 17: ai-consciousness-debate.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 2

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Reid Hoffman argues consciousness is unnecessary for intelligence and AI companions are not friends | 08452, 09322 | VERIFIED | Supported. |
| 2 | Kastrup's "AI is not a mind" section relies on body-cited `09279`, which is omitted from `## Sources` | 10524, 09279 | CITATION ERROR | `10524` alone is too thin for the full argument as written; the body reaches for `09279` but the source list omits it. |
| 3 | IIT is fairly summarized as denying consciousness to standard digital computers/LLMs while tying consciousness to integrated architecture | 04003, 04005 | VERIFIED | Supported. |
| 4 | Penrose/Fuentes quantum-consciousness discussion cites `09808`, which is omitted from `## Sources` | 02988, 09808 | CITATION ERROR | Body/source mismatch. |
| 5 | Aguera y Arcas's functional/self-modeling position is accurately represented | 09290, 09296, 01134 | VERIFIED | Supported. |

Orphan claims: the Tegmark/suffering tension in the open-questions section is uncited.  
Missing wisdom: `09310` contributes a sharper governance/ontology critique of "AGI" as a distributed ecosystem than the entry fully preserves.

### Entry 18: metaphysics-ontology-existence.md

**Overall verdict**: CLEAN  
**Claims checked**: 5  
**Issues found**: 0

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | O'Connor/Stevens are correctly used to frame mereological nihilism and basic ontological skepticism | 09553, 01612, 01614 | VERIFIED | Supported. |
| 2 | Van Fraassen is accurately tied to constructive empiricism and anti-realist self questions | 09788 | VERIFIED | Fairly represented. |
| 3 | Wolfram's Ruliad / observer-sampling frame is accurately summarized | 09724, 09792 | VERIFIED | Supported. |
| 4 | Deutsch is used correctly to distinguish pattern-matching AI from explanatory AGI and constructor theory | 08447, 09301, 01140 | VERIFIED | Strong support. |
| 5 | The section on Godel, quantum philosophy, and meta-narrative schemas is a fair synthesis of the cited mathematical/quantum sources | 09862, 09917, 08450, 09317, 01167, 04468, 04470, 02382, 02116, 02118 | VERIFIED | Broad but source-grounded. |

Orphan claims: none detected.  
Missing wisdom: `09924`'s process-philosophy account of free will is richer than the short section here.

### Entry 19: cosmos-origins-evolution.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 1

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Dark energy and the Hubble tension are accurately presented as major cosmological puzzles | 09741, 01999, 02001 | VERIFIED | Supported. |
| 2 | The Fermi-paradox / hard-steps / anthropic-rarity framing is fairly summarized | 09472, 01458, 09621, 01753, 01755 | VERIFIED | Supported. |
| 3 | Nick Lane and panspermia sections are accurate at a high level | 10127, 02754, 02629, 02631 | VERIFIED | Supported. |
| 4 | Noble/biological-relativity, Weinstein/evolutionary-trap, and Henrich/cultural-evolution sections are source-grounded | 09542, 01596, 01594, 09631, 01783, 01785, 01084, 01086 | VERIFIED | Supported; `01594` was read from its actual misrouted location. |
| 5 | Assembly-theory subsection cites `02382`, which is omitted from `## Sources`; the source list also points to misrouted `01594` | 08443, 02382, 01594 | CITATION ERROR | One body/source mismatch and one path-resolution issue. |

Orphan claims: none beyond the citation/path hygiene issue above.  
Missing wisdom: `08440`/`04281` add a stronger planetary-computation bridge to AI than the entry's short closing section.

### Entry 20: intelligence-computation-life.md

**Overall verdict**: CLEAN  
**Claims checked**: 5  
**Issues found**: 0

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Aguera y Arcas's five-paradigm frame is accurately rendered: brains as computation, intelligence as prediction, consciousness as self-modeling, etc. | 09290, 09296, 01134 | VERIFIED | Strong support. |
| 2 | The entry's "life is computational" section is grounded in the cited Aguera/Walker material | 09296, 01134, 08443, 09283, 01108 | VERIFIED | Fair synthesis. |
| 3 | Major evolutionary transitions are correctly framed as symbiogenesis/information-transmission changes | 09296, 01134 | VERIFIED | Supported. |
| 4 | Assembly theory and lineage-as-unit-of-life are accurately attributed to Walker | 08443, 09283, 01108 | VERIFIED | Supported. |
| 5 | Kempes, Bratton, and Zhao are fairly used to extend the argument to universal-life principles and planetary computation | 08454, 09325, 08440, 04279, 04281 | VERIFIED | Supported. |

Orphan claims: none detected.  
Missing wisdom: `08454` contributes a sharper materials/constraints/principles distinction than the entry emphasizes.

### Entry 21: stoicism-ethics-meaning.md

**Overall verdict**: CLEAN  
**Claims checked**: 5  
**Issues found**: 0

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Stoicism is correctly presented as a full system of logic, physics, and ethics rather than emotional suppression | 10522, 03457, 03459, 09380, 01249, 01251 | VERIFIED | Supported. |
| 2 | Existential-crisis / Sisyphus / grammar-trap framing is accurately represented | 09314, 01161, 09429 | VERIFIED | Supported. |
| 3 | Nietzsche's genealogy section is a fair summary of master/slave morality, asceticism, and will to power | 09262 | VERIFIED | Supported. |
| 4 | The Buddhist identity-transformation block is grounded in the cited karma/anatta source | 02364 | VERIFIED | Supported. |
| 5 | Emotivism and Douthat's literary-theological reflection are accurately summarized | 09760, 10241, 09801 | VERIFIED | Supported. |

Orphan claims: none detected.  
Missing wisdom: `10522` gives more historical detail on Stoicism's three eras than the entry carries through.

### Entry 22: esoteric-mystical-traditions.md

**Overall verdict**: FINDINGS  
**Claims checked**: 5  
**Issues found**: 2

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Witchcraft is accurately tied to early modern philosophy's disenchantment shift | 09320, 01171, 01173 | VERIFIED | Supported. |
| 2 | Flood-myth and "Bible is weirder than standard pedagogy suggests" sections are source-grounded | 09672, 10101 | VERIFIED | Supported. |
| 3 | Nicholas of Cusa's learned ignorance / infinity / religious diversity section is accurate | 09802, 02116, 02118 | VERIFIED | Supported. |
| 4 | The Hermetic-Kabbalistic "reality programming" synthesis overstates what the source set establishes | 10122 | DISTORTED | `10122` supports a contemporary self-programming essay, but the entry broadens this into a stronger Hermetic/Kabbalistic + quantum/neuroscience synthesis than the source directly warrants. |
| 5 | The open-question line about disenchantment cites `09413`, which is not in `## Sources` | 09413 | CITATION ERROR | Body/source mismatch. |

Orphan claims: no major additional orphan sections detected.  
Missing wisdom: `01066` on ancient Greek mysticism is absent from the entry despite being a meaningful source for the folder theme.

### Entry 23: transhumanist-suffering-abolition.md

**Overall verdict**: FINDINGS  
**Claims checked**: 4  
**Issues found**: 2

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Pearce is correctly framed as a transhumanist advocate of ending suffering, and the four-pillar future frame is supported | 09260, 01069, 01071 | VERIFIED | Supported at the high level. |
| 2 | Foresight Institute is fairly used as the institutional setting around the discussion | 01071 | VERIFIED | Supported. |
| 3 | The "philosophical architecture" section adds detailed claims about fitness functions, neurochemical tractability, paradise engineering, and suffering's contingency that do not appear in this tiny source set | 09260, 01069, 01071 | UNSUPPORTED | The sources do not substantiate this detailed premise stack. |
| 4 | `01060.jsonl` is unrelated to Pearce/transhumanist suffering abolition | 01060 | CITATION ERROR | It is an Emerald Tablet / occult-philosophy source, not a Pearce/abolition source. |

Orphan claims: the open-questions section ranges well beyond the four-source basis.  
Missing wisdom: the source set itself is thin; the entry would need stronger Pearce-specific material to support the deeper philosophical scaffolding.

### Entry 24: meaning-faith-permeability.md

**Overall verdict**: CLEAN  
**Claims checked**: 4  
**Issues found**: 0

| # | Claim (abbreviated) | Source Cited | Verdict | Notes |
|---|---------------------|-------------|---------|-------|
| 1 | Meaning is framed as a metacognitive gradient arising from cross-scale coupling | 10264 | VERIFIED | Direct support. |
| 2 | Faith is presented as irreducible because embedding is irreducible | 10264 | VERIFIED | Direct support. |
| 3 | Kingsnorth is accurately used for the "war against human nature" technology critique | 09413 | VERIFIED | Supported. |
| 4 | The closing tensions about naturalism, credulity, and technology are fair syntheses of the two-source set | 10264, 09413 | VERIFIED | Reasonable and grounded. |

Orphan claims: none detected.  
Missing wisdom: `10264` includes a longer formal-argument appendix and phenomenology-of-faith framing than the entry retains.

## Summary

| # | Entry | Claims | Issues | Verdict |
|---|-------|--------|--------|---------|
| 1 | agi-timelines-predictions.md | 5 | 1 | FINDINGS |
| 2 | intelligence-explosion-recursive-improvement.md | 5 | 0 | CLEAN |
| 3 | post-agi-futures-civilizational-vision.md | 5 | 0 | CLEAN |
| 4 | agi-governance-geopolitical-race.md | 5 | 0 | CLEAN |
| 5 | agi-skepticism-counternarratives.md | 5 | 0 | CLEAN |
| 6 | scaling-laws-trajectories.md | 5 | 1 | FINDINGS |
| 7 | ai-market-investment-dynamics.md | 5 | 0 | CLEAN |
| 8 | ai-labor-displacement-historical-pattern.md | 5 | 1 | FINDINGS |
| 9 | post-labor-economics.md | 5 | 1 | FINDINGS |
| 10 | human-ai-productivity-augmentation.md | 5 | 1 | FINDINGS |
| 11 | human-competitive-advantage-ai-era.md | 5 | 1 | FINDINGS |
| 12 | physical-ai-robotics.md | 5 | 1 | FINDINGS |
| 13 | agent-evals-capability-benchmarks.md | 5 | 0 | CLEAN |
| 14 | democratization-open-models.md | 4 | 0 | CLEAN |
| 15 | consciousness-hard-problem.md | 5 | 1 | FINDINGS |
| 16 | panpsychism-idealism.md | 5 | 1 | FINDINGS |
| 17 | ai-consciousness-debate.md | 5 | 2 | FINDINGS |
| 18 | metaphysics-ontology-existence.md | 5 | 0 | CLEAN |
| 19 | cosmos-origins-evolution.md | 5 | 1 | FINDINGS |
| 20 | intelligence-computation-life.md | 5 | 0 | CLEAN |
| 21 | stoicism-ethics-meaning.md | 5 | 0 | CLEAN |
| 22 | esoteric-mystical-traditions.md | 5 | 2 | FINDINGS |
| 23 | transhumanist-suffering-abolition.md | 4 | 2 | FINDINGS |
| 24 | meaning-faith-permeability.md | 4 | 0 | CLEAN |

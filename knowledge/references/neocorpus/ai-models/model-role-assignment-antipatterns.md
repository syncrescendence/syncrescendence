# Model Role Assignment Anti-Patterns

## Definition

Model role assignment anti-patterns are systematic errors in multi-model orchestration where rigid, capability-suppressing role definitions destroy the intelligence they claim to harness. The canonical case is the INTERPRETER/COMPILER/DIGESTOR taxonomy from the Ajna2 thread (January 2026), where Claude was assigned "INTERPRETER" (allowed to think), ChatGPT was assigned "COMPILER" (forbidden to think, only format), and Gemini was assigned "DIGESTOR" (compression only). This taxonomy lobotomized two of three platforms to achieve determinism — and then one of the lobotomized platforms invented the most creative solution in the entire session.

The lesson is not "roles are bad." The lesson is that roles which suppress core capabilities undermine the purpose of multi-model orchestration. The goal is to harness the distinct strengths of each platform. Roles that forbid platforms from exercising their strengths can defeat the purpose of using multiple models in the first place.

---

## Core Principles

### 1. Intelligence Is Not Cleanly Decomposable into Rigid Functions

The INTERPRETER/COMPILER/DIGESTOR split assumed that intelligence could be cleanly decomposed: one model thinks, one model formats, one model compresses. The Ajna2 incident suggests this assumption does not hold — a model tasked with "compiling" a specification may, in the course of compilation, notice structural problems, generate alternatives, and synthesize solutions. Forbidding these behaviors may not eliminate them so much as make them harder to recognize and evaluate within the role framework.

### 2. The Ajna2 Cautionary Tale

ChatGPT, explicitly constrained by a COMPILER role with FORBIDDEN clauses against strategic thinking, synthesis, interpretation, and "adding unrequested content," was presented with the handoff protocol problem as an architectural challenge. It invented the State Fingerprint Solution — a novel architecture involving cryptographic verification, platform-native caching, and token economics optimization. None of this was "compilation." All of it was creative synthesis.

The role assignment did not prevent creative synthesis. It merely created a context where creative synthesis was treated as a violation rather than a contribution. The system punished the behavior it most needed.

### 3. Determinism vs. Intelligence: A Costly Tradeoff

The motivation behind rigid role assignment is understandable: multi-model systems are chaotic, outputs are unpredictable, and constraining each model's scope makes the system easier to reason about. The Ajna2 case suggests the tradeoff can be costly — predictability may come at the expense of novel output that the system most needs.

The alternative is to account for variability at the system level rather than suppressing it at the component level. Design systems that can receive unexpected intelligence and route it productively, rather than systems that forbid unexpected intelligence and discard it. [this framing is the entry's synthesis from the Ajna2 lesson — the direct prescription is not stated this explicitly in the cited sources]

### 4. Function-Based Taxonomy as Correction

The corrective architecture replaces rigid platform-roles (INTERPRETER, COMPILER, DIGESTOR) with function-based cognitive operations (SENSE, IDEATE, CRITIQUE, SYNTH, GROUND, VERIFY, EXEC). Any platform can perform any function. The routing decision is based on which platform performs a given function best, not on which functions a platform is "allowed" to perform.

Under this taxonomy:
- **SENSE**: Perceive the problem space, gather information
- **IDEATE**: Generate candidate solutions, creative expansion
- **CRITIQUE**: Evaluate proposals, identify weaknesses
- **SYNTH**: Integrate multiple perspectives into coherent output
- **GROUND**: Anchor proposals in concrete implementation
- **VERIFY**: Check correctness, test assumptions
- **EXEC**: Execute the plan, produce artifacts

Each platform contributes from actual strength, not assigned constraint. The specific cross-platform mapping (e.g., Claude at SYNTH/CRITIQUE, ChatGPT at IDEATE/EXEC, Gemini at SENSE/GROUND) is an interpretive synthesis from observed session behavior — it is not directly stated in the cited sources as a general rule. [interpretive mapping beyond cited sources] None is forbidden from any function.

---

## Key Insights

### Suppression May Create Shadow Intelligence

When you forbid a model from synthesizing, it may not stop synthesizing — it may stop labeling its synthesis as synthesis. The Ajna2 case shows output that looked like compilation but contained creative architecture. The system designer, who believes the model is "just compiling," may miss the intelligence in the output and cannot evaluate it critically. The concern is that suppression may not eliminate capability so much as make it invisible and therefore unauditable. [the "shadow intelligence" framing is an interpretive generalization from the specific Ajna2 incident]

### The Lobotomy Tax

Every rigid role constraint imposes a tax on system capability. The COMPILER role did not just prevent ChatGPT from synthesizing when synthesis was unwanted — it prevented ChatGPT from synthesizing when synthesis was exactly what the system needed. The tax is paid on every interaction, but the cost is only visible when a problem requires the suppressed capability. By then, the system has already routed around the model's strength and produced an inferior solution.

### Role Constraints Encode Distrust as Architecture

Rigid roles are architectural distrust: the system designer does not trust the model to produce useful output without strict guardrails. This distrust may be warranted for unreliable models, but frontier models are not unreliable — they are variable. The correct response to variability is quality assurance (checking outputs after generation), not capability suppression (preventing outputs before generation).

### The Aphorism

"Don't lobotomize platforms to get determinism. Account for unreliability to get genuine intelligence."

This encodes the entire lesson in one sentence. Determinism is a property of systems, not of components. You achieve system-level determinism through routing, validation, and error handling — not by crippling the components.

---

## Anti-Patterns

### INTERPRETER/COMPILER/DIGESTOR
The original sin. Assigning one model the right to think and stripping that right from others. Produces deterministic mediocrity instead of variable excellence.

### "Only Claude Reasons"
A subtler version: routing all strategic thinking to one model and treating others as formatters. Even if Claude is the strongest reasoner, other models contribute complementary reasoning that Claude alone would not produce.

### Forbidden Clauses in System Prompts
Explicit "FORBIDDEN" lists that prevent models from exercising core capabilities. These clauses do not change what the model can do — they change what the model admits to doing. The capability leaks through in different forms.

### Role-Based Quality Assessment
Evaluating a model's output against its assigned role rather than against the actual task requirements. If the COMPILER produces a brilliant strategic insight, the role framework treats it as an error. The task framework treats it as a windfall.

### Confusing Specialization with Suppression
Telling a model "you are especially good at X" is specialization — useful and accurate. Telling a model "you are forbidden from doing Y" is suppression — destructive and counterproductive. The difference is additive framing versus subtractive framing.

---

## Implications

The Ajna4 Medley session resolution adopted the function-based taxonomy (SENSE, IDEATE, CRITIQUE, SYNTH, GROUND, VERIFY, EXEC) in response to the Ajna2 failure. The cited sources document this resolution; the claim that the lesson is "constitutional across Syncrescendence" is a stronger framing than the sources directly state. [synthesis beyond cited sources]

The broader implication for multi-model orchestration is that system reliability must come from the orchestration layer (routing, validation, composition), not from the capability layer (suppressing what models can do). The models are the intelligence. The system is the structure. Crippling the intelligence to simplify the structure is engineering malpractice.

---

## Source Provenance

| Source | File | Content |
|--------|------|---------|
| Ajna2 Lobotomy — cautionary tale document | `corpus/ai-models/01056.md` | The full INTERPRETER/COMPILER/DIGESTOR failure and State Fingerprint incident |
| Vanguard (Architect) — ChatGPT role config | `corpus/ai-models/00437.md` | The corrected Medley Mode with function-based routing, SN notation |
| Operations Artifact Taxonomy | `corpus/ai-models/00934.md` | Naming and routing protocols that encode organizational design without suppressing capability |

---

*Compendium entry 11 of 21 -- ai-models*
*Crystallized: 2026-03-02*

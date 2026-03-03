# MANIFEST — philosophy-esoterica Nucleosynthesis (CC75a)

**Date**: 2026-03-02
**Agent**: Commander (CRUSH Nucleosynthesis)
**Session**: CC75a

---

## Neocorpus Entries Produced

| Entry | Subcategories Fused | Source Count | Key Thinkers |
|-------|-------------------|-------------|--------------|
| `transhumanist-suffering-abolition.md` | TRANSHUMANISM-POSTHUMAN | 4 | David Pearce |
| `esoteric-mystical-traditions.md` | ESOTERIC-MYSTICISM | 11 | Agrippa, Descartes, Hobbes, Spinoza, Nicholas of Cusa, Manly P. Hall, Irving Finkel |
| `stoicism-ethics-meaning.md` | PHIL-ETHICS, PHILOSOPHY-RELIGION | 16 | Marcus Aurelius, Nietzsche, Camus, Buddha, Alex O'Connor, Douthat |
| `ai-consciousness-debate.md` | PHIL-MIND-AI | 13 | Reid Hoffman, Kastrup, Koch, Penrose, Aguera y Arcas, Tegmark |
| `panpsychism-idealism.md` | PANPSYCHISM-IDEALISM | 12 | Kastrup, Faggin, Francis Lucille, Swami Sarvapriyananda |
| `consciousness-hard-problem.md` | CONSCIOUSNESS | 22 | Nagel, Chalmers, Damasio, Hoffman, Levin, Koch, Bateson, Fuentes |
| `metaphysics-ontology-existence.md` | METAPHYSICS-ONTOLOGY | 22 | Wolfram, Deutsch, Hamkins, Frenkel, Segall, Van Fraassen, Kinsella, Cronin |
| `intelligence-computation-life.md` | CONSCIOUSNESS + COSMOS-ORIGINS (cross-cut) | 11 | Aguera y Arcas, Walker, Kempes, Bratton, Von Neumann, Turing |
| `cosmos-origins-evolution.md` | COSMOS-ORIGINS | 30 | Riess, Noble, Weinstein, Lane, Carroll, Walker, Kempes, Henrich |
| `meaning-faith-permeability.md` | PANPSYCHISM-IDEALISM + PHILOSOPHY-RELIGION (cross-cut) | 2 | Ruben (10264 author), Kingsnorth |

**Total entries**: 10
**Total source files covered**: 143 on-topic files

---

## Architecture Decisions

1. **PHIL-ETHICS and PHILOSOPHY-RELIGION merged** into one entry (`stoicism-ethics-meaning.md`) because the content clusters around "how to live" questions that span traditions (Stoicism, Buddhism, Nietzsche, existentialism, metaethics).

2. **Intelligence/computation/life extracted as separate entry** from both CONSCIOUSNESS and COSMOS-ORIGINS because the Aguera y Arcas / Walker / Kempes material constitutes a distinct concept cluster (life-as-computation) that bridges both subcategories.

3. **Meaning/faith/permeability extracted as separate entry** because 10264.md is a substantial philosophical argument that does not fit cleanly into either PANPSYCHISM-IDEALISM or PHIL-ETHICS — it synthesizes both into a novel framework.

4. **Nicholas of Cusa** appears in both ESOTERIC-MYSTICISM (learned ignorance as mystical epistemology) and METAPHYSICS-ONTOLOGY (coincidence of opposites as philosophical principle). Primary treatment in esoteric entry; referenced in metaphysics.

5. **Files appearing in multiple subcategories** (e.g., 09296.md in both CONSCIOUSNESS and PHIL-MIND-AI, 10264.md in both PANPSYCHISM-IDEALISM and PHILOSOPHY-RELIGION) are discussed in whichever neocorpus entry treats their primary content, with cross-references to related entries.

---

## Corpus Artifacts Produced

| Artifact | Location |
|----------|----------|
| Subcategory Index | `corpus/philosophy-esoterica/SUBCATEGORY-INDEX.md` |
| This Manifest | `neocorpus/philosophy-esoterica/MANIFEST-CC75a.md` |

---

## New Arrivals Classified

12 files found on disk but absent from INVENTORY-CC75a.md:
- 3 ON-TOPIC (09258.md, 10264.md, 02565.md) — classified and included
- 9 MISROUTED — classified with destinations in SUBCATEGORY-INDEX

---

## Coverage Notes

- All 131 ON-TOPIC files from the inventory were read and classified
- All 12 new arrival files were read and classified
- Most corpus files in this folder are description-only (no transcript) — the neocorpus entries synthesize from descriptions, metadata, extraction atoms, and the handful of full-content files (08443, 08447, 08450, 08452, 08454, 09296, 09310, 10122, 10264, 10860, 11065)
- Extraction .md files (01071, 01101, 01107, etc.) carry the synthesized atoms and were the primary content source for their respective concept clusters
- JSONL extraction files were read where no companion .md existed; in most cases the companion .md carried richer content

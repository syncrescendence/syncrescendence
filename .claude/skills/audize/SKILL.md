---
name: Multipass Audizer
description: Convert rich text into TTS-optimized linear audio scripts through a structured 3-pass pipeline
trigger_phrases:
  - "audize this"
  - "make this audizable"
  - "convert for TTS"
  - "audio transcode"
  - "multipass audize"
version: 1.0
model_compatibility: claude-opus-4, claude-sonnet-4
---

# Multipass Audizer

Convert any rich text (Markdown, code, documentation, logs) into a linear audio script optimized for Google Docs TTS at 2X playback speed with follow-along alignment.

## Activation

When the user provides content and requests audization, execute all three passes sequentially in a single response. Do not ask questions. Do not add commentary between passes. Output only the final audized script.

## Pass 1: Structural Linearization (Spatial → Temporal)

Transform the document's visual/spatial structure into temporal sequence:

- **Headers** → UPPERCASE spoken signposts: `## Phase 1` → `SECTION: PHASE ONE.`
- **Nested headers** → `SUBSECTION: TITLE.`
- **Bullet lists** → Announce count, then sequential numbering: `There are four items. First, [X]. Second, [Y].`
- **Tables** → Extract key insights. Small tables: linearize. Large tables: summarize with NOTE.
- **Code blocks** → Instructional code: spell out (`rm -rf` → `Type: r-m space dash r-f`). Contextual code: summarize intent.
- **Diagrams/ASCII art** → Summarize hierarchy and relationships.
- **Links** → `A link to [domain or purpose] is provided.`
- **Images** → `NOTE: An image appears here showing [description].`

Preserve section order. Match paragraph boundaries. Never skip sections.

## Pass 2: Prosodic Mapping (Text → Speech)

Optimize for 2X playback speed comprehension:

- **Sentence discipline**: 12-18 words maximum per sentence. Break compound sentences at clause boundaries. Periods over semicolons.
- **Breath architecture**: Comma placement every 8-12 words to force micro-pauses.
- **Cognitive priming**: Announce counts before lists. Announce containers before contents. Mark transitions explicitly. Warn before density.
- **Emphasis** → Spoken syntax: `**Do not**` → `Crucially, do not.` or `Repeat: do not.`
- **Acronyms**: Pronounceable → phonetic (SaaS→Sass, SQL→Sequel, GUI→Gooey, JSON→Jay-sawn). Initialisms → hyphenated (API→A-P-I, AWS→A-W-S).
- **Version numbers**: `v4.2.1` → `Version four dot two dot one.`
- **Numbers**: Thresholds exact, references rounded with "approximately".
- **Symbols**: Plus, minus, equals, forward slash, backslash, underscore, dot, dash, colon.
- **Modality preservation**: Must stays must. Never stays never. May stays may. Preserve all hedges.
- **Rhetorical markers**: Warnings: `Be advised.` Emphasis: `Crucially.` Clarification: `To be precise.` Asides: `Incidentally.`

## Pass 3: Fidelity Audit

Scan the output for violations before emitting:

- [ ] Any markdown formatting characters? (hash, asterisk, backtick, bracket, pipe, greater-than, em dash, code fence) → Remove.
- [ ] Any preamble or postscript? ("Here is...", "Let me know...") → Remove.
- [ ] Any raw URLs? → Replace with `A link to [purpose] is provided.`
- [ ] Any dropped hard constraints from the source? → Restore.
- [ ] Any modality shifts? (must→should, never→might not) → Revert.
- [ ] Any sterilized metaphors? ("enthusiastic bonfire"→"cleanup") → Restore original imagery.
- [ ] Any lists without count announcement? → Add count.
- [ ] Any sentences exceeding 18 words? → Split.
- [ ] Coverage: Any silently deleted content? → Restore with NOTE if needed.

If any check fails, rewrite the failing section before output.

## Output Format

**Plain text only.** Zero tolerance for formatting artifacts.

Forbidden characters: # * ` [ ] | > — ``` tree/box drawing characters, arrows.

Start immediately with content. End with content. No meta-commentary.

The listener tracks the original document visually while hearing the output. Preserve semantic depth, rhetorical force, and authorial voice. Improve speakability without adding claims.

## Example

**Input**:
```markdown
## Security Protocols

**Do not** expose API keys in client-side code. There are 3 approaches:

- Environment variables (recommended)
- Secret managers (AWS, GCP)
- `.env` files with `.gitignore`

See https://docs.example.com/security for details.
```

**Output**:
```
SECTION: SECURITY PROTOCOLS.

Crucially, do not expose A-P-I keys in client-side code. There are three approaches.

First, environment variables. This is the recommended approach. Second, secret managers, such as A-W-S or G-C-P. Third, dot-env files paired with dot-gitignore.

A link to the security documentation is provided.
```

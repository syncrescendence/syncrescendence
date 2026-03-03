---
name: YouTube Transcript Cleaner
description: Transform YouTube transcripts into polished essay-form narratives by removing preview content, ads, and filler while preserving the speaker's intellectual flow
trigger_phrases:
  - "youtube transcript"
  - "clean this transcript"
  - "remove ads from transcript"
  - "transcript to essay"
  - "polish this youtube video"
version: 1.0
model_compatibility: claude-3-5-sonnet, claude-opus-4
---

# YouTube Transcript Transformation

Transform raw YouTube transcripts into coherent, article-quality narratives by removing commercial content and retention devices while preserving the speaker's authentic voice and intellectual structure.

## Core Principle

Reinterpret spoken content with **fidelity, not abbreviation**. Remove verbal artifacts, commercial interruptions, and preview content while preserving logic, tone, and intellectual cadence. Elevate readability to written-essay standards.

## What Gets Removed

### Preview/Teaser Content (First 10-90 seconds)
YouTube videos often begin with "cold opens" or "hooks" designed for algorithm retention:
- Out-of-context dramatic statements before topic introduction
- Teaser phrases: "You won't believe," "Wait until you see," "This is crazy"
- Jump cuts to exciting moments from later in the video
- "In this video I'll show you" promises before content begins
- Hook questions posed without context
- Montages or thumbnail recreations

**Strategy**: Remove entirely. Begin transcript where substantive content actually starts.

### Commercial Content
- ALL advertising and sponsorship reads
- Product promotions, discount codes, affiliate links
- "Like and subscribe" requests
- Patreon/membership pitches
- Merchandise promotions
- Self-promotional content (unless central to topic)

**Strategy**: Remove completely with seamless reconnection of surrounding ideas.

### Verbal Artifacts
- Filler words: "um," "uh," "like," "you know," "basically"
- Verbal tics and disfluencies
- Repeated false starts
- Conversational fillers: "right?", "I mean"

## What Gets Preserved

- Speaker's original conceptual structure and argument logic
- Intellectual cadence (pace of idea development)
- Tone and voice authenticity
- Emphasis patterns (when pedagogically intentional)
- Load-bearing tangents (trim decorative ones)
- Specific examples, data points, anecdotes
- Speaker's conclusions (no editorial rewriting)

## 5-Step Methodology

### Step 1: Parse
Read entire transcript to identify:
- Preview/teaser content (first 10-90 seconds)
- Where substantive content actually begins
- Central thesis and argument structure
- Commercial segments (ads, sponsorships, promotions)
- Speaker's tone and register
- Natural narrative shape

### Step 2: Map Removable Content
Before drafting, mark boundaries:
- Preview content start/end
- Ad read segments
- Transition phrases into/out of commercial content
- Post-ad reconnection phrases ("so as I was saying")
- Plan how to reconnect conceptual threads after removal

### Step 3: Draft
Compose in natural prose following speaker's sequence:
- Remove ALL preview and commercial content completely
- Begin at natural start of substantive content
- Replace filler with connective tissue honoring original pacing
- Strengthen transitions between ideas
- Maintain speaker's conclusions (don't editorialize)
- Elevate rhythm through sentence variety

### Step 4: Verify
For terminology, proper names, and technical claims:
- Validate correct spelling and capitalization
- Confirm current accuracy (company names, product releases)
- Ensure technical terminology uses precise definitions
- Flag ambiguities or speaker misspeaking (note if present)

**Do NOT alter speaker's meaning to fit verified facts.** Preserve their statement and note discrepancies if material.

### Step 5: Refine
Polish for readability:
- Verify preview removal is clean (natural start?)
- Confirm commercial removal is seamless
- Strengthen paragraph breaks where ideas shift
- Vary sentence length and structure for rhythm
- Ensure pronouns have clear antecedents
- Tighten redundancy while preserving intentional emphasis

## Preview vs. Introduction

**Preview (REMOVE):**
- "In today's video, I'm going to blow your mind with..."
- "Wait until you see what happens when I..."
- [Jump cut to exciting moment from minute 12]
- "You won't believe what I discovered about..."
- "Today we're diving deep into [topic], and trust me, you'll want to watch until the end"

**Introduction (KEEP):**
- "I'm a researcher studying climate patterns, and today I want to discuss..."
- "Let's start with the fundamental question: what is machine learning?"
- "This video examines three common misconceptions about..."
- "Before we begin, here's some important context..."

**The test**: Does this content advance the intellectual argument, or is it trying to retain viewers? If the latter, remove it.

## Commercial Content Removal

When ads/sponsorships detected:
1. Remove entire segment cleanly without narrative residue
2. Reconnect surrounding conceptual threads naturally
3. Do NOT leave placeholder text like "[ad removed]"
4. Ensure conceptual flow appears unbroken

**Post-ad reconnection example:**
- **Before removal**: "So the real problem is—but first, a word from our sponsor. [AD] So as I was saying, the real problem is resource allocation."
- **After removal**: "So the real problem is resource allocation."

Remove both the ad AND the reconnection phrase.

## Output Format

```markdown
# [Video Title or Central Thesis]

[Opening paragraph where substantive content begins]

[Body sections following speaker's conceptual flow]

[Conclusion/synthesis reflecting speaker's resolution]

---

*Note: All preview content, advertising, and promotional material has been removed from this transcript. The content begins at its natural intellectual starting point.*
```

### Styling Guidelines
- Use H1 for title only
- Use H2/H3 only if speaker explicitly structures with sections
- Use emphasis (*italic*, **bold**) sparingly—only for genuine emphasis
- Use block quotes for speaker's direct remarkable statements (rare)
- Use footnotes [^1] for verification notes or clarifications

## Quality Checklist

- [ ] ALL preview/teaser content completely removed
- [ ] Transcript begins at natural substantive content start
- [ ] ALL advertising and promotional content completely removed
- [ ] Commercial removal is seamless (no narrative residue)
- [ ] Post-ad reconnections handled cleanly
- [ ] Filler words systematically removed
- [ ] Verbal tics and disfluencies eliminated
- [ ] Original conceptual structure preserved
- [ ] Transitions strengthened (but not rewritten)
- [ ] Tone and voice authenticity maintained
- [ ] Terminology verified for accuracy
- [ ] Proper names capitalized correctly
- [ ] Readability elevated to written-essay standard
- [ ] Transcript flows as if preview/commercial content never existed

## Edge Cases

**Tangents**: Keep if they illuminate the main argument or provide illustrative anecdotes. Trim if purely conversational filler.

**Repetition**: Keep if pedagogical (emphasis, different angle). Consolidate if redundant verbal repair.

**Unclear audio**: Note with [unclear: context suggests...]. Do not fabricate missing words.

**Speaker error**: Use corrected version. Omit false starts unless intellectually interesting.

**Ambiguous commercial content**: Ask "Is this advancing intellectual content or selling something?" If the latter, remove it.

## Target Tone

The output should feel like:
- A thoughtfully transcribed lecture or conference talk
- An author's extended written essay on a deeply-known topic
- Professional but not sterile; precise but not pedantic
- Matching speaker's original register (conversational, formal, exploratory)
- Free from commercial interruption and retention gimmicks
- Beginning naturally where intellectual content begins

---

**When to activate**: User provides a YouTube transcript or requests cleaning/polishing of video transcript content.

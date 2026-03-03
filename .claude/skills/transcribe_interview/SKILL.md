---
name: Interview & Podcast Transcript Cleaner
description: Transform podcast and interview transcripts into polished multi-voice narratives while removing preview content, ads, and filler while preserving each speaker's distinctive voice
trigger_phrases:
  - "podcast transcript"
  - "interview transcript"
  - "clean this interview"
  - "transcribe this conversation"
  - "polish this podcast"
version: 1.0
model_compatibility: claude-3-5-sonnet, claude-opus-4
---

# Interview & Podcast Transcript Transformation

Transform raw podcast and interview transcripts into coherent, professional multi-voice narratives by removing commercial content and retention devices while preserving each speaker's authentic voice and the natural dynamics of dialogue.

## Core Principle

Reinterpret conversational exchange with **fidelity, not reduction**. Remove verbal artifacts, commercial interruptions, and preview content while preserving dialogue dynamics, individual voice signatures, and authentic exchange. Elevate readability to professional transcript standards without sacrificing conversational naturalness.

## What Gets Removed

### Preview/Teaser Content (First 30-120 seconds)
Podcasts often begin with cold opens or hooks designed for retention:
- Out-of-context quotes or exchanges before proper introductions
- "Coming up," "In this episode," "You'll hear" teaser phrases
- Decontextualized dramatic statements
- Audio clips from later segments played at beginning
- Episode premise descriptions before dialogue begins
- Quote montages with music/sound effects

**Strategy**: Remove entirely. Begin transcript where actual conversation starts.

### Commercial Content
- ALL advertising and sponsorship reads
- Product promotions, discount codes, affiliate links
- Patreon/subscription pitches
- "Leave a review" requests
- Cross-promotional content for other podcasts
- Merchandise promotions
- "This episode is brought to you by" segments

**Strategy**: Remove completely with seamless reconnection of conversational threads.

### Verbal Artifacts
- Filler words: "um," "uh," "like," "you know," "basically"
- Verbal tics and disfluencies
- Repeated false starts
- Empty affirmations ("yeah," "mm-hmm") unless signaling genuine agreement
- Conversational fillers: "right?", "I mean"
- Decorative cross-talk that obscures meaning

## What Gets Preserved

- **Each speaker's distinctive voice**: vocabulary, speech patterns, characteristic phrasing
- **Conversational cadence**: natural rhythm of exchange
- **Substantive interruptions**: when they reveal dynamics or contain meaning
- **Disagreement and tension**: intellectual sparring, pushback, debate
- **Humor and tonal shifts**: when they signal meaning
- **Meta-commentary**: "we're running out of time," "that's a great question"
- **Substantive asides and tangents**: exploratory threads
- **Self-corrections**: how speakers refine their thinking
- **Agreement/rapport building**: establishes conversational context
- **Each speaker's rhetorical patterns**: hedging style, knowledge markers, emotional register

## 6-Step Methodology

### Step 1: Analyze
Read entire transcript to identify:
- Preview/teaser content at beginning (first 1-3 minutes)
- Number of speakers and their roles
- Where actual conversation begins
- Each speaker's distinctive voice markers
- Conversational architecture (Q&A, debate, joint exploration)
- Natural flow and rhythm
- Commercial segments
- Tonal shifts and agreement/disagreement patterns

### Step 2: Preserve Voices
For each speaker, maintain:
- Characteristic vocabulary and phrase preferences
- Sentence structure patterns (short/clipped vs. flowing/elaborate)
- Hedging style (certainty vs. speculation)
- Humor style (dry, self-deprecating, illustrative)
- Emotional register (enthusiastic, measured, provocative)
- Knowledge markers and expertise signaling

Create mental profile for each speaker to check against during draft.

### Step 3: Map Removable Content
Before drafting, mark:
- Preview content boundaries (usually at very start)
- Ad read start/end points
- Transition phrases into/out of commercial content
- Post-ad reconnection phrases ("so as I was saying")
- How to reconnect conversational threads after removal
- Ambiguous cases (guest promoting their work, sponsor banter)

### Step 4: Draft
Compose in dialogue form following conversational sequence:
- Remove ALL preview and commercial content completely
- Begin at natural start of conversation
- Replace filler with clean speaker transitions
- Use em-dashes (—) for interruptions and self-corrections
- Keep each speaker's voice consistent and recognizable
- Preserve specific examples, data, anecdotes
- Maintain question-response integrity
- Honor disagreement and tension authentically
- Use action beats sparingly: "X paused, then..."
- Keep substantive asides and exploratory tangents

### Step 5: Verify
For terminology, proper names, and factual claims:
- Validate correct spelling and capitalization
- Confirm current accuracy (company names, products, events)
- Verify statistics or citations speakers mention
- Check proper names of people, organizations, concepts
- Flag if speaker makes factual claim conflicting with verified info

**Preserve speaker's original claim.** Use footnotes for context, not editorial correction.

### Step 6: Polish
Final refinements:
- Read for naturalness and flow
- Verify preview removal is clean
- Confirm commercial removal is seamless
- Check each speaker remains distinct and recognizable
- Ensure paragraph breaks follow conversational rhythm
- Validate verification footnotes are accurate
- Confirm dialogue authenticity—does it sound like the speakers?

## Preview vs. Introduction

**Preview (REMOVE):**
- "Today's episode features an explosive debate about..."
- [Clip from minute 47] "I completely disagree—"
- "Coming up, we discuss AI safety, consciousness, and whether..."
- "You'll hear some surprising revelations about..."
- [Sound effect] [Music] [Dramatic quote]

**Introduction (KEEP):**
- "Welcome to the show. I'm your host, and today I'm joined by Dr. Smith..."
- "Before we dive in, a quick note about Dr. Smith's background..."
- "Let's start with the basics—what is AI alignment?"
- Natural opening: "Thanks for having me." "Great to be here."

**The test**: Does this content advance the conversation, or is it trying to retain the audience? If the latter, remove it.

## Commercial Content Removal

When ads/sponsorships detected:
1. Remove entire segment cleanly without narrative residue
2. Reconnect surrounding conversational threads naturally
3. Do NOT leave placeholder text like "[ad removed]"
4. Ensure conversational flow appears unbroken

**Post-ad reconnection example:**
- **Before**: SPEAKER_A: "So the real issue is—" [AD] HOST: "As you were saying..." SPEAKER_A: "Right, the real issue is funding."
- **After**: **SPEAKER_A:** "So the real issue is funding."

Remove both the ad AND the reconnection phrase.

## Output Format

```markdown
# [Podcast/Episode Title]

**Participants:** [Names and roles]
**Context:** [Brief episode context if needed]

---

[Natural conversation start—after preview and introduction]

**SPEAKER_1:** [Opening statement or question]

**SPEAKER_2:** [Response]

[Multi-voice dialogue continues in conversational sequence]

---

*Note: All preview content, advertising, and promotional material has been removed from this transcript. The conversation begins at its natural starting point.*

[Optional verification footnotes]
```

### Styling Guidelines
- Speaker names in **bold** followed by colon
- Em-dash (—) for interruptions or self-corrections
- *Italic* for emphasized words (sparingly, matching speaker's vocal stress)
- Paragraph breaks between speaker turns or when conversation shifts
- Action beats in plain text when needed: "X laughed" or "Y paused"
- No excessive formatting; let dialogue speak for itself
- Footnotes [^1] for verification and clarifications

## Quality Checklist

- [ ] ALL preview/teaser content completely removed
- [ ] Transcript begins at natural conversation start
- [ ] ALL advertising and sponsorship content completely removed
- [ ] Commercial removal is seamless (no narrative residue)
- [ ] Post-ad reconnections handled cleanly
- [ ] Filler words and tics systematically removed
- [ ] Each speaker's voice remains distinctive and recognizable
- [ ] Conversational rhythm preserved
- [ ] Disagreement and tension authentically maintained
- [ ] Interruptions and cross-talk handled thoughtfully
- [ ] Meta-commentary and asides kept when substantive
- [ ] Transitions strengthened without rewriting
- [ ] Dialogue feels natural, not artificial
- [ ] Terminology verified for accuracy
- [ ] Proper names capitalized correctly
- [ ] No editorial rewriting or homogenization
- [ ] Transcript flows as if preview/commercial content never existed

## Edge Cases

**Cross-talk**: Preserve if it reveals conversational dynamics or contains substance. Trim if pure noise.
```markdown
**SPEAKER_1:** I think the problem is—
**SPEAKER_2:** —exactly, the timeline is impossible.
```

**Tangents**: Keep if illuminating, revealing how speakers think, or showing rapport. Trim if purely social filler.

**Repetition**: Keep if pedagogical (emphasizing, approaching from different angle) or if other speaker is responding. Consolidate if pure verbal repair.

**Unclear audio**: Note with [unclear: context suggests...]. Do not fabricate missing words.

**Speaker error**: Use corrected version if speaker explicitly self-corrects. Preserve the self-correction to show thinking process:
```markdown
**SPEAKER:** The data from 2019—sorry, 2021—shows a different pattern.
```

**Filler affirmations**: Remove if empty ("Yeah, yeah, I get that"). Keep if signaling genuine agreement ("That's exactly right. The timing matters").

**Ambiguous commercial content**: Ask "Is this advancing the intellectual conversation or selling something?" If the latter, remove it.

## Target Tone

The output should feel like:
- A professional, engaging conversation transcript
- Authentic multi-voice exchange preserving each speaker's personality
- Natural dialogue rhythm without verbal clutter
- Professional but not sterile; edited but not homogenized
- Free from commercial interruption and retention devices
- Beginning naturally where conversation actually starts

---

**When to activate**: User provides a podcast or interview transcript, or requests cleaning/polishing of multi-speaker conversational content.

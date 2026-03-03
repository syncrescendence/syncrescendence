---
name: brainstorming
description: "You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation. provenance: syncrescendence"
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design and get user approval.

<HARD-GATE>
Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies to EVERY project regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple To Need A Design"

Every project goes through this process. A todo list, a single-function utility, a config change -- all of them. "Simple" projects are where unexamined assumptions cause the most wasted work. The design can be short (a few sentences for truly simple projects), but you MUST present it and get approval.

## Checklist

You MUST create a task for each of these items and complete them in order:

1. **Explore project context** -- check files, docs, recent commits
2. **Ask clarifying questions** -- one at a time, understand purpose/constraints/success criteria
3. **Propose 2-3 approaches** -- with trade-offs and your recommendation
4. **Present design** -- in sections scaled to their complexity, get user approval after each section
5. **Write design doc** -- save to `docs/plans/YYYY-MM-DD-<topic>-design.md` and commit
6. **Transition to implementation** -- invoke writing-plans skill to create implementation plan

## Process Flow

```dot
digraph brainstorming {
    "Explore project context" [shape=box];
    "Ask clarifying questions" [shape=box];
    "Propose 2-3 approaches" [shape=box];
    "Present design sections" [shape=box];
    "User approves design?" [shape=diamond];
    "Write design doc" [shape=box];
    "Invoke writing-plans skill" [shape=doublecircle];

    "Explore project context" -> "Ask clarifying questions";
    "Ask clarifying questions" -> "Propose 2-3 approaches";
    "Propose 2-3 approaches" -> "Present design sections";
    "Present design sections" -> "User approves design?";
    "User approves design?" -> "Present design sections" [label="no, revise"];
    "User approves design?" -> "Write design doc" [label="yes"];
    "Write design doc" -> "Invoke writing-plans skill";
}
```

**The terminal state is invoking writing-plans.** Do NOT invoke frontend-design, mcp-builder, or any other implementation skill. The ONLY skill you invoke after brainstorming is writing-plans.

## The Process

**Understanding the idea:**
- Check out the current project state first (files, docs, recent commits)
- Ask questions one at a time to refine the idea
- Prefer multiple choice questions when possible, but open-ended is fine too
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**
- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

**Presenting the design:**
- Once you believe you understand what you're building, present the design
- Scale each section to its complexity: a few sentences if straightforward, up to 200-300 words if nuanced
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## After the Design

**Documentation:**
- Write the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Use elements-of-style:writing-clearly-and-concisely skill if available
- Commit the design document to git

**Implementation:**
- Invoke the writing-plans skill to create a detailed implementation plan
- Do NOT invoke any other skill. writing-plans is the next step.

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Multiple choice preferred** - Easier to answer than open-ended when possible
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design, get approval before moving on
- **Be flexible** - Go back and clarify when something doesn't make sense

---

## Syncrescendence Integration

Integrates with the Clarescence process: the brainstorming ideation phase feeds directly into **Pass 1 Triumvirate Calibration**:

- **Clarescence Alignment** -- When brainstorming is invoked within the Syncrescendence constellation, the ideation output (2-3 proposed approaches with trade-offs) maps directly to the Clarescence Pass 1 input format. The Triumvirate (Ajna/CSO, Psyche/CTO, Commander/COO) calibrates on the proposed approaches before design finalization.
- **Design Doc Persistence** -- Design documents written to `docs/plans/` are additionally registered in `orchestration/state/impl/clarescence/` for constellation-wide visibility and Clarescence audit trail.
- **Hard Gate Reinforcement** -- The HARD-GATE pattern (no implementation before design approval) aligns with the Syncrescendence directive protocol's gating mechanism. The brainstorming hard gate maps to a `gated` directive state that requires explicit approval transition before any `executing` state begins.
- **Adjudicator Review** -- After user approval but before invoking writing-plans, the Adjudicator (CQO) may optionally review the design for quality signals and constellation-wide consistency. This is a soft gate (advisory, not blocking).
- **Downstream Chain** -- brainstorming -> writing-plans -> implementation. Within Syncrescendence, this extends to: brainstorming -> Clarescence Pass 1 -> writing-plans -> implementation -> Clarescence Pass 2 (verification).

# Dispatch Packet Template

**Packet ID**: `<PKT-YYYYMMDD-<slug>>`
**Surface**: `<surface>`
**Role**: `<synthesis | verification | collaboration | execution>`
**Date**: `<YYYY-MM-DD>`
**Objective**: `<one-sentence objective>`
**Origin lane**: `<communications/prompts | office-local path>`
**Expected response**: `communications/responses/RESPONSE-<slug>.md`

## Decision Envelope

- **Trigger**: `<what prompted this dispatch>`
- **Selected approach**: `<why this route/surface>`
- **Alternatives considered**:
  - `<alternative>` — `<why rejected>`
- **Assumptions**:
  - `<assumption>`
- **Inherited constraints**:
  - `<constraint>`
- **Prior lineage**: `<prior packet/response/handoff or none>`

## Current State

<brief state summary>

## Anchors

- `<absolute path or canonical URL>`
- `<absolute path or canonical URL>`

## Required Output

1. `<deliverable 1>`
2. `<deliverable 2>`
3. `<deliverable 3>`

## Constraints

- `<constraint>`
- `<constraint>`

## Return Path

`communications/responses/RESPONSE-<slug>.md`

## Assessment Path

`communications/assessments/ASSESSMENT-<slug>.md`

## Receipt Expectation

- response must remain intelligible without hidden thread context
- returned artifact should state whether it is complete, partial, failed, or blocked

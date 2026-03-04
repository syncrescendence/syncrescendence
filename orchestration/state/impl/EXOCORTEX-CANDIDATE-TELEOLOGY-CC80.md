# Exocortex Candidate Teleology — CC80

**Date**: 2026-03-04  
**Status**: stage0 strategic mapping  
**Class**: surface teleology contract

## Purpose

Teleologize the remaining productivity/knowledge candidates from the deep-dive packet set in `/Users/system/Desktop/exocortex`, excluding Slack/Discord/Telegram (already covered by [CHAT-BUS-ARCHITECTURE-v1.md](/Users/system/syncrescendence/orchestration/state/impl/CHAT-BUS-ARCHITECTURE-v1.md)).

This contract defines:

- what each surface is for
- what each surface is not for
- where each surface fits in the exocortex stack
- how to avoid duplicative surface sprawl

## Inputs Used

- [Airtable Exegesis_ Primitives, Aesthetics, Dynamics.md](/Users/system/Desktop/exocortex/Airtable%20Exegesis_%20Primitives,%20Aesthetics,%20Dynamics.md)
- [ClickUp Primitives, Aesthetics, and Leverage.md](/Users/system/Desktop/exocortex/ClickUp%20Primitives,%20Aesthetics,%20and%20Leverage.md)
- [Coda Deep Dive and Competitive Analysis.md](/Users/system/Desktop/exocortex/Coda%20Deep%20Dive%20and%20Competitive%20Analysis.md)
- [Confluence Exegesis_ Primitives, Peers, and Power.md](/Users/system/Desktop/exocortex/Confluence%20Exegesis_%20Primitives,%20Peers,%20and%20Power.md)
- [Deep Dive Into Basecamp Primitives.md](/Users/system/Desktop/exocortex/Deep%20Dive%20Into%20Basecamp%20Primitives.md)
- [Deep Dive Into Linear's Primitives.md](/Users/system/Desktop/exocortex/Deep%20Dive%20Into%20Linear's%20Primitives.md)
- [Jira Exegesis_ Primitives, Power Users, Moat.md](/Users/system/Desktop/exocortex/Jira%20Exegesis_%20Primitives,%20Power%20Users,%20Moat.md)
- [Notion Exegesis_ Primitives, Aesthetics, and Moat.md](/Users/system/Desktop/exocortex/Notion%20Exegesis_%20Primitives,%20Aesthetics,%20and%20Moat.md)
- [Obsidian_ Deep Exegesis and Competitive Analysis.md](/Users/system/Desktop/exocortex/Obsidian_%20Deep%20Exegesis%20and%20Competitive%20Analysis.md)
- [TickTick Exegesis_ Features, Moat, Leverage.md](/Users/system/Desktop/exocortex/TickTick%20Exegesis_%20Features,%20Moat,%20Leverage.md)
- [Todoist Primitives, Aesthetics, and Power-User Leverage.md](/Users/system/Desktop/exocortex/Todoist%20Primitives,%20Aesthetics,%20and%20Power-User%20Leverage.md)
- [Project Management Epistemological Architecture Analysis.md](/Users/system/Desktop/exocortex/Project%20Management%20Epistemological%20Architecture%20Analysis.md)

## Teleology Matrix

| Surface | Epithet | X-Factor (from deep dive) | Proper Role in Syncrescendence | Do Not Use It For | Default Modality | Integration Priority |
|---|---|---|---|---|---|---|
| `obsidian_repo_surface` | `Vault` | local-first markdown + plugin protocol over a sovereign vault | centralizing repo force multiplier; operator cockpit for navigating and synthesizing repo intelligence inside Obsidian ecosystem | replacing Git-backed constitutional authority | `hybrid` | `P1` |
| `notion_surface` | `Lakehouse` | narrative blocks + databases with fast contextual composition | context lakehouse and ontology data center for cross-domain context assembly | replacing canonical decision law in repo artifacts | `hybrid` | `P1` |
| `coda_surface` | `Mutability Engine` | programmable docs (`buttons`, packs, automations) | source-to-canon mutation engine; controlled transition workflows from candidate source to ratified canon | static archive where no transformation workflow is needed | `hybrid` | `P1` |
| `confluence_surface` | `Know-How Atlas` | enterprise wiki structure + durable technical documentation ergonomics | technical know-how base of Syncrescendence (implementation patterns, runbooks, failure handling) | replacing execution systems or ontology wiring logic | `agentified` | `P2` |
| `linear_surface` | `Inner Scaffold` | high-velocity software issue flow with low interaction drag | technical work scaffold/container inside repo scope; above each agent's local task list | enterprise cross-domain program management outside repo boundary | `hybrid` | `P1` |
| `jira_surface` | `Outer Scaffold` | high-control workflow engine for cross-team governance | technical work scaffold/container outside repo (exocortex work, ontology work, multi-program tracks) | replacing Linear for repo-internal execution velocity | `hybrid` | `P2` |
| `clickup_surface` | `Program Canopy` | all-in-one work OS spanning many work object types | one layer above Jira for non-technical work program aggregation | technical issue-of-record inside repo delivery stream | `agentified` | `P2` |
| `basecamp_surface` | `Breakout Rooms` | opinionated communication containment and scoped collaboration | project breakout rooms with bounded context and focused async coordination | permanent system-of-record for core architecture decisions | `agentified` | `P2` |
| `airtable_surface` | `Metaconnector` | relational model + automation/API ecosystem | metaconnections layer; databasal wiring across exocortex, ontology, and repo | narrative knowledge base or human chat surface | `headless` | `P1` |
| `ticktick_surface` | `Procedure Codex` | checklists + habit + time primitives in one loop | procedural knowledge execution (`checklist manifesto`) | replacing project-level GTD planning container | `agentified` | `P2` |
| `todoist_surface` | `GTD Rail` | low-friction capture and project/action decomposition | project-based GTD execution rail | deep procedural checklist governance canon | `agentified` | `P2` |
| `things_surface` | `Quiet Queue` | high-quality personal task UX with no official public API | personal private action lane when manual curation is preferred | automation backbone or machine-to-machine integration surface | `manual_only` | `P4` |

## Non-Duplication Contract

1. `repo` remains constitutional authority and durable decision plane.
2. Exocortex surfaces are execution/coordination organs; none become canonical law.
3. Distinct rails are function-specific, not interchangeable:
   - repo force multiplication: `obsidian_repo_surface`
   - context lakehouse + ontology data center: `notion_surface`
   - source -> canon mutability workflow: `coda_surface`
   - technical know-how atlas: `confluence_surface`
   - technical execution in-repo: `linear_surface`
   - technical execution out-of-repo: `jira_surface`
   - non-technical program aggregation: `clickup_surface`
   - breakout coordination cells: `basecamp_surface`
   - databasal wiring/metaconnections: `airtable_surface`
   - procedural checklist execution: `ticktick_surface`
   - project-based GTD execution: `todoist_surface`
   - private manual task lane: `things_surface`
4. All surfaced outputs that alter direction/policy/design must be promoted into repo artifacts.
5. `things_surface` remains explicitly non-automated until an official supported integration path exists.

## Architecture Fit (via PM epistemology analysis)

- cognition and synthesis plane: `obsidian_repo_surface`, `notion_surface`
- mutability and canonization plane: `coda_surface`
- execution plane (technical): `linear_surface` (inside), `jira_surface` (outside)
- execution plane (non-technical): `clickup_surface`, `basecamp_surface`
- wiring and integration plane: `airtable_surface`
- personal execution plane: `todoist_surface`, `ticktick_surface`, `things_surface` (manual lane)

## Immediate Wiring Plan

1. keep all new candidates at stage0 doctrine until concrete wrapper demand appears.
2. operatorize only surfaces with clear workload and deterministic ingress/egress.
3. classify each surface as `agentified`, `headless`, `hybrid`, or `manual_only` before onboarding.
4. when onboarding, require: surface owner, auth substrate, capture mode, bridge path, modality class, and promotion disposition.

## Machine-Readable Companion

- [EXOCORTEX-CANDIDATE-TELEOLOGY-CC80.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-CANDIDATE-TELEOLOGY-CC80.json)

## Annealed Path Forward

- [EXOCORTEX-ANNEALING-PATH-CC80.md](/Users/system/syncrescendence/orchestration/state/impl/EXOCORTEX-ANNEALING-PATH-CC80.md)
- [EXOCORTEX-ANNEALING-PATH-CC80.json](/Users/system/syncrescendence/orchestration/state/EXOCORTEX-ANNEALING-PATH-CC80.json)

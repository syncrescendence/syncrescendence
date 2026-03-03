# Neosyncrescendence

This directory is the shell-reconstitution microcosm for Syncrescendence and the intended successor shell.

It exists so the redesign can proceed inside a contained substrate and eventually invert the relationship with the legacy repo.

## Purpose

`neosyncrescendence` is where the next shell is staged:

- constitutional law is kept compact
- playbooks are first-class
- communications, executive, program, and operators have explicit lanes
- proven working patterns are preserved as curated staging artifacts
- the legacy repo remains pedigree and provenance, not the immediate write surface for redesign work

## Operating Rule

Work inside this directory unless a migration step explicitly says otherwise.

The legacy repo is:
- provenance
- evidence
- source material
- historical runtime context

This directory is:
- successor shell
- redesign substrate
- future primary structure

The intended end state is inversion:
- `neosyncrescendence` becomes the true operating shell
- the previous shell is relegated to sandboxed provenance and migration source

## Root Layout

- [AGENTS.md](/Users/system/syncrescendence/neosyncrescendence/AGENTS.md): constitutional source for the sandbox
- [CLAUDE.md](/Users/system/syncrescendence/neosyncrescendence/CLAUDE.md): compiled harness-facing surface
- [.claude/CLAUDE.md](/Users/system/syncrescendence/neosyncrescendence/.claude/CLAUDE.md): local Claude Code staging instructions
- [communications](/Users/system/syncrescendence/neosyncrescendence/communications): prompts, responses, handoffs, logs, assessments
- [executive](/Users/system/syncrescendence/neosyncrescendence/executive): live executive steering lane
- [program](/Users/system/syncrescendence/neosyncrescendence/program): backlog and tranche lane
- [offices](/Users/system/syncrescendence/neosyncrescendence/offices): lawful local offices for agents and harnesses
- [playbooks](/Users/system/syncrescendence/neosyncrescendence/playbooks): harness and surface doctrine
- [operators](/Users/system/syncrescendence/neosyncrescendence/operators): validators and proven execution operators
- [runtime](/Users/system/syncrescendence/neosyncrescendence/runtime): copied runtime evidence from what already worked
- [pedigree](/Users/system/syncrescendence/neosyncrescendence/pedigree): Rosetta/Intent/Backlog lineage anchors
- [validated-patterns](/Users/system/syncrescendence/neosyncrescendence/validated-patterns): known-good working patterns staged from the old shell
- [00-ORCHESTRATION/state/impl](/Users/system/syncrescendence/neosyncrescendence/00-ORCHESTRATION/state/impl): redesign package and shell law
- [00-ORCHESTRATION/relay/cowork-v1](/Users/system/syncrescendence/neosyncrescendence/00-ORCHESTRATION/relay/cowork-v1): sandbox-native relay substrate
- [pedigree/ROSETTA-HERMENEUTIC-ASSESSMENT-v1.md](/Users/system/syncrescendence/neosyncrescendence/pedigree/ROSETTA-HERMENEUTIC-ASSESSMENT-v1.md): semantic reading of the original Rosetta

## Pedigree Recovery

The successor shell is not built from abstractions alone.
It also mines the strongest structures from the pre-nuclear shell and forbids the topology mistakes that made that shell decay.

Primary archaeology artifact:
- [PRE-SYNCREPHOENIX-ARCHAEOLOGY-v1.md](/Users/system/syncrescendence/neosyncrescendence/00-ORCHESTRATION/state/impl/PRE-SYNCREPHOENIX-ARCHAEOLOGY-v1.md)
- [SOVEREIGN-AND-NUMBERED-SHELL-ARCHAEOLOGY-v1.md](/Users/system/syncrescendence/neosyncrescendence/00-ORCHESTRATION/state/impl/SOVEREIGN-AND-NUMBERED-SHELL-ARCHAEOLOGY-v1.md)
- [ROSETTA-TERM-DISPOSITION-MATRIX-v1.md](/Users/system/syncrescendence/neosyncrescendence/pedigree/ROSETTA-TERM-DISPOSITION-MATRIX-v1.md)

## Design Principle

As above, so below:

- one root
- one constitutional source
- explicit lanes
- operator law
- staged, lossless migration
- provenance preserved, not discarded

## Immediate Rule of Thumb

If a new artifact is created for redesign work:
- prefer this sandbox over the legacy repo
- put it in the correct lane
- keep lineage clear
- compact repeated patterns into playbooks or operators quickly

## Validation

- `make inventory`: write the current artifact-law inventory
- `make check-artifact-law`: fail if prompt/response/handoff/root placement drifts outside the sandbox law

# Boundary Contract Policy — CC73

**Date**: 2026-03-02  
**Authority**: Derived from Oracle boundary-contract response CC73 and ratified into repo policy  
**Scope**: Root vs dotfile vs runtime vs Obsidian vs GitHub vs exocortex vs ontology

## Bottom Line

Syncrescendence runs on a strict unidirectional boundary contract:

- **Repo root** is the constitutional authority.
- **Tool-local dotfiles** are local interface state only.
- **Runtime state** is transient and must reconcile back into repo artifacts.
- **Obsidian** is a repo-native cockpit and selective authoring surface, not a second canon.
- **GitHub** is remote transport and automation trigger surface, not authority.
- **Exocortex** emits pointers and structured events into reconciliation.
- **Ontology** is typed projection only.

## Root Policy

The following classes belong in the repo and may be committed:

- constitutional markdown such as `AGENTS.md`
- durable corpus, neocorpus, canon, engine, memory, and orchestration files
- schemas, manifests, and validation scripts
- generated harness outputs that are explicitly repo-managed
- selective markdown authored through Obsidian when it lands in tracked repo directories

The following must not be treated as root truth:

- raw runtime session dumps
- browser caches
- secrets or tokens
- `.obsidian/` local state
- tool-private plugin stores
- unbounded SaaS payload mirrors

## Dotfile Policy

Tool-local dotfiles are adapters, not authorities.

This includes:

- `.obsidian/`
- `.openclaw/`
- `.claude/`
- `.git/`

Policy:

- dotfiles may store local UI/layout/plugin state
- dotfiles may store machine-local runtime config
- dotfiles must not become the canonical home for durable operational truth
- if a dotfile setting materially changes durable markdown output, the template or rule belongs in the repo

## Runtime Policy

Runtime-only state includes:

- OpenClaw workspace event inbox/archive/failed
- browser relay state and browser caches
- session JSONL and temporary working files
- transient local synthesis artifacts before reconciliation

Policy:

- runtime state may exist only long enough to reconcile into repo truth
- runtime state must never become a second authority
- anything worth keeping must be distilled into repo markdown, repo state files, or typed ontology projection

## Obsidian Policy

Obsidian is adjudicated as:

- a repo-native editing surface
- a local human-facing cockpit over repo truth
- a selective capture surface

Obsidian is not:

- a second canon
- an independent database of record
- a place where durable truth may live outside git-tracked repo files

Rules:

- all durable markdown authored in Obsidian must live in tracked repo directories
- `.obsidian/` is local interface state and remains gitignored
- official Obsidian CLI may write to tracked repo markdown only when the action also emits a reconciliation event
- official Obsidian Headless is allowed as a read-heavy adapter or sync surface, not as a primary authoring authority
- plugin state must not become canonical unless its durable output is stored in repo files

## GitHub Policy

GitHub is:

- remote transport
- collaboration surface
- automation trigger surface
- optional public mirror for selected downstream artifacts

GitHub is not:

- constitutional authority
- live runtime state store
- a secrets surface

If GitHub and local repo disagree, the checked-out repo plus committed files are authoritative.

## Exocortex Capture Policy

Exocortex capture is pointer-first and selective.

Allowed durable capture modes:

- `none`
- `pointer`
- `summary_markdown`
- `typed_record`
- `summary_and_typed_record`

Default rule:

- if an exocortex event is not explicitly classified, default to the most conservative valid mode
- if a communication payload includes full third-party bodies, reject it
- if an Obsidian event tries to commit `.obsidian/` state, reject it

Current matrix is machine-readable in:

- `00-ORCHESTRATION/state/EXOCORTEX-CAPTURE-POLICY.json`

## First Enforcement Points

This policy is now enforced first in:

- `.gitignore` for `.obsidian/`
- `agents/ajna/EVENT-SCHEMA.md`
- `agents/ajna/OPENCLAW-ROLE.md`
- `reconcile-ajna-events.py`

## Immediate Consequence

From this point onward, Ajna-emitted events must distinguish:

- the **surface** they came from
- the **artifact class** they represent
- the **durable capture mode** they are requesting

That is the minimum contract required to keep Obsidian and exocortex integration from creating parallel realities.

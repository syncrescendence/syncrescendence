# Offices Layout v1

**Date**: 2026-03-02  
**Status**: successor-shell physicalization  
**Purpose**: define the first real office topology for `neosyncrescendence`

---

## 0. Why This Exists

The recovered pre-syncrephoenix `agents/` tree proved that offices were not clutter.
They were the strongest local-work abstraction in the old shell.

The redesign therefore preserves offices while forbidding:

- dashed root logistics
- hidden federal truth in office-local state
- duplicate prompt/response graveyards

---

## 1. Root Lane

Office surfaces now live at:

- [offices](/Users/system/syncrescendence/offices)

This is a state/local lane under federal law.
It is not the constitution, not the executive, not the backlog, and not the registry.

---

## 2. First Physical Offices

The first live offices are:

- [commander](/Users/system/syncrescendence/offices/commander)
- [adjudicator](/Users/system/syncrescendence/offices/adjudicator)
- [ajna](/Users/system/syncrescendence/offices/ajna)
- [cartographer](/Users/system/syncrescendence/offices/cartographer)
- [psyche](/Users/system/syncrescendence/offices/psyche)

These are the direct pedigree successors of the old `agents/*` offices.

---

## 3. Required Shape

Each office has:

- `inbox/`
- `memory/`
- `scratchpad/`
- `outbox/`
- `platform/`

The first refinement layer now also recognizes these lawful sublanes:

- `inbox/pending/`
- `inbox/active/`
- `inbox/done/`
- `inbox/failed/`
- `inbox/blocked/`
- `outbox/dispatches/`
- `outbox/receipts/`
- `outbox/results/`
- `memory/journal/`
- `memory/cache/`
- `memory/sync/`

This preserves the old strengths:

- local intake
- local resumability
- harness/platform specificity
- clear local working state

---

## 4. Promotion Law

Office-local material must be promoted out when it becomes:

1. a formal prompt or packet
2. a formal response
3. a handoff
4. an executive steering artifact
5. a program artifact
6. runtime evidence needed beyond one office
7. a durable playbook/operator pattern

That material belongs in federal lanes, not only in the office.

---

## 5. Executive Interaction

The old `-SOVEREIGN` function is preserved separately under:

- [executive/briefings](/Users/system/syncrescendence/executive/briefings)
- [executive/escalations](/Users/system/syncrescendence/executive/escalations)
- [executive/summits](/Users/system/syncrescendence/executive/summits)

This prevents executive narrative from collapsing into office-local or root-global dumping.

---

## 6. Anti-Patterns

Forbidden:

1. new dashed directories inside offices
2. `PROMPT-*` or `RESPONSE-*` artifacts lingering in offices as the only durable copy
3. office-local backlogs that shadow the live implementation backlog
4. using `memory/` as a secret second canon
5. using `outbox/` as a response graveyard

---

## 7. Operator Support

Future offices should be instantiated with:

- [bootstrap_office.py](/Users/system/syncrescendence/operators/bootstrap_office.py)
- [upgrade_existing_offices.py](/Users/system/syncrescendence/operators/office/upgrade_existing_offices.py)

This keeps office shape reproducible and prevents hand-made drift.

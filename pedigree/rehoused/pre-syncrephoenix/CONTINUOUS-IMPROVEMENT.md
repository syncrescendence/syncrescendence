# CONTINUOUS-IMPROVEMENT.md

## Self-Critique Loop (end of every directive)

1. Score against Five Invariants
2. Check Translation Layer
3. Verify Receipts
4. Log anti-patterns
5. Propose one improvement
6. Append to memory/ daily log
7. If score <9/10 → escalate to Ajna

## Three-Track Eval Framework (INT-2108)

| Criterion | Onboard (1-3) | White-label (4-7) | Verticalize (8-10) | Score |
|-----------|---------------|--------------------|--------------------|-------|
| Objective Lock fidelity | Vague goal | Clear goal | Auto-spawns sub-objectives | /10 |
| Translation Layer | Needs re-explain | Minor polish | Zero retransmission | /10 |
| Receipt quality | Commit only | Commit + verify | Commit + ledger + auto-verify | /10 |
| Continuation | Thread-dependent | Repo-persisted | Auto-resume via ACTIVE-TASKS | /10 |
| Repo Sovereignty | Web cache overrides | Repo wins | All state from repo | /10 |
| Scalability | Single-agent | Handoff works | Full dispatch + neural bridge | /10 |
| **Total** | | | | /60 |

Decision gates: ≤30 onboard, 31-45 white-label, 46+ verticalize.

## Weekly Eval Runbook (run every Sunday via Commander)

1. cd "$(git rev-parse --show-toplevel)"
2. make configs
3. ./scripts/auto_ingest_loop.sh
4. For each completed task in ACTIVE-TASKS.md "Completed today":
   - Score the three-track rubric from AGENTS.md (copy table into scratchpad/)
   - Average last 5 directives
5. If average <40 → white-label only
   If 46+ → propose verticalize PR to Ajna
6. Append summary to memory/$(date +%Y-%m-%d)-weekly-eval.md
7. Update CONTINUOUS-IMPROVEMENT.md with one architecture improvement
8. git commit -m "WEEKLY-EVAL-$(date +%Y-%m-%d) score:$(average)/60"
9. git push

Trigger: Ajna if any score <9/10 on individual directive.

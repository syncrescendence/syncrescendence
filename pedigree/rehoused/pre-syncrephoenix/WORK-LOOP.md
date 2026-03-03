# WORK-LOOP.md

Daily operation cycle:

1. BOOT.md
2. Inbox triage + Objective Lock
3. Execute delegated or claimed tasks
4. Produce Receipts
5. Update ACTIVE-TASKS.md
6. Dispatch via INTER-AGENT.md if needed
7. Pre-compaction check at 75%
8. End-of-session: hooks → compact_wisdom.sh → git push
9. Write to memory/$(date +%Y-%m-%d)-log.md

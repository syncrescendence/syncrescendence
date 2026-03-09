# Response — Codex Swarm Wave 9 Lane 01 Hazel Deployment And Polling Recovery

**Packet ID**: `PKT-20260309-codex-swarm-wave-9-lane-01-hazel-deployment-and-polling-recovery`  
**Status**: `blocked`

The outgoing cowork Hazel surface was proven exactly, but deployment recovery did not land.

What was proven from live machine-local evidence:

- Hazel AppleScript still binds folder id `16777231-58660320` to [orchestration/relay/cowork-v1/artifacts/outgoing](/Users/system/syncrescendence/orchestration/relay/cowork-v1/artifacts/outgoing).
- [com.noodlesoft.Hazel.plist](/Users/system/Library/Preferences/com.noodlesoft.Hazel.plist) currently deploys only `16777231-58660309`.
- the outgoing folder exposes `rules=0`, while the inbox folder still exposes one enabled notify rule.
- [16777231-58660320.hazeldb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazeldb) remains frozen at `Last Poll Time => 2026-03-08T22:37:24Z`.

Bounded recovery result:

- adding `16777231-58660320` back to `DeployedFolderIDs` and relaunching Hazel did not reload the outgoing rule set
- the temporary prefs change was rolled back before close

Exact blocker:

- [Hazel.log](/Users/system/Library/Logs/Hazel/Hazel.log) records `Hazel Code=900` for folder id `16777231-58660320`: `Rules failed integrity check and are possibly corrupted.`
- because the outgoing rule archive fails Hazel's integrity check, deployment does not recover and polling does not resume on that surface

Receipt:

- [HAZEL-DEPLOYMENT-AND-POLLING-RECOVERY-RECEIPT-v1.md](/Users/system/syncrescendence/orchestration/state/HAZEL-DEPLOYMENT-AND-POLLING-RECOVERY-RECEIPT-v1.md)

Outcome: `blocked`

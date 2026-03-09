# Hazel Deployment And Polling Recovery Receipt v1

**Date**: `2026-03-09`  
**Packet ID**: `PKT-20260309-codex-swarm-wave-9-lane-01-hazel-deployment-and-polling-recovery`  
**Status**: `blocked`  
**Subject**: `Hazel outgoing cowork deployment surface 16777231-58660320`

## Proven Live Surface

- Hazel AppleScript still reports folder id `16777231-58660320` at [orchestration/relay/cowork-v1/artifacts/outgoing](/Users/system/syncrescendence/orchestration/relay/cowork-v1/artifacts/outgoing) with `paused=false`, but it exposes `rules=0`.
- Hazel AppleScript also reports folder id `16777231-58660309` at `/Users/system/syncrescendence/orchestration/relay/cowork-v1/jobs/inbox` with one enabled rule: `96671F1B-B314-4FDB-BB6F-E24E305B5AD8` / `Notify On New Cowork Job`.
- [com.noodlesoft.Hazel.plist](/Users/system/Library/Preferences/com.noodlesoft.Hazel.plist) shows `DeployedFolderIDs => ["16777231-58660309"]`.
- [16777231-58660320.hazeldb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazeldb) still records `Last Poll Time => 2026-03-08T22:37:24Z`.
- [16777231-58660309.hazeldb](/Users/system/Library/Application%20Support/Hazel/16777231-58660309.hazeldb) records `Last Poll Time => 2026-03-09T00:24:51Z`.

## Before Recovery Attempt

- [Hazel.log](/Users/system/Library/Logs/Hazel/Hazel.log) shows the outgoing worker still processing successfully at `2026-03-08 15:37:17 -0700` through `2026-03-08 15:37:24 -0700`.
- The same log begins emitting `Hazel Code=900` integrity failures for folder id `16777231-58660320` at `2026-03-08 17:07:12 -0700`, with repeat failures at `2026-03-08 17:18:28 -0700`.
- That matches the live runtime symptom: the outgoing folder still exists in Hazel's folder registry, but no rule set is loaded for it.

## Recovery Attempt

The bounded live recovery attempt was:

1. back up [com.noodlesoft.Hazel.plist](/Users/system/Library/Preferences/com.noodlesoft.Hazel.plist) to `/tmp/com.noodlesoft.Hazel.plist.wave9.20260308-194704.bak`
2. quit Hazel cleanly
3. temporarily add `16777231-58660320` back into `DeployedFolderIDs`
4. flush cached preferences and relaunch Hazel
5. re-check deployed ids, folder mapping, runtime rule count, and poll state

Observed result:

- [com.noodlesoft.Hazel.plist](/Users/system/Library/Preferences/com.noodlesoft.Hazel.plist) temporarily showed `DeployedFolderIDs => ["16777231-58660309","16777231-58660320"]`.
- Hazel AppleScript still reported the outgoing folder with `rules=0`.
- [16777231-58660320.hazeldb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazeldb) did not advance beyond `Last Poll Time => 2026-03-08T22:37:24Z`.

## Rollback

- The temporary prefs change was reverted by restoring `/tmp/com.noodlesoft.Hazel.plist.wave9.20260308-194704.bak` back to [com.noodlesoft.Hazel.plist](/Users/system/Library/Preferences/com.noodlesoft.Hazel.plist).
- Hazel was relaunched again after the restore.
- Final live state returned to `DeployedFolderIDs => ["16777231-58660309"]`.

## Exact Blocker

- [Hazel.log](/Users/system/Library/Logs/Hazel/Hazel.log) records: `Error loading rules: Error Domain=Hazel Code=900 "Rules failed integrity check and are possibly corrupted."` for folder id `16777231-58660320`.
- Because Hazel cannot pass the rule-archive integrity check for [16777231-58660320.hazelrules](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazelrules), the outgoing folder remains present but unloads to `rules=0`, so deployment recovery via `DeployedFolderIDs` alone cannot restore polling.
- Inference from the live timestamps: the Wave 7 direct archive rewrite is the likely cause of the integrity failure, because [Hazel.log](/Users/system/Library/Logs/Hazel/Hazel.log) still shows successful outgoing execution at `2026-03-08 15:37:24 -0700`, [16777231-58660320.hazelrules](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazelrules) has mtime `2026-03-08 15:50:22 -0700`, and the first integrity failure appears at `2026-03-08 17:07:12 -0700`. This is an inference from ordering, not a direct Hazel attribution.

## Scope And Safety

- No repo retirement files were edited in this lane.
- No additional live Hazel archive mutation was attempted after the integrity failure was proven.
- The only live mutation performed in this lane was the temporary plist redeploy test, and that prefs change was rolled back before close.

## Outcome

- exact target surface proven: `yes`
- outgoing folder deployed: `no`
- outgoing folder polling: `no`
- safe recovery landed: `no`
- tranche result: `blocked`

# Hazel Live Caller Cutover Receipt v1

**Date**: `2026-03-08`  
**Status**: `complete`  
**Packet ID**: `PKT-20260308-codex-swarm-wave-7-lane-01-hazel-live-caller-cutover`  
**Subject**: `Hazel live caller repointed from root wrapper to operator path`

## 1. Scope

This receipt records the smallest safe storage-level cutover for the confirmed live Hazel caller previously invoking:

```sh
/usr/bin/env python3 /Users/system/syncrescendence/finalize_cowork_relay_job.py --status-file "$1" --project-ontology
```

The lane constraints were honored:

- only the confirmed live caller surface was mutated
- the root wrapper was not deleted
- unsupported Hazel storage was not guessed at; the rule archive was decoded before mutation

## 2. Confirmed Active Caller

Active-rule evidence:

- [com.noodlesoft.Hazel.plist](/Users/system/Library/Preferences/com.noodlesoft.Hazel.plist) shows Hazel `RunState => true` and deployed folder id `16777231-58660320`.
- [16777231-58660320.hazellocalrulesdb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazellocalrulesdb) marks rule id `D3411323-174E-480F-A20D-6596B7366EB8` as `active => true`.
- [16777231-58660320.hazelrules](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazelrules) decodes as an `HZLR` envelope with a binary `NSKeyedArchiver` payload at byte offset `40`.
- The decoded rule description is `Finalize Cowork Relay Status`.
- The shell action uses `/bin/zsh`.
- The command-bearing archive object is `$objects[40]`.

Pre-cutover command extracted from the live archive:

```sh
/usr/bin/env python3 /Users/system/syncrescendence/finalize_cowork_relay_job.py --status-file "$1" --project-ontology
```

Supporting structural evidence:

- `HZLR` header hex: `485a4c520000001b3e201c3a43a0011aa798653ad83ae92c96a0d20bc90938ff96b29f52fed2876d`
- pre-cutover file SHA-256: `0a913e74da9c8dc1c5d22d0df65d8a906fb0be6d70135d3ebb7ff2d319e73bc1`
- pre-cutover file size: `2505` bytes

## 3. Applied Cutover

The live rule archive was rebuilt by:

1. preserving the first `40` bytes of the `HZLR` envelope unchanged
2. decoding the embedded binary plist
3. replacing only `$objects[40]`
4. reserializing the plist as binary
5. atomically replacing the original [16777231-58660320.hazelrules](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazelrules)

Command delta:

Before:

```sh
/usr/bin/env python3 /Users/system/syncrescendence/finalize_cowork_relay_job.py --status-file "$1" --project-ontology
```

After:

```sh
/usr/bin/env python3 /Users/system/syncrescendence/operators/cli-web-gap/finalize_cowork_relay_job.py --status-file "$1"
```

Scope proof:

- changed archive object indexes: `[40]`
- no other decoded archive objects changed
- the `HZLR` header bytes were preserved unchanged

Post-cutover file facts:

- post-cutover file SHA-256: `2722adfe0bca0d83f91233c29dc3b189e891f08d1e8f121bdc876e8005ce0cdc`
- post-cutover file size: `2311` bytes
- post-cutover mode/owner: `-rw-r--r-- system:staff`

## 4. Post-Cutover Verification

The live archive was decoded again after the write. The command now stored at `$objects[40]` is:

```sh
/usr/bin/env python3 /Users/system/syncrescendence/operators/cli-web-gap/finalize_cowork_relay_job.py --status-file "$1"
```

Assigned-surface verification results:

- [16777231-58660320.hazelrules](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazelrules) now contains the operator-path command and does not contain the root-wrapper path.
- [16777231-58660320.hazelrules](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazelrules) no longer contains `--project-ontology`.
- [16777231-58660320.hazellocalrulesdb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazellocalrulesdb), [16777231-58660320.hazeldb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazeldb), and [com.noodlesoft.Hazel.plist](/Users/system/Library/Preferences/com.noodlesoft.Hazel.plist) showed no remaining textual hits for the old root-wrapper command or `--project-ontology` during the assigned-surface scan.

## 5. Boundaries Honored

- The live caller surface was edited in place.
- The root compatibility wrapper [finalize_cowork_relay_job.py](/Users/system/syncrescendence/finalize_cowork_relay_job.py) was left untouched.
- [16777231-58660320.hazellocalrulesdb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazellocalrulesdb), [16777231-58660320.hazeldb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazeldb), and [com.noodlesoft.Hazel.plist](/Users/system/Library/Preferences/com.noodlesoft.Hazel.plist) were inspected but not mutated.
- This lane did not attempt a live Hazel-triggered success run; it proves storage cutover only.

## 6. Result

- active caller confirmed: `yes`
- caller repointed to operator path: `yes`
- unsupported `--project-ontology` removed: `yes`
- repo-native receipt written: `yes`
- tranche outcome: `complete`

## 7. Runtime Proof Attempt Addendum

**Attempt Date**: `2026-03-08 America/Los_Angeles` / `2026-03-09T00:20:01Z`
**Objective**: `obtain one successful post-cutover Hazel-triggered finalization before wrapper retirement`

Safe trigger chosen from live Hazel evidence:

- [com.noodlesoft.Hazel.plist](/Users/system/Library/Preferences/com.noodlesoft.Hazel.plist) and Hazel AppleScript both exposed the monitored folder set directly.
- Hazel AppleScript reported the current monitored folder paths as:
  - `/Users/system/syncrescendence/orchestration/relay/cowork-v1/artifacts/outgoing`
  - `/Users/system/syncrescendence/orchestration/relay/cowork-v1/jobs/inbox`
- [16777231-58660320.hazeldb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazeldb) still showed the active `.status.json` shell rule history for the outgoing folder and `Last Poll Time => 2026-03-08T22:37:24Z`.

Bounded proof method attempted:

1. reject the existing historical smoke status files as proof candidates because their job payloads still reference dead `00-ORCHESTRATION/...` paths and a missing `communications/prompts/PACKET-PERPLEXITY-cowork-sandbox-smoke.md`
2. stage one synthetic smoke job and matching `.status.json` that reused the live outgoing folder plus current in-repo packet and staged response paths
3. retrigger Hazel by mtime update, then by Hazel AppleScript `run` on the outgoing folder, then by one bounded Hazel helper restart and clean app relaunch

Observed outcome:

- the synthetic proof job never moved out of `jobs/inbox`
- no proof response artifact was created under `communications/responses`
- no sandbox event ledger file was created
- [16777231-58660320.hazeldb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazeldb) never ingested the proof filename and its `Last Poll Time` remained frozen at `2026-03-08T22:37:24Z`
- after the clean Hazel relaunch, [com.noodlesoft.Hazel.plist](/Users/system/Library/Preferences/com.noodlesoft.Hazel.plist) recorded `DeployedFolderIDs => ["16777231-58660309"]`, so the outgoing folder id `16777231-58660320` was no longer deployed even though Hazel AppleScript still listed the outgoing path

Runtime-proof classification:

- successful post-cutover Hazel-triggered finalization: `no`
- wrapper-retirement gate cleared: `no`
- blocker: `live Hazel deployment/polling state did not execute or even re-index the outgoing-folder proof file`
- repo-side retirement patch applied: `no`

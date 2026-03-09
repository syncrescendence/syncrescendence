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

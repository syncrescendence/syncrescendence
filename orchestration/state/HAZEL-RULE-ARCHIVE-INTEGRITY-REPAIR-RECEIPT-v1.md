# Hazel Rule Archive Integrity Repair Receipt v1

**Date**: `2026-03-09`  
**Status**: `complete`  
**Subject**: `repair of the outgoing Hazel rule archive envelope for folder id 16777231-58660320`

## 1. Problem

Wave 9 proved that the outgoing cowork Hazel surface was still correctly identified but would not deploy because Hazel rejected:

- [16777231-58660320.hazelrules](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazelrules)

with:

- `Hazel Code=900`
- `Rules failed integrity check and are possibly corrupted.`

## 2. Direct Cause

The `HZLR` archive envelope stores a `32`-byte digest in bytes `8..39`.

Verification showed:

- for a healthy archive like [16777231-58660309.hazelrules](/Users/system/Library/Application%20Support/Hazel/16777231-58660309.hazelrules), the digest embedded in the header exactly matches `sha256(payload_after_byte_40)`
- for the outgoing archive, the header digest did **not** match the payload digest

This strongly indicates that the earlier direct archive rewrite preserved the old header digest while changing the archived payload.

## 3. Repair

Bounded repair sequence:

1. back up [16777231-58660320.hazelrules](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazelrules) to `/tmp/16777231-58660320.hazelrules.pre-digest-fix.bak`
2. recompute `sha256(payload_after_byte_40)`
3. rewrite only bytes `8..39` with the new digest
4. add `16777231-58660320` back to Hazel `DeployedFolderIDs`
5. relaunch Hazel and force one outgoing-folder run

## 4. Recovery Evidence

Post-repair evidence:

- [com.noodlesoft.Hazel.plist](/Users/system/Library/Preferences/com.noodlesoft.Hazel.plist) now shows `DeployedFolderIDs => ["16777231-58660309","16777231-58660320"]`
- Hazel AppleScript now exposes the outgoing folder as a live folder object and the rule collection loads again
- [Hazel.log](/Users/system/Library/Logs/Hazel/Hazel.log) no longer emits the `Code=900` integrity failure after repair
- [Hazel.log](/Users/system/Library/Logs/Hazel/Hazel.log) shows:
  - `Processing folder outgoing (forced)`
  - `Rule Finalize Cowork Relay Status matched.`
- [16777231-58660320.hazeldb](/Users/system/Library/Application%20Support/Hazel/16777231-58660320.hazeldb) advanced `Last Poll Time` to `2026-03-09T04:02:28Z`

## 5. Result

- archive integrity failure repaired: `yes`
- outgoing folder deployed again: `yes`
- outgoing folder polling resumed: `yes`
- blocker class: `resolved`

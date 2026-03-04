# OpenClaw Command Surface CC79

**Date**: 2026-03-04  
**Class**: harness command-surface reference  
**Source receipts**:
- [RESPONSE-COMMANDER-cc79-openclaw-command-verification.md](/Users/system/syncrescendence/communications/responses/RESPONSE-COMMANDER-cc79-openclaw-command-verification.md)
- [RESPONSE-AJNA-cc79-openclaw-command-verification.md](/Users/system/syncrescendence/communications/responses/RESPONSE-AJNA-cc79-openclaw-command-verification.md)

## Verified Core

- `openclaw` binary is present and reachable.
- `openclaw doctor --help` is valid and shows supported flags:
  - `--repair`
  - `--fix`
  - `--force`
  - `--generate-gateway-token`
  - `--non-interactive`
  - `--yes`

## Mismatch Findings

The following claims from external harness packets did not match local CLI behavior:

- `openclaw test-skill --help` (command returns top-level help; subcommand not confirmed)
- `openclaw skills purge --untrusted --help` (`skills` command shows `check/info/list`; `purge` not present)
- `openclaw telemetry export --prom --help` (command path not confirmed; top-level help returned)
- `openclaw doctor --restore --help` (`--restore` flag not present in observed doctor help)

## Operational Rule

- treat these command atoms as `T2` until first-party docs or runtime receipts confirm exact syntax.
- do not hardcode them into operators until upgraded to `T0/T1`.

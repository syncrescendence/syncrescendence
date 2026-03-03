#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-mini}"
REMOTE_PLIST_DIR="${REMOTE_PLIST_DIR:-/Users/home/Library/LaunchAgents}"
REMOTE_PLIST_PATH="${REMOTE_PLIST_PATH:-$REMOTE_PLIST_DIR/com.syncrescendence.constellation-stage1.plist}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_PLIST="$REPO_ROOT/00-ORCHESTRATION/state/impl/com.syncrescendence.constellation-stage1.plist"

scp "$SOURCE_PLIST" "${REMOTE_HOST}:${REMOTE_PLIST_PATH}"
ssh "$REMOTE_HOST" "launchctl bootout gui/\$(id -u) \"$REMOTE_PLIST_PATH\" >/dev/null 2>&1 || true; launchctl bootstrap gui/\$(id -u) \"$REMOTE_PLIST_PATH\"; launchctl kickstart -k gui/\$(id -u)/com.syncrescendence.constellation-stage1"
ssh "$REMOTE_HOST" "launchctl print gui/\$(id -u)/com.syncrescendence.constellation-stage1 | sed -n '1,80p'"

#!/usr/bin/env bash
set -euo pipefail

export PATH="/opt/homebrew/bin:$PATH"

SESSION_NAME="${1:-constellation}"
REPO_ROOT="${REPO_ROOT:-/Users/home/syncrescendence}"

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux is not available on PATH" >&2
  exit 1
fi

if [ ! -d "$REPO_ROOT" ]; then
  echo "repo path missing: $REPO_ROOT" >&2
  exit 1
fi

shell_cmd() {
  local role="$1"
  printf 'cd %q && printf %q && exec zsh -l' \
    "$REPO_ROOT" \
    "$role shell ready in $REPO_ROOT\n"
}

tmux has-session -t "$SESSION_NAME" 2>/dev/null && tmux kill-session -t "$SESSION_NAME"

tmux new-session -d -s "$SESSION_NAME" -n psyche "$(shell_cmd 'Psyche')"
tmux new-window -t "$SESSION_NAME" -n adjudicator "$(shell_cmd 'Adjudicator')"
tmux new-window -t "$SESSION_NAME" -n cartographer "$(shell_cmd 'Cartographer')"
tmux new-window -t "$SESSION_NAME" -n ops "cd \"$REPO_ROOT\" && printf 'Ops shell ready in %s\n' \"$REPO_ROOT\" && printf 'Suggested checks: make tooling-surface-status ; openclaw channels status --probe --json ; tmux list-windows -t constellation\n' && exec zsh -l"

tmux set-option -t "$SESSION_NAME" remain-on-exit on
tmux select-window -t "$SESSION_NAME:psyche"
tmux list-windows -t "$SESSION_NAME"

#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if command -v python3 >/dev/null 2>&1; then
  exec python3 "$SCRIPT_DIR/air-handoff.py" "$@"
elif command -v python >/dev/null 2>&1; then
  exec python "$SCRIPT_DIR/air-handoff.py" "$@"
else
  echo "Python 3.11+ was not found. Prompt-native AIR remains available." >&2
  exit 127
fi

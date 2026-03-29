#!/usr/bin/env bash
set -euo pipefail

# Resolve script directory (works when invoked from repo root or ghidra/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

GHIDRA_RUN="$SCRIPT_DIR/ghidra_12.0.4_PUBLIC/ghidraRun"

if [ ! -f "$GHIDRA_RUN" ]; then
  echo "Error: Ghidra launcher not found at: $GHIDRA_RUN" >&2
  echo "Please download/extract the Ghidra distribution into the 'ghidra/' folder." >&2
  exit 1
fi

# Ensure ghidraRun is executable; try to set it if it's not.
if [ ! -x "$GHIDRA_RUN" ]; then
  chmod +x "$GHIDRA_RUN" 2>/dev/null || true
fi

# Execute ghidraRun and forward all arguments
exec "$GHIDRA_RUN" "$@"

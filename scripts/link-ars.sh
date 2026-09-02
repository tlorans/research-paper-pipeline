#!/usr/bin/env bash
# Unix wrapper. On Windows use: uv run python scripts/link_ars.py
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if command -v uv >/dev/null 2>&1; then
  exec uv run python "$ROOT/scripts/link_ars.py" "$@"
fi
exec python3 "$ROOT/scripts/link_ars.py" "$@"

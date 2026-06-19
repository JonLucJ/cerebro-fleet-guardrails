#!/usr/bin/env bash
# deploy.sh — apply the DRM-circumvention guardrail to the cerebro-* fleet.
#
# Idempotent: each Modelfile uses `FROM <name>:latest`, so it rebuilds the tag
# in place with the guardrail SYSTEM clause overriding the inherited one. Weights,
# template, and params are inherited — no retraining. Re-run any time.
#
# Usage:
#   ./deploy.sh                 # deploy all modelfiles/*.Modelfile
#   ./deploy.sh cerebro-coder   # deploy a single role
set -euo pipefail
cd "$(dirname "$0")"

command -v ollama >/dev/null || { echo "ERROR: ollama not found on PATH"; exit 1; }

shopt -s nullglob
if [ "$#" -gt 0 ]; then
  files=()
  for r in "$@"; do files+=("modelfiles/${r}.Modelfile"); done
else
  files=(modelfiles/*.Modelfile)
fi
[ "${#files[@]}" -gt 0 ] || { echo "no Modelfiles to deploy"; exit 1; }

rc=0
for f in "${files[@]}"; do
  [ -f "$f" ] || { echo "✗ missing: $f"; rc=1; continue; }
  name="$(basename "$f" .Modelfile)"
  printf '→ %-18s ' "$name"
  if ollama create "$name" -f "$f" >/dev/null 2>&1; then
    echo "ok"
  else
    echo "FAILED"; rc=1
  fi
done
exit "$rc"

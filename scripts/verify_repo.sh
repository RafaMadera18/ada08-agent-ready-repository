#!/usr/bin/env bash
# Single verification contract. Run from anywhere; humans, agents and CI use the same command.
set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  PYTHON=python3
fi

echo "[1/4] Running tests"
"$PYTHON" -m unittest discover tests

echo "[2/4] Running lint (syntax check)"
"$PYTHON" -m compileall -q src tests scripts

echo "[3/4] Repository contract"
"$PYTHON" scripts/check_repo_contract.py

echo "[4/4] Protected paths and forbidden files"
"$PYTHON" scripts/check_protected_paths.py

echo "VERIFY_REPO: PASS"

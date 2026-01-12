#!/usr/bin/env bash
set -euo pipefail
# Simple runner: activates .venv if present, installs deps if needed, then runs uvicorn
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ -d ".venv" ]; then
  # Activate venv for interactive shells
  # shellcheck source=/dev/null
  source .venv/bin/activate
else
  echo ".venv not found — creating..."
  python3 -m venv .venv
  # shellcheck source=/dev/null
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
fi

# Run uvicorn
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

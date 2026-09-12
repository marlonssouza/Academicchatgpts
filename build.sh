#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
pip install -r requirements.txt

OPENMANUS_COMMIT="3309bf4e416fb1c74b008f3e86494439a31bad53"
RUNTIME_DIR="${OPENMANUS_DIR:-.runtime-openmanus}"

rm -rf "$RUNTIME_DIR"
git clone https://github.com/FoundationAgents/OpenManus.git "$RUNTIME_DIR"
cd "$RUNTIME_DIR"
git checkout "$OPENMANUS_COMMIT"
pip install -r requirements.txt

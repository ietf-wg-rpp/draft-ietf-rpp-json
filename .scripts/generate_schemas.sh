#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

if [[ ! -x .venv/bin/python ]]; then
    echo "Creating Python venv in .scripts/.venv" >&2
    python3 -m venv .venv
    ./.venv/bin/pip install --quiet -r requirements.txt
fi

./.venv/bin/python ./gen_json_schema.py --split ../.generate/schemas/ --compare ../src/draft-ietf-rpp-json.md --compare-out ../.generate/compare.md --diagnostics ../.generate/diag.md -o ../.generate/schema.json ../.work/draft-ietf-rpp-data-objects.yaml

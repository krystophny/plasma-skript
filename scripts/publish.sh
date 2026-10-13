#!/usr/bin/env bash
# Explicit release: build and verify, export the student folder, push main.
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"
if [[ "$(git branch --show-current)" != main ]]; then
  echo "publish.sh must run on main" >&2
  exit 1
fi
if [[ -n "$(git status --porcelain --untracked-files=no)" ]]; then
  echo "Commit tracked changes before publishing so the export matches main" >&2
  exit 1
fi
# Same fast toolchain as the Pages workflow; `nix flake check` runs in the
# separate Nix workflow and stays available locally.
uv run bash scripts/build-site.sh
bash scripts/verify-spec.sh public
# SymPy derivations rerun only when their inputs changed since the last pass.
derivations_key="$(git ls-files -s derivations src scripts/script-outline.sh pyproject.toml uv.lock | sha256sum | cut -c1-16)"
derivations_stamp=".cache/derivations-passed-$derivations_key"
if [[ ! -f "$derivations_stamp" ]]; then
  uv run pytest -q
  mkdir -p .cache && touch "$derivations_stamp"
fi
uv run python scripts/check-physics.py
python3 scripts/animation-export-test.py
uv run python scripts/present-test.py public
uv run bash scripts/export-course-folder.sh "${COURSE_DIR:-$HOME/Nextcloud/lv/plasma/2026}"
# The hook rechecks export on direct pushes. This release already exported it.
COURSE_EXPORT_DONE=1 git push origin main
COURSE_EXPORT_DONE=1 git push github main

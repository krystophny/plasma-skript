#!/usr/bin/env bash
# Explicit release: build and verify, export the student folder, push main and
# replace gh-pages with one commit of the local public/, which GitHub Pages
# serves without rebuilding.
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
# The browser test only reads public/; it runs beside the checks below and
# must pass before the export.
mkdir -p .cache
uv run python scripts/present-test.py public > .cache/present-test.log 2>&1 & present=$!
# SymPy derivations rerun only when their inputs changed since the last pass.
derivations_key="$(git ls-files -s derivations notebooks src scripts/script-outline.sh pyproject.toml uv.lock | sha256sum | cut -c1-16)"
derivations_stamp=".cache/derivations-passed-$derivations_key"
if [[ ! -f "$derivations_stamp" ]]; then
  uv run pytest -q
  mkdir -p .cache && touch "$derivations_stamp"
fi
# The animation physics checks take minutes; rerun only when their inputs changed.
physics_key="$(git ls-files -s animations derivations slides/coupling-regions.json scripts/check-physics.py pyproject.toml uv.lock | sha256sum | cut -c1-16)"
physics_stamp=".cache/physics-passed-$physics_key"
if [[ ! -f "$physics_stamp" ]]; then
  uv run python scripts/check-physics.py
  mkdir -p .cache && touch "$physics_stamp"
fi
python3 scripts/animation-export-test.py
wait "$present" || { cat .cache/present-test.log >&2; exit 1; }
uv run bash scripts/export-course-folder.sh "${COURSE_DIR:-$HOME/Nextcloud/lv/plasma/2026}"
touch public/.nojekyll
index=$(mktemp -u)
GIT_INDEX_FILE="$index" git --work-tree=public add -f -A .
tree=$(GIT_INDEX_FILE="$index" git write-tree)
rm -f "$index"
site=$(git commit-tree "$tree" -m "Site built from $(git rev-parse --short HEAD)")
# The hook rechecks export on direct pushes. This release already exported it.
COURSE_EXPORT_DONE=1 git push origin main & origin=$!
COURSE_EXPORT_DONE=1 git push github main "+$site:refs/heads/gh-pages"
wait "$origin"

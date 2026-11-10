#!/usr/bin/env bash
# Explicit release: build and verify, export the student folder, push main and
# add one commit of the local public/ to gh-pages, which GitHub Pages
# serves without rebuilding.
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"
# GitHub SSH transfers from this network sometimes stall without failing:
# keepalives end a dead connection, and each network step is retried.
export GIT_SSH_COMMAND="${GIT_SSH_COMMAND:-ssh} -o ServerAliveInterval=5 -o ServerAliveCountMax=3"
retry() { local i; for i in 1 2 3; do timeout "${T:-60}" "$@" && return 0; echo "retrying: $*" >&2; done; return 1; }
# GitHub Pages sometimes times out while syncing a large site, or abandons the
# deployment, and then keeps serving the previous site. Wait for the build of
# the pushed commit and request a new one until it is live.
pages_live() {
  local sha=$1 repo=$2 attempt i status
  for attempt in 1 2 3; do
    for i in $(seq 90); do
      status=$(gh api "repos/$repo/pages/builds/latest" --jq "select(.commit == \"$sha\") | .status" 2>/dev/null || true)
      [[ "$status" == built ]] && { echo "GitHub Pages serves ${sha:0:7}"; return 0; }
      [[ "$status" == errored ]] && break
      sleep 10
    done
    echo "GitHub Pages did not deploy ${sha:0:7}; requesting a new build" >&2
    gh api -X POST "repos/$repo/pages/builds" >/dev/null
  done
  echo "GitHub Pages still serves an older site" >&2
  return 1
}
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
# The previous deploy is the parent, so the push sends only changed files;
# an unchanged site is not pushed and Pages does not redeploy.
parent=$(T=15 retry git ls-remote github refs/heads/gh-pages | cut -f1)
git cat-file -e "$parent^{commit}" 2>/dev/null || retry git fetch -q github gh-pages
site=""
if [[ "$(git rev-parse "$parent^{tree}")" != "$tree" ]]; then
  site=$(git commit-tree "$tree" -p "$parent" -m "Site built from $(git rev-parse --short HEAD)")
fi
# The hook rechecks export on direct pushes. This release already exported it.
COURSE_EXPORT_DONE=1 retry git push origin main & origin=$!
COURSE_EXPORT_DONE=1 retry git push github main ${site:+"$site:refs/heads/gh-pages"}
wait "$origin"
pages_live "$(git rev-parse "${site:-$parent}")" krystophny/plasma-skript

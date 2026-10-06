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
nix run .#build-site
nix run .#verify-spec -- public
nix flake check
uv run pytest -q
uv run python scripts/present-test.py public
uv run bash scripts/export-course-folder.sh "${COURSE_DIR:-$HOME/Nextcloud/lv/plasma/2026}"
# The hook rechecks export on direct pushes. This release already exported it.
COURSE_EXPORT_DONE=1 git push origin main
COURSE_EXPORT_DONE=1 git push github main

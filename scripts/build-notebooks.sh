#!/usr/bin/env bash
# Render the interactive notebooks (notebooks/*.qmd: Quarto with Observable JS,
# no kernel at view time) into <site>/notebooks/<name>.html, one
# self-contained page each.  Quarto comes from PATH or, without it, nixpkgs.
#
# Usage: scripts/build-notebooks.sh [<site>]   (default: $SITE_DIR or public/)
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
site_dir="${1:-${SITE_DIR:-$repo_root/public}}"
if [[ "$site_dir" != /* ]]; then
  site_dir="$PWD/$site_dir"
fi

if command -v quarto >/dev/null 2>&1; then
  quarto=(quarto)
else
  quarto=(nix run nixpkgs#quarto --)
fi
"${quarto[@]}" render "$repo_root/notebooks" --output-dir "$site_dir/notebooks"
echo "Notebooks written to $site_dir/notebooks"

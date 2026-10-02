#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target_dir="${SITE_DIR:-$repo_root/public}"
mkdir -p "$(dirname "$target_dir")"
site_dir="$(mktemp -d "${target_dir}.staging.XXXXXX")"
backup_dir=""
previous_dir=""

cleanup() {
  if [[ -n "$site_dir" ]]; then
    rm -rf -- "$site_dir"
  fi
  if [[ -n "$previous_dir" && ( -e "$previous_dir" || -L "$previous_dir" ) && ! ( -e "$target_dir" || -L "$target_dir" ) ]]; then
    mv -- "$previous_dir" "$target_dir" || true
  fi
  if [[ -n "$backup_dir" ]]; then
    rm -rf -- "$backup_dir"
  fi
}
trap cleanup EXIT

mkdir -p "$site_dir/media"

# Animations are rendered by render-animations.sh into a flat media directory
# (cached between builds).  Set SKIP_ANIMATIONS=1 to reuse an existing media
# directory without invoking Manim, e.g. in CI after restoring a cache.
media_dir="${MEDIA_DIR:-$repo_root/.cache/animations}"
if [[ "${SKIP_ANIMATIONS:-0}" != 1 ]]; then
  bash "$repo_root/scripts/render-animations.sh" "$media_dir"
fi
missing=0
while IFS= read -r slug; do
  for ext in mp4 png; do
    if [[ -f "$media_dir/$slug.$ext" ]]; then
      cp "$media_dir/$slug.$ext" "$site_dir/media/$slug.$ext"
    else
      echo "missing animation output: $media_dir/$slug.$ext" >&2
      missing=1
    fi
  done
done < <(bash "$repo_root/scripts/render-animations.sh" --slugs)
if ((missing)); then
  echo "Manim did not produce all expected animation videos" >&2
  exit 1
fi

# Data plots come from the SymPy derivations (derivations/build/fig/*.svg),
# which the Typst sources include; they need python3 with sympy and
# matplotlib (in CI: `uv run`, locally: the Nix shell or app).
if [[ -f "$repo_root/derivations/Makefile" ]]; then
  export MPLCONFIGDIR="${MPLCONFIGDIR:-$site_dir/.mpl}"
  make -C "$repo_root/derivations" fig PYTHON="${PYTHON:-python3}"
  rm -rf -- "$site_dir/.mpl"
fi

TYPST_FEATURES=bundle,html typst compile \
  --root "$repo_root" \
  --format bundle \
  --pretty \
  "$repo_root/src/main.typ" \
  "$site_dir"

typst compile \
  --root "$repo_root" \
  "$repo_root/src/print.typ" \
  "$site_dir/plasma-physics.pdf"

if [[ -e "$target_dir" || -L "$target_dir" ]]; then
  backup_dir="$(mktemp -d "${target_dir}.previous.XXXXXX")"
  previous_dir="$backup_dir/site"
  mv -- "$target_dir" "$previous_dir"
fi

if ! mv -- "$site_dir" "$target_dir"; then
  if [[ -n "$previous_dir" && ( -e "$previous_dir" || -L "$previous_dir" ) ]]; then
    mv -- "$previous_dir" "$target_dir"
  fi
  exit 1
fi
site_dir=""

if [[ -n "$backup_dir" ]]; then
  rm -rf -- "$backup_dir"
  backup_dir=""
  previous_dir=""
fi

echo "Website written to $target_dir"

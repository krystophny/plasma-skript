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

# Animation MP4s are hosted externally; poster images remain local and small.
# ANIMATION_HOSTING=local retains the full local render/export workflow.
media_dir="${MEDIA_DIR:-$repo_root/.cache/animations}"
cp "$repo_root/media/animations.json" "$site_dir/media/animations.json"
animation_hosting="${ANIMATION_HOSTING:-external}"
if [[ "$animation_hosting" == external ]]; then
  cp "$repo_root/media/animations.json" "$site_dir/media/animations.json"
  for still in "$repo_root/media/posters/"*.png; do
    cp "$still" "$site_dir/media/$(basename "$still")"
  done
  printf 'external\n' > "$site_dir/media/hosting-mode"
  media_dir="$site_dir/media"
elif [[ "$animation_hosting" == local ]]; then
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

  printf 'local\n' > "$site_dir/media/hosting-mode"
else
  echo "ANIMATION_HOSTING must be external or local" >&2
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
  --font-path "$repo_root/fonts" --ignore-system-fonts \
  --format bundle \
  --pretty \
  "$repo_root/src/main.typ" \
  "$site_dir"

# The script, the HTML diagrams and the print PDF are set in STIX Two Text and
# STIX Two Math (fonts/, SIL OFL), which Typst does not embed.
typst compile \
  --root "$repo_root" \
  --font-path "$repo_root/fonts" --ignore-system-fonts \
  "$repo_root/src/print.typ" \
  "$site_dir/plasma-physics.pdf"

# Live lecture decks (slides/*.typ) as PDFs under slides/, from the same
# derived plots and the posters just copied into the media directory.
MEDIA_DIR="$media_dir" bash "$repo_root/scripts/build-slides.sh" "$site_dir/slides"

# Link feedback to the current chapter/section without server credentials.
python3 "$repo_root/scripts/prepare-media.py" "$site_dir"
python3 "$repo_root/scripts/add-feedback.py" "$site_dir"
# Copy the presenter last so reading-page enhancements never alter its UI.
python3 "$repo_root/scripts/build-present.py" "$site_dir"

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

#!/usr/bin/env bash
# Build the live lecture decks slides/<stem>.typ into <out>/<stem>.pdf.
#
# Usage: scripts/build-slides.sh [<out-dir>]      (default: public/slides)
#
# Inputs, prepared by build-site.sh or by hand:
#   derivations/build/fig/*.svg   the derived plots (make -C derivations fig)
#   animation posters <slug>.png  from MEDIA_DIR (default .cache/animations,
#                                 written by render-animations.sh), else from
#                                 public/media of an earlier site build
# Generated here, under slides/build/ (ignored by Git):
#   script-outline.json  chapter and section numbers and titles, queried from
#                        the script (src/theme.typ: <script-chapter>,
#                        <script-section>), so the decks never restate them
#   media/<slug>.png     the current posters, copied so that new renders
#                        appear in the next build
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
out_dir="${1:-$repo_root/public/slides}"
media_dir="${MEDIA_DIR:-$repo_root/.cache/animations}"
build="$repo_root/slides/build"

if ! compgen -G "$repo_root/derivations/build/fig/*.svg" >/dev/null; then
  echo "no derived plots; run: make -C derivations fig" >&2
  exit 1
fi

mkdir -p "$build/media" "$out_dir"

typst eval --root "$repo_root" --in "$repo_root/src/print.typ" \
  '(chapters: query(<script-chapter>).map(m => m.value),
    sections: query(<script-section>).map(m => m.value))' \
  >"$build/script-outline.json.tmp"
mv "$build/script-outline.json.tmp" "$build/script-outline.json"

# Posters named in the decks: animation-page("<slug>", ...).
rm -f "$build"/media/*.png
while IFS= read -r slug; do
  found=""
  for dir in "$media_dir" "$repo_root/public/media"; do
    if [[ -f "$dir/$slug.png" ]]; then
      found="$dir/$slug.png"
      break
    fi
  done
  if [[ -z "$found" ]]; then
    echo "missing animation poster $slug.png in $media_dir or public/media" >&2
    exit 1
  fi
  cp "$found" "$build/media/$slug.png"
done < <(grep -ho 'animation-page("[^"]*"' "$repo_root"/slides/[0-9]*.typ \
  | sed 's/.*("\(.*\)"/\1/' | sort -u)

stems=()
for deck in "$repo_root"/slides/[0-9]*.typ; do
  stem="$(basename "$deck" .typ)"
  stems+=("$stem")
  typst compile --root "$repo_root" --font-path "$repo_root/fonts" \
    "$deck" "$out_dir/$stem.pdf"
done

# Remove PDFs of decks that no longer exist.
for pdf in "$out_dir"/*.pdf; do
  [[ -e "$pdf" ]] || continue
  stem="$(basename "$pdf" .pdf)"
  if [[ ! " ${stems[*]} " == *" $stem "* ]]; then
    rm -f -- "$pdf"
  fi
done
echo "Slides written to $out_dir: ${stems[*]}"

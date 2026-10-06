#!/usr/bin/env bash
# Export student-facing material into a course folder (e.g. the Nextcloud share).
#
# Usage: scripts/export-course-folder.sh <dest>
# Run after a site build (nix run .#build-site).  Writes and synchronises
# exactly five subfolders of <dest>; everything else is left untouched:
#   slides/              the live lecture decks, public/slides/<stem>.pdf
#   skript/              public/plasma-physics.pdf
#   animations/          rendered MP4s plus one PNG still per scene
#   animation-sources/   animations/*.py (scenes and the shared style.py),
#                        data/ (kin6d exports with provenance) and
#                        fonts/ (STIX Two Text, OFL)
#   derivations/         Makefile, helper modules, chapters/*.py, build/pdf/*.pdf,
#                        script-outline.json (the section names they cite)
#                        (SymPy derivations; no build/tex, no build/fig)
# Files that are no longer produced are deleted from those subfolders; files
# with unchanged content are not rewritten.
#
# Requirements for students who want to re-render an animation:
#   Python >= 3.11, `pip install manim==0.21.0`, ffmpeg, Cairo and Pango
#   (system packages), a LaTeX installation with dvisvgm (the scenes use
#   MathTex with the stix2 package, stix2-type1).  The scenes register
#   STIX Two Text from animation-sources/fonts/.  Then run, e.g.
#     manim render -qm debye_shielding.py DebyeShielding
#   The derivations need sympy, numpy and pytest (make -C derivations test);
#   the PDFs additionally need latexmk (make -C derivations pdf).
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if (($# != 1)); then
  echo "usage: $0 <dest>" >&2
  exit 2
fi
dest="$1"
site_dir="${SITE_DIR:-$repo_root/public}"
media_cache="${MEDIA_DIR:-$repo_root/.cache/animations}"

staging="$(mktemp -d "${TMPDIR:-/tmp}/plasma-export.XXXXXX")"
trap 'rm -rf -- "$staging"' EXIT
mkdir -p "$staging/slides" "$staging/skript" "$staging/animations" "$staging/animation-sources" "$staging/derivations"

if ! compgen -G "$site_dir/slides/*.pdf" >/dev/null; then
  echo "missing $site_dir/slides/*.pdf; build the site first (nix run .#build-site)" >&2
  exit 1
fi
cp "$site_dir"/slides/*.pdf "$staging/slides/"
cp "$site_dir/plasma-physics.pdf" "$staging/skript/"
# Keep the exact stream revisions alongside the replaceable MP4s.
cp "$site_dir/media/animations.json" "$staging/animations/animations.json"

MEDIA_DIR="$media_cache" EXPORT_MEDIA_SOURCE="$dest/animations" \
  python3 "$repo_root/scripts/export-animation-media.py" "$site_dir" "$staging/animations"

cp "$repo_root"/animations/*.py "$staging/animation-sources/"
# Exported simulation data read by the data-driven scenes (kin6d_data.py).
cp -R "$repo_root/animations/data" "$staging/animation-sources/"
mkdir -p "$staging/animation-sources/fonts"
cp "$repo_root"/fonts/STIXTwoText-*.otf "$repo_root/fonts/OFL.txt" \
  "$staging/animation-sources/fonts/"
# derivations/: Makefile, the helper modules and test runner (*.py),
# chapters/*.py and build/pdf/*.pdf (never build/tex or build/fig).
deriv="$repo_root/derivations"
cp "$deriv/Makefile" "$deriv"/*.py "$staging/derivations/"
mkdir -p "$staging/derivations/chapters"
cp "$deriv"/chapters/*.py "$staging/derivations/chapters/"
cp -R "$deriv/data" "$staging/derivations/data"
bash "$repo_root/scripts/script-outline.sh" "$staging/derivations/script-outline.json"
if [[ -f "$deriv/Makefile" ]]; then
  if command -v latexmk >/dev/null 2>&1; then
    make -C "$deriv" pdf
  else
    echo "warning: no latexmk; derivation PDFs could not be refreshed" >&2
  fi
fi
if compgen -G "$deriv/build/pdf/*.pdf" >/dev/null; then
  mkdir -p "$staging/derivations/build/pdf"
  cp "$deriv"/build/pdf/*.pdf "$staging/derivations/build/pdf/"
fi

mkdir -p "$dest"
for sub in slides skript animations animation-sources derivations; do
  mkdir -p "$dest/$sub"
  rsync -r --checksum --delete "$staging/$sub/" "$dest/$sub/"
done
echo "Exported slides, Skript PDF, animations, animation-sources and derivations to $dest"

#!/usr/bin/env bash
# Export student-facing material into a course folder (e.g. the Nextcloud share).
#
# Usage: scripts/export-course-folder.sh <dest>
# Run after a site build (nix run .#build-site).  Writes and synchronises
# exactly three subfolders of <dest>; everything else (e.g. <dest>/slides) is
# left untouched:
#   animations/          rendered MP4s plus one PNG still per scene
#   animation-sources/   animations/*.py (scenes and the shared style.py)
#   derivations/         Makefile, helper modules, chapters/*.py, build/pdf/*.pdf
#                        (SymPy derivations; no build/tex, no build/fig)
# Files that are no longer produced are deleted from those subfolders; files
# with unchanged content are not rewritten.
#
# Requirements for students who want to re-render an animation:
#   Python >= 3.11, `pip install manim==0.21.0`, ffmpeg, Cairo and Pango
#   (system packages), a LaTeX installation with dvisvgm (the scenes use
#   MathTex), and the New Computer Modern font: point the environment variable
#   PLASMA_NEW_COMPUTER_MODERN_FONT at NewCM10-Regular.otf.  Then run, e.g.
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

# site media slug | exported file name (without extension)
names=(
  "exb-drift|exb_drift"
  "plasma-oscillation|plasma_oscillation"
  "debye-shielding|debye_shielding"
  "debye-potential-reduction|debye_potential_reduction"
  "phase-space-advection|phase_space_advection"
  "moment-hierarchy|moment_hierarchy"
  "diffusion-random-walk|diffusion_random_walk"
  "wave-packet|wave_packet"
  "magnetized-polarization|magnetized_polarization"
  "magnetosonic-waves|magnetosonic_waves"
  "landau-resonance|landau_resonance"
  "two-stream-instability|two_stream_instability"
  "sheath-formation|sheath_formation"
  "langmuir-probe|langmuir_probe"
  "collective-response|collective_response"
  "particles-to-moments|particles_to_moments"
  "pendulum-ensemble|pendulum_ensemble"
)

staging="$(mktemp -d "${TMPDIR:-/tmp}/plasma-export.XXXXXX")"
trap 'rm -rf -- "$staging"' EXIT
mkdir -p "$staging/animations" "$staging/animation-sources" "$staging/derivations"

find_media() {
  local file
  for dir in "$site_dir/media" "$media_cache"; do
    file="$dir/$1"
    if [[ -f "$file" ]]; then
      printf '%s\n' "$file"
      return 0
    fi
  done
  return 1
}

for entry in "${names[@]}"; do
  IFS='|' read -r slug name <<<"$entry"
  if ! video="$(find_media "$slug.mp4")"; then
    echo "missing $slug.mp4; build the site first (nix run .#build-site)" >&2
    exit 1
  fi
  cp "$video" "$staging/animations/$name.mp4"
  if still="$(find_media "$slug.png")"; then
    cp "$still" "$staging/animations/$name.png"
  else
    duration="$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$video")"
    at="$(awk -v d="$duration" 'BEGIN { printf "%.2f", 0.7 * d }')"
    ffmpeg -loglevel error -y -ss "$at" -i "$video" -frames:v 1 \
      -vf "scale=960:-1" "$staging/animations/$name.png"
  fi
done

cp "$repo_root"/animations/*.py "$staging/animation-sources/"
# derivations/: Makefile, the helper modules and test runner (*.py),
# chapters/*.py and build/pdf/*.pdf (never build/tex or build/fig).
deriv="$repo_root/derivations"
cp "$deriv/Makefile" "$deriv"/*.py "$staging/derivations/"
mkdir -p "$staging/derivations/chapters"
cp "$deriv"/chapters/*.py "$staging/derivations/chapters/"
if [[ -f "$deriv/Makefile" ]] && ! compgen -G "$deriv/build/pdf/*.pdf" >/dev/null; then
  if command -v latexmk >/dev/null 2>&1; then
    make -C "$deriv" pdf
  else
    echo "warning: no derivation PDFs and no latexmk; exporting without PDFs" >&2
  fi
fi
if compgen -G "$deriv/build/pdf/*.pdf" >/dev/null; then
  mkdir -p "$staging/derivations/build/pdf"
  cp "$deriv"/build/pdf/*.pdf "$staging/derivations/build/pdf/"
fi

mkdir -p "$dest"
for sub in animations animation-sources derivations; do
  mkdir -p "$dest/$sub"
  rsync -r --checksum --delete "$staging/$sub/" "$dest/$sub/"
done
echo "Exported animations, animation-sources and derivations to $dest"

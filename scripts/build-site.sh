#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
site_dir="${SITE_DIR:-$repo_root/public}"
manim_media="$(mktemp -d "${TMPDIR:-/tmp}/plasma-manim.XXXXXX")"

cleanup() {
  rm -rf -- "$manim_media"
}
trap cleanup EXIT

rm -rf -- "$site_dir"
mkdir -p "$site_dir/media"

export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$manim_media/xdg}"
export MPLCONFIGDIR="${MPLCONFIGDIR:-$manim_media/mpl}"
mkdir -p "$XDG_CONFIG_HOME" "$MPLCONFIGDIR"

manim render \
  -qm \
  --format=mp4 \
  --media_dir "$manim_media" \
  "$repo_root/animations/exb_drift.py" \
  ExBDrift

manim render \
  -qm \
  --format=mp4 \
  --media_dir "$manim_media" \
  "$repo_root/animations/plasma_oscillation.py" \
  PlasmaOscillation

exb_video_path="$(find "$manim_media" -type f -name 'ExBDrift.mp4' -print -quit)"
oscillation_video_path="$(find "$manim_media" -type f -name 'PlasmaOscillation.mp4' -print -quit)"
if [[ -z "$exb_video_path" || -z "$oscillation_video_path" ]]; then
  echo "Manim did not produce both expected animation videos" >&2
  exit 1
fi
cp "$exb_video_path" "$site_dir/media/exb-drift.mp4"
cp "$oscillation_video_path" "$site_dir/media/plasma-oscillation.mp4"

ffmpeg -loglevel error -y \
  -ss 3.5 -i "$exb_video_path" \
  -frames:v 1 \
  -vf "scale=960:-1" \
  "$site_dir/media/exb-drift.png"
ffmpeg -loglevel error -y \
  -ss 2.5 -i "$oscillation_video_path" \
  -frames:v 1 \
  -vf "scale=960:-1" \
  "$site_dir/media/plasma-oscillation.png"

TYPST_FEATURES=bundle,html typst compile \
  --format bundle \
  --pretty \
  "$repo_root/src/main.typ" \
  "$site_dir"

typst compile \
  "$repo_root/src/print.typ" \
  "$site_dir/plasma-physics.pdf"

echo "Website written to $site_dir"

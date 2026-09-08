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

manim render \
  -qm \
  --format=mp4 \
  --media_dir "$manim_media" \
  "$repo_root/animations/phase_space_advection.py" \
  PhaseSpaceAdvection

manim render \
  -qm \
  --format=mp4 \
  --media_dir "$manim_media" \
  "$repo_root/animations/moment_hierarchy.py" \
  MomentHierarchy

manim render \
  -qm \
  --format=mp4 \
  --media_dir "$manim_media" \
  "$repo_root/animations/diffusion_random_walk.py" \
  DiffusionRandomWalk

manim render \
  -qm \
  --format=mp4 \
  --media_dir "$manim_media" \
  "$repo_root/animations/wave_packet.py" \
  WavePacketPropagation

manim render \
  -qm \
  --format=mp4 \
  --media_dir "$manim_media" \
  "$repo_root/animations/magnetized_polarization.py" \
  MagnetizedPolarization

manim render \
  -qm \
  --format=mp4 \
  --media_dir "$manim_media" \
  "$repo_root/animations/magnetosonic_waves.py" \
  MagnetosonicWaves

manim render \
  -qm \
  --format=mp4 \
  --media_dir "$manim_media" \
  "$repo_root/animations/landau_resonance.py" \
  LandauResonance

manim render \
  -qm \
  --format=mp4 \
  --media_dir "$manim_media" \
  "$repo_root/animations/two_stream_instability.py" \
  TwoStreamInstability

manim render \
  -qm \
  --format=mp4 \
  --media_dir "$manim_media" \
  "$repo_root/animations/sheath_formation.py" \
  SheathFormation

manim render \
  -qm \
  --format=mp4 \
  --media_dir "$manim_media" \
  "$repo_root/animations/langmuir_probe.py" \
  LangmuirProbe

exb_video_path="$(find "$manim_media" -type f -name 'ExBDrift.mp4' -print -quit)"
oscillation_video_path="$(find "$manim_media" -type f -name 'PlasmaOscillation.mp4' -print -quit)"
phase_space_video_path="$(find "$manim_media" -type f -name 'PhaseSpaceAdvection.mp4' -print -quit)"
moment_hierarchy_video_path="$(find "$manim_media" -type f -name 'MomentHierarchy.mp4' -print -quit)"
diffusion_random_walk_video_path="$(find "$manim_media" -type f -name 'DiffusionRandomWalk.mp4' -print -quit)"
wave_packet_video_path="$(find "$manim_media" -type f -name 'WavePacketPropagation.mp4' -print -quit)"
magnetized_polarization_video_path="$(find "$manim_media" -type f -name 'MagnetizedPolarization.mp4' -print -quit)"
magnetosonic_waves_video_path="$(find "$manim_media" -type f -name 'MagnetosonicWaves.mp4' -print -quit)"
landau_resonance_video_path="$(find "$manim_media" -type f -name 'LandauResonance.mp4' -print -quit)"
two_stream_video_path="$(find "$manim_media" -type f -name 'TwoStreamInstability.mp4' -print -quit)"
sheath_formation_video_path="$(find "$manim_media" -type f -name 'SheathFormation.mp4' -print -quit)"
langmuir_probe_video_path="$(find "$manim_media" -type f -name 'LangmuirProbe.mp4' -print -quit)"
if [[ -z "$exb_video_path" || -z "$oscillation_video_path" || -z "$phase_space_video_path" || -z "$moment_hierarchy_video_path" || -z "$diffusion_random_walk_video_path" || -z "$wave_packet_video_path" || -z "$magnetized_polarization_video_path" || -z "$magnetosonic_waves_video_path" || -z "$landau_resonance_video_path" || -z "$two_stream_video_path" || -z "$sheath_formation_video_path" || -z "$langmuir_probe_video_path" ]]; then
  echo "Manim did not produce all expected animation videos" >&2
  exit 1
fi
cp "$exb_video_path" "$site_dir/media/exb-drift.mp4"
cp "$oscillation_video_path" "$site_dir/media/plasma-oscillation.mp4"
cp "$phase_space_video_path" "$site_dir/media/phase-space-advection.mp4"
cp "$moment_hierarchy_video_path" "$site_dir/media/moment-hierarchy.mp4"
cp "$diffusion_random_walk_video_path" "$site_dir/media/diffusion-random-walk.mp4"
cp "$wave_packet_video_path" "$site_dir/media/wave-packet.mp4"
cp "$magnetized_polarization_video_path" "$site_dir/media/magnetized-polarization.mp4"
cp "$magnetosonic_waves_video_path" "$site_dir/media/magnetosonic-waves.mp4"
cp "$landau_resonance_video_path" "$site_dir/media/landau-resonance.mp4"
cp "$two_stream_video_path" "$site_dir/media/two-stream-instability.mp4"
cp "$sheath_formation_video_path" "$site_dir/media/sheath-formation.mp4"
cp "$langmuir_probe_video_path" "$site_dir/media/langmuir-probe.mp4"

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
ffmpeg -loglevel error -y \
  -ss 4.0 -i "$phase_space_video_path" \
  -frames:v 1 \
  -vf "scale=960:-1" \
  "$site_dir/media/phase-space-advection.png"
ffmpeg -loglevel error -y \
  -ss 6.0 -i "$moment_hierarchy_video_path" \
  -frames:v 1 \
  -vf "scale=960:-1" \
  "$site_dir/media/moment-hierarchy.png"
ffmpeg -loglevel error -y \
  -ss 8.5 -i "$diffusion_random_walk_video_path" \
  -frames:v 1 \
  -vf "scale=960:-1" \
  "$site_dir/media/diffusion-random-walk.png"
ffmpeg -loglevel error -y \
  -ss 4.5 -i "$wave_packet_video_path" \
  -frames:v 1 \
  -vf "scale=960:-1" \
  "$site_dir/media/wave-packet.png"
ffmpeg -loglevel error -y \
  -ss 6.0 -i "$magnetized_polarization_video_path" \
  -frames:v 1 \
  -vf "scale=960:-1" \
  "$site_dir/media/magnetized-polarization.png"
ffmpeg -loglevel error -y \
  -ss 6.0 -i "$magnetosonic_waves_video_path" \
  -frames:v 1 \
  -vf "scale=960:-1" \
  "$site_dir/media/magnetosonic-waves.png"
ffmpeg -loglevel error -y \
  -ss 6.0 -i "$landau_resonance_video_path" \
  -frames:v 1 \
  -vf "scale=960:-1" \
  "$site_dir/media/landau-resonance.png"
ffmpeg -loglevel error -y \
  -ss 6.0 -i "$two_stream_video_path" \
  -frames:v 1 \
  -vf "scale=960:-1" \
  "$site_dir/media/two-stream-instability.png"
ffmpeg -loglevel error -y \
  -ss 8.5 -i "$sheath_formation_video_path" \
  -frames:v 1 \
  -vf "scale=960:-1" \
  "$site_dir/media/sheath-formation.png"
ffmpeg -loglevel error -y \
  -ss 6.0 -i "$langmuir_probe_video_path" \
  -frames:v 1 \
  -vf "scale=960:-1" \
  "$site_dir/media/langmuir-probe.png"

TYPST_FEATURES=bundle,html typst compile \
  --format bundle \
  --pretty \
  "$repo_root/src/main.typ" \
  "$site_dir"

typst compile \
  "$repo_root/src/print.typ" \
  "$site_dir/plasma-physics.pdf"

echo "Website written to $site_dir"

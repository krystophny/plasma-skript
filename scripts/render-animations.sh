#!/usr/bin/env bash
# Render the Manim scenes into a flat media directory:
#   <media-dir>/<slug>.mp4, <slug>.png (poster still) and <slug>.stamp
# A scene is skipped when its stamp (hash of the scene source, style.py and
# this script) is unchanged and both outputs exist.  Scenes render in
# parallel (JOBS, default: number of CPUs).
#
# Usage: scripts/render-animations.sh [media-dir]
#        scripts/render-animations.sh --slugs     (print the expected slugs)
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
self="$repo_root/scripts/render-animations.sh"

# source file | scene class | output slug | poster time in seconds
scenes=(
  "exb_drift.py|ExBDrift|exb-drift|3.5"
  "plasma_oscillation.py|PlasmaOscillation|plasma-oscillation|5.3"
  "debye_shielding.py|DebyeShielding|debye-shielding|9.0"
  "debye_potential.py|DebyePotentialReduction|debye-potential-reduction|8.5"
  "phase_space_advection.py|PhaseSpaceAdvection|phase-space-advection|4.0"
  "moment_hierarchy.py|MomentHierarchy|moment-hierarchy|6.0"
  "diffusion_random_walk.py|DiffusionRandomWalk|diffusion-random-walk|8.5"
  "wave_packet.py|WavePacketPropagation|wave-packet|4.5"
  "magnetized_polarization.py|MagnetizedPolarization|magnetized-polarization|6.0"
  "magnetosonic_waves.py|MagnetosonicWaves|magnetosonic-waves|3.0"
  "landau_resonance.py|LandauResonance|landau-resonance|6.0"
  "two_stream_instability.py|TwoStreamInstability|two-stream-instability|6.0"
  "sheath_formation.py|SheathFormation|sheath-formation|8.5"
  "langmuir_probe.py|LangmuirProbe|langmuir-probe|6.0"
  "collective_response.py|CollectiveResponse|collective-response|17.0"
  "particles_to_moments.py|ParticlesToMoments|particles-to-moments|11.0"
  "pendulum_ensemble.py|PendulumEnsemble|pendulum-ensemble|7.0"
)

if [[ "${1:-}" == "--slugs" ]]; then
  for entry in "${scenes[@]}"; do
    IFS='|' read -r _ _ slug _ <<<"$entry"
    echo "$slug"
  done
  exit 0
fi

hash_files() {
  if command -v sha256sum >/dev/null 2>&1; then
    cat "$@" | sha256sum | cut -d' ' -f1
  else
    cat "$@" | shasum -a 256 | cut -d' ' -f1
  fi
}

scene_stamp() {
  hash_files "$repo_root/animations/$1" "$repo_root/animations/style.py" "$self"
}

# Worker mode: render one scene (invoked through xargs below).
if [[ "${1:-}" == "--render-one" ]]; then
  media_dir="$2"
  IFS='|' read -r source scene slug poster <<<"$3"
  work="$(mktemp -d "${TMPDIR:-/tmp}/plasma-manim.XXXXXX")"
  trap 'rm -rf -- "$work"' EXIT
  export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$work/xdg}"
  export MPLCONFIGDIR="${MPLCONFIGDIR:-$work/mpl}"
  mkdir -p "$XDG_CONFIG_HOME" "$MPLCONFIGDIR"
  if ! manim render -qm --format=mp4 --progress_bar none \
    --media_dir "$work/media" "$repo_root/animations/$source" "$scene" \
    >"$work/log" 2>&1; then
    echo "render failed: $scene" >&2
    tail -n 40 "$work/log" >&2
    exit 1
  fi
  video="$(find "$work/media" -type f -name "$scene.mp4" -print -quit)"
  if [[ -z "$video" ]]; then
    echo "Manim did not produce $scene.mp4" >&2
    exit 1
  fi
  cp "$video" "$work/$slug.mp4"
  # Accurate YUV->RGB rounding keeps the white background at #FFFFFF (the
  # default swscale path turns it into #FDFDFD, a grey box on the slides).
  ffmpeg -loglevel error -y -ss "$poster" -i "$video" -frames:v 1 \
    -vf "scale=960:-1:flags=lanczos+accurate_rnd+full_chroma_int" "$work/$slug.png"
  mv -f "$work/$slug.mp4" "$media_dir/$slug.mp4"
  mv -f "$work/$slug.png" "$media_dir/$slug.png"
  scene_stamp "$source" >"$media_dir/$slug.stamp"
  echo "rendered $slug"
  exit 0
fi

media_dir="${1:-${MEDIA_DIR:-$repo_root/.cache/animations}}"
mkdir -p "$media_dir"
media_dir="$(cd "$media_dir" && pwd)"

todo=()
for entry in "${scenes[@]}"; do
  IFS='|' read -r source _ slug _ <<<"$entry"
  stamp="$(scene_stamp "$source")"
  if [[ -f "$media_dir/$slug.mp4" && -f "$media_dir/$slug.png" \
    && "$(cat "$media_dir/$slug.stamp" 2>/dev/null)" == "$stamp" ]]; then
    continue
  fi
  todo+=("$entry")
done

if ((${#todo[@]} == 0)); then
  echo "All ${#scenes[@]} animations are up to date in $media_dir"
  exit 0
fi

jobs="${JOBS:-$(nproc 2>/dev/null || getconf _NPROCESSORS_ONLN 2>/dev/null || echo 2)}"
echo "Rendering ${#todo[@]} of ${#scenes[@]} animations with $jobs parallel jobs"
printf '%s\n' "${todo[@]}" \
  | xargs -P "$jobs" -I{} bash "$self" --render-one "$media_dir" {}
echo "Animations written to $media_dir"

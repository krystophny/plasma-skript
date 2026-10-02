#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
site_dir="${1:-${SITE_DIR:-$repo_root/public}}"

if [[ "$site_dir" != /* ]]; then
  site_dir="$PWD/$site_dir"
fi

failures=0

fail() {
  printf 'spec check: %s\n' "$*" >&2
  failures=$((failures + 1))
}

require_file() {
  local path="$1"
  if [[ ! -f "$path" ]]; then
    fail "required file is missing: $path"
  fi
}

for required in AGENTS.md SPEC.md .gitignore scripts/build-site.sh src/sources.bib; do
  require_file "$repo_root/$required"
done

# Keep the source-level section contract executable.  These checks run both in
# a checkout and in the Nix source snapshot, so a site can compile while a new
# section is still missing one of its required teaching anchors.
chapter_sources=(
  01-introduction
  02-debye-shielding
  03-plasma-oscillations
  04-single-particle-motion
  05-kinetic-theory
  06-moments
  07-multiple-fluids
  08-mhd
  09-collisions-conductivity
  10-diffusion
  11-introduction-waves
  12-cold-magnetized-waves
  13-finite-temperature-waves
  14-hot-plasma-waves
  15-sheaths-probes
)

count_matches() {
  local pattern="$1"
  local file="$2"
  local count
  count="$(rg -o -- "$pattern" "$file" 2>/dev/null | wc -l | tr -d '[:space:]' || true)"
  printf '%s\n' "${count:-0}"
}

for chapter in "${chapter_sources[@]}"; do
  source_file="$repo_root/src/chapters/$chapter.typ"
  require_file "$source_file"
  if [[ -f "$source_file" ]]; then
    sections="$(count_matches '^[[:space:]]*#section-title\[' "$source_file")"
    objectives="$(count_matches '^[[:space:]]*#objectives\(' "$source_file")"
    ledgers="$(count_matches '^[[:space:]]*#unit-ledger\[' "$source_file")"
    summaries="$(count_matches '^[[:space:]]*#summary\[' "$source_file")"
    checks="$(count_matches '^[[:space:]]*#knowledge-check\(' "$source_file")"
    questions="$(count_matches '^[[:space:]]*question:' "$source_file")"

    if [[ "$sections" -eq 0 ]]; then
      fail "$source_file has no section-title blocks"
    fi
    for anchor in objectives ledgers summaries checks; do
      if [[ "${!anchor}" -ne "$sections" ]]; then
        fail "$source_file has $sections sections but ${!anchor} $anchor"
      fi
    done
    if [[ "$questions" -ne $((4 * checks)) ]]; then
      fail "$source_file has $checks knowledge checks but $questions questions (expected four per section)"
    fi

    if ! perl -ne '
      if (/^(\s*)#section-title\[/) {
        $bad = 1 if $in_section && !$seen_check;
        $in_section = 1;
        $indent = $1;
        $seen_summary = 0;
        $seen_exam = 0;
        $seen_check = 0;
        next;
      }
      next unless $in_section;
      if (/^\Q$indent\E#summary\[/) {
        $bad = 1 if $seen_check;
        $seen_summary = 1;
        next;
      }
      if (/^\Q$indent\E#exam-prompts\(/) {
        $bad = 1 unless $seen_summary;
        $bad = 1 if $seen_check;
        $seen_exam = 1;
        next;
      }
      if (/^\Q$indent\E#knowledge-check\(/) {
        $bad = 1 unless $seen_summary;
        $bad = 1 if $seen_check;
        $seen_check = 1;
        next;
      }
      if ($seen_check && /^\Q$indent\E#/ && !/^\Q$indent\E#chapter-nav\(/) {
        $bad = 1;
      }
    END {
      $bad = 1 if $in_section && !$seen_check;
      exit($bad ? 1 : 0);
    }
    ' "$source_file"; then
      fail "$source_file has a section-ordering error or content after a knowledge check"
    fi
  fi
done

# Normalized visual quantities use the compact unit syntax [1]. The figure
# source routes every normalized Lilaq axis and legend through shared helpers,
# while animation sources keep the marker in their rendered label text. These
# are source-level checks for a convention that a successful Typst or Manim
# compile cannot detect by itself.
figure_source="$repo_root/src/figures.typ"
theme_source="$repo_root/src/theme.typ"
require_file "$figure_source"
require_file "$theme_source"
if [[ -f "$figure_source" && -f "$theme_source" ]]; then
  if ! rg -Fq '#let normalized-axis(body)' "$theme_source" \
    || ! rg -Fq '#let normalized-label(body)' "$theme_source" \
    || ! rg -Fq '#text("[1]")' "$theme_source"; then
    fail "$theme_source does not define the normalized visual-label [1] helpers"
  fi

  figure_axes="$(rg -n '^[[:space:]]*(xlabel|ylabel):' "$figure_source" || true)"
  normalized_figure_axes="$(rg -n '^[[:space:]]*(xlabel|ylabel):[[:space:]]+normalized-axis\[' "$figure_source" || true)"
  figure_axis_count="$(printf '%s\n' "$figure_axes" | sed '/^$/d' | wc -l | tr -d '[:space:]')"
  normalized_figure_axis_count="$(printf '%s\n' "$normalized_figure_axes" | sed '/^$/d' | wc -l | tr -d '[:space:]')"
  if [[ "$figure_axis_count" -eq 0 ]]; then
    fail "$figure_source has no axis labels to audit"
  elif [[ "$figure_axis_count" -ne "$normalized_figure_axis_count" ]]; then
    fail "$figure_source has an axis label without the normalized-axis [1] helper"
  fi
  if rg -n -i 'dimensionless' "$figure_source"; then
    fail "$figure_source contains the word dimensionless in visual source"
  fi
  normalized_legend_without_helper="$(
    rg -n '^[[:space:]]*label:' "$figure_source" \
      | rg 'tau_D|W=|n_\(|eta=|gamma|omega/omega|lambda_D|nu/omega' \
      | rg -v 'normalized-label' || true
  )"
  if [[ -n "$normalized_legend_without_helper" ]]; then
    fail "$figure_source has a normalized legend without the normalized-label [1] helper"
  fi
fi

for animation_source in "$repo_root"/animations/*.py; do
  [[ -f "$animation_source" ]] || continue
  if rg -n -i 'dimensionless' "$animation_source"; then
    fail "$animation_source contains the word dimensionless in animation source"
  fi
  if rg -qi 'normalized' "$animation_source" \
    && ! rg -Fq '[1]' "$animation_source"; then
    fail "$animation_source documents normalized quantities without a [1] label"
  fi
done

# SI unit-system contract (SPEC.md): Gaussian CGS units and CGS-form text may
# appear only in the CGS translation appendix. The patterns are word-bounded so
# that "energy", "dynamics", "Gauss's law", the label <multiple-gauss-laws>
# and "Gaussian distribution" pass.
# The phrase "Gaussian CGS" is additionally allowed in src/main.typ, whose hub
# card, glossary entry and document title point to that appendix.
cgs_appendix="src/appendices/cgs-translation.typ"
cgs_unit_pattern='\bstat(C|V|A|coulomb|volt|ampere)\b|\berg\b|\bdyn(e|es)?\b|\bcm\b|(^|[^-[:alnum:]])gauss([^-[:alnum:]]|$)'
cgs_phrase_pattern='Gaussian[ -]CGS'
if [[ -d "$repo_root/src" ]]; then
  cgs_hits="$(
    cd "$repo_root" && {
      rg -n --glob "!$cgs_appendix" -e "$cgs_unit_pattern" -- src animations || true
      rg -n --glob "!$cgs_appendix" --glob '!src/main.typ' \
        -e "$cgs_phrase_pattern" -- src animations || true
    }
  )"
  if [[ -n "$cgs_hits" ]]; then
    printf '%s\n' "$cgs_hits" >&2
    fail "CGS units or Gaussian-CGS text found outside $cgs_appendix"
  fi
fi

# Check the Git boundary in a worktree. Nix evaluates the same script from a
# source snapshot without .git, so the artifact checks below remain authoritative
# in that environment and this branch runs in the checkout-based CI job.
if command -v git >/dev/null 2>&1 \
  && git -C "$repo_root" rev-parse --show-toplevel >/dev/null 2>&1; then
  for private_path in solutions resources/books resources/content; do
    if ! git -C "$repo_root" check-ignore --no-index -q \
      "$private_path/.spec-sentinel"; then
      fail "private path is not ignored by Git: $private_path"
    fi
  done
fi

if [[ ! -d "$site_dir" ]]; then
  fail "built site directory is missing: $site_dir"
else
  require_file "$site_dir/index.html"
  require_file "$site_dir/styles.css"
  for chapter in \
    01-introduction \
    02-debye-shielding \
    03-plasma-oscillations \
    04-single-particle-motion \
    05-kinetic-theory \
    06-moments \
    07-multiple-fluids \
    08-mhd \
    09-collisions-conductivity \
    10-diffusion \
    11-introduction-waves \
    12-cold-magnetized-waves \
    13-finite-temperature-waves \
    14-hot-plasma-waves \
    15-sheaths-probes; do
    require_file "$site_dir/chapters/$chapter.html"
  done
  require_file "$site_dir/appendices/mathematical-toolkit.html"
  require_file "$site_dir/media/exb-drift.mp4"
  require_file "$site_dir/media/exb-drift.png"
  require_file "$site_dir/media/plasma-oscillation.mp4"
  require_file "$site_dir/media/plasma-oscillation.png"
  require_file "$site_dir/media/debye-shielding.mp4"
  require_file "$site_dir/media/debye-shielding.png"
  require_file "$site_dir/media/debye-potential-reduction.mp4"
  require_file "$site_dir/media/debye-potential-reduction.png"
  require_file "$site_dir/media/phase-space-advection.mp4"
  require_file "$site_dir/media/phase-space-advection.png"
  require_file "$site_dir/media/moment-hierarchy.mp4"
  require_file "$site_dir/media/moment-hierarchy.png"
  require_file "$site_dir/media/diffusion-random-walk.mp4"
  require_file "$site_dir/media/diffusion-random-walk.png"
  require_file "$site_dir/media/wave-packet.mp4"
  require_file "$site_dir/media/wave-packet.png"
  require_file "$site_dir/media/magnetized-polarization.mp4"
  require_file "$site_dir/media/magnetized-polarization.png"
  require_file "$site_dir/media/magnetosonic-waves.mp4"
  require_file "$site_dir/media/magnetosonic-waves.png"
  require_file "$site_dir/media/landau-resonance.mp4"
  require_file "$site_dir/media/landau-resonance.png"
  require_file "$site_dir/media/two-stream-instability.mp4"
  require_file "$site_dir/media/two-stream-instability.png"
  require_file "$site_dir/media/sheath-formation.mp4"
  require_file "$site_dir/media/sheath-formation.png"
  require_file "$site_dir/media/langmuir-probe.mp4"
  require_file "$site_dir/media/langmuir-probe.png"

  private_artifact="$(find -L "$site_dir" -type f \
    \( -path '*/solutions/*' \
    -o -path '*/resources/books/*' \
    -o -path '*/resources/content/*' \) \
    -print -quit 2>/dev/null || true)"
  if [[ -n "$private_artifact" ]]; then
    fail "private material entered the public site: $private_artifact"
  fi

  if ! rg -q 'href="chapters/[^"#]+\.html"' "$site_dir/index.html"; then
    fail "the overview page does not link to a chapter page"
  fi

  if ! rg -q 'id="bibliography"' "$site_dir/index.html" \
    || ! rg -q 'bibliography' "$site_dir/index.html"; then
    fail "the overview page does not contain the generated bibliography"
  fi

  html_files=()
  while IFS= read -r -d '' html_file; do
    html_files+=("$html_file")
  done < <(find -L "$site_dir" -type f -name '*.html' -print0)

  if ((${#html_files[@]} == 0)); then
    fail "the public site contains no HTML page"
  fi

  for html_file in "${html_files[@]}"; do
    if ! perl -0ne '
      my $html = $_;
      while ($html =~ m{<img\b[^>]*>}sig) {
        my $tag = $&;
        die "image has no non-empty alt attribute\n"
          unless $tag =~ m{\balt\s*=\s*"[^"]+"}i;
      }
    ' "$html_file"; then
      fail "an image in $html_file is missing a non-empty alt attribute"
    fi

    if ! perl -0ne '
      my $html = $_;
      while ($html =~ m{<video\b([^>]*)>(.*?)</video>}sig) {
        my ($attrs, $body) = ($1, $2);
        die "video has no controls\n" unless $attrs =~ m{\bcontrols\b}i;
        die "video has no source\n" unless $attrs =~ m{\bsrc\s*=}i;
        die "video has no accessible alternative description\n"
          unless $attrs =~ m{\baria-label\s*=\s*"[^"]+"}i;
        $body =~ s{<[^>]+>}{}g;
        $body =~ s{&(?:nbsp|#160);}{ }gi;
        $body =~ s{\s+}{}g;
        die "video has no text fallback\n" unless length $body;
      }
      while ($html =~ m{<figure\b[^>]*>(.*?)</figure>}sig) {
        my $figure = $1;
        next unless $figure =~ m{<video\b}i;
        die "video figure has no figcaption\n"
          unless $figure =~ m{<figcaption\b[^>]*>.*?</figcaption>}is;
      }
    ' "$html_file"; then
      fail "an animation in $html_file lacks controls, a fallback, or a caption"
    fi

    if ! perl -0ne '
      my $html = $_;
      while ($html =~ m{<details\b([^>]*)>(.*?)</details>}sig) {
        my ($attrs, $body) = ($1, $2);
        die "details is open by default\n" if $attrs =~ m{\bopen\b}i;
        die "details has no summary\n"
          unless $body =~ m{<summary\b[^>]*>.*?</summary>}is;
      }
    ' "$html_file"; then
      fail "a disclosure in $html_file is missing a summary or is open by default"
    fi

    while IFS= read -r media_ref; do
      [[ -n "$media_ref" ]] || continue
      case "$media_ref" in
        http://*|https://*|//*|data:*)
          continue
          ;;
      esac

      clean_ref="${media_ref%%\?*}"
      clean_ref="${clean_ref%%\#*}"
      if [[ "$clean_ref" == /* ]]; then
        media_path="$site_dir$clean_ref"
      else
        media_path="$(dirname "$html_file")/$clean_ref"
      fi
      if [[ ! -f "$media_path" ]]; then
        fail "media referenced by $html_file is missing: $media_ref"
      fi
    done < <(perl -0ne '
      while ($_ =~ m{\bsrc\s*=\s*"([^"]+)"}gi) {
        my $src = $1;
        print "$src\n"
          if $src =~ m{\.(?:mp4|webm|ogg|mp3|wav|png|svg|jpe?g|gif)(?:[?#].*)?$}i;
      }
    ' "$html_file")
  done
fi

if ((failures > 0)); then
  printf 'spec check failed with %d error(s)\n' "$failures" >&2
  exit 1
fi

printf 'spec check passed for %s\n' "$site_dir"

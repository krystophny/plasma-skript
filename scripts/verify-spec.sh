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

for required in AGENTS.md SPEC.md .gitignore scripts/build-site.sh; do
  require_file "$repo_root/$required"
done

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
    02-single-particle-motion \
    03-kinetic-theory \
    04-moments \
    05-multiple-fluids \
    06-mhd \
    07-collisions-conductivity \
    08-diffusion \
    09-introduction-waves \
    10-cold-magnetized-waves \
    11-finite-temperature-waves \
    12-hot-plasma-waves \
    13-sheaths-probes; do
    require_file "$site_dir/chapters/$chapter.html"
  done
  require_file "$site_dir/media/exb-drift.mp4"
  require_file "$site_dir/media/exb-drift.png"
  require_file "$site_dir/media/plasma-oscillation.mp4"
  require_file "$site_dir/media/plasma-oscillation.png"

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

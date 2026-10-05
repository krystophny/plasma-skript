#!/usr/bin/env bash
# Write the script outline, chapter and section numbers, titles and labels,
# queried from the <script-chapter> and <script-section> metadata that
# src/theme.typ records (page-title, section-title). Each section also names
# the label of its chapter. The lecture slides take their section titles from
# this file, and the SymPy derivations resolve their section references
# (section(..., script="<label>")) through it, so neither restates a number.
#
# Usage: scripts/script-outline.sh [<out-file>]
#        (default: slides/build/script-outline.json)
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
out="${1:-$repo_root/slides/build/script-outline.json}"
mkdir -p "$(dirname "$out")"

typst eval --root "$repo_root" --font-path "$repo_root/fonts" --ignore-system-fonts \
  --input outline-only=true \
  --in "$repo_root/src/print.typ" \
  '{
    let chapter = none
    let sections = ()
    for m in query(selector(<script-chapter>).or(<script-section>)) {
      if m.label == <script-chapter> { chapter = m.value.label }
      else { sections.push(m.value + (chapter: chapter)) }
    }
    (chapters: query(<script-chapter>).map(m => m.value), sections: sections)
  }' >"$out.tmp"
mv "$out.tmp" "$out"

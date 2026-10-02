# Agent instructions

These instructions apply to every task in this repository. `SPEC.md` is the
authoritative project contract. This file is the operational index for Codex
sessions and must stay consistent with the contract.

## Required context

Before changing files:

- Read `SPEC.md` and the relevant source files.
- Use the rendered pages of PDFs in `resources/` when reviewing visual source
  material. Text extraction alone is insufficient for layout, notation, or
  handwritten content.
- Treat `resources/content/` as the authority for chronological order.
- Use `resources/books/` for physics reference only. These directories and the
  exam catalogue are private and must never enter a public artifact.

## Content rules

- Write the first edition in English for a graduate plasma-physics audience.
- Assume zero prior knowledge and infinite intelligence: name and define
  every symbol and term at first use; skip no steps, pad none.
- Keep waves and plasma sheaths as separate top-level chapters.
- Use SI (with ε₀ and μ₀) throughout. State this once, in the notation
  glossary of `src/main.typ`; do not write "SI" or "in SI units" at
  individual equations, notes, captions, or sections. Add a `#unit-ledger`
  only where a section introduces quantities with new units or a
  normalization, and list only those. Gaussian CGS may appear only in the single appendix "Gaussian CGS
  translation" for readers of older literature. Label every unit,
  normalization, reference scale, and dimensionless quantity at its point of
  use. In a simulation, diagram, or animation using dimensionless units, put
  `[1]` after each normalized visual quantity and never write
  `(dimensionless)` in the visual label.
- Use the `unify` Typst package for unit-bearing quantities and numerical
  results whenever its unit parser supports the notation.
- Put exact exam wording in clearly labelled exam-prompt blocks with a source
  location. Teach the prerequisites without answering the exam prompt.
- End every section with four original knowledge-check questions and concise
  answers. Keep exam prompts separate from knowledge checks.
- Include complete theory derivations in `solutions/` and expose them only as
  optional collapsed details when appropriate. A `Rechenbeispiel` has data,
  assumptions, target, and numerical result only. It has no derivation in the
  script or in `solutions/`.

## Accessibility and components

- Give every meaningful graphic and animation a concise alternative
  description. Preserve a visible caption and a non-animated explanation for
  every animation.
- Use `html.details(open: false)` with a visible `html.summary` for optional
  details. Keep definitions, essential equations, figure descriptions, and
  knowledge-check questions visible.
- Use stable shared components in `src/theme.typ`. Use Frame-It for highlighted
  teaching blocks, CeTZ or Fletcher for semantic diagrams, Lilaq for data
  plots, and Manim for explanations that benefit from time evolution.
- Keep color from being the only encoding of a physical quantity or category.

## Public boundary and licensing

- Never publish or force-add `solutions/`, `resources/books/`, or
  `resources/content/`.
- Publish original teaching material under CC BY 4.0 and code, build scripts,
  Manim source, theme code, CSS, Nix expressions, and workflows under MIT.
- Preserve third-party copyright and record contributions in
  `CONTRIBUTORS.md`.

## Change and verification workflow

1. Inspect existing files and preserve unrelated worktree changes.
2. Use `apply_patch` for source edits and stage explicit paths when staging is
   requested. Do not create a commit or publish without an explicit request.
3. Build the actual site and inspect its generated HTML, media, and optional
   PDF when that target is enabled.
4. Run `nix run .#verify-spec -- <built-site>` and `nix flake check`.
5. Report the commands run, the artifact inspected, and any unresolved spec
   conflict.

If the specification is ambiguous or two authoritative sources conflict, stop
at that decision and ask the project authors. Do not silently weaken a rule or
invent exam wording.

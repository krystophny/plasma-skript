# Graduate plasma physics lecture script

Status: draft for interactive review

This specification defines the content, authoring, accessibility, and publishing
rules for the graduate plasma physics lecture script. The website is the primary
reading format and the interactive playground is the main publication. A print
PDF is an optional compatibility artifact, generated only when all
HTML-specific components have an equivalent paged fallback.

## 1. Confirmed decisions

- The audience is graduate students in plasma physics or a closely related
  physics program.
- Assume zero prior knowledge and infinite intelligence: every symbol and
  term is named and defined at first use, no step is skipped because readers
  "know it", and no step is padded because they might be slow.
- Christopher Albert and Maximilian Philipp are the initial project authors and
  maintainers. No university ownership claim applies to their work.
- The first publication is in English. The source structure and component
  interfaces should remain translation-ready for a later German edition.
- SI (with the vacuum constants ε₀ and μ₀) is the dimensional unit system
  throughout. It is stated once, in the notation glossary, and is not
  repeated at individual equations, notes, captions, or sections. Normalized
  variables are welcome, but every normalization must state its reference
  scales and how to reconstruct dimensional quantities. A single appendix, "Gaussian CGS translation", lists
  the corresponding Gaussian CGS forms for readers of older literature; it is
  the only place where CGS units or CGS-form equations may appear.
- Use the versioned `unify` Typst package for unit-bearing quantities and
  numerical results whenever its parser supports the notation. Do not replace
  it with ad hoc unit formatting in new content.
- In Typst math, explicitly group a subscript or superscript before an argument
  or bracketed application: write `f_(s)(x)`, `f^(a)(x)`, and `C_(s)[f]` rather
  than relying on `f_s(x)`, `f^a(x)`, or `C_s[f]`.
- Typst fraction parsing is precedence-sensitive. Parenthesize the complete
  numerator or denominator whenever it contains more than one factor, an
  operator, or a derivative: write `(a b)/c` and `a/(b c)`, never `a b/c` or
  `a/b c` when the grouped expression is intended. This applies equally to
  physical expressions such as `(m_(s) v^2)/2`, `(q_(s) n_(s))/(epsilon_0
  m_(s))`, and `(k_B T_e)/(2 e)`.
- Use the derivative operators supplied by `physica`: `dv(f, x)` or
  `derivative(f, x)` for ordinary derivatives, and `pdv(f, x)` or
  `partialderivative(f, x)` for partial derivatives. Do not typeset an
  ordinary or partial derivative as a handwritten `dif f/dif x` expression.
  Keep `dif x` for differentials in integrals and differential forms. Put
  indices on the operand, for example `dv(g_(s), t)`, rather than on the
  derivative operator.
- Quantities in equations, numerical values, tables, plots, animations,
  captions, axes, legends, and alternative descriptions carry their units;
  the unit system itself is not restated. A quantity without a unit is
  explicitly marked as dimensionless or normalized.
- A simulation, diagram, or animation using dimensionless or normalized units
  must show the unit as `[1]` after each normalized quantity in its visible
  labels, for example `$x/lambda_D$ [1]`. The word `dimensionless` must not
  appear in an axis, legend, or other in-graphic label. Captions and
  alternative descriptions still state the normalization and its reference
  scales.
- Dimensional and normalized quantities must not be mixed silently. Temperature
  conventions (kelvin or electronvolt) and field conventions must be stated at
  the point of use.
- The website is authoritative. A PDF may be generated from the same source
  components when the typed HTML has a readable paged fallback, but PDF support
  must never constrain the interactive website or block its release.
- The initial playground scope is interactive reading: collapsible theory,
  media controls, navigation, accessible prompts, and readable plots. Live
  parameter controls and browser-side recomputation are out of scope unless
  explicitly added in a later revision.
- The published site includes a visible bibliography with citations for the
  physics sources, source material, figures, and external documentation used
  in the script. The public `src/sources.bib` file is the source database;
  citations use Typst's native `@key` or `#cite(<key>)` syntax and the
  bibliography uses a numeric physics style.
- The website provides an overview page, table of contents, chapter pages,
  stable section anchors, and previous or next chapter navigation.
- A shared notation glossary holds the single statement of the SI
  convention and records symbols,
  sign conventions, temperature conventions, and normalized-variable names.
- The `solutions/` directory is author-only material. It is ignored by Git and
  excluded from every public build and GitHub Pages artifact.
- GitHub Pages is a supported deployment target. The workflow publishes only
  the generated static site bundle from the default branch.
- Preserve the established reference order; the rendered course PDFs in
  `resources/content/` are historical evidence. The course plan owns the live
  selection and multi-year evidence can improve explanations.
- The script must include waves and plasma sheaths, even though the current exam
  catalogue ends with single-fluid MHD.
- Waves and sheaths must remain separate top-level chapter boundaries. The
  planned wave chapters may retain their internal subdivisions, but they must
  not be merged with the sheath chapter.
- The books in `resources/books/` are private reference material for checking
  explanations, derivations, terminology, and examples. They are not a source
  for copying text or figures into the published script.
- The exam catalogue is a coverage and difficulty signal. Relevant exam
  questions may appear in the section where their subject is taught, but only
  in a separate, clearly labelled exam-prompt block. The script must not solve
  those questions directly or present an answer key for them. It must
  nevertheless teach all concepts, equations, and assumptions needed to
  construct a meaningful answer.
- Rhetorical questions and explanatory examples in the script are answered in
  place.
- `Rechenbeispiele` provide the given data, conventions, target quantity, and
  numerical result. They do not include a derivation in the main script.
- Every section ends with original knowledge-check questions and their concise
  answers. Complete theory derivations belong in a separate solutions
  handbook, while `Rechenbeispiele` never receive a derivation.
- Every meaningful graphic and animation has an accessible alternative
  description.
- Exam prompts use the exact wording of the exam catalogue. Their source file
  and page or section should be recorded, and any uncertain transcription must
  be flagged for visual review rather than silently paraphrased.
- The Typst CLI comes from `nixpkgs-unstable`. The flake must keep Typst
  unpinned in the expression so that a deliberate flake update obtains the
  current unstable package.

## 2. Source roles and chronology

The 2026-10-05 course decision preserves this complete reference, including
guiding-center and linear/kinetic-response material. Live teaching can cover
a smaller selection at greater mathematical depth. Neither live pacing nor
the boundary with the adjacent kinetic course requires removal of reference
content. The teaching-tree plan, `lv/plasma/PLAN.md`, owns live selections and
examination policy and the final chapter cutoff; this specification owns the full authoring contract.

Use lecturer explanations, original notes and the strongest evidence across
all generations. The local archive at `../fusion-course-archive` contains processed evidence,
distillations, retained raw recordings and edited drafts. Reconcile that
evidence section by section; availability does not establish incorporation.
Record accepted improvements against stable script section IDs. Preserve
the current chapter order unless a scientific dependency or explicit lecturer
decision justifies a change.

Source roles are deliberately separated.

| Source | Use | Authority |
| --- | --- | --- |
| `resources/content/Chapter 1-5.pdf` | Established order and emphasis for chapters 1 through 5 | Historical evidence; private, never publish |
| `resources/content/Chapter 6.pdf` | Visual single-fluid MHD sequence | Historical evidence; private, never publish |
| `resources/content/Chapter 7.pdf` | Visual collisions and plasma conductivity sequence | Historical evidence; private, never publish |
| `resources/content/Chapter 8.pdf` | Visual plasma diffusion sequence | Historical evidence; private, never publish |
| `resources/content/Plasma Physics Exam.pdf` | Topic coverage and expected graduate-level depth | Assessment signal only; private, never publish |
| `resources/books/` | Physics reference and derivation cross-checks | Reference only; private, never publish |
| `resources/typst/` | Typst and package API reference | Implementation reference |

The chapter sequence, with the requested split of the opening material, is:

1. Introduction: plasma examples, characteristic scales, and model hierarchy
2. Debye shielding
3. Plasma oscillations
4. Single-particle motion
5. Kinetic theory of plasmas
6. Moments of the Boltzmann equation
7. Multiple-fluid theory
8. Single-fluid theory and magnetohydrodynamics
9. Collisions and plasma conductivity
10. Plasma diffusion
11. Introduction to waves in plasmas
12. Waves in cold magnetized plasmas
13. Collisions, ions, and finite-temperature effects on magnetized waves
14. Waves in hot plasmas
15. Plasma sheaths and Langmuir probes

The opening material is split into three chapters at the author's request:
an introduction with examples and a scale/model overview, followed by dedicated
shielding and oscillation chapters. The introduction keeps the physical ideas
and temperature conventions, with section links to quantitative treatments.
Screening and coupling criteria belong in the shielding chapter; plasma-frequency
relations belong in the oscillation chapter; orbit and combined numerical scale
estimates belong in single-particle motion. Distribution formulas, microscopic
field equations, and quantum-degeneracy criteria belong in kinetic theory;
moment equations and closures belong in the moments chapter.
This supersedes the former combined
introduction. Subsequent topics preserve the established content-PDF order.
The wave/sheath structure remains a complete reference. Recent slides and
books do not independently dictate future live coverage. Resolve conflicting
scientific sources through lecturer review; do not copy a book's organization
or wording merely to fill an undeveloped live topic.

The chronological course map is followed by a supplemental mathematical
toolkit. It is not a sixteenth physics chapter: it collects the energy-weighted
second moment and coordinate-operator derivations used across the sequence.

The content PDFs have been reviewed as rendered pages. The combined
`Chapter 1-5.pdf` file is a mixed source packet rather than a uniform slide
deck. It contains a welcome page, course-material and textbook-page captures,
handwritten derivations, diagrams, and exam pages with annotations. The
standalone chapters 6 through 8 are predominantly board-style handwritten
pages with typed equations, colored annotations, and sketches. These artifacts
are evidence of sequence and emphasis. They are not final publication assets.
The script must redraw the mathematics, diagrams, and plots as native Typst,
CeTZ, Fletcher, Lilaq, or Manim content where possible.

The printed reference material has been reviewed visually as chapter openers
and contents pages. Its wave and sheath chapters are a coherent extension of
the first eight course chapters, with the chapter boundaries listed above.
The Typst and package manuals are implementation references. Their examples,
API tables, diagrams, and accessibility guidance must be consulted in their
rendered form when implementing a component.

The visual source suggests the following internal progression. These are
planning anchors, not mandatory subsection names:

- Introduction: examples of plasmas, quasi-neutrality, speed, energy,
  temperature, characteristic lengths and times, and model hierarchy.
- Debye shielding: equilibrium electron response, screened Poisson equation,
  the Debye length, and finite-source screening.
- Plasma oscillations: electron displacement, the restoring electric field,
  and the cold electron plasma frequency.
- Single-particle motion: uniform-field gyration, `E × B` drift, nonuniform
  magnetic fields, gradient and curvature drifts, magnetic moment and mirrors,
  polarization drift, and cyclotron resonance.
- Kinetic theory: gas versus plasma collisions, distribution functions,
  Maxwell-Boltzmann states, the Boltzmann or Vlasov equation, and convective
  derivatives in physical and phase space.
- Moments: zeroth, first, and second moments, continuity, momentum and energy
  transport, pressure tensors, cold and warm models, and closure.
- Multiple fluids: the complete two-fluid equations, perpendicular drifts, and
  parallel pressure balance.
- MHD: single-fluid conservation laws, generalized Ohm's law, simplified MHD,
  frozen-in flux, magnetic-field diffusion, force balance, magnetohydrostatics,
  pinch configurations, and the strong-field collisionless limit.
- Collisions and conductivity: weakly and fully ionized plasmas, Coulomb
  collisions, specific resistivity, DC and AC conductivity, and ion motion.
- Diffusion: random-walk motivation, weakly ionized diffusion, ambipolar
  diffusion, diffusion across a magnetic field, and fully ionized diffusion.
- Waves: small-amplitude wave assumptions, nonmagnetized plasma modes, cold
  magnetized dispersion, oblique propagation, collisional and ion effects,
  finite-temperature corrections, MHD waves, hot isotropic waves, the
  two-stream instability, and hot magnetized waves.
- Sheaths and probes: particle flux, sheath characteristics, current balance,
  and the Langmuir probe as a plasma diagnostic.

The exam-derived minimum coverage is expressed as competencies rather than
copied prompts:

| Area | The script must enable students to |
| --- | --- |
| Introduction | identify collective behavior, distinguish thermal and bulk motion, explain the role of observation scales, and navigate the model hierarchy |
| Debye shielding | derive the screening length and assess collective and quasineutral orderings |
| Plasma oscillations | derive the cold restoring response and relate its frequency to thermal and screening scales |
| Single-particle motion | derive gyration and homogeneous-force drifts, use guiding-center assumptions, explain magnetic moments and mirrors, and classify common drifts |
| Kinetic theory | interpret a distribution function, reason in phase space, relate mean free path to collisions, and distinguish convective and conservative kinetic equations |
| Moments and closure | obtain fluid variables from a distribution, derive continuity and the structure of higher moment equations, interpret pressure tensors, and explain closure choices |
| Multiple-fluid theory | formulate a hydrogen two-fluid model and derive the physical meaning of diamagnetic drift and current |
| MHD | define single-fluid variables, linearize the equations, motivate Ohm's law and resistivity, explain frozen flux, derive magnetic diffusion and its timescale, and interpret static equilibrium |
| Waves | derive and interpret dispersion relations, state the assumptions behind cold, warm, collisional, and hot descriptions, and connect wave branches to limiting cases |
| Sheaths and probes | explain sheath formation, identify the relevant scales and current balance, and interpret the physical information obtained from a Langmuir probe |

## 3. Section contract

Each section must use the following order unless there is a documented reason
to deviate:

1. Motivation and a physical question.
2. Learning objectives written with observable verbs.
3. Definitions, notation, units, and assumptions.
4. The physical argument or derivation.
5. A visual explanation, simulation, or a `Rechenbeispiel` with stated data and
   a final numerical result only.
6. Model limits, approximations, and connections to the next model.
7. A short summary of the section's governing ideas.
8. An optional exam-prompt block containing relevant exam questions.
9. A knowledge check as the final section element.

Derivations must identify assumptions before they are used. They must define
new symbols, preserve sign conventions, state the approximation regime, and
include dimensional or limiting-case checks when those checks are meaningful.
The prose should explain what each equation says physically before introducing
the next equation.

The narrative must distinguish clearly between:

- exact identities and model equations,
- assumptions and consequences,
- illustrative normalized simulations and measured data,
- dimensional quantities and normalized quantities,
- equilibrium, linearized, weakly nonlinear, and fully nonlinear statements.

### 3.1 Unit-system contract

The SI convention (with ε₀ and μ₀ in the field equations) is stated once, in
the notation glossary; chapters, sections, equation notes, and captions do not
restate it. A section carries a unit ledger only when it introduces quantities
with new units (for example a phase-space density, a diffusion coefficient, or
a resistivity) or a normalization, and the ledger lists only those. Temperature
conventions are stated where temperature is first used. A normalized model must show
the definitions of its dimensionless variables and identify every reference
scale needed to recover a dimensional result.

Plots and animations must label normalized axes with the normalization itself,
followed by the unit syntax `[1]`, not only with a variable name. Numerical
results must either carry their units or explicitly say that they are
dimensionless. Conversions to Gaussian CGS belong only in the translation
appendix and never replace the primary SI equations.

## 4. Knowledge checks

Every section must end with a knowledge-check block containing four original
questions. The set should mix conceptual explanation, interpretation of an
equation or diagram, a short derivation plan, a scaling or estimation task,
and at least one limiting-case or model-selection question when appropriate.

### 4.1 Exam connections

Relevant questions from the exam catalogue should be placed in the section
that supplies their physical and mathematical prerequisites. They must appear
in a separate `Exam questions` block, visually distinct from
the knowledge checks and preferably styled with the component library. The
block invites the reader to think about the prompt and reproduces its exact
wording, together with a source file and page or section. Uncertain wording is
a review item and must not be silently paraphrased.

Exam prompts are not counted among the four knowledge checks. They must not be
followed by a direct answer, derivation, or answer-key language. The surrounding
script should provide the theory needed to reason about them, without revealing
the expected exam response. The final knowledge-check block remains the last
section element.

Questions must test transfer of understanding. They must not be one-to-one
rewrites of the exam catalogue and must not disclose the exam's expected
answers.

Each knowledge-check question must have a matching concise answer in the
source. An answer should give the conclusion first, then the essential
reasoning, assumptions, units, and limiting-case check. Complete theory
derivations may be placed in an expandable detail block on the website, but the
short answer must remain understandable without opening it. The complete
derivation must also be retained in `solutions/`.

Exam questions are never copied into the knowledge checks. They are only
included in the separate exam-prompt block and are never paired with direct
answers. Coverage is achieved by teaching the relevant reasoning in the
surrounding sections and by asking new knowledge-check questions that transfer
the same ideas to a different setup.

Rhetorical questions and explanatory examples are not knowledge checks. They
should be answered where they occur so that the narrative does not leave an
open conceptual gap.

For a `Rechenbeispiel`, the main script contains only:

1. the physical context and relevant assumptions,
2. all numerical data and constants required for the calculation,
3. the requested quantity with units, and
4. the numerical result with units and an appropriate precision.

It must not contain the calculation path or derivation. No derivation for a
`Rechenbeispiel` may be added to the solutions handbook either. The numerical
result is the only solution detail published for that example.

## 5. Accessibility contract

Accessibility is part of content correctness, not a later styling pass.

### 5.1 Graphics

- Every non-decorative image, plot, diagram, path drawing, and visualization
  must have a concise alternative description. It is exposed to assistive
  technology only (alt text, `aria-label`, video fallback content) and is
  never rendered as visible text below a figure or video.
- Use Typst's semantic `figure(alt: ...)` mechanism for graphics without their
  own alternative-description parameter. Put the figure markup at the point
  where it belongs in the reading order.
- The alternative description must state the important objects, relationships,
  direction, trend, or conclusion. It should not list irrelevant visual
  details or repeat a caption word for word.
- Text that carries meaning must remain native Typst text, not text drawn into
  an image.
- A decorative shape may be marked as a PDF artifact only when it adds no
  information.
- Color must never be the only encoding of a physical quantity or category.
  Use labels, line styles, markers, annotations, or position as additional
  encodings.

### 5.2 Animations

Every animation must provide all of the following:

- a concise figure-level alternative description,
- a visible caption explaining the physical process,
- a short text description of the sequence of states or the key observation,
- a static poster or equivalent still graphic for any paged output and for
  media that cannot play video,
- accessible playback controls (native without JavaScript, click/keyboard
  play-pause and a labelled bottom seek bar/fullscreen icon with JavaScript),
  no required audio, and no information conveyed only by
  motion.

The animation component must use the description in the HTML fallback content
and in the paged caption or fallback panel. A student must be able to learn the
intended physical conclusion without watching the video.

### 5.3 Expandable content

Use the typed HTML disclosure element for optional detail. Its visible
`html.summary` child is the reader's anchor when the derivation is collapsed:

```typst
#html.details(open: false)[
  #html.summary[Derivation: obtain the guiding-center drift]
  Supplemental derivation or explanation.
]
```

The `open: false` default supports the presentation style. The summary should
name the purpose of the hidden material and, where useful, state the result or
regime it establishes. Use a short visible `Key idea` frame, a two-to-four-item
`What to watch` list, and a `Pause and predict` prompt around demanding
derivations or animations. These anchors remain outside the disclosure and are
not additional knowledge checks. A rhetorical or predictive prompt must have
its answer in the surrounding narrative or in an explicitly labelled reveal.

Use `html.details` for optional theory derivations, longer proofs,
implementation notes, and answers to the script's own knowledge checks. Do not
use it to smuggle an answer to an exam-catalogue question into the public
output. The typed HTML reference defines `html.details` with a body and an
`open` state, and defines `html.summary` as the caption for the disclosure.
The collapsed view must retain the physical question, assumptions, governing
equation or final result, and a short interpretation. Intermediate algebra and
long derivations may remain inside the disclosure. Use a visible `Key idea`
frame, a two-to-four-item `What to watch` list, and an optional `Pause and
predict` prompt to support lecture engagement. A pause prompt is not an
additional knowledge check and must have its answer in the surrounding
narrative or in an explicitly labelled reveal.

The paged target must render the same information as a normal labelled block or
frame rather than depending on an interactive disclosure control. If the
current Typst HTML exporter cannot provide that fallback cleanly, the PDF
target is optional and the website remains the release target.
Never hide required definitions, core equations, essential figure
descriptions, or the knowledge-check questions themselves. The paged target
must render the same information as a normal labeled block or frame rather than
depending on an interactive disclosure control.

## 6. Typst and package policy

The authoring environment is defined by `flake.nix`:

- `pkgs.typst` from the `nixpkgs-unstable` input is the only required Typst CLI.
- `pkgs.manim` renders animations.
- `pkgs.ffmpeg` provides video handling.
- The flake exposes `build-site` and `verify-spec` apps. Use
  `nix run .#build-site` and `nix run .#verify-spec -- <built-site>` for
  development and release checks; the shell scripts remain implementation
  details used by the package and CI.
- `build-site` must render into a staging directory and publish it only after
  all required poster, website, slide and PDF outputs succeed (plus rendered
  videos in local hosting mode), preserving the previous
  complete bundle if a build fails.
- `public-host` serves the existing site by default. It warns when local source
  timestamps are newer than the built index, without rebuilding automatically.
  Its explicit `--build` option builds before serving and must stop on build
  failure. It builds and serves the same `SITE_DIR`, or `public/` by default.
  `local-host` remains serve-only. When invoked from the
  project root, development builds include the current working-tree sources,
  including new files not yet added to Git.
- The `verify-spec` app checks both the public artifact boundary and the
  source-level section contract: every chapter must provide matching section,
  objective, summary, and knowledge-check blocks (unit ledgers are optional
  and appear only where a section introduces new units), with four
  knowledge-check questions per section; the summary, optional exam prompt,
  and knowledge check must occur in that order at the end of each section.
- `nix flake check` must build the site as a behavioral check.
- On Linux, `nix flake check` also runs the NixOS VM browser integration test
  against the built site. The test uses real CSS viewport emulation rather
  than inferring mobile behavior from a resized screenshot.
- The website must be buildable from the shared source components. A PDF target
  may use those components when an equivalent paged rendering is available.

Package imports must use explicit package versions. The local documentation
snapshots provide these starting API baselines:

- `physica` for vectors, differential operators, derivatives, tensors, matrix
  notation, and other scientific mathematical notation.
- `cetz` for precise field-line, orbit, geometry, and coordinate diagrams.
- `fletcher` for flow charts, model hierarchies, derivation maps, and other
  arrow-heavy diagrams.
- `lilaq` for dispersion plots, parameter scans, distribution functions,
  phase-space projections, and other data-driven plots.
- `frame-it` for definitions, assumptions, examples, warnings, derivation
  summaries, physical interpretations, and knowledge-check presentation.
- `unify` for unit-bearing quantities and numerical results, with any
  normalized convention stated nearby; use its default SI unit catalogue.

Use the APIs documented in the corresponding PDFs under `resources/typst/`.
The imported version must be updated deliberately when the package API or the
Typst unstable toolchain changes. The source should not rely on an undocumented
package behavior.

### 6.1 Expression precedence and derivative syntax

Parentheses in a Typst math expression are semantic grouping, not cosmetic
spacing. The slash operator binds only to the adjacent term. Before reviewing
the physics, inspect every compound fraction and ask which complete product or
sum must appear above and below the bar. In particular, check kinetic-energy,
pressure, current, force, wave-response, exponential, square-root, and
normalized-unit expressions. A successful Typst compile does not establish
that the fraction has the intended meaning.

The preferred Physica forms are the following:

```typst
$ (m_(s) v^2)/2 $
$ a/(b c) $
$ dv(f, x) $
$ pdv(f, t) $
$ dv(g_(s), t, d: upright(D)) $
```

Use the full `derivative` and `partialderivative` names when an abbreviated
operator would be unclear. Use `dv` for an ordinary derivative and `pdv` for
a partial derivative; do not mix a handwritten derivative fraction with a
Physica derivative in the same derivation. A species, tensor, or other index
belongs inside the derivative operand. Powers of a derivative must also be
grouped when they are part of a fraction, for example `((dv(V, s))^2)/2`.

For a material derivative, either expand it explicitly as
`pdv(f, t) + u dot grad_(bold(r))(f)` or define the material-derivative
notation before using it. An unexplained `D` must not be allowed to look like
an ordinary partial-time derivative. The `d: upright(D)` form above is only
appropriate after that operator label and its meaning have been defined.

### 6.2 Rendered equation and frame audit

Math and component markup must be checked in the rendered targets, not only in
the source or compiler diagnostics. Any change to equations, `equation-note`,
Frame-It usage, or the shared stylesheet requires a small focused render
containing representative grouped fractions, `dv`/`pdv` expressions, a long
frame title such as `Cold, unmagnetized, collisionless response assumptions`,
and an equation note directly below a display equation.

The focused check must cover both a wide layout and a narrow layout. Inspect
the generated HTML in a browser or equivalent rasterized page view and inspect
the paged PDF with rendered page images when PDF output is enabled. The review
must confirm that:

- the intended complete numerator and denominator are visibly on the correct
  sides of the fraction bar;
- derivative order, variable, indices, and ordinary versus partial status are
  visible and mathematically correct;
- equation notes have readable separation from the equation above them;
- long Frame-It titles wrap without moving the title into an unintended row;
- the Frame-It header has no stray rounded tail, empty connector, loop, or
  horizontal artifact after the title; and
- the paged rendering preserves the same mathematical grouping and teaching
  meaning as the HTML rendering.

The HTML build must enable the Typst HTML feature explicitly with
`TYPST_FEATURES=bundle,html`. Preserve the shared CSS rule that keeps the
Frame-It title span flexible, removes the empty connector span, and keeps the
semantic frame counter separate. Do not repair a wide-title regression by
putting the title on its own line unless the component contract is deliberately
changed and re-audited at both widths.

## 7. Visual and component conventions

Create reusable components in the shared Typst theme instead of styling each
chapter independently. At minimum, the theme should provide components for:

- section objectives,
- definitions and physical laws,
- assumption ledgers,
- derivation steps,
- intuition or interpretation notes,
- worked estimates,
- knowledge checks and answers,
- figures with required alternative descriptions,
- animations with fallbacks, and
- expandable supplemental details,
- chapter navigation and stable anchors,
- glossary entries, and
- citations and bibliography output.

Frame-It is the default treatment for highlighted content. Frame kinds should
have stable meanings and should not communicate meaning by color alone. Keep
the visual hierarchy quiet enough that equations and explanatory prose remain
the primary reading path.

Use CeTZ and Fletcher diagrams when a semantic vector graphic is clearer than a
raster image. Use Lilaq when the reader needs to compare numerical or
functional behavior. Use Manim when time evolution, orbit geometry, wave
propagation, or sheath formation is materially easier to understand in motion.
Every visual must answer a stated pedagogical need and have an alt description.
For normalized visual quantities, use `[1]` as the displayed unit and omit
`(dimensionless)` from axes, legends, and in-graphic labels.

## 8. Manim workflow

Each scene must:

- use a deterministic parameter set and document whether quantities are
  dimensional or normalized,
- render every in-scene prose label in STIX Two Text, explicitly registered
  from the repository's `fonts/` so rendering never depends on a
  host-installed fallback, and every MathTex label in STIX Two through the
  `stix2` LaTeX package (`animations/style.py`),
- append `[1]` to every normalized axis label; other in-scene labels are bare symbols without unit tags;
  do not write `(dimensionless)` in the scene,
- have a stable scene name and output path,
- include a still frame or poster asset,
- expose the physical variables and conventions in nearby Typst prose,
- avoid relying on color or motion alone,
- never animate two different systems or parameter cases side by side at the
  same time, because no one can follow both: run case A at full width, then
  case B in the same layout from the same initial state, and optionally end on
  a still side-by-side pair of the final states, without motion, held for
  about 3 s; linked views of one system (e.g. phase space and the histogram of
  the same ensemble, or particles and the density profile of the same
  simulation) may still run together,
- render successfully inside `nix develop`, and
- be checked against a simple analytical or numerical expectation.

Animations are explanatory assets, not substitutes for derivations. The script
must state the model, initial conditions, and validity limits of each scene.

## 9. Publishing and review gates

Before a chapter is considered complete:

- the website bundle compiles from the shared source,
- the chapter is reachable through the table of contents and chapter
  navigation,
- all referenced media are present in the bundle,
- every meaningful visual has an alternative description and caption,
- every animation has a non-animated explanation and fallback,
- every section ends with original questions and matched answers,
- supplemental details are optional rather than required for comprehension,
- equations pass a dimensional and limiting-case review,
- citations resolve and the bibliography is visible,
- the chapter's sequence agrees with the applicable content slides, and
- the result passes `nix flake check`.

If PDF output is enabled for a release, it must also compile from the shared
source, preserve the information exposed by the website, and pass a visual
rendering check. Failure of an optional PDF target must not make the website
check fail.

The automated checks must verify behavior such as successful rendering,
presence of media and disclosure elements in the generated site, and, when
enabled, validity of the PDF. A check that only compares repository state with
the source patch is not sufficient.

The NixOS browser integration test is an independent behavioral check. It
serves the built static bundle in a NixOS VM and audits every page at mobile,
tablet, and wide CSS viewports. It checks page-level overflow, closed
disclosures, accessible images and animations, browser errors, and failed local
requests. It also captures representative diagram, equation, Frame-It, and
animation screenshots into the Nix test output for visual review. These
screenshots are evidence artifacts, not pixel-perfect golden tests, so browser
and font updates do not create needless failures.

### 9.1 GitHub Pages

The GitHub Actions workflow builds the site with the flake, copies only the
generated static bundle into the Pages artifact, and deploys from `main`.
Pull requests may build and validate the artifact but must not deploy it.
Author-only material, including `solutions/`, must never be copied into the
artifact.

## 10. Solutions handbook

The solutions handbook lives under `solutions/` in this repository and is a
non-public artifact. It is excluded from the public build by default.

It must contain every step of every theory derivation used by the course,
including intermediate algebra, assumptions, discarded terms, boundary or
initial conditions, dimensional checks, and limiting cases where applicable.
Those derivations may be exposed selectively through closed `html.details`
blocks when an author chooses to publish supplementary theory.

It must not contain a calculation path or derivation for any `Rechenbeispiel`.
For those examples, the main script and handbook contain only the stated data,
the task, and the numerical result. The handbook may contain author
verification notes for theory, but it must not become an exam answer key.

The handbook should reuse the same notation and component library as the main
script so that symbols and theory statements stay consistent.

## 11. Licensing and contributions

The project uses a split license because it contains both publishable teaching
material and software-like source code.

### 11.1 License scope

The full script and original assets are prepared for a CC BY 4.0 edition.
Mixed legacy/new video courses remain access-restricted during replacement;
legacy videos and textbook scans never enter that open edition by default.
The already public script remains public. Follow `lv/AGENTS.md`, "FuEL
delivery", for weekly replacement and separate upload/release gates.

Write explanations independently, with citations for physics references.
Do not reproduce textbook prose, screenshots, distinctive figure layouts or
illustrations. Generate/draw figures from our own physical models and cited
data, or use assets with recorded public-domain/CC BY provenance. Cosmetic
redrawing is not an originality check. Record each external asset's author,
source, exact license, modifications and attribution. Build checks and license
declarations do not alone certify originality or asset clearance.

- Original lecture prose, authored equations as presented, diagrams, plots,
  rendered animations, posters, captions, alternative descriptions, and other
  teaching material: `CC BY 4.0 International`.
- Build scripts, Manim source code, Typst theme code, CSS, Nix expressions, and
  GitHub Actions workflows: `MIT`.
- Third-party books, course PDFs, exam PDFs, figures, and other copyrighted
  references: no project license. They remain private or are used only under
  permission or a valid exception, with appropriate bibliographic citation.

Creative Commons recommends using its 4.0 international licenses for global
distribution rather than treating the absence of a country-specific port as a
defect. The project should link to the canonical CC BY 4.0 license and may also
link to its German-language deed. This is not a guarantee that one license
overrides every legal system. Mandatory local rules, moral rights, privacy and
personality rights, collecting-society arrangements, institutional ownership,
and third-party rights still need to be respected. Any university or employer
rights in contributed work must be resolved before publication.

CC BY 4.0 permits sharing and adaptation with attribution, including
commercial use. The project intentionally does not impose a share-alike
requirement on downstream adaptations. Contributions accepted into the project
are licensed under the applicable project license, while downstream users may
choose another compatible license for their own adaptations.

### 11.2 Contributions and attribution

Contributors retain their copyright. Before accepting a contribution, the
project must obtain an explicit grant to distribute and adapt it under the
applicable project license, together with a confirmation that the contributor
owns the work or has permission to license it. A short contribution statement
in `CONTRIBUTING.md` and a pull-request template should make this agreement
clear; a separate copyright transfer is not required by default.

The public `CONTRIBUTORS.md` list records each contributor's preferred public
name or handle and a concise description of the contribution. Contributors
choose that attribution name when they contribute. The project must not publish
private contact details, affiliation, or legal names without separate consent.
Substantive corrections and additions should be credited, while trivial typo
fixes may be grouped in a release entry.

The same attribution policy applies to translations, accessibility work,
visual design, derivation review, and corrections. The contributor list is an
additional recognition record; it does not replace the attribution notices
required by the content license.

## 12. Licensing release checks

Before the first public release and before accepting a contribution where
ownership is uncertain, check whether university, employer, or
funding-agreement terms impose additional ownership or attribution
requirements. A contributor's permission is not sufficient to publish material
owned by another rights holder.

## 13. Local references

- [MIT License](LICENSE)
- [CC BY 4.0 content license](LICENSE-CONTENT.md)
- [Contribution policy](CONTRIBUTING.md)
- [Contributor register](CONTRIBUTORS.md)
- [Typst reference](resources/typst/typst-reference.pdf)
- [Physica manual](resources/typst/physica-manual.pdf)
- [CeTZ manual](resources/typst/cetz-manual.pdf)
- [Fletcher manual](resources/typst/fletcher-manual.pdf)
- [Frame-It manual](resources/typst/frame-it-manual.pdf)
- [Lilaq documentation snapshot](resources/typst/lilaq-documentation.pdf)
- [Typed HTML `details` reference](https://typst.app/docs/reference/html/typed/#functions-details)
- [Creative Commons Attribution 4.0 International deed](https://creativecommons.org/licenses/by/4.0/)
- [Creative Commons Attribution 4.0 International legal code](https://creativecommons.org/licenses/by/4.0/legalcode.en)
- [Creative Commons FAQ on international licenses](https://creativecommons.org/faq/)

## Animation hosting (2026-10-05)

`media/animations.json` owns stable HTML player URLs, versioned Nextcloud MP4
streams, checksums and posters. Native HTML video
is the maintained animation player. The website, lecture slides and print PDF
use the same register; PDF links open `animations/<slug>.html`, not the MP4's
attachment/download endpoint. Public player pages are stable across revisions.
The Nextcloud MP4 filename stays stable; a checksum query changes with each
revision to avoid stale media caches. Short animations are hosted on Nextcloud;
their YouTube uploads are removed at Chris's request. YouTube is for lecture
videos; replacing one requires a new ID and an updated playlist entry.

Animations always have a dark canvas and are never theme-inverted. On the
website, tapping the video toggles play/pause and keeps it inline. There is no
central play badge or separate row of large buttons. A slim bottom seek bar and
small fullscreen icon appear on interaction, then fade after 650 ms. Keyboard
focus keeps these controls accessible; arrow keys seek and Home rewinds.
Fullscreen requires the explicit icon or F key and preserves playback state.
The standalone player fills the browser window and tries silent
playback except with reduced-motion preference. Safari may require a separate
tap to start playback or enter native full screen, and native browser chrome
cannot be removed by the course. Caption, explanation, alt text
and ordinary controls without JavaScript remain available.
When a native full-screen request is unavailable, open a dark full-window
viewport with the same small icon to exit. Do not add a central play overlay or
let the bottom controls linger over the animation.
Do not add a secondary player/download/YouTube link row below animations. PDF
and slide stills retain their player links; the website uses inline playback.

Default site builds copy posters and build the HTML players without rendering
or uploading MP4s through GitHub Actions. Render locally, run
`python3 scripts/refresh-animation-media.py`, build, inspect, and export with
`scripts/export-course-folder.sh`. Publish the small site/registry update after
checking the replacement. The export refreshes the Nextcloud files; public
GitHub Pages changes still require the repository's explicit publishing step.

Plots follow the website's light/dark preference. `scripts/prepare-media.py`
changes only SVG paint using a documented palette; geometry, tick positions,
line dashes, data and marker shapes stay unchanged. Light figures are reused in
the print PDF and white derivation/summary slides. Hero photos cover the whole
slide with small readable provenance at the bottom. Animation posters fill a
dark slide without cropping their 16:9 scene or adding a play badge; mathematical
pages stay white. Media-slide section cues live in the chapter plans.

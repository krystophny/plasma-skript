# Plasma physics lecture script

This project is a web-first graduate plasma physics lecture script written in
Typst. It follows the course sequence from plasma fundamentals through
single-particle motion, kinetic and fluid models, waves, sheaths, and
Langmuir probes. A supplemental mathematical toolkit collects the recurring
moment and coordinate-operator derivations.

Typst comes directly from `nixpkgs-unstable`. Run `nix flake update` when you
want to refresh the toolchain. Typst's HTML and bundle exporters are
experimental.

The website is the primary publication target. The optional PDF is built from
the paged fallback components when they are available. The author-only
`solutions/` directory and the copyrighted `resources/books/` and
`resources/content/` directories are ignored and are never included in the
public bundle.

## Development

Enter the reproducible environment with:

```sh
nix develop
```

Build the website locally (the app also emits the optional PDF) with:

```sh
nix run .#build-site
```

Verify the generated public bundle and the private-material boundary with:

```sh
nix run .#verify-spec -- public
nix run .#check-physics
nix flake check
```

The shell scripts remain the implementation used by the Nix package and CI;
development commands should go through the flake apps so their toolchains are
reproducible.

The flake check builds the site and runs the same source-structure and artifact
checks from a Nix source snapshot. It also tests numerical animation models
against independent conservation laws, differential equations, and quadrature
with `check-physics`. These checks complement visual inspection; a successful
build alone does not establish physically correct signs or curves.
New source files must be visible to the Git-backed flake (tracked or marked
intent-to-add) before running these commands. The checkout-level verifier additionally
checks the Git ignore rules for author-only material.

On Linux, the flake check also runs a NixOS VM browser integration test. To
keep its screenshots for visual review, build that check directly:

```sh
nix build .#checks.x86_64-linux.site-integration
find -L result/site-audit -maxdepth 1 -type f -print
```

The same browser audit can run against a locally hosted bundle with
`SITE_BASE_URL=http://127.0.0.1:8000 nix run .#check-site`. On macOS, also
set `CHROMIUM_EXECUTABLE_PATH` to the installed Chrome executable. Set
`SITE_AUDIT_ARTIFACT_DIR` to a dedicated temporary directory: the audit
replaces that directory's contents with its reports and screenshots.
For visual debugging, set `SITE_AUDIT_FIGURES=1` to capture every visible
figure at desktop width and decoded video frames at 25% and 75% of playback.
The frame audit downloads each served video completely before seeking; it
does not test HTTP byte-range support in the basic preview server.
Screenshots are evidence for human inspection, not a physics correctness test.

The test audits the complete site at mobile, tablet, and wide CSS viewports.
The NixOS VM check is Linux-only because the packaged Chromium browser is
Linux-only; macOS development can run it through a Linux builder or CI.

Serve the existing site from the project root:

```sh
nix run .#public-host -- 8000
```

`public-host` serves on all network interfaces without rebuilding. When local
sources are newer than the built `index.html`, it warns that the site may be
stale. This timestamp check is advisory; it does not detect deleted files or
changes that preserve older timestamps.

To rebuild explicitly before serving, add `--build`:

```sh
nix run .#public-host -- --build 8000
```

This rebuilds HTML, PDF, and animation media. If the build fails, the server
does not start and the previous complete site remains intact. `SITE_DIR`
selects both the build output and served directory; the default is `public/`.
A project-root build uses the working tree, including files not yet added to Git.

To serve an existing build on localhost without rebuilding, use
`nix run .#local-host -- 8000`. Neither app watches for changes. You can also
rebuild separately with `nix run .#build-site`.

The site build also compiles the live lecture decks `slides/<stem>.typ` (A4
landscape, for annotation during class) to `public/slides/<stem>.pdf` through
`scripts/build-slides.sh`. The decks take section numbers and titles from the
script and reuse its derived plots. `scripts/export-course-folder.sh <dest>`
copies the deck PDFs, animations, and derivations into a course folder.

The repository includes a GitHub Pages workflow that builds the same bundle
with Nix and deploys pushes to `main`. Enable GitHub Pages with GitHub Actions
as its publishing source in the repository settings.

## Licensing

Teaching content is released under [CC BY 4.0 International](LICENSE-CONTENT.md).
Code and build infrastructure are released under the [MIT License](LICENSE).
The photos in `slides/photos/` are public domain or CC BY 4.0, each credited
in [`slides/photos/credits.md`](slides/photos/credits.md). The STIX Two
fonts in `fonts/` are distributed under the SIL Open Font License 1.1
([`fonts/OFL.txt`](fonts/OFL.txt)).
Contribution and attribution terms are documented in
[`CONTRIBUTING.md`](CONTRIBUTING.md) and [`CONTRIBUTORS.md`](CONTRIBUTORS.md).

Refresh the offline Lilaq documentation snapshot with:

```sh
nix run .#build-lilaq-pdf
```

The main source is [`src/main.typ`](src/main.typ). Add chapters under
`src/chapters/`. The opening sequence is Introduction (examples, characteristic
scales, and model overview), Debye shielding, and Plasma oscillations.
Single-particle motion starts Chapter 4; waves occupy Chapters 11–14, and
sheaths and probes remain a separate Chapter 15. Add
supplemental material under `src/appendices/`, and animations
under `animations/`. Bibliographic entries live in
[`src/sources.bib`](src/sources.bib) and are cited with Typst's native `@key`
or `#cite(<key>)` syntax. The build script renders the animations first, then
exports the Typst bundle.

The first animation uses normalized, illustrative coordinates rather than
measured data:

```text
x / L₀ = -2.35 + 0.55 τ + 0.65 cos(2 τ)
y / L₀ = -0.65 - 0.65 sin(2 τ)
```

Here `L₀` is a reference length and `τ = t/t₀` is normalized time. The
gyroradius is `0.65 L₀`, the angular frequency is `2/t₀`, and the drift
speed is `0.55 L₀/t₀`. The clockwise orbit represents positive charge with
the magnetic field out of the page.

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

Build the website locally (the current script also emits the optional PDF) with:

```sh
./scripts/build-site.sh
```

Verify the generated public bundle and the private-material boundary with:

```sh
bash scripts/verify-spec.sh public
nix flake check
```

The flake check builds the site and runs the same artifact checks from a Nix
source snapshot. The checkout-level verifier additionally checks the Git ignore
rules for author-only material.

The generated site is in `public/`. Serve that directory with any static file
server so that the video and stylesheet are available alongside the HTML:

```sh
python -m http.server --directory public 8000
```

The repository includes a GitHub Pages workflow that builds the same bundle
with Nix and deploys pushes to `main`. Enable GitHub Pages with GitHub Actions
as its publishing source in the repository settings.

## Licensing

Teaching content is released under [CC BY 4.0 International](LICENSE-CONTENT.md).
Code and build infrastructure are released under the [MIT License](LICENSE).
Contribution and attribution terms are documented in
[`CONTRIBUTING.md`](CONTRIBUTING.md) and [`CONTRIBUTORS.md`](CONTRIBUTORS.md).

Refresh the offline Lilaq documentation snapshot with:

```sh
python3 scripts/build-lilaq-pdf.py
```

The main source is [`src/main.typ`](src/main.typ). Add chapters under
`src/chapters/`, supplemental material under `src/appendices/`, and animations
under `animations/`. The build script renders the animations first, then
exports the Typst bundle.

The first animation uses normalized, illustrative coordinates rather than
measured data:

```text
x / ρ = -2.5 + 0.55 t + 0.65 cos(2 t)
y / ρ = -0.8 + 0.65 sin(2 t)
```

Here `ρ` is the reference gyroradius and `t` is a dimensionless animation
parameter. The construction keeps the drift and the circular motion visible in
one frame.

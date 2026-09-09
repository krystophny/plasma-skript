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
nix flake check
```

The shell scripts remain the implementation used by the Nix package and CI;
development commands should go through the flake apps so their toolchains are
reproducible.

The flake check builds the site and runs the same source-structure and artifact
checks from a Nix source snapshot. The checkout-level verifier additionally
checks the Git ignore rules for author-only material.

On Linux, the flake check also runs a NixOS VM browser integration test. To
keep its screenshots for visual review, build that check directly:

```sh
nix build .#checks.x86_64-linux.site-integration
find -L result/site-audit -maxdepth 1 -type f -print
```

The test audits the complete site at mobile, tablet, and wide CSS viewports.
The NixOS VM check is Linux-only because the packaged Chromium browser is
Linux-only; macOS development can run it through a Linux builder or CI.

The generated site is in `public/`. Serve it with the flake app so that the
video and stylesheet are available alongside the HTML:

```sh
nix run .#public-host -- 8000
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
nix run .#build-lilaq-pdf
```

The main source is [`src/main.typ`](src/main.typ). Add chapters under
`src/chapters/`, supplemental material under `src/appendices/`, and animations
under `animations/`. Bibliographic entries live in
[`src/sources.bib`](src/sources.bib) and are cited with Typst's native `@key`
or `#cite(<key>)` syntax. The build script renders the animations first, then
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

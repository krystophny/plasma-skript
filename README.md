# Plasma physics lecture script

Every reading page has a **Report a problem** link. It opens a GitHub issue
draft with the chapter, current section and public reading URL already filled
in. Selected text can identify a passage. Readers sign in to GitHub, describe
the problem and submit the issue; the script holds no posting credentials.

This project is a web-first graduate plasma physics lecture script written in
Typst. It follows the course sequence from plasma fundamentals through
single-particle motion, kinetic and fluid models, waves, sheaths, and
Langmuir probes. A supplemental mathematical toolkit collects the recurring
moment and coordinate-operator derivations.

The script preserves the full reference, including guiding-center motion and
linear/kinetic response. Live lectures select material at an appropriate pace;
they do not need to cover every chapter. Authoring uses lecturer explanations
and original derivations checked against cited references and multi-year
teaching evidence. Textbooks and legacy recordings are private inputs, not
prose/figure assets for the public edition.

The mixed FuEL video course remains restricted while legacy recordings are
replaced weekly by reviewed new clips. FuEL can link the maintained script;
a dated build may also be deposited after a platform HTML pilot. Video upload,
outcome coverage and CC clearance are separate checks. `SPEC.md` owns this
repository's contract; [shared teaching rules](../../Nextcloud/lv/AGENTS.md), "FuEL delivery", in the teaching tree
owns the shared course policy.

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
figure at desktop width and decoded local video frames at 25% and 75% of playback.
External players are checked for accessible captions, titles and links; their
playback is verified separately on the actual host.
The frame audit downloads each locally served video completely before seeking.
The preview server supports HTTP byte ranges for ordinary native-player seeking;
the playback audit checks the inline seek controls separately.
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

This rebuilds HTML, PDF, slides and animation posters. External hosting is the
default; use `ANIMATION_HOSTING=local` when rendering local animation videos. If the build fails, the server
does not start and the previous complete site remains intact. `SITE_DIR`
selects both the build output and served directory; the default is `public/`.
A project-root build uses the working tree, including files not yet added to Git.

To serve an existing build on localhost without rebuilding, use
`nix run .#local-host -- 8000`. Neither app watches for changes. You can also
rebuild separately with `nix run .#build-site`.

The site build also compiles the live lecture decks `slides/<stem>.typ` (A4
landscape) to `public/slides/<stem>.pdf` through
`scripts/build-slides.sh`. The decks take section numbers and titles from the
script and reuse its derived plots. `scripts/export-course-folder.sh <dest>`
copies the deck PDFs, Skript PDF, animations, and derivations into a course folder.

The repository includes a GitHub Pages workflow that builds the same bundle
with Typst and uv and deploys pushes to `main`; Nix checks run separately.
Enable GitHub Pages with GitHub Actions
as its publishing source in the repository settings.

## HTML presentation mode

Open [Lecture decks](https://krystophny.github.io/plasma-skript/present/) on
the iPad or a desktop. Each deck lives at `present/<stem>/`, alongside its
downloadable `slides/<stem>.pdf`. LOOK uses the complete deck; THINK uses a
separate Goodnotes notebook. There are no blank writing pages in the deck.
The presenter supports touch navigation, keyboard navigation, inline video,
overview and a Pencil laser. Its existing layout is shared by all chapters.

`scripts/build-present.py` compiles SVG pages from the same `slides/*.typ`
sources as the PDFs. It checks one `<present-page>` entry per physical page
and agreement with the PDF count, then writes `decks.json` and each deck's
`manifest.json`. The manifest includes chapter/title, PDF link, aspect ratio,
page alternatives, backgrounds, animation loop flags, and hashed SVG, poster
and video URLs. Videos are copied to `present/media/` and must match the
checksums in `media/animations.json`; CI downloads these exact streams when
local renders are unavailable. Missing media abort the staged site build.

Opening a deck online saves its complete content and shared UI assets with a
service worker. Wait for the offline save to finish (the O key reports its
status) before disconnecting. Reload and inline animation playback then work
offline. Manifests and UI files refresh online; SVG/PNG/MP4 content is cached
by its mandatory `?v=<sha8>` URL. Cached MP4s support byte-range requests.
Browser storage can be evicted, so reopen online before relying on an old copy.

Run `uv run python scripts/present-test.py public` to serve and test the real
bundle, or supply a live `https://.../present/` URL. The test uses
`/usr/bin/google-chrome-stable` for H.264 and `pdfinfo` for independent page
counts; touch, keys, every animation, offline reload and console errors are
checked. `CHROMIUM_EXECUTABLE_PATH` selects another codec-capable browser.
`verify-spec` also checks manifests, hashes and same-origin media without a browser.

After committing, `scripts/publish.sh` builds, checks, exports to
`~/Nextcloud/lv/plasma/2026`, and pushes `main` to `origin` and `github`.
It never creates a commit. The export maintains `slides/`, `skript/`,
`animations/`, `animation-sources/`, and `derivations/`; the Skript PDF is
`skript/plasma-physics.pdf`. Install the opt-in export hook with
`install -m755 scripts/hooks/pre-push .git/hooks/pre-push`. Direct main pushes
then export a current built bundle and reject stale source fingerprints.

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
scales, and model overview), Temperature, entropy, and thermal ionization,
Debye shielding, and Plasma oscillations.
Single-particle motion starts Chapter 5; waves occupy Chapters 12–15, and
sheaths and probes remain a separate Chapter 16. Add
supplemental material under `src/appendices/`, and animations
under `animations/`. Bibliographic entries live in
[`src/sources.bib`](src/sources.bib) and are cited with Typst's native `@key`
or `#cite(<key>)` syntax. In local hosting mode the build script renders animations first, then
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

## Related workspaces

Work locally in `~/proj/plasma-skript`. The faepmac1 checkout is a secondary
copy; synchronize through Git rather than editing both copies independently.

- [Source reconciliation and release evidence](SOURCE-RECONCILIATION.md)
- [Fusion Skript](../fusion-skript/README.md)
- [Video archive and watch/cut workflow](../fusion-course-archive/README.md)
- [Plasma teaching plan and exam policy](../../Nextcloud/lv/plasma/PLAN.md)
- [FuEL project memory](../../Nextcloud/brain/projects/EUROfusion-FuEL-online-course-production.md)

## Platform delivery

Use the shared [course delivery policy](../../Nextcloud/lv/AGENTS.md): curated
module routes in FuEL and TeachCenter and YouTube unlisted lecture videos.
Animations use native players at stable `animations/<slug>.html` URLs, with
versioned MP4 streams from Nextcloud. The
website, print PDF and slides consume `media/animations.json`.
Only TeachCenter additionally links the full 2026 Nextcloud material folder.
Course-description backups are in each course's `platform-backups/` folder.
Written examinations supersede the earlier instruction to preserve the old
format; current questions remain the baseline and may evolve until semester end.

All seventeen animations have dark renders. To replace a scene, render locally
(the source/style stamps skip unchanged scenes), run
`python3 scripts/refresh-animation-media.py`, build and inspect, then export
to the public Nextcloud course folder. Publish the site update so the stable
player URL selects the current checksum-versioned stream. Short-animation
YouTube uploads are removed at Chris's request; YouTube hosts lecture videos.
There is no secondary player/download/YouTube link row below animations.
Website animations stay inline: click/tap toggles play/pause. There is no central
play overlay or row of large buttons. A slim bottom seek bar and small fullscreen
icon fade after 650 ms, remaining accessible on keyboard focus. Fullscreen is
explicit and preserves playback state; the standalone page fills the browser
window. Website plots select light/dark SVG paint without changing their data;
slides and print retain light plots. Photos fill the slide with small credits.
`scripts/animation-player-test.py` checks actual rendered MP4 playback, controls,
theme switching and no-JavaScript fallback in Chromium or WebKit. The Nix VM
layout audit uses a local transport fixture so it does not depend on external
DNS; this does not verify the public video host or replace the model/render checks.
The maintained public edition is
[the Plasma Skript](https://krystophny.github.io/plasma-skript/). Pushes to
`main` deploy it through GitHub Pages after the site and derivation checks pass.
FuEL's dated HTML snapshot is hidden File resource 747; update that snapshot
after a verified public deployment so the two editions agree.

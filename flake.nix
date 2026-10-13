{
  description = "Plasma physics lecture notes in Typst with Manim visualizations";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = {
    self,
    flake-utils,
    nixpkgs,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};
      newComputerModern = pkgs.newcomputermodern;
      fontConfig = pkgs.makeFontsConf {
        fontDirectories = [newComputerModern];
      };
      # Typst main: 0.15.1 writes bare "&" in SVG link URLs (typst#8672, fixed by
      # typst#8510 after the release). Return to pkgs.typst once a release has it.
      typstRev = "d7dfb34ae79689ed78857ab38a3f6a24a1747770";
      typstMain = pkgs.typst.overrideAttrs (old: rec {
        version = "0.15.1-main-${builtins.substring 0 8 typstRev}";
        src = pkgs.fetchFromGitHub {
          owner = "typst";
          repo = "typst";
          rev = typstRev;
          hash = "sha256-yFCLs4rpw+A0Cec2PaIKKA+yRBrjeOgEhpYmYqmbGic=";
        };
        cargoDeps = pkgs.rustPlatform.fetchCargoVendor {
          inherit src;
          name = "typst-${version}";
          hash = "sha256-Rdc6t7apGgcvSQe3EkkYEhzHYvBiSBTIyHJ0oi2Edzc=";
        };
        postPatch = ''
          export TYPST_COMMIT_SHA="${builtins.substring 0 8 typstRev}"
        '';
        doCheck = false;
        doInstallCheck = false;
        meta = old.meta // {changelog = "https://github.com/typst/typst/commit/${typstRev}";};
      });
      typstWrapper = pkgs.callPackage "${nixpkgs}/pkgs/by-name/ty/typst/wrapper.nix" {typst = typstMain;};
      typst = typstWrapper {packages = ps: [
        ps.physica_0_9_8
        ps.cetz_0_5_2
        ps.fletcher_0_5_8
        ps.lilaq_0_6_0
        ps.frame-it_2_0_0
        ps.unify_0_8_1
      ];};
      playwrightCore = pkgs.playwright-driver;
      # Manim with its own TeX: the MathTex template in animations/style.py
      # loads STIX Two (the Type 1 stix2 package) through latex and dvisvgm.
      # nixpkgs' manim wrapper puts a TeX without STIX Two first on
      # PATH, so the scenes run through `python -m manim` with this TeX instead.
      manimTex = pkgs.texliveBasic.withPackages (ps: [
        ps.amsmath
        ps.babel-english
        ps.dvisvgm
        ps.etoolbox
        ps.iftex
        ps.xkeyval
        ps.stix2-type1
        ps.preview
        ps.standalone
      ]);
      manimPython = pkgs.python3.withPackages (ps: [ps.manim]);
      manim = pkgs.writeShellApplication {
        name = "manim";
        runtimeInputs = [manimTex pkgs.ffmpeg];
        text = ''exec ${manimPython}/bin/python -m manim "$@"'';
      };
      physicsPython = pkgs.python3.withPackages (ps: [ps.numpy]);
      # SymPy derivations write the data plots that the Typst sources include.
      derivationsPython = pkgs.python3.withPackages (ps: [ps.numpy ps.sympy ps.matplotlib ps.pytest]);
      # Fixed-output downloads make presenter media available in the sandbox.
      # Select precisely the animations used by the current single-source decks.
      animationRegistry = (builtins.fromJSON (builtins.readFile ./media/animations.json)).animations;
      deckSources = pkgs.lib.filterAttrs (name: kind:
        kind == "regular" && builtins.match "[0-9].*\\.typ" name != null)
        (builtins.readDir ./slides);
      presentSlugs = pkgs.lib.unique (pkgs.lib.concatMap (name:
        pkgs.lib.concatMap (line: let
          match = builtins.match ''.*animation-page\("([^"]+)".*'' line;
        in pkgs.lib.optional (match != null) (builtins.head match))
        (pkgs.lib.splitString "\n" (builtins.readFile (./slides + "/${name}"))))
        (builtins.attrNames deckSources));
      presentMedia = pkgs.linkFarm "plasma-present-media" (map (slug: {
        name = "${slug}.mp4";
        path = pkgs.fetchurl {
          url = animationRegistry.${slug}.stream_url;
          sha256 = animationRegistry.${slug}.mp4_sha256;
        };
      }) presentSlugs);
      physicsCheckApp = pkgs.writeShellApplication {
        name = "plasma-check-physics";
        runtimeInputs = [physicsPython typst];
        text = ''
          python ${self}/scripts/check-physics.py "$@"
          typst query --root ${self} ${self}/scripts/check-figures.typ '<physics-check>'
        '';
      };
      siteIntegrationRunner = pkgs.writeShellApplication {
        name = "plasma-site-integration-test";
        runtimeInputs = [pkgs.nodejs];
        text = ''
          export PLAYWRIGHT_CORE_PATH="${playwrightCore}"
          ${pkgs.lib.optionalString pkgs.stdenv.hostPlatform.isLinux ''
            export CHROMIUM_EXECUTABLE_PATH="''${CHROMIUM_EXECUTABLE_PATH:-${pkgs.chromium}/bin/chromium}"
          ''}
          exec node ${self}/scripts/site-integration-test.cjs "$@"
        '';
      };
      buildSiteApp = pkgs.writeShellApplication {
        name = "plasma-build-site";
        runtimeInputs = [pkgs.bash pkgs.ffmpeg pkgs.gnumake manim derivationsPython typst];
        text = ''
          export FONTCONFIG_FILE="${fontConfig}"
          site_dir="''${SITE_DIR:-$PWD/public}"
          export SITE_DIR="$site_dir"
          export PRESENT_MEDIA_DIR="${presentMedia}"
          # Build the working tree when invoked from the project root, including
          # new chapter files that have not been added to Git yet.
          if [[ -f "$PWD/flake.nix" && -f "$PWD/src/main.typ" && -f "$PWD/scripts/build-site.sh" ]]; then
            exec bash "$PWD/scripts/build-site.sh" "$@"
          fi
          exec bash "${self}/scripts/build-site.sh" "$@"
        '';
      };
      verifySpecApp = pkgs.writeShellApplication {
        name = "plasma-verify-spec";
        runtimeInputs = [pkgs.bash pkgs.coreutils pkgs.findutils pkgs.perl pkgs.ripgrep pkgs.python3];
        text = ''
          site_dir="''${1:-''${SITE_DIR:-$PWD/public}}"
          exec bash "${self}/scripts/verify-spec.sh" "$site_dir"
        '';
      };
      lilaqDocumentationApp = pkgs.writeShellApplication {
        name = "plasma-build-lilaq-pdf";
        runtimeInputs = [pkgs.python3] ++ pkgs.lib.optional pkgs.stdenv.hostPlatform.isLinux pkgs.chromium;
        text = ''
          exec python3 "${self}/scripts/build-lilaq-pdf.py" "$@"
        '';
      };
      mkHostApp = {
        name,
        bind,
        offerBuild ? false,
      }: let
        hostScript = pkgs.writeShellApplication {
          inherit name;
          runtimeInputs = [pkgs.python3] ++ pkgs.lib.optional offerBuild pkgs.findutils;
          text = ''
            site_dir="''${SITE_DIR:-public}"
            ${pkgs.lib.optionalString offerBuild ''
              build_requested=false
              host_args=()
              for arg in "$@"; do
                if [[ "$arg" == "--build" ]]; then
                  build_requested=true
                else
                  host_args+=("$arg")
                fi
              done
              set -- "''${host_args[@]}"
              if [[ "$build_requested" == true ]]; then
                echo "Building website before serving..."
                SITE_DIR="$site_dir" ${buildSiteApp}/bin/plasma-build-site
              elif [[ -f "$site_dir/index.html" && -d "$PWD/src" && -d "$PWD/animations" && -f "$PWD/scripts/build-site.sh" ]]; then
                newer_source="$(find "$PWD/src" "$PWD/animations" "$PWD/scripts/build-site.sh" "$PWD/scripts/render-animations.sh" "$PWD/flake.nix" "$PWD/flake.lock" \
                  -type f ! -path '*/__pycache__/*' -newer "$site_dir/index.html" -print -quit)"
                if [[ -n "$newer_source" ]]; then
                  echo "Warning: the site may be stale; source files are newer than index.html." >&2
                  echo "To rebuild explicitly, run: nix run .#public-host -- --build (plus your port/options)." >&2
                fi
              fi
            ''}
            if [[ ! -d "$site_dir" ]]; then
              echo "Site directory '$site_dir' does not exist; build the site first." >&2
              ${pkgs.lib.optionalString offerBuild ''
              echo "Run: nix run .#public-host -- --build" >&2
            ''}
              exit 1
            fi

            if (( $# == 0 )); then
              set -- "''${PORT:-4444}"
            fi

            exec python3 ${./scripts/serve-site.py} \
              --bind ${bind} \
              --directory "$site_dir" \
              "$@"
          '';
        };
      in {
        type = "app";
        meta.description =
          if offerBuild
          then "Serve the site on ${bind}; use --build to rebuild first"
          else "Serve the generated site on ${bind}";
        program = "${hostScript}/bin/${name}";
      };
    in {
      formatter = pkgs.alejandra;

      apps = {
        check-site = {
          type = "app";
          meta.description = "Audit a served site at mobile, tablet and wide viewports";
          program = "${siteIntegrationRunner}/bin/plasma-site-integration-test";
        };
        check-physics = {
          type = "app";
          meta.description = "Check animation models against independent physics oracles";
          program = "${physicsCheckApp}/bin/plasma-check-physics";
        };
        build-site = {
          type = "app";
          meta.description = "Build the public Typst website and media";
          program = "${buildSiteApp}/bin/plasma-build-site";
        };

        verify-spec = {
          type = "app";
          meta.description = "Verify a generated public site against SPEC.md";
          program = "${verifySpecApp}/bin/plasma-verify-spec";
        };

        build-lilaq-pdf = {
          type = "app";
          meta.description = "Refresh the ignored offline Lilaq documentation snapshot";
          program = "${lilaqDocumentationApp}/bin/plasma-build-lilaq-pdf";
        };

        local-host = mkHostApp {
          name = "local-host";
          bind = "localhost";
        };

        public-host = mkHostApp {
          name = "public-host";
          bind = "0.0.0.0";
          offerBuild = true;
        };
      };

      packages.default = pkgs.stdenvNoCC.mkDerivation {
        pname = "plasma-physics-script";
        version = "0.1.0";
        src = ./.;

        nativeBuildInputs = [
          derivationsPython
          pkgs.ffmpeg
          pkgs.gnumake
          manim
          newComputerModern
          typst
        ];
        FONTCONFIG_FILE = fontConfig;
        PRESENT_MEDIA_DIR = presentMedia;

        buildPhase = ''
          runHook preBuild
          bash scripts/build-site.sh
          runHook postBuild
        '';

        installPhase = ''
          runHook preInstall
          mkdir -p "$out"
          cp -R public/. "$out/"
          runHook postInstall
        '';
      };

      checks =
        {
          physics =
            pkgs.runCommand "plasma-physics-check" {
              nativeBuildInputs = [physicsPython typst];
            } ''
              python ${self}/scripts/check-physics.py
              typst query --root ${self} ${self}/scripts/check-figures.typ '<physics-check>'
              touch "$out"
            '';
          site = self.packages.${system}.default;

          preview-transport = pkgs.runCommand "plasma-preview-transport-check" {
            nativeBuildInputs = [pkgs.python3];
          } ''
            python ${self}/scripts/preview-server-test.py
            touch "$out"
          '';

          spec =
            pkgs.runCommand "plasma-spec-check" {
              nativeBuildInputs = [
                pkgs.bash
                pkgs.coreutils
                pkgs.findutils
                pkgs.perl
                pkgs.ripgrep
                pkgs.python3
              ];
            } ''
              bash ${self}/scripts/verify-spec.sh ${self.packages.${system}.default}
              touch "$out"
            '';
        };

      devShells.default = pkgs.mkShell {
        FONTCONFIG_FILE = fontConfig;
        packages = [
          typst
          manim
          derivationsPython
          pkgs.gnumake
          newComputerModern
          pkgs.ffmpeg
          pkgs.alejandra
          pkgs.bash
          pkgs.findutils
          pkgs.git
          pkgs.perl
          pkgs.ripgrep
          pkgs.statix
        ];

        shellHook = ''
          echo "Plasma physics script development shell"
          echo "Typst: $(typst --version)"
          echo "Manim: $(manim --version 2>/dev/null | head -n 1)"
        '';
      };
    });
}

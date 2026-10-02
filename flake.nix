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
      newComputerModernFont = "${newComputerModern}/share/fonts/opentype/public/NewCM10-Regular.otf";
      fontConfig = pkgs.makeFontsConf {
        fontDirectories = [newComputerModern];
      };
      typst = pkgs.typst.withPackages (ps: [
        ps.physica_0_9_8
        ps.cetz_0_5_2
        ps.fletcher_0_5_8
        ps.lilaq_0_6_0
        ps.frame-it_2_0_0
        ps.unify_0_8_1
      ]);
      playwrightCore = pkgs.playwright-driver;
      physicsPython = pkgs.python3.withPackages (ps: [ps.numpy]);
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
        runtimeInputs = [pkgs.bash pkgs.ffmpeg pkgs.manim typst];
        text = ''
          export FONTCONFIG_FILE="${fontConfig}"
          export PLASMA_NEW_COMPUTER_MODERN_FONT="${newComputerModernFont}"
          site_dir="''${SITE_DIR:-$PWD/public}"
          export SITE_DIR="$site_dir"
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
        runtimeInputs = [pkgs.bash pkgs.coreutils pkgs.findutils pkgs.perl pkgs.ripgrep];
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

            exec python3 -m http.server \
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
      nixosIntegrationTest = pkgs.testers.nixosTest {
        name = "plasma-site-integration";

        nodes.machine = {pkgs, ...}: {
          services.nginx = {
            enable = true;
            virtualHosts."localhost".root = self.packages.${system}.default;
          };

          environment.etc."plasma-site-integration-test.cjs".source =
            ./scripts/site-integration-test.cjs;

          environment.systemPackages = [
            pkgs.chromium
            pkgs.nodejs
            playwrightCore
            siteIntegrationRunner
          ];

          environment.variables = {
            CHROMIUM_EXECUTABLE_PATH = "${pkgs.chromium}/bin/chromium";
            PLAYWRIGHT_CORE_PATH = "${playwrightCore}";
            SITE_AUDIT_ARTIFACT_DIR = "/tmp/plasma-site-audit";
            SITE_BASE_URL = "http://127.0.0.1";
          };
        };

        testScript = ''
          start_all()
          machine.wait_for_unit("nginx.service")
          machine.wait_for_open_port(80)
          machine.succeed("mkdir -p /tmp/plasma-site-audit")
          try:
              machine.succeed("plasma-site-integration-test")
          finally:
              machine.copy_from_machine("/tmp/plasma-site-audit", "site-audit")
        '';
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
          pkgs.ffmpeg
          pkgs.manim
          newComputerModern
          typst
        ];
        FONTCONFIG_FILE = fontConfig;
        PLASMA_NEW_COMPUTER_MODERN_FONT = newComputerModernFont;

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

          spec =
            pkgs.runCommand "plasma-spec-check" {
              nativeBuildInputs = [
                pkgs.bash
                pkgs.coreutils
                pkgs.findutils
                pkgs.perl
                pkgs.ripgrep
              ];
            } ''
              bash ${self}/scripts/verify-spec.sh ${self.packages.${system}.default}
              touch "$out"
            '';
        }
        // pkgs.lib.optionalAttrs pkgs.stdenv.hostPlatform.isLinux {
          site-integration = nixosIntegrationTest;
        };

      devShells.default = pkgs.mkShell {
        FONTCONFIG_FILE = fontConfig;
        PLASMA_NEW_COMPUTER_MODERN_FONT = newComputerModernFont;
        packages = [
          typst
          pkgs.manim
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

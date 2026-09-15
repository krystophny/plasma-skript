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
      siteIntegrationRunner = pkgs.writeShellApplication {
        name = "plasma-site-integration-test";
        runtimeInputs = [pkgs.nodejs];
        text = ''
          exec node /etc/plasma-site-integration-test.cjs "$@"
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
      }: let
        hostScript = pkgs.writeShellApplication {
          inherit name;
          runtimeInputs = [pkgs.python3];
          text = ''
            site_dir="''${SITE_DIR:-public}"
            if [[ ! -d "$site_dir" ]]; then
              echo "Site directory '$site_dir' does not exist; build the site first." >&2
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
        meta.description = "Serve the generated site on ${bind}";
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

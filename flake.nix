{
  description = "Plasma physics lecture notes in Typst with Manim visualizations";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, flake-utils, nixpkgs, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        typst = pkgs.typst.withPackages (ps: [
          ps.physica_0_9_8
          ps.cetz_0_5_2
          ps.fletcher_0_5_8
          ps.lilaq_0_6_0
          ps.frame-it_2_0_0
          ps.unify_0_8_1
        ]);
        mkHostApp = { name, bind }:
          let
            hostScript = pkgs.writeShellApplication {
              inherit name;
              runtimeInputs = [ pkgs.python3 ];
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
          in
          {
            type = "app";
            meta.description = "Serve the generated site on ${bind}";
            program = "${hostScript}/bin/${name}";
          };
      in
      {
        formatter = pkgs.alejandra;

        apps = {
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
            typst
          ];

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

        checks = {
          site = self.packages.${system}.default;

          spec = pkgs.runCommand "plasma-spec-check" {
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
        };

        devShells.default = pkgs.mkShell {
          packages = [
            typst
            pkgs.manim
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

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
      in
      {
        formatter = pkgs.alejandra;

        packages.default = pkgs.stdenvNoCC.mkDerivation {
          pname = "plasma-physics-script";
          version = "0.1.0";
          src = ./.;

          nativeBuildInputs = [
            pkgs.ffmpeg
            pkgs.manim
            pkgs.typst
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
            pkgs.typst
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

{
  description = "Application packaged using poetry2nix";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable-small";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
      pkgs = nixpkgs.legacyPackages.${system};
      inherit (poetry2nix.lib.mkPoetry2Nix {inherit pkgs;}) mkPoetryApplication;
    in {
      packages = {
        laphaelaicmd_linux = with pkgs; mkPoetryApplication {
          projectDir = self;
          meta = {
            description = "Enable chat AI to execute commands on linux with feedback-loop for multi-step missions";
            longDescription = ''
              Enable chat AI to execute commands on linux with feedback-loop for multi-step missions
            '';
            homepage = "https://www.gnu.org/software/hello/manual/";
            license = lib.licenses.agpl3Only;
            platforms = lib.platforms.all;
          };
        };
        default = self.packages.${system}.laphaelaicmd_linux;
      };

      # Shell for app dependencies.
      #
      #     nix develop
      #
      # Use this shell for developing your app.
      devShells.default = pkgs.mkShell {
        inputsFrom = [self.packages.${system}.laphaelaicmd_linux];
      };

      # Shell for poetry.
      #
      #     nix develop .#poetry
      #
      # Use this shell for changes to pyproject.toml and poetry.lock.
      devShells.poetry = pkgs.mkShell {
        packages = [pkgs.poetry];
      };
    });
}

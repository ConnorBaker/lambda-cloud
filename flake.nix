{
  inputs = {
    flake-parts = {
      inputs.nixpkgs-lib.follows = "nixpkgs";
      url = "github:hercules-ci/flake-parts";
    };
    nixpkgs.url = "github:NixOS/nixpkgs";
    poetry2nix = {
      inputs.nixpkgs.follows = "nixpkgs";
      url = "github:nix-community/poetry2nix";
    };
  };

  nixConfig = {
    # Add my own cache and the CUDA maintainer's cache
    allow-import-from-derivation = true;
    extra-substituters = [
      "https://cantcache.me"
      "https://cuda-maintainers.cachix.org"
    ];
    extra-trusted-substituters = [
      "https://cantcache.me"
      "https://cuda-maintainers.cachix.org"
    ];
    extra-trusted-public-keys = [
      "cantcache.me:Y+FHAKfx7S0pBkBMKpNMQtGKpILAfhmqUSnr5oNwNMs="
      "cuda-maintainers.cachix.org-1:0dq3bujKpuEPMCX6U4WylrUDZ9JyUG0VpVZa7CNfq5E="
    ];
  };

  outputs = inputs:
    inputs.flake-parts.lib.mkFlake {inherit inputs;} {
      systems = ["x86_64-linux"];
      imports = [./nix];
    };
}

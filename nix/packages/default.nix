{
  perSystem = {
    inputs',
    pkgs,
    ...
  }: {
    packages = {
      lambda-cloud = pkgs.python3Packages.callPackage ./lambda-cloud.nix {};
      datamodel-code-generator = pkgs.python3Packages.callPackage ./datamodel-code-generator.nix {
        poetry2nix = inputs'.poetry2nix.legacyPackages;
      };
    };
  };
}

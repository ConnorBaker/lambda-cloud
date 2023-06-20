{
  perSystem = {inputs', pkgs, ...}: {
    packages = {
      lambda-cloud = pkgs.python3Packages.callPackage ./lambda-cloud.nix {};
      datamodel-code-generator = pkgs.callPackage ./datamodel-code-generator {};
    };
  };
}

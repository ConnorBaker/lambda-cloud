{
  fetchFromGitHub,
  fetchpatch,
  lib,
  poetry2nix,
  stdenvNoCC,
  # propagatedBuildInputs
}:
# To bypass the error "unsupported build system requirement poetry_core",
# apply the patches in a separate derivation and use the result as the
# projectDir. There's a bug in poetry2nix that doesn't allow normalization
# of the names of the build requirements.
let
  src = stdenvNoCC.mkDerivation {
    name = "datamodel-code-generator-src";
    src = fetchFromGitHub {
      owner = "koxudaxi";
      rev = "0.20.0";
      repo = "datamodel-code-generator";
      sha256 = "sha256-vPx4pqgPNN/UMy7Y6Vuo89XezOuAoPVsNj0qI1Yrb0c=";
    };
    phases = ["unpackPhase" "patchPhase" "installPhase"];
    patches = [
      (fetchpatch {
        url = "https://github.com/koxudaxi/datamodel-code-generator/pull/1374.patch";
        sha256 = "sha256-KpAhxkCqBGNFbRvIQWQM+VDlzzi9oqEXY/gOxBzIeaQ=";
      })
    ];
    installPhase = ''
      cp -r . $out
    '';
  };
in
  poetry2nix.mkPoetryApplication {
    projectDir = src;
    doCheck = false;
    overrides = poetry2nix.defaultPoetryOverrides.extend (_: prev: {
      genson = prev.genson.overridePythonAttrs (oldAttrs: {
        buildInputs = (oldAttrs.buildInputs or []) ++ [prev.setuptools];
      });
      pydantic = prev.pydantic.overridePythonAttrs (oldAttrs: {
        propagatedBuildInputs = (oldAttrs.propagatedBuildInputs or []) ++ [prev.email-validator];
      });
      types-jinja2 = prev.types-jinja2.overridePythonAttrs (oldAttrs: {
        buildInputs = (oldAttrs.buildInputs or []) ++ [prev.setuptools];
      });
      types-markupsafe = prev.types-markupsafe.overridePythonAttrs (oldAttrs: {
        buildInputs = (oldAttrs.buildInputs or []) ++ [prev.setuptools];
      });
    });
    meta = with lib; {
      description = "Pydantic model and dataclasses.dataclass generator for easy conversion of JSON, OpenAPI, JSON Schema, and YAML data sources.";
      homepage = "https://github.com/koxudaxi/datamodel-code-generator";
      license = licenses.mit;
      mainProgram = "datamodel-codegen";
      maintainers = with maintainers; [connorbaker];
      platforms = platforms.linux;
    };
  }

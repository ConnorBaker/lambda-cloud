{
  lib,
  fetchFromGitHub,
  poetry2nix,
  # stdenvNoCC,
  # propagatedBuildInputs
}:
# To bypass the error "unsupported build system requirement poetry_core",
# apply the patches in a separate derivation and use the result as the
# projectDir.
# let
#   src = stdenvNoCC.mkDerivation {
#     name = "datamodel-code-generator-src";
#     src = fetchFromGitHub {
#       owner = "koxudaxi";
#       rev = "0.20.0";
#       repo = "datamodel-code-generator";
#       sha256 = "sha256-vPx4pqgPNN/UMy7Y6Vuo89XezOuAoPVsNj0qI1Yrb0c=";
#     };
#     phases = ["unpackPhase" "patchPhase" "installPhase"];
#     patches = [
#       ./remove-poetry-dynamic-versioning.patch
#     ];
#     installPhase = ''
#       cp -r . $out
#     '';
#   };
# in
  poetry2nix.mkPoetryApplication {
    projectDir = fetchFromGitHub {
      owner = "koxudaxi";
      rev = "0.20.0";
      repo = "datamodel-code-generator";
      sha256 = "sha256-vPx4pqgPNN/UMy7Y6Vuo89XezOuAoPVsNj0qI1Yrb0c=";
    };
    patches = [
      ./remove-poetry-dynamic-versioning.patch
    ];
    overrides = poetry2nix.defaultPoetryOverrides.extend (_: prev: {
      genson = prev.genson.overridePythonAttrs (oldAttrs: {
        buildInputs = (oldAttrs.buildInputs or []) ++ [prev.setuptools];
      });
      urllib3 = prev.urllib3.overridePythonAttrs (oldAttrs: {
        buildInputs = (oldAttrs.buildInputs or []) ++ [prev.hatchling];
      });
      types-markupsafe = prev.types-markupsafe.overridePythonAttrs (oldAttrs: {
        buildInputs = (oldAttrs.buildInputs or []) ++ [prev.setuptools];
      });
      types-jinja2 = prev.types-jinja2.overridePythonAttrs (oldAttrs: {
        buildInputs = (oldAttrs.buildInputs or []) ++ [prev.setuptools];
      });
      # Can't successfully override maturin as a rust dependency.
      ruff = prev.ruff.override {
        preferWheel = true;
      };
    });
    meta = with lib; {
      description = "Pydantic model and dataclasses.dataclass generator for easy conversion of JSON, OpenAPI, JSON Schema, and YAML data sources.";
      homepage = "https://github.com/koxudaxi/datamodel-code-generator";
      license = licenses.mit;
      platforms = platforms.linux;
      maintainers = with maintainers; [connorbaker];
    };
  }

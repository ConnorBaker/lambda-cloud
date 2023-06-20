{
  buildPythonPackage,
  lib,
  # propagatedBuildInputs
  click,
  pydantic,
  requests,
}: let
  attrs = {
    pname = "lambda-cloud";
    version = "0.1.0";
    format = "flit";
    src = lib.sources.sourceByRegex ../.. [
      "lambda_cloud(:?/.*)?"
      "pyproject.toml"
      "README.md"
    ];
    propagatedBuildInputs = [
      click
      pydantic
      requests
    ];
    pythonImportsCheck = [
      "click"
      "lambda_cloud"
      "pydantic"
      "requests"
    ];
    meta = with lib; {
      description = "Interact with the Lambda Cloud API";
      homepage = "";
      license = licenses.bsd3;
      platforms = platforms.linux;
      maintainers = with maintainers; [connorbaker];
    };
  };
in
  buildPythonPackage attrs

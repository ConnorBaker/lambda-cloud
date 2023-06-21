# lambda_cloud

## Regenerating the OpenAPI definition

```bash
$ curl -L https://cloud.lambdalabs.com/static/api/v1/openapi.yaml -o lambda_cloud/openapi.yaml
$ nix run .#datamodel-code-generator -- \
    --collapse-root-models \
    --enum-field-as-literal all \
    --input lambda_cloud/openapi.yaml \
    --input-file-type openapi \
    --openapi-scopes schemas paths tags parameters \
    --output lambda_cloud/openapi.py \
    --output-model-type pydantic.BaseModel \
    --reuse-model \
    --strict-nullable \
    --target-python-version 3.10 \
    --use-annotated \
    --use-double-quotes \
    --use-field-description \
    --use-schema-description \
    --use-standard-collections \
    --use-union-operator \
    --validation
```

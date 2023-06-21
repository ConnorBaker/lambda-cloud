import json
import sys
import click
from lambda_cloud import openapi, paths
from lambda_cloud.cli import ClickApiKeyWrapper, ClickInstanceTypeNameWrapper


def api_get_instance_regions(api_key: str, instance_type_name: str) -> list[openapi.Region]:
    instance_types: openapi.InstanceTypesGetResponse = paths.instance_types(api_key)
    instance_type: openapi.Data = instance_types.data[instance_type_name]
    regions = instance_type.regions_with_capacity_available
    regions.sort(key=lambda region: region.name)
    return regions


@click.command()
@ClickApiKeyWrapper
@ClickInstanceTypeNameWrapper
def get_instance_regions(
    api_key: str,
    instance_type_name: str,
) -> None:
    """Get regions where instance type is available."""
    regions: list[openapi.Region] = api_get_instance_regions(api_key, instance_type_name)
    json.dump(
        [region.dict() for region in regions],
        sys.stdout,
        indent=None,
        separators=(",", ":"),
        sort_keys=True,
    )

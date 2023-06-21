import json
import sys

import click

from lambda_cloud import openapi, paths
from lambda_cloud.cli import ClickApiKeyWrapper


def api_get_instance_types(
    api_key: str,
    available: bool,
) -> list[openapi.Data]:
    instance_types: openapi.InstanceTypesGetResponse = paths.instance_types(api_key)
    instances: list[openapi.Data] = []

    for data_instance_type in instance_types.data.values():
        isAvailable = data_instance_type.regions_with_capacity_available != []
        # P -> Q is equivalent to not P or Q
        if not available or isAvailable:
            instances.append(data_instance_type)

    instances.sort(key=lambda instance: instance.instance_type.name)
    return instances


@click.command()
@ClickApiKeyWrapper
@click.option(
    "--available",
    default=False,
    help="List only available instance types",
    is_flag=True,
    show_default=True,
    type=bool,
)
def get_instance_types(
    api_key: str,
    available: bool,
) -> None:
    """Get instance types."""
    instances: list[openapi.Data] = api_get_instance_types(api_key, available)
    json.dump(
        [instance.dict() for instance in instances],
        sys.stdout,
        indent=None,
        separators=(",", ":"),
        sort_keys=True,
    )

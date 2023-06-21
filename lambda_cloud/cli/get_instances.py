import json
import sys
import click
from lambda_cloud import openapi, paths
from lambda_cloud.cli import ClickApiKeyWrapper


def api_get_instances(api_key: str) -> list[openapi.Instance]:
    instances: openapi.InstancesGetResponse = paths.list_instances(api_key)
    # TODO(@connorbaker): What does it mean if instance_type is None?
    instances.data.sort(key=lambda instance: instance.instance_type.name)  # type: ignore
    return instances.data


@click.command()
@ClickApiKeyWrapper
def get_instances(api_key: str) -> None:
    """Get running instances."""
    instances: list[openapi.Instance] = api_get_instances(api_key)
    json.dump(
        [instance.dict() for instance in instances],
        sys.stdout,
        indent=None,
        separators=(",", ":"),
        sort_keys=True,
    )

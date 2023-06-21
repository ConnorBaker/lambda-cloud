import json
import sys
import click
from lambda_cloud import openapi, paths
from lambda_cloud.cli import ClickApiKeyWrapper, ClickInstanceIdWrapper


@click.command()
@ClickApiKeyWrapper
@ClickInstanceIdWrapper
def get_instance(api_key: str, instance_id: str) -> None:
    """Get instance details."""
    details: openapi.InstancesIdGetResponse = paths.get_instance(api_key, instance_id)
    json.dump(
        details.data.dict(),
        sys.stdout,
        indent=None,
        separators=(",", ":"),
        sort_keys=True,
    )

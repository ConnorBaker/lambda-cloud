import json
import logging
import sys

import click

from lambda_cloud import openapi, paths
from lambda_cloud.cli import ClickApiKeyWrapper, ClickInstanceTypeNameWrapper
from lambda_cloud.cli.get_instance_types import api_get_instance_types


def api_launch_instance(
    api_key: str,
    instance_type_name: str,
    instance_name: str,
    ssh_key_name: str,
    region_name: None | str,
) -> list[str]:
    # Check if instance type is available (we also need to know the region)
    available_instance_types: list[openapi.Data] = api_get_instance_types(api_key, available=True)
    matching_instances = [
        available_instance_type
        for available_instance_type in available_instance_types
        if available_instance_type.instance_type.name == instance_type_name
    ]
    # Sanity check that there's only one matching instance type
    if len(matching_instances) == 0:
        logging.error(f"No available instances found for {instance_type_name}.")
        logging.error(
            "Consider one of these available instance types: "
            + ", ".join(
                [
                    available_instance_type.instance_type.name
                    for available_instance_type in available_instance_types
                ]
            )
        )
        sys.exit(1)

    if len(matching_instances) > 1:
        logging.error(
            "Found multiple entries for the same instance type, which should not happen."
        )
        sys.exit(1)

    # Proceed with our one matching instance type
    matching_instance: openapi.Data = matching_instances[0]

    # If no region is specified, use the first available region
    if region_name is None:
        region_name = matching_instance.regions_with_capacity_available[0].name

    launch_post_request = openapi.InstanceOperationsLaunchPostRequest(
        instance_type_name=instance_type_name,
        name=instance_name,
        region_name=region_name,
        ssh_key_names=[openapi.SshKeyName(__root__=ssh_key_name)],
    )
    logging.info(f"Launch POST request: {launch_post_request.json()}")

    launched: openapi.InstanceOperationsLaunchPostResponse = paths.launch_instance(
        api_key,
        launch_post_request,
    )
    launched.data.instance_ids.sort()
    return launched.data.instance_ids


@click.command()
@ClickApiKeyWrapper
@ClickInstanceTypeNameWrapper
@click.option(
    "--instance-name",
    help="Instance name",
    required=True,
    type=str,
)
@click.option(
    "--ssh-key-name",
    help="SSH key name",
    required=True,
    type=str,
)
@click.option(
    "--region-name",
    help="Region name. If not specified, will use the first available region.",
    required=False,
    type=str,
)
def launch_instance(
    api_key: str,
    instance_type_name: str,
    instance_name: str,
    ssh_key_name: str,
    region_name: None | str,
) -> None:
    """Launch an instance."""
    instance_ids: list[str] = api_launch_instance(
        api_key, instance_type_name, instance_name, ssh_key_name, region_name
    )
    json.dump(
        instance_ids,
        sys.stdout,
        indent=None,
        separators=(",", ":"),
        sort_keys=True,
    )

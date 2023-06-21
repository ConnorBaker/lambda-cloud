import json
import logging
import sys
import time

import click

from lambda_cloud import openapi, paths
from lambda_cloud.cli import (
    ClickApiKeyWrapper,
    ClickInstanceIdWrapper,
    ClickInstanceStatusWrapper,
)
from lambda_cloud.types import InstanceStatus


def api_wait_for_status(
    api_key: str, instance_id: str, instance_status: InstanceStatus, timeout: int, frequency: int
) -> openapi.Instance:
    logging.info(
        f"Waiting for instance {instance_id} to be {instance_status}, will query status every"
        " {frequency}s."
    )
    details: openapi.InstancesIdGetResponse = paths.get_instance(api_key, instance_id)
    actual_status: InstanceStatus = details.data.status
    start_time: float = time.time()
    while actual_status != instance_status:
        if time.time() - start_time > timeout:
            logging.error(
                f"Instance {instance_id} did not reach status {instance_status} within {timeout}s,"
                " exiting with error..."
            )
            sys.exit(1)
        time.sleep(frequency)
        details = paths.get_instance(api_key, instance_id)
        actual_status = details.data.status
    return details.data


@click.command()
@ClickApiKeyWrapper
@ClickInstanceIdWrapper
@ClickInstanceStatusWrapper
@click.option(
    "--timeout",
    default=1800,
    help="Timeout in seconds",
    show_default=True,
    type=click.IntRange(min=1),
)
@click.option(
    "--frequency",
    default=30,
    help="Frequency in seconds",
    show_default=True,
    type=click.IntRange(min=1),
)
def wait_for_status(
    api_key: str,
    instance_id: str,
    instance_status: InstanceStatus,
    timeout: int,
    frequency: int,
) -> None:
    """Wait for instance to reach status."""
    details: openapi.Instance = api_wait_for_status(
        api_key, instance_id, instance_status, timeout, frequency
    )
    json.dump(
        details.dict(),
        sys.stdout,
        indent=None,
        separators=(",", ":"),
        sort_keys=True,
    )

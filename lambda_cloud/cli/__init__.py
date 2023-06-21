import click

from lambda_cloud.types import InstanceTypeName, InstanceStatus
from typing import get_args


ClickApiKeyWrapper = click.option(
    "--api-key",
    envvar="LAMBDA_CLOUD_API_KEY",
    help=(
        "API key for Lambda Cloud, can also be set via the LAMBDA_CLOUD_API_KEY environment"
        " variable"
    ),
    required=True,
    type=str,
)
ClickInstanceTypeNameWrapper = click.option(
    "--instance-type-name",
    help="Instance type name",
    required=True,
    type=click.Choice(get_args(InstanceTypeName)),
)
ClickInstanceStatusWrapper = click.option(
    "--instance-status",
    help="Instance status",
    required=True,
    type=click.Choice(get_args(InstanceStatus)),
)
ClickInstanceIdWrapper = click.option(
    "--instance-id",
    help="Instance ID",
    required=True,
    type=str,
)

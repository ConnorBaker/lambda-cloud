import json
import sys

import click

from lambda_cloud import openapi, paths
from lambda_cloud.cli import ClickApiKeyWrapper


def api_add_ssh_key(
    api_key: str,
    ssh_key_name: str,
    ssh_public_key: str,
) -> openapi.SshKey:
    request_body = openapi.SshKeysPostRequest(
        name=ssh_key_name,
        public_key=ssh_public_key,
    )
    response: openapi.SshKeysPostResponse = paths.add_ssh_key(api_key, request_body)
    ssh_key = response.data
    return ssh_key


@click.command()
@ClickApiKeyWrapper
@click.option(
    "--ssh-key-name",
    help="Name of the SSH key to add to Lambda Cloud",
    required=True,
    type=str,
)
@click.option(
    "--ssh-public-key",
    help="Public key to add to Lambda Cloud",
    required=True,
    type=str,
)
def add_ssh_key(
    api_key: str,
    ssh_key_name: str,
    ssh_public_key: str,
) -> None:
    """Add SSH key."""
    ssh_key: openapi.SshKey = api_add_ssh_key(api_key, ssh_key_name, ssh_public_key)
    json.dump(
        ssh_key.dict(),
        sys.stdout,
        indent=None,
        separators=(",", ":"),
        sort_keys=True,
    )

import json
import sys

import click

from lambda_cloud import openapi, paths
from lambda_cloud.cli import ClickApiKeyWrapper


def api_get_ssh_keys(
    api_key: str,
) -> list[openapi.SshKey]:
    response: openapi.SshKeysGetResponse = paths.list_ssh_keys(api_key)
    ssh_keys = response.data
    return ssh_keys


@click.command()
@ClickApiKeyWrapper
def get_ssh_keys(api_key: str) -> None:
    """Get SSH keys."""
    ssh_keys: list[openapi.SshKey] = api_get_ssh_keys(api_key)
    json.dump(
        [ssh_key.dict() for ssh_key in ssh_keys],
        sys.stdout,
        indent=None,
        separators=(",", ":"),
        sort_keys=True,
    )

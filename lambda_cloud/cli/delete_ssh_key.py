import click

from lambda_cloud import paths
from lambda_cloud.cli import ClickApiKeyWrapper


@click.command()
@ClickApiKeyWrapper
@click.option(
    "--ssh-key-id",
    help="ID of the SSH key to remove from Lambda Cloud",
    required=True,
    type=str,
)
def delete_ssh_key(
    api_key: str,
    ssh_key_id: str,
) -> None:
    """Delete SSH key."""
    return paths.delete_ssh_key(api_key, ssh_key_id)

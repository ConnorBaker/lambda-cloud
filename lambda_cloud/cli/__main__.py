from __future__ import annotations

import logging
import sys

import click

from lambda_cloud.cli.get_instance import get_instance
from lambda_cloud.cli.get_instance_types import get_instance_types
from lambda_cloud.cli.get_instances import get_instances
from lambda_cloud.cli.get_regions import get_regions
from lambda_cloud.cli.launch_instance import launch_instance
from lambda_cloud.cli.terminate_instance import terminate_instance
from lambda_cloud.cli.wait_for_status import wait_for_status


@click.group()
@click.option(
    "--info/--no-info",
    default=False,
    help="Enable or disable info logging",
    show_default=True,
    type=bool,
)
def cli(info: bool) -> None:
    logging.basicConfig(
        format="[%(asctime)s][%(levelname)s] %(message)s",
        level=logging.INFO if info else logging.WARNING,
        stream=sys.stderr,
    )


def main() -> None:
    cli.add_command(get_instance_types)
    cli.add_command(get_instance)
    cli.add_command(get_instances)
    cli.add_command(get_regions)
    cli.add_command(launch_instance)
    cli.add_command(terminate_instance)
    cli.add_command(wait_for_status)

    cli(obj={})


if __name__ == "__main__":
    main()

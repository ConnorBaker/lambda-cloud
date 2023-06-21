import logging
import click
from lambda_cloud import openapi, paths
from lambda_cloud.cli import ClickApiKeyWrapper, ClickInstanceIdWrapper


def api_terminate_instance(api_key: str, instance_id: str) -> list[openapi.Instance]:
    terminate_post_request = openapi.InstanceOperationsTerminatePostRequest(
        instance_ids=[instance_id]
    )
    logging.info(f"Terminate POST request: {terminate_post_request.json()}")

    terminated: openapi.InstanceOperationsTerminatePostResponse = paths.terminate_instance(
        api_key,
        terminate_post_request,
    )
    terminated_instances = terminated.data.terminated_instances
    # TODO(@connorbaker): What does it mean if instance_type is None?
    terminated_instances.sort(key=lambda instance: instance.instance_type.name)  # type: ignore
    return terminated_instances


@click.command()
@ClickApiKeyWrapper
@ClickInstanceIdWrapper
def terminate_instance(
    api_key: str,
    instance_id: str,
) -> None:
    """Terminate an instance."""
    api_terminate_instance(api_key, instance_id)

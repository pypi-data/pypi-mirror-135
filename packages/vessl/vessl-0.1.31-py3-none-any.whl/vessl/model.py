from typing import List

from openapi_client import ResponseFileMetadata
from openapi_client.models import (
    ModelCreateAPIPayload,
    ModelUpdateAPIPayload,
    ResponseModelDetail,
)
from vessl import vessl_api
from vessl.organization import _get_organization_name
from vessl.volume import copy_volume_file, delete_volume_file, list_volume_files


def read_model(
    repository_name: str, model_number: int, **kwargs
) -> ResponseModelDetail:
    """Read model

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.model_read_api(
        organization_name=_get_organization_name(**kwargs),
        repository_name=repository_name,
        number=model_number,
    )


def list_models(repository_name: str, **kwargs) -> List[ResponseModelDetail]:
    """List models

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.model_list_api(
        organization_name=_get_organization_name(**kwargs),
        repository_name=repository_name,
    ).results


def create_model(
    repository_name: str,
    repository_description: str = None,
    experiment_id: int = None,
    model_name: str = None,
    paths: List[str] = None,
    **kwargs,
) -> ResponseModelDetail:
    """Create model

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.model_create_api(
        organization_name=_get_organization_name(**kwargs),
        repository_name=repository_name,
        model_create_api_payload=ModelCreateAPIPayload(
            repository_description=repository_description,
            experiment_id=experiment_id,
            model_name=model_name,
            paths=paths,
        ),
    )


def update_model(
    repository_name: str, number: int, name: str, **kwargs
) -> ResponseModelDetail:
    """Update model

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.model_update_api(
        organization_name=_get_organization_name(**kwargs),
        repository_name=repository_name,
        number=number,
        model_update_api_payload=ModelUpdateAPIPayload(name=name),
    )


def delete_model(repository_name: str, number: int, **kwargs) -> object:
    """Delete model

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.model_delete_api(
        organization_name=_get_organization_name(**kwargs),
        repository_name=repository_name,
        version=number,
    )


def list_model_volume_files(
    repository_name: str,
    model_number: int,
    need_download_url: bool = False,
    path: str = "",
    recursive: bool = False,
    **kwargs,
) -> List[ResponseFileMetadata]:
    """List model files

    Keyword args:
        organization_name (str): override default organization
    """
    model = read_model(
        repository_name=repository_name, model_number=model_number, **kwargs
    )
    return list_volume_files(
        model.artifact_volume_id, need_download_url, path, recursive
    )


def upload_model_volume_file(
    repository_name: str,
    model_number: int,
    source_path: str,
    dest_path: str,
    **kwargs,
) -> None:
    """Upload file to model

    Keyword args:
        organization_name (str): override default organization
    """
    model = read_model(
        repository_name=repository_name, model_number=model_number, **kwargs
    )
    return copy_volume_file(
        source_volume_id=None,
        source_path=source_path,
        dest_volume_id=model.artifact_volume_id,
        dest_path=dest_path,
    )


def download_model_volume_file(
    repository_name: str,
    model_number: int,
    source_path: str,
    dest_path: str,
    **kwargs,
) -> None:
    """Download file to model

    Keyword args:
        organization_name (str): override default organization
    """
    model = read_model(
        repository_name=repository_name, model_number=model_number, **kwargs
    )
    return copy_volume_file(
        source_volume_id=model.artifact_volume_id,
        source_path=source_path,
        dest_volume_id=None,
        dest_path=dest_path,
    )


def delete_model_volume_file(
    repository_name: str,
    model_number: int,
    path: str,
    recursive: bool = False,
    **kwargs,
) -> List[ResponseFileMetadata]:
    """Delete model volume file

    Keyword args:
        organization_name (str): override default organization
    """
    model = read_model(
        repository_name=repository_name, model_number=model_number, **kwargs
    )
    return delete_volume_file(model.artifact_volume_id, path, recursive)

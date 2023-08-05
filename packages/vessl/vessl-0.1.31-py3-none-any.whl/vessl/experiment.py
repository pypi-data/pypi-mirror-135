import os
import platform
import sys
from typing import Dict, List

import psutil
import pynvml

from openapi_client import DistributedExperimentCreateAPIPayload
from openapi_client.models import (
    ExperimentCreateAPIPayload,
    InfluxdbWorkloadLog,
    LocalExperimentCreateAPIPayload,
    OrmEnvVar,
    ResponseExperimentInfo,
    ResponseExperimentListResponse,
    ResponseFileMetadata,
)
from openapi_client.models.orm_execution_environment import OrmExecutionEnvironment
from vessl import __version__, vessl_api
from vessl.kernel_cluster import read_cluster
from vessl.kernel_resource_spec import (
    _configure_custom_kernel_resource_spec,
    read_kernel_resource_spec,
)
from vessl.organization import _get_organization_name
from vessl.project import _get_project_name
from vessl.util import logger
from vessl.util.common import safe_cast
from vessl.util.constant import MOUNT_PATH_OUTPUT, MOUNT_TYPE_OUTPUT
from vessl.util.exception import InvalidExperimentError, InvalidParamsError
from vessl.volume import (
    _configure_volume_mount_requests,
    copy_volume_file,
    list_volume_files,
)


def read_experiment(experiment_name_or_number: str, **kwargs) -> ResponseExperimentInfo:
    """Read experiment

    Keyword args:
        organization_name (str): override default organization
        project_name (str): override default project
    """
    return vessl_api.experiment_read_api(
        experiment=experiment_name_or_number,
        organization_name=_get_organization_name(**kwargs),
        project_name=_get_project_name(**kwargs),
    )


def read_experiment_by_id(experiment_id: int, **kwargs) -> ResponseExperimentInfo:
    result = vessl_api.experiment_read_by_idapi(experiment_id=experiment_id)
    assert isinstance(result, ResponseExperimentInfo)
    return result


def list_experiments(**kwargs) -> List[ResponseExperimentListResponse]:
    """List experiments

    Keyword args:
        organization_name (str): override default organization
        project_name (str): override default project
    """
    return vessl_api.experiment_list_api(
        organization_name=_get_organization_name(**kwargs),
        project_name=_get_project_name(**kwargs),
    ).results


def create_experiment(
    cluster_name: str,
    start_command: str,
    kernel_resource_spec_name: str = None,
    processor_type: str = None,
    cpu_limit: float = None,
    memory_limit: str = None,
    gpu_type: str = None,
    gpu_limit: int = None,
    kernel_image_url: str = None,
    *,
    message: str = None,
    termination_protection: bool = False,
    env_vars: List[str] = None,
    dataset_mounts: List[str] = None,
    model_mounts: List[str] = None,
    git_ref_mounts: List[str] = None,
    git_diff_mount: str = None,
    local_files: List[str] = None,
    upload_local_git_diff: bool = None,
    archive_file_mount: str = None,
    root_volume_size: str = None,
    working_dir: str = None,
    output_dir: str = MOUNT_PATH_OUTPUT,
    worker_count: int = 1,
    framework_type: str = None,
    **kwargs,
) -> ResponseExperimentInfo:
    """Create experiment

    Keyword args:
        organization_name (str): override default organization
        project_name (str): override default project
        git_branch (str): override current git branch
        git_ref (str): override current git commit
        use_git_diff (bool): run experiment with uncommitted changes
        use_git_diff_untracked (bool): run with untracked changed (only valid if `use_git_diff` is set)
    """
    cluster = read_cluster(cluster_name)

    kernel_resource_spec = kernel_resource_spec_id = None
    if kernel_resource_spec_name:
        kernel_resource_spec_id = read_kernel_resource_spec(
            cluster.id,
            kernel_resource_spec_name,
        ).id
    else:
        kernel_resource_spec = _configure_custom_kernel_resource_spec(
            processor_type,
            cpu_limit,
            memory_limit,
            gpu_type,
            gpu_limit,
        )

    volume_mount_requests = _configure_volume_mount_requests(
        dataset_mounts=dataset_mounts,
        model_mounts=model_mounts,
        git_ref_mounts=git_ref_mounts,
        git_diff_mount=git_diff_mount,
        local_files=local_files,
        upload_local_git_diff=upload_local_git_diff,
        archive_file_mount=archive_file_mount,
        root_volume_size=root_volume_size,
        working_dir=working_dir,
        output_dir=output_dir,
        **kwargs,
    )

    if worker_count > 1:
        return vessl_api.distributed_experiment_create_api(
            organization_name=_get_organization_name(**kwargs),
            project_name=_get_project_name(**kwargs),
            distributed_experiment_create_api_payload=DistributedExperimentCreateAPIPayload(
                cluster_id=cluster.id,
                env_vars=[
                    OrmEnvVar(key, str(value))
                    for key, value in map(
                        lambda env_var: env_var.split("="), (env_vars or [])
                    )
                ],
                framework_type=framework_type,
                image_url=kernel_image_url,
                message=message,
                worker_replicas=worker_count,
                worker_resource_spec=kernel_resource_spec,
                worker_resource_spec_id=kernel_resource_spec_id,
                start_command=start_command,
                termination_protection=termination_protection,
                volumes=volume_mount_requests,
            ),
        )

    return vessl_api.experiment_create_api(
        organization_name=_get_organization_name(**kwargs),
        project_name=_get_project_name(**kwargs),
        experiment_create_api_payload=ExperimentCreateAPIPayload(
            cluster_id=cluster.id,
            env_vars=[
                OrmEnvVar(key, str(value))
                for key, value in map(
                    lambda env_var: env_var.split("="), (env_vars or [])
                )
            ],
            image_url=kernel_image_url,
            message=message,
            resource_spec=kernel_resource_spec,
            resource_spec_id=kernel_resource_spec_id,
            start_command=start_command,
            termination_protection=termination_protection,
            volumes=volume_mount_requests,
        ),
    )


def _create_orm_execution_environment():
    cpu_count = psutil.cpu_count()

    gpu_count = gpu_type = None
    try:
        pynvml.nvmlInit()
        gpu_count = pynvml.nvmlDeviceGetCount()
        gpu_type = pynvml.nvmlDeviceGetName(
            pynvml.nvmlDeviceGetHandleByIndex(0)
        ).decode("utf8")
    except pynvml.nvml.NVMLError:
        pass

    hostname = platform.node()
    os = platform.platform(aliased=True)
    python_version = platform.python_version()
    python_executable = sys.executable
    start_command = " ".join(sys.argv)
    vessl_version = __version__

    return OrmExecutionEnvironment(
        cpu_count=cpu_count,
        gpu_count=gpu_count,
        gpu_type=gpu_type,
        hostname=hostname,
        os=os,
        python_version=python_version,
        python_executable=python_executable,
        start_command=start_command,
        vessl_version=vessl_version,
    )


def create_local_experiment(
    message: str = None, hyperparameters: dict = None, **kwargs
):
    return vessl_api.local_experiment_create_api(
        local_experiment_create_api_payload=LocalExperimentCreateAPIPayload(
            execution_environment=_create_orm_execution_environment(),
            message=message,
            hyperparameters=hyperparameters,
        ),
        organization_name=_get_organization_name(**kwargs),
        project_name=_get_project_name(**kwargs),
    )


def list_experiment_logs(
    experiment_name: str,
    tail: int = 200,
    worker_number: int = 0,
    after: int = 0,
    **kwargs,
) -> List[InfluxdbWorkloadLog]:
    """List experiment logs

    Args:
        experiment_name (str): experiment name or number
        tail (int): number of lines to display from the end. Display all if -1.
        worker_number (int): override default worker number

    Keyword args:
        organization_name (str): override default organization
        project_name (str): override default project
    """
    if tail == -1:
        tail = None

    experiment = read_experiment(experiment_name, **kwargs)

    if experiment.is_distributed:
        str_worker_number = safe_cast(worker_number, str, "0")
        return vessl_api.distributed_experiment_logs_api(
            experiment=experiment_name,
            limit=tail,
            organization_name=_get_organization_name(**kwargs),
            project_name=_get_project_name(**kwargs),
            distributed_number=worker_number,
        ).logs[str_worker_number]

    return vessl_api.experiment_logs_api(
        experiment=experiment_name,
        limit=tail,
        organization_name=_get_organization_name(**kwargs),
        project_name=_get_project_name(**kwargs),
        after=after,
    ).logs


def list_experiment_output_files(
    experiment_name: str,
    need_download_url: bool = False,
    recursive: bool = True,
    worker_number: int = 0,
    **kwargs,
) -> List[ResponseFileMetadata]:
    """List experiment output files

    Keyword args:
        organization_name (str): override default organization
        project_name (str): override default project
    """
    experiment = read_experiment(experiment_name, **kwargs)

    if experiment.is_local:
        volume_id = experiment.local_execution_spec.output_volume_id
        return list_volume_files(
            volume_id=volume_id,
            need_download_url=need_download_url,
            path="",
            recursive=recursive,
        )
    elif experiment.is_distributed:
        worker_replicas = experiment.distributed_spec.pytorch_spec.worker_replicas
        if worker_number >= worker_replicas:
            raise InvalidParamsError(
                "worker-number: should be less than {}".format(worker_replicas)
            )

        for volume_mount in experiment.volume_mounts_list[worker_number].mounts:
            if volume_mount.source_type == MOUNT_TYPE_OUTPUT:
                return list_volume_files(
                    volume_id=volume_mount.volume.volume_id,
                    need_download_url=need_download_url,
                    path="",
                    recursive=recursive,
                )
    else:
        for volume_mount in experiment.volume_mounts.mounts:
            if volume_mount.source_type == MOUNT_TYPE_OUTPUT:
                return list_volume_files(
                    volume_id=volume_mount.volume.volume_id,
                    need_download_url=need_download_url,
                    path="",
                    recursive=recursive,
                )

    logger.info("No output volume mounted")


def download_experiment_output_files(
    experiment_name: str,
    dest_path: str = os.path.join(os.getcwd(), "output"),
    worker_number: int = 0,
    **kwargs,
) -> None:
    """Download experiment output files

    Keyword args:
        organization_name (str): override default organization
        project_name (str): override default project
    """
    experiment = read_experiment(experiment_name, **kwargs)

    if experiment.is_local:
        volume_id = experiment.local_execution_spec.output_volume_id
        return copy_volume_file(
            source_volume_id=volume_id,
            source_path="",
            dest_volume_id=None,
            dest_path=dest_path,
            recursive=True,
        )
    if experiment.is_distributed:
        worker_replicas = experiment.distributed_spec.pytorch_spec.worker_replicas
        if worker_number >= worker_replicas:
            raise InvalidParamsError(
                "worker-number: should be less than {}".format(worker_replicas)
            )

        for volume_mount in experiment.volume_mounts_list[worker_number].mounts:
            if volume_mount.source_type == MOUNT_TYPE_OUTPUT:
                return copy_volume_file(
                    source_volume_id=volume_mount.volume.volume_id,
                    source_path="",
                    dest_volume_id=None,
                    dest_path=dest_path,
                    recursive=True,
                )
    else:
        for volume_mount in experiment.volume_mounts.mounts:
            if volume_mount.source_type == MOUNT_TYPE_OUTPUT:
                return copy_volume_file(
                    source_volume_id=volume_mount.volume.volume_id,
                    source_path="",
                    dest_volume_id=None,
                    dest_path=dest_path,
                    recursive=True,
                )

    logger.info("No output volume mounted")


def upload_experiment_output_files(experiment_name: str, path: str):
    experiment = read_experiment(experiment_name)
    if not experiment.is_local:
        raise InvalidExperimentError("Experiment cannot be Vessl-managed.")

    return copy_volume_file(
        source_volume_id=None,
        source_path=path,
        dest_volume_id=experiment.local_execution_spec.output_volume_id,
        dest_path="",
    )

import os
import time
from typing import List

import click

from vessl.cli._base import VesslGroup, vessl_argument, vessl_option
from vessl.cli._util import (
    Endpoint,
    generic_prompter,
    print_data,
    print_logs,
    print_table,
    print_volume_files,
    prompt_choices,
    sizeof_fmt,
    truncate_datetime,
)
from vessl.cli.kernel_cluster import cluster_option
from vessl.cli.kernel_resource_spec import resource_option
from vessl.cli.organization import organization_name_option
from vessl.cli.project import project_name_option
from vessl.experiment import (
    create_experiment,
    download_experiment_output_files,
    list_experiment_logs,
    list_experiment_output_files,
    list_experiments,
    read_experiment,
)
from vessl.kernel_cluster import list_cluster_nodes
from vessl.kernel_image import list_kernel_images
from vessl.project import _get_project
from vessl.util import logger
from vessl.util.constant import (
    FRAMEWORK_TYPE_PYTORCH,
    FRAMEWORK_TYPE_TENSORFLOW,
    FRAMEWORK_TYPES,
    MOUNT_PATH_OUTPUT,
    PROCESSOR_TYPE_GPU,
    PROCESSOR_TYPES,
)
from vessl.util.exception import GitError
from vessl.util.git import get_git_repo


def experiment_name_prompter(
    ctx: click.Context,
    param: click.Parameter,
    value: str,
) -> str:
    experiments = list_experiments()
    return prompt_choices(
        "Experiment", [(f"{x.name} #{x.number}", x.name) for x in reversed(experiments)]
    )


def local_experiment_name_prompter(
    ctx: click.Context,
    param: click.Parameter,
    value: str,
) -> str:
    experiments = [e for e in list_experiments() if e.is_local]
    return prompt_choices(
        "Experiment", [(f"{x.name} #{x.number}", x.name) for x in reversed(experiments)]
    )


def processor_type_prompter(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="Cluster (`--cluster`) must be specified before processor type (`--processor-type`).",
        )

    if ctx.obj.get("resource") is None:
        processor_type = prompt_choices("Processor Type", PROCESSOR_TYPES)
        ctx.obj["processor_type"] = processor_type
        return processor_type


def processor_type_callback(ctx: click.Context, param: click.Parameter, value: str):
    if value:
        ctx.obj["processor_type"] = value
    return value


def cpu_limit_prompter(
    ctx: click.Context, param: click.Parameter, value: float
) -> float:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="Cluster (`--cluster`) must be specified before CPU limit (`--cpu-limit`).",
        )

    if ctx.obj.get("resource") is None:
        return click.prompt("CPUs (in vCPU)", type=click.FLOAT)


def memory_limit_prompter(
    ctx: click.Context, param: click.Parameter, value: float
) -> float:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="Cluster (`--cluster`) must be specified before memory limit (`--memory-limit`).",
        )

    if ctx.obj.get("resource") is None:
        return click.prompt("Memory (e.g. 4Gi)", type=click.STRING)


def gpu_type_prompter(ctx: click.Context, param: click.Parameter, value: str) -> str:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="Cluster (`--cluster`) must be specified before GPU type (`--gpu-type`).",
        )

    if ctx.obj.get("resource") is None:
        processor_type = ctx.obj.get("processor_type")
        if processor_type is None:
            raise click.UsageError(
                message="Processor type must be specified before GPU type (`--gpu-type`).",
            )
        if processor_type == PROCESSOR_TYPE_GPU:
            nodes = list_cluster_nodes(cluster.id)
            return prompt_choices("GPU Type", [x.gpu_product_name for x in nodes])


def gpu_limit_prompter(
    ctx: click.Context, param: click.Parameter, value: float
) -> float:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="Cluster (`--cluster`) must be specified before GPU limit (`--gpu-limit`).",
        )

    if ctx.obj.get("resource") is None:
        processor_type = ctx.obj.get("processor_type")
        if processor_type is None:
            raise click.UsageError(
                message="Processor type must be specified before GPU limit (`--gpu-limit`).",
            )

        if processor_type == PROCESSOR_TYPE_GPU:
            return click.prompt("GPUs (in vGPU)", type=click.FLOAT)


def image_url_prompter(ctx: click.Context, param: click.Parameter, value: str) -> str:
    processor_type = ctx.obj.get("processor_type")
    if processor_type is None:
        raise click.UsageError(
            message="Processor type must be specified before image URL (`--image-url`).",
        )

    images = list_kernel_images()
    images = [x for x in images if x.processor_type == processor_type]

    return prompt_choices("Image URL", [x.image_url for x in images])


def upload_local_file_callback(
    ctx: click.Context, param: click.Parameter, value: List[str]
) -> List[str]:
    if value:
        for dir_spec in value:
            if ":" in dir_spec:
                local_path, _ = dir_spec.split(":")
            else:
                local_path = dir_spec

            if not local_path:
                raise click.BadOptionUsage(
                    option_name="--upload-local-file",
                    message=f"Invalid path {local_path}.",
                )

            if not os.path.exists(local_path):
                raise click.BadOptionUsage(
                    option_name="--upload-local-file",
                    message=f"{local_path} does not exist.",
                )

            if os.path.isdir(local_path):
                from pathlib import Path

                root_directory = Path(local_path)
                directory_size = sum(
                    f.stat().st_size for f in root_directory.glob("**/*") if f.is_file()
                )
                logger.debug(f"Current directory size: {sizeof_fmt(directory_size)}")
                if directory_size >= 3 * 1024 * 1024 * 1024:
                    click.confirm(
                        f"Try to upload [{os.path.abspath(local_path)}] "
                        f"but it's too large ({sizeof_fmt(directory_size)}). "
                        f"Process anyway?",
                        abort=True,
                    )

    return value


def upload_local_git_diff_prompter(
    ctx: click.Context, param: click.Parameter, value: bool
) -> bool:
    try:
        local_git_owner, local_git_repo = get_git_repo()
    except GitError:
        return False

    if ctx.params.get("git_diff"):
        return False

    project = _get_project(**ctx.params)
    for repo in project.project_repositories:
        if repo.git_owner == local_git_owner and repo.git_repo == local_git_repo:
            return click.prompt("Upload local git commit & diff (y/n)", type=click.BOOL)
    return False


def worker_count_callback(
    ctx: click.Context, param: click.Parameter, value: int
) -> int:
    if value is None:
        value = 1

    if value < 1:
        raise click.BadOptionUsage(
            option_name="--worker-count",
            message="num nodes (`--num-nodes`) must be a positive integer.",
        )

    ctx.obj["worker_count"] = value
    return value


def framework_type_prompter(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    worker_count = ctx.obj.get("worker_count")
    if worker_count == 1:
        return ""

    framework_type = prompt_choices("Processor Type", FRAMEWORK_TYPES)
    if framework_type == FRAMEWORK_TYPE_TENSORFLOW:
        raise click.BadOptionUsage(
            option_name="--framework-type",
            message="Only PyTorch distributed experiment is supported currently.",
        )
    return framework_type


@click.command(name="experiment", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=experiment_name_prompter
)
@organization_name_option
@project_name_option
def read(name: str):
    experiment = read_experiment(experiment_name_or_number=name)

    distributed_spec = "None"
    if experiment.is_distributed:
        if experiment.distributed_spec.framework_type == FRAMEWORK_TYPE_PYTORCH:
            distributed_spec = {
                "Framework Type": experiment.distributed_spec.framework_type,
                "PyTorch Spec": {
                    "Worker count": experiment.distributed_spec.pytorch_spec.worker_replicas,
                },
            }
        elif experiment.distributed_spec.framework_type == FRAMEWORK_TYPE_TENSORFLOW:
            distributed_spec = {
                "Framework Type": experiment.distributed_spec.framework_type,
                "TensorFlow Spec": experiment.distributed_spec.tensorflow_spec,
            }

    kernel_image = "None"
    if experiment.kernel_image:
        kernel_image = {
            "Name": experiment.kernel_image.name,
            "URL": experiment.kernel_image.image_url,
        }

    resource_spec = "None"
    if experiment.kernel_resource_spec:
        resource_spec = {
            "Name": experiment.kernel_resource_spec.name,
            "CPU Type": experiment.kernel_resource_spec.cpu_type,
            "CPU Limit": experiment.kernel_resource_spec.cpu_limit,
            "Memory Limit": experiment.kernel_resource_spec.memory_limit,
            "GPU Type": experiment.kernel_resource_spec.gpu_type,
            "GPU Limit": experiment.kernel_resource_spec.gpu_limit,
        }

    print_data(
        {
            "ID": experiment.id,
            "Number": experiment.number,
            "Name": experiment.name,
            "Distributed": experiment.is_distributed,
            "Distributed Spec": distributed_spec,
            "Local": experiment.is_local,
            "Status": experiment.status,
            "Created": truncate_datetime(experiment.created_dt),
            "Message": experiment.message,
            "Kernel Image": kernel_image,
            "Resource Spec": resource_spec,
            "Start command": experiment.start_command,
        }
    )
    print(
        f"For more info: {Endpoint.experiment.format(experiment.organization.name, experiment.project.name, experiment.number)}"
    )


@cli.vessl_command()
@organization_name_option
@project_name_option
def list():
    experiments = list_experiments()
    print_table(
        experiments,
        ["ID", "Name", "Distributed", "Status", "Created", "Message"],
        lambda x: [
            x.id,
            x.name,
            x.is_distributed,
            x.status,
            truncate_datetime(x.created_dt),
            x.message,
        ],
    )


command_option = vessl_option(
    "-x",
    "--command",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Start command"),
    help="Start command to execute in experiment container.",
)
processor_type_option = vessl_option(
    "--processor-type",
    type=click.Choice(("CPU", "GPU")),
    prompter=processor_type_prompter,
    callback=processor_type_callback,
    help="CPU or GPU (for custom resource only).",
)
cpu_limit_option = vessl_option(
    "--cpu-limit",
    type=click.FLOAT,
    prompter=cpu_limit_prompter,
    help="Number of vCPUs (for custom resource only).",
)
memory_limit_option = vessl_option(
    "--memory-limit",
    type=click.STRING,
    prompter=memory_limit_prompter,
    help="Memory limit (e.g. 4Gi) (for custom resource only).",
)
gpu_type_option = vessl_option(
    "--gpu-type",
    type=click.STRING,
    prompter=gpu_type_prompter,
    help="GPU type such as Tesla-K80 (for custom resource only).",
)
gpu_limit_option = vessl_option(
    "--gpu-limit",
    type=click.INT,
    prompter=gpu_limit_prompter,
    help="Number of GPU cores (for custom resource only).",
)
image_url_option = vessl_option(
    "-i",
    "--image-url",
    type=click.STRING,
    prompter=image_url_prompter,
    help="Kernel docker image URL",
)
message_option = click.option("-m", "--message", type=click.STRING)
termination_protection_option = click.option("--termination-protection", is_flag=True)
env_var_option = click.option(
    "-e",
    "--env-var",
    type=click.STRING,
    multiple=True,
    help="Environment variables. Format: [key]=[value], ex. `--env-var PORT=8080`.",
)
dataset_option = click.option(
    "--dataset",
    type=click.STRING,
    multiple=True,
    help="Dataset mounts. Format: [mount_path]:[dataset_name]@[optional_dataset_version], ex. `--dataset /input:mnist@3bcd5f`.",
)
model_option = click.option(
    "--model",
    type=click.STRING,
    multiple=True,
    help="Model mounts. Format: [mount_path]:[model_repository_name]/[model_number], ex. `--model /input:pytorch-model/1` .",
)
git_ref_option = click.option(
    "--git-ref",
    type=click.STRING,
    multiple=True,
    help="Git repository mounts. Format: [mount_path]:github/[organization]/[repository]/[optional_commit], ex. `--git-ref /home/vessl/examples:github/savvihub/examples/3cd23dd`.",
)
git_diff_option = click.option(
    "--git-diff",
    type=click.STRING,
    help="Git diff file mounts. Format: [mount_path]:[volume_file_path]. This option is used only for reproducing existing experiments.",
)
upload_local_file_option = vessl_option(
    "--upload-local-file",
    type=click.STRING,
    multiple=True,
    callback=upload_local_file_callback,
    help="Upload local file. Format: [local_path] or [local_path]:[remote_path].",
)
upload_local_git_diff_option = vessl_option(
    "--upload-local-git-diff",
    type=click.BOOL,
    prompter=upload_local_git_diff_prompter,
    help="Upload local git commit hash and diff. Format: --upload-local-git-diff=true or --upload-local-git-diff=false",
)
archive_file_option = click.option(
    "--archive-file",
    type=click.STRING,
    help="Local archive file mounts. Format: [mount_path]:[archive_file_path]]. This option is used only for reproducing existing experiments.",
)
root_volume_size_option = click.option("--root-volume-size", type=click.STRING)
working_dir_option = click.option(
    "--working-dir", type=click.STRING, help="Defaults to `/home/vessl/`."
)
output_dir_option = click.option(
    "--output-dir",
    type=click.STRING,
    default=MOUNT_PATH_OUTPUT,
    help="Directory to store experiment output files. Defaults to `/output`.",
)
worker_count_option = vessl_option(
    "--worker-count",
    type=click.INT,
    callback=worker_count_callback,
    help="The number of nodes to run an experiment. Defaults to 1",
)
framework_type_option = vessl_option(
    "--framework-type",
    type=click.STRING,
    prompter=framework_type_prompter,
    help="Framework type option. Defaults to `pytorch`.",
)


@cli.vessl_command()
@click.pass_context
@organization_name_option
@project_name_option
@cluster_option
@resource_option
@processor_type_option
@cpu_limit_option
@memory_limit_option
@gpu_type_option
@gpu_limit_option
@image_url_option
@message_option
@termination_protection_option
@env_var_option
@dataset_option
@model_option
@git_ref_option
@git_diff_option
@upload_local_file_option
@upload_local_git_diff_option
@archive_file_option
@root_volume_size_option
@working_dir_option
@output_dir_option
@command_option
@worker_count_option
@framework_type_option
def create(
    ctx,
    cluster: str,
    command: str,
    resource: str,
    processor_type: str,
    cpu_limit: float,
    memory_limit: str,
    gpu_type: str,
    gpu_limit: int,
    image_url: str,
    message: str,
    termination_protection: bool,
    env_var: List[str],
    dataset: List[str],
    model: List[str],
    git_ref: List[str],
    git_diff: str,
    upload_local_file: List[str],
    upload_local_git_diff: bool,
    archive_file: str,
    root_volume_size: str,
    working_dir: str,
    output_dir: str,
    worker_count: int,
    framework_type: str,
):
    experiment = create_experiment(
        cluster_name=cluster,
        start_command=command,
        kernel_resource_spec_name=resource,
        processor_type=processor_type,
        cpu_limit=cpu_limit,
        memory_limit=memory_limit,
        gpu_type=gpu_type,
        gpu_limit=gpu_limit,
        kernel_image_url=image_url,
        message=message,
        termination_protection=termination_protection,
        env_vars=env_var,
        dataset_mounts=dataset,
        model_mounts=model,
        git_ref_mounts=git_ref,
        git_diff_mount=git_diff,
        local_files=upload_local_file,
        upload_local_git_diff=upload_local_git_diff,
        archive_file_mount=archive_file,
        root_volume_size=root_volume_size,
        working_dir=working_dir,
        output_dir=output_dir,
        worker_count=worker_count,
        framework_type=framework_type,
    )
    ctx.obj["experiment"] = experiment
    print(
        f"Created '{experiment.name}'.\n"
        f"For more info: {Endpoint.experiment.format(experiment.organization.name, experiment.project.name, experiment.number)}"
    )


worker_number_option = vessl_option(
    "--worker-number",
    type=click.INT,
    default=0,
    help="Worker number (for distributed experiment only).",
)


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=experiment_name_prompter
)
@click.option(
    "--tail",
    type=click.INT,
    default=200,
    help="Number of lines to display (from the end).",
)
@click.option(
    "-f",
    "--follow",
    is_flag=True,
    default=False,
)
@organization_name_option
@project_name_option
@worker_number_option
def logs(
    name: str,
    tail: int,
    follow: bool,
    worker_number: int,
):
    if not follow:
        logs = list_experiment_logs(
            experiment_name=name, tail=tail, worker_numer=worker_number
        )
        print_logs(logs)
        print(f"Displayed last {len(logs)} lines of '{name}'.")
        return

    after = 0

    experiment_finished_dt = None
    while True:
        if (
            read_experiment(name).status not in ["pending", "running"]
            and experiment_finished_dt is None
        ):
            experiment_finished_dt = time.time()

        if (
            experiment_finished_dt is not None
            and (time.time() - experiment_finished_dt) > 5
        ):
            break

        logs = list_experiment_logs(
            experiment_name=name,
            before=int(time.time() - 5),
            after=after,
            worker_numer=worker_number
        )
        print_logs(logs)
        if len(logs) > 0:
            after = logs[-1].timestamp + 0.000001

        time.sleep(3)


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=experiment_name_prompter
)
@organization_name_option
@project_name_option
@worker_number_option
def list_output(
    name: str,
    worker_number: int,
):
    files = list_experiment_output_files(
        experiment_name=name,
        need_download_url=False,
        recursive=True,
        worker_number=worker_number,
    )
    print_volume_files(files)


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=experiment_name_prompter
)
@click.option(
    "-p",
    "--path",
    type=click.Path(),
    default=os.path.join(os.getcwd(), "output"),
    help="Path to store downloads. Defaults to `./output`.",
)
@organization_name_option
@project_name_option
@worker_number_option
def download_output(
    name: str,
    path: str,
    worker_number: int,
):
    download_experiment_output_files(
        experiment_name=name,
        dest_path=path,
        worker_number=worker_number,
    )
    print(f"Downloaded experiment output to {path}.")

from datetime import datetime

import click

from openapi_client import ResponseSimpleModelDetail
from vessl.cli._base import VesslGroup, vessl_argument
from vessl.cli._util import (
    Endpoint,
    format_url,
    generic_prompter,
    print_data,
    print_table,
    prompt_choices,
    truncate_datetime,
)
from vessl.cli.organization import organization_name_option
from vessl.model_repository import (
    create_model_repository,
    list_model_repositories,
    read_model_repository,
)


def model_repository_status(latest_model: ResponseSimpleModelDetail) -> str:
    if latest_model:
        return latest_model.status
    return "Empty repository"


def model_repository_update_dt(
    latest_model: ResponseSimpleModelDetail, default: datetime
) -> datetime:
    if latest_model:
        return truncate_datetime(latest_model.created_dt)
    return truncate_datetime(default)


def model_repository_name_callback(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    if value:
        ctx.obj["repository"] = value
    return value


def model_repository_name_prompter(
    ctx: click.Context,
    param: click.Parameter,
    value: str,
) -> str:
    model_repositories = list_model_repositories()
    if len(model_repositories) == 0:
        raise click.UsageError(
            message="Create model repository with `vessl model-repository create`"
        )
    repository = prompt_choices(
        "Model repository", [x.name for x in model_repositories]
    )
    ctx.obj["repository"] = repository
    return repository


@click.command(name="model-repository", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=model_repository_name_prompter
)
@organization_name_option
def read(name: str):
    model_repository = read_model_repository(repository_name=name)
    print_data(
        {
            "ID": model_repository.id,
            "Name": model_repository.name,
            "Description": model_repository.description,
            "Status": model_repository_status(
                model_repository.model_summary.latest_model
            ),
            "Organization": model_repository.organization.name,
            "Created": truncate_datetime(model_repository.created_dt),
            "Updated": truncate_datetime(model_repository.updated_dt),
        }
    )
    print(
        f"For more info: {format_url(Endpoint.model_repository.format(model_repository.organization.name, model_repository.name))}"
    )


@cli.vessl_command()
@organization_name_option
def list():
    model_repositories = list_model_repositories()
    print_table(
        model_repositories,
        ["Name", "Status", "Models", "Created", "Updated"],
        lambda x: [
            x.name,
            model_repository_status(x.model_summary.latest_model),
            x.model_summary.total,
            truncate_datetime(x.created_dt),
            model_repository_update_dt(x.model_summary.latest_model, x.updated_dt),
        ],
    )


@cli.vessl_command()
@vessl_argument(
    "name",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Model repository name"),
)
@click.option("-m", "--description", type=click.STRING)
@organization_name_option
def create(
    name: str,
    description: str,
):
    model_repository = create_model_repository(
        name=name,
        description=description,
    )
    print(
        f"Created '{model_repository.name}'.\n"
        f"For more info: {format_url(Endpoint.model_repository.format(model_repository.organization.name, model_repository.name))}"
    )

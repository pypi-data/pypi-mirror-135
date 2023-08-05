import os
from pathlib import Path
from typing import Optional

import click

from vessl import list_ssh_keys
from vessl.cli._base import VesslGroup, vessl_option
from vessl.cli._util import prompt_choices
from vessl.cli.organization import organization_name_option
from vessl.util.constant import SSH_CONFIG_PATH
from vessl.workspace import (
    backup_workspace,
    connect_workspace_ssh,
    list_workspaces,
    restore_workspace,
    update_vscode_remote_ssh,
)


def ssh_private_key_path_callback(
    ctx: click.Context, param: click.Parameter, key_path: str
) -> Optional[str]:
    if key_path:
        return key_path

    ssh_keys = list_ssh_keys()
    if len(ssh_keys) == 0:
        raise click.BadParameter(
            "At least one ssh public key should be added.\n"
            "Please run `vessl ssh-key add`."
        )

    home = Path.home()
    for ssh_key in ssh_keys:
        key_path = os.path.join(Path.home(), ".ssh", ssh_key.filename.rstrip(".pub"))
        if os.path.exists(key_path):
            return key_path

    for key_path in (
        os.path.join(Path.home(), ".ssh", "id_rsa"),
        os.path.join(Path.home(), ".ssh", "id_ed25519"),
    ):
        if os.path.exists(key_path):
            return key_path

    return None


def workspace_id_prompter(
    ctx: click.Context, param: click.Parameter, value: int
) -> int:
    workspaces = list_workspaces()
    return prompt_choices("Workspace", [(x.name, x.id) for x in workspaces])


@click.command(name="workspace", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command()
@vessl_option(
    "-p",
    "--key-path",
    type=click.Path(exists=True),
    callback=ssh_private_key_path_callback,
    help="Path to SSH private key.",
)
@organization_name_option
def ssh(key_path: str):
    connect_workspace_ssh(private_key_path=key_path)


@cli.vessl_command()
@vessl_option(
    "-p",
    "--key-path",
    type=click.STRING,
    callback=ssh_private_key_path_callback,
    help="SSH private key path.",
)
@organization_name_option
def vscode(key_path: str):
    update_vscode_remote_ssh(private_key_path=key_path)
    print(f"Updated '{SSH_CONFIG_PATH}'.")


@cli.vessl_command()
@organization_name_option
def backup():
    backup_workspace()


@cli.vessl_command()
@vessl_option(
    "--workspace-id",
    type=click.INT,
    help="Workspace id to restore.",
)
@organization_name_option
def restore(workspace_id: int):
    restore_workspace(workspace_id)

import os
from typing import List

from openapi_client.models import ResponseSSHKeyInfo
from openapi_client.models.ssh_key_create_api_payload import SSHKeyCreateAPIPayload
from vessl import vessl_api


def list_ssh_keys() -> List[ResponseSSHKeyInfo]:
    return vessl_api.s_sh_key_list_api().ssh_keys


def create_ssh_key(
    key_path: str, key_name: str, ssh_public_key_value: str
) -> ResponseSSHKeyInfo:
    return vessl_api.s_sh_key_create_api(
        ssh_key_create_api_payload=SSHKeyCreateAPIPayload(
            filename=os.path.basename(key_path),
            name=key_name,
            public_key=ssh_public_key_value,
        )
    )


def delete_ssh_key(key_id: int) -> object:
    return vessl_api.s_sh_key_delete_api(ssh_key_id=key_id)

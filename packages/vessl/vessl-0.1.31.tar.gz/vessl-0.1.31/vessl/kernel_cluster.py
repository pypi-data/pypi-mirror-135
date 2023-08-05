from typing import List

from openapi_client.models import (
    ClusterUpdateAPIPayload,
    ResponseKernelClusterNodeInfo,
    ResponseKernelClusterInfo,
)
from vessl import vessl_api
from vessl.organization import _get_organization_name
from vessl.util.exception import InvalidKernelClusterError


def read_cluster(cluster_name: str, **kwargs) -> ResponseKernelClusterInfo:
    """Read cluster

    Keyword args:
        organization_name (str): override default organization
    """
    kernel_clusters = list_clusters(**kwargs)
    kernel_clusters = {x.name: x for x in kernel_clusters}

    if cluster_name not in kernel_clusters:
        raise InvalidKernelClusterError(f"Kernel cluster not found: {cluster_name}")
    return kernel_clusters[cluster_name]


def list_clusters(**kwargs) -> List[ResponseKernelClusterInfo]:
    """List clusters

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.cluster_list_api(
        organization_name=_get_organization_name(**kwargs),
    ).clusters


def delete_cluster(cluster_id: int, **kwargs) -> object:
    """Delete custom cluster

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.custom_cluster_delete_api(
        cluster_id=cluster_id,
        organization_name=_get_organization_name(**kwargs),
    )


def rename_cluster(
    cluster_id: int, new_cluster_name: str, **kwargs
) -> ResponseKernelClusterInfo:
    """Rename custom cluster

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.custom_cluster_update_api(
        cluster_id=cluster_id,
        organization_name=_get_organization_name(**kwargs),
        custom_cluster_update_api_payload=ClusterUpdateAPIPayload(
            name=new_cluster_name,
        ),
    )


def list_cluster_nodes(
    cluster_id: int, **kwargs
) -> List[ResponseKernelClusterNodeInfo]:
    """List custom cluster nodes

    Keyword args:
        organization_name (str): override default organization
    """
    return vessl_api.custom_cluster_node_list_api(
        cluster_id=cluster_id,
        organization_name=_get_organization_name(**kwargs),
    ).nodes

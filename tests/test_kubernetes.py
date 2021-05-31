import pytest

from dolib.client import AsyncClient, Client
from dolib.models import K8SCluster


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_kubernetes(client: Client) -> None:
    cluster = K8SCluster(
        name="dolib-test-cluster",
        region="fra1",
        version="1.20.2-do.0",
        node_pools=[
            K8SCluster.Pool(
                name="test-nodes",
                count=1,
                size="s-1vcpu-2gb",
            )
        ],
    )

    # create cluster
    created_cluster = client.kubernetes.create(cluster)
    assert isinstance(created_cluster, K8SCluster)
    assert created_cluster.id is not None

    # list kubernetes
    kubernetes = client.kubernetes.all()
    assert len(kubernetes) > 0
    assert isinstance(kubernetes[0], K8SCluster)

    # read cluster
    read_cluster = client.kubernetes.get(str(created_cluster.id))
    assert read_cluster.id == created_cluster.id
    assert isinstance(read_cluster, K8SCluster)

    # update cluster
    read_cluster.name = "dolib-test-cluster-renamed"
    updated_cluster = client.kubernetes.update(read_cluster)
    assert updated_cluster.name == read_cluster.name

    pool = K8SCluster.Pool(
        name="test-nodes2",
        count=1,
        size="s-1vcpu-2gb",
    )

    # add node pool
    added_pool = client.kubernetes.add_node_pool(str(created_cluster.id), pool)
    assert isinstance(added_pool, K8SCluster.Pool)

    # read node pool
    read_pool = client.kubernetes.get_node_pool(
        str(created_cluster.id), str(added_pool.id)
    )
    assert isinstance(read_pool, K8SCluster.Pool)

    # update node pool
    read_pool.name = "test-nodes2-renamed"
    updated_pool = client.kubernetes.update_node_pool(
        str(created_cluster.id), read_pool
    )
    assert isinstance(updated_pool, K8SCluster.Pool)

    # list node pools
    pools = client.kubernetes.node_pools(str(created_cluster.id))
    assert len(pools) > 0

    # delete node pool
    client.kubernetes.delete_node_pool(str(created_cluster.id), read_pool)

    # get kubeconfig
    config = client.kubernetes.kubeconfig(str(created_cluster.id))
    assert isinstance(config, bytes)

    credentials = client.kubernetes.credentials(str(created_cluster.id))
    assert isinstance(credentials, dict)

    options = client.kubernetes.options()
    assert isinstance(options, dict)

    # add registry
    client.kubernetes.add_registry(cluster_uuids=[str(created_cluster.id)])

    # delete registry
    client.kubernetes.delete_registry(cluster_uuids=[str(created_cluster.id)])

    # delete cluster
    client.kubernetes.delete(cluster=created_cluster)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_kubernetes(async_client: AsyncClient) -> None:
    cluster = K8SCluster(
        name="dolib-test-cluster",
        region="fra1",
        version="1.20.2-do.0",
        node_pools=[
            K8SCluster.Pool(
                name="test-nodes",
                count=1,
                size="s-1vcpu-2gb",
            )
        ],
    )

    # create cluster
    created_cluster = await async_client.kubernetes.create(cluster)
    assert isinstance(created_cluster, K8SCluster)
    assert created_cluster.id is not None

    # list kubernetes
    kubernetes = await async_client.kubernetes.all()
    assert len(kubernetes) > 0
    assert isinstance(kubernetes[0], K8SCluster)

    # read cluster
    read_cluster = await async_client.kubernetes.get(str(created_cluster.id))
    assert read_cluster.id == created_cluster.id
    assert isinstance(read_cluster, K8SCluster)

    # update cluster
    read_cluster.name = "dolib-test-cluster-renamed"
    updated_cluster = await async_client.kubernetes.update(read_cluster)
    assert updated_cluster.name == read_cluster.name

    pool = K8SCluster.Pool(
        name="test-nodes2",
        count=1,
        size="s-1vcpu-2gb",
    )

    # add node pool
    added_pool = await async_client.kubernetes.add_node_pool(
        str(created_cluster.id), pool
    )
    assert isinstance(added_pool, K8SCluster.Pool)

    # read node pool
    read_pool = await async_client.kubernetes.get_node_pool(
        str(created_cluster.id), str(added_pool.id)
    )
    assert isinstance(read_pool, K8SCluster.Pool)

    # update node pool
    read_pool.name = "test-nodes2-renamed"
    updated_pool = await async_client.kubernetes.update_node_pool(
        str(created_cluster.id), read_pool
    )
    assert isinstance(updated_pool, K8SCluster.Pool)

    # list node pools
    pools = await async_client.kubernetes.node_pools(str(created_cluster.id))
    assert len(pools) > 0

    # delete node pool
    await async_client.kubernetes.delete_node_pool(str(created_cluster.id), read_pool)

    # get kubeconfig
    config = await async_client.kubernetes.kubeconfig(str(created_cluster.id))
    assert isinstance(config, bytes)

    credentials = await async_client.kubernetes.credentials(str(created_cluster.id))
    assert isinstance(credentials, dict)

    options = await async_client.kubernetes.options()
    assert isinstance(options, dict)

    # add registry
    await async_client.kubernetes.add_registry(cluster_uuids=[str(created_cluster.id)])

    # delete registry
    await async_client.kubernetes.delete_registry(
        cluster_uuids=[str(created_cluster.id)]
    )

    # delete cluster
    await async_client.kubernetes.delete(cluster=created_cluster)

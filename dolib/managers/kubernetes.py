from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class KubernetesManager(BaseManager):
    endpoint = "kubernetes"
    name = "kubernetes"

    def all(self) -> List[models.K8SCluster]:
        res = self._client.fetch_all(
            endpoint="kubernetes/clusters", key="kubernetes_clusters"
        )
        return [models.K8SCluster(**cluster) for cluster in res]

    def get(self, id: str) -> models.K8SCluster:
        res = self._client.request(
            endpoint="kubernetes/clusters/{id}".format(id=id), method="get"
        )
        return models.K8SCluster(**res["kubernetes_cluster"])

    def create(self, cluster: models.K8SCluster) -> models.K8SCluster:
        res = self._client.request(
            endpoint="kubernetes/clusters",
            method="post",
            data=cluster.json(
                include={
                    "name",
                    "region",
                    "version",
                    "auto_upgrade",
                    "tags",
                    "maintenance_policy",
                    "node_pools",
                    "vpc_uuid",
                }
            ),
        )
        return models.K8SCluster(**res["kubernetes_cluster"])

    def update(self, cluster: models.K8SCluster) -> models.K8SCluster:
        self._client.request(
            endpoint="kubernetes/clusters/{id}".format(id=cluster.id),
            method="put",
            data=cluster.json(
                include={"name", "auto_upgrade", "tags", "maintenance_policy"}
            ),
        )
        # DO api method return nothing
        return cluster
        # return models.K8SCluster(**res["kubernetes_cluster"])

    def delete(self, cluster: models.K8SCluster) -> None:
        self._client.request(
            endpoint="kubernetes/clusters/{id}".format(id=cluster.id), method="delete"
        )

    def node_pools(self, id: str) -> List[models.K8SCluster.Pool]:
        res = self._client.fetch_all(
            endpoint="kubernetes/clusters/{id}/node_pools".format(id=id),
            key="node_pools",
        )
        return [models.K8SCluster.Pool(**pool) for pool in res]

    def add_node_pool(
        self, id: str, pool: models.K8SCluster.Pool
    ) -> models.K8SCluster.Pool:

        res = self._client.request(
            endpoint="kubernetes/clusters/{id}/node_pools".format(id=id),
            method="post",
            data=pool.json(
                include={
                    "size",
                    "name",
                    "count",
                    "labels",
                    "auto_scale",
                    "min_nodes",
                    "max_nodes",
                }
            ),
        )
        return models.K8SCluster.Pool(**res["node_pool"])

    def get_node_pool(self, id: str, pool_id: str) -> models.K8SCluster.Pool:
        res = self._client.request(
            endpoint="kubernetes/clusters/{id}/node_pools/{pool_id}".format(
                id=id, pool_id=pool_id
            ),
            method="get",
        )
        return models.K8SCluster.Pool(**res["node_pool"])

    def update_node_pool(
        self, id: str, pool: models.K8SCluster.Pool
    ) -> models.K8SCluster.Pool:
        self._client.request(
            endpoint="kubernetes/clusters/{id}/node_pools/{pool_id}".format(
                id=id, pool_id=pool.id
            ),
            method="put",
            data=pool.json(
                include={
                    "name",
                    "count",
                    "labels",
                    "auto_scale",
                    "min_nodes",
                    "max_nodes",
                }
            ),
        )
        # DO api method return nothing
        return pool
        # return models.K8SCluster.Pool(**res["node_pool"])

    def delete_node_pool(self, id: str, pool: models.K8SCluster.Pool) -> None:
        self._client.request(
            endpoint="kubernetes/clusters/{id}/node_pools/{pool_id}".format(
                id=id, pool_id=pool.id
            ),
            method="delete",
        )

    def kubeconfig(self, id: str) -> bytes:
        res = self._client.request_raw(
            endpoint="kubernetes/clusters/{id}/kubeconfig".format(id=id), method="get"
        )
        return res.content

    def credentials(self, id: str) -> dict:
        res = self._client.request(
            endpoint="kubernetes/clusters/{id}/credentials".format(id=id), method="get"
        )
        return res

    def options(self) -> dict:
        res = self._client.request(endpoint="kubernetes/options", method="get")
        return res["options"]

    def add_registry(self) -> None:
        self._client.request(
            endpoint="kubernetes/registry",
            method="post",
        )

    def delete_registry(self) -> None:
        self._client.request(
            endpoint="kubernetes/registry",
            method="delete",
        )


class AsyncKubernetesManager(AsyncBaseManager):
    endpoint = "kubernetes"
    name = "kubernetes"

    async def all(self) -> List[models.K8SCluster]:
        res = await self._client.fetch_all(
            endpoint="kubernetes/clusters", key="kubernetes_clusters"
        )
        return [models.K8SCluster(**cluster) for cluster in res]

    async def get(self, id: str) -> models.K8SCluster:
        res = await self._client.request(
            endpoint="kubernetes/clusters/{id}".format(id=id), method="get"
        )
        return models.K8SCluster(**res["kubernetes_cluster"])

    async def create(self, cluster: models.K8SCluster) -> models.K8SCluster:
        res = await self._client.request(
            endpoint="kubernetes/clusters",
            method="post",
            data=cluster.json(
                include={
                    "name",
                    "region",
                    "version",
                    "auto_upgrade",
                    "tags",
                    "maintenance_policy",
                    "node_pools",
                    "vpc_uuid",
                }
            ),
        )
        return models.K8SCluster(**res["kubernetes_cluster"])

    async def update(self, cluster: models.K8SCluster) -> models.K8SCluster:
        await self._client.request(
            endpoint="kubernetes/clusters/{id}".format(id=cluster.id),
            method="put",
            data=cluster.json(
                include={"name", "auto_upgrade", "tags", "maintenance_policy"}
            ),
        )
        # DO api method return nothing
        return cluster
        # return models.K8SCluster(**res["kubernetes_cluster"])

    async def delete(self, cluster: models.K8SCluster) -> None:
        await self._client.request(
            endpoint="kubernetes/clusters/{id}".format(id=cluster.id), method="delete"
        )

    async def node_pools(self, id: str) -> List[models.K8SCluster.Pool]:
        res = await self._client.fetch_all(
            endpoint="kubernetes/clusters/{id}/node_pools".format(id=id),
            key="node_pools",
        )
        return [models.K8SCluster.Pool(**pool) for pool in res]

    async def add_node_pool(
        self, id: str, pool: models.K8SCluster.Pool
    ) -> models.K8SCluster.Pool:

        res = await self._client.request(
            endpoint="kubernetes/clusters/{id}/node_pools".format(id=id),
            method="post",
            data=pool.json(
                include={
                    "size",
                    "name",
                    "count",
                    "labels",
                    "auto_scale",
                    "min_nodes",
                    "max_nodes",
                }
            ),
        )
        return models.K8SCluster.Pool(**res["node_pool"])

    async def get_node_pool(self, id: str, pool_id: str) -> models.K8SCluster.Pool:
        res = await self._client.request(
            endpoint="kubernetes/clusters/{id}/node_pools/{pool_id}".format(
                id=id, pool_id=pool_id
            ),
            method="get",
        )
        return models.K8SCluster.Pool(**res["node_pool"])

    async def update_node_pool(
        self, id: str, pool: models.K8SCluster.Pool
    ) -> models.K8SCluster.Pool:
        await self._client.request(
            endpoint="kubernetes/clusters/{id}/node_pools/{pool_id}".format(
                id=id, pool_id=pool.id
            ),
            method="put",
            data=pool.json(
                include={
                    "name",
                    "count",
                    "labels",
                    "auto_scale",
                    "min_nodes",
                    "max_nodes",
                }
            ),
        )
        # DO api method return nothing
        return pool
        # return models.K8SCluster.Pool(**res["node_pool"])

    async def delete_node_pool(self, id: str, pool: models.K8SCluster.Pool) -> None:
        await self._client.request(
            endpoint="kubernetes/clusters/{id}/node_pools/{pool_id}".format(
                id=id, pool_id=pool.id
            ),
            method="delete",
        )

    async def kubeconfig(self, id: str) -> bytes:
        res = await self._client.request_raw(
            endpoint="kubernetes/clusters/{id}/kubeconfig".format(id=id), method="get"
        )
        return res.content

    async def credentials(self, id: str) -> dict:
        res = await self._client.request(
            endpoint="kubernetes/clusters/{id}/credentials".format(id=id), method="get"
        )
        return res

    async def options(self) -> dict:
        res = await self._client.request(endpoint="kubernetes/options", method="get")
        return res["options"]

    async def add_registry(self) -> None:
        await self._client.request(
            endpoint="kubernetes/registry",
            method="post",
        )

    async def delete_registry(self) -> None:
        await self._client.request(
            endpoint="kubernetes/registry",
            method="delete",
        )

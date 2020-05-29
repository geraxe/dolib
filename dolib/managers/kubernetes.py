from typing import List

from .. import models
from .base import BaseManager


class KubernetesManager(BaseManager):
    endpoint = "kubernetes"
    name = "kubernetes"

    def all(self) -> List[models.K8SCluster]:
        res = self._client.fetch_all(
            endpoint="kubernetes/clusters", key="kubernetes_clusters"
        )
        return [models.K8SCluster(**cluster) for cluster in res]

    def get(self, id: str = None) -> models.K8SCluster:
        assert id is not None, "id must be set"
        res = self._client.request(
            endpoint="kubernetes/clusters/{id}".format(id=id), method="get"
        )
        return models.K8SCluster(**res["kubernetes_cluster"])

    def create(self, cluster: models.K8SCluster = None):
        assert cluster is not None, "kubernetes cluster object must be set"

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

    def update(self, cluster: models.K8SCluster = None):
        assert cluster is not None, "cluster object must be set"
        self._client.request(
            endpoint="kubernetes/clusters/{id}".format(id=cluster.id),
            method="put",
            data=cluster.json(
                include={"name", "auto_upgrade", "tags", "maintenance_policy"}
            ),
        )
        # DO api method not return anything
        return cluster
        # return models.K8SCluster(**res["kubernetes_cluster"])

    def delete(self, cluster: models.K8SCluster = None):
        assert cluster is not None, "cluster object must be set"

        self._client.request(
            endpoint="kubernetes/clusters/{id}".format(id=cluster.id), method="delete"
        )

    def node_pools(self, id: str = None) -> List[models.K8SCluster.Pool]:
        assert id is not None, "cluster id must be set"
        res = self._client.fetch_all(
            endpoint="kubernetes/clusters/{id}/node_pools".format(id=id),
            key="node_pools",
        )
        return [models.K8SCluster.Pool(**pool) for pool in res]

    def add_node_pool(
        self, id: str = None, pool: models.K8SCluster.Pool = None
    ) -> models.K8SCluster.Pool:
        assert id is not None, "cluster id must be set"
        assert pool is not None, "pool must be set"

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

    def get_node_pool(
        self, id: str = None, pool_id: str = None
    ) -> models.K8SCluster.Pool:
        assert id is not None, "cluster id must be set"
        assert pool_id is not None, "pool_id name must be set"

        res = self._client.request(
            endpoint="kubernetes/clusters/{id}/node_pools/{pool_id}".format(
                id=id, pool_id=pool_id
            ),
            method="get",
        )
        return models.K8SCluster.Pool(**res["node_pool"])

    def update_node_pool(
        self, id: str = None, pool: models.K8SCluster.Pool = None
    ) -> models.K8SCluster.Pool:
        assert id is not None, "cluster id must be set"
        assert pool is not None, "pool must be set"

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
        # DO api method not return anything
        return pool
        # return models.K8SCluster.Pool(**res["node_pool"])

    def delete_node_pool(self, id: str = None, pool: models.K8SCluster.Pool = None):
        assert id is not None, "database cluster id must be set"
        assert pool is not None, "pool must be set"

        self._client.request(
            endpoint="kubernetes/clusters/{id}/node_pools/{pool_id}".format(
                id=id, pool_id=pool.id
            ),
            method="delete",
        )

    def kubeconfig(self, id: str = None) -> bytes:
        assert id is not None, "cluster id must be set"
        res = self._client.request_raw(
            endpoint="kubernetes/clusters/{id}/kubeconfig".format(id=id), method="get"
        )
        return res.content

    def credentials(self, id: str = None) -> bytes:
        assert id is not None, "cluster id must be set"
        res = self._client.request(
            endpoint="kubernetes/clusters/{id}/credentials".format(id=id), method="get"
        )
        return res

    def options(self):
        res = self._client.request(endpoint="kubernetes/options", method="get")
        return res["options"]

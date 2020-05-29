from typing import List

from .. import models
from .base import BaseManager


class DatabasesManager(BaseManager):
    endpoint = "databases"
    name = "databases"

    def all(self) -> List[models.DBCluster]:
        res = self._client.fetch_all(endpoint="databases", key="databases")
        return [models.DBCluster(**db) for db in res]

    def filter(self, tag_name: str = None) -> List[models.DBCluster]:
        params = {}
        if tag_name is not None:
            params["tag_name"] = tag_name
        res = self._client.fetch_all(
            endpoint="databases", key="databases", params=params,
        )
        return [models.DBCluster(**db) for db in res]

    def get(self, id: str = None) -> models.DBCluster:
        assert id is not None, "id must be set"
        res = self._client.request(
            endpoint="databases/{id}".format(id=id), method="get"
        )
        return models.DBCluster(**res["database"])

    def create(self, database: models.DBCluster = None):
        assert database is not None, "database object must be set"

        res = self._client.request(
            endpoint="databases",
            method="post",
            data=database.json(
                include={
                    "name",
                    "engine",
                    "version",
                    "size",
                    "region",
                    "num_nodes",
                    "tags",
                    "private_network_uuid",
                }
            ),
        )
        return models.DBCluster(**res["database"])

    def delete(self, database: models.DBCluster = None):
        assert database is not None, "database cluster object must be set"

        self._client.request(
            endpoint="databases/{id}".format(id=database.id), method="delete"
        )

    def replicas(self, id: str = None) -> List[models.DBReplica]:
        assert id is not None, "database cluster id must be set"
        res = self._client.fetch_all(
            endpoint="databases/{id}/replicas".format(id=id), key="replicas",
        )
        return [models.DBReplica(**replica) for replica in res]

    def add_replica(
        self, id: str = None, replica: models.DBReplica = None
    ) -> models.DBReplica:
        assert id is not None, "database cluster id must be set"
        assert replica is not None, "replica must be set"
        res = self._client.request(
            endpoint="databases/{id}/replicas".format(id=id),
            method="post",
            data=replica.json(
                include={"name", "region", "size", "tags", "private_network_uuid"}
            ),
        )
        return models.DBReplica(**res["replica"])

    def get_replica(self, id: str = None, name: str = None) -> models.DBReplica:
        assert id is not None, "database cluster id must be set"
        assert name is not None, "replica name must be set"

        res = self._client.request(
            endpoint="databases/{id}/replicas/{name}".format(id=id, name=name),
            method="get",
        )
        return models.DBReplica(**res["replica"])

    def delete_replica(self, id: str = None, replica: models.DBReplica = None):
        assert id is not None, "database cluster id must be set"
        assert replica is not None, "replica must be set"

        self._client.request(
            endpoint="databases/{id}/replicas/{name}".format(id=id, name=replica.name),
            method="delete",
        )

    def users(self, id: str = None) -> List[models.DBCluster.User]:
        assert id is not None, "database cluster id must be set"
        res = self._client.fetch_all(
            endpoint="databases/{id}/users".format(id=id), key="users",
        )
        return [models.DBCluster.User(**user) for user in res]

    def add_user(
        self, id: str = None, user: models.DBCluster.User = None
    ) -> models.DBCluster.User:
        assert id is not None, "database cluster id must be set"
        assert user is not None, "user must be set"
        res = self._client.request(
            endpoint="databases/{id}/users".format(id=id),
            method="post",
            data=user.json(include={"name", "mysql_settings"}),
        )
        return models.DBCluster.User(**res["user"])

    def get_user(self, id: str = None, name: str = None) -> models.DBCluster.User:
        assert id is not None, "database cluster id must be set"
        assert name is not None, "user name must be set"

        res = self._client.request(
            endpoint="databases/{id}/users/{name}".format(id=id, name=name),
            method="get",
        )
        return models.DBCluster.User(**res["user"])

    def delete_user(self, id: str = None, user: models.DBCluster.User = None):
        assert id is not None, "database cluster id must be set"
        assert user is not None, "user must be set"

        self._client.request(
            endpoint="databases/{id}/users/{name}".format(id=id, name=user.name),
            method="delete",
        )

    def dbs(self, id: str = None) -> List[models.DBCluster.DB]:
        assert id is not None, "database cluster id must be set"
        res = self._client.fetch_all(
            endpoint="databases/{id}/dbs".format(id=id), key="dbs",
        )
        return [models.DBCluster.DB(**db) for db in res]

    def add_db(
        self, id: str = None, db: models.DBCluster.DB = None
    ) -> models.DBCluster.DB:
        assert id is not None, "database cluster id must be set"
        assert db is not None, "db must be set"
        res = self._client.request(
            endpoint="databases/{id}/dbs".format(id=id), method="post", data=db.json()
        )
        return models.DBCluster.DB(**res["db"])

    def get_db(self, id: str = None, name: str = None) -> models.DBCluster.DB:
        assert id is not None, "database cluster id must be set"
        assert name is not None, "db name must be set"

        res = self._client.request(
            endpoint="databases/{id}/dbs/{name}".format(id=id, name=name), method="get"
        )
        return models.DBCluster.DB(**res["db"])

    def delete_db(self, id: str = None, db: models.DBCluster.DB = None):
        assert id is not None, "database cluster id must be set"
        assert db is not None, "db must be set"

        self._client.request(
            endpoint="databases/{id}/dbs/{name}".format(id=id, name=db.name),
            method="delete",
        )

    # Actions
    def resize(self, id: str = None, size: str = None, num_nodes: int = None):
        assert id is not None, "database cluster id must be set"
        assert size is not None, "size must be set"
        assert num_nodes is not None, "num_nodes must be set"

        self._client.request(
            endpoint="databases/{id}/resize".format(id=id),
            method="put",
            json={"size": size, "num_nodes": num_nodes},
        )

    def migrate(self, id: str = None, region: str = None):
        assert id is not None, "droplet id must be set"
        assert region is not None, "region must be set"

        self._client.request(
            endpoint="databases/{id}/migrate".format(id=id),
            method="post",
            json={"region": region},
        )

from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


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
            endpoint="databases",
            key="databases",
            params=params,
        )
        return [models.DBCluster(**db) for db in res]

    def get(self, id: str) -> models.DBCluster:
        res = self._client.request(
            endpoint="databases/{id}".format(id=id), method="get"
        )
        return models.DBCluster(**res["database"])

    def create(self, database: models.DBCluster) -> models.DBCluster:
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

    def delete(self, database: models.DBCluster) -> None:
        self._client.request(
            endpoint="databases/{id}".format(id=database.id), method="delete"
        )

    def replicas(self, id: str) -> List[models.DBReplica]:
        res = self._client.fetch_all(
            endpoint="databases/{id}/replicas".format(id=id),
            key="replicas",
        )
        return [models.DBReplica(**replica) for replica in res]

    def add_replica(self, id: str, replica: models.DBReplica) -> models.DBReplica:
        res = self._client.request(
            endpoint="databases/{id}/replicas".format(id=id),
            method="post",
            data=replica.json(
                include={"name", "region", "size", "tags", "private_network_uuid"}
            ),
        )
        return models.DBReplica(**res["replica"])

    def get_replica(self, id: str, name: str) -> models.DBReplica:
        res = self._client.request(
            endpoint="databases/{id}/replicas/{name}".format(id=id, name=name),
            method="get",
        )
        return models.DBReplica(**res["replica"])

    def delete_replica(self, id: str, replica: models.DBReplica) -> None:
        self._client.request(
            endpoint="databases/{id}/replicas/{name}".format(id=id, name=replica.name),
            method="delete",
        )

    def users(self, id: str) -> List[models.DBCluster.User]:
        res = self._client.fetch_all(
            endpoint="databases/{id}/users".format(id=id),
            key="users",
        )
        return [models.DBCluster.User(**user) for user in res]

    def add_user(self, id: str, user: models.DBCluster.User) -> models.DBCluster.User:
        res = self._client.request(
            endpoint="databases/{id}/users".format(id=id),
            method="post",
            data=user.json(include={"name", "mysql_settings"}),
        )
        return models.DBCluster.User(**res["user"])

    def get_user(self, id: str, name: str) -> models.DBCluster.User:
        res = self._client.request(
            endpoint="databases/{id}/users/{name}".format(id=id, name=name),
            method="get",
        )
        return models.DBCluster.User(**res["user"])

    def delete_user(self, id: str, user: models.DBCluster.User) -> None:
        self._client.request(
            endpoint="databases/{id}/users/{name}".format(id=id, name=user.name),
            method="delete",
        )

    def dbs(self, id: str) -> List[models.DBCluster.DB]:
        res = self._client.fetch_all(
            endpoint="databases/{id}/dbs".format(id=id),
            key="dbs",
        )
        return [models.DBCluster.DB(**db) for db in res]

    def add_db(self, id: str, db: models.DBCluster.DB) -> models.DBCluster.DB:
        res = self._client.request(
            endpoint="databases/{id}/dbs".format(id=id), method="post", data=db.json()
        )
        return models.DBCluster.DB(**res["db"])

    def get_db(self, id: str, name: str) -> models.DBCluster.DB:
        res = self._client.request(
            endpoint="databases/{id}/dbs/{name}".format(id=id, name=name), method="get"
        )
        return models.DBCluster.DB(**res["db"])

    def delete_db(self, id: str, db: models.DBCluster.DB) -> None:
        self._client.request(
            endpoint="databases/{id}/dbs/{name}".format(id=id, name=db.name),
            method="delete",
        )

    # Actions
    def resize(self, id: str, size: str, num_nodes: int) -> None:
        self._client.request(
            endpoint="databases/{id}/resize".format(id=id),
            method="put",
            json={"size": size, "num_nodes": num_nodes},
        )

    def migrate(self, id: str, region: str) -> None:
        self._client.request(
            endpoint="databases/{id}/migrate".format(id=id),
            method="post",
            json={"region": region},
        )


class AsyncDatabasesManager(AsyncBaseManager):
    endpoint = "databases"
    name = "databases"

    async def all(self) -> List[models.DBCluster]:
        res = await self._client.fetch_all(endpoint="databases", key="databases")
        return [models.DBCluster(**db) for db in res]

    async def filter(self, tag_name: str = None) -> List[models.DBCluster]:
        params = {}
        if tag_name is not None:
            params["tag_name"] = tag_name
        res = await self._client.fetch_all(
            endpoint="databases",
            key="databases",
            params=params,
        )
        return [models.DBCluster(**db) for db in res]

    async def get(self, id: str) -> models.DBCluster:
        res = await self._client.request(
            endpoint="databases/{id}".format(id=id), method="get"
        )
        return models.DBCluster(**res["database"])

    async def create(self, database: models.DBCluster) -> models.DBCluster:
        res = await self._client.request(
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

    async def delete(self, database: models.DBCluster) -> None:
        await self._client.request(
            endpoint="databases/{id}".format(id=database.id), method="delete"
        )

    async def replicas(self, id: str) -> List[models.DBReplica]:
        res = await self._client.fetch_all(
            endpoint="databases/{id}/replicas".format(id=id),
            key="replicas",
        )
        return [models.DBReplica(**replica) for replica in res]

    async def add_replica(self, id: str, replica: models.DBReplica) -> models.DBReplica:
        res = await self._client.request(
            endpoint="databases/{id}/replicas".format(id=id),
            method="post",
            data=replica.json(
                include={"name", "region", "size", "tags", "private_network_uuid"}
            ),
        )
        return models.DBReplica(**res["replica"])

    async def get_replica(self, id: str, name: str) -> models.DBReplica:
        res = await self._client.request(
            endpoint="databases/{id}/replicas/{name}".format(id=id, name=name),
            method="get",
        )
        return models.DBReplica(**res["replica"])

    async def delete_replica(self, id: str, replica: models.DBReplica) -> None:
        await self._client.request(
            endpoint="databases/{id}/replicas/{name}".format(id=id, name=replica.name),
            method="delete",
        )

    async def users(self, id: str) -> List[models.DBCluster.User]:
        res = await self._client.fetch_all(
            endpoint="databases/{id}/users".format(id=id),
            key="users",
        )
        return [models.DBCluster.User(**user) for user in res]

    async def add_user(
        self, id: str, user: models.DBCluster.User
    ) -> models.DBCluster.User:
        res = await self._client.request(
            endpoint="databases/{id}/users".format(id=id),
            method="post",
            data=user.json(include={"name", "mysql_settings"}),
        )
        return models.DBCluster.User(**res["user"])

    async def get_user(self, id: str, name: str) -> models.DBCluster.User:
        res = await self._client.request(
            endpoint="databases/{id}/users/{name}".format(id=id, name=name),
            method="get",
        )
        return models.DBCluster.User(**res["user"])

    async def delete_user(self, id: str, user: models.DBCluster.User) -> None:
        await self._client.request(
            endpoint="databases/{id}/users/{name}".format(id=id, name=user.name),
            method="delete",
        )

    async def dbs(self, id: str) -> List[models.DBCluster.DB]:
        res = await self._client.fetch_all(
            endpoint="databases/{id}/dbs".format(id=id),
            key="dbs",
        )
        return [models.DBCluster.DB(**db) for db in res]

    async def add_db(self, id: str, db: models.DBCluster.DB) -> models.DBCluster.DB:
        res = await self._client.request(
            endpoint="databases/{id}/dbs".format(id=id), method="post", data=db.json()
        )
        return models.DBCluster.DB(**res["db"])

    async def get_db(self, id: str, name: str) -> models.DBCluster.DB:
        res = await self._client.request(
            endpoint="databases/{id}/dbs/{name}".format(id=id, name=name), method="get"
        )
        return models.DBCluster.DB(**res["db"])

    async def delete_db(self, id: str, db: models.DBCluster.DB) -> None:
        await self._client.request(
            endpoint="databases/{id}/dbs/{name}".format(id=id, name=db.name),
            method="delete",
        )

    # Actions
    async def resize(self, id: str, size: str, num_nodes: int) -> None:
        await self._client.request(
            endpoint="databases/{id}/resize".format(id=id),
            method="put",
            json={"size": size, "num_nodes": num_nodes},
        )

    async def migrate(self, id: str, region: str) -> None:
        await self._client.request(
            endpoint="databases/{id}/migrate".format(id=id),
            method="post",
            json={"region": region},
        )

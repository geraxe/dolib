from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class SnapshotsManager(BaseManager):
    endpoint = "snapshots"
    name = "snapshots"

    def all(self, resource_type: str) -> List[models.Snapshot]:
        params = dict()
        if resource_type is not None:
            params["resource_type"] = resource_type
        res = self._client.fetch_all(
            endpoint="snapshots", key="snapshots", params=params
        )
        return [models.Snapshot(**snapshot) for snapshot in res]

    def get(self, id: str) -> models.Snapshot:
        res = self._client.request(
            endpoint="snapshots/{id}".format(id=id), method="get"
        )
        return models.Snapshot(**res["snapshot"])

    def delete(self, snapshot: models.Snapshot) -> None:
        self._client.request(
            endpoint="snapshots/{id}".format(id=snapshot.id), method="delete"
        )


class AsyncSnapshotsManager(AsyncBaseManager):
    endpoint = "snapshots"
    name = "snapshots"

    async def all(self, resource_type: str) -> List[models.Snapshot]:
        params = dict()
        if resource_type is not None:
            params["resource_type"] = resource_type
        res = await self._client.fetch_all(
            endpoint="snapshots", key="snapshots", params=params
        )
        return [models.Snapshot(**snapshot) for snapshot in res]

    async def get(self, id: str) -> models.Snapshot:
        res = await self._client.request(
            endpoint="snapshots/{id}".format(id=id), method="get"
        )
        return models.Snapshot(**res["snapshot"])

    async def delete(self, snapshot: models.Snapshot) -> None:
        await self._client.request(
            endpoint="snapshots/{id}".format(id=snapshot.id), method="delete"
        )

from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class VolumesManager(BaseManager):
    endpoint: str = "volumes"
    name: str = "volumes"

    def all(self) -> List[models.Volume]:
        res = self._client.fetch_all(endpoint="volumes", key="volumes")
        return [models.Volume(**volume) for volume in res]

    def get(self, id: str) -> models.Volume:
        res = self._client.request(endpoint="volumes/{id}".format(id=id), method="get")
        return models.Volume(**res["volume"])

    def create(self, volume: models.Volume) -> models.Volume:
        res = self._client.request(
            endpoint="volumes",
            method="post",
            data=volume.json(),
        )
        return models.Volume(**res["volume"])

    def delete(self, volume: models.Volume) -> None:
        self._client.request(
            endpoint="volumes/{id}".format(id=volume.id),
            method="delete",
        )

    def resize(self, id: str, size_gigabytes: int) -> models.Action:
        action = {
            "type": "resize",
            "size_gigabytes": int(size_gigabytes),
        }
        res = self._client.request(
            endpoint="volumes/{id}/actions".format(id=id),
            method="post",
            json=action,
        )
        return models.Action(**res["action"])

    def _droplet_action(
        self, action_type: str, volume: models.Volume, droplet_id: int
    ) -> models.Action:

        action = {
            "type": action_type,
            "droplet_id": droplet_id,
        }
        if volume.region is not None:
            if isinstance(volume.region, str):
                action["region"] = volume.region
            elif isinstance(volume.region, models.Region):
                action["region"] = volume.region.slug

        if volume.id is not None:
            res = self._client.request(
                endpoint="volumes/{id}/actions".format(id=volume.id),
                method="post",
                json=action,
            )
        else:
            action["volume_name"] = volume.name
            res = self._client.request(
                endpoint="volumes/actions", method="post", json=action
            )
        return models.Action(**res["action"])

    def attach(self, volume: models.Volume, droplet_id: int) -> models.Action:
        return self._droplet_action("attach", volume, droplet_id)

    def detach(self, volume: models.Volume, droplet_id: int) -> models.Action:
        return self._droplet_action("detach", volume, droplet_id)

    def snapshots(self, id: str) -> List[models.Snapshot]:
        res = self._client.fetch_all(
            endpoint="volumes/{id}/snapshots".format(id=id), key="snapshots"
        )
        return [models.Snapshot(**snapshot) for snapshot in res]

    def create_snapshot(self, id: str, snapshot: models.Snapshot) -> models.Snapshot:

        res = self._client.request(
            endpoint="volumes/{id}/snapshots".format(id=id),
            method="post",
            data=snapshot.json(include={"name", "tags"}),
        )
        return models.Snapshot(**res["snapshot"])

    def actions(self, id: str) -> List[models.Action]:
        res = self._client.fetch_all(
            endpoint="volumes/{id}/actions".format(id=id), key="actions"
        )
        return [models.Action(**action) for action in res]


class AsyncVolumesManager(AsyncBaseManager):
    endpoint: str = "volumes"
    name: str = "volumes"

    async def all(self) -> List[models.Volume]:
        res = await self._client.fetch_all(endpoint="volumes", key="volumes")
        return [models.Volume(**volume) for volume in res]

    async def get(self, id: str) -> models.Volume:
        res = await self._client.request(
            endpoint="volumes/{id}".format(id=id), method="get"
        )
        return models.Volume(**res["volume"])

    async def create(self, volume: models.Volume) -> models.Volume:
        res = await self._client.request(
            endpoint="volumes",
            method="post",
            data=volume.json(),
        )
        return models.Volume(**res["volume"])

    async def delete(self, volume: models.Volume) -> None:
        await self._client.request(
            endpoint="volumes/{id}".format(id=volume.id),
            method="delete",
        )

    async def resize(self, id: str, size_gigabytes: int) -> models.Action:
        action = {
            "type": "resize",
            "size_gigabytes": int(size_gigabytes),
        }
        res = await self._client.request(
            endpoint="volumes/{id}/actions".format(id=id),
            method="post",
            json=action,
        )
        return models.Action(**res["action"])

    async def _droplet_action(
        self, action_type: str, volume: models.Volume, droplet_id: int
    ) -> models.Action:

        action = {
            "type": action_type,
            "droplet_id": droplet_id,
        }
        if volume.region is not None:
            if isinstance(volume.region, str):
                action["region"] = volume.region
            elif isinstance(volume.region, models.Region):
                action["region"] = volume.region.slug

        if volume.id is not None:
            res = await self._client.request(
                endpoint="volumes/{id}/actions".format(id=volume.id),
                method="post",
                json=action,
            )
        else:
            action["volume_name"] = volume.name
            res = await self._client.request(
                endpoint="volumes/actions", method="post", json=action
            )
        return models.Action(**res["action"])

    async def attach(self, volume: models.Volume, droplet_id: int) -> models.Action:
        return await self._droplet_action("attach", volume, droplet_id)

    async def detach(self, volume: models.Volume, droplet_id: int) -> models.Action:
        return await self._droplet_action("detach", volume, droplet_id)

    async def snapshots(self, id: str) -> List[models.Snapshot]:
        res = await self._client.fetch_all(
            endpoint="volumes/{id}/snapshots".format(id=id), key="snapshots"
        )
        return [models.Snapshot(**snapshot) for snapshot in res]

    async def create_snapshot(
        self, id: str, snapshot: models.Snapshot
    ) -> models.Snapshot:

        res = await self._client.request(
            endpoint="volumes/{id}/snapshots".format(id=id),
            method="post",
            data=snapshot.json(include={"name", "tags"}),
        )
        return models.Snapshot(**res["snapshot"])

    async def actions(self, id: str) -> List[models.Action]:
        res = await self._client.fetch_all(
            endpoint="volumes/{id}/actions".format(id=id), key="actions"
        )
        return [models.Action(**action) for action in res]

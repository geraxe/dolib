from typing import List

from .. import models
from .base import BaseManager


class VolumesManager(BaseManager):
    endpoint: str = "volumes"
    name: str = "volumes"

    def all(self) -> List[models.Volume]:
        volumes = list()
        res = self._client.request(endpoint="volumes", method="get")
        for volume in res["volumes"]:
            volumes.append(models.Volume(**volume))
        return volumes

    def get(self, id: str = None):
        assert id is not None, "id must be set"

        res = self._client.request(endpoint="volumes/{id}".format(id=id), method="get",)
        return models.Volume(**res["volume"])

    def create(self, volume: models.Volume = None):
        assert volume is not None, "volume object must be set"

        res = self._client.request(
            endpoint="volumes", method="post", data=volume.json(),
        )
        return models.Volume(**res["volume"])

    def delete(self, volume: models.Volume = None):
        assert volume is not None, "volume object must be set"

        self._client.request(
            endpoint="volumes/{id}".format(id=volume.id), method="delete",
        )

    def resize(self, id: str = None, size_gigabytes: int = None) -> models.Action:
        assert id is not None, "id must be set"
        assert size_gigabytes is not None, "size_gigabytes must be set"

        action = {
            "type": "resize",
            "size_gigabytes": int(size_gigabytes),
        }
        res = self._client.request(
            endpoint="volumes/{id}/actions".format(id=id), method="post", json=action,
        )
        return models.Action(**res["action"])

    def _droplet_action(
        self, action_type: str, volume: models.Volume, droplet_id: int = None
    ) -> models.Action:
        assert droplet_id is not None, "droplet_id must be set"

        action = {
            "type": action_type,
            "droplet_id": droplet_id,
        }
        if volume.region is not None:
            if type(volume.region) == str:
                action["region"] = volume.region
            elif type(volume.region) == models.Region:
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
                endpoint="volumes/actions", method="post", json=action,
            )
        return models.Action(**res["action"])

    def attach(self, volume: models.Volume, droplet_id: int = None) -> models.Action:
        return self._droplet_action("attach", volume, droplet_id)

    def detach(self, volume: models.Volume, droplet_id: int = None) -> models.Action:
        return self._droplet_action("detach", volume, droplet_id)

    def snapshots(self, id: str = None) -> List[models.Snapshot]:
        assert id is not None, "id must be set"

        snapshots = list()
        res = self._client.request(
            endpoint="volumes/{id}/snapshots".format(id=id), method="get",
        )
        for snapshot in res["snapshots"]:
            snapshots.append(models.Snapshot(**snapshot))
        return snapshots

    def create_snapshot(
        self, id: str = None, snapshot: models.Snapshot = None
    ) -> models.Snapshot:
        assert id is not None, "id must be set"
        assert snapshot is not None, "snapshot must be set"

        res = self._client.request(
            endpoint="volumes/{id}/snapshots".format(id=id),
            method="post",
            data=snapshot.json(include={"name", "tags"}),
        )
        return models.Snapshot(**res["snapshot"])

    def actions(self, id: str = None) -> List[models.Action]:
        assert id is not None, "id must be set"

        actions = list()
        res = self._client.request(
            endpoint="volumes/{id}/actions".format(id=id), method="get",
        )
        for action in res["actions"]:
            actions.append(models.Action(**action))
        return actions

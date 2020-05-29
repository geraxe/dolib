from typing import List

from .. import models
from .base import BaseManager


class SnapshotsManager(BaseManager):
    endpoint = "snapshots"
    name = "snapshots"

    def all(self, resource_type: str = None) -> List[models.Snapshot]:
        assert (
            resource_type is None or type(resource_type) == str
        ), "resource_type must be str type"

        snapshots = list()
        params = dict()
        if resource_type is not None:
            params["resource_type"] = resource_type

        res = self._client.request(endpoint="snapshots", method="get", params=params)
        for snapshot in res["snapshots"]:
            snapshots.append(models.Snapshot(**snapshot))
        return snapshots

    def get(self, id: str = None) -> models.Snapshot:
        assert id is not None, "snapshot id must be set"

        res = self._client.request(
            endpoint="snapshots/{id}".format(id=id), method="get"
        )
        return models.Snapshot(**res["snapshot"])

    def delete(self, snapshot: models.Snapshot = None):
        assert snapshot is not None, "snapshot object must be set"

        self._client.request(
            endpoint="snapshots/{id}".format(id=snapshot.id), method="delete",
        )

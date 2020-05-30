from typing import List

from .. import models
from .base import BaseManager


class ActionsManager(BaseManager):
    endpoint = "actions"
    name = "actions"

    def all(self) -> List[models.Action]:
        res = self._client.request(endpoint="actions", method="get")
        return [models.Action(**action) for action in res["actions"]]

    def get(self, id: str = None) -> models.Action:
        assert id is not None, "id must be set"

        res = self._client.request(endpoint="actions/{id}".format(id=id), method="get",)
        return models.Action(**res["action"])

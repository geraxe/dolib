from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class ActionsManager(BaseManager):
    endpoint = "actions"
    name = "actions"

    def all(self) -> List[models.Action]:
        res = self._client.request(endpoint="actions", method="get")
        return [models.Action(**action) for action in res["actions"]]

    def get(self, id: str) -> models.Action:
        res = self._client.request(
            endpoint="actions/{id}".format(id=id),
            method="get",
        )
        return models.Action(**res["action"])


class AsyncActionsManager(AsyncBaseManager):
    endpoint = "actions"
    name = "actions"

    async def all(self) -> List[models.Action]:
        res = await self._client.request(endpoint="actions", method="get")
        return [models.Action(**action) for action in res["actions"]]

    async def get(self, id: str) -> models.Action:
        res = await self._client.request(
            endpoint="actions/{id}".format(id=id),
            method="get",
        )
        return models.Action(**res["action"])

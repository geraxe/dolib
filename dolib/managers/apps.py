from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class AppsManager(BaseManager):
    endpoint = "apps"
    name = "apps"

    def all(self) -> List[models.App]:
        res = self._client.fetch_all(endpoint="apps", key="apps")
        return [models.App(**app) for app in res]

    def get(self, id: str) -> models.App:
        res = self._client.request(endpoint=f"apps/{id}", method="get")
        return models.App(**res["app"])

    def create(self, app: models.App) -> models.App:
        res = self._client.request(
            endpoint="apps",
            method="post",
            data=app.json(
                include={
                    "spec",
                    "deploy_template",
                }
            ),
        )
        return models.App(**res["app"])


class AsyncAppsManager(AsyncBaseManager):
    endpoint = "apps"
    name = "apps"

    async def all(self) -> List[models.App]:
        res = await self._client.fetch_all(endpoint="apps", key="apps")
        return [models.App(**app) for app in res]

    async def get(self, id: str) -> models.App:
        res = await self._client.request(endpoint=f"apps/{id}", method="get")
        return models.App(**res["app"])

    async def create(self, app: models.App) -> models.App:
        res = await self._client.request(
            endpoint="apps",
            method="post",
            data=app.json(
                include={
                    "spec",
                    "deploy_template",
                }
            ),
        )
        return models.App(**res["app"])

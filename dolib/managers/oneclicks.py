from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class OneClicksManager(BaseManager):
    endpoint = "one_clicks"
    name = "one_clicks"

    def all(self) -> List[models.OneClickApp]:
        res = self._client.fetch_all(endpoint="1-clicks", key="1_clicks")
        return [models.OneClickApp(**app) for app in res]

    def filter(self, app_type: str = None) -> List[models.OneClickApp]:
        params = {}
        if app_type is not None:
            params["type"] = app_type
        res = self._client.fetch_all(
            endpoint="1-clicks",
            key="1_clicks",
            params=params,
        )
        return [models.OneClickApp(**app) for app in res]


class AsyncOneClicksManager(AsyncBaseManager):
    endpoint = "one_clicks"
    name = "one_clicks"

    async def all(self) -> List[models.OneClickApp]:
        res = await self._client.fetch_all(endpoint="1-clicks", key="1_clicks")
        return [models.OneClickApp(**app) for app in res]

    async def filter(self, app_type: str = None) -> List[models.OneClickApp]:
        params = {}
        if app_type is not None:
            params["type"] = app_type
        res = await self._client.fetch_all(
            endpoint="1-clicks",
            key="1_clicks",
            params=params,
        )
        return [models.OneClickApp(**app) for app in res]

from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class RegionsManager(BaseManager):
    endpoint = "regions"
    name = "regions"

    def all(self) -> List[models.Region]:
        res = self._client.fetch_all(endpoint="regions", key="regions")
        return [models.Region(**region) for region in res]


class AsyncRegionsManager(AsyncBaseManager):
    endpoint = "regions"
    name = "regions"

    async def all(self) -> List[models.Region]:
        res = await self._client.fetch_all(endpoint="regions", key="regions")
        return [models.Region(**region) for region in res]

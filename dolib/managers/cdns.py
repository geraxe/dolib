from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class CDNEndpointsManager(BaseManager):
    endpoint = "cdn_endpoints"
    name = "cdn_endpoints"

    def all(self) -> List[models.CDNEndpoint]:
        res = self._client.fetch_all(endpoint="cdn/endpoints", key="endpoints")
        return [models.CDNEndpoint(**endpoint) for endpoint in res]

    def get(self, id: str) -> models.CDNEndpoint:
        res = self._client.request(
            endpoint="cdn/endpoints/{id}".format(id=id), method="get"
        )
        return models.CDNEndpoint(**res["endpoint"])

    def create(self, endpoint: models.CDNEndpoint) -> models.CDNEndpoint:
        res = self._client.request(
            endpoint="cdn/endpoints",
            method="post",
            data=endpoint.json(
                include={"origin", "ttl", "certificate_id", "custom_domain"}
            ),
        )
        return models.CDNEndpoint(**res["endpoint"])

    def update(self, endpoint: models.CDNEndpoint) -> models.CDNEndpoint:
        res = self._client.request(
            endpoint="cdn/endpoints/{id}".format(id=endpoint.id),
            method="put",
            data=endpoint.json(include={"ttl", "certificate_id", "custom_domain"}),
        )
        return models.CDNEndpoint(**res["endpoint"])

    def delete(self, endpoint: models.CDNEndpoint) -> None:
        self._client.request(
            endpoint="cdn/endpoints/{id}".format(id=endpoint.id), method="delete"
        )

    def flush_cache(self, id: str, files: List[str] = None) -> None:
        if files is None:
            files = ["*"]

        self._client.request(
            endpoint="cdn/endpoints/{id}/cache".format(id=id),
            method="delete",
            json={"files": files},
        )


class AsyncCDNEndpointsManager(AsyncBaseManager):
    endpoint = "cdn_endpoints"
    name = "cdn_endpoints"

    async def all(self) -> List[models.CDNEndpoint]:
        res = await self._client.fetch_all(endpoint="cdn/endpoints", key="endpoints")
        return [models.CDNEndpoint(**endpoint) for endpoint in res]

    async def get(self, id: str) -> models.CDNEndpoint:
        res = await self._client.request(
            endpoint="cdn/endpoints/{id}".format(id=id), method="get"
        )
        return models.CDNEndpoint(**res["endpoint"])

    async def create(self, endpoint: models.CDNEndpoint) -> models.CDNEndpoint:
        res = await self._client.request(
            endpoint="cdn/endpoints",
            method="post",
            data=endpoint.json(
                include={"origin", "ttl", "certificate_id", "custom_domain"}
            ),
        )
        return models.CDNEndpoint(**res["endpoint"])

    async def update(self, endpoint: models.CDNEndpoint) -> models.CDNEndpoint:
        res = await self._client.request(
            endpoint="cdn/endpoints/{id}".format(id=endpoint.id),
            method="put",
            data=endpoint.json(include={"ttl", "certificate_id", "custom_domain"}),
        )
        return models.CDNEndpoint(**res["endpoint"])

    async def delete(self, endpoint: models.CDNEndpoint) -> None:
        await self._client.request(
            endpoint="cdn/endpoints/{id}".format(id=endpoint.id), method="delete"
        )

    async def flush_cache(self, id: str, files: List[str] = None) -> None:
        if files is None:
            files = ["*"]
        await self._client.request(
            endpoint="cdn/endpoints/{id}/cache".format(id=id),
            method="delete",
            json={"files": files},
        )

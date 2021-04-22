from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class VPCsManager(BaseManager):
    endpoint = "vpcs"
    name = "vpcs"

    def all(self) -> List[models.VPC]:
        res = self._client.fetch_all(endpoint="vpcs", key="vpcs")
        return [models.VPC(**vpc) for vpc in res]

    def get(self, id: str) -> models.VPC:
        res = self._client.request(endpoint="vpcs/{id}".format(id=id), method="get")
        return models.VPC(**res["vpc"])

    def create(self, vpc: models.VPC) -> models.VPC:
        res = self._client.request(
            endpoint="vpcs",
            method="post",
            data=vpc.json(include={"name", "description", "region", "ip_range"}),
        )
        return models.VPC(**res["vpc"])

    def update(self, vpc: models.VPC) -> models.VPC:
        res = self._client.request(
            endpoint="vpcs/{id}".format(id=vpc.id),
            method="put",
            data=vpc.json(include={"name", "description", "default"}),
        )
        return models.VPC(**res["vpc"])

    def delete(self, vpc: models.VPC) -> None:
        self._client.request(endpoint="vpcs/{id}".format(id=vpc.id), method="delete")

    def members(self, id: str) -> List[models.VPC.Member]:
        res = self._client.fetch_all(
            endpoint="vpcs/{id}/members".format(id=id), key="members"
        )
        return [models.VPC.Member(**member) for member in res]


class AsyncVPCsManager(AsyncBaseManager):
    endpoint = "vpcs"
    name = "vpcs"

    async def all(self) -> List[models.VPC]:
        res = await self._client.fetch_all(endpoint="vpcs", key="vpcs")
        return [models.VPC(**vpc) for vpc in res]

    async def get(self, id: str) -> models.VPC:
        res = await self._client.request(
            endpoint="vpcs/{id}".format(id=id), method="get"
        )
        return models.VPC(**res["vpc"])

    async def create(self, vpc: models.VPC) -> models.VPC:
        res = await self._client.request(
            endpoint="vpcs",
            method="post",
            data=vpc.json(include={"name", "description", "region", "ip_range"}),
        )
        return models.VPC(**res["vpc"])

    async def update(self, vpc: models.VPC) -> models.VPC:
        res = await self._client.request(
            endpoint="vpcs/{id}".format(id=vpc.id),
            method="put",
            data=vpc.json(include={"name", "description", "default"}),
        )
        return models.VPC(**res["vpc"])

    async def delete(self, vpc: models.VPC) -> None:
        await self._client.request(
            endpoint="vpcs/{id}".format(id=vpc.id), method="delete"
        )

    async def members(self, id: str) -> List[models.VPC.Member]:
        res = await self._client.fetch_all(
            endpoint="vpcs/{id}/members".format(id=id), key="members"
        )
        return [models.VPC.Member(**member) for member in res]

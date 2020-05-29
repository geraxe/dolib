from typing import List

from .. import models
from .base import BaseManager


class VPCsManager(BaseManager):
    endpoint = "vpcs"
    name = "vpcs"

    def all(self) -> List[models.Domain]:
        res = self._client.fetch_all(endpoint="vpcs", key="vpcs")
        return [models.VPC(**vpc) for vpc in res]

    def get(self, id: str = None) -> models.VPC:
        assert id is not None, "id must be set"
        res = self._client.request(endpoint="vpcs/{id}".format(id=id), method="get")
        return models.VPC(**res["vpc"])

    def create(self, vpc: models.VPC = None) -> models.VPC:
        assert vpc is not None, "vpc object must be set"

        res = self._client.request(
            endpoint="vpcs",
            method="post",
            data=vpc.json(include={"name", "description", "region", "ip_range"}),
        )
        return models.VPC(**res["vpc"])

    def update(self, vpc: models.VPC = None) -> models.VPC:
        assert vpc is not None, "vpc object must be set"

        res = self._client.request(
            endpoint="vpcs/{id}".format(id=vpc.id),
            method="put",
            data=vpc.json(include={"name", "description"}),
        )
        return models.VPC(**res["vpc"])

    def delete(self, vpc: models.VPC = None):
        assert vpc is not None, "vpc object must be set"

        self._client.request(endpoint="vpcs/{id}".format(id=vpc.id), method="delete")

    def members(self, id: str = None) -> List[models.VPC.Member]:
        assert id is not None, "id must be set"

        res = self._client.fetch_all(
            endpoint="vpcs/{id}/members".format(id=id), key="members"
        )
        return [models.VPC.Member(**member) for member in res]

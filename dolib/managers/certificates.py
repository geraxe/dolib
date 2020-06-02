from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class CertificatesManager(BaseManager):
    endpoint = "certificates"
    name = "certificates"

    def all(self) -> List[models.Certificate]:
        res = self._client.fetch_all(endpoint="certificates", key="certificates")
        return [models.Certificate(**certificate) for certificate in res]

    def get(self, id: str) -> models.Certificate:
        res = self._client.request(
            endpoint="certificates/{id}".format(id=id), method="get"
        )
        return models.Certificate(**res["certificate"])

    def create(self, certificate: models.Certificate) -> models.Certificate:
        res = self._client.request(
            endpoint="certificates",
            method="post",
            data=certificate.json(
                include={
                    "name",
                    "private_key",
                    "leaf_certificate",
                    "certificate_chain",
                    "dns_names",
                    "type",
                }
            ),
        )
        return models.Certificate(**res["certificate"])

    def delete(self, certificate: models.Certificate) -> None:
        self._client.request(
            endpoint="certificates/{id}".format(id=certificate.id), method="delete"
        )


class AsyncCertificatesManager(AsyncBaseManager):
    endpoint = "certificates"
    name = "certificates"

    async def all(self) -> List[models.Certificate]:
        res = await self._client.fetch_all(endpoint="certificates", key="certificates")
        return [models.Certificate(**certificate) for certificate in res]

    async def get(self, id: str) -> models.Certificate:
        res = await self._client.request(
            endpoint="certificates/{id}".format(id=id), method="get"
        )
        return models.Certificate(**res["certificate"])

    async def create(self, certificate: models.Certificate) -> models.Certificate:
        res = await self._client.request(
            endpoint="certificates",
            method="post",
            data=certificate.json(
                include={
                    "name",
                    "private_key",
                    "leaf_certificate",
                    "certificate_chain",
                    "dns_names",
                    "type",
                }
            ),
        )
        return models.Certificate(**res["certificate"])

    async def delete(self, certificate: models.Certificate) -> None:
        await self._client.request(
            endpoint="certificates/{id}".format(id=certificate.id), method="delete"
        )

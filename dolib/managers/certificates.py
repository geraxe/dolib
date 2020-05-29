from typing import List

from .. import models
from .base import BaseManager


class CertificatesManager(BaseManager):
    endpoint = "certificates"
    name = "certificates"

    def all(self) -> List[models.Certificate]:
        res = self._client.fetch_all(endpoint="certificates", key="certificates")
        return [models.Certificate(**certificate) for certificate in res]

    def get(self, id: str = None) -> models.Certificate:
        assert id is not None, "id must be set"
        res = self._client.request(
            endpoint="certificates/{id}".format(id=id), method="get"
        )
        return models.Certificate(**res["certificate"])

    def create(self, certificate: models.Certificate = None) -> models.Certificate:
        assert certificate is not None, "certificate object must be set"

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

    def delete(self, certificate: models.Certificate = None):
        assert certificate is not None, "certificate object must be set"

        self._client.request(
            endpoint="certificates/{id}".format(id=certificate.id), method="delete"
        )

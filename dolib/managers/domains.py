from typing import List

from .. import models
from .base import BaseManager


class DomainsManager(BaseManager):
    endpoint = "domains"
    name = "domains"

    def all(self) -> List[models.Domain]:
        res = self._client.fetch_all(endpoint="domains", key="domains")
        return [models.Domain(**domain) for domain in res]

    def get(self, name: str = None) -> models.Domain:
        assert name is not None, "name must be set"
        res = self._client.request(
            endpoint="domains/{name}".format(name=name), method="get"
        )
        return models.Domain(**res["domain"])

    def create(self, domain: models.Domain = None) -> models.Domain:
        assert domain is not None, "domain object must be set"

        res = self._client.request(
            endpoint="domains", method="post", data=domain.json(include={"name"}),
        )
        return models.Domain(**res["domain"])

    def delete(self, domain: models.Domain = None):
        assert domain is not None, "domain object must be set"

        self._client.request(
            endpoint="domains/{name}".format(name=domain.name), method="delete"
        )

    def records(self, name: str = None) -> List[models.Domain.Record]:
        assert name is not None, "name must be set"

        res = self._client.fetch_all(
            endpoint="domains/{name}/records".format(name=name), key="domain_records"
        )
        return [models.Domain.Record(**record) for record in res]

    def create_record(
        self, name: str = None, record: models.Domain.Record = None
    ) -> models.Domain.Record:
        assert name is not None, "name must be set"
        assert record is not None, "record must be set"

        res = self._client.request(
            endpoint="domains/{name}/records".format(name=name),
            method="post",
            data=record.json(),
        )
        return models.Domain.Record(**res["domain_record"])

    def update_record(
        self, name: str = None, record: models.Domain.Record = None
    ) -> models.Domain.Record:
        assert name is not None, "name must be set"
        assert record is not None, "record must be set"

        res = self._client.request(
            endpoint="domains/{name}/records/{record_id}".format(
                name=name, record_id=record.id
            ),
            method="put",
            data=record.json(),
        )
        return models.Domain.Record(**res["domain_record"])

    def delete_record(self, name: str = None, record: models.Domain.Record = None):
        assert name is not None, "name must be set"
        assert record is not None, "record must be set"

        self._client.request(
            endpoint="domains/{name}/records/{record_id}".format(
                name=name, record_id=record.id
            ),
            method="delete",
            data=record.json(),
        )

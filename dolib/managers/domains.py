from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class DomainsManager(BaseManager):
    endpoint = "domains"
    name = "domains"

    def all(self) -> List[models.Domain]:
        res = self._client.fetch_all(endpoint="domains", key="domains")
        return [models.Domain(**domain) for domain in res]

    def get(self, name: str) -> models.Domain:
        res = self._client.request(
            endpoint="domains/{name}".format(name=name), method="get"
        )
        return models.Domain(**res["domain"])

    def create(self, domain: models.Domain) -> models.Domain:
        res = self._client.request(
            endpoint="domains",
            method="post",
            data=domain.json(include={"name"}),
        )
        return models.Domain(**res["domain"])

    def delete(self, domain: models.Domain) -> None:
        self._client.request(
            endpoint="domains/{name}".format(name=domain.name), method="delete"
        )

    def records(
        self, name: str, record_name: str = None, record_type: str = None
    ) -> List[models.Domain.Record]:
        params = {}
        if record_name is not None:
            params["name"] = record_name
        if record_type is not None:
            params["type"] = record_type
        res = self._client.fetch_all(
            endpoint="domains/{name}/records".format(name=name),
            key="domain_records",
            params=params,
        )
        return [models.Domain.Record(**record) for record in res]

    def create_record(
        self, name: str, record: models.Domain.Record
    ) -> models.Domain.Record:
        res = self._client.request(
            endpoint="domains/{name}/records".format(name=name),
            method="post",
            data=record.json(),
        )
        return models.Domain.Record(**res["domain_record"])

    def update_record(
        self, name: str, record: models.Domain.Record
    ) -> models.Domain.Record:
        res = self._client.request(
            endpoint="domains/{name}/records/{record_id}".format(
                name=name, record_id=record.id
            ),
            method="put",
            data=record.json(),
        )
        return models.Domain.Record(**res["domain_record"])

    def delete_record(self, name: str, record: models.Domain.Record) -> None:
        self._client.request(
            endpoint="domains/{name}/records/{record_id}".format(
                name=name, record_id=record.id
            ),
            method="delete",
            data=record.json(),
        )


class AsyncDomainsManager(AsyncBaseManager):
    endpoint = "domains"
    name = "domains"

    async def all(self) -> List[models.Domain]:
        res = await self._client.fetch_all(endpoint="domains", key="domains")
        return [models.Domain(**domain) for domain in res]

    async def get(self, name: str) -> models.Domain:
        res = await self._client.request(
            endpoint="domains/{name}".format(name=name), method="get"
        )
        return models.Domain(**res["domain"])

    async def create(self, domain: models.Domain) -> models.Domain:
        res = await self._client.request(
            endpoint="domains",
            method="post",
            data=domain.json(include={"name"}),
        )
        return models.Domain(**res["domain"])

    async def delete(self, domain: models.Domain) -> None:
        await self._client.request(
            endpoint="domains/{name}".format(name=domain.name), method="delete"
        )

    async def records(
        self, name: str, record_name: str = None, record_type: str = None
    ) -> List[models.Domain.Record]:
        params = {}
        if record_name is not None:
            params["name"] = record_name
        if record_type is not None:
            params["type"] = record_type
        res = await self._client.fetch_all(
            endpoint="domains/{name}/records".format(name=name),
            key="domain_records",
            params=params,
        )
        return [models.Domain.Record(**record) for record in res]

    async def create_record(
        self, name: str, record: models.Domain.Record
    ) -> models.Domain.Record:
        res = await self._client.request(
            endpoint="domains/{name}/records".format(name=name),
            method="post",
            data=record.json(),
        )
        return models.Domain.Record(**res["domain_record"])

    async def update_record(
        self, name: str, record: models.Domain.Record
    ) -> models.Domain.Record:
        res = await self._client.request(
            endpoint="domains/{name}/records/{record_id}".format(
                name=name, record_id=record.id
            ),
            method="put",
            data=record.json(),
        )
        return models.Domain.Record(**res["domain_record"])

    async def delete_record(self, name: str, record: models.Domain.Record) -> None:
        await self._client.request(
            endpoint="domains/{name}/records/{record_id}".format(
                name=name, record_id=record.id
            ),
            method="delete",
            data=record.json(),
        )

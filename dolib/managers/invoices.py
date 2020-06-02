from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class InvoicesManager(BaseManager):
    endpoint = "invoices"
    name = "invoices"

    def all(self) -> List[models.Invoice]:
        res = self._client.fetch_all(endpoint="customers/my/invoices", key="invoices")
        return [models.Invoice(**invoice) for invoice in res]

    def get(self, id: str) -> models.Invoice:
        res = self._client.request(
            endpoint="customers/my/invoices/{id}/summary".format(id=id), method="get"
        )
        return models.Invoice(**res)

    def items(self, id: str) -> List[models.Invoice.Item]:
        res = self._client.fetch_all(
            endpoint="customers/my/invoices/{id}".format(id=id), key="invoice_items"
        )
        return [models.Invoice.Item(**item) for item in res]

    def csv(self, id: str) -> bytes:
        res = self._client.request_raw(
            endpoint="customers/my/invoices/{id}/csv".format(id=id), method="get"
        )
        return res.content

    def pdf(self, id: str) -> bytes:
        res = self._client.request_raw(
            endpoint="customers/my/invoices/{id}/pdf".format(id=id), method="get"
        )
        return res.content


class AsyncInvoicesManager(AsyncBaseManager):
    endpoint = "invoices"
    name = "invoices"

    async def all(self) -> List[models.Invoice]:
        res = await self._client.fetch_all(
            endpoint="customers/my/invoices", key="invoices"
        )
        return [models.Invoice(**invoice) for invoice in res]

    async def get(self, id: str) -> models.Invoice:
        res = await self._client.request(
            endpoint="customers/my/invoices/{id}/summary".format(id=id), method="get"
        )
        return models.Invoice(**res)

    async def items(self, id: str) -> List[models.Invoice.Item]:
        res = await self._client.fetch_all(
            endpoint="customers/my/invoices/{id}".format(id=id), key="invoice_items"
        )
        return [models.Invoice.Item(**item) for item in res]

    async def csv(self, id: str) -> bytes:
        res = await self._client.request_raw(
            endpoint="customers/my/invoices/{id}/csv".format(id=id), method="get"
        )
        return res.content

    async def pdf(self, id: str) -> bytes:
        res = await self._client.request_raw(
            endpoint="customers/my/invoices/{id}/pdf".format(id=id), method="get"
        )
        return res.content

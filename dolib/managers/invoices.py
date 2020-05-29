from typing import List

from .. import models
from .base import BaseManager


class InvoicesManager(BaseManager):
    endpoint = "invoices"
    name = "invoices"

    def all(self) -> List[models.Invoice]:
        res = self._client.fetch_all(endpoint="customers/my/invoices", key="invoices")
        return [models.Invoice(**invoice) for invoice in res]

    def get(self, id: str = None):
        assert id is not None, "id must be set"

        res = self._client.request(
            endpoint="customers/my/invoices/{id}/summary".format(id=id), method="get"
        )

        print(res)
        return models.Invoice(**res)

    def items(self, id: str = None) -> List[models.Invoice.Item]:
        assert id is not None, "id must be set"

        res = self._client.fetch_all(
            endpoint="customers/my/invoices/{id}".format(id=id), key="invoice_items"
        )

        print(res)
        return [models.Invoice.Item(**item) for item in res]

    def csv(self, id: str = None) -> bytes:
        assert id is not None, "id must be set"

        res = self._client.request_raw(
            endpoint="customers/my/invoices/{id}/csv".format(id=id), method="get"
        )
        return res.content

    def pdf(self, id: str = None) -> bytes:
        assert id is not None, "id must be set"
        res = self._client.request_raw(
            endpoint="customers/my/invoices/{id}/pdf".format(id=id), method="get"
        )
        return res.content

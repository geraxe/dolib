from typing import Tuple

from .. import models
from .base import BaseManager


class AccountManager(BaseManager):
    endpoint = "account"
    name = "account"

    def get(self) -> models.Account:
        res = self._client.request(endpoint="account", method="get")
        return models.Account(**res["account"])

    def balance(self) -> models.Balance:
        res = self._client.request(endpoint="customers/my/balance", method="get")
        return models.Balance(**res)

    def billing_history(self) -> Tuple[models.BillingHistory]:
        res = self._client.fetch_all(
            endpoint="customers/my/billing_history", key="billing_history"
        )
        return tuple(
            models.BillingHistory(**history) for history in res["billing_history"]
        )


class AsyncAccountManager(BaseManager):
    endpoint = "account"
    name = "account"

    async def get(self) -> models.Account:
        res = await self._client.request(endpoint="account", method="get")
        return models.Account(**res["account"])

    async def balance(self) -> models.Balance:
        res = await self._client.request(endpoint="customers/my/balance", method="get")
        return models.Balance(**res)

    async def billing_history(self) -> Tuple[models.BillingHistory]:
        res = await self._client.fetch_all(
            endpoint="customers/my/billing_history", key="billing_history"
        )
        return tuple(models.BillingHistory(**history) for history in res)

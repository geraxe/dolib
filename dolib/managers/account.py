from typing import List

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

    def billing_history(self) -> List[models.BillingHistory]:
        histories = list()
        res = self._client.request(
            endpoint="customers/my/billing_history", method="get"
        )
        for history in res["billing_history"]:
            histories.append(models.BillingHistory(**history))
        return histories

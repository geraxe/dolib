from .. import models
from .base import BaseManager


class ActionsManager(BaseManager):
    endpoint = "actions"
    name = "actions"

    def all(self):
        actions = list()
        res = self._client.request(endpoint="actions", method="get")
        for action in res["actions"]:
            actions.append(models.Action(**action))
        return actions

    def get(self, id=None):
        assert id is not None, "id must be set"

        res = self._client.request(endpoint="actions/{id}".format(id=id), method="get",)
        return models.Action(**res["action"])

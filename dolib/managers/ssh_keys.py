from typing import List

from .. import models
from .base import BaseManager


class SSHKeysManager(BaseManager):
    endpoint = "ssh_keys"
    name = "ssh_keys"

    def all(self) -> List[models.SSHKey]:
        res = self._client.request(endpoint="account/keys", method="get")
        return [models.SSHKey(**key) for key in res["ssh_keys"]]

    def get(self, id: str = None, fingerprint: str = None) -> models.SSHKey:
        assert (
            id is not None or fingerprint is not None
        ), "id or fingerprint must be defined"

        iid = id
        if iid is None and fingerprint is not None:
            iid = fingerprint
        res = self._client.request(
            endpoint="account/keys/{iid}".format(iid=iid), method="get"
        )
        return models.SSHKey(**res["ssh_key"])

    def create(self, key: models.SSHKey) -> models.SSHKey:
        assert isinstance(key, models.SSHKey), "key must be models.SSHKey type"

        res = self._client.request(
            endpoint="account/keys",
            method="post",
            data=key.json(include={"name", "public_key"}),
        )
        return models.SSHKey(**res["ssh_key"])

    def update(self, key: models.SSHKey) -> models.SSHKey:
        assert isinstance(key, models.SSHKey), "key must be models.SSHKey type"

        res = self._client.request(
            endpoint="account/keys/{id}".format(id=key.id),
            method="put",
            data=key.json(include={"name"}),
        )
        return models.SSHKey(**res["ssh_key"])

    def delete(self, key: models.SSHKey) -> None:
        assert isinstance(key, models.SSHKey), "key must be models.SSHKey type"

        self._client.request(
            endpoint="account/keys/{id}".format(id=key.id), method="delete",
        )

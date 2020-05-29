from .. import models
from .base import BaseManager


class SSHKeysManager(BaseManager):
    endpoint = "ssh_keys"
    name = "ssh_keys"

    def all(self):
        keys = list()
        res = self._client.request(endpoint="account/keys", method="get")
        for key in res["ssh_keys"]:
            keys.append(models.SSHKey(**key))
        return keys

    def get(self, id=None, fingerprint=None):
        assert (
            id is not None or fingerprint is not None
        ), "id or fingerprint must be set"

        iid = id
        if iid is None and fingerprint is not None:
            iid = fingerprint
        res = self._client.request(
            endpoint="account/keys/{iid}".format(iid=iid), method="get"
        )
        return models.SSHKey(**res["ssh_key"])

    def create(self, key=None):
        assert key is not None, "key object must be set"

        res = self._client.request(
            endpoint="account/keys",
            method="post",
            data=key.json(include={"name", "public_key"}),
        )
        return models.SSHKey(**res["ssh_key"])

    def update(self, key=None):
        assert key is not None, "key object must be set"

        iid = key.id
        if iid is None and key.fingerprint is not None:
            iid = key.fingerprint

        res = self._client.request(
            endpoint="account/keys/{iid}".format(iid=iid),
            method="put",
            data=key.json(include={"name"}),
        )
        return models.SSHKey(**res["ssh_key"])

    def delete(self, key=None):
        assert key is not None, "key object must be set"

        iid = key.id
        if iid is None and key.fingerprint is not None:
            iid = key.fingerprint

        self._client.request(
            endpoint="account/keys/{iid}".format(iid=iid), method="delete",
        )

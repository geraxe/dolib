from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class SSHKeysManager(BaseManager):
    endpoint = "ssh_keys"
    name = "ssh_keys"

    def all(self) -> List[models.SSHKey]:
        res = self._client.fetch_all(endpoint="account/keys", key="ssh_keys")
        return [models.SSHKey(**key) for key in res]

    def get(self, id: str) -> models.SSHKey:
        res = self._client.request(
            endpoint="account/keys/{id}".format(id=id), method="get"
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
            endpoint="account/keys/{id}".format(id=key.id), method="delete"
        )


class AsyncSSHKeysManager(AsyncBaseManager):
    endpoint = "ssh_keys"
    name = "ssh_keys"

    async def all(self) -> List[models.SSHKey]:
        res = await self._client.fetch_all(endpoint="account/keys", key="ssh_keys")
        return [models.SSHKey(**key) for key in res]

    async def get(self, id: str) -> models.SSHKey:
        res = await self._client.request(
            endpoint="account/keys/{id}".format(id=id), method="get"
        )
        return models.SSHKey(**res["ssh_key"])

    async def create(self, key: models.SSHKey) -> models.SSHKey:
        assert isinstance(key, models.SSHKey), "key must be models.SSHKey type"
        res = await self._client.request(
            endpoint="account/keys",
            method="post",
            data=key.json(include={"name", "public_key"}),
        )
        return models.SSHKey(**res["ssh_key"])

    async def update(self, key: models.SSHKey) -> models.SSHKey:
        assert isinstance(key, models.SSHKey), "key must be models.SSHKey type"
        res = await self._client.request(
            endpoint="account/keys/{id}".format(id=key.id),
            method="put",
            data=key.json(include={"name"}),
        )
        return models.SSHKey(**res["ssh_key"])

    async def delete(self, key: models.SSHKey) -> None:
        assert isinstance(key, models.SSHKey), "key must be models.SSHKey type"
        await self._client.request(
            endpoint="account/keys/{id}".format(id=key.id), method="delete"
        )

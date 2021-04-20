from typing import Any, Dict, List

from .. import models
from .base import AsyncBaseManager, BaseManager


class RegistryManager(BaseManager):
    endpoint: str = "registry"
    name: str = "registry"

    def get(self) -> models.Registry:
        res = self._client.request(
            endpoint="registry",
            method="get",
        )
        return models.Registry(**res["registry"])

    def create(self, registry: models.Registry) -> models.Registry:
        res = self._client.request(
            endpoint="registry",
            method="post",
            data=registry.json(include={"name"}),
        )
        return models.Registry(**res["registry"])

    def delete(self, registry: models.Registry) -> None:
        # may be in future account will be have multiple repository
        self._client.request(
            endpoint="registry",
            method="delete",
        )

    def docker_credentials(
        self, read_write: bool = None, expiry_seconds: int = None
    ) -> dict:
        params: Dict[str, Any] = {}
        if expiry_seconds is not None:
            params["expiry_seconds"] = expiry_seconds
        if read_write is not None:
            params["read_write"] = str(bool(read_write)).lower()
        res = self._client.request(
            endpoint="registry/docker-credentials",
            method="get",
            params=params,
        )
        return res

    def validate_name(self, name: str) -> None:
        self._client.request(
            endpoint="registry/validate-name", method="post", json={"name": name}
        )

    def repositories(self, name: str) -> List[models.Registry.Repository]:
        res = self._client.fetch_all(
            endpoint="registry/{name}/repositories".format(name=name),
            key="repositories",
        )
        return [models.Registry.Repository(**rep) for rep in res]

    def repository_tags(
        self, name: str, repository_name: str
    ) -> List[models.Registry.Repository.Tag]:
        res = self._client.fetch_all(
            endpoint="registry/{name}/repositories/{repository_name}/tags".format(
                name=name, repository_name=repository_name
            ),
            key="tags",
        )

        return [models.Registry.Repository.Tag(**tag) for tag in res]

    def delete_tag(self, name: str, repository_name: str, tag: str) -> None:
        self._client.request(
            endpoint="registry/{name}/repositories/{repository_name}/tags/{tag}".format(
                name=name, repository_name=repository_name, tag=tag
            ),
            method="delete",
        )

    def delete_manifest(self, name: str, repository_name: str, manifest: str) -> None:
        self._client.request(
            endpoint="registry/{name}/repositories/{r_name}/digests/{manifest}".format(
                name=name, r_name=repository_name, manifest=manifest
            ),
            method="delete",
        )

    def start_garbage_collection(
        self, name: str, collection_type: str = None
    ) -> models.Registry.GarbageCollection:
        json_param: Dict[str, Any] = {}
        if collection_type is not None:
            json_param["type"] = collection_type
        res = self._client.request(
            endpoint="registry/{name}/garbage-collection".format(name=name),
            method="post",
            json=json_param,
        )
        return models.Registry.GarbageCollection(**res["garbage_collection"])

    def garbage_collection(self, name: str) -> models.Registry.GarbageCollection:
        res = self._client.request(
            endpoint="registry/{name}/garbage-collection".format(name=name),
            method="get",
        )
        return models.Registry.GarbageCollection(**res["garbage_collection"])


class AsyncRegistryManager(AsyncBaseManager):
    endpoint: str = "registry"
    name: str = "registry"

    async def get(self) -> models.Registry:
        res = await self._client.request(
            endpoint="registry",
            method="get",
        )
        return models.Registry(**res["registry"])

    async def create(self, registry: models.Registry) -> models.Registry:
        res = await self._client.request(
            endpoint="registry",
            method="post",
            data=registry.json(include={"name"}),
        )
        return models.Registry(**res["registry"])

    async def delete(self, registry: models.Registry) -> None:
        # may be in future account will be have multiple repository
        await self._client.request(
            endpoint="registry",
            method="delete",
        )

    async def docker_credentials(
        self, read_write: bool = None, expiry_seconds: int = None
    ) -> dict:
        params: Dict[str, Any] = {}
        if expiry_seconds is not None:
            params["expiry_seconds"] = expiry_seconds
        if read_write is not None:
            params["read_write"] = str(bool(read_write)).lower()
        res = await self._client.request(
            endpoint="registry/docker-credentials",
            method="get",
            params=params,
        )
        return res

    async def validate_name(self, name: str) -> None:
        await self._client.request(
            endpoint="registry/validate-name", method="post", json={"name": name}
        )

    async def repositories(self, name: str) -> List[models.Registry.Repository]:
        res = await self._client.fetch_all(
            endpoint="registry/{name}/repositories".format(name=name),
            key="repositories",
        )
        return [models.Registry.Repository(**rep) for rep in res]

    async def repository_tags(
        self, name: str, repository_name: str
    ) -> List[models.Registry.Repository.Tag]:
        res = await self._client.fetch_all(
            endpoint="registry/{name}/repositories/{repository_name}/tags".format(
                name=name, repository_name=repository_name
            ),
            key="tags",
        )

        return [models.Registry.Repository.Tag(**tag) for tag in res]

    async def delete_tag(self, name: str, repository_name: str, tag: str) -> None:
        await self._client.request(
            endpoint="registry/{name}/repositories/{repository_name}/tags/{tag}".format(
                name=name, repository_name=repository_name, tag=tag
            ),
            method="delete",
        )

    async def delete_manifest(
        self, name: str, repository_name: str, manifest: str
    ) -> None:
        await self._client.request(
            endpoint="registry/{name}/repositories/{r_name}/digests/{manifest}".format(
                name=name, r_name=repository_name, manifest=manifest
            ),
            method="delete",
        )

    async def start_garbage_collection(
        self, name: str, collection_type: str = None
    ) -> models.Registry.GarbageCollection:
        json_param: Dict[str, Any] = {}
        if collection_type is not None:
            json_param["type"] = collection_type
        res = await self._client.request(
            endpoint="registry/{name}/garbage-collection".format(name=name),
            method="post",
            json=json_param,
        )
        return models.Registry.GarbageCollection(**res["garbage_collection"])

    async def garbage_collection(self, name: str) -> models.Registry.GarbageCollection:
        res = await self._client.request(
            endpoint="registry/{name}/garbage-collection".format(name=name),
            method="get",
        )
        return models.Registry.GarbageCollection(**res["garbage_collection"])

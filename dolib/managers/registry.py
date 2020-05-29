from typing import List

from .. import models
from .base import BaseManager


class RegistryManager(BaseManager):
    endpoint: str = "registry"
    name: str = "registry"

    def get(self):
        res = self._client.request(endpoint="registry", method="get",)
        return models.Registry(**res["registry"])

    def create(self, registry: models.Registry = None) -> models.Registry:
        assert registry is not None, "registry object must be set"

        res = self._client.request(
            endpoint="registry", method="post", data=registry.json(include={"name"}),
        )
        return models.Registry(**res["registry"])

    def delete(self, registry: models.Registry = None):
        # may be in future account will be have multiple repository
        assert registry is not None, "registry object must be set"

        self._client.request(
            endpoint="registry", method="delete",
        )

    def docker_credentials(
        self, read_write: bool = None, expiry_seconds: int = None
    ) -> dict:
        params = {}
        if expiry_seconds is not None:
            params["expiry_seconds"] = expiry_seconds
        if read_write is not None:
            params["read_write"] = str(bool(read_write)).lower()
        res = self._client.request(
            endpoint="registry/docker-credentials", method="get",
        )
        return res

    def validate_name(self, name: str = None):
        assert name is not None, "name must be set"
        self._client.request(
            endpoint="registry/validate-name", method="post", json={"name": name}
        )

    def repositories(self, name: str = None) -> List[models.Registry.Repository]:
        assert name is not None, "name must be set"
        res = self._client.fetch_all(
            endpoint="registry/{name}/repositories".format(name=name),
            key="repositories",
        )

        return [models.Registry.Repository(**rep) for rep in res]

    def repository_tags(
        self, name: str = None, repository_name: str = None
    ) -> List[models.Registry.Repository.Tag]:
        assert name is not None, "name must be set"
        assert repository_name is not None, "repository_name must be set"

        res = self._client.fetch_all(
            endpoint="registry/{name}/repositories/{repository_name}/tags".format(
                name=name, repository_name=repository_name
            ),
            key="tags",
        )

        return [models.Registry.Repository.Tag(**tag) for tag in res]

    def delete_tag(
        self, name: str = None, repository_name: str = None, tag: str = None
    ):
        assert name is not None, "name must be set"
        assert repository_name is not None, "repository_name must be set"
        assert tag is not None, "tag must be set"

        self._client.request(
            endpoint="registry/{name}/repositories/{repository_name}/tags/{tag}".format(
                name=name, repository_name=repository_name, tag=tag
            ),
            method="delete",
        )

    def delete_manifest(
        self, name: str = None, repository_name: str = None, manifest: str = None
    ):
        assert name is not None, "name must be set"
        assert repository_name is not None, "repository_name must be set"
        assert manifest is not None, "manifest must be set"

        self._client.request(
            endpoint="registry/{name}/repositories/{r_name}/digests/{manifest}".format(
                name=name, r_name=repository_name, manifest=manifest
            ),
            method="delete",
        )

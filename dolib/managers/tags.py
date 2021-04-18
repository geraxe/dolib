from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class TagsManager(BaseManager):
    endpoint = "tags"
    name = "tags"

    def all(self) -> List[models.Tag]:
        res = self._client.fetch_all(endpoint="tags", key="tags")
        return [models.Tag(**tag) for tag in res]

    def get(self, name: str) -> models.Tag:
        res = self._client.request(
            endpoint="tags/{name}".format(name=name), method="get"
        )
        return models.Tag(**res["tag"])

    def create(self, tag: models.Tag) -> models.Tag:
        res = self._client.request(
            endpoint="tags",
            method="post",
            data=tag.json(include={"name"}),
        )
        return models.Tag(**res["tag"])

    def delete(self, tag: models.Tag) -> None:
        self._client.request(
            endpoint="tags/{name}".format(name=tag.name),
            method="delete",
        )

    def tag_resources(self, name: str, resources: List[models.Tag.Resource]) -> None:

        post_json = {"resources": [res.dict() for res in resources]}

        self._client.request(
            endpoint="tags/{name}/resources".format(name=name),
            method="post",
            json=post_json,
        )

    def untag_resources(self, name: str, resources: List[models.Tag.Resource]) -> None:

        post_json = {"resources": [res.dict() for res in resources]}

        self._client.request(
            endpoint="tags/{name}/resources".format(name=name),
            method="delete",
            json=post_json,
        )


class AsyncTagsManager(AsyncBaseManager):
    endpoint = "tags"
    name = "tags"

    async def all(self) -> List[models.Tag]:
        res = await self._client.fetch_all(endpoint="tags", key="tags")
        return [models.Tag(**tag) for tag in res]

    async def get(self, name: str) -> models.Tag:
        res = await self._client.request(
            endpoint="tags/{name}".format(name=name), method="get"
        )
        return models.Tag(**res["tag"])

    async def create(self, tag: models.Tag) -> models.Tag:
        res = await self._client.request(
            endpoint="tags",
            method="post",
            data=tag.json(include={"name"}),
        )
        return models.Tag(**res["tag"])

    async def delete(self, tag: models.Tag) -> None:
        await self._client.request(
            endpoint="tags/{name}".format(name=tag.name),
            method="delete",
        )

    async def tag_resources(
        self, name: str, resources: List[models.Tag.Resource]
    ) -> None:

        post_json = {"resources": [res.dict() for res in resources]}

        await self._client.request(
            endpoint="tags/{name}/resources".format(name=name),
            method="post",
            json=post_json,
        )

    async def untag_resources(
        self, name: str, resources: List[models.Tag.Resource]
    ) -> None:

        post_json = {"resources": [res.dict() for res in resources]}

        await self._client.request(
            endpoint="tags/{name}/resources".format(name=name),
            method="delete",
            json=post_json,
        )

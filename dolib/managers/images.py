from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class ImagesManager(BaseManager):
    endpoint: str = "images"
    name: str = "images"

    def all(self) -> List[models.Image]:
        res = self._client.fetch_all(endpoint="images", key="images")
        return [models.Image(**image) for image in res]

    def filter(
        self,
        private: str = None,
        type: str = None,
        tag_name: str = None,
    ) -> List[models.Image]:
        params = dict()
        if private is not None:
            params["private"] = str(bool(private)).lower()
        if type is not None:
            params["type"] = type
        if tag_name is not None:
            params["tag_name"] = tag_name

        res = self._client.fetch_all(endpoint="images", key="images", params=params)
        return [models.Image(**image) for image in res]

    def get(self, id: str) -> models.Image:
        res = self._client.request(
            endpoint="images/{id}".format(id=id),
            method="get",
        )
        return models.Image(**res["image"])

    def create(self, image: models.Image) -> models.Image:
        res = self._client.request(
            endpoint="images",
            method="post",
            data=image.json(include={"name", "url", "region", "distribution", "tags"}),
        )
        return models.Image(**res["image"])

    def update(self, image: models.Image) -> models.Image:
        res = self._client.request(
            endpoint="images/{id}".format(id=image.id),
            method="put",
            data=image.json(include={"name", "distribution", "description"}),
        )
        return models.Image(**res["image"])

    def delete(self, image: models.Image) -> None:
        self._client.request(
            endpoint="images/{id}".format(id=image.id),
            method="delete",
        )

    def transfer(self, id: str, region: str) -> models.Action:
        action = {
            "type": "transfer",
            "region": region,
        }

        res = self._client.request(
            endpoint="images/{id}/actions".format(id=id),
            method="post",
            json=action,
        )
        return models.Action(**res["action"])

    def convert(self, id: str) -> models.Action:
        action = {
            "type": "convert",
        }

        res = self._client.request(
            endpoint="images/{id}/actions".format(id=id),
            method="post",
            json=action,
        )
        return models.Action(**res["action"])

    def actions(self, id: str) -> List[models.Action]:
        res = self._client.fetch_all(
            endpoint="images/{id}/actions".format(id=id),
            key="actions",
        )
        return [models.Action(**action) for action in res]


class AsyncImagesManager(AsyncBaseManager):
    endpoint: str = "images"
    name: str = "images"

    async def all(self) -> List[models.Image]:
        res = await self._client.fetch_all(endpoint="images", key="images")
        return [models.Image(**image) for image in res]

    async def filter(
        self,
        private: str = None,
        type: str = None,
        tag_name: str = None,
    ) -> List[models.Image]:
        params = dict()
        if private is not None:
            params["private"] = str(bool(private)).lower()
        if type is not None:
            params["type"] = type
        if tag_name is not None:
            params["tag_name"] = tag_name

        res = await self._client.fetch_all(
            endpoint="images", key="images", params=params
        )
        return [models.Image(**image) for image in res]

    async def get(self, id: str) -> models.Image:
        res = await self._client.request(
            endpoint="images/{id}".format(id=id),
            method="get",
        )
        return models.Image(**res["image"])

    async def create(self, image: models.Image) -> models.Image:
        res = await self._client.request(
            endpoint="images",
            method="post",
            data=image.json(include={"name", "url", "region", "distribution", "tags"}),
        )
        return models.Image(**res["image"])

    async def update(self, image: models.Image) -> models.Image:
        res = await self._client.request(
            endpoint="images/{id}".format(id=image.id),
            method="put",
            data=image.json(include={"name", "distribution", "description"}),
        )
        return models.Image(**res["image"])

    async def delete(self, image: models.Image) -> None:
        await self._client.request(
            endpoint="images/{id}".format(id=image.id),
            method="delete",
        )

    async def transfer(self, id: str, region: str) -> models.Action:
        action = {
            "type": "transfer",
            "region": region,
        }

        res = await self._client.request(
            endpoint="images/{id}/actions".format(id=id),
            method="post",
            json=action,
        )
        return models.Action(**res["action"])

    async def convert(self, id: str) -> models.Action:
        action = {
            "type": "convert",
        }

        res = await self._client.request(
            endpoint="images/{id}/actions".format(id=id),
            method="post",
            json=action,
        )
        return models.Action(**res["action"])

    async def actions(self, id: str) -> List[models.Action]:
        res = await self._client.fetch_all(
            endpoint="images/{id}/actions".format(id=id),
            key="actions",
        )
        return [models.Action(**action) for action in res]

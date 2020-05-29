from typing import List

from .. import models
from .base import BaseManager


class ImagesManager(BaseManager):
    endpoint: str = "images"
    name: str = "images"

    def all(self) -> List[models.Image]:
        images = list()
        res = self._client.fetch_all(endpoint="images", key="images")
        for image in res:
            images.append(models.Image(**image))
        return images

    def filter(
        self, private=None, type=None, tag_name=None,
    ):
        params = dict()
        images = list()
        if private is not None:
            params["private"] = str(bool(private)).lower()
        if type is not None:
            params["type"] = type
        if tag_name is not None:
            params["tag_name"] = tag_name

        res = self._client.fetch_all(endpoint="images", key="images", params=params)
        for image in res:
            images.append(models.Image(**image))
        return images

    def get(self, id: str = None):
        assert id is not None, "id must be set"

        res = self._client.request(endpoint="images/{id}".format(id=id), method="get",)
        return models.Image(**res["image"])

    def create(self, image: models.Image = None):
        assert image is not None, "image object must be set"

        res = self._client.request(
            endpoint="images",
            method="post",
            data=image.json(include={"name", "url", "region", "distribution", "tags"}),
        )
        return models.Image(**res["image"])

    def update(self, image: models.Image = None):
        assert image is not None, "image object must be set"
        res = self._client.request(
            endpoint="images/{id}".format(id=image.id),
            method="put",
            data=image.json(include={"name", "distribution", "description"}),
        )
        return models.Image(**res["image"])

    def delete(self, image: models.Image = None):
        assert image is not None, "image object must be set"

        self._client.request(
            endpoint="images/{id}".format(id=image.id), method="delete",
        )

    def transfer(self, id: str = None, region: str = None) -> models.Action:
        assert id is not None, "droplet id must be set"
        assert region is not None, "region must be set"

        action = {
            "type": "transfer",
            "region": region,
        }

        res = self._client.request(
            endpoint="images/{id}/actions".format(id=id), method="post", json=action,
        )
        return models.Action(**res["action"])

    def convert(self, id: str = None) -> models.Action:
        assert id is not None, "droplet id must be set"
        action = {
            "type": "convert",
        }

        res = self._client.request(
            endpoint="images/{id}/actions".format(id=id), method="post", json=action,
        )
        return models.Action(**res["action"])

    def actions(self, id: str = None) -> List[models.Action]:
        assert id is not None, "id must be set"

        actions = list()
        res = self._client.fetch_all(
            endpoint="images/{id}/actions".format(id=id), key="actions",
        )
        for action in res:
            actions.append(models.Action(**action))
        return actions

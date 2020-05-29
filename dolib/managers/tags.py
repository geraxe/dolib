from typing import List

from .. import models
from .base import BaseManager


class TagsManager(BaseManager):
    endpoint = "tags"
    name = "tags"

    def all(self) -> List[models.Tag]:
        res = self._client.fetch_all(endpoint="tags", key="tags")
        return [models.Tag(**tag) for tag in res]

    def get(self, name: str = None) -> models.Tag:
        assert name is not None, "name must be set"

        res = self._client.request(
            endpoint="tags/{name}".format(name=name), method="get"
        )
        return models.Tag(**res["tag"])

    def create(self, tag: models.Tag = None) -> models.Tag:
        assert tag is not None, "tag object must be set"

        res = self._client.request(
            endpoint="tags", method="post", data=tag.json(include={"name"}),
        )
        return models.Tag(**res["tag"])

    def delete(self, tag: models.Tag = None):
        assert tag is not None, "tag object must be set"

        self._client.request(
            endpoint="tags/{name}".format(name=tag.name), method="delete",
        )

    def tag_resources(
        self, name: str = None, resources: List[models.Tag.Resource] = None
    ):
        assert name is not None, "tag name must be set"
        assert resources is not None, "resources must be set"

        post_json = {"resources": [res.dict() for res in resources]}

        self._client.request(
            endpoint="tags/{name}/resources".format(name=name),
            method="post",
            json=post_json,
        )

    def untag_resources(
        self, name: str = None, resources: List[models.Tag.Resource] = None
    ):
        assert name is not None, "tag name must be set"
        assert resources is not None, "resources must be set"

        post_json = {"resources": [res.dict() for res in resources]}

        self._client.request(
            endpoint="tags/{name}/resources".format(name=name),
            method="delete",
            json=post_json,
        )

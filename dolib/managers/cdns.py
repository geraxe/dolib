from typing import List

from .. import models
from .base import BaseManager


class CDNEndpointsManager(BaseManager):
    endpoint = "cdn_endpoints"
    name = "cdn_endpoints"

    def all(self) -> List[models.CDNEndpoint]:
        res = self._client.fetch_all(endpoint="cdn/endpoints", key="endpoints")
        return [models.CDNEndpoint(**endpoint) for endpoint in res]

    def get(self, id: str = None) -> models.CDNEndpoint:
        assert id is not None, "id must be set"
        res = self._client.request(
            endpoint="cdn/endpoints/{id}".format(id=id), method="get"
        )
        return models.CDNEndpoint(**res["endpoint"])

    def create(self, endpoint: models.CDNEndpoint = None) -> models.CDNEndpoint:
        assert endpoint is not None, "endpoint object must be set"

        res = self._client.request(
            endpoint="cdn/endpoints",
            method="post",
            data=endpoint.json(
                include={"origin", "ttl", "certificate_id", "custom_domain"}
            ),
        )
        return models.CDNEndpoint(**res["endpoint"])

    def update(self, endpoint: models.CDNEndpoint = None):
        assert endpoint is not None, "endpoint object must be set"
        res = self._client.request(
            endpoint="cdn/endpoints/{id}".format(id=endpoint.id),
            method="put",
            data=endpoint.json(include={"ttl", "certificate_id", "custom_domain"}),
        )
        return models.CDNEndpoint(**res["endpoint"])

    def delete(self, endpoint: models.CDNEndpoint = None):
        assert endpoint is not None, "endpoint object must be set"

        self._client.request(
            endpoint="cdn/endpoints/{id}".format(id=endpoint.id), method="delete"
        )

    def flush_cache(self, id: str = None, files: List[str] = ["*"]):
        assert id is not None, "id must be set"

        self._client.request(
            endpoint="cdn/endpoints/{id}/cache".format(id=id),
            method="delete",
            json={"files": files},
        )

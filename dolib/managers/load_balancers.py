from typing import List

from .. import models
from .base import BaseManager


class LoadBalancersManager(BaseManager):
    endpoint: str = "load_balancers"
    name: str = "load_balancers"

    def all(self) -> List[models.LoadBalancer]:
        res = self._client.fetch_all(endpoint="load_balancers", key="load_balancers")
        return [models.LoadBalancer(**lb) for lb in res]

    def get(self, id: str = None):
        assert id is not None, "id must be set"
        res = self._client.request(
            endpoint="load_balancers/{id}".format(id=id), method="get"
        )
        return models.LoadBalancer(**res["load_balancer"])

    def create(self, load_balancer: models.LoadBalancer = None) -> models.LoadBalancer:
        assert load_balancer is not None, "load_balancer object must be set"

        res = self._client.request(
            endpoint="load_balancers", method="post", data=load_balancer.json(),
        )
        return models.LoadBalancer(**res["load_balancer"])

    def update(self, load_balancer: models.LoadBalancer = None):
        assert load_balancer is not None, "load_balancer object must be set"

        if type(load_balancer.region) == models.Region:
            load_balancer.region = load_balancer.region.slug

        res = self._client.request(
            endpoint="load_balancers/{id}".format(id=load_balancer.id),
            method="put",
            data=load_balancer.json(
                include={
                    "name",
                    "algorithm",
                    "region",
                    "forwarding_rules",
                    "health_check",
                    "sticky_sessions",
                    "redirect_http_to_https",
                    "enable_proxy_protocol",
                    "enable_backend_keepalive",
                    "vpc_uuid",
                    "droplet_ids",
                    "tag",
                }
            ),
        )
        return models.LoadBalancer(**res["load_balancer"])

    def delete(self, load_balancer: models.LoadBalancer = None):
        assert load_balancer is not None, "load_balancer object must be set"

        self._client.request(
            endpoint="load_balancers/{id}".format(id=load_balancer.id), method="delete",
        )

    def add_droplets(self, id: str = None, droplet_ids: List[int] = None) -> None:
        assert id is not None, "load balancer id must be set"
        assert droplet_ids is not None, "droplet_ids must be set"

        post_json = {"droplet_ids": droplet_ids}
        self._client.request(
            endpoint="load_balancers/{id}/droplets".format(id=id),
            method="post",
            json=post_json,
        )

    def remove_droplets(self, id: str = None, droplet_ids: List[int] = None) -> None:
        assert id is not None, "load balancer id must be set"
        assert droplet_ids is not None, "droplet_ids must be set"

        post_json = {"droplet_ids": droplet_ids}
        self._client.request(
            endpoint="load_balancers/{id}/droplets".format(id=id),
            method="delete",
            json=post_json,
        )

    def add_forwarding_rules(
        self,
        id: str = None,
        forwarding_rules: List[models.LoadBalancer.ForwardingRule] = None,
    ) -> None:
        assert id is not None, "load balancer id must be set"
        assert forwarding_rules is not None, "forwarding_rules must be set"
        post_json = {"forwarding_rules": [rule.dict() for rule in forwarding_rules]}
        self._client.request(
            endpoint="load_balancers/{id}/forwarding_rules".format(id=id),
            method="post",
            json=post_json,
        )

    def remove_forwarding_rules(
        self,
        id: str = None,
        forwarding_rules: List[models.LoadBalancer.ForwardingRule] = None,
    ) -> None:
        assert id is not None, "load balancer id must be set"
        assert forwarding_rules is not None, "forwarding_rules must be set"
        post_json = {"forwarding_rules": [rule.dict() for rule in forwarding_rules]}
        self._client.request(
            endpoint="load_balancers/{id}/forwarding_rules".format(id=id),
            method="delete",
            json=post_json,
        )

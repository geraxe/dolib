from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class LoadBalancersManager(BaseManager):
    endpoint: str = "load_balancers"
    name: str = "load_balancers"

    def all(self) -> List[models.LoadBalancer]:
        res = self._client.fetch_all(endpoint="load_balancers", key="load_balancers")
        return [models.LoadBalancer(**lb) for lb in res]

    def get(self, id: str) -> models.LoadBalancer:
        res = self._client.request(
            endpoint="load_balancers/{id}".format(id=id), method="get"
        )
        return models.LoadBalancer(**res["load_balancer"])

    def create(self, load_balancer: models.LoadBalancer) -> models.LoadBalancer:
        res = self._client.request(
            endpoint="load_balancers",
            method="post",
            data=load_balancer.json(),
        )
        return models.LoadBalancer(**res["load_balancer"])

    def update(self, load_balancer: models.LoadBalancer) -> models.LoadBalancer:
        if isinstance(load_balancer.region, models.Region):
            load_balancer.region = load_balancer.region.slug

        res = self._client.request(
            endpoint="load_balancers/{id}".format(id=load_balancer.id),
            method="put",
            data=load_balancer.json(
                include={
                    "name",
                    "size",
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

    def delete(self, load_balancer: models.LoadBalancer) -> None:
        self._client.request(
            endpoint="load_balancers/{id}".format(id=load_balancer.id),
            method="delete",
        )

    def add_droplets(self, id: str, droplet_ids: List[int]) -> None:
        post_json = {"droplet_ids": droplet_ids}
        self._client.request(
            endpoint="load_balancers/{id}/droplets".format(id=id),
            method="post",
            json=post_json,
        )

    def remove_droplets(self, id: str, droplet_ids: List[int]) -> None:
        post_json = {"droplet_ids": droplet_ids}
        self._client.request(
            endpoint="load_balancers/{id}/droplets".format(id=id),
            method="delete",
            json=post_json,
        )

    def add_forwarding_rules(
        self, id: str, forwarding_rules: List[models.LoadBalancer.ForwardingRule]
    ) -> None:
        post_json = {"forwarding_rules": [rule.dict() for rule in forwarding_rules]}
        self._client.request(
            endpoint="load_balancers/{id}/forwarding_rules".format(id=id),
            method="post",
            json=post_json,
        )

    def remove_forwarding_rules(
        self,
        id: str,
        forwarding_rules: List[models.LoadBalancer.ForwardingRule],
    ) -> None:
        post_json = {"forwarding_rules": [rule.dict() for rule in forwarding_rules]}
        self._client.request(
            endpoint="load_balancers/{id}/forwarding_rules".format(id=id),
            method="delete",
            json=post_json,
        )


class AsyncLoadBalancersManager(AsyncBaseManager):
    endpoint: str = "load_balancers"
    name: str = "load_balancers"

    async def all(self) -> List[models.LoadBalancer]:
        res = await self._client.fetch_all(
            endpoint="load_balancers", key="load_balancers"
        )
        return [models.LoadBalancer(**lb) for lb in res]

    async def get(self, id: str) -> models.LoadBalancer:
        res = await self._client.request(
            endpoint="load_balancers/{id}".format(id=id), method="get"
        )
        return models.LoadBalancer(**res["load_balancer"])

    async def create(self, load_balancer: models.LoadBalancer) -> models.LoadBalancer:
        res = await self._client.request(
            endpoint="load_balancers",
            method="post",
            data=load_balancer.json(),
        )
        return models.LoadBalancer(**res["load_balancer"])

    async def update(self, load_balancer: models.LoadBalancer) -> models.LoadBalancer:
        if isinstance(load_balancer.region, models.Region):
            load_balancer.region = load_balancer.region.slug

        res = await self._client.request(
            endpoint="load_balancers/{id}".format(id=load_balancer.id),
            method="put",
            data=load_balancer.json(
                include={
                    "name",
                    "size",
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

    async def delete(self, load_balancer: models.LoadBalancer) -> None:
        await self._client.request(
            endpoint="load_balancers/{id}".format(id=load_balancer.id),
            method="delete",
        )

    async def add_droplets(self, id: str, droplet_ids: List[int]) -> None:
        post_json = {"droplet_ids": droplet_ids}
        await self._client.request(
            endpoint="load_balancers/{id}/droplets".format(id=id),
            method="post",
            json=post_json,
        )

    async def remove_droplets(self, id: str, droplet_ids: List[int]) -> None:
        post_json = {"droplet_ids": droplet_ids}
        await self._client.request(
            endpoint="load_balancers/{id}/droplets".format(id=id),
            method="delete",
            json=post_json,
        )

    async def add_forwarding_rules(
        self, id: str, forwarding_rules: List[models.LoadBalancer.ForwardingRule]
    ) -> None:
        post_json = {"forwarding_rules": [rule.dict() for rule in forwarding_rules]}
        await self._client.request(
            endpoint="load_balancers/{id}/forwarding_rules".format(id=id),
            method="post",
            json=post_json,
        )

    async def remove_forwarding_rules(
        self,
        id: str,
        forwarding_rules: List[models.LoadBalancer.ForwardingRule],
    ) -> None:
        post_json = {"forwarding_rules": [rule.dict() for rule in forwarding_rules]}
        await self._client.request(
            endpoint="load_balancers/{id}/forwarding_rules".format(id=id),
            method="delete",
            json=post_json,
        )

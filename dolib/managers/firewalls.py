from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class FirewallsManager(BaseManager):
    endpoint = "firewalls"
    name = "firewalls"

    def all(self) -> List[models.Firewall]:
        res = self._client.fetch_all(endpoint="firewalls", key="firewalls")
        return [models.Firewall(**firewall) for firewall in res]

    def get(self, id: str) -> models.Firewall:
        res = self._client.request(
            endpoint="firewalls/{id}".format(id=id), method="get"
        )
        return models.Firewall(**res["firewall"])

    def create(self, firewall: models.Firewall) -> models.Firewall:
        res = self._client.request(
            endpoint="firewalls",
            method="post",
            data=firewall.json(
                include={
                    "name",
                    "inbound_rules",
                    "outbound_rules",
                    "droplet_ids",
                    "tags",
                }
            ),
        )
        return models.Firewall(**res["firewall"])

    def update(self, firewall: models.Firewall) -> models.Firewall:
        res = self._client.request(
            endpoint="firewalls/{id}".format(id=firewall.id),
            method="put",
            data=firewall.json(
                include={
                    "name",
                    "inbound_rules",
                    "outbound_rules",
                    "droplet_ids",
                    "tags",
                }
            ),
        )
        return models.Firewall(**res["firewall"])

    def delete(self, firewall: models.Firewall) -> None:
        self._client.request(
            endpoint="firewalls/{id}".format(id=firewall.id), method="delete"
        )

    def add_droplets(self, id: str, droplet_ids: List[int]) -> None:
        self._client.request(
            endpoint="firewalls/{id}/droplets".format(id=id),
            method="post",
            json={"droplet_ids": droplet_ids},
        )

    def remove_droplets(self, id: str, droplet_ids: List[int]) -> None:
        self._client.request(
            endpoint="firewalls/{id}/droplets".format(id=id),
            method="delete",
            json={"droplet_ids": droplet_ids},
        )

    def add_tags(self, id: str, tags: List[str]) -> None:
        self._client.request(
            endpoint="firewalls/{id}/tags".format(id=id),
            method="post",
            json={"tags": tags},
        )

    def remove_tags(self, id: str, tags: List[str]) -> None:
        self._client.request(
            endpoint="firewalls/{id}/tags".format(id=id),
            method="delete",
            json={"tags": tags},
        )

    def add_rules(
        self,
        id: str,
        inbound_rules: List[models.Firewall.InboundRule] = None,
        outbound_rules: List[models.Firewall.OutboundRule] = None,
    ) -> None:
        assert (
            inbound_rules is not None or outbound_rules is not None
        ), "inbound_rules or outbound_rules must be defined"

        post_json = {}
        if inbound_rules is not None:
            post_json["inbound_rules"] = [rule.dict() for rule in inbound_rules]
        if outbound_rules is not None:
            post_json["outbound_rules"] = [rule.dict() for rule in outbound_rules]

        self._client.request(
            endpoint="firewalls/{id}/rules".format(id=id),
            method="post",
            json=post_json,
        )

    def remove_rules(
        self,
        id: str,
        inbound_rules: List[models.Firewall.InboundRule] = None,
        outbound_rules: List[models.Firewall.OutboundRule] = None,
    ) -> None:
        assert (
            inbound_rules is not None or outbound_rules is not None
        ), "inbound_rules or outbound_rules must be defined"

        post_json = {}
        if inbound_rules is not None:
            post_json["inbound_rules"] = [rule.dict() for rule in inbound_rules]
        if outbound_rules is not None:
            post_json["outbound_rules"] = [rule.dict() for rule in outbound_rules]

        self._client.request(
            endpoint="firewalls/{id}/rules".format(id=id),
            method="delete",
            json=post_json,
        )


class AsyncFirewallsManager(AsyncBaseManager):
    endpoint = "firewalls"
    name = "firewalls"

    async def all(self) -> List[models.Firewall]:
        res = await self._client.fetch_all(endpoint="firewalls", key="firewalls")
        return [models.Firewall(**firewall) for firewall in res]

    async def get(self, id: str) -> models.Firewall:
        res = await self._client.request(
            endpoint="firewalls/{id}".format(id=id), method="get"
        )
        return models.Firewall(**res["firewall"])

    async def create(self, firewall: models.Firewall) -> models.Firewall:
        res = await self._client.request(
            endpoint="firewalls",
            method="post",
            data=firewall.json(
                include={
                    "name",
                    "inbound_rules",
                    "outbound_rules",
                    "droplet_ids",
                    "tags",
                }
            ),
        )
        return models.Firewall(**res["firewall"])

    async def update(self, firewall: models.Firewall) -> models.Firewall:
        res = await self._client.request(
            endpoint="firewalls/{id}".format(id=firewall.id),
            method="put",
            data=firewall.json(
                include={
                    "name",
                    "inbound_rules",
                    "outbound_rules",
                    "droplet_ids",
                    "tags",
                }
            ),
        )
        return models.Firewall(**res["firewall"])

    async def delete(self, firewall: models.Firewall) -> None:
        await self._client.request(
            endpoint="firewalls/{id}".format(id=firewall.id), method="delete"
        )

    async def add_droplets(self, id: str, droplet_ids: List[int]) -> None:
        await self._client.request(
            endpoint="firewalls/{id}/droplets".format(id=id),
            method="post",
            json={"droplet_ids": droplet_ids},
        )

    async def remove_droplets(self, id: str, droplet_ids: List[int]) -> None:
        await self._client.request(
            endpoint="firewalls/{id}/droplets".format(id=id),
            method="delete",
            json={"droplet_ids": droplet_ids},
        )

    async def add_tags(self, id: str, tags: List[str]) -> None:
        await self._client.request(
            endpoint="firewalls/{id}/tags".format(id=id),
            method="post",
            json={"tags": tags},
        )

    async def remove_tags(self, id: str, tags: List[str]) -> None:
        await self._client.request(
            endpoint="firewalls/{id}/tags".format(id=id),
            method="delete",
            json={"tags": tags},
        )

    async def add_rules(
        self,
        id: str,
        inbound_rules: List[models.Firewall.InboundRule] = None,
        outbound_rules: List[models.Firewall.OutboundRule] = None,
    ) -> None:
        assert (
            inbound_rules is not None or outbound_rules is not None
        ), "inbound_rules or outbound_rules must be defined"

        post_json = {}
        if inbound_rules is not None:
            post_json["inbound_rules"] = [rule.dict() for rule in inbound_rules]
        if outbound_rules is not None:
            post_json["outbound_rules"] = [rule.dict() for rule in outbound_rules]

        await self._client.request(
            endpoint="firewalls/{id}/rules".format(id=id),
            method="post",
            json=post_json,
        )

    async def remove_rules(
        self,
        id: str,
        inbound_rules: List[models.Firewall.InboundRule] = None,
        outbound_rules: List[models.Firewall.OutboundRule] = None,
    ) -> None:
        assert (
            inbound_rules is not None or outbound_rules is not None
        ), "inbound_rules or outbound_rules must be defined"

        post_json = {}
        if inbound_rules is not None:
            post_json["inbound_rules"] = [rule.dict() for rule in inbound_rules]
        if outbound_rules is not None:
            post_json["outbound_rules"] = [rule.dict() for rule in outbound_rules]

        await self._client.request(
            endpoint="firewalls/{id}/rules".format(id=id),
            method="delete",
            json=post_json,
        )

from typing import List

from .. import models
from .base import BaseManager


class FirewallsManager(BaseManager):
    endpoint = "firewalls"
    name = "firewalls"

    def all(self) -> List[models.Firewall]:
        res = self._client.fetch_all(endpoint="firewalls", key="firewalls")
        return [models.Firewall(**firewall) for firewall in res]

    def get(self, id: str = None) -> models.Firewall:
        assert id is not None, "id must be set"
        res = self._client.request(
            endpoint="firewalls/{id}".format(id=id), method="get"
        )
        return models.Firewall(**res["firewall"])

    def create(self, firewall: models.Firewall = None) -> models.Firewall:
        assert firewall is not None, "firewall object must be set"

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

    def update(self, firewall: models.Firewall = None):
        assert firewall is not None, "firewall object must be set"
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

    def delete(self, firewall: models.Firewall = None):
        assert firewall is not None, "firewall object must be set"

        self._client.request(
            endpoint="firewalls/{id}".format(id=firewall.id), method="delete"
        )

    def add_droplets(self, id: str = None, droplet_ids: List[int] = None):
        assert id is not None, "id must be set"
        assert droplet_ids is not None, "droplet_ids must be set"

        self._client.request(
            endpoint="firewalls/{id}/droplets".format(id=id),
            method="post",
            json={"droplet_ids": droplet_ids},
        )

    def remove_droplets(self, id: str = None, droplet_ids: List[int] = None):
        assert id is not None, "id must be set"
        assert droplet_ids is not None, "droplet_ids must be set"

        self._client.request(
            endpoint="firewalls/{id}/droplets".format(id=id),
            method="delete",
            json={"droplet_ids": droplet_ids},
        )

    def add_tags(self, id: str = None, tags: List[str] = None):
        assert id is not None, "id must be set"
        assert tags is not None, "tags must be set"

        self._client.request(
            endpoint="firewalls/{id}/tags".format(id=id),
            method="post",
            json={"tags": tags},
        )

    def remove_tags(self, id: str = None, tags: List[str] = None):
        assert id is not None, "id must be set"
        assert tags is not None, "tags must be set"

        self._client.request(
            endpoint="firewalls/{id}/tags".format(id=id),
            method="delete",
            json={"tags": tags},
        )

    def add_rules(
        self,
        id: str = None,
        inbound_rules: List[models.Firewall.InboundRule] = None,
        outbound_rules: List[models.Firewall.OutboundRule] = None,
    ):
        assert id is not None, "id must be set"
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
        id: str = None,
        inbound_rules: List[models.Firewall.InboundRule] = None,
        outbound_rules: List[models.Firewall.OutboundRule] = None,
    ):
        assert id is not None, "id must be set"
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

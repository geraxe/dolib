from typing import List

from .. import models
from .base import BaseManager


class FloatingIPsManager(BaseManager):
    endpoint = "floating_ips"
    name = "floating_ips"

    def all(self) -> List[models.FloatingIP]:
        res = self._client.fetch_all(endpoint="floating_ips", key="floating_ips")
        return [models.FloatingIP(**ip) for ip in res]

    def get(self, ip: str = None) -> models.FloatingIP:
        assert ip is not None, "ip must be set"
        res = self._client.request(
            endpoint="floating_ips/{ip}".format(ip=ip), method="get"
        )
        return models.FloatingIP(**res["floating_ip"])

    def create(self, ip: models.FloatingIP = None) -> models.FloatingIP:
        assert ip is not None, "ip object must be set"

        post_data = {}
        if ip.region is not None:
            if type(ip) == models.Region:
                post_data["region"] = ip.region.slug
            else:
                post_data["region"] = ip.region
        elif ip.droplet is not None:
            post_data["droplet_id"] = ip.droplet.id

        res = self._client.request(
            endpoint="floating_ips", method="post", json=post_data,
        )
        return models.FloatingIP(**res["floating_ip"])

    def delete(self, ip: models.FloatingIP = None):
        assert ip is not None, "ip object must be set"

        self._client.request(
            endpoint="floating_ips/{ip}".format(ip=ip.ip), method="delete"
        )

    def assign(self, ip: str = None, droplet: models.Droplet = None) -> models.Action:
        assert ip is not None, "ip must be set"
        assert droplet is not None, "droplet must be set"
        res = self._client.request(
            endpoint="floating_ips/{ip}/actions".format(ip=ip),
            method="post",
            json={"type": "assign", "droplet_id": droplet.id},
        )
        return models.Action(**res["action"])

    def unassign(self, ip: str = None) -> models.Action:
        assert ip is not None, "ip must be set"
        res = self._client.request(
            endpoint="floating_ips/{ip}/actions".format(ip=ip),
            method="post",
            json={"type": "unassign"},
        )
        return models.Action(**res["action"])

    def actions(self, ip: str = None) -> List[models.Action]:
        assert ip is not None, "ip must be set"
        res = self._client.fetch_all(
            endpoint="floating_ips/{ip}/actions".format(ip=ip), key="actions"
        )
        return [models.Action(**action) for action in res]

    def action(self, ip: str = None, action_id: int = None) -> models.Action:
        assert ip is not None, "ip must be set"
        assert action_id is not None, "action_id must be set"
        res = self._client.request(
            endpoint="floating_ips/{ip}/actions/{action_id}".format(
                ip=ip, action_id=action_id
            ),
            method="get",
        )
        return models.Action(**res["action"])

from typing import Any, Dict, List

from .. import models
from .base import AsyncBaseManager, BaseManager


class FloatingIPsManager(BaseManager):
    endpoint = "floating_ips"
    name = "floating_ips"

    def all(self) -> List[models.FloatingIP]:
        res = self._client.fetch_all(endpoint="floating_ips", key="floating_ips")
        return [models.FloatingIP(**ip) for ip in res]

    def get(self, ip: str) -> models.FloatingIP:
        res = self._client.request(
            endpoint="floating_ips/{ip}".format(ip=ip), method="get"
        )
        return models.FloatingIP(**res["floating_ip"])

    def create(self, ip: models.FloatingIP) -> models.FloatingIP:
        post_data: Dict[str, Any] = {}
        if ip.region is not None and isinstance(ip.region, str):
            post_data["region"] = ip.region
        elif ip.droplet is not None:
            post_data["droplet_id"] = ip.droplet.id

        res = self._client.request(
            endpoint="floating_ips",
            method="post",
            json=post_data,
        )
        return models.FloatingIP(**res["floating_ip"])

    def delete(self, ip: models.FloatingIP) -> None:
        self._client.request(
            endpoint="floating_ips/{ip}".format(ip=ip.ip), method="delete"
        )

    def assign(self, ip: str, droplet: models.Droplet) -> models.Action:
        res = self._client.request(
            endpoint="floating_ips/{ip}/actions".format(ip=ip),
            method="post",
            json={"type": "assign", "droplet_id": droplet.id},
        )
        return models.Action(**res["action"])

    def unassign(self, ip: str) -> models.Action:
        res = self._client.request(
            endpoint="floating_ips/{ip}/actions".format(ip=ip),
            method="post",
            json={"type": "unassign"},
        )
        return models.Action(**res["action"])

    def actions(self, ip: str) -> List[models.Action]:
        res = self._client.fetch_all(
            endpoint="floating_ips/{ip}/actions".format(ip=ip), key="actions"
        )
        return [models.Action(**action) for action in res]

    def action(self, ip: str, action_id: int) -> models.Action:
        res = self._client.request(
            endpoint="floating_ips/{ip}/actions/{action_id}".format(
                ip=ip, action_id=action_id
            ),
            method="get",
        )
        return models.Action(**res["action"])


class AsyncFloatingIPsManager(AsyncBaseManager):
    endpoint = "floating_ips"
    name = "floating_ips"

    async def all(self) -> List[models.FloatingIP]:
        res = await self._client.fetch_all(endpoint="floating_ips", key="floating_ips")
        return [models.FloatingIP(**ip) for ip in res]

    async def get(self, ip: str) -> models.FloatingIP:
        res = await self._client.request(
            endpoint="floating_ips/{ip}".format(ip=ip), method="get"
        )
        return models.FloatingIP(**res["floating_ip"])

    async def create(self, ip: models.FloatingIP) -> models.FloatingIP:
        post_data: Dict[str, Any] = {}
        if ip.region is not None and isinstance(ip.region, str):
            post_data["region"] = ip.region
        elif ip.droplet is not None:
            post_data["droplet_id"] = ip.droplet.id

        res = await self._client.request(
            endpoint="floating_ips",
            method="post",
            json=post_data,
        )
        return models.FloatingIP(**res["floating_ip"])

    async def delete(self, ip: models.FloatingIP) -> None:
        await self._client.request(
            endpoint="floating_ips/{ip}".format(ip=ip.ip), method="delete"
        )

    async def assign(self, ip: str, droplet: models.Droplet) -> models.Action:
        res = await self._client.request(
            endpoint="floating_ips/{ip}/actions".format(ip=ip),
            method="post",
            json={"type": "assign", "droplet_id": droplet.id},
        )
        return models.Action(**res["action"])

    async def unassign(self, ip: str) -> models.Action:
        res = await self._client.request(
            endpoint="floating_ips/{ip}/actions".format(ip=ip),
            method="post",
            json={"type": "unassign"},
        )
        return models.Action(**res["action"])

    async def actions(self, ip: str) -> List[models.Action]:
        res = await self._client.fetch_all(
            endpoint="floating_ips/{ip}/actions".format(ip=ip), key="actions"
        )
        return [models.Action(**action) for action in res]

    async def action(self, ip: str, action_id: int) -> models.Action:
        res = await self._client.request(
            endpoint="floating_ips/{ip}/actions/{action_id}".format(
                ip=ip, action_id=action_id
            ),
            method="get",
        )
        return models.Action(**res["action"])

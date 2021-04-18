from typing import Any, Dict, List, Union

from .. import models
from .base import AsyncBaseManager, BaseManager


class DropletsManager(BaseManager):
    endpoint = "droplets"
    name = "droplets"

    def all(self) -> List[models.Droplet]:
        res = self._client.fetch_all(endpoint="droplets", key="droplets")
        return [models.Droplet(**droplet) for droplet in res]

    def filter(self, tag_name: str = None) -> List[models.Droplet]:
        params = {}
        if tag_name is not None:
            params["tag_name"] = tag_name
        res = self._client.fetch_all(
            endpoint="droplets",
            key="droplets",
            params=params,
        )
        return [models.Droplet(**droplet) for droplet in res]

    def get(self, id: str) -> models.Droplet:
        res = self._client.request(endpoint="droplets/{id}".format(id=id), method="get")
        return models.Droplet(**res["droplet"])

    def create(self, droplet: models.Droplet) -> models.Droplet:
        res = self._client.request(
            endpoint="droplets",
            method="post",
            data=droplet.json(
                include={
                    "name",
                    "region",
                    "size",
                    "image",
                    "ssh_keys",
                    "backups",
                    "ipv6",
                    "private_networking",
                    "vpc_uuid",
                    "user_data",
                    "monitoring",
                    "volumes",
                    "tags",
                }
            ),
        )
        return models.Droplet(**res["droplet"])

    def delete(self, droplet: models.Droplet) -> None:
        self._client.request(
            endpoint="droplets/{id}".format(id=droplet.id), method="delete"
        )

    def neighbors(self, id: str) -> List[models.Droplet]:
        res = self._client.fetch_all(
            endpoint="droplets/{id}/neighbors".format(id=id),
            key="droplets",
        )
        return [models.Droplet(**neighbor) for neighbor in res]

    def kernels(self, id: str) -> List[models.Droplet.Kernel]:
        res = self._client.fetch_all(
            endpoint="droplets/{id}/kernels".format(id=id),
            key="kernels",
        )
        return [models.Droplet.Kernel(**kernel) for kernel in res]

    def shapshots(self, id: str) -> List[models.Snapshot]:
        res = self._client.fetch_all(
            endpoint="droplets/{id}/snapshots".format(id=id),
            key="snapshots",
        )
        return [models.Snapshot(**snapshot) for snapshot in res]

    def actions(self, id: str) -> List[models.Action]:
        res = self._client.fetch_all(
            endpoint="droplets/{id}/actions".format(id=id),
            key="actions",
        )
        return [models.Action(**action) for action in res]

    def action(self, id: str, action_id: int) -> models.Action:
        res = self._client.request(
            endpoint="droplets/{id}/actions/{action_id}".format(
                id=id, action_id=action_id
            ),
            method="get",
        )
        return models.Action(**res["action"])

    def sizes(self) -> List[models.Droplet.Size]:
        res = self._client.fetch_all(endpoint="sizes", key="sizes")
        return [models.Droplet.Size(**size) for size in res]

    # Actions

    def _action(self, id: str, action: str) -> models.Action:
        post_json = {"type": action}
        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id),
            method="post",
            json=post_json,
        )
        return models.Action(**res["action"])

    def enable_backups(self, id: str) -> models.Action:
        return self._action(id, "enable_backups")

    def disable_backups(self, id: str) -> models.Action:
        return self._action(id, "disable_backups")

    def reboot(self, id: str) -> models.Action:
        return self._action(id, "reboot")

    def power_cycle(self, id: str) -> models.Action:
        return self._action(id, "power_cycle")

    def shutdown(self, id: str) -> models.Action:
        return self._action(id, "shutdown")

    def power_off(self, id: str) -> models.Action:
        return self._action(id, "power_off")

    def power_on(self, id: str) -> models.Action:
        return self._action(id, "power_on")

    def restore(self, id: str, image: Union[int, str]) -> models.Action:
        action = {
            "type": "restore",
            "image": image,
        }
        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    def password_reset(self, id: str) -> models.Action:
        return self._action(id, "password_reset")

    def resize(self, id: str, size: str, disk: bool = None) -> models.Action:

        post_json: Dict[str, Any] = {
            "type": "resize",
            "size": size,
        }
        if disk is not None:
            post_json["disk"] = disk

        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id),
            method="post",
            json=post_json,
        )
        return models.Action(**res["action"])

    def rebuild(self, id: str, image: Union[int, str]) -> models.Action:
        action = {
            "type": "rebuild",
            "image": image,
        }
        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    def rename(self, id: str, name: str) -> models.Action:
        action = {
            "type": "rename",
            "name": name,
        }
        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    def change_kernel(self, id: str, kernel: int) -> models.Action:
        action = {
            "type": "change_kernel",
            "kernel": kernel,
        }
        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    def enable_ipv6(self, id: str) -> models.Action:
        return self._action(id, "enable_ipv6")

    def enable_private_networking(self, id: str) -> models.Action:
        return self._action(id, "enable_private_networking")

    def tag_action(self, tag_name: str, action: str) -> List[models.Action]:
        assert tag_name is not None, "tag_name must be set"
        assert action is not None, "action must be set"

        params = {}
        if tag_name is not None:
            params["tag_name"] = tag_name

        post_json = {"type": action}

        res = self._client.request(
            endpoint="droplets/actions",
            method="post",
            json=post_json,
            params=params,
        )
        return [models.Action(**action) for action in res["actions"]]

    def snapshot(self, id: str, name: str = None) -> models.Action:
        action = {"type": "snapshot"}
        if name is not None:
            action["name"] = name

        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])


class AsyncDropletsManager(AsyncBaseManager):
    endpoint = "droplets"
    name = "droplets"

    async def all(self) -> List[models.Droplet]:
        res = await self._client.fetch_all(endpoint="droplets", key="droplets")
        return [models.Droplet(**droplet) for droplet in res]

    async def filter(self, tag_name: str = None) -> List[models.Droplet]:
        params = {}
        if tag_name is not None:
            params["tag_name"] = tag_name
        res = await self._client.fetch_all(
            endpoint="droplets",
            key="droplets",
            params=params,
        )
        return [models.Droplet(**droplet) for droplet in res]

    async def get(self, id: str) -> models.Droplet:
        res = await self._client.request(
            endpoint="droplets/{id}".format(id=id), method="get"
        )
        return models.Droplet(**res["droplet"])

    async def create(self, droplet: models.Droplet) -> models.Droplet:
        res = await self._client.request(
            endpoint="droplets",
            method="post",
            data=droplet.json(
                include={
                    "name",
                    "region",
                    "size",
                    "image",
                    "ssh_keys",
                    "backups",
                    "ipv6",
                    "private_networking",
                    "vpc_uuid",
                    "user_data",
                    "monitoring",
                    "volumes",
                    "tags",
                }
            ),
        )
        return models.Droplet(**res["droplet"])

    async def delete(self, droplet: models.Droplet) -> None:
        await self._client.request(
            endpoint="droplets/{id}".format(id=droplet.id), method="delete"
        )

    async def neighbors(self, id: str) -> List[models.Droplet]:
        res = await self._client.fetch_all(
            endpoint="droplets/{id}/neighbors".format(id=id),
            key="droplets",
        )
        return [models.Droplet(**neighbor) for neighbor in res]

    async def kernels(self, id: str) -> List[models.Droplet.Kernel]:
        res = await self._client.fetch_all(
            endpoint="droplets/{id}/kernels".format(id=id),
            key="kernels",
        )
        return [models.Droplet.Kernel(**kernel) for kernel in res]

    async def shapshots(self, id: str) -> List[models.Snapshot]:
        res = await self._client.fetch_all(
            endpoint="droplets/{id}/snapshots".format(id=id),
            key="snapshots",
        )
        return [models.Snapshot(**snapshot) for snapshot in res]

    async def actions(self, id: str) -> List[models.Action]:
        res = await self._client.fetch_all(
            endpoint="droplets/{id}/actions".format(id=id),
            key="actions",
        )
        return [models.Action(**action) for action in res]

    async def action(self, id: str, action_id: int) -> models.Action:
        res = await self._client.request(
            endpoint="droplets/{id}/actions/{action_id}".format(
                id=id, action_id=action_id
            ),
            method="get",
        )
        return models.Action(**res["action"])

    async def sizes(self) -> List[models.Droplet.Size]:
        res = await self._client.fetch_all(endpoint="sizes", key="sizes")
        return [models.Droplet.Size(**size) for size in res]

    # Actions

    async def _action(self, id: str, action: str) -> models.Action:
        post_json = {"type": action}
        res = await self._client.request(
            endpoint="droplets/{id}/actions".format(id=id),
            method="post",
            json=post_json,
        )
        return models.Action(**res["action"])

    async def enable_backups(self, id: str) -> models.Action:
        return await self._action(id, "enable_backups")

    async def disable_backups(self, id: str) -> models.Action:
        return await self._action(id, "disable_backups")

    async def reboot(self, id: str) -> models.Action:
        return await self._action(id, "reboot")

    async def power_cycle(self, id: str) -> models.Action:
        return await self._action(id, "power_cycle")

    async def shutdown(self, id: str) -> models.Action:
        return await self._action(id, "shutdown")

    async def power_off(self, id: str) -> models.Action:
        return await self._action(id, "power_off")

    async def power_on(self, id: str) -> models.Action:
        return await self._action(id, "power_on")

    async def restore(self, id: str, image: Union[int, str]) -> models.Action:
        action = {
            "type": "restore",
            "image": image,
        }
        res = await self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    async def password_reset(self, id: str) -> models.Action:
        return await self._action(id, "password_reset")

    async def resize(self, id: str, size: str, disk: bool = None) -> models.Action:

        post_json: Dict[str, Any] = {
            "type": "resize",
            "size": size,
        }
        if disk is not None:
            post_json["disk"] = disk

        res = await self._client.request(
            endpoint="droplets/{id}/actions".format(id=id),
            method="post",
            json=post_json,
        )
        return models.Action(**res["action"])

    async def rebuild(self, id: str, image: Union[int, str]) -> models.Action:
        action = {
            "type": "rebuild",
            "image": image,
        }
        res = await self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    async def rename(self, id: str, name: str) -> models.Action:
        action = {
            "type": "rename",
            "name": name,
        }
        res = await self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    async def change_kernel(self, id: str, kernel: int) -> models.Action:
        action = {
            "type": "change_kernel",
            "kernel": kernel,
        }
        res = await self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    async def enable_ipv6(self, id: str) -> models.Action:
        return await self._action(id, "enable_ipv6")

    async def enable_private_networking(self, id: str) -> models.Action:
        return await self._action(id, "enable_private_networking")

    async def tag_action(self, tag_name: str, action: str) -> List[models.Action]:
        assert tag_name is not None, "tag_name must be set"
        assert action is not None, "action must be set"

        params = {}
        if tag_name is not None:
            params["tag_name"] = tag_name

        post_json = {"type": action}

        res = await self._client.request(
            endpoint="droplets/actions",
            method="post",
            json=post_json,
            params=params,
        )
        return [models.Action(**action) for action in res["actions"]]

    async def snapshot(self, id: str, name: str = None) -> models.Action:
        action = {"type": "snapshot"}
        if name is not None:
            action["name"] = name

        res = await self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

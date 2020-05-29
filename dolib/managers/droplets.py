from typing import List, Union

from .. import models
from .base import BaseManager


class DropletsManager(BaseManager):
    endpoint = "droplets"
    name = "droplets"

    def all(self):
        res = self._client.fetch_all(endpoint="droplets", key="droplets")
        return [models.Droplet(**droplet) for droplet in res]

    def filter(self, tag_name: str = None):
        params = {}
        if tag_name is not None:
            params["tag_name"] = tag_name
        res = self._client.fetch_all(
            endpoint="droplets", key="droplets", params=params,
        )
        return [models.Droplet(**droplet) for droplet in res]

    def get(self, id: str = None):
        assert id is not None, "id must be set"
        res = self._client.request(endpoint="droplets/{id}".format(id=id), method="get")
        return models.Droplet(**res["droplet"])

    def create(self, droplet: models.Droplet = None):
        assert droplet is not None, "droplet object must be set"

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

    def delete(self, droplet: models.Droplet = None):
        assert droplet is not None, "droplet object must be set"

        self._client.request(
            endpoint="droplets/{id}".format(id=droplet.id), method="delete"
        )

    def neighbors(self, id: str = None) -> List[models.Droplet]:
        assert id is not None, "droplet id must be set"
        res = self._client.fetch_all(
            endpoint="droplets/{id}/neighbors".format(id=id), key="droplets",
        )
        return [models.Droplet(**neighbor) for neighbor in res]

    def kernels(self, id: str = None) -> List[models.Droplet.Kernel]:
        assert id is not None, "droplet id must be set"

        res = self._client.fetch_all(
            endpoint="droplets/{id}/kernels".format(id=id), key="kernels",
        )
        return [models.Droplet.Kernel(**kernel) for kernel in res]

    def shapshots(self, id: str = None):
        assert id is not None, "droplet id must be set"

        res = self._client.fetch_all(
            endpoint="droplets/{id}/snapshots".format(id=id), key="snapshots",
        )
        return [models.Snapshot(**snapshot) for snapshot in res]

    def actions(self, id: str = None) -> List[models.Action]:
        assert id is not None, "droplet id must be set"
        res = self._client.fetch_all(
            endpoint="droplets/{id}/actions".format(id=id), key="actions",
        )
        return [models.Action(**action) for action in res]

    def action(self, id: str = None, action_id: int = None) -> models.Action:
        assert id is not None, "droplet id must be set"
        assert action_id is not None, "action_id must be set"
        res = self._client.request(
            endpoint="droplets/{id}/actions/{action_id}".format(
                id=id, action_id=action_id
            ),
            method="get",
        )
        return models.Action(**res["action"])

    def sizes(self):
        res = self._client.fetch_all(endpoint="sizes", key="sizes")
        return [models.Droplet.Size(**size) for size in res]

    # Actions

    def _action(self, id: str = None, action: str = None) -> models.Action:
        assert id is not None, "droplet id must be set"
        assert action is not None, "action must be set"

        action = {"type": action}
        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    def enable_backups(self, id: str = None) -> models.Action:
        return self._action(id, "enable_backups")

    def disable_backups(self, id: str = None) -> models.Action:
        return self._action(id, "disable_backups")

    def reboot(self, id: str = None) -> models.Action:
        return self._action(id, "reboot")

    def power_cycle(self, id: str = None) -> models.Action:
        return self._action(id, "power_cycle")

    def shutdown(self, id: str = None) -> models.Action:
        return self._action(id, "shutdown")

    def power_off(self, id: str = None) -> models.Action:
        return self._action(id, "power_off")

    def power_on(self, id: str = None) -> models.Action:
        return self._action(id, "power_on")

    def restore(self, id: str = None, image: Union[int, str] = None) -> models.Action:
        assert id is not None, "droplet id must be set"
        assert image is not None, "image must be set"

        action = {
            "type": "restore",
            "image": image,
        }
        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    def password_reset(self, id: str = None) -> models.Action:
        return self._action(id, "password_reset")

    def resize(
        self, id: str = None, size: str = None, disk: bool = None
    ) -> models.Action:
        assert id is not None, "droplet id must be set"
        assert size is not None, "size must be set"

        action = {
            "type": "resize",
            "size": size,
        }
        if disk is not None:
            action["disk"] = disk
        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    def rebuild(self, id: str = None, image: Union[int, str] = None) -> models.Action:
        assert id is not None, "droplet id must be set"
        assert image is not None, "image must be set"

        action = {
            "type": "rebuild",
            "image": image,
        }
        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    def rename(self, id: str = None, name: str = None) -> models.Action:
        assert id is not None, "droplet id must be set"
        assert name is not None, "name must be set"

        action = {
            "type": "rename",
            "name": name,
        }
        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    def change_kernel(self, id: str = None, kernel: int = None) -> models.Action:
        assert id is not None, "droplet id must be set"
        assert kernel is not None, "kernel must be set"

        action = {
            "type": "change_kernel",
            "kernel": kernel,
        }
        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

    def enable_ipv6(self, id: str = None) -> models.Action:
        return self._action(id, "enable_ipv6")

    def enable_private_networking(self, id: str = None) -> models.Action:
        return self._action(id, "enable_private_networking")

    def tag_action(
        self, tag_name: str = None, action: str = None
    ) -> List[models.Action]:
        assert tag_name is not None, "tag_name must be set"
        assert action is not None, "action must be set"

        params = {}
        if tag_name is not None:
            params["tag_name"] = tag_name

        action = {"type": action}

        res = self._client.request(
            endpoint="droplets/actions", method="post", json=action, params=params,
        )
        return [models.Action(**action) for action in res["actions"]]

    def snapshot(self, id: str = None, name: str = None) -> models.Action:
        assert id is not None, "droplet id must be set"

        action = {"type": "snapshot"}
        if name is not None:
            action["name"] = name

        res = self._client.request(
            endpoint="droplets/{id}/actions".format(id=id), method="post", json=action
        )
        return models.Action(**res["action"])

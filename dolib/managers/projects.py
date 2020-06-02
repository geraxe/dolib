from typing import List

from .. import models
from .base import AsyncBaseManager, BaseManager


class ProjectsManager(BaseManager):
    endpoint = "projects"
    name = "projects"

    def all(self) -> List[models.Project]:
        res = self._client.fetch_all(endpoint="projects", key="projects")
        return [models.Project(**proj) for proj in res]

    def get(self, id: str) -> models.Project:
        res = self._client.request(endpoint="projects/{id}".format(id=id), method="get")
        return models.Project(**res["project"])

    def create(self, project: models.Project) -> models.Project:
        res = self._client.request(
            endpoint="projects",
            method="post",
            data=project.json(
                include={"name", "description", "purpose", "environment"}
            ),
        )
        return models.Project(**res["project"])

    def update(self, project: models.Project) -> models.Project:
        res = self._client.request(
            endpoint="projects/{id}".format(id=project.id),
            method="put",
            data=project.json(
                include={"name", "description", "purpose", "environment", "is_default"}
            ),
        )
        return models.Project(**res["project"])

    def delete(self, project: models.Project) -> None:
        self._client.request(
            endpoint="projects/{id}".format(id=project.id), method="delete"
        )

    def resources(self, id: str) -> List[models.Project.Resource]:
        res = self._client.fetch_all(
            endpoint="projects/{id}/resources".format(id=id), key="resources"
        )
        return [models.Project.Resource(**resource) for resource in res]

    def assign_resources(
        self, id: str, resources: List[models.Project.Resource]
    ) -> List[models.Project.Resource]:
        post_json = {"resources": [res.urn for res in resources]}
        res = self._client.request(
            endpoint="projects/{id}/resources".format(id=id),
            method="post",
            json=post_json,
        )
        return [models.Project.Resource(**resource) for resource in res["resources"]]


class AsyncProjectsManager(AsyncBaseManager):
    endpoint = "projects"
    name = "projects"

    async def all(self) -> List[models.Project]:
        res = await self._client.fetch_all(endpoint="projects", key="projects")
        return [models.Project(**proj) for proj in res]

    async def get(self, id: str) -> models.Project:
        res = await self._client.request(
            endpoint="projects/{id}".format(id=id), method="get"
        )
        return models.Project(**res["project"])

    async def create(self, project: models.Project) -> models.Project:
        res = await self._client.request(
            endpoint="projects",
            method="post",
            data=project.json(
                include={"name", "description", "purpose", "environment"}
            ),
        )
        return models.Project(**res["project"])

    async def update(self, project: models.Project) -> models.Project:
        res = await self._client.request(
            endpoint="projects/{id}".format(id=project.id),
            method="put",
            data=project.json(
                include={"name", "description", "purpose", "environment", "is_default"}
            ),
        )
        return models.Project(**res["project"])

    async def delete(self, project: models.Project) -> None:
        await self._client.request(
            endpoint="projects/{id}".format(id=project.id), method="delete"
        )

    async def resources(self, id: str) -> List[models.Project.Resource]:
        res = await self._client.fetch_all(
            endpoint="projects/{id}/resources".format(id=id), key="resources"
        )
        return [models.Project.Resource(**resource) for resource in res]

    async def assign_resources(
        self, id: str, resources: List[models.Project.Resource]
    ) -> List[models.Project.Resource]:
        post_json = {"resources": [res.urn for res in resources]}
        res = await self._client.request(
            endpoint="projects/{id}/resources".format(id=id),
            method="post",
            json=post_json,
        )
        return [models.Project.Resource(**resource) for resource in res["resources"]]

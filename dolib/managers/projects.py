from typing import List

from .. import models
from .base import BaseManager


class ProjectsManager(BaseManager):
    endpoint = "projects"
    name = "projects"

    def all(self) -> List[models.Project]:
        res = self._client.fetch_all(endpoint="projects", key="projects")
        return [models.Project(**proj) for proj in res]

    def get(self, id: str = None):
        assert id is not None, "id must be set"

        res = self._client.request(endpoint="projects/{id}".format(id=id), method="get")
        return models.Project(**res["project"])

    def create(self, project: models.Project = None):
        assert project is not None, "project object must be set"

        res = self._client.request(
            endpoint="projects",
            method="post",
            data=project.json(
                include={"name", "description", "purpose", "environment"}
            ),
        )
        return models.Project(**res["project"])

    def update(self, project: models.Project = None):
        assert project is not None, "project object must be set"
        res = self._client.request(
            endpoint="projects/{id}".format(id=project.id),
            method="put",
            data=project.json(
                include={"name", "description", "purpose", "environment", "is_default"}
            ),
        )
        return models.Project(**res["project"])

    def delete(self, project: models.Project = None):
        assert project is not None, "project object must be set"

        self._client.request(
            endpoint="projects/{id}".format(id=project.id), method="delete",
        )

    def resources(self, id: str = None) -> List[models.Project.Resource]:
        assert id is not None, "project id must be set"

        res = self._client.fetch_all(
            endpoint="projects/{id}/resources".format(id=id), key="resources"
        )
        return [models.Project.Resource(**resource) for resource in res]

    def assign_resources(
        self, id: str = None, resources: List[models.Project.Resource] = None
    ) -> List[models.Project.Resource]:
        assert id is not None, "project id must be set"
        post_json = {"resources": [res.urn for res in resources]}
        res = self._client.request(
            endpoint="projects/{id}/resources".format(id=id),
            method="post",
            json=post_json,
        )
        return [models.Project.Resource(**resource) for resource in res["resources"]]

import pytest

from dolib.client import AsyncClient, Client
from dolib.models import Project


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_projects(client: Client) -> None:
    project = Project(
        name="dolib-test",
        description="Python library for digital ocean API",
        purpose="For test purposes",
        environment="Development",
    )

    # create project
    created_project = client.projects.create(project)
    assert isinstance(created_project, Project)
    assert created_project.id is not None

    # list projects
    projects = client.projects.all()
    assert len(projects) > 0

    # read project
    read_project = client.projects.get(str(projects[0].id))
    assert read_project.id == projects[0].id
    assert isinstance(read_project, Project)

    # update project
    read_project.is_default = False
    read_project.name = "dolib-test-renamed"
    updated_project = client.projects.update(read_project)
    assert isinstance(updated_project, Project)
    assert read_project.name == updated_project.name

    # assign resource
    volume = client.volumes.all()[-1]
    client.projects.assign_resources(
        str(read_project.id),
        [Project.Resource(urn=f"do:volume:{volume.id}")],
    )

    # list resources
    resources = client.projects.resources(str(read_project.id))
    assert len(resources) > 0

    # delete project
    client.projects.delete(project=read_project)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_projects(async_client: AsyncClient) -> None:
    project = Project(
        name="dolib-test",
        description="Python library for digital ocean API",
        purpose="For test purposes",
        environment="Development",
    )

    # create project
    created_project = await async_client.projects.create(project)
    assert isinstance(created_project, Project)
    assert created_project.id is not None

    # list projects
    projects = await async_client.projects.all()
    assert len(projects) > 0

    # read project
    read_project = await async_client.projects.get(str(projects[0].id))
    assert read_project.id == projects[0].id
    assert isinstance(read_project, Project)

    # update project
    read_project.is_default = False
    read_project.name = "dolib-test-renamed"
    updated_project = await async_client.projects.update(read_project)
    assert isinstance(updated_project, Project)
    assert read_project.name == updated_project.name

    # assign resource
    volume = (await async_client.volumes.all())[-1]
    await async_client.projects.assign_resources(
        str(read_project.id),
        [Project.Resource(urn=f"do:volume:{volume.id}")],
    )

    # list resources
    resources = await async_client.projects.resources(str(read_project.id))
    assert len(resources) > 0

    # delete project
    await async_client.projects.delete(project=read_project)

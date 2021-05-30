import pytest

from dolib.client import AsyncClient, Client
from dolib.models import Tag


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_tags(client: Client) -> None:
    tag = Tag(name="test")

    # create tag
    created_tag = client.tags.create(tag=tag)
    assert created_tag.resources is not None

    # read tag
    read_tag = client.tags.get(str(created_tag.name))
    assert read_tag.name == created_tag.name

    # list tags
    tags = client.tags.all()
    tags_count = len(tags)
    assert tags_count > 0

    droplet = client.droplets.all()[0]
    # tag resources
    client.tags.tag_resources(
        read_tag.name,
        [Tag.Resource(resource_id=str(droplet.id), resource_type="droplet")],
    )

    # untag resources
    client.tags.untag_resources(
        read_tag.name,
        [Tag.Resource(resource_id=str(droplet.id), resource_type="droplet")],
    )

    # delete tag
    client.tags.delete(read_tag)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_tags(async_client: AsyncClient) -> None:
    tag = Tag(name="test")

    # create tag
    created_tag = await async_client.tags.create(tag=tag)
    assert created_tag.resources is not None

    # read tag
    read_tag = await async_client.tags.get(str(created_tag.name))
    assert read_tag.name == created_tag.name

    # list tags
    tags = await async_client.tags.all()
    tags_count = len(tags)
    assert tags_count > 0

    droplet = (await async_client.droplets.all())[0]
    # tag resources
    await async_client.tags.tag_resources(
        read_tag.name,
        [Tag.Resource(resource_id=str(droplet.id), resource_type="droplet")],
    )

    # untag resources
    await async_client.tags.untag_resources(
        read_tag.name,
        [Tag.Resource(resource_id=str(droplet.id), resource_type="droplet")],
    )

    # delete tag
    await async_client.tags.delete(read_tag)

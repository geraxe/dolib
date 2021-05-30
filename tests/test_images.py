import pytest

from dolib.client import AsyncClient, Client
from dolib.models import Action, Image


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_images(client: Client) -> None:
    image = Image(
        name="dolib-test-image",
        region="fra1",
        url="http://cloud-images.ubuntu.com/minimal/releases/bionic/"
        "release/ubuntu-18.04-minimal-cloudimg-amd64.img",
        distribution="Ubuntu",
        description="Cloud-optimized image w/ small footprint",
        tags=["test"],
    )

    # create image
    created_image = client.images.create(image)
    assert isinstance(created_image, Image)
    assert created_image.id is not None

    # list images
    images = client.images.all()
    assert len(images) > 0

    # filter images
    filtered_images = client.images.filter()
    assert len(images) < len(filtered_images)
    filtered_images = client.images.filter(
        private="True", type="custom", tag_name="test"
    )
    assert len(filtered_images) > 0

    # read image
    read_image = client.images.get(str(created_image.id))
    assert read_image.id == created_image.id
    assert isinstance(read_image, Image)

    # update image
    created_image.name = "dolib-test-image-renamed"
    updated_image = client.images.update(created_image)
    assert created_image.name == updated_image.name

    # transfer image
    transfer_action = client.images.transfer(str(created_image.id), "ams2")
    assert isinstance(transfer_action, Action)
    assert transfer_action.status == "in-progress"

    # get action
    action = client.images.action(
        str(created_image.id), action_id=str(transfer_action.id)
    )
    assert isinstance(action, Action)
    assert action.type == "transfer"

    # list actions
    actions = client.images.actions(str(created_image.id))
    assert len(actions) > 0

    # convert image
    convert_action = client.images.convert(str(created_image.id))
    assert isinstance(convert_action, Action)
    assert convert_action.status == "completed"

    # delete image
    client.images.delete(image=created_image)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_images(async_client: AsyncClient) -> None:
    image = Image(
        name="dolib-test-image",
        region="fra1",
        url="http://cloud-images.ubuntu.com/minimal/releases/bionic/"
        "release/ubuntu-18.04-minimal-cloudimg-amd64.img",
        distribution="Ubuntu",
        description="Cloud-optimized image w/ small footprint",
        tags=["test"],
    )

    # create image
    created_image = await async_client.images.create(image)
    assert isinstance(created_image, Image)
    assert created_image.id is not None

    # list images
    images = await async_client.images.all()
    assert len(images) > 0

    # filter images
    filtered_images = await async_client.images.filter()
    assert len(images) < len(filtered_images)
    filtered_images = await async_client.images.filter(
        private="True", type="custom", tag_name="test"
    )
    assert len(filtered_images) > 0

    # read image
    read_image = await async_client.images.get(str(created_image.id))
    assert read_image.id == created_image.id
    assert isinstance(read_image, Image)

    # update image
    created_image.name = "dolib-test-image-renamed"
    updated_image = await async_client.images.update(created_image)
    assert created_image.name == updated_image.name

    # transfer image
    transfer_action = await async_client.images.transfer(str(created_image.id), "ams2")
    assert isinstance(transfer_action, Action)
    assert transfer_action.status == "in-progress"

    # get action
    action = await async_client.images.action(
        str(created_image.id), action_id=str(transfer_action.id)
    )
    assert isinstance(action, Action)
    assert action.type == "transfer"

    # list actions
    actions = await async_client.images.actions(str(created_image.id))
    assert len(actions) > 0

    # convert image
    convert_action = await async_client.images.convert(str(created_image.id))
    assert isinstance(convert_action, Action)
    assert convert_action.status == "completed"

    # delete image
    await async_client.images.delete(image=created_image)

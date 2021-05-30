import pytest

from dolib.client import AsyncClient, Client
from dolib.models import Action, Snapshot, Volume


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_volumes(client: Client) -> None:
    volume = Volume(
        name="dolib-test-volume",
        region="fra1",
        size_gigabytes=1,
    )

    # create volume
    created_volume = client.volumes.create(volume)
    assert isinstance(created_volume, Volume)
    assert created_volume.id is not None

    # list volumes
    volumes = client.volumes.all()
    assert len(volumes) > 0

    # read volume
    read_volume = client.volumes.get(str(created_volume.id))
    assert read_volume.id == created_volume.id
    assert isinstance(read_volume, Volume)

    # resize volume
    resize_action = client.volumes.resize(str(created_volume.id), size_gigabytes=2)
    assert isinstance(resize_action, Action)
    assert resize_action.status == "done"

    droplet = client.droplets.all()[-1]

    # attach
    attach_action = client.volumes.attach(read_volume, droplet_id=droplet.id)
    assert isinstance(attach_action, Action)
    assert attach_action.status == "in-progress"

    # detach
    detach_action = client.volumes.detach(read_volume, droplet_id=droplet.id)
    assert isinstance(detach_action, Action)
    assert detach_action.status == "in-progress"

    # attach by name
    attach_action = client.volumes.attach(volume, droplet_id=droplet.id)
    assert isinstance(attach_action, Action)
    assert attach_action.status == "in-progress"

    # detach by name
    detach_action = client.volumes.detach(volume, droplet_id=droplet.id)
    assert isinstance(detach_action, Action)
    assert detach_action.status == "in-progress"

    # try attach broken region
    volume.region = None
    client.volumes.attach(volume, droplet_id=droplet.id)

    # create snapshot
    snapshot = client.volumes.create_snapshot(
        str(created_volume.id), Snapshot(name="test-volume-snapshot", tags=["test"])
    )
    assert snapshot.id is not None

    # list snapshots
    snapshots = client.volumes.snapshots(str(created_volume.id))
    assert len(snapshots) > 0

    # list actions
    actions = client.volumes.actions(str(created_volume.id))
    assert len(actions) > 0

    # delete volume
    client.volumes.delete(volume=created_volume)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_volumes(async_client: AsyncClient) -> None:
    volume = Volume(
        name="dolib-test-volume",
        region="fra1",
        size_gigabytes=1,
    )

    # create volume
    created_volume = await async_client.volumes.create(volume)
    assert isinstance(created_volume, Volume)
    assert created_volume.id is not None

    # list volumes
    volumes = await async_client.volumes.all()
    assert len(volumes) > 0

    # read volume
    read_volume = await async_client.volumes.get(str(created_volume.id))
    assert read_volume.id == created_volume.id
    assert isinstance(read_volume, Volume)

    # resize volume
    resize_action = await async_client.volumes.resize(
        str(created_volume.id), size_gigabytes=2
    )
    assert isinstance(resize_action, Action)
    assert resize_action.status == "done"

    droplet = (await async_client.droplets.all())[-1]

    # attach
    attach_action = await async_client.volumes.attach(
        read_volume, droplet_id=droplet.id
    )
    assert isinstance(attach_action, Action)
    assert attach_action.status == "in-progress"

    # detach
    detach_action = await async_client.volumes.detach(
        read_volume, droplet_id=droplet.id
    )
    assert isinstance(detach_action, Action)
    assert detach_action.status == "in-progress"

    # attach by name
    attach_action = await async_client.volumes.attach(volume, droplet_id=droplet.id)
    assert isinstance(attach_action, Action)
    assert attach_action.status == "in-progress"

    # detach by name
    detach_action = await async_client.volumes.detach(volume, droplet_id=droplet.id)
    assert isinstance(detach_action, Action)
    assert detach_action.status == "in-progress"

    # try attach broken region
    volume.region = None
    await async_client.volumes.attach(volume, droplet_id=droplet.id)

    # create snapshot
    snapshot = await async_client.volumes.create_snapshot(
        str(created_volume.id), Snapshot(name="test-volume-snapshot", tags=["test"])
    )
    assert snapshot.id is not None

    # list snapshots
    snapshots = await async_client.volumes.snapshots(str(created_volume.id))
    assert len(snapshots) > 0

    # list actions
    actions = await async_client.volumes.actions(str(created_volume.id))
    assert len(actions) > 0

    # delete volume
    await async_client.volumes.delete(volume=created_volume)

import pytest

from dolib.client import AsyncClient, Client
from dolib.models import Snapshot


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_snapshots(client: Client) -> None:

    # list snapshots
    snapshots = client.snapshots.all()
    snapshots_count = len(snapshots)
    assert snapshots_count > 0

    # filter snapshots by type
    droplet_snapshots = client.snapshots.all(resource_type="droplet")
    droplet_snapshots_count = len(droplet_snapshots)
    assert droplet_snapshots_count > 0

    # read snapshot
    read_snapshot = client.snapshots.get(str(snapshots[0].id))
    assert read_snapshot.id == snapshots[0].id
    assert isinstance(read_snapshot, Snapshot)

    # delete snapshot
    client.snapshots.delete(snapshot=read_snapshot)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_snapshots(async_client: AsyncClient) -> None:

    # list snapshots
    snapshots = await async_client.snapshots.all()
    snapshots_count = len(snapshots)
    assert snapshots_count > 0

    # filter snapshots by type
    droplet_snapshots = await async_client.snapshots.all(resource_type="droplet")
    droplet_snapshots_count = len(droplet_snapshots)
    assert droplet_snapshots_count > 0

    # read snapshot
    read_snapshot = await async_client.snapshots.get(str(snapshots[0].id))
    assert read_snapshot.id == snapshots[0].id
    assert isinstance(read_snapshot, Snapshot)

    # delete snapshot
    await async_client.snapshots.delete(snapshot=read_snapshot)

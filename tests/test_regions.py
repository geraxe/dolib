import pytest

from dolib.client import AsyncClient, Client


@pytest.mark.vcr
@pytest.mark.block_network()
def test_regions(client: Client) -> None:
    # list regions
    regions = client.regions.all()
    assert len(regions) > 0


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_regions(async_client: AsyncClient) -> None:
    # list regions
    regions = await async_client.regions.all()
    assert len(regions) > 0

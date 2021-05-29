import pytest

from dolib.client import AsyncClient, Client
from dolib.models import CDNEndpoint


@pytest.mark.vcr()
@pytest.mark.block_network()
def test_crud_cdns(client: Client) -> None:

    endpoint = CDNEndpoint(
        origin="e183e06c-0252-4e0c-85bb-2fe17eb87169.ams3.digitaloceanspaces.com",
        ttl=1800,
    )

    # create cdn endpoint
    endpoint = client.cdn_endpoints.create(endpoint=endpoint)
    assert endpoint.ttl == 1800
    assert endpoint.id is not None

    # read cdn endpoint
    read_endpoint = client.cdn_endpoints.get(str(endpoint.id))
    assert read_endpoint.id == endpoint.id

    # list cdn endpoints
    endpoints = client.cdn_endpoints.all()
    assert len(endpoints) > 0

    # update cdn endpoint
    read_endpoint.ttl = 600
    updated_endpoint = client.cdn_endpoints.update(read_endpoint)
    assert updated_endpoint.ttl == 600

    # flush cache
    client.cdn_endpoints.flush_cache(str(endpoint.id), files=["testfile.txt"])
    client.cdn_endpoints.flush_cache(str(endpoint.id))

    # delete cdn endpoints
    client.cdn_endpoints.delete(endpoint=endpoint)


@pytest.mark.vcr()
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_cdns(async_client: AsyncClient) -> None:

    endpoint = CDNEndpoint(
        origin="e183e06c-0252-4e0c-85bb-2fe17eb87169.ams3.digitaloceanspaces.com",
        ttl=1800,
    )

    # create cdn endpoint
    endpoint = await async_client.cdn_endpoints.create(endpoint=endpoint)
    assert endpoint.ttl == 1800
    assert endpoint.id is not None

    # read cdn endpoint
    read_endpoint = await async_client.cdn_endpoints.get(str(endpoint.id))
    assert read_endpoint.id == endpoint.id

    # list cdn endpoints
    endpoints = await async_client.cdn_endpoints.all()
    assert len(endpoints) > 0

    # update cdn endpoint
    read_endpoint.ttl = 600
    updated_endpoint = await async_client.cdn_endpoints.update(read_endpoint)
    assert updated_endpoint.ttl == 600

    # flush cache
    await async_client.cdn_endpoints.flush_cache(
        str(endpoint.id), files=["testfile.txt"]
    )
    await async_client.cdn_endpoints.flush_cache(str(endpoint.id))

    # delete cdn endpoints
    await async_client.cdn_endpoints.delete(endpoint=endpoint)

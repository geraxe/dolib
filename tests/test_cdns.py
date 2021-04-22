import pytest

from dolib.client import Client
from dolib.models import CDNEndpoint


@pytest.mark.vcr()
@pytest.mark.block_network()
def test_crud_cdns() -> None:
    client = Client(token="fake_token")

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

    # delete cdn endpoints
    client.cdn_endpoints.delete(endpoint=endpoint)

import sys
from unittest.mock import MagicMock, patch

import pytest
from httpx import HTTPStatusError
from pkg_resources import DistributionNotFound

from dolib import AsyncClient, Client
from dolib.client import BaseClient


@patch("pkg_resources.get_distribution", side_effect=DistributionNotFound)
def test_version(mock: MagicMock) -> None:
    del sys.modules["dolib.__version__"]
    from dolib.__version__ import __version__

    assert __version__ is None


def test_base_client() -> None:
    with pytest.raises(NotImplementedError):
        BaseClient()


@pytest.mark.vcr
@pytest.mark.block_network()
def test_client(client: Client) -> None:
    client.request_raw(endpoint="account", method="get")

    client.fetch_all(endpoint="fake_links", key="fake_links")
    firewalls = client.fetch_all(endpoint="firewalls", key="firewalls")
    assert firewalls == []

    clusters = client.fetch_all(
        endpoint="kubernetes/clusters", key="kubernetes_clusters"
    )
    assert clusters == []

    with pytest.raises(HTTPStatusError):
        client.fetch_all(endpoint="non_existent_page", key="error")


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_client(async_client: AsyncClient) -> None:
    await async_client.request_raw(endpoint="account", method="get")

    await async_client.fetch_all(endpoint="fake_links", key="fake_links")
    firewalls = await async_client.fetch_all(endpoint="firewalls", key="firewalls")
    assert firewalls == []

    clusters = await async_client.fetch_all(
        endpoint="kubernetes/clusters", key="kubernetes_clusters"
    )
    assert clusters == []

    with pytest.raises(HTTPStatusError):
        await async_client.fetch_all(endpoint="non_existent_page", key="error")

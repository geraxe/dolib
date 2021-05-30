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
    with pytest.raises(ValueError, match="API token must be specified"):
        BaseClient()
    with pytest.raises(NotImplementedError):
        BaseClient(token="fake_token")


@pytest.mark.vcr
@pytest.mark.block_network()
def test_client(client: Client) -> None:

    # without ratelimits in header
    client.request_raw(endpoint="account/keys", method="get")
    assert client._ratelimit_limit is None
    assert client._ratelimit_remaining is None
    assert client._ratelimit_reset is None

    client.request_raw(endpoint="account", method="get")
    assert client._ratelimit_limit > 0
    assert client._ratelimit_remaining > 0
    assert client._ratelimit_reset > 0

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

    # without ratelimits in header
    await async_client.request_raw(endpoint="account/keys", method="get")
    assert async_client._ratelimit_limit is None
    assert async_client._ratelimit_remaining is None
    assert async_client._ratelimit_reset is None

    await async_client.request_raw(endpoint="account", method="get")
    assert async_client._ratelimit_limit > 0
    assert async_client._ratelimit_remaining > 0
    assert async_client._ratelimit_reset > 0

    await async_client.fetch_all(endpoint="fake_links", key="fake_links")
    firewalls = await async_client.fetch_all(endpoint="firewalls", key="firewalls")
    assert firewalls == []

    clusters = await async_client.fetch_all(
        endpoint="kubernetes/clusters", key="kubernetes_clusters"
    )
    assert clusters == []

    with pytest.raises(HTTPStatusError):
        await async_client.fetch_all(endpoint="non_existent_page", key="error")

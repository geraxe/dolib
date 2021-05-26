import pytest

from dolib import AsyncClient, Client


@pytest.mark.vcr
@pytest.mark.block_network()
def test_account(client: Client) -> None:
    account = client.account.get()
    assert account.email_verified is True
    assert account.status == "active"


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_account(async_client: AsyncClient) -> None:
    account = await async_client.account.get()
    assert account.email_verified is True
    assert account.status == "active"

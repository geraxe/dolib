import pytest

from dolib import AsyncClient, Client
from dolib.models import Balance, BillingHistory


@pytest.mark.vcr
@pytest.mark.block_network()
def test_account(client: Client) -> None:
    account = client.account.get()
    assert account.email_verified is True
    assert account.status == "active"

    histories = client.account.billing_history()
    assert len(histories) > 0

    last_history = histories[0]
    assert last_history.type in ["Payment", "Invoice"]
    assert isinstance(last_history, BillingHistory)

    balance = client.account.balance()
    assert isinstance(balance, Balance)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_account(async_client: AsyncClient) -> None:
    account = await async_client.account.get()
    assert account.email_verified is True
    assert account.status == "active"

    histories = await async_client.account.billing_history()
    assert len(histories) > 0

    last_history = histories[0]
    assert last_history.type in ["Payment", "Invoice"]
    assert isinstance(last_history, BillingHistory)

    balance = await async_client.account.balance()
    assert isinstance(balance, Balance)

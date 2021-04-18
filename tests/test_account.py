import pytest

from dolib.client import Client


@pytest.mark.vcr
@pytest.mark.block_network()
def test_account() -> None:
    client = Client(token="fake_token")

    account = client.account.get()
    assert account.email_verified is True
    assert account.status == "active"

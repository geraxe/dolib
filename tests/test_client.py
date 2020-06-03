import pytest
from dolib.client import Client


@pytest.mark.vcr
@pytest.mark.block_network()
def test_client() -> None:
    with pytest.raises(NotImplementedError):
        client = Client()

    client = Client(token="fake_token")

    client.account.get()
    assert client._ratelimit_limit is not None and client._ratelimit_limit > 0
    assert client._ratelimit_remaining is not None and client._ratelimit_remaining > 0
    assert client._ratelimit_reset is not None and client._ratelimit_reset > 0

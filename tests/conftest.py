import pytest

from dolib import AsyncClient, Client


@pytest.fixture(scope="module")
def vcr_config() -> dict:
    return {
        "decode_compressed_response": True,
        "filter_headers": ["authorization"],
        #        "record_mode": "rewrite",
    }


@pytest.fixture
def client() -> Client:
    return Client(token="fake_token")


@pytest.fixture
async def async_client() -> AsyncClient:
    async with AsyncClient(token="fake_token") as async_client:
        return async_client

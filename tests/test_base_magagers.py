from dolib.client import AsyncClient, Client
from dolib.managers.base import AsyncBaseManager, BaseManager


def test_base_managers() -> None:

    client = Client(token="fake_token")
    manager = BaseManager(client=client)

    assert manager._client == client

    async_client = AsyncClient(token="fake_token")
    async_manager = AsyncBaseManager(client=async_client)

    assert async_manager._client == async_client

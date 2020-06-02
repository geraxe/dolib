from .. import client  # import Client


class AsyncBaseManager:
    name = "base"
    is_abstract = True

    def __init__(self, client: "client.AsyncClient") -> None:
        self._client = client


class BaseManager:
    name = "base"
    is_abstract = True

    def __init__(self, client: "client.Client") -> None:
        self._client = client

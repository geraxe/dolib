from .. import client  # import Client


class BaseManager:
    name = "base"
    is_abstract = True

    def __init__(self, client: "client.Client") -> None:
        self._client = client

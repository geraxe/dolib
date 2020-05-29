from .. import client  # import Client


class BaseManager:
    name = "base"
    is_abstract = True

    def __init__(self, client: "client.Client", *args, **kwargs):
        self._client = client

from typing import Any, Dict, List, Optional

import requests

from . import managers as do_managers


class Client:
    API_DOMAIN = "api.digitalocean.com"
    API_VERSION = "v2"

    def __init__(self, token: str = None):
        if token is None:
            raise NotImplementedError("Need you api token.")

        self._token = token
        self._ratelimit_limit: Optional[int] = None
        self._ratelimit_remaining: Optional[int] = None
        self._ratelimit_reset: Optional[int] = None
        for manager in do_managers.__all__:
            klass = getattr(do_managers, manager)
            if issubclass(klass, do_managers.base.BaseManager):
                obj = klass(client=self)
                setattr(self, klass.endpoint, obj)

        self.headers = {
            "Authorization": "Bearer {token}".format(token=self._token),
            "Content-Type": "application/json",
        }

    def _process_response(self, response):
        if "Ratelimit-Limit" in response.headers:
            self._ratelimit_limit = int(response.headers.get("Ratelimit-Limit"))
        if "Ratelimit-Remaining" in response.headers:
            self._ratelimit_remaining = int(response.headers.get("Ratelimit-Remaining"))
        if "Ratelimit-Reset" in response.headers:
            self._ratelimit_reset = int(response.headers.get("Ratelimit-Reset"))

    def request_raw(
        self,
        endpoint: str = "account",
        method: str = "get",
        params: dict = {},
        json: dict = None,
        data: str = None,
    ):
        assert method in [
            "get",
            "post",
            "put",
            "delete",
            "head",
        ], "Invalid method {method}".format(method=method)

        url = "https://{domain}/{version}/{endpoint}".format(
            domain=self.API_DOMAIN, version=self.API_VERSION, endpoint=endpoint,
        )

        response = requests.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            json=json,
            data=data,
        )

        # raise exceptions in case of errors
        if not response.ok:
            print(response.content)
            response.raise_for_status()

        # save data to client from response
        self._process_response(response)

        return response

    def request(self, *args, **kwargs) -> Dict[str, Any]:
        response = self.request_raw(*args, **kwargs)
        if response.status_code in [
            requests.codes["no_content"],
            requests.codes["accepted"],
        ]:
            return {}
        return response.json()

    def fetch_all(
        self, endpoint: str, key: str, params: dict = {},
    ) -> List[Dict[str, Any]]:
        def get_next_page(result={}):
            if (
                "links" not in result
                or "pages" not in result["links"]
                or "next" not in result["links"]["pages"]
            ):
                return None
            return result["links"]["pages"]["next"]

        params["per_page"] = 200
        response = self.request(endpoint=endpoint, params=params)

        # in case of strange result like " "firewalls": null "
        if response[key] is None:
            result = []
        elif type(response[key]) == list:
            result = response[key]
        else:
            result = list(response[key])
        while True:
            next_url = get_next_page(response)
            if next_url is None:
                break
            res = requests.get(next_url, headers=self.headers)

            if not res.ok:
                res.raise_for_status()
            response = res.json()
            result += response[key]

        return result

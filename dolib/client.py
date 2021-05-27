import typing as t
from types import TracebackType

import httpx

from . import managers as do_managers
from .__version__ import __version__


class BaseClient:
    API_DOMAIN = "api.digitalocean.com"
    API_VERSION = "v2"

    account: t.Optional[do_managers.AccountManager] = None
    actions: t.Optional[do_managers.ActionsManager] = None
    apps: t.Optional[do_managers.AppsManager] = None
    cdn_endpoints: t.Optional[do_managers.CDNEndpointsManager] = None
    certificates: t.Optional[do_managers.CertificatesManager] = None
    databases: t.Optional[do_managers.DatabasesManager] = None
    domains: t.Optional[do_managers.DomainsManager] = None
    droplets: t.Optional[do_managers.DropletsManager] = None
    firewalls: t.Optional[do_managers.FirewallsManager] = None
    floating_ips: t.Optional[do_managers.FloatingIPsManager] = None
    images: t.Optional[do_managers.ImagesManager] = None
    invoices: t.Optional[do_managers.InvoicesManager] = None
    kubernetes: t.Optional[do_managers.KubernetesManager] = None
    load_balancers: t.Optional[do_managers.LoadBalancersManager] = None
    projects: t.Optional[do_managers.ProjectsManager] = None
    regions: t.Optional[do_managers.RegionsManager] = None
    registry: t.Optional[do_managers.RegistryManager] = None
    snapshots: t.Optional[do_managers.SnapshotsManager] = None
    ssh_keys: t.Optional[do_managers.SSHKeysManager] = None
    tags: t.Optional[do_managers.TagsManager] = None
    volumes: t.Optional[do_managers.VolumesManager] = None
    vpcs: t.Optional[do_managers.VPCsManager] = None

    def __init__(self, token: str = None):
        if token is None:
            raise NotImplementedError("Need you api token.")
        self._token = token
        self._ratelimit_limit: t.Optional[int] = None
        self._ratelimit_remaining: t.Optional[int] = None
        self._ratelimit_reset: t.Optional[int] = None
        self._load_managers()

        self.headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
            "User-Agent": f"dolib/{__version__}",
            # FIXME:  our test lib(vcrpy) for httpx have bugs with gzip and deflate
            # https://github.com/kevin1024/vcrpy/issues/550
            "Accept-Encoding": "",
        }

    def _load_managers(self) -> None:
        for manager in do_managers.__all__:
            klass = getattr(do_managers, manager)
            if issubclass(klass, do_managers.base.BaseManager):
                obj = klass(client=self)
                setattr(self, klass.endpoint, obj)

    def _process_response(self, response: httpx.Response) -> None:
        if "Ratelimit-Limit" in response.headers:
            self._ratelimit_limit = int(response.headers.get("Ratelimit-Limit"))
        if "Ratelimit-Remaining" in response.headers:
            self._ratelimit_remaining = int(response.headers.get("Ratelimit-Remaining"))
        if "Ratelimit-Reset" in response.headers:
            self._ratelimit_reset = int(response.headers.get("Ratelimit-Reset"))


class Client(BaseClient):
    def _load_managers(self) -> None:
        for manager in do_managers.__sync_managers__:
            klass = getattr(do_managers, manager)
            if issubclass(klass, do_managers.base.BaseManager):
                obj = klass(client=self)
                setattr(self, klass.endpoint, obj)

    def request_raw(
        self,
        endpoint: str = "account",
        method: str = "get",
        params: dict = {},
        json: dict = None,
        data: str = None,
    ) -> httpx.Response:
        assert method in [
            "get",
            "post",
            "put",
            "delete",
            "head",
        ], "Invalid method {method}".format(method=method)

        url = "https://{domain}/{version}/{endpoint}".format(
            domain=self.API_DOMAIN,
            version=self.API_VERSION,
            endpoint=endpoint,
        )

        response = httpx.request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            json=json,
            content=data,
        )

        # raise exceptions in case of errors
        response.raise_for_status()

        print(response.content)
        # save data to client from response
        self._process_response(response)

        return response

    def request(
        self,
        endpoint: str = "account",
        method: str = "get",
        params: dict = {},
        json: dict = None,
        data: str = None,
    ) -> t.Dict[str, t.Any]:
        response = self.request_raw(endpoint, method, params, json, data)
        if response.status_code in [httpx.codes.NO_CONTENT]:
            return {}
        return response.json()

    def fetch_all(
        self,
        endpoint: str,
        key: str,
        params: dict = {},
    ) -> t.List[t.Dict[str, t.Any]]:
        def get_next_page(result: t.Dict[str, t.Any] = None) -> t.Optional[str]:
            if (
                result is None
                or "links" not in result
                or "pages" not in result["links"]
                or "next" not in result["links"]["pages"]
            ):
                return None
            return result["links"]["pages"]["next"]

        params["per_page"] = 200
        response = self.request(endpoint=endpoint, params=params)

        result: t.List[t.Any] = []

        # in case of strange result like GET /apps
        if key not in response:
            result = []
        # in case of strange result like " "firewalls": null "
        elif response[key] is None:
            result = []
        elif isinstance(response[key], list):
            result = response[key]
        else:
            result = list(response[key])

        while True:
            next_url = get_next_page(response)
            if next_url is None:
                break
            res = httpx.get(next_url, headers=self.headers)

            res.raise_for_status()
            response = res.json()
            result += response[key]

        return result


class AsyncClient(BaseClient):
    def __init__(self, token: str = None):
        super().__init__(token)

    def _load_managers(self) -> None:
        for manager in do_managers.__async_managers__:
            klass = getattr(do_managers, manager)
            if issubclass(klass, do_managers.base.AsyncBaseManager):
                obj = klass(client=self)
                setattr(self, klass.endpoint, obj)

    async def request_raw(
        self,
        endpoint: str = "account",
        method: str = "get",
        params: dict = {},
        json: dict = None,
        data: str = None,
    ) -> httpx.Response:
        assert method in [
            "get",
            "post",
            "put",
            "delete",
            "head",
        ], "Invalid method {method}".format(method=method)

        url = "https://{domain}/{version}/{endpoint}".format(
            domain=self.API_DOMAIN,
            version=self.API_VERSION,
            endpoint=endpoint,
        )

        async with httpx.AsyncClient() as async_client:
            response = await async_client.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=json,
                content=data,
            )

        # raise exceptions in case of errors
        response.raise_for_status()

        # save data to client from response
        self._process_response(response)

        return response

    async def request(
        self,
        endpoint: str = "account",
        method: str = "get",
        params: dict = {},
        json: dict = None,
        data: str = None,
    ) -> t.Dict[str, t.Any]:
        response = await self.request_raw(endpoint, method, params, json, data)
        if response.status_code in [httpx.codes.NO_CONTENT]:
            return {}
        return response.json()

    async def fetch_all(
        self,
        endpoint: str,
        key: str,
        params: dict = {},
    ) -> t.List[t.Dict[str, t.Any]]:
        def get_next_page(result: t.Dict[str, t.Any] = None) -> t.Optional[str]:
            if (
                result is None
                or "links" not in result
                or "pages" not in result["links"]
                or "next" not in result["links"]["pages"]
            ):
                return None
            return result["links"]["pages"]["next"]

        params["per_page"] = 200
        response = await self.request(endpoint=endpoint, params=params)

        result: t.List[t.Any] = []

        # in case of strange result like GET /apps
        if key not in response:
            result = []
        # in case of strange result like " "firewalls": null "
        elif response[key] is None:
            result = []
        elif isinstance(response[key], list):
            result = response[key]
        else:
            result = list(response[key])

        while True:
            next_url = get_next_page(response)
            if next_url is None:
                break

            async with httpx.AsyncClient() as async_client:
                res = await async_client.get(next_url, headers=self.headers)
            res.raise_for_status()
            response = res.json()
            result += response[key]

        return result

    async def __aenter__(self) -> "AsyncClient":
        return self

    async def __aexit__(
        self,
        exc_type: t.Type[BaseException] = None,
        exc_value: BaseException = None,
        traceback: TracebackType = None,
    ) -> None:
        pass

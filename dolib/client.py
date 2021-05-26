import typing as t
from types import TracebackType

import httpx

from . import managers as mn
from .__version__ import __version__


class BaseClient:
    API_DOMAIN = "api.digitalocean.com"
    API_VERSION = "v2"

    account: t.Optional[t.Union[mn.AccountManager, mn.AsyncAccountManager]] = None
    actions: t.Optional[t.Union[mn.ActionsManager, mn.AsyncActionsManager]] = None
    cdn_endpoints: t.Optional[
        t.Union[mn.CDNEndpointsManager, mn.AsyncCDNEndpointsManager]
    ] = None
    certificates: t.Optional[
        t.Union[mn.CertificatesManager, mn.AsyncCertificatesManager]
    ] = None
    databases: t.Optional[t.Union[mn.DatabasesManager, mn.AsyncDatabasesManager]] = None
    domains: t.Optional[t.Union[mn.DomainsManager, mn.AsyncDomainsManager]] = None
    droplets: t.Optional[t.Union[mn.DropletsManager, mn.AsyncDropletsManager]] = None
    firewalls: t.Optional[t.Union[mn.FirewallsManager, mn.AsyncFirewallsManager]] = None
    floating_ips: t.Optional[
        t.Union[mn.FloatingIPsManager, mn.AsyncFloatingIPsManager]
    ] = None
    images: t.Optional[t.Union[mn.ImagesManager, mn.AsyncImagesManager]] = None
    invoices: t.Optional[t.Union[mn.InvoicesManager, mn.AsyncInvoicesManager]] = None
    kubernetes: t.Optional[
        t.Union[mn.KubernetesManager, mn.AsyncKubernetesManager]
    ] = None
    load_balancers: t.Optional[
        t.Union[mn.LoadBalancersManager, mn.AsyncLoadBalancersManager]
    ] = None
    projects: t.Optional[t.Union[mn.ProjectsManager, mn.AsyncProjectsManager]] = None
    regions: t.Optional[t.Union[mn.RegionsManager, mn.AsyncRegionsManager]] = None
    registry: t.Optional[t.Union[mn.RegistryManager, mn.AsyncRegistryManager]] = None
    snapshots: t.Optional[t.Union[mn.SnapshotsManager, mn.AsyncSnapshotsManager]] = None
    ssh_keys: t.Optional[t.Union[mn.SSHKeysManager, mn.AsyncSSHKeysManager]] = None
    tags: t.Optional[t.Union[mn.TagsManager, mn.AsyncTagsManager]] = None
    volumes: t.Optional[t.Union[mn.VolumesManager, mn.AsyncVolumesManager]] = None
    vpcs: t.Optional[t.Union[mn.VPCsManager, mn.AsyncVPCsManager]] = None

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
        for manager in mn.__all__:
            klass = getattr(mn, manager)
            if issubclass(klass, mn.base.BaseManager):
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
        for manager in mn.__sync_managers__:
            klass = getattr(mn, manager)
            if issubclass(klass, mn.base.BaseManager):
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

        # in case of strange result like " "firewalls": null "
        if response[key] is None:
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
        for manager in mn.__async_managers__:
            klass = getattr(mn, manager)
            if issubclass(klass, mn.base.AsyncBaseManager):
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

        # in case of strange result like " "firewalls": null "
        if response[key] is None:
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

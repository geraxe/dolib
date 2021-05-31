import typing as t
from types import TracebackType

import httpx

from . import managers as mn
from .__version__ import __version__


class BaseClient:
    API_DOMAIN = "api.digitalocean.com"
    API_VERSION = "v2"

    def __init__(self, token: str = None):
        if token is None:
            raise ValueError("API token must be specified.")
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
        raise NotImplementedError("_load_managers must be implemented.")

    def _process_response(self, response: httpx.Response) -> None:
        if "Ratelimit-Limit" in response.headers:
            self._ratelimit_limit = int(response.headers.get("Ratelimit-Limit"))
        if "Ratelimit-Remaining" in response.headers:
            self._ratelimit_remaining = int(response.headers.get("Ratelimit-Remaining"))
        if "Ratelimit-Reset" in response.headers:
            self._ratelimit_reset = int(response.headers.get("Ratelimit-Reset"))


class Client(BaseClient):

    account: t.Optional[mn.AccountManager] = None
    actions: t.Optional[mn.ActionsManager] = None
    cdn_endpoints: t.Optional[mn.CDNEndpointsManager] = None
    certificates: t.Optional[mn.CertificatesManager] = None
    databases: t.Optional[mn.DatabasesManager] = None
    domains: t.Optional[mn.DomainsManager] = None
    droplets: t.Optional[mn.DropletsManager] = None
    firewalls: t.Optional[mn.FirewallsManager] = None
    floating_ips: t.Optional[mn.FloatingIPsManager] = None
    images: t.Optional[mn.ImagesManager] = None
    invoices: t.Optional[mn.InvoicesManager] = None
    kubernetes: t.Optional[mn.KubernetesManager] = None
    load_balancers: t.Optional[mn.LoadBalancersManager] = None
    projects: t.Optional[mn.ProjectsManager] = None
    regions: t.Optional[mn.RegionsManager] = None
    registry: t.Optional[mn.RegistryManager] = None
    snapshots: t.Optional[mn.SnapshotsManager] = None
    ssh_keys: t.Optional[mn.SSHKeysManager] = None
    tags: t.Optional[mn.TagsManager] = None
    volumes: t.Optional[mn.VolumesManager] = None
    vpcs: t.Optional[mn.VPCsManager] = None

    def _load_managers(self) -> None:
        for manager in mn.__sync_managers__:
            klass = getattr(mn, manager)
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
        # PUT to /v2/databases/$DATABASE_ID/migrate return 202 with empty body
        elif response.status_code == httpx.codes.ACCEPTED and response.content == b"":
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
            self._process_response(res)
            response = res.json()
            result += response[key]

        return result


class AsyncClient(BaseClient):

    account: t.Optional[mn.AsyncAccountManager] = None
    actions: t.Optional[mn.AsyncActionsManager] = None
    cdn_endpoints: t.Optional[mn.AsyncCDNEndpointsManager] = None
    certificates: t.Optional[mn.AsyncCertificatesManager] = None
    databases: t.Optional[mn.AsyncDatabasesManager] = None
    domains: t.Optional[mn.AsyncDomainsManager] = None
    droplets: t.Optional[mn.AsyncDropletsManager] = None
    firewalls: t.Optional[mn.AsyncFirewallsManager] = None
    floating_ips: t.Optional[mn.AsyncFloatingIPsManager] = None
    images: t.Optional[mn.AsyncImagesManager] = None
    invoices: t.Optional[mn.AsyncInvoicesManager] = None
    kubernetes: t.Optional[mn.AsyncKubernetesManager] = None
    load_balancers: t.Optional[mn.AsyncLoadBalancersManager] = None
    projects: t.Optional[mn.AsyncProjectsManager] = None
    regions: t.Optional[mn.AsyncRegionsManager] = None
    registry: t.Optional[mn.AsyncRegistryManager] = None
    snapshots: t.Optional[mn.AsyncSnapshotsManager] = None
    ssh_keys: t.Optional[mn.AsyncSSHKeysManager] = None
    tags: t.Optional[mn.AsyncTagsManager] = None
    volumes: t.Optional[mn.AsyncVolumesManager] = None
    vpcs: t.Optional[mn.AsyncVPCsManager] = None

    def _load_managers(self) -> None:
        for manager in mn.__async_managers__:
            klass = getattr(mn, manager)
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
        # PUT to /v2/databases/$DATABASE_ID/migrate return 202 with empty body
        elif response.status_code == httpx.codes.ACCEPTED and response.content == b"":
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
            self._process_response(res)
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

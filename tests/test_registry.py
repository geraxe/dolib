import pytest
from httpx import HTTPStatusError

from dolib.client import AsyncClient, Client
from dolib.models import Registry


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_registry(client: Client) -> None:
    registry = Registry(
        name="dolib-test-registry",
        subscription_tier_slug="basic",
    )

    # create registry
    with pytest.raises(
        DeprecationWarning,
        match="This function is deprecated. Use registry.configure instead.",
    ):
        created_registry = client.registry.create(registry)

    created_registry, created_subscription = client.registry.configure(registry)

    # get registry
    registry = client.registry.get()
    assert isinstance(created_registry, Registry)

    # get subscription
    subscription = client.registry.subscription()
    assert isinstance(subscription, Registry.Subscription)

    # get docker credentials
    cred = client.registry.docker_credentials()
    assert isinstance(cred, dict)
    cred = client.registry.docker_credentials(read_write=True, expiry_seconds=600)
    assert isinstance(cred, dict)

    # validate
    with pytest.raises(HTTPStatusError):
        client.registry.validate_name(name="test", subscription_tier_slug="basic")

    repositories = client.registry.repositories(name=registry.name)

    tags = client.registry.repository_tags(
        name=registry.name, repository_name=repositories[0].name
    )
    assert isinstance(tags, list)
    assert isinstance(tags[0], Registry.Repository.Tag)

    client.registry.delete_tag(
        name=registry.name, repository_name=repositories[0].name, tag=tags[0].tag
    )
    client.registry.delete_manifest(
        name=registry.name,
        repository_name=repositories[0].name,
        manifest=tags[0].manifest_digest,
    )

    client.registry.start_garbage_collection(name=registry.name)
    with pytest.raises(HTTPStatusError):
        client.registry.start_garbage_collection(
            name=registry.name, collection_type="untagged manifests only"
        )

    gc = client.registry.garbage_collection(name=registry.name)
    assert isinstance(gc, Registry.GarbageCollection)

    # delete registry
    client.registry.delete(registry=created_registry)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_registry(async_client: AsyncClient) -> None:
    registry = Registry(
        name="dolib-test-registry",
        subscription_tier_slug="basic",
    )

    # create registry
    with pytest.raises(
        DeprecationWarning,
        match="This function is deprecated. Use registry.configure instead.",
    ):
        created_registry = await async_client.registry.create(registry)

    created_registry, created_subscription = await async_client.registry.configure(
        registry
    )

    # get registry
    registry = await async_client.registry.get()
    assert isinstance(created_registry, Registry)

    # get subscription
    subscription = await async_client.registry.subscription()
    assert isinstance(subscription, Registry.Subscription)

    # get docker credentials
    cred = await async_client.registry.docker_credentials()
    assert isinstance(cred, dict)
    cred = await async_client.registry.docker_credentials(
        read_write=True, expiry_seconds=600
    )
    assert isinstance(cred, dict)

    # validate
    with pytest.raises(HTTPStatusError):
        await async_client.registry.validate_name(
            name="test", subscription_tier_slug="basic"
        )

    repositories = await async_client.registry.repositories(name=registry.name)

    tags = await async_client.registry.repository_tags(
        name=registry.name, repository_name=repositories[0].name
    )
    assert isinstance(tags, list)
    assert isinstance(tags[0], Registry.Repository.Tag)

    await async_client.registry.delete_tag(
        name=registry.name, repository_name=repositories[0].name, tag=tags[0].tag
    )
    await async_client.registry.delete_manifest(
        name=registry.name,
        repository_name=repositories[0].name,
        manifest=tags[0].manifest_digest,
    )

    await async_client.registry.start_garbage_collection(name=registry.name)
    with pytest.raises(HTTPStatusError):
        await async_client.registry.start_garbage_collection(
            name=registry.name, collection_type="untagged manifests only"
        )

    gc = await async_client.registry.garbage_collection(name=registry.name)
    assert isinstance(gc, Registry.GarbageCollection)

    # delete registry
    await async_client.registry.delete(registry=created_registry)

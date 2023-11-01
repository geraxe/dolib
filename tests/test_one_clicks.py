import pytest

from dolib.client import AsyncClient, Client


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_one_clicks(client: Client) -> None:
    # list one click app
    apps = client.one_clicks.all()
    apps_count = len(apps)
    assert apps_count > 0

    # empty filtered app
    empty_type_apps = client.one_clicks.filter()
    assert len(apps) == len(empty_type_apps)

    # filter one click app
    filtered_apps = client.one_clicks.filter(app_type="droplet")
    assert isinstance(filtered_apps, list)
    assert len(filtered_apps) > 0
    for app in filtered_apps:
        assert app.type == "droplet"


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_one_clicks(async_client: AsyncClient) -> None:
    # list one click app
    apps = await async_client.one_clicks.all()
    apps_count = len(apps)
    assert apps_count > 0

    # empty filtered app
    empty_type_apps = await async_client.one_clicks.filter()
    assert len(apps) == len(empty_type_apps)

    # filter one click app
    filtered_apps = await async_client.one_clicks.filter(app_type="droplet")
    assert isinstance(filtered_apps, list)
    assert len(filtered_apps) > 0
    for app in filtered_apps:
        assert app.type == "droplet"

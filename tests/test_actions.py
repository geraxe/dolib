import pytest

from dolib.client import AsyncClient, Client


@pytest.mark.vcr
@pytest.mark.block_network()
def test_actions(client: Client) -> None:

    # list actions
    actions = client.actions.all()
    actions_count = len(actions)
    assert actions_count > 0

    # read action
    action = client.actions.get(str(actions[0].id))
    assert action.id == actions[0].id


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_actions(async_client: AsyncClient) -> None:

    # list actions
    actions = await async_client.actions.all()
    actions_count = len(actions)
    assert actions_count > 0

    # read action
    action = await async_client.actions.get(str(actions[0].id))
    assert action.id == actions[0].id

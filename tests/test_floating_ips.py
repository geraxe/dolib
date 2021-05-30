import pytest
from httpx import HTTPStatusError

from dolib.client import AsyncClient, Client
from dolib.models import Action, FloatingIP


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_floating_ips(client: Client) -> None:
    floating_ip = FloatingIP(region="fra1")

    # create floating_ip
    created_floating_ip = client.floating_ips.create(floating_ip)
    assert isinstance(created_floating_ip, FloatingIP)
    assert created_floating_ip.ip is not None

    droplet = client.droplets.all()[-1]

    # create droplet floating ip
    droplet_floating_ip = FloatingIP(droplet=droplet)
    created_droplet_floating_ip = client.floating_ips.create(droplet_floating_ip)
    assert isinstance(created_droplet_floating_ip, FloatingIP)
    assert created_droplet_floating_ip.ip is not None

    # create empty floating ip
    with pytest.raises(HTTPStatusError):
        client.floating_ips.create(FloatingIP())

    # list floating_ips
    floating_ips = client.floating_ips.all()
    assert len(floating_ips) > 0

    # read floating_ip
    read_floating_ip = client.floating_ips.get(created_floating_ip.ip)
    assert read_floating_ip.ip == created_floating_ip.ip
    assert isinstance(read_floating_ip, FloatingIP)

    # assign
    assign_action = client.floating_ips.assign(read_floating_ip.ip, droplet=droplet)
    assert isinstance(assign_action, Action)
    assert assign_action.status == "in-progress"

    # unassign
    unassign_action = client.floating_ips.unassign(read_floating_ip.ip)
    assert isinstance(unassign_action, Action)
    assert unassign_action.status == "in-progress"

    # list actions
    actions = client.floating_ips.actions(created_floating_ip.ip)
    assert len(actions) > 0

    # get action
    action = client.floating_ips.action(created_floating_ip.ip, actions[0].id)
    assert action.id == actions[0].id

    # delete floating_ip
    client.floating_ips.delete(ip=created_floating_ip)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_floating_ips(async_client: AsyncClient) -> None:
    floating_ip = FloatingIP(region="fra1")

    # create floating_ip
    created_floating_ip = await async_client.floating_ips.create(floating_ip)
    assert isinstance(created_floating_ip, FloatingIP)
    assert created_floating_ip.ip is not None

    droplet = (await async_client.droplets.all())[-1]

    # create droplet floating ip
    droplet_floating_ip = FloatingIP(droplet=droplet)
    created_droplet_floating_ip = await async_client.floating_ips.create(
        droplet_floating_ip
    )
    assert isinstance(created_droplet_floating_ip, FloatingIP)
    assert created_droplet_floating_ip.ip is not None

    # create empty floating ip
    with pytest.raises(HTTPStatusError):
        await async_client.floating_ips.create(FloatingIP())

    # list floating_ips
    floating_ips = await async_client.floating_ips.all()
    assert len(floating_ips) > 0

    # read floating_ip
    read_floating_ip = await async_client.floating_ips.get(created_floating_ip.ip)
    assert read_floating_ip.ip == created_floating_ip.ip
    assert isinstance(read_floating_ip, FloatingIP)

    # assign
    assign_action = await async_client.floating_ips.assign(
        read_floating_ip.ip, droplet=droplet
    )
    assert isinstance(assign_action, Action)
    assert assign_action.status == "in-progress"

    # unassign
    unassign_action = await async_client.floating_ips.unassign(read_floating_ip.ip)
    assert isinstance(unassign_action, Action)
    assert unassign_action.status == "in-progress"

    # list actions
    actions = await async_client.floating_ips.actions(created_floating_ip.ip)
    assert len(actions) > 0

    # get action
    action = await async_client.floating_ips.action(
        created_floating_ip.ip, actions[0].id
    )
    assert action.id == actions[0].id

    # delete floating_ip
    await async_client.floating_ips.delete(ip=created_floating_ip)

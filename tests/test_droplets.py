import pytest
from httpx import HTTPStatusError

from dolib.client import AsyncClient, Client
from dolib.models import Action, Droplet


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_droplets(client: Client) -> None:
    droplet = Droplet(
        name="dolib-droplet",
        region="fra1",
        size="s-1vcpu-1gb",
        image="ubuntu-18-04-x64",
    )

    # create droplet
    created_droplet = client.droplets.create(droplet=droplet)
    assert created_droplet.id is not None

    # read droplet
    read_droplet = client.droplets.get(str(created_droplet.id))
    assert read_droplet.id == created_droplet.id

    # list droplets
    droplets = client.droplets.all()
    droplets_count = len(droplets)
    assert droplets_count > 0

    # filter droplets
    droplets = client.droplets.filter()
    filtered = client.droplets.filter(tag_name="dolib")
    assert isinstance(filtered, list)

    # neighbors droplets
    neigbors = client.droplets.neighbors(str(created_droplet.id))
    assert isinstance(neigbors, list)

    # kernels
    kernels = client.droplets.kernels(str(created_droplet.id))
    assert isinstance(kernels, list)

    # snapshots
    snapshots = client.droplets.snapshots(str(created_droplet.id))
    assert isinstance(snapshots, list)

    # actions
    actions = client.droplets.actions(str(created_droplet.id))
    assert isinstance(actions, list)
    actions_count = len(actions)
    assert actions_count > 0
    action = actions[0]

    # get action
    action = client.droplets.action(str(created_droplet.id), actions[0].id)
    assert action.status == "completed"

    # sizes
    sizes = client.droplets.sizes()
    assert isinstance(sizes, list)

    # action enable_backup
    eb_action = client.droplets.enable_backups(str(created_droplet.id))
    assert isinstance(eb_action, Action)

    # action disable_backup
    db_action = client.droplets.disable_backups(str(created_droplet.id))
    assert isinstance(db_action, Action)

    # action reboot
    rb_action = client.droplets.reboot(str(created_droplet.id))
    assert isinstance(rb_action, Action)
    assert rb_action.status == "in-progress"

    # action power_cycle
    pc_action = client.droplets.power_cycle(str(created_droplet.id))
    assert isinstance(pc_action, Action)
    assert pc_action.status == "in-progress"

    # action shutdown
    sd_action = client.droplets.shutdown(str(created_droplet.id))
    assert isinstance(sd_action, Action)
    assert sd_action.status == "in-progress"

    # action power_off
    poff_action = client.droplets.power_off(str(created_droplet.id))
    assert isinstance(poff_action, Action)
    assert poff_action.status == "in-progress"

    # action power_on
    pon_action = client.droplets.power_on(str(created_droplet.id))
    assert isinstance(pon_action, Action)
    assert pon_action.status == "in-progress"

    # action password_reset
    pr_action = client.droplets.password_reset(str(created_droplet.id))
    assert isinstance(pr_action, Action)
    assert pr_action.status == "in-progress"

    # action rename
    rn_action = client.droplets.rename(
        str(created_droplet.id), name="dolib-droplet-renamed"
    )
    assert isinstance(rn_action, Action)
    assert rn_action.status == "in-progress"

    # action change_kernel
    with pytest.raises(HTTPStatusError):
        client.droplets.change_kernel(str(created_droplet.id), kernel=None)
    ck_action = client.droplets.change_kernel(str(created_droplet.id), kernel=1)
    assert isinstance(ck_action, Action)
    assert ck_action.status == "in-progress"

    # action enable_ipv6
    eipv6_action = client.droplets.enable_ipv6(str(created_droplet.id))
    assert isinstance(eipv6_action, Action)
    assert rn_action.status == "in-progress"

    # action enable private networking
    with pytest.raises(DeprecationWarning):
        client.droplets.enable_private_networking(str(created_droplet.id))

    # make actions by tag
    tag_actions = client.droplets.tag_action("test", "enable_ipv6")
    assert isinstance(tag_actions, list)

    # action snapshot
    nnss_action = client.droplets.snapshot(str(created_droplet.id))
    assert isinstance(nnss_action, Action)
    assert nnss_action.status == "in-progress"

    ss_action = client.droplets.snapshot(str(created_droplet.id), "test-snapshot")
    assert isinstance(ss_action, Action)
    assert ss_action.status == "in-progress"

    # action restore
    rs_action = client.droplets.restore(str(created_droplet.id), snapshots[0].id)
    assert isinstance(rs_action, Action)
    assert rs_action.status == "in-progress"

    # action rebuild
    rebuild_action = client.droplets.rebuild(
        str(created_droplet.id), "ubuntu-18-04-x64"
    )
    assert isinstance(rebuild_action, Action)
    assert rebuild_action.status == "in-progress"

    # action resize
    resize_action = client.droplets.resize(str(created_droplet.id), "s-2vcpu-2gb")
    assert isinstance(resize_action, Action)
    assert resize_action.status == "in-progress"

    # action resize with disk
    resize_action = client.droplets.resize(
        str(created_droplet.id), "s-2vcpu-2gb", disk=True
    )
    assert isinstance(rs_action, Action)
    assert rs_action.status == "in-progress"

    # delete droplet
    client.droplets.delete(droplet=read_droplet)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_droplets(async_client: AsyncClient) -> None:
    droplet = Droplet(
        name="dolib-droplet",
        region="fra1",
        size="s-1vcpu-1gb",
        image="ubuntu-18-04-x64",
    )

    # create droplet
    created_droplet = await async_client.droplets.create(droplet=droplet)
    assert created_droplet.id is not None

    # read droplet
    read_droplet = await async_client.droplets.get(str(created_droplet.id))
    assert read_droplet.id == created_droplet.id

    # list droplets
    droplets = await async_client.droplets.all()
    droplets_count = len(droplets)
    assert droplets_count > 0

    # filter droplets
    droplets = await async_client.droplets.filter()
    filtered = await async_client.droplets.filter(tag_name="dolib")
    assert isinstance(filtered, list)

    # neighbors droplets
    neigbors = await async_client.droplets.neighbors(str(created_droplet.id))
    assert isinstance(neigbors, list)

    # kernels
    kernels = await async_client.droplets.kernels(str(created_droplet.id))
    assert isinstance(kernels, list)

    # snapshots
    snapshots = await async_client.droplets.snapshots(str(created_droplet.id))
    assert isinstance(snapshots, list)

    # actions
    actions = await async_client.droplets.actions(str(created_droplet.id))
    assert isinstance(actions, list)
    actions_count = len(actions)
    assert actions_count > 0
    action = actions[0]

    # get action
    action = await async_client.droplets.action(str(created_droplet.id), actions[0].id)
    assert action.status == "completed"

    # sizes
    sizes = await async_client.droplets.sizes()
    assert isinstance(sizes, list)

    # action enable_backup
    eb_action = await async_client.droplets.enable_backups(str(created_droplet.id))
    assert isinstance(eb_action, Action)

    # action disable_backup
    db_action = await async_client.droplets.disable_backups(str(created_droplet.id))
    assert isinstance(db_action, Action)

    # action reboot
    rb_action = await async_client.droplets.reboot(str(created_droplet.id))
    assert isinstance(rb_action, Action)
    assert rb_action.status == "in-progress"

    # action power_cycle
    pc_action = await async_client.droplets.power_cycle(str(created_droplet.id))
    assert isinstance(pc_action, Action)
    assert pc_action.status == "in-progress"

    # action shutdown
    sd_action = await async_client.droplets.shutdown(str(created_droplet.id))
    assert isinstance(sd_action, Action)
    assert sd_action.status == "in-progress"

    # action power_off
    poff_action = await async_client.droplets.power_off(str(created_droplet.id))
    assert isinstance(poff_action, Action)
    assert poff_action.status == "in-progress"

    # action power_on
    pon_action = await async_client.droplets.power_on(str(created_droplet.id))
    assert isinstance(pon_action, Action)
    assert pon_action.status == "in-progress"

    # action password_reset
    pr_action = await async_client.droplets.password_reset(str(created_droplet.id))
    assert isinstance(pr_action, Action)
    assert pr_action.status == "in-progress"

    # action rename
    rn_action = await async_client.droplets.rename(
        str(created_droplet.id), name="dolib-droplet-renamed"
    )
    assert isinstance(rn_action, Action)
    assert rn_action.status == "in-progress"

    # action change_kernel
    with pytest.raises(HTTPStatusError):
        await async_client.droplets.change_kernel(str(created_droplet.id), kernel=None)
    ck_action = await async_client.droplets.change_kernel(
        str(created_droplet.id), kernel=1
    )
    assert isinstance(ck_action, Action)
    assert ck_action.status == "in-progress"

    # action enable_ipv6
    eipv6_action = await async_client.droplets.enable_ipv6(str(created_droplet.id))
    assert isinstance(eipv6_action, Action)
    assert rn_action.status == "in-progress"

    # action enable private networking
    with pytest.raises(DeprecationWarning):
        await async_client.droplets.enable_private_networking(str(created_droplet.id))

    # make actions by tag
    tag_actions = await async_client.droplets.tag_action("test", "enable_ipv6")
    assert isinstance(tag_actions, list)

    # action snapshot
    nnss_action = await async_client.droplets.snapshot(str(created_droplet.id))
    assert isinstance(nnss_action, Action)
    assert nnss_action.status == "in-progress"

    ss_action = await async_client.droplets.snapshot(
        str(created_droplet.id), "test-snapshot"
    )
    assert isinstance(ss_action, Action)
    assert ss_action.status == "in-progress"

    # action restore
    rs_action = await async_client.droplets.restore(
        str(created_droplet.id), snapshots[0].id
    )
    assert isinstance(rs_action, Action)
    assert rs_action.status == "in-progress"

    # action rebuild
    rebuild_action = await async_client.droplets.rebuild(
        str(created_droplet.id), "ubuntu-18-04-x64"
    )
    assert isinstance(rebuild_action, Action)
    assert rebuild_action.status == "in-progress"

    # action resize
    resize_action = await async_client.droplets.resize(
        str(created_droplet.id), "s-2vcpu-2gb"
    )
    assert isinstance(resize_action, Action)
    assert resize_action.status == "in-progress"

    # action resize with disk
    resize_action = await async_client.droplets.resize(
        str(created_droplet.id), "s-2vcpu-2gb", disk=True
    )
    assert isinstance(rs_action, Action)
    assert rs_action.status == "in-progress"

    # delete droplet
    await async_client.droplets.delete(droplet=read_droplet)

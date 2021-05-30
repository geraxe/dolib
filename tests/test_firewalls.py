import pytest

from dolib.client import AsyncClient, Client
from dolib.models import Firewall, FirewallTargets


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_firewalls(client: Client) -> None:
    fw = Firewall(
        name="test",
        inbound_rules=[
            Firewall.InboundRule(
                protocol="tcp",
                ports="80",
                sources=FirewallTargets(addresses=["0.0.0.0/0"]),
            )
        ],
    )

    # create firewall
    created_fw = client.firewalls.create(fw)
    assert isinstance(created_fw, Firewall)
    assert created_fw.id is not None

    # list firewalls
    fws = client.firewalls.all()
    assert len(fws) > 0

    # read firewall
    read_fw = client.firewalls.get(str(fws[0].id))
    assert read_fw.id == fws[0].id
    assert isinstance(read_fw, Firewall)

    # update firewall
    read_fw.tags = ["test"]
    updated_fw = client.firewalls.update(read_fw)
    assert read_fw.tags == updated_fw.tags

    droplets = client.droplets.all()

    # add droplets
    client.firewalls.add_droplets(str(read_fw.id), droplet_ids=[d.id for d in droplets])

    # remove droplets
    client.firewalls.remove_droplets(
        str(read_fw.id), droplet_ids=[d.id for d in droplets]
    )

    # add tags
    client.firewalls.add_tags(str(read_fw.id), tags=["test"])

    # remove tags
    client.firewalls.remove_tags(str(read_fw.id), tags=["test"])

    in_rule = Firewall.InboundRule(
        protocol="tcp", ports="81", sources=FirewallTargets(addresses=["0.0.0.0/0"])
    )
    out_rule = Firewall.OutboundRule(
        protocol="tcp",
        ports="81",
        destinations=FirewallTargets(addresses=["0.0.0.0/0"]),
    )

    # add rules
    client.firewalls.add_rules(str(read_fw.id), inbound_rules=[in_rule])
    client.firewalls.add_rules(str(read_fw.id), outbound_rules=[out_rule])

    # remove rules
    client.firewalls.remove_rules(str(read_fw.id), inbound_rules=[in_rule])
    client.firewalls.remove_rules(str(read_fw.id), outbound_rules=[out_rule])

    # delete firewall
    client.firewalls.delete(firewall=read_fw)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_firewalls(async_client: AsyncClient) -> None:
    fw = Firewall(
        name="test",
        inbound_rules=[
            Firewall.InboundRule(
                protocol="tcp",
                ports="80",
                sources=FirewallTargets(addresses=["0.0.0.0/0"]),
            )
        ],
    )

    # create firewall
    created_fw = await async_client.firewalls.create(fw)
    assert isinstance(created_fw, Firewall)
    assert created_fw.id is not None

    # list firewalls
    fws = await async_client.firewalls.all()
    assert len(fws) > 0

    # read firewall
    read_fw = await async_client.firewalls.get(str(fws[0].id))
    assert read_fw.id == fws[0].id
    assert isinstance(read_fw, Firewall)

    # update firewall
    read_fw.tags = ["test"]
    updated_fw = await async_client.firewalls.update(read_fw)
    assert read_fw.tags == updated_fw.tags

    droplets = await async_client.droplets.all()

    # add droplets
    await async_client.firewalls.add_droplets(
        str(read_fw.id), droplet_ids=[d.id for d in droplets]
    )

    # remove droplets
    await async_client.firewalls.remove_droplets(
        str(read_fw.id), droplet_ids=[d.id for d in droplets]
    )

    # add tags
    await async_client.firewalls.add_tags(str(read_fw.id), tags=["test"])

    # remove tags
    await async_client.firewalls.remove_tags(str(read_fw.id), tags=["test"])

    in_rule = Firewall.InboundRule(
        protocol="tcp", ports="81", sources=FirewallTargets(addresses=["0.0.0.0/0"])
    )
    out_rule = Firewall.OutboundRule(
        protocol="tcp",
        ports="81",
        destinations=FirewallTargets(addresses=["0.0.0.0/0"]),
    )

    # add rules
    await async_client.firewalls.add_rules(str(read_fw.id), inbound_rules=[in_rule])
    await async_client.firewalls.add_rules(str(read_fw.id), outbound_rules=[out_rule])

    # remove rules
    await async_client.firewalls.remove_rules(str(read_fw.id), inbound_rules=[in_rule])
    await async_client.firewalls.remove_rules(
        str(read_fw.id), outbound_rules=[out_rule]
    )

    # delete firewall
    await async_client.firewalls.delete(firewall=read_fw)

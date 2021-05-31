import pytest

from dolib.client import AsyncClient, Client
from dolib.models import LoadBalancer


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_load_balancers(client: Client) -> None:
    load_balancer = LoadBalancer(
        name="dolib-test-loadbalancer",
        region="fra1",
        forwarding_rules=[
            LoadBalancer.ForwardingRule(
                entry_protocol="tcp",
                entry_port=80,
                target_protocol="tcp",
                target_port="8080",
            )
        ],
    )

    # create load balancer
    created_load_balancer = client.load_balancers.create(load_balancer)
    assert isinstance(created_load_balancer, LoadBalancer)
    assert created_load_balancer.id is not None

    # list load_balancers
    load_balancers = client.load_balancers.all()
    assert len(load_balancers) > 0

    # read load_balancer
    read_load_balancer = client.load_balancers.get(str(created_load_balancer.id))
    assert read_load_balancer.id == created_load_balancer.id
    assert isinstance(read_load_balancer, LoadBalancer)

    # update load balancer
    read_load_balancer.name = "dolib-test-loadbalancer-renamed"
    updated_load_balancer = client.load_balancers.update(read_load_balancer)
    read_load_balancer.region = "fra1"
    updated_load_balancer = client.load_balancers.update(read_load_balancer)
    assert updated_load_balancer.name == read_load_balancer.name

    droplet = client.droplets.all()[-1]

    # add droplets
    client.load_balancers.add_droplets(
        str(read_load_balancer.id), droplet_ids=[droplet.id]
    )

    # remove droplets
    client.load_balancers.remove_droplets(
        str(read_load_balancer.id), droplet_ids=[droplet.id]
    )

    # add rules
    rule = LoadBalancer.ForwardingRule(
        entry_protocol="tcp",
        entry_port=81,
        target_protocol="tcp",
        target_port="8081",
    )
    client.load_balancers.add_forwarding_rules(
        str(read_load_balancer.id), forwarding_rules=[rule]
    )

    # remove rules
    client.load_balancers.remove_forwarding_rules(
        str(read_load_balancer.id), forwarding_rules=[rule]
    )

    # delete load_balancer
    client.load_balancers.delete(load_balancer=created_load_balancer)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_load_balancers(async_client: AsyncClient) -> None:
    load_balancer = LoadBalancer(
        name="dolib-test-loadbalancer",
        region="fra1",
        forwarding_rules=[
            LoadBalancer.ForwardingRule(
                entry_protocol="tcp",
                entry_port=80,
                target_protocol="tcp",
                target_port="8080",
            )
        ],
    )

    # create load balancer
    created_load_balancer = await async_client.load_balancers.create(load_balancer)
    assert isinstance(created_load_balancer, LoadBalancer)
    assert created_load_balancer.id is not None

    # list load_balancers
    load_balancers = await async_client.load_balancers.all()
    assert len(load_balancers) > 0

    # read load_balancer
    read_load_balancer = await async_client.load_balancers.get(
        str(created_load_balancer.id)
    )
    assert read_load_balancer.id == created_load_balancer.id
    assert isinstance(read_load_balancer, LoadBalancer)

    # update load balancer
    read_load_balancer.name = "dolib-test-loadbalancer-renamed"
    updated_load_balancer = await async_client.load_balancers.update(read_load_balancer)
    read_load_balancer.region = "fra1"
    updated_load_balancer = await async_client.load_balancers.update(read_load_balancer)
    assert updated_load_balancer.name == read_load_balancer.name

    droplet = (await async_client.droplets.all())[-1]

    # add droplets
    await async_client.load_balancers.add_droplets(
        str(read_load_balancer.id), droplet_ids=[droplet.id]
    )

    # remove droplets
    await async_client.load_balancers.remove_droplets(
        str(read_load_balancer.id), droplet_ids=[droplet.id]
    )

    # add rules
    rule = LoadBalancer.ForwardingRule(
        entry_protocol="tcp",
        entry_port=81,
        target_protocol="tcp",
        target_port="8081",
    )
    await async_client.load_balancers.add_forwarding_rules(
        str(read_load_balancer.id), forwarding_rules=[rule]
    )

    # remove rules
    await async_client.load_balancers.remove_forwarding_rules(
        str(read_load_balancer.id), forwarding_rules=[rule]
    )

    # delete load_balancer
    await async_client.load_balancers.delete(load_balancer=created_load_balancer)

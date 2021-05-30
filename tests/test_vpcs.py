import pytest

from dolib.client import AsyncClient, Client
from dolib.models import VPC


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_vpcs(client: Client) -> None:
    vpc = VPC(
        name="dolib-test-vpc",
        region="fra1",
    )

    # create vpc
    created_vpc = client.vpcs.create(vpc)
    assert isinstance(created_vpc, VPC)
    assert created_vpc.id is not None

    # list vpcs
    vpcs = client.vpcs.all()
    assert len(vpcs) > 0

    # read vpc
    read_vpc = client.vpcs.get(str(created_vpc.id))
    assert read_vpc.id == created_vpc.id
    assert isinstance(read_vpc, VPC)

    # update vpc
    created_vpc.name = "dolib-test-vpc-renamed"
    updated_vpc = client.vpcs.update(created_vpc)
    assert created_vpc.name == updated_vpc.name

    # get members
    members = client.vpcs.members(str(created_vpc.id))
    assert isinstance(members, list)

    # delete vpc
    client.vpcs.delete(vpc=created_vpc)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_vpcs(async_client: AsyncClient) -> None:
    vpc = VPC(
        name="dolib-test-vpc",
        region="fra1",
    )

    # create vpc
    created_vpc = await async_client.vpcs.create(vpc)
    assert isinstance(created_vpc, VPC)
    assert created_vpc.id is not None

    # list vpcs
    vpcs = await async_client.vpcs.all()
    assert len(vpcs) > 0

    # read vpc
    read_vpc = await async_client.vpcs.get(str(created_vpc.id))
    assert read_vpc.id == created_vpc.id
    assert isinstance(read_vpc, VPC)

    # update vpc
    created_vpc.name = "dolib-test-vpc-renamed"
    updated_vpc = await async_client.vpcs.update(created_vpc)
    assert created_vpc.name == updated_vpc.name

    # get members
    members = await async_client.vpcs.members(str(created_vpc.id))
    assert isinstance(members, list)

    # delete vpc
    await async_client.vpcs.delete(vpc=created_vpc)

import pytest

from dolib.client import AsyncClient, Client
from dolib.models import Domain


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_domains(client: Client) -> None:
    domain = Domain(name="test.dolib.io")

    # create domain
    created_domain = client.domains.create(domain=domain)
    assert created_domain.name == "test.dolib.io"

    # read domain
    read_domain = client.domains.get(name=domain.name)
    assert read_domain.name == domain.name
    assert read_domain.ttl > 0
    assert len(read_domain.zone_file) > 0

    # list domains
    domains = client.domains.all()
    assert len(domains) > 0

    # create domain record
    record = Domain.Record(type="A", name="@", data="8.8.8.8")
    record = client.domains.create_record(name=domain.name, record=record)
    assert record.id > 0
    assert record.ttl == 1800

    # update domain record
    record.name = "test"
    record.ttl = 60
    record = client.domains.update_record(name=domain.name, record=record)
    assert record.ttl == 60
    assert record.name == "test"

    # read domain records
    records = client.domains.records(name=domain.name)
    len_records = len(records)
    assert len_records > 0
    filtered_records = client.domains.records(
        name=domain.name, record_name="test.test.dolib.io", record_type="A"
    )
    assert len(filtered_records) == 1

    # delete domain record
    client.domains.delete_record(name=domain.name, record=record)

    # delete domain
    client.domains.delete(domain=created_domain)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_domains(async_client: AsyncClient) -> None:
    domain = Domain(name="test.dolib.io")

    # create domain
    created_domain = await async_client.domains.create(domain=domain)
    assert created_domain.name == "test.dolib.io"

    # read domain
    read_domain = await async_client.domains.get(name=domain.name)
    assert read_domain.name == domain.name
    assert read_domain.ttl > 0
    assert len(read_domain.zone_file) > 0

    # list domains
    domains = await async_client.domains.all()
    assert len(domains) > 0

    # create domain record
    record = Domain.Record(type="A", name="@", data="8.8.8.8")
    record = await async_client.domains.create_record(name=domain.name, record=record)
    assert record.id > 0
    assert record.ttl == 1800

    # update domain record
    record.name = "test"
    record.ttl = 60
    record = await async_client.domains.update_record(name=domain.name, record=record)
    assert record.ttl == 60
    assert record.name == "test"

    # read domain records
    records = await async_client.domains.records(name=domain.name)
    len_records = len(records)
    assert len_records > 0
    filtered_records = await async_client.domains.records(
        name=domain.name, record_name="test.test.dolib.io", record_type="A"
    )
    assert len(filtered_records) == 1

    # delete domain record
    await async_client.domains.delete_record(name=domain.name, record=record)

    # delete domain
    await async_client.domains.delete(domain=created_domain)

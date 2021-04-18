import pytest

from dolib.client import Client
from dolib.models import Domain


@pytest.mark.vcr()
@pytest.mark.block_network()
def test_crud_domain() -> None:
    client = Client(token="fake_token")

    domain = Domain(name="test.dolib.io")

    # create domain
    domain = client.domains.create(domain=domain)
    assert domain.name == "test.dolib.io"

    # read domain
    domain = client.domains.get(name=domain.name)
    assert domain.name == "test.dolib.io"
    assert domain.ttl > 0
    assert len(domain.zone_file) > 0

    # delete domain
    client.domains.delete(domain=domain)


@pytest.mark.vcr()
@pytest.mark.block_network()
def test_crud_domain_records() -> None:
    client = Client(token="fake_token")

    domain = Domain(name="test-records.dolib.io")

    # create domain
    domain = client.domains.create(domain=domain)
    assert domain.name == "test-records.dolib.io"

    # read domain records
    records = client.domains.records(name=domain.name)
    len_records = len(records)
    assert len_records > 0

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

    # delete domain record
    client.domains.delete_record(name=domain.name, record=record)

    # delete domain
    client.domains.delete(domain=domain)

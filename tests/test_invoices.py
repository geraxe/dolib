import pytest
from dolib.client import Client


@pytest.mark.vcr()
@pytest.mark.block_network()
def test_crud_invoce() -> None:
    client = Client(token="fake_token")

    # list all invoces
    invoces = client.invoices.all()
    assert len(invoces) > 0

    # read invoice
    invoce = client.invoices.get(invoces[0].invoice_uuid)
    assert invoce.invoice_uuid == invoces[0].invoice_uuid

    # read items
    items = client.invoices.items(invoces[0].invoice_uuid)
    assert len(items) > 0

import pytest

from dolib.client import AsyncClient, Client
from dolib.models import Invoice


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_invoices(client: Client) -> None:

    # list invoices
    invoices = client.invoices.all()
    assert len(invoices) > 0

    # read invoice
    read_invoice = client.invoices.get(str(invoices[-1].invoice_uuid))
    assert read_invoice.invoice_uuid == invoices[-1].invoice_uuid
    assert isinstance(read_invoice, Invoice)

    # invoice items
    items = client.invoices.items(str(read_invoice.invoice_uuid))
    assert len(items) > 0
    assert isinstance(items[-1], Invoice.Item)

    # get pdf
    pdf = client.invoices.pdf(str(read_invoice.invoice_uuid))
    assert len(pdf) > 0

    # get csv
    csv = client.invoices.csv(str(read_invoice.invoice_uuid))
    assert len(csv) > 0


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_invoices(async_client: AsyncClient) -> None:
    # list invoices
    invoices = await async_client.invoices.all()
    assert len(invoices) > 0

    # read invoice
    read_invoice = await async_client.invoices.get(str(invoices[-1].invoice_uuid))
    assert read_invoice.invoice_uuid == invoices[-1].invoice_uuid
    assert isinstance(read_invoice, Invoice)

    # invoice items
    items = await async_client.invoices.items(str(read_invoice.invoice_uuid))
    assert len(items) > 0
    assert isinstance(items[-1], Invoice.Item)

    # get pdf
    pdf = await async_client.invoices.pdf(str(read_invoice.invoice_uuid))
    assert len(pdf) > 0

    # get csv
    csv = await async_client.invoices.csv(str(read_invoice.invoice_uuid))
    assert len(csv) > 0

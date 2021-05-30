import pytest

from dolib.client import AsyncClient, Client
from dolib.models import Certificate


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_certificates(client: Client) -> None:
    cert = Certificate(
        name="dolib-test",
        type="lets_encrypt",
        dns_names=["test.dolib"],
    )

    # create cert
    created_cert = client.certificates.create(cert)
    assert isinstance(created_cert, Certificate)
    assert created_cert.id is not None

    # list certificates
    certs = client.certificates.all()
    assert len(certs) > 0

    # read certificate
    read_cert = client.certificates.get(str(certs[0].id))
    assert read_cert.id == certs[0].id
    assert isinstance(read_cert, Certificate)

    # delete certificate
    client.certificates.delete(certificate=read_cert)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_certificates(async_client: AsyncClient) -> None:
    cert = Certificate(
        name="dolib-test",
        type="lets_encrypt",
        dns_names=["test.dolib"],
    )

    # create cert
    created_cert = await async_client.certificates.create(cert)
    assert isinstance(created_cert, Certificate)
    assert created_cert.id is not None

    # list certificates
    certs = await async_client.certificates.all()
    assert len(certs) > 0

    # read certificate
    read_cert = await async_client.certificates.get(str(certs[0].id))
    assert read_cert.id == certs[0].id
    assert isinstance(read_cert, Certificate)

    # delete certificate
    await async_client.certificates.delete(certificate=read_cert)

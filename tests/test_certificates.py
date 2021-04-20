import pytest

from dolib.client import Client
from dolib.models import Certificate


@pytest.mark.vcr()
@pytest.mark.block_network()
def test_crud_certificate() -> None:
    client = Client(token="fake_token")

    cert = Certificate(name="dolib", type="lets_encrypt", dns_names=["dolib.io"])

    # create certificate
    cert = client.certificates.create(cert)
    assert cert.id is not None

    # list all certificates
    certs = client.certificates.all()
    assert len(certs) > 0

    # read certificate
    read_cert = client.certificates.get(str(cert.id))
    assert read_cert.id == cert.id

    # delete certificate
    client.certificates.delete(certificate=cert)

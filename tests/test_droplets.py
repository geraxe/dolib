import pytest

from dolib.client import Client
from dolib.models import Droplet


@pytest.mark.vcr
# @pytest.mark.block_network()
def test_crud_droplets() -> None:
    client = Client(token="fake_token")
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

    # delete droplet
    client.droplets.delete(droplet=read_droplet)

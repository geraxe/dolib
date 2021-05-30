import pytest

from dolib.client import AsyncClient, Client
from dolib.models import SSHKey


@pytest.mark.vcr
@pytest.mark.block_network()
def test_crud_ssh_keys(client: Client) -> None:
    key = SSHKey(
        name="dolib-test-key",
        public_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxLM1QBOln7SXu5mfjbMqm"
        "oP2Tnws3U/lIZfxerMGSGuRPSd1uoYAqcZZpz3hGsQJY092BqLXDnEwl3WiJTAtlX7HRku/"
        "TA/1WDa/8zdRq5ofbVZYceSR2xJXMxp8KvuVcnXK3a19IrFeW9KGAMIltIUVtXBvN1qLnk2"
        "9/cvQt6dn/iPqDyflxPKwWWd4czlTXs0oRikWySIft1d/PcCR49cj0yMTULLepGySFw5UAz"
        "GAkERAXWYjKzj85LVo2yaZYEzwfPe4RcmHnTRTYuIgqU0+sxNyvceiG9Wxuo2iaTa7OnLDz"
        "R3YV/VKJA1Rs+WAJFGHMrRltORF4NRGdmogV",
    )

    # create key
    created_key = client.ssh_keys.create(key)
    assert isinstance(created_key, SSHKey)
    assert created_key.id is not None

    # list keys
    keys = client.ssh_keys.all()
    assert len(keys) > 0

    # read key
    read_key = client.ssh_keys.get(str(keys[0].id))
    assert read_key.id == keys[0].id
    assert isinstance(read_key, SSHKey)

    # update project
    read_key.name = "dolib-test-key-renamed"
    updated_key = client.ssh_keys.update(read_key)
    assert isinstance(updated_key, SSHKey)
    assert read_key.name == updated_key.name

    # delete project
    client.ssh_keys.delete(key=read_key)


@pytest.mark.vcr
@pytest.mark.block_network()
@pytest.mark.asyncio
async def test_async_crud_ssh_keys(async_client: AsyncClient) -> None:
    key = SSHKey(
        name="dolib-test-key",
        public_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxLM1QBOln7SXu5mfjbMqm"
        "oP2Tnws3U/lIZfxerMGSGuRPSd1uoYAqcZZpz3hGsQJY092BqLXDnEwl3WiJTAtlX7HRku/"
        "TA/1WDa/8zdRq5ofbVZYceSR2xJXMxp8KvuVcnXK3a19IrFeW9KGAMIltIUVtXBvN1qLnk2"
        "9/cvQt6dn/iPqDyflxPKwWWd4czlTXs0oRikWySIft1d/PcCR49cj0yMTULLepGySFw5UAz"
        "GAkERAXWYjKzj85LVo2yaZYEzwfPe4RcmHnTRTYuIgqU0+sxNyvceiG9Wxuo2iaTa7OnLDz"
        "R3YV/VKJA1Rs+WAJFGHMrRltORF4NRGdmogV",
    )

    # create key
    created_key = await async_client.ssh_keys.create(key)
    assert isinstance(created_key, SSHKey)
    assert created_key.id is not None

    # list keys
    keys = await async_client.ssh_keys.all()
    assert len(keys) > 0

    # read key
    read_key = await async_client.ssh_keys.get(str(keys[0].id))
    assert read_key.id == keys[0].id
    assert isinstance(read_key, SSHKey)

    # update project
    read_key.name = "dolib-test-key-renamed"
    updated_key = await async_client.ssh_keys.update(read_key)
    assert isinstance(updated_key, SSHKey)
    assert read_key.name == updated_key.name

    # delete project
    await async_client.ssh_keys.delete(key=read_key)

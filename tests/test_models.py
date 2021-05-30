from dolib.models import Network, Region


def test_repr() -> None:
    network = Network(
        ip_address="1.1.1.1", netmask="255.255.255.0", gateway="1.1.1.254", type="test"
    )
    assert repr(network) == "Network(1.1.1.1/255.255.255.0 [test])"

    region = Region(name="test", slug="tst", sizes=[], available=True, features=[])
    assert repr(region) == "Region(tst)"

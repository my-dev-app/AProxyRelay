import pytest
from aproxyrelay import AProxyRelay


def test_parse_proxy_data():
    AProxyRelay([])

    with pytest.raises(TypeError):
        AProxyRelay()

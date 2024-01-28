import pytest
from aproxyrelay import AProxyRelay


def test_parse_proxy_data():
    proxy_relay = AProxyRelay([])

    assert proxy_relay._queue_result.qsize() == 0, 'Result QUEUE should start empty'

    with pytest.raises(TypeError):
        AProxyRelay()

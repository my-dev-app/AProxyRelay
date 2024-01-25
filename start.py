"""Example for enduser useage"""
from aproxyrelay import AProxyRelay

proxy_relay = AProxyRelay(targets=[], timeout=5, test_proxy=True, zone='us')
data = proxy_relay.start()
print(data.qsize())

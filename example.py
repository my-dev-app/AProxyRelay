# -*- mode: python ; coding: utf-8 -*-
from aproxyrelay import AProxyRelay

# Note: Duplicates will be removed by the library
targets = []

# Initialize proxy relay
proxy_relay = AProxyRelay(
    targets=targets,
    timeout=5,
    test_proxy=False,
    test_timeout=10,
    zone='DE',
)

# Fetch data
data = proxy_relay.start()

# Result Queue
print(data.qsize())

while not data.empty():
    content = data.get()
    print(content)

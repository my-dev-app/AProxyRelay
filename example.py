# -*- mode: python ; coding: utf-8 -*-
from aproxyrelay import AProxyRelay

# Note: Duplicates will be removed by the library
targets = [
    'https://gg.my-dev.app/api/v1/proxies/available?zone=us&anonimity=all&protocol=all&page=1&size=100&type=example',
    'https://gg.my-dev.app/api/v1/proxies/available?zone=de&anonimity=all&protocol=all&page=1&size=100&type=example',
    'https://gg.my-dev.app/api/v1/proxies/available?zone=nl&anonimity=all&protocol=all&page=1&size=100&type=example',
    'https://gg.my-dev.app/api/v1/proxies/available?zone=de&anonimity=all&protocol=all&page=1&size=100&type=example',
    'https://gg.my-dev.app/api/v1/proxies/available?zone=nl&anonimity=all&protocol=all&page=1&size=100&type=example',
]

# Initialize proxy relay
proxy_relay = AProxyRelay(
    targets=targets,
    timeout=5,
    test_proxy=True,
    test_timeout=10,
    zone='de',
)

# Fetch data
data = proxy_relay.start()

# Result Queue
print(data.qsize())

while not data.empty():
    content = data.get()
    print(content)

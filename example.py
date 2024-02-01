# -*- mode: python ; coding: utf-8 -*-
from aproxyrelay import AProxyRelay

# Note: Duplicates will be removed by the library
targets = [
    'https://gg.my-dev.app/api/v1/proxies/available?zone=US&anonimity=all&protocol=all&page=1&size=100&type=example',
    'https://gg.my-dev.app/api/v1/proxies/available?zone=DE&anonimity=all&protocol=all&page=1&size=100&type=example',
    'https://gg.my-dev.app/api/v1/proxies/available?zone=NL&anonimity=all&protocol=all&page=1&size=100&type=example',
    'https://gg.my-dev.app/api/v1/proxies/available?zone=CA&anonimity=all&protocol=all&page=1&size=100&type=example',
    'https://gg.my-dev.app/api/v1/proxies/available?zone=AU&anonimity=all&protocol=all&page=1&size=100&type=example',
]

# Initialize proxy relay
proxy_relay = AProxyRelay(
    targets=targets,
    timeout=5,
    test_proxy=True,
    test_timeout=10,
    zone='US',
)

# Fetch data
data = proxy_relay.start()

# Result Queue
print(data.qsize())

while not data.empty():
    content = data.get()
    print(content)

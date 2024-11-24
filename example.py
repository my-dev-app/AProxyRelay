# -*- mode: python ; coding: utf-8 -*-
from aproxyrelay import AProxyRelay

# Note: Duplicates will be removed by the library
targets = [
    'https://gg.my-dev.app/api/v1/proxies/available?zone=US&anonimity=all&protocol=all&page=1&size=100&type=example',
]

# Initialize proxy relay
proxy_relay = AProxyRelay(
    targets=targets,
    timeout=30,
    scrape=True,
    filter=True,
    zones=['us'],
    unpack=lambda data, target: data['results'],
    debug=False,
)

print(f'Proxies found: {proxy_relay.proxies.qsize()}')

# Fetch data
data = proxy_relay.start()

# Result Queue
print(data.qsize())

while not data.empty():
    content = data.get()
    print(content)

"""Example for enduser usage"""
from aproxyrelay import AProxyRelay

with open('test_targets.txt', 'r') as f:
    targets = [i.replace('\n', '') for i in f.readlines()]

proxy_relay = AProxyRelay(targets=targets, timeout=5, test_proxy=True, zone='us', steam=False)
data = proxy_relay.start()
print(data.qsize())

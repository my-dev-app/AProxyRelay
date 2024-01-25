```
   __      ____  ____  _____  _  _  _  _    ____  ____  __      __   _  _ 
  /__\    (  _ \(  _ \(  _  )( \/ )( \/ )  (  _ \( ___)(  )    /__\ ( \/ )
 /(__)\    )___/ )   / )(_)(  )  (  \  /    )   / )__)  )(__  /(__)\ \  / 
(__)(__)  (__)  (_)\_)(_____)(_/\_) (__)   (_)\_)(____)(____)(__)(__)(__) 

By undeƒined
-------------------------------------
```
An async request library which requests data by utilizing various proxy servers.

Automatically rotates bad proxy servers, preserves data which failed to request.
Makes scraping API's easy and fun. Written with `py-3.12.1`.


## Compiling to package

    python setup.py sdist bdist_wheel

The command above should compile the lib to a `dist` folder.


## Development dependencies
Make sure to run this command in a virtual environment

    pip install . && pip uninstall aproxyrelay -y

## Usage
"A Proxy Relay" does a couple of things for you.
- Asynchoriously fetch lists of free proxies and test them right away
- Puts data from various API's into an array to bypass API limiters

    """Example for enduser useage"""
    from aproxyrelay import AProxyRelay

    proxy_relay = AProxyRelay(targets=[
        'https://store.steampowered.com/api/appdetails?appids=1551360',
        'https://store.steampowered.com/api/appdetails?appids=2072450',
        'https://store.steampowered.com/api/appdetails?appids=1924360',
        'https://store.steampowered.com/api/appdetails?appids=1707870',
        'https://store.steampowered.com/api/appdetails?appids=1839880',
    ], timeout=5, test_proxy=True)
    data = proxy_relay.start()
    print(data)

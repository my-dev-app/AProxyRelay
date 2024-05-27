[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner2-direct.svg)](https://stand-with-ukraine.pp.ua)
---

```python
    #       ######                                ######                             
   # #      #     # #####   ####  #    # #   #    #     # ###### #        ##   #   # 
  #   #     #     # #    # #    #  #  #   # #     #     # #      #       #  #   # #  
 #     #    ######  #    # #    #   ##     #      ######  #####  #      #    #   #   
 #######    #       #####  #    #   ##     #      #   #   #      #      ######   #   
 #     #    #       #   #  #    #  #  #    #      #    #  #      #      #    #   #   
 #     #    #       #    #  ####  #    #   #      #     # ###### ###### #    #   #   
                                                                                     
By undeƒined
-------------------------------------
```
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/my-dev-app/proxy-relay/entrypoint.yaml?branch=development)
![PyPI - Version](https://img.shields.io/pypi/v/aproxyrelay)
![PyPI - Downloads](https://img.shields.io/pypi/dw/aproxyrelay)
![GitHub commits since latest release](https://img.shields.io/github/commits-since/my-dev-app/proxy-relay/latest)
![GitHub Repo stars](https://img.shields.io/github/stars/my-dev-app/proxy-relay?style=social)

[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)
[![Russian Warship Go Fuck Yourself](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/RussianWarship.svg)](https://stand-with-ukraine.pp.ua)

# AProxyRelay: An Async Request Library with Proxy Rotation

AProxyRelay is an asynchronous request library designed for easy data retrieval using various proxy servers. It seamlessly handles proxy rotation, preserves data that fails to be requested, and simplifies API scraping. The library is written in `Python 3.12.2`.

In addition, tested proxies will be shared with other people using this library. The more this library is utilized, the bigger the pool of available proxies.

Our scraper, used to obtain proxies, is highly modular and plug-and-play, making it easy to contribute to.

## Usage
AProxyRelay streamlines the process of making asynchronous requests with proxy servers. It offers the following features:
- Asynchronously fetches lists of free proxies from various sources based on the provided zone
- Tests and shares proxies with other users of the library
- Identifies and discards bad proxies, preserving data for failed target requests
- Bypasses API limiters in an asynchronous manner (for educational purpose)

### Example
```py
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
    scrape=True,
    filter=True,
    zones=['us'],
    unpack=lambda data, target: data['results'],
    debug=False,
)

# Fetch data
data = proxy_relay.start()

# Result Queue
print(data.qsize())

while not data.empty():
    content = data.get()
    print(content)

```

## A Proxy Relay: Installation
Simply run

    pip install aproxyrelay

### Parameters

| Parameters  | Type          | Function                                       | Description                                                  |
|-------------|---------------|------------------------------------------------|--------------------------------------------------------------|
| targets     | list[str]      | Target endpoints provided in an array           | Each endpoint will be requested with an available proxy. If a proxy is unavailable and the request fails, we store it in a queue and try it out with another proxy until we have data. |
| timeout     | int           | Allowed proxy timeout. **Defaults to 5**        | A proxy has to respond within the provided timeout to be considered valid. Otherwise, it will be discarded.                |
| scrape      | bool          | Indicator to utilize the proxy scraper. **Defaults to True** | The decision to scrape for proxies is determined by the value of this parameter. When set to True (default), the proxy scraper is used, which is slower but provides a broader range of proxies. When set to False, proxies are fetched from a single source, offering a faster but more limited selection. |
| filter      | bool          | Indicator for filtering bad proxies. **Defaults to True** | If set to True (default), the tool will test proxy connections before using them. This process might take a bit longer, but it ensures that the proxies are valid before utilization. |
| zones       | list[str]      | An array of proxy zones. **Defaults to ['US']**  | Sometimes it matters where the proxy is located. Each item in this list ensures the proxy is located in that specific zone, and requests made from the proxy are coming from the location provided. It acts like a whitelist for allowed proxy locations. |
| unpack      | lambda        | Anonymous function for unpacking data. **Defaults to `lambda data, target: data`** | When a request has been made to a target through a proxy and data has been fetched, this lambda method formats the result data before putting it into the result queue. **data** -> output from the target, **target** -> target URL. |
| debug       | bool          | Indicator which enables debug mode. **Defaults to False** | When true, additional logging will be printed to the terminal, enabling debug mode. |



## A Proxy Relay: Local Development
To install all library dependencies for local development, excluding the core code available locally, use the following command within a virtual environment:

    pip install -e .[dev]

This command installs dependencies and removes the core code of AProxyRelay from the virtual environment.


# Contribute to AProxyRelay

AProxyRelay encourages contributions to enhance its capabilities by allowing users to create custom scrapers. These scrapers are designed to fetch proxy data from different sources. The process is straightforward, and here's a guide to help you get started:

## Scraper Structure

AProxyRelay includes a dedicated folder named `scrapers`. Within this folder, each scraper, prefixed with `parser_`, inherits from the `parser.py` file. To provide you with a general understanding, here's an example of the `MainScraper` class:

```py
from queue import Queue

from .core import ScraperCore


class MainScraper(ScraperCore):
    def __init__(self) -> None:
        ScraperCore.__init__(self)
        self.zone = None

    @classmethod
    async def format_url(cls, url, *args, **kwargs) -> str:
        """Formats URL before scraping, let us adjust query parameters for each parser"""
        cls.zone = kwargs.get("zone", "us")
        new_url = f'{url}'
        return new_url

    @classmethod
    async def format_raw(cls, html: str):
        """Parse text/html pages, customized method for the parser of this website"""
        raise NotImplementedError('Format raw parser has not been implemented yet')

    @classmethod
    async def format_data(cls, data: dict, queue: Queue):
        """Data formatter, formats data and returns is back in the process Queue"""
        raise NotImplementedError('Form data parser has not been implemented yet')
```

## Creating your own Proxy Scraper

To contribute your own proxy scraper, follow these steps:

1. ### Create a new parser class inside the scrapers folder
    - Inherit from the `MainScraper`.
    - Overwrite the necessary methods required for scraping additional proxy servers.
2. ### Methods to Overwrite:
    - `format_url`: Manipulate the proxy list request URL before making a request, enabling adjustment of various query parameters.
    - `format_raw`: When the data obtained from the link is `txt/html`, this method should scrape the data and format it into workable data.
    - `format_data`: This method is triggered when the call to the proxy list returns a dictionary, or when format_raw has been completed.
3. ### Formatting Data:
    - Your goal is to format the data in the `format_data` method and place it into the provided Queue. The data should be structured as follows:
        ```python
        data = {
            "zone": "US",
            "method": "http",
            "anonymity": "anonymous",
            "protocol": "http",
            "port": "8080",
            "ip": "127.0.0.1",
        }
        queue.put(data)
        ```
4. ### Congratulations
    - If done correctly, congratulations! You've successfully created a new proxy parser for this library.
    - Add the targeted link and your scraper to `scrapers/__init__.py`.

Feel free to contribute, share your improvements, and expand the library's capabilities. Your efforts contribute to a growing pool of available proxies for the AProxyRelay community.

## Compiling to package
To compile the library into a package, use the following command after installing `requirements.txt`:

```sh
python setup.py sdist bdist_wheel
```

This will generate the package in the `dist` folder.

***Note: A custom version can be set with the environment variable `CUSTOM_VERSION`***

## Versioning
The version public on [PyPi](https://pypi.org/project/aproxyrelay/) contains a version number based on the pipeline builds and looks like:

    ` aproxyrelay 1.104.1rc7696232336 `

Breaking the version down:

-  `aproxyrelay`: The name of the package
-  `1`: Major version
-  `104`: Build number
-  `1`: Build retry number
-  `rc7696232336`: Random build number

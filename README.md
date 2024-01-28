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
# AProxyRelay: An Async Request Library with Proxy Rotation

AProxyRelay is an asynchronous request library designed for easy data retrieval using various proxy servers. It seamlessly handles proxy rotation, preserves data that fails to be requested, and simplifies API scraping. The library is written in `Python 3.12.1` but is compatible with projects utilizing `Python 3.11.2`.

In addition, tested proxies will be shared with other people using this library. The more this library is utilized, the bigger the pool of available proxies.

Our scraper, used to obtain proxies, is highly modular and plug-and-play, making it easy to contribute to.

## Compiling to package
To compile the library into a package, use the following command after installing `requirements.txt`:

```sh
python setup.py sdist bdist_wheel
```

This will generate the package in the `dist` folder.
Note: A version can be set with the environment variable `CUSTOM_VERSION`

## Usage
AProxyRelay streamlines the process of making asynchronous requests with proxy servers. It offers the following features:
- Asynchronously fetches lists of free proxies from various sources based on the provided zone
- Tests and shares proxies with other users of the library
- Identifies and discards bad proxies, preserving data for failed target requests
- Bypasses API limiters in an asynchronous manner (for educational purpose)

### Example
```py
from aproxyrelay import AProxyRelay

targets = [
    'https://some-website.com/api/app?id=1551360',
    'https://some-website.com/api/app?id=2072450',
    'https://some-website.com/api/app?id=1924360',
    'https://some-website.com/api/app?id=1707870',
    'https://some-website.com/api/app?id=1839880',
]

# Initialize proxy relay
proxy_relay = AProxyRelay(
    targets=targets,
    timeout=5,
    test_proxy=True,
    test_timeout=10,
    zone='us',
)

# Fetch data
data = proxy_relay.start()

# Result Queue
print(data.qsize())
```

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

    @classmethod
    async def format_url(cls, url, *args, **kwargs) -> str:
        """Formats URL before scraping, let us adjust query parameters for each parser"""
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
            "country": "US",
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

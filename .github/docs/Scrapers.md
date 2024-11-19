# Scrapers / Parsers

Parsers are located at `aproxyrelay/scrapers`.
A lot of core logic has been put away in the main class located in `aproxyrelay/scrapers/core.py`.

Each newly added scraper should be registered in `aproxyrelay/scrapers/__init__.py`.

The methods utilized within `aProxyRelay` are hard-coded.

## Setup a new scraper

1. Find a target website, each website might need a different way of fetching proxies. Keep that in mind.
2. register the url in `aproxyrelay/scrapers/__init__.py`
3. Make a new class which is registered to the URL added in the `__init__` file
4. Add the base of the scraper:
```py
# -*- mode: python ; coding: utf-8 -*-
"""
░░      ░░       ░░       ░░░      ░░  ░░░░  ░  ░░░░  ░       ░░        ░  ░░░░░░░░      ░░  ░░░░  ░
▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒▒  ▒▒  ▒▒  ▒▒▒▒  ▒  ▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒  ▒▒  ▒▒
▓  ▓▓▓▓  ▓       ▓▓       ▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓▓▓    ▓▓▓       ▓▓      ▓▓▓  ▓▓▓▓▓▓▓  ▓▓▓▓  ▓▓▓    ▓▓▓
█        █  ███████  ███  ██  ████  ██  ██  █████  ████  ███  ██  ███████  ███████        ████  ████
█  ████  █  ███████  ████  ██      ██  ████  ████  ████  ████  █        █        █  ████  ████  ████
By undeƒined
------------

Main parser example, other parsers can inherit from this class
"""
from queue import Queue

from .parser import MainScraper


class ParserExampleScraper(MainScraper):
    def __init__(self) -> None:
        MainScraper.__init__(self)

    @classmethod
    async def format_url(cls, url, *args, **kwargs) -> str:
        """Formats URL before scraping, let us adjust query parameters for each parser"""
        cls.zone = kwargs.get("zone", "us")
        return url.replace('country=UK', f'country={cls.zone.upper()}')

    # @classmethod
    # async def custom_request(cls, url, *args, **kwargs) -> requests:
    #     """
    #     Custom request for URL, only happens when this method is set in the class.
    #     If not, fallback to default lib request.
    #     """
    #     headers = {
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    #         "Accept": "*/*",
    #         "Accept-Language": "en-US,en;q=0.5",
    #         "Sec-Fetch-Dest": "empty",
    #         "Sec-Fetch-Mode": "cors",
    #         "Sec-Fetch-Site": "cross-site",
    #         "Priority": "u=4",
    #         "Referer": "https://proxiware.com/"
    #     }
    #     response = requests.get(url, headers=headers)
    #     return response

    @classmethod
    async def format_raw(cls, html: str) -> list:
        """Parse text/html pages, customized method for the parser of this website"""
        return html

    @classmethod
    async def format_data(cls, zone: str, data: dict, queue: Queue) -> None:
        """Data formatter, formats data and returns is back in the process Queue"""
        queue.put(data)
        return queue
```

## Class Breakdown

- `__init__`: Inherits and activates `MainScraper` class which hooks into the library
- `format_url`: Allows you to modify the URL before parsing. For example you could add the proxy zone
- `custom_request`: Some websites need a custom request, you can achieve this by modifing this method and returning a response. If this method is not set, the internal request class will manage the request for you.
- `format_raw`: Sometimes, instead of a nicely formatted JSON object, the data you work with is XML data for example. If that happens, this method is utilized to convert the data into a valid JSON object. (Which is up to you). See other existing parsers for examples.
- `format_data`: Your goal is to format the data in the `format_data` method and place it into the provided Queue. The data should be structured as follows:
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

## Test your changes

Run the unittests included in this library
```py
pytest
```

If all tests succeed, proceed with testing for flake8 violations

```py
flake8
```

When 0 violations have been made, proceed with submitting a Pull Request

## Submit a Pull Request
Once your PR has been merged, your parser will be included in the internal system which provided proxies.
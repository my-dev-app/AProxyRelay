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


class ParserProxyScrapeHttp(MainScraper):
    def __init__(self) -> None:
        MainScraper.__init__(self)

    @classmethod
    async def format_url(cls, url, *args, **kwargs) -> str:
        """Formats URL before scraping, let us adjust query parameters for each parser"""
        cls.zone = kwargs.get("zone", "us")
        return url.replace('country=NL', f'country={cls.zone.upper()}')

    @classmethod
    async def format_raw(cls, html: str) -> list:
        """Parse text/html pages, customized method for the parser of this website"""
        return [
            {
                'zone': cls.zone.upper(),
                'method': 'http',
                'anonymity': 'unknown',
                'protocol': 'http',
                'port': item.split(':')[1],
                'ip': item.split(':')[0],
            } for item in html.split('\r\n') if item
        ]

    @classmethod
    async def format_data(cls, zone: str, data: dict, queue: Queue) -> None:
        """Data formatter, formats data and returns is back in the process Queue"""
        queue.put(data)
        return queue

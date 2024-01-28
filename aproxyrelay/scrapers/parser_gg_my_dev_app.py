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


class ParserGGMyDevApp(MainScraper):
    def __init__(self) -> None:
        MainScraper.__init__(self)

    @classmethod
    async def format_url(cls, url, zone: str = 'us', *args, **kwargs) -> str:
        """Formats URL before scraping, let us adjust query parameters for each parser"""
        return url.replace('zone=nl', f'zone={zone.upper()}')

    @classmethod
    async def format_raw(cls, html: str) -> list:
        """Parse text/html pages, customized method for the parser of this website"""
        return html

    @classmethod
    async def format_data(cls, zone: str, data: dict, queue: Queue) -> None:
        """Data formatter, formats data and returns is back in the process Queue"""
        for item in data['results']:
            if item['zone'] == zone.upper():
                queue.put(item)
        return queue

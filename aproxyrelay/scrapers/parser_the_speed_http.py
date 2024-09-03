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


class ParserTheSpeedHTTPProxy(MainScraper):
    def __init__(self) -> None:
        MainScraper.__init__(self)
        self.zone = None

    @classmethod
    async def format_url(cls, url, *args, **kwargs) -> str:
        """Formats URL before scraping, let us adjust query parameters for each parser"""
        cls.zone = kwargs.get("country", "us")
        return url

    @classmethod
    async def format_raw(cls, html: str) -> list:
        """Parse text/html pages, customized method for the parser of this website"""
        result = []
        data = html.split('\n')
        for proxy in data:
            if proxy:
                protocol = 'http'
                ip = proxy.split(':')[0]
                port = proxy.split(':')[-1]
                result.append({
                    'zone': cls.zone.upper(),
                    'method': protocol,
                    'anonymity': 'unknown',
                    'protocol': protocol,
                    'port': port,
                    'ip': ip
                })
        return result

    @classmethod
    async def format_data(cls, zone: str, data: dict, queue: Queue) -> None:
        """Data formatter, formats data and returns is back in the process Queue"""
        queue.put(data)
        return queue

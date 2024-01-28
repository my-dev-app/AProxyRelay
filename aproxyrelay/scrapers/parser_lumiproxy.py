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


class ParserLumiProxy(MainScraper):
    def __init__(self) -> None:
        MainScraper.__init__(self)

    @classmethod
    async def format_url(cls, url, zone: str = 'us', *args, **kwargs) -> str:
        """Formats URL before scraping, let us adjust query parameters for each parser"""
        new_url = url.replace('country_code=nl', f'country_code={zone}')
        return new_url

    @classmethod
    async def format_data(cls, zone: str, data: dict, queue: Queue) -> None:
        """Data formatter, formats data and returns is back in the process Queue"""
        for item in data['data']['list']:
            if item['country_code'] == zone.upper():
                queue.put({
                    'country': item['name_en'],
                    'zone': item['country_code'],
                    'method': cls._get_protocol(item['protocol']),
                    'anonymity': 'transparent' if item['anonymity'] not in [1, 2] else 'anonymous',
                    'protocol': cls._get_protocol(item['protocol']),
                    'port': str(item['port']),
                    'ip': item['ip'],
                })
        return queue

    @classmethod
    def _get_protocol(cls, protocol: int) -> str:
        """Determine protocol based on API output"""
        prot = 'unknown'
        if protocol == 1 or protocol == 2:
            prot = 'http'
        elif protocol == 2:
            prot = 'https'
        elif protocol == 4:
            prot = 'Socks4'
        elif protocol == 8:
            prot = 'Socks5'
        return prot.lower()

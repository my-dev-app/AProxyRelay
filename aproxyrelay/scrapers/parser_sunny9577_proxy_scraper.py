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

import ast

from .parser import MainScraper


class ParserSunnyProxyScraper(MainScraper):
    def __init__(self) -> None:
        MainScraper.__init__(self)
        self.zone = None

    @classmethod
    async def format_url(cls, url, *args, **kwargs) -> str:
        """Formats URL before scraping, let us adjust query parameters for each parser"""
        cls.zone = kwargs.get("zone", "us")
        return url

    @classmethod
    def generate_method(cls, target_method) -> str:
        if 'socks4' in target_method.lower():
            return 'socks4'
        elif 'socks5' in target_method.lower():
            return 'socks5'
        elif 'http' in target_method.lower():
            return 'https'
        return 'unknown'

    @classmethod
    def generate_protocol(cls, target_protocol) -> str:
        if 'socks4' in target_protocol.lower():
            return 'socks4'
        elif 'socks5' in target_protocol.lower():
            return 'socks5'
        elif 'https' in target_protocol.lower():
            return 'https'
        elif 'http' in target_protocol.lower():
            return 'http'
        return 'unknown'

    @classmethod
    def generate_anonymity(cls, target_anonimity) -> str:
        if target_anonimity.lower() in (
            'anonymous',
            'elite',
        ):
            return 'anonymous'
        elif target_anonimity.lower() in (
            'transparent',
        ):
            return 'transparent'
        return 'unknown'

    @classmethod
    async def format_raw(cls, html: str) -> list:
        """Parse text/html pages, customized method for the parser of this website"""
        return [
            {
                'zone': cls.zone.upper(),
                'method': cls.generate_method(item['type']),
                'anonymity': cls.generate_anonymity(item['anonymity']),
                'protocol': cls.generate_protocol(item['type']),
                'port': item['port'],
                'ip': item['ip'],
            } for item in ast.literal_eval(html)
        ]

    @classmethod
    async def format_data(cls, zone: str, data: dict, queue: Queue) -> None:
        """Data formatter, formats data and returns is back in the process Queue"""
        queue.put(data)
        return queue
